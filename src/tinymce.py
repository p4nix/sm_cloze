from aqt.qt import *
from aqt.webview import AnkiWebView
from typing import Any
from .utils import get_config_value

from aqt import mw

from .consts import ADDON_NAME
from aqt.utils import showInfo

class TinyMCE(AnkiWebView):
    def __init__(self, parent):
        AnkiWebView.__init__(self, title = "Extractor")

        self.parent = parent
        addon_id = ADDON_NAME

        self.set_bridge_command(self._on_bridge_cmd, self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.stdHtml(f"""<html><body id="htmlcontent"></body></html>""",
        css = [f"../_addons/{addon_id}/web/style.css"],
        js = [f"../_addons/{addon_id}/web/content.js",
              f"../_addons/{addon_id}/web/tinymce/tinymce.min.js"])

        self.eval(f"""var absolute_base_url = "http://127.0.0.1:{mw.mediaServer.getPort()}/";""")

    def _on_bridge_cmd(self, cmd: str) -> Any:
        if cmd.startswith("extractor-cloze"):
            (save_cmd, clozetext) = cmd.split(":", 1)
            self.parent.make_cloze(clozetext)

        elif cmd.startswith("extractor-extract"):
            (save_cmd, extract) = cmd.split(":", 1)
            self.parent.make_extract(extract)

        elif cmd == "extractor-loaded":
            self.parent.enable()
