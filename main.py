import requests
import json
import TOKENS


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


def battleLog(tag):
    tag = tagFormat(tag)
    return get(f'players/{tag}/battlelog')['items']


def playerInfo(tag):
    tag = tagFormat(tag)
    data = get(f'players/{tag}')
    if data:
        data['brawlers'].sort(key=lambda d: -d['trophies'])
        data['club'] = data['club']['tag']
    return data


def clubInfo(tag):
    tag = tagFormat(tag)
    return get(f'clubs/{tag}')


print(playerInfo('PPL280GGQ'))
