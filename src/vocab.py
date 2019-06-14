import os
from typing import List, NamedTuple

from bs4 import BeautifulSoup
from progressbar import progressbar
import requests

from pronounce import download_pronunciation


class Vocab(NamedTuple):
    id: int
    kana: str
    kanji: str
    pos: List[str]
    defn: str
    path: str


URL_FMT = 'https://jlptstudy.net/N{0}/lists/n{0}_vocab-list.html'
JLPT_LEVELS = [2, 4, 5]


def get_vocab_html(level):
    assert level in JLPT_LEVELS

    url = URL_FMT.format(level)
    res = requests.get(url)

    assert res.status_code == 200

    return str(res.content, encoding='utf8')


def get_vocab(level):
    assert level in JLPT_LEVELS

    html = get_vocab_html(level)
    soup = BeautifulSoup(html, 'html.parser')

    vocab_table = soup.find('table', {'class':'vocab-list'})

    def process_row(vocab):
        fields = vocab.find_all('td')
        idx, kana, kanji, pos, defn = [tag.text.strip() for tag in fields]

        if kanji == '':
            kanji = kana

        path = '{}.mp3'.format(kanji.replace('/', '-'))
        if not os.path.isfile(path):
            try:
                path = download_pronunciation(kanji)
            except AssertionError:
                path = None

        return Vocab(int(idx), kana, kanji, pos.split(','), defn, path)

    vocab_rows = [r for r in vocab_table.find_all('tr') if len(r.find_all('td')) == 5]
    return [process_row(r) for r in progressbar(vocab_rows)]
