from aqt import mw
from .config import get_config_value

class View():
    def __init__(self):
        self.is_smcloze = False

    def new_question(self, card):
        if card.model()["name"] != get_config_value("model_name"):
            self.is_smcloze = False
            return

        self.is_smcloze = True

        mw.web.eval("""alert("Hello World");""")
