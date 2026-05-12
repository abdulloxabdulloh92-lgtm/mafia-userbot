import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from urllib.parse import urlparse, parse_qs
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# ═══════════════════════════════════════
# MA'LUMOTLAR
# ═══════════════════════════════════════
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
TARGET_GROUP = int(os.environ.get("TARGET_GROUP"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
MAFIA_BOT = "MafiaBakuBlack1Bot"
# ═══════════════════════════════════════

# Holat
olmos_active = True
royxat_active = True
userbot_active = True

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def click_button(event, label_hint=""):
    if not event.buttons:
        return False
    for row in event.buttons:
        for btn in row:
            if getattr(btn, "url", None):
                try:
                    parsed = urlparse(btn.url)
                    params = parse_qs(parsed.query)
                    if "start" in params:
                        start_param = params["start"][0]
                        await client.send_message(MAFIA_BOT, f"/start {start_param}")
                        print(f"[✅] {label_hint} — olindi! Param: {start_param}")
                        return True
                    else:
                        path = parsed.path.strip("/")
                        if path:
                            await client.send_message(path, "/start")
                            print(f"[✅] {label_hint} — /start yuborildi: {path}")
                            return True
                except Exception as e:
                    print(f"[❌] {label_hint} URL xato: {e}")

            if getattr(btn, "data", None):
                try:
                    await client(GetBotCallbackAnswerRequest(
                        peer=TARGET_GROUP,
                        msg_id=event.id,
                        data=btn.data
                    ))
                    print(f"[✅] {label_hint} — olindi!")
                    return True
                except Exception as e:
                    print(f"[❌] {label_hint} callback xato: {e}")
    return False


@client.on(events.NewMessage(chats=TARGET_GROUP))
async def handler(event):
    global userbot_active, olmos_active, royxat_active

    if not userbot_active:
        return

    text = event.raw_text or ""

    if royxat_active and "yxatdan o'tish" in text:
        print(f"[+] Ro'yxat boshlandi!")
        await click_button(event, "Ro'yxat")
        return

    if olmos_active and ("💎" in text or "olmos" in text.lower()):
        print(f"[💎] Olmos keldi!")
        await click_button(event, "Olmos")
        return


# ═══════════════════════════════════════
# ADMIN BOT BUYRUQLARI
# ═══════════════════════════════════════
def is_admin(user_id):
    return user_id == ADMIN_ID


@dp.message(Command("status"))
async def cmd_status(message: Message):
    if not is_admin(message.from_user.id): return
    userbot_txt = "🟢 Ishlayapti" if userbot_active else "🔴 To'xtatilgan"
    olmos_txt = "🟢 Yoqilgan" if olmos_active else "🔴 O'chirilgan"
    royxat_txt = "🟢 Yoqilgan" if royxat_active else "🔴 O'chirilgan"
    await message.answer(
        f"📊 <b>Holat:</b>\n\n"
        f"🤖 Userbot: {userbot_txt}\n"
        f"💎 Olmos: {olmos_txt}\n"
        f"📝 Ro'yxat: {royxat_txt}",
        parse_mode="HTML"
    )


@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    global userbot_active
    if not is_admin(message.from_user.id): return
    userbot_active = False
    await message.answer("🔴 Userbot to'xtatildi!")


@dp.message(Command("start_bot"))
async def cmd_start_bot(message: Message):
    global userbot_active
    if not is_admin(message.from_user.id): return
    userbot_active = True
    await message.answer("🟢 Userbot ishga tushdi!")


@dp.message(Command("olmos_on"))
async def cmd_olmos_on(message: Message):
    global olmos_active
    if not is_admin(message.from_user.id): return
    olmos_active = True
    await message.answer("💎 Olmos yoqildi!")


@dp.message(Command("olmos_off"))
async def cmd_olmos_off(message: Message):
    global olmos_active
    if not is_admin(message.from_user.id): return
    olmos_active = False
    await message.answer("💎 Olmos o'chirildi!")


@dp.message(Command("royxat_on"))
async def cmd_royxat_on(message: Message):
    global royxat_active
    if not is_admin(message.from_user.id): return
    royxat_active = True
    await message.answer("📝 Ro'yxat yoqildi!")


@dp.message(Command("royxat_off"))
async def cmd_royxat_off(message: Message):
    global royxat_active
    if not is_admin(message.from_user.id): return
    royxat_active = False
    await message.answer("📝 Ro'yxat o'chirildi!")


@dp.message(Command("start"))
async def cmd_start(message: Message):
    if not is_admin(message.from_user.id): return
    await message.answer(
        "🤖 <b>Mafia Userbot Panel</b>\n\n"
        "/status — holat\n"
        "/stop — to'xtatish\n"
        "/start_bot — ishga tushirish\n"
        "/olmos_on — olmos yoqish\n"
        "/olmos_off — olmos o'chirish\n"
        "/royxat_on — ro'yxat yoqish\n"
        "/royxat_off — ro'yxat o'chirish",
        parse_mode="HTML"
    )


# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════
async def main():
    await client.start()
    me = await client.get_me()
    print(f"[✅] Userbot kirdi: {me.first_name} (@{me.username})")
    print(f"[✅] Admin bot ishga tushdi")
    print(f"[*] Guruh kuzatilmoqda: {TARGET_GROUP}")

    await asyncio.gather(
        client.run_until_disconnected(),
        dp.start_polling(bot)
    )


asyncio.run(main())
