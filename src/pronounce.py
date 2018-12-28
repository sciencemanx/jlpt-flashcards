import json
import os
import tempfile

import requests

FORVO_KEY = 'XXXX'
FORVO_URL = 'https://apifree.forvo.com/{}'

PARAM_DEFAULTS = {
    'format': 'json',
    'key': FORVO_KEY,
    'action': 'word-pronunciations',
    'language': 'ja',
}


def forvo(**kwargs):
    for k, v in PARAM_DEFAULTS.items():
        kwargs[k] = kwargs.get(k, v)

    params = ['{}/{}'.format(k, v) for k, v in kwargs.items()]
    url = FORVO_URL.format('/'.join(params))
    res = requests.get(url)

    assert res.status_code == 200

    d = json.loads(res.text)
    return d['items']


def get_pronunciation_url(word, ext='ogg', **kwargs):
    assert ext in ['ogg', 'mp3']

    items = forvo(word=word, **kwargs)
    best = max(items, key=lambda item: item['hits'])

    if ext == 'ogg':
        return best['pathogg']
    if ext == 'mp3':
        return best['pathmp3']


def download_pronunciation(word, ext='ogg', **kwargs):
    assert ext in ['ogg', 'mp3']

    url = get_pronunciation_url(word, ext=ext, **kwargs)
    res = requests.get(url)

    assert res.status_code == 200

    (fd, name) = tempfile.mkstemp(prefix='{}-'.format(word), suffix='.{}'.format(ext))

    os.write(fd, res.content)
    os.close(fd)

    return name
