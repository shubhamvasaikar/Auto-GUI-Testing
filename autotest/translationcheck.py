import polib
import os
import pyatspiwrapper
from fuzzywuzzy import fuzz, process


def extractStringsFromPo(po_name, locale_code):
    home = os.path.expanduser('~')
    po_dir = home + "/.autotest/pot_files/"
    po_path = po_dir + "/" + locale_code + "." + po_name + ".po"

    po = polib.pofile(po_path)

    po_dict = {}

    for entry in po:
        po_dict[entry.msgstr.replace("_", "")] = entry.msgid

    for i in po_dict:
        print i + ":" + po_dict[i]

    return po_dict


def checkTranslations(program_name, po_dict):
    app = pyatspiwrapper.getAppReference(program_name)

    translated = {}
    untranslated = {}
    app_strings = pyatspiwrapper.getAppStrings(app)

    localized = po_dict.keys()

    # for line in app_strings:
    #     try:
    #         if line in localized:
    #             translated.append(line)
    #         else:
    #             untranslated.append(line)
    #     except:
    #         untranslated.append(line)

    for line in app_strings:
        try:
            score = process.extractBests(line, localized, scorer=fuzz.ratio, limit=1)
            if score[0][1] >= 65:
                translated[line] = score
            else:
                untranslated[line] = score
        except:
            pass

    print 'done.'
    return translated, untranslated
