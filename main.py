import os
import threading
from flask import Flask
import telebot

# ضع التوكن الخاص بك هنا بين العلامتين ""
BOT_TOKEN = "8857836455:AAGlE1EIFp79Q3-v53KM1DThj7kgx_fJ-QI"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# صفحة رئيسية بسيطة ليتأكد السيرفر أن البوت حيّ
@app.route('/')
def index():
    return "البوت يعمل بنجاح في الخلفية 24 ساعة دون انقطاع!"

# دالة الحذف التي يتم استدعاؤها بعد انتهاء الوقت
def delete_msg(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
        print(f"تم حذف مقطع الفيديو ذو الرقم {message_id} بنجاح بعد دقيقتين.")
    except Exception as e:
        print(f"فشل حذف الرسالة. السبب: {e}")

# مراقبة أي منشور جديد ينزل في القناة (سواء كان فيديو أو رسوم متحركة GIF)
@bot.channel_post_handler(content_types=['video', 'animation'])
def auto_delete_video(message):
    print(f"تم رصد مقطع فيديو جديد في القناة بالرقم: {message.message_id}")
    
    # تشغيل مؤقت (Timer) في الخلفية ينبض بعد 120 ثانية (دقيقتين) ثم يحذف الرسالة
    # هذه الطريقة تجعل البوت يتعامل مع كذا فيديو بوقت واحد دون أن يعلق
    threading.Timer(120.0, delete_msg, args=[message.chat.id, message.message_id]).start()

# دالة لتشغيل خادم الويب مدمج لخدعة الـ 24 ساعة
def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خيط (Thread) منفصل بالخلفية
    t = threading.Thread(target=run_web_server)
    t.daemon = True
    t.start()
    
    # تشغيل البوت واستقبال رسائل التليجرام بشكل مستمر
    print("جاري تشغيل البوت واستقبال البيانات...")
    bot.infinity_polling()
