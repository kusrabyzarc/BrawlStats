import time

from core import *
import public_const
EJ = public_const.emoji


def alarm(x):
    print(x)


def short_info(player):
    return f'''{EJ('hash')} Тэг: {player['tag']}
{EJ('person')} Ник: {player['name']}
{EJ('trophy')} Трофеи: {player['trophies']}'''

def loop():
    # Compare old and new sets of players
    with open('tracking_players.txt') as file:
        old_set = set(file.read().split('\n'))
    new_set = []
    for club in public_const.alliance_clubs:
        new_set += [member['tag'][1:] for member in Club(club)['members']]
    new_set = set(new_set)
    joined = new_set - old_set
    left = old_set - new_set
    print(old_set)
    print(new_set)
    if joined:
        for tag in joined:
            p = Player(tag)
            alarm(f"Найден новый игрок!\n{short_info(p)}")
    if left:
        for tag in left:
            p = Player(tag)
            alarm(f"Потерян игрок!\n{short_info(p)}\nИгрок не состоит ни в одном из клубов альянса.")


while 1:
    loop()
    time.sleep(3)