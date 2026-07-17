import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# نحفظ آخر رابط أرسله كل مستخدم
user_links = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 أهلاً بك في Universal Downloader Bot\n\n"
        "📥 أرسل رابط فيديو من:\n"
        "• YouTube\n"
        "• TikTok\n"
        "• Instagram\n"
        "• Facebook"
    )

@bot.message_handler(func=lambda m: True)
def receive_link(message):

    link = message.text

    if not link.startswith("http"):
        bot.reply_to(message, "❌ أرسل رابط صحيح.")
        return

    user_links[message.chat.id] = link

    keyboard = InlineKeyboardMarkup()

    keyboard.row(
        InlineKeyboardButton("🎥 فيديو", callback_data="video"),
        InlineKeyboardButton("🎵 MP3", callback_data="mp3")
    )

    bot.send_message(
        message.chat.id,
        "✅ اختر نوع التحميل:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "video":

        bot.answer_callback_query(call.id)

        bot.send_message(
            call.message.chat.id,
            "🚧 تحميل الفيديو سنضيفه بالخطوة القادمة."
        )

    elif call.data == "mp3":

        bot.answer_callback_query(call.id)

        bot.send_message(
            call.message.chat.id,
            "🚧 تحميل MP3 سنضيفه بالخطوة القادمة."
        )

print("Bot Started")

bot.infinity_polling(skip_pending=True)
