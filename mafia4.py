import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

# ═══════════════════════════════════════
# MA'LUMOTLAR
# ═══════════════════════════════════════
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
TARGET_GROUP = int(os.environ.get("TARGET_GROUP"))
# ═══════════════════════════════════════

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=TARGET_GROUP))
async def handler(event):
    text = event.raw_text or ""

    if "💎" not in text and "olmos" not in text.lower():
        return

    print(f"[💎] Olmos keldi!")

    # Tugmalarni olish — avval event dan, bo'lmasa qayta yuklab
    if event.buttons:
        rows = event.buttons
    else:
        msg = await client.get_messages(TARGET_GROUP, ids=event.id)
        if not msg or not msg.buttons:
            print("[-] Tugma yo'q")
            return
        rows = msg.buttons

    for row in rows:
        for btn in row:
            if getattr(btn, "data", None):
                try:
                    await client(GetBotCallbackAnswerRequest(
                        peer=TARGET_GROUP,
                        msg_id=event.id,
                        data=btn.data
                    ))
                    print(f"[✅] Olmos olindi!")
                    return
                except Exception as e:
                    print(f"[❌] Xato: {e}")

async def main():
    await client.start()
    me = await client.get_me()
    print(f"[✅] Kirdi: {me.first_name} (@{me.username})")
    print(f"[*] Olmos kuzatilmoqda...")
    await client.run_until_disconnected()

asyncio.run(main())
