#! /usr/bin/env python3

import genanki

from vocab import get_vocab

MODEL_ID = 654321
DECK_BASE_ID = 563412

VOCAB_FIELDS = [
    {'name': 'id'},
    {'name': 'kana'},
    {'name': 'kanji'},
    {'name': 'partofspeech'},
    {'name': 'meaning'},
]

JA_EN_TEMPLATE = {
    'name': 'kana->kanji/meaning',
    'qfmt': '<strong><span style="font-family: Meiryo; font-size: 60px; ">{{kana}}</span></strong><br/>(<i>{{partofspeech}}</i>)',
    'afmt': '{{FrontSide}}<hr><span style="font-family: Meiryo; font-size: 30px; ">{{kanji}}</span><br><strong><span style="font-size: 40px; ">{{meaning}}</span></strong></br>',
}

EN_JA_TEMPLATE = {
    'name': 'meaning->kana/kanji',
    'qfmt': '<strong><span style="font-size: 40px; ">{{meaning}}</span></strong> (<i>{{partofspeech}}</i>)</br>',
    'afmt': '{{FrontSide}}<hr><strong><span style="font-family: Meiryo; font-size: 60px; ">{{kanji}}</span></strong></br><span style="font-family: Meiryo; font-size: 30px; ">{{kana}}</span></br>',
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


def get_deck(jlpt_level):
    vocab = get_vocab(jlpt_level)
    deck = genanki.Deck(DECK_BASE_ID + jlpt_level, 'JLPT Vocab::N{}'.format(jlpt_level))
    for v in vocab:
        note = genanki.Note(
            model=VOCAB_MODEL,
            fields=[str(v.id), v.kana, v.kanji, ', '.join(v.pos), v.defn]
        )
        deck.add_note(note)
    return deck


if __name__ == '__main__':
    jlpt_level = 5
    deck = get_deck(jlpt_level)
    deck.write_to_file('jlpt_n{}.apkg'.format(jlpt_level))
