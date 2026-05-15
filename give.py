import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# ═══════════════════════════════════════
# MA'LUMOTLAR
# ═══════════════════════════════════════
API_ID = 39185077
API_HASH = "a4d31bf9e715bd4967bedaec282efa2e"
SESSION_STRING = "1ApWapzMBu4FzMz-ZGkY-fABdWXMVfP93n_hewqpQ5NJ0L1pps8RW6MzIgLx5Jj67KkSm80HBk1khVBDVThzGExlnHpRO-kDt2DDv_Dm0VM0bM4glh055Lg7cG28rSCV73CxXcu6KXurG-j8upxj41O99HE7MkwTuCFum8pKxviIUxj9ck0iFQvv56sJgDiiafMtRD_bB2DdoB-YFsLBpzo1IUUMUAHpXCwIbUKo8T7hPb3OtYY1H1A53B9fpkYQs8lSVDANT81UBPUUN8htlgJLYPqTzcQIoQ7Z7fzc_KZSDL8MUKFArwv0Idd_rjtPccOx7CoYS_Y7ijtxBlBuGMGcdynIDLyc="
TARGET_GROUP = -1003640042053  # guruh ID
# ═══════════════════════════════════════

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    await client.start()
    me = await client.get_me()
    print(f"[✅] Kirdi: {me.first_name}")
    print(f"[*] Har 4 sekundda /giveaway yuborilmoqda...")

    while True:
        try:
            await client.send_message(TARGET_GROUP, "/giveaway")
            print(f"[📨] /giveaway yuborildi")
        except Exception as e:
            print(f"[❌] Xatolik: {e}")
        await asyncio.sleep(4)

asyncio.run(main())
