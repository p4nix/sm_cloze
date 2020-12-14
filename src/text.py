

class TextManager:
    def cloze(self):
        if not mw.web.selectedText():
            showInfo("Please select some text to cloze!")
            return

        #mw.web.evalWithCallback("getHtmlText()", )
