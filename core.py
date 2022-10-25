import requests
import json
from secret_const import brawlAPI as APIToken
import time


def tagFormat(tag):
    if tag[0] != '#':
        tag = '%23' + tag
    else:
        tag = '%23' + tag[1:]
    return tag.upper()


class Icon:
    def __init__(self):
        self.baseLink = 'https://raw.githubusercontent.com/heliocosta1337/brawl-stars-cdn/main/public'
        self.playerIcon = 'player-icon'
        self.rankIcon = 'rank'
        self.starpowerIcon = 'starpower'
        self.pinIcon = 'pins/brawlers'
        self.gamemodeIcon = 'gamemode-icon'
        self.gadgetIcon = 'gadget'
        self.clubIcon = 'club-badge'
        self.brawlerPortrait = 'brawler-portrait'
        self.brawlerIcon = 'brawler-icon'
        self.brawler3D = 'brawler-3d'
Icon = Icon()


def getIcon(type, id): return f'{Icon.baseLink}/{type}/{id}.png'


def get(params):
    headers = {
        'authorization': f'Bearer {APIToken}'
    }
    try:
        data = requests.get(f'https://api.brawlstars.com/v1/{params}', headers=headers)
        data = json.loads(data.text)
        if data['reason'] == 'notFound': return False
    except requests.ConnectionError:
        return False
    except json.decoder.JSONDecodeError:
        return False
    except KeyError:
        return data


class Player:
    def __getitem__(self, item): return self.data[item]
    def __setitem__(self, key, value): self.data[key] = value

    def __init__(self, tag):
        self.timestamp = None
        self.data = None
        self.tag = tagFormat(tag)
        self.update()

    def update(self):
        self.data = get(f'players/{self.tag}')
        self.timestamp = time.time()
        if self.data:
            self['brawlers'].sort(key=lambda d: -d['trophies'])
            for brawler in self['brawlers']:
                brawler['icon'] = getIcon(Icon.brawlerIcon, brawler['id'])
                for star in brawler['starPowers']: star['icon'] = getIcon(Icon.starpowerIcon, star['id'])
                for gadget in brawler['gadgets']: gadget['icon'] = getIcon(Icon.gadgetIcon, gadget['id'])
            self['icon']['link'] = getIcon(Icon.playerIcon, self['icon']['id'])
            self['battleLog'] = get(f'players/{self.tag}/battlelog')['items']
            self['timestamp'] = self.timestamp


class Club:
    def __getitem__(self, item): return self.data[item]
    def __setitem__(self, key, value): self.data[key] = value

    def __init__(self, tag):
        self.timestamp = None
        self.data = None
        self.tag = tagFormat(tag)
        self.update()

    def update(self):
        self.data = get(f'clubs/{self.tag}')
        self.timestamp = time.time()
        if self.data:
            self['icon'] = {'id': self['badgeId'], 'link': getIcon(Icon.clubIcon, self['badgeId'])}
            self.data.pop('badgeId')
            for member in self['members']:
                member['icon']['link'] = getIcon(Icon.playerIcon, member['icon']['id'])
            self['timestamp'] = self.timestamp


if __name__ == '__main__': pass
    # club = Club('28GLU0CU9')
    # for k in club.data:
    #     print(f'{k}: {club.data[k]}')
