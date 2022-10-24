import requests
import json
import TOKENS
import time


baseLink = 'https://raw.githubusercontent.com/heliocosta1337/brawl-stars-cdn/main/public/'

playerIcon = baseLink + 'player-icon/'
rankIcon = baseLink + 'rank/'
starpowerIcon = baseLink + 'starpower/'
pinIcon = baseLink + 'pins/brawlers/'
gamemodeIcon = baseLink + 'gamemode-icon/'
gadgetIcon = baseLink + 'gadget/'
clubIcon = baseLink + 'club-badge/'
brawlerPortrait = baseLink + 'brawler-portrait/'
brawlerIcon = baseLink + 'brawler-icon/'
brawler3D = baseLink + 'brawler-3d/'


def get(params):
    headers = {
        'authorization': f'Bearer {TOKENS.brawlAPI()}'
    }
    try:
        data = requests.get(f'https://api.brawlstars.com/v1/{params}', headers=headers)
        return json.loads(data.text)
    except requests.ConnectionError:
        return False
    except json.decoder.JSONDecodeError:
        return False


def tagFormat(tag):
    if tag[0] != '#':
        tag = '%23' + tag
    else:
        tag = '%23' + tag[1:]
    return tag


class PlayerStatement:
    def __init__(self, tag):
        self.tag = tagFormat(tag)
        self.update()

    def update(self):
        self.data = get(f'players/{self.tag}')
        self.timestamp = time.time()
        self.data['icon']['link'] = f'{playerIcon}{self.data["icon"]["id"]}.png'
        if self.data:
            self.data['brawlers'].sort(key=lambda d: -d['trophies'])
        self.data['battleLog'] = get(f'players/{self.tag}/battlelog')['items']


def clubInfo(tag):
    tag = tagFormat(tag)
    return get(f'clubs/{tag}')


if __name__ == '__main__':
    player = PlayerStatement('PPL280GGQ')
    player.update()
    for key in player.data: print(f'{key}: {player.data[key]}')
