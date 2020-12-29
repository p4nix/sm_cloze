from aqt import mw

ADDON_NAME = mw.addonManager.addonFromModule(__name__)

EXTRACT_MODEL = "ALL_SMCloze"
EXTRACT_CARD = "smcloze"
EXTRACT_MAX = 20

EXTRACT_FLDS = {
    'tx': "Text",
    'ex': "Extra",
    'cx': "Context",
    'sc': "Source",
    'c_': "c",
    'p_id': "Parent NIDs",
    'c_id': "Child NIDs"
}

EXTRACT_FLDS_IDS = ['tx', 'ex', 'cx', 'sc', 'c_', 'p_id', 'c_id']
