from aqt import mw
from aqt.utils import showInfo
from aqt.qt import QAction
from aqt import gui_hooks
from anki.hooks import wrap

from aqt.reviewer import Reviewer

from .options import open_options
from .config import get_config_value
from .view import View


def initialize():
    # initialize menu
    manage_smcloze = QAction("Manage SM-Cloze", mw)
    manage_smcloze.triggered.connect(open_options)

    mw.form.menuTools.addAction(manage_smcloze)

    # initialize reviewer
    view = View()

    gui_hooks.reviewer_did_show_question.append(view.new_question)

def init_after_profile_open():
    if mw.col.models.byName(get_config_value("model_name")):
        return

    showInfo("Please go to Tools>Manage SM-Cloze")





initialize()
gui_hooks.profile_did_open.append(init_after_profile_open)
