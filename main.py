import os
import threading
from flask import Flask
import telebot

BOT_TOKEN = "8857836455:AAHjYfUCltosPYLte7W59XATr16-ztmstD4"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# قاموس لتخزين مؤقت للقروب ميديا لضمان تزامن الحذف
media_groups = {}

def delete_msg(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

@bot.channel_post_handler(content_types=['photo', 'video', 'animation', 'document', 'audio', 'voice'])
def handle_media(message):
    # إذا كان المقطع جزءاً من قروب ميديا
    if message.media_group_id:
        # نشغل المؤقت لكل مقطع في القروب بشكل مستقل ليتم حذفهم جميعاً بعد 90 ثانية
        threading.Timer(90.0, delete_msg, args=[message.chat.id, message.message_id]).start()
    else:
        # إذا كان مقطعاً منفرداً (ليس قروب)
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
