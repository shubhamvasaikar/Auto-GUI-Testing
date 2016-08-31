import os
import logging

log = logging.getLogger(__name__)

def checkLocales(program_name, locale):
    """ Check if l10n files are present
        for all supported locales
    """

    # Create a path for the .mo file.
    path = "/usr/share/locale/"+locale+"/LC_MESSAGES/"+program_name+".mo"

    if (os.path.isfile(path)):           # If file does not exist
        log.info(".mo file present.")
        return True
    else:
        log.error(".mo file not present.")
        return False 
