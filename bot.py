import os
import telebot

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🎉 أهلاً بك في Universal Downloader Bot\n\n"
        "📥 أرسل أي رابط فيديو وسأقوم بتحميله لك."
    )


@bot.message_handler(func=lambda message: True)
def receive(message):
    bot.reply_to(
        message,
        "✅ تم استلام الرابط.\n\n"
        "🚧 ميزة التحميل سنضيفها بالخطوة القادمة."
    )


print("Bot Started...")

bot.infinity_polling(skip_pending=True)
