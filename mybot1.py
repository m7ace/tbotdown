import os
import telebot
import yt_dlp
from flask import Flask
from threading import Thread

# 1. إعداد السيرفر الوهمي لضمان بقاء البوت نشطاً
app = Flask(__name__) # تم التصحيح هنا

@app.route('/')
def home():
    return "البوت يعمل الآن بنجاح!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. إعداد البوت
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أرسل رابط الفيديو وسأقوم بتحويله إلى MP3 فوراً.")

@bot.message_handler(func=lambda message: True)
def download_audio(message):
    url = message.text
    if "list=" in url:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط فيديو واحد فقط (بدون قائمة تشغيل).")
        return

    msg = bot.reply_to(message, "⏳ جاري المعالجة...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, ext = os.path.splitext(filename)
            mp3_file = base + '.mp3'
            
        bot.edit_message_text("✅ تم التحويل، جاري الإرسال...", message.chat.id, msg.message_id)
        
        with open(mp3_file, 'rb') as audio:
            bot.send_audio(message.chat.id, audio)
        
        bot.delete_message(message.chat.id, msg.message_id)
        
        if os.path.exists(mp3_file):
            os.remove(mp3_file)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: {str(e)}", message.chat.id, msg.message_id)

# 3. التشغيل
if __name__ == '__main__': # تم التصحيح هنا
    keep_alive()
    bot.infinity_polling()

