from aqt import mw

import aqt
from aqt import mw, gui_hooks
from aqt.utils import showInfo
from anki.consts import MODEL_STD
from .html import js, text_front, text_back, cloze_back, cloze_front, css

from .utils import get_config_value
from .consts import ADDON_NAME, EXTRACT_MODEL, EXTRACT_FLDS, EXTRACT_FLDS_IDS, EXTRACT_CARD, EXTRACT_MAX


def check_model(model):
    """Sanity check for the model and fields"""


def add_model(col):
    models = col.models
    model = models.new(EXTRACT_MODEL)
    model['type'] = MODEL_STD
    model['css'] = css
    model['sortf'] = 0 # set sortfield to Text

    # add fields
    for i in EXTRACT_FLDS_IDS:
        if i == "c_":
            for n in range(1, EXTRACT_MAX+1):
                cname = EXTRACT_FLDS["c_"] + str(n)
                fld = models.newField(cname)
                fld["size"] = 12
                models.addField(model, fld)

                template = models.newTemplate(cname)
                template['qfmt'] = cloze_front % (cname, cname, js, cname)
                template['afmt'] = cloze_back % cname
                models.addTemplate(model, template)
            continue
        fld = models.newField(EXTRACT_FLDS[i])
        models.addField(model, fld)

        if i == "tx":
            template = models.newTemplate("Text")
            template['qfmt'] = text_front
            template['afmt'] = text_back
            models.addTemplate(model, template)

    models.add(model)
    return model


def update_templates():
    col = mw.col
    model = col.models.byName(EXTRACT_MODEL)

    # change first template
    template = model['tmpls'][0]
    template['qfmt'] = text_front
    template['afmt'] = text_back
    model['css'] = css

    for i in range(1, EXTRACT_MAX + 1):
        cname = "c"+str(i)
        template = model['tmpls'][i]
        template['qfmt'] = cloze_front % (cname, cname, js, cname)
        template['afmt'] = cloze_back % cname

    col.models.save(model)

    return model


def initialize_models():
    model = mw.col.models.byName(get_config_value("model_name"))
    if not model:
        model = add_model(mw.col)

    update_templates()
