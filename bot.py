import telebot
from telebot import types
from config import TOKEN, BOT_NAME
import yt_dlp
import os
from keyboards.menu import main_menu

bot = telebot.TeleBot(TOKEN)

os.makedirs("downloads", exist_ok=True)


@bot.message_handler(commands=['start'])
def start(message):
    markup = main_menu()

    text = f"""
🎬 أهلاً بك في {BOT_NAME}

━━━━━━━━━━━━━━━

✅ YouTube
✅ TikTok
✅ Instagram
✅ Facebook
✅ X (Twitter)
✅ Pinterest

━━━━━━━━━━━━━━━

📥 أرسل الرابط فقط وسيتم تحميله.
"""

    bot.send_message(message.chat.id, text, reply_markup=markup)
@bot.message_handler(func=lambda message: "youtube.com" in message.text.lower() or "youtu.be" in message.text.lower())
def youtube_info(message):

    bot.reply_to(message, "🔍 جاري قراءة معلومات الفيديو...")

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "cookiefile": "cookies.txt",
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message.text, download=False)

        title = info.get("title", "Unknown")
        duration = info.get("duration", 0)
        thumbnail = info.get("thumbnail")

        minutes = duration // 60
        seconds = duration % 60

        text = f"""
🎬 {title}

⏱ {minutes}:{seconds:02}

اختر طريقة التحميل بالخطوة القادمة.
"""

        if thumbnail:
            bot.send_photo(
                message.chat.id,
                thumbnail,
                caption=text
            )
        else:
            bot.send_message(
                message.chat.id,
                text
            )

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ:\n{e}")

print("Bot Started...")

bot.infinity_polling(skip_pending=True)
