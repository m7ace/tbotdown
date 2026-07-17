import telebot
from telebot import types
from config import TOKEN, BOT_NAME

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("📹 فيديو")
    btn2 = types.KeyboardButton("🎵 صوت")
    btn3 = types.KeyboardButton("⚙️ الإعدادات")
    btn4 = types.KeyboardButton("🌍 اللغة")
    btn5 = types.KeyboardButton("⭐ Premium")
    btn6 = types.KeyboardButton("📢 القناة")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)

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


print("Bot Started...")

bot.infinity_polling(skip_pending=True)
