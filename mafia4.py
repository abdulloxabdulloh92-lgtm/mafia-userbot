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


# =============================================
# 1. RO'YXATGA AVTOMATIK QO'SHILISH
# =============================================
@client.on(events.NewMessage(chats=TARGET_GROUP))
async def handler(event):
    text = event.raw_text

    # --- RO'YXAT ---
    if "yxatdan o'tish" in text:
        print(f"[+] Ro'yxat xabari topildi!")

        if event.buttons:
            for row in event.buttons:
                for btn in row:
                    if hasattr(btn, "url") and btn.url:
                        print(f"[+] Tugma URL: {btn.url}")
                        try:
                            parsed = urlparse(btn.url)
                            params = parse_qs(parsed.query)
                            if "start" in params:
                                start_param = params["start"][0]
                                await asyncio.sleep(0.3)
                                await client.send_message(MAFIA_BOT, f"/start {start_param}")
                                print(f"[✅] Ro'yxatdan o'tildi! Param: {start_param}")
                                return
                        except Exception as e:
                            print(f"[❌] Ro'yxat xatolik: {e}")

        # Matndan qidirish (zaxira)
        if "t.me/" in text:
            for word in text.split():
                if "t.me/" in word and "start=" in word:
                    try:
                        parsed = urlparse(word)
                        params = parse_qs(parsed.query)
                        if "start" in params:
                            start_param = params["start"][0]
                            await asyncio.sleep(0.3)
                            await client.send_message(MAFIA_BOT, f"/start {start_param}")
                            print(f"[✅] Matndan o'tildi! Param: {start_param}")
                            return
                    except:
                        pass

    # --- OLMOS ---
    if "💎" in text or "olmos" in text.lower():
        print(f"[💎] Olmos xabari topildi!")

        if event.buttons:
            for row in event.buttons:
                for btn in row:
                    # Callback button (inline) — "Bosing" tugmasi
                    if hasattr(btn, "data") and btn.data:
                        try:
                            await asyncio.sleep(0.2)
                            await client(GetBotCallbackAnswerRequest(
                                peer=TARGET_GROUP,
                                msg_id=event.id,
                                data=btn.data
                            ))
                            print(f"[✅] Olmos olindi! (callback)")
                            return
                        except Exception as e:
                            print(f"[❌] Callback xatolik: {e}")

                    # URL button bo'lsa
                    if hasattr(btn, "url") and btn.url:
                        try:
                            parsed = urlparse(btn.url)
                            params = parse_qs(parsed.query)
                            if "start" in params:
                                start_param = params["start"][0]
                                await asyncio.sleep(0.2)
                                await client.send_message(MAFIA_BOT, f"/start {start_param}")
                                print(f"[✅] Olmos olindi! (url)")
                                return
                        except Exception as e:
                            print(f"[❌] URL xatolik: {e}")
        else:
            print("[-] Olmos xabarida tugma topilmadi")


async def main():
    await client.start()
    me = await client.get_me()
    print(f"[✅] Kirdi: {me.first_name} (@{me.username})")
    print(f"[*] Guruh kuzatilmoqda: {TARGET_GROUP}")
    print(f"[*] Ro'yxat va olmos kuzatilmoqda...")
    await client.run_until_disconnected()


asyncio.run(main())
