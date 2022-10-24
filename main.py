import requests
import json
import TOKENS
import time


baseLink = 'https://raw.githubusercontent.com/heliocosta1337/brawl-stars-cdn/main/public'

get_images = {
    'playerIcon': 'player-icon',
    'rankIcon': 'rank',
    'starpowerIcon': 'starpower',
    'pinIcon': 'pins/brawlers',
    'gamemodeIcon': 'gamemode-icon',
    'gadgetIcon': 'gadget',
    'clubIcon': 'club-badge',
    'brawlerPortrait': 'brawler-portrait',
    'brawlerIcon': 'brawler-icon',
    'brawler3D': 'brawler-3d'
}


def getIcon(type, id): return f'{baseLink}/{get_images[type]}/{id}.png'

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
        if self.data:
            self.data['brawlers'].sort(key=lambda d: -d['trophies'])
            self.data['icon']['link'] = getIcon('playerIcon', self.data['icon']['id'])
            self.data['battleLog'] = get(f'players/{self.tag}/battlelog')['items']


def clubInfo(tag):
    tag = tagFormat(tag)
    return get(f'clubs/{tag}')


if __name__ == '__main__':
    player = PlayerStatement('PPL280GGQ')
    player.update()
    for key in player.data: print(f'{key}: {player.data[key]}')
