import aqt
from aqt.qt import *
from aqt import mw
from aqt.utils import showInfo
from typing import Any
import time

from .utils import get_config_value
from .consts import ADDON_NAME, EXTRACT_MAX, EXTRACT_FLDS, EXTRACT_MODEL
from .tinymce import TinyMCE
import re
from anki.notes import Note

def review_card(card):
    mw.reset()
    card.timerStarted = time.time() - 10
    if mw.col.schedVer() == 2:
        ease = 3
    else:
        ease = 2
    mw.col.sched.answerCard(card, ease)
    mw.reset()

def review_clozes(note):
    cards = note.cards()

    for card in cards:
        # if clozes found, bump them up in review
        if card.ord == 0 or card.type != 0:
            continue

        review_card(card)


class Extract(QWidget):
    def set_addcards(self, addcards):
        self.addcards = addcards
        self.editor_web = addcards.editor.web
        self.editor_note = self.addcards.editor.note

    def __init__(self):
        QWidget.__init__(self)

        self.tinyMCE = TinyMCE(self)

        self.setWindowTitle("Extract")
        self.setWindowFlag(Qt.Dialog)

        self.init_sidebar()
        self.init_shortcuts()

    def make_cloze(self, cloze_text):
        keys = self.note.keys()

        for i in range(1, EXTRACT_MAX + 1):
            cname = "c" + str(i)
            if cname in keys and self.note[cname] == "":
                self.note[cname] = cloze_text
                self.save_note()

                return
        showInfo("No empty field for cloze found, try making a new extract!")

    def make_extract(self, extract_text):
        model = mw.col.models.byName(EXTRACT_MODEL)
        model['did'] = self.did

        new_note = Note(mw.col, model)

        new_note["Text"] = extract_text
        new_note[EXTRACT_FLDS["p_id"]] = str(self.note.id)
        new_note[EXTRACT_FLDS["cx"]] = self.note[EXTRACT_FLDS["cx"]]
        new_note[EXTRACT_FLDS["sc"]] = self.note[EXTRACT_FLDS["sc"]]

        new_note.setTagsFromStr(self.note.stringTags())

        mw.col.addNote(new_note)
        self.note[EXTRACT_FLDS["c_id"]] += str(new_note.id) + ","

        self.do_action_after_save = ["change_note", new_note]
        self.save_note()

    def cloze_html(self):
        self.tinyMCE.eval("do_html_cloze();")

    def extract_html(self):
        self.tinyMCE.eval("do_html_extract();")

    def save_note(self, callback = None):
        note = self.note
        def cb(text: str):
            note["Text"] = text
            note.flush()

            review_clozes(note)

            if self.do_action_after_save:
                action = self.do_action_after_save[0]
                item = self.do_action_after_save[1]
                self.do_action_after_save = None
                self.do_action(action, item)

            mw.reset()

        self.tinyMCE.evalWithCallback("save_text();", cb)

    def do_action(self, action, item):
        if action == "change_note":
            self.change_note(item)
        elif action == "review_card":
            review_card(item)
            self.disable()
        elif action == "suspend_card":
            mw.col.sched.suspend_cards([item.id])
            mw.reset()
            self.disable()
        elif action == "bury_card":
            mw.col.sched.bury_cards([item.id])
            mw.reset()
            self.disable()
        else:
            showInfo("Couldn't do: "+action)


    def go_to_parent(self):
        self.do_action_after_save = ["change_note", self.parent]
        self.save_note()

    def go_to_child(self, idx):
        nid = self.children_button.itemData(idx)
        self.do_action_after_save = ["change_note", mw.col.getNote(nid)]
        self.save_note()

    def init_sidebar(self):
        self.title_box = QHBoxLayout()

        self.parent_button = QPushButton("Parent")
        self.parent_button.clicked.connect(self.go_to_parent)
        self.children_button = QComboBox()
        self.children_button.activated.connect(self.go_to_child)

        self.title_box.addWidget(self.parent_button)
        self.title_box.addWidget(self.children_button)

        self.bottom_box = QHBoxLayout()

        self.review_button = QPushButton("Review")
        self.review_button.clicked.connect(self.review_text_card)

        self.suspend_button = QPushButton("Suspend")
        self.suspend_button.clicked.connect(self.suspend_text_card)

        self.bury_button = QPushButton("Bury")
        self.bury_button.clicked.connect(self.bury_text_card)

        self.bottom_box.addWidget(self.suspend_button)
        self.bottom_box.addWidget(self.bury_button)
        self.bottom_box.addWidget(self.review_button)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.title_box)
        self.vbox.addWidget(self.tinyMCE)
        self.vbox.addLayout(self.bottom_box)

        self.setLayout(self.vbox)

    def get_text_card(self):
        cards = self.note.cards()
        return cards[0]

    def review_text_card(self):
        self.do_action_after_save = ["review_card", self.get_text_card()]
        self.save_note()

    def suspend_text_card(self):
        self.do_action_after_save = ["suspend_card", self.get_text_card()]
        self.save_note()

    def bury_text_card(self):
        self.do_action_after_save = ["bury_card" ,self.get_text_card()]
        self.disable()

    def init_shortcuts(self):
        self.sc_cloze = QShortcut(get_config_value("shortcut.cloze_text"), self)
        self.sc_cloze.activated.connect(self.cloze_html)

        self.sc_extract = QShortcut(get_config_value("shortcut.extract_text"), self)
        self.sc_extract.activated.connect(self.extract_html)

        self.escape = QShortcut("Escape", self)
        self.escape.activated.connect(self.disable)

    def change_note(self, note):
        if note is None:
            return

        self.do_action_after_save = None

        self.note = note
        card = self.get_text_card()
        self.did = card.odid or card.did

        self.get_parent()
        self.get_children()

        content = self.note["Text"]
        self.tinyMCE.eval(f"load_html(`{content}`);")

    def get_parent(self):
        parent_string = self.note[EXTRACT_FLDS["p_id"]]
        parent_string = re.sub('[^0-9,]', '', parent_string)
        parent_string = parent_string.rstrip(',')

        if parent_string == "":
            parent_string = "1"

        notes = mw.col.find_notes(f""" "nid:{parent_string}" """)

        parent_string = ""
        if notes:
            note = mw.col.getNote(notes[0])
            self.parent = note
            parent_string = str(note.id)
            self.parent_button.setEnabled(True)
        else:
            self.parent = None
            self.note[EXTRACT_FLDS["p_id"]]
            self.parent_button.setEnabled(False)
        self.note[EXTRACT_FLDS["p_id"]] = parent_string

    def get_children(self):
        children_string = self.note[EXTRACT_FLDS["c_id"]]
        children_string = re.sub('[^0-9,]', '', children_string)
        children_string = children_string.rstrip(',')

        self.children_button.clear()
        if children_string == "":
            children_string = "1"
        notes = mw.col.find_notes(f""" "nid:{children_string}" """)

        children_string = ""
        for n in notes:
            note = mw.col.getNote(n)
            children_string += str(note.id) + ","
            info = note["Text"]
            info = (info[:75] + '..') if len(info) > 75 else info
            self.children_button.addItem(info, note.id)
        self.note[EXTRACT_FLDS["c_id"]] = children_string


    def enable(self):
        self.setVisible(True)
        self.raise_()
        self.is_enabled = True

    def disable(self):
        self.setVisible(False)
        self.is_enabled = False

        self.note = None

extract_widget = Extract()
