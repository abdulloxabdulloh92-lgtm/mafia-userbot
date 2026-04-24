import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
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
    if not event.buttons:
        print(f"[-] {label_hint} — tugma yo'q")
        return False

    for row in event.buttons:
        for btn in row:
            # 1. URL button
            if getattr(btn, "url", None):
                try:
                    parsed = urlparse(btn.url)
                    params = parse_qs(parsed.query)
                    if "start" in params:
                        start_param = params["start"][0]
                        await asyncio.sleep(0)
                        await client.send_message(MAFIA_BOT, f"/start {start_param}")
                        print(f"[✅] {label_hint} — olindi! Param: {start_param}")
                        return True
                    else:
                        path = parsed.path.strip("/")
                        if path:
                            await asyncio.sleep(0)
                            await client.send_message(path, "/start")
                            print(f"[✅] {label_hint} — /start yuborildi: {path}")
                            return True
                except Exception as e:
                    print(f"[❌] {label_hint} URL xatolik: {e}")

            # 2. Callback button
            if getattr(btn, "data", None):
                try:
                    await asyncio.sleep(0)
                    await client(GetBotCallbackAnswerRequest(
                        peer=TARGET_GROUP,
                        msg_id=event.id,
                        data=btn.data
                    ))
                    print(f"[✅] {label_hint} — olindi!")
                    return True
                except Exception as e:
                    print(f"[❌] {label_hint} callback xatolik: {e}")

    return False


@client.on(events.NewMessage(chats=TARGET_GROUP))
async def handler(event):
    text = event.raw_text

    if "yxatdan o'tish" in text:
        print(f"[+] Ro'yxat boshlandi!")
        await click_button(event, "Ro'yxat")
        return

    if "💎" in text or "olmos" in text.lower():
        print(f"[💎] Olmos keldi!")
        await click_button(event, "Olmos")
        return


async def main():
    await client.start()
    me = await client.get_me()
    print(f"[✅] Kirdi: {me.first_name} (@{me.username})")
    print(f"[*] Guruh kuzatilmoqda: {TARGET_GROUP}")
    print(f"[*] Ro'yxat va olmos kuzatilmoqda...")
    await client.run_until_disconnected()


asyncio.run(main())
