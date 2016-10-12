import polib
import os
import pyatspiwrapper


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

    li = []
    translated = []
    untranslated = []

    pyatspiwrapper.getAppStrings(app, li)

    li = [x for x in li if x]

    for line in li:
        try:
            line = unicode(line)
            if line in po_dict:
                print True,
                translated.append(line)
            else:
                untranslated.append(line)
        except:
            untranslated.append(line)

    return translated, untranslated
