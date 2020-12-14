def add_model():
    cloze_modelname = get_config_value("model_name")

    if mw.col.models.byName(cloze_modelname):
        return

    model = mw.col.models.new(cloze_modelname)
#model['css'] = """
#    .card {
#
#
#        }
#    """

    i = 0
    for i <= get_config_value("num_clozes"):
        i += 1

        cloze_field = mw.col.models.newField("c" + str(i))
        mw.col.models.addField(model, cloze_field)
