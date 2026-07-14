import os
import telebot
import yt_dlp
from flask import Flask
from threading import Thread

# -----------------------------
# Flask (لإبقاء البوت يعمل)
# -----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()

# -----------------------------
# Telegram Bot
# -----------------------------
TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise Exception("TOKEN variable not found!")

bot = telebot.TeleBot(TOKEN)

# -----------------------------
# /start
# -----------------------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🎵 أهلاً بك!\n\nأرسل رابط فيديو يوتيوب وسأحوله إلى MP3."
    )

# -----------------------------
# Download Audio
# -----------------------------
@bot.message_handler(func=lambda m: True)
def download_audio(message):

    url = message.text.strip()

    if "list=" in url:
        bot.reply_to(message, "❌ أرسل رابط فيديو فقط وليس Playlist.")
        return

    msg = bot.reply_to(message, "⏳ جاري التحميل...")

    try:

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "noplaylist": True,
            "quiet": True,
            "cookiefile": "cookies.txt",

            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        mp3_file = "audio.mp3"

        if not os.path.exists(mp3_file):
            raise Exception("فشل إنشاء ملف MP3")

        bot.edit_message_text(
            "📤 جاري إرسال الملف...",
            message.chat.id,
            msg.message_id
        )

        with open(mp3_file, "rb") as audio:
            bot.send_audio(message.chat.id, audio)

        bot.delete_message(message.chat.id, msg.message_id)

        # حذف الملفات المؤقتة
        for file in os.listdir("."):
            if file.startswith("audio."):
                try:
                    os.remove(file)
                except:
                    pass

    except Exception as e:
        bot.edit_message_text(
            f"❌ حدث خطأ:\n{e}",
            message.chat.id,
            msg.message_id
        )

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(skip_pending=True)
