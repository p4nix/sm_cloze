from .editor import initialize_editor

import aqt
from aqt import mw, gui_hooks
from aqt.utils import showInfo
from aqt.qt import *
from aqt.editor import Editor
from aqt.addcards import AddCards

from .utils import get_config_value
from .consts import ADDON_NAME, EXTRACT_MODEL
from .extract import Extract, extract_widget
from .template import initialize_models


def check_card_for_extract(card):
    note = card.note()

    if note.model()["name"] == EXTRACT_MODEL and card.ord == 0:
        extract_widget.change_note(card.note())
        extract_widget.enable()
        mw.requireReset()

def delayed_init():
    initialize_models()

initialize_editor()

gui_hooks.reviewer_did_show_question.append(check_card_for_extract)
gui_hooks.profile_did_open.append(delayed_init)

mw.addonManager.setWebExports(ADDON_NAME, ".*\\.(js|css|map|png|svg|ttf)$")
