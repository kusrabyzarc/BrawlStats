import json

import telegram_bot
from core import *
import public_const
import secret_const

EJ = public_const.emoji


class DataOutdatedError(Exception):
    def __init__(self): pass


def alarm(x):
    telegram_bot.send(secret_const.chatlog, x)


def short_info(player):
    return f'''------------
{EJ('hash')} Тэг: {player['tag']}
{EJ('person')} Ник: {player['name']}
{EJ('trophy')} Трофеи: {player['trophies']}
------------'''


def loop():
    # Compare old and new sets of players
    try:
        with open('tracking_players.txt') as file:
            old_set = set(file.read().split('\n'))
        new_set = []
        for club in public_const.alliance_clubs:
            new_set += [member['tag'][1:] for member in Club(club)['members']]
        new_set = set(new_set)
        joined = new_set - old_set
        leave = old_set - new_set
        if joined or leave:
            to_edit = True
        else:
            to_edit = False
        if joined:
            for tag in joined:
                if tag == '': continue
                p = Player(tag)
                alarm(f"{EJ('ok')} Найден новый игрок!\n{short_info(p)}")
        if leave:
            for tag in leave:
                if tag == '': continue
                p = Player(tag)
                alarm(f"{EJ('error')} Потерян игрок!\n{short_info(p)}\nИгрок не состоит ни в одном из клубов альянса.")
        if to_edit:
            with open('tracking_players.txt', 'w') as file:
                new_set = list(new_set)
                file.writelines([i + '\n' for i in new_set if new_set.index(i) != len(new_set) - 1])
                file.write(new_set[-1])
    except TypeError:
        return -1

    # Update player data
    for tag in new_set:
        try:
            with open(f'players/cache/{tag}.json', 'r') as file:
                old_data = json.loads(file.read())
                if time.time() - old_data['timestamp'] > public_const.playerUpdateDelay:
                    raise DataOutdatedError
        except (FileNotFoundError, DataOutdatedError, json.decoder.JSONDecodeError, TypeError):
            with open(f'players/cache/{tag}.json', 'w') as file:
                data = Player(tag).data
                try:
                    if old_data['battleLog'] != data['battleLog']:
                        progression = (time.time(), data['trophies'])
                        try:
                            with open(f'players/progress/{tag}.json', 'r') as file1:
                                prog = json.loads(file1.read())
                        except:
                            prog = []
                        prog.append(progression)
                        with open(f'players/progress/{tag}.json', 'w') as file1:
                            file1.write(json.dumps(prog))
                            if prog[-1][1] - prog[-2][1] > 0:
                                alarm(f'{EJ("ok")} {data["name"]} (#{tag}): +{prog[-1][1] - prog[-2][1]}{EJ("trophy")}')
                            elif prog[-1][1] - prog[-2][1] < 0:
                                alarm(f'{EJ("error")} {data["name"]} (#{tag}): {prog[-1][1] - prog[-2][1]}{EJ("trophy")}')
                            else:
                                alarm(f'{EJ("kaif")} {data["name"]} (#{tag}): 0{EJ("trophy")}')
                except IndexError as e:
                    print(tag)
                if data:
                    file.write(json.dumps(data))
                else:
                    raise ConnectionError
        except ConnectionError:
            print('Нет интернета')


while 1:
    error = loop()
    time.sleep(3)
    if error == -1:
        print('Скорее всего, токен в бане или нет интернета. Останов.')
        break
