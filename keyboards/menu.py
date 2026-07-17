from telebot import types


def main_menu():
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

    return markup
