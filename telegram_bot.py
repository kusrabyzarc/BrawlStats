import telebot
from secret_const import telegramBotAPI as token
from core import *

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['ping'])
def ping(message):
    t = ''.join(message.text[6:])
    print(t)
    bot.reply_to(message, t)

@bot.message_handler(commands=['test'])
def test(message):
    pass


bot.infinity_polling()


