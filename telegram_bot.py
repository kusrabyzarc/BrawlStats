import json

import telebot
from secret_const import telegramBotAPI as token
from secret_const import admin_list as admins
from secret_const import admin_nick
from secret_const import superuser_list
from public_const import emoji
from core import *
import os
EJ = emoji

admins.extend(superuser_list)

bot = telebot.TeleBot(token)

def is_banned(id_):
    try:
        with open('players/banned/{id_}.txt') as file:
            print(f'{id_} banned.')
            return True
    except:
        print(f'{id_} is not banned.')
        return False


def send(chat_id, text):
    bot.send_message(chat_id, text)


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

@bot.message_handler(commands=['ping'])
def ping(message):
    if is_banned(message.from_user.id): return 0
    bot.reply_to(message, 'Pong!')
    print('Ping from:', message.chat.id)


@bot.message_handler(commands=['link'])
def link(message):
    if is_banned(message.from_user.id): return 0
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
    if is_banned(message.from_user.id): return 0
    try:
        with open(f'players/links/{message.from_user.id}.txt', 'r') as file:
            tag = file.read()
        with open(f'players/cache/{tag}.json', 'r') as file:
            player = json.loads(file.read())

        bot.reply_to(message, stat(player))
    except FileNotFoundError:
        bot.reply_to(message, 'Привязка аккаунта не найдена. Привяжите аккаунт командой /link ТЕГ')
        

@bot.message_handler(commands=['who'])
def info(message):
    if is_banned(message.from_user.id): return 0
    try:
        with open(f'players/links/{message.reply_to_message.from_user.id}.txt', 'r') as file:
            tag = file.read()
        with open(f'players/cache/{tag}.json', 'r') as file:
            player = json.loads(file.read())
        bot.reply_to(message, stat(player))
    except AttributeError:
        bot.reply_to(message, 'Используйте эту команду с ответом на сообщение')
    except FileNotFoundError:
        bot.reply_to(message, 'Привязка аккаунта не найдена.')

@bot.message_handler(commands=['force_link'])
def force_link(message):
    if is_banned(message.from_user.id): return 0
    if message.from_user.id not in admins: bot.reply_to(message, f'{admin_nick}, оторви ему руки.')
    else:
        data = message.text.upper()[12:]
        try:
            tg_id = message.reply_to_message.from_user.id
            if data == 'DELETE':
                try:
                    with open(f'players/links/{tg_id}.txt', 'r') as file:
                        tag = file.read()
                    os.remove(f'players/links/{tg_id}.txt')
                    os.remove(f'players/links/{tag}.txt')
                    bot.reply_to(message, 'Аккаунты отвязаны')
                except FileNotFoundError:
                    bot.reply_to(message, 'Привязка аккаунта не найдена.')
            else:
                message.text = f'/link {data}'
                message.from_user.id = tg_id
                link(message)
        except AttributeError:
            bot.reply_to(message, 'Используйте эту команду с ответом на сообщение')
        
@bot.message_handler(commands=['ban'])
def huesos(message):
    if is_banned(message.from_user.id): return 0
    if message.from_user.id not in admins: bot.reply_to(message, f'{admin_nick}, оторви ему руки.')
    else:
        huesos_id = message.reply_to_message.from_user.id
        open(f'players/banned/{huesos_id}.txt', 'w').close()
        bot.reply_to(message, f'@{message.reply_to_message.from_user.username}, забанен, чекай.')


if __name__ == '__main__':
    bot.infinity_polling()


