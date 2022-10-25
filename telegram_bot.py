import json

import telebot
from secret_const import telegramBotAPI as token
from public_const import emoji
from core import *
EJ = emoji

bot = telebot.TeleBot(token)


def stat(player):
    return f'''{EJ('hash')}: {player['tag']}
{EJ('person')}: {player['name']}
{EJ('trophy')}: {player['trophies']} (max: {player['highestTrophies']})
{EJ('blue')}: {player['expLevel']} ({player['expPoints'] - sum([i * 10 + 30 for i in range(player['expLevel'])]) + 30}/{player['expLevel'] * 10 + 30})
3x3: {player['3vs3Victories']}
solo: {player['soloVictories']}
duo: {player['duoVictories']}
3 лучших бравлера:
- {player['brawlers'][0]['name']}: {player['brawlers'][0]['trophies']}{EJ('trophy')} (max: {player['brawlers'][0]['highestTrophies']}{EJ('trophy')})
- {player['brawlers'][1]['name']}: {player['brawlers'][1]['trophies']}{EJ('trophy')} (max: {player['brawlers'][1]['highestTrophies']}{EJ('trophy')})
- {player['brawlers'][2]['name']}: {player['brawlers'][2]['trophies']}{EJ('trophy')} (max: {player['brawlers'][2]['highestTrophies']}{EJ('trophy')})
icon: {player['icon']['link']}
'''


def send(chat_id, text):
    bot.send_message(chat_id, text)


@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, 'pong')
    print(message.chat.id)


@bot.message_handler(commands=['link'])
def link(message):
    data = message.text[6:].upper()
    with open('tracking_players.txt', 'r') as file:
        players = file.read().split('\n')
    if data != '' and data[0] == '#': tag = data[1:]
    else: tag = data
    if data not in players:
        bot.reply_to(message, 'Этот тег не найден среди наших кланов. Пожалуйста, проверьте тег и повторите через 5 минут.')
    else:
        try:
            open(f'players/links/{message.from_user.id}.txt', 'r').close()
            bot.reply_to(message, 'Вы уже привязали аккаунт BS к этому аккаунту ТГ.')
        except:
            try:
                open(f'players/links/{tag}.txt', 'r').close()
                bot.reply_to(message, 'Этот аккаунт BS уже привязан к другому аккаунту ТГ.')
            except:
                with open(f'players/links/{tag}.txt', 'w') as f: f.write(str(message.from_user.id))
                with open(f'players/links/{message.from_user.id}.txt', 'w') as f: f.write(str(tag))
                bot.reply_to(message, 'Аккаунты успешно связаны!')


@bot.message_handler(commands=['me'])
def me(message):
    try:
        with open(f'players/links/{message.from_user.id}.txt', 'r') as file:
            tag = file.read()
        with open(f'players/cache/{tag}.json', 'r') as file:
            player = json.loads(file.read())

        bot.reply_to(message, stat(player))
    except:
        bot.reply_to(message, 'Привязка аккаунта не найдена. Привяжите аккаунт командой /link ТЕГ')


if __name__ == '__main__':
    bot.infinity_polling()


