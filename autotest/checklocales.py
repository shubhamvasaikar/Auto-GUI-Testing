import os

def checkLocales(program_name, locale):
    """ Check if l10n files are present
        for all supported locales
    """

    # Create a path for the l10n file.
    path = "/usr/share/locale/"+locale+"/LC_MESSAGES/"+program_name+".mo"

    if (os.path.isfile(path)):           # If file does not exist
        return True 
    else:
        return False 


def test_checkLocales():
    locale_absent = checkLocales("yelp", "de")
    # locale_absent must be empty if all supported locales present.
    assert locale_absent
