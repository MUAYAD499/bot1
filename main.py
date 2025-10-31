from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
import os

# ====== سيرفر بسيط ليتلقى طلبات HTTP (حتى تبقي الخدمة نشطة على Render) ======
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ====== إعدادات Telegram (من Environment Variables) ======
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']

client = TelegramClient("bot", api_id, api_hash)

targets = ["@tamkeenco1", "@fullmark13", "@tamkeenco3"]

keywords = [
    "يحل", "يسوي", "عرض", "بحث", "تكليف", "يعرف",
    "فاهم", "يشرح", "مختص", "خصوصي", "سيفي", "تقرير"
]

@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text
    if any(word in text for word in keywords):
        for target in targets:
            await client.forward_messages(target, event.message)

if __name__ == "__main__":
    keep_alive()
    print("🚀 البوت شغال على Render ...")
    client.start()
    client.run_until_disconnected()
