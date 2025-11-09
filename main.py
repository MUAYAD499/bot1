from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, PeerFloodError
from flask import Flask
from threading import Thread
import os
import asyncio

# ====== Flask Server to keep Render alive ======
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ====== Telegram Config ======
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']

client = TelegramClient("bot", api_id, api_hash)

targets = ["@fullmark13"]

keywords = [
    "يحل", "يسوي", "عرض", "بحث", "تكليف", "يعرف",
    "فاهم", "يشرح", "مختص", "خصوصي", "سيفي", "تقرير"
]

@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text
    if any(word in text for word in keywords):
        for target in targets:
            try:
                await asyncio.sleep(10)  # تأخير 10 ثوانٍ بين كل رسالة وأخرى
                await client.forward_messages(target, event.message)
            except FloodWaitError as e:
                print(f"⏳ FloodWaitError: يجب الانتظار {e.seconds} ثانية")
                await asyncio.sleep(e.seconds)
            except PeerFloodError:
                print("🚫 تم اكتشاف نشاط مشبوه (PeerFloodError).")
            except Exception as e:
                print(f"⚠️ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    keep_alive()
    print("🚀 البوت شغال على Render ...")
    client.start()
    client.run_until_disconnected()
