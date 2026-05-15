import asyncio
import logging
import os
import re
import math
import hashlib
import aiohttp
from collections import Counter
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

# ================== CONFIG ==================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VT_API_KEY = os.getenv("VT_API_KEY")

# ================== LOG ==================
logging.basicConfig(level=logging.INFO)

# ================== BOT ==================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ================== ANALYZER ==================
def entropy(data):
    if not data:
        return 0
    c = Counter(data)
    n = len(data)
    return -sum((x/n)*math.log2(x/n) for x in c.values())

def analyze(data):
    score = 0
    e = entropy(data)

    if e > 7:
        score += 50
    elif e > 6:
        score += 20

    if b"powershell" in data.lower():
        score += 30

    if b"http" in data.lower():
        score += 10

    if score > 70:
        verdict = "⛔ ZARARLI"
    elif score > 30:
        verdict = "⚠️ SHUBHALI"
    else:
        verdict = "✅ XAVFSIZ"

    return verdict, score, round(e, 2)

# ================== VIRUSTOTAL ==================
async def check_hash(hash_str):
    if not VT_API_KEY:
        return "VT o‘chirilgan"

    url = f"https://www.virustotal.com/api/v3/files/{hash_str}"
    headers = {"x-apikey": VT_API_KEY}

    async with aiohttp.ClientSession() as s:
        async with s.get(url, headers=headers) as r:
            if r.status != 200:
                return "Topilmadi"
            data = await r.json()
            stats = data["data"]["attributes"]["last_analysis_stats"]
            return f"🔴 {stats['malicious']} | 🟡 {stats['suspicious']}"

# ================== COMMANDS ==================
@router.message(CommandStart())
async def start(msg: Message):
    await msg.answer("🛡 MalwareGuard ishlayapti!\nFayl yubor yoki /hash yoz")

@router.message(Command("hash"))
async def hash_cmd(msg: Message):
    parts = msg.text.split()
    if len(parts) < 2:
        return await msg.answer("Misol: /hash abc123")

    h = parts[1]
    res = await check_hash(h)
    await msg.answer(f"Natija:\n{res}")

# ================== FILE ==================
@router.message(lambda m: m.document)
async def file_handler(msg: Message):
    file = await bot.get_file(msg.document.file_id)
    data = await bot.download_file(file.file_path)

    content = data.read()

    verdict, score, ent = analyze(content)
    sha256 = hashlib.sha256(content).hexdigest()

    vt = await check_hash(sha256)

    text = f"""
📄 {msg.document.file_name}

{verdict}
Ball: {score}/100
Entropy: {ent}

VT: {vt}
SHA256:
{sha256}
"""

    await msg.answer(text)

# ================== RUN ==================
async def main():
    print("🚀 Bot ishga tushdi")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


