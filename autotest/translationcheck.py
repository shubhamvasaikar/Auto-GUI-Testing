import polib
import os
import pyatspiwrapper
import getpass

unicode_ranges = {
    'zh_CN': range(0x4E00, 0x9FFF),
    'zh_TW': range(0x4E00, 0x9FFF),
    'ko_KR': range(0x4E00, 0x9FFF),
    'ru_RU': range(0x0400, 0x052F)
}


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


def checkTranslations(program_name, locale_code):
    user = getpass.getuser()
    home = ""
    if user != "root":
        home = "/home/" + user
    else:
        home = "/root"
    extracted_strings_dir = home + "/.autotest/extracted_strings"
    if not os.path.exists(extracted_strings_dir):
        os.makedirs(extracted_strings_dir)
    extracted_strings_file = extracted_strings_dir + "/" + program_name + "." + locale_code

    app = pyatspiwrapper.getAppReference(program_name)

    translated = []
    untranslated = []
    app_strings = pyatspiwrapper.getAppStrings(app)

    with open(extracted_strings_file, 'w') as f:
        for line in app_strings:
            f.write("%s\n" % line.encode('utf-8'))

    for line in app_strings:
        flag = False
        rep = line.encode("unicode_escape")
        chars = rep.split('\u')
        chars = chars[1:]
        for code in chars:
            try:
                if int(code, 16) in unicode_ranges[locale_code]:
                    translated.append(line)
                    flag = True
                    break
            except:
                continue

        if not flag:
            untranslated.append(line)

    return untranslated
