import re

from anki.hooks import wrap, addHook

from aqt.qt import *
from aqt import mw
from aqt.editor import Editor
from aqt.addcards import AddCards
from aqt.editcurrent import EditCurrent
from aqt.utils import tooltip, showInfo

from .utils import get_config_value


def setup_hotkeys(editor):
    sequence = QKeySequence(get_config_value("shortcut.extract_text"))
    extract_text = QShortcut(sequence, editor.widget)
    extract_text.activated.connect(lambda: on_extract(editor))

def editor_save_then(callback):
    def onSaved(editor, *args, **kwargs):
        # uses evalWithCallback internally:
        editor.saveNow(lambda: callback(editor, *args, **kwargs))

    return onSaved

def on_extract(editor):
    showInfo(editor.note["Text"])
    showInfo("test")

def setup_buttons(buttons, editor):
    setup_hotkeys(editor)
    return buttons

@editor_save_then
def on_insert_cloze(editor, _old):
    """Handles cloze-wraps when the add-on model is active"""
    note = editor.note
    if note.model()["name"] != get_config_value("model_name"):
        return _old(editor)

    """target_field = get_empty_cloze_field(note);
    if target_field is None:
        return

    def cb(test):
        showInfo(target_field)

    editor.web.evalWithCallback(f
        wrap('<span style="color: violet;" class="extractor">', '</span>');
    , cb)"""

    editor.web.eval("wrap('{{c::', '}}');")


def get_empty_cloze_field(note):
    keys = editor.note.keys()

    for i in range(1, get_config_value("max_clozes")):
        fname = "c" + str(i)
        if fname in keys and note[fname] == "":
            return fname

    return None


def initialize_editor():
    Editor.onCloze = wrap(Editor.onCloze, on_insert_cloze, "around")

    addHook("setupEditorButtons", setup_buttons)
