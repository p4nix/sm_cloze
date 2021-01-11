from aqt import mw
from aqt.utils import tooltip
import time
import re
from bs4 import BeautifulSoup

def strip_length(text, length = 80):
    return (text[:length-3] + '..') if len(text) > length else text
    
def strip_html(text):
    return BeautifulSoup(text, features="html.parser").get_text()

def review_card(card):
    mw.reset()
    card.timerStarted = time.time() - 10
    if mw.col.schedVer() == 2:
        ease = 3
    else:
        ease = 2
    if card.queue < 0:
        card.queue = 1
        tooltip("Assertion error!", parent = mw)
    mw.col.sched.answerCard(card, ease)

    mw.reset()

def review_clozes(note):
    cards = note.cards()

    i = 0
    for card in cards:
        # if clozes found, bump them up in review
        if card.ord == 0 or card.type != 0:
            continue

        review_card(card)
        i += 1
    tooltip(f"Reviewed {i} new clozes.", parent = mw)

"""
    get_notes_from_string:
        gets notes based on string with syntax {nid},{nid},{nid},...
"""
def get_notes_from_string(string):
    string = re.sub('[^0-9,]', '', string)
    string = string.rstrip(',')

    if string == "":
        return []
    else:
        return mw.col.find_notes(f""" "nid:{string}" """)
