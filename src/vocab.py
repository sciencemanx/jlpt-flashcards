from typing import List, NamedTuple

from bs4 import BeautifulSoup
import requests

from pronounce import get_pronunciation_url


class Vocab(NamedTuple):
    id: int
    kana: str
    kanji: str
    pos: List[str]
    defn: str
    url: str


URL_FMT = 'https://jlptstudy.net/N{0}/lists/n{0}_vocab-list.html'
JLPT_LEVELS = [2, 3, 4, 5]


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
        url = get_pronunciation_url(kanji)
        return Vocab(int(idx), kana, kanji, pos.split(','), defn, url)

    rows = vocab_table.find_all('tr')
    return [process_row(r) for r in rows if len(r.find_all('td')) == 5]
