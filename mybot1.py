import os
import telebot
import yt_dlp

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "🎵 أرسل رابط يوتيوب وسأحوله إلى MP3")

@bot.message_handler(func=lambda m: True)
def download(message):

    url = message.text

    msg = bot.reply_to(message, "⏳ جاري التحويل...")

    try:

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "noplaylist": True,
            "cookiefile": "cookies.txt",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("audio.mp3", "rb") as f:
            bot.send_audio(message.chat.id, f)

        bot.delete_message(message.chat.id, msg.message_id)

        for file in os.listdir("."):
            if file.startswith("audio."):
                os.remove(file)

    except Exception as e:
        bot.edit_message_text(
            str(e),
            message.chat.id,
            msg.message_id
        )

bot.infinity_polling(skip_pending=True)
