import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from urllib.parse import urlparse, parse_qs

# === ENVIRONMENT VARIABLES ===
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
TARGET_GROUP = int(os.environ.get("TARGET_GROUP"))
MAFIA_BOT = "MafiaBakuBlack1Bot"
# ==============================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def click_button(event, label_hint=""):
    if not event.reply_markup or not event.buttons:
        print(f"[-] {label_hint} — tugma yo'q")
        return False

    for row in event.buttons:
        for btn in row:
            # 1. URL tugmalarni tekshirish (Agar olmos start-havola orqali berilsa)
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
                        if path and not path.isdigit():
                            await client.send_message(path, "/start")
                            print(f"[✅] {label_hint} — /start yuborildi: {path}")
                            return True
                except Exception as e:
                    print(f"[❌] {label_hint} URL xatolik: {e}")
            
            # 2. Callback (Inline) tugmalarni bosish (Agar olmos oddiy tugma bo'lsa)
            elif getattr(btn, "data", None):
                try:
                    await btn.click()
                    print(f"[✅] {label_hint} — olindi!")
                    return True
                except Exception as e:
                    print(f"[❌] {label_hint} callback xatolik: {e}")
                    
    return False

@client.on(events.NewMessage(chats=TARGET_GROUP))
async def handler(event):
    text = event.raw_text or ""
    
    # ❌ Ro'yxatdan o'tish (O'yinga qo'shilish) qismi olib tashlandi.
    
    # 💎 Faqat olmos kelganda ishlaydi
    if "💎" in text or "olmos" in text.lower():
        print(f"[💎] Olmos xabari aniqlandi! Tugma bosilmoqda...")
        await click_button(event, "Olmos")
        return

async def main():
    await client.start()
    me = await client.get_me()
    print(f"[✅] Kirdi: {me.first_name} (@{me.username})")
    print(f"[*] Guruh kuzatilmoqda: {TARGET_GROUP}")
    print(f"[*] FAQAT OLMOS KUZATILMOQDA (O'yinga qo'shilmaydi)...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
