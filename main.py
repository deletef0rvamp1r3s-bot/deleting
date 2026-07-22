import os
import threading
from flask import Flask
import telebot

# سحب التوكن من متغيرات البيئة في ريندر بشكل آمن
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def delete_msg(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")
        pass

@bot.channel_post_handler(content_types=['photo', 'video', 'animation', 'document', 'audio', 'voice'])
def handle_media(message):
    # تشغيل المؤقت لكل مقطع بشكل مستقل ليتم حذفه بعد 90 ثانية
    threading.Timer(90.0, delete_msg, args=[message.chat.id, message.message_id]).start()

@app.route('/')
def index():
    return "البوت يعمل 24 ساعة!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, use_reloader=False)

if __name__ == "__main__":
    t = threading.Thread(target=run_web_server)
    t.daemon = True
    t.start()
    bot.infinity_polling()
