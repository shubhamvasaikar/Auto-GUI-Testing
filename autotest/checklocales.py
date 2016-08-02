import os

# A list of all the supported locales.
locales = ['pt_BR',
           'zh_CN',
           'zh_TW',
           'ja',  # ja_JP
           'ko',  # ko_KR
           'fr',  # fr_FR
           'de',  # de_DE
           'it',  # it_IT
           'ru',  # ru_RU
           'es'   # es_ES
          ]


def checkLocales(program_name):
    """ Check if l10n files are present
        for all supported locales
    """
    locale_absent = []  # Initialize list for absent files.

    for locale in locales:

        # Create a path for the l10n file.
        path = "/usr/share/locale/"+locale+"/LC_MESSAGES/"+program_name+".mo"

        if (os.path.isfile(path) == False):  # If file does not exist
            locale_absent.append(locale)     # Add locale code to list

    return locale_absent


def test_checkLocales():
    locale_absent = checkLocales("yelp")
    # locale_absent must be empty if all supported locales present.
    assert len(locale_absent) == 0
