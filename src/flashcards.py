#! /usr/bin/env python3

import os
import shutil

import genanki
import requests

from vocab import get_vocab, JLPT_LEVELS

MODEL_ID = 654321
DECK_BASE_ID = 563412

VOCAB_FIELDS = [
    {'name': 'id'},
    {'name': 'kana'},
    {'name': 'kanji'},
    {'name': 'partofspeech'},
    {'name': 'meaning'},
    {'name': 'audio'},
]

JA_EN_TEMPLATE = {
    'name': 'kana->kanji/meaning',
    'qfmt': '{{audio}}</br><strong><span style="font-family: Meiryo; font-size: 60px; ">{{kana}}</span></strong><br/>(<i>{{partofspeech}}</i>)',
    'afmt': '{{FrontSide}}<hr><span style="font-family: Meiryo; font-size: 30px; ">{{kanji}}</span><br><strong><span style="font-size: 40px; ">{{meaning}}</span></strong></br>',
}

EN_JA_TEMPLATE = {
    'name': 'meaning->kana/kanji',
    'qfmt': '<strong><span style="font-size: 40px; ">{{meaning}}</span></strong> (<i>{{partofspeech}}</i>)</br>',
    'afmt': '{{FrontSide}}<hr><strong><span style="font-family: Meiryo; font-size: 60px; ">{{kanji}}</span></strong></br><span style="font-family: Meiryo; font-size: 30px; ">{{kana}}</span></br>{{audio}}',
}

MODEL_CSS = '''
.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color: #969696; }
.card2 { background-color: #FFFFFF; }'
)
'''

VOCAB_MODEL = genanki.Model(
    MODEL_ID,
    'JLPT Vocab Model',
    fields=VOCAB_FIELDS,
    templates=[
        JA_EN_TEMPLATE,
        EN_JA_TEMPLATE,
    ],
    css=MODEL_CSS,
)


class KanjiNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0], self.fields[1])


def get_deck(jlpt_level):
    vocab = get_vocab(jlpt_level)
    deck = genanki.Deck(DECK_BASE_ID + jlpt_level, 'JLPT Vocab::N{}'.format(jlpt_level))
    media = []
    for v in vocab:
        if v.path is not None:
            media.append(v.path)
            audio = '[sound:{}]'.format(v.path)
        else:
            audio = ''

        note = KanjiNote(
            model=VOCAB_MODEL,
            fields=[str(v.id), v.kana, v.kanji, ', '.join(v.pos), v.defn, audio]
        )

        deck.add_note(note)
    return deck, media

def get_package(jlpt_levels=None):
    if jlpt_levels is None:
        jlpt_levels = list(JLPT_LEVELS)

    assert all(jlpt_level in JLPT_LEVELS for jlpt_level in jlpt_levels)

    all_media = []
    decks = []
    for jlpt_level in jlpt_levels:
        deck, media = get_deck(jlpt_level)
        decks.append(deck)
        all_media.extend(media)

    return genanki.Package(decks, media_files=all_media)

if __name__ == '__main__':
    levels = [2]
    package = get_package(levels)
    package.write_to_file('jlpt_{}.apkg'.format('-'.join('n{}'.format(n) for n in levels)))
