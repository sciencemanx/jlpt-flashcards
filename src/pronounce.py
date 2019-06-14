import json
import os

import requests

FORVO_KEY = ''
FORVO_URL = 'https://apifree.forvo.com/{}'

PARAM_DEFAULTS = {
    'format': 'json',
    'key': FORVO_KEY,
    'action': 'pronounced-words-search',
    'language': 'ja',
}

dot = '・'
tilde = '～'
slash = '/'

FORVO_FAILING = False

def forvo(**kwargs):
    global FORVO_FAILING
    if FORVO_FAILING:
        raise AssertionError

    for k, v in PARAM_DEFAULTS.items():
        kwargs[k] = kwargs.get(k, v)

    params = ['{}/{}'.format(k, v) for k, v in kwargs.items()]
    url = FORVO_URL.format('/'.join(params))
    res = requests.get(url)

    if res.status_code == 400:
        print(url)
        print(res)
        print(res.text)
        print('forvo failing')
        FORVO_FAILING = True

    assert res.status_code == 200

    d = json.loads(res.text)
    return d['items']


def get_pronunciation_url(word, ext='mp3', **kwargs):
    assert ext in ['ogg', 'mp3']

    word = word.replace(tilde, '')
    word = word.replace('(', '')
    word = word.replace(')', '')

    if dot in word:
        word = word.split(dot)[0]

    if slash in word:
        word = word.split(slash)[0]

    items = forvo(search=word, **kwargs)

    if len(items) == 0:
        print(word)
        raise AssertionError()

    best = items[0]['standard_pronunciation']

    if ext == 'ogg':
        return best['pathogg']
    if ext == 'mp3':
        return best['pathmp3']


def download_pronunciation(word, ext='ogg', **kwargs):
    assert ext in ['ogg', 'mp3']

    url = get_pronunciation_url(word, ext=ext, **kwargs)
    res = requests.get(url)

    assert res.status_code == 200

    filename = '{}.{}'.format(word.replace('/', '-'), ext)
    with open(filename, 'wb') as f:
        f.write(res.content)

    return filename
