import os
import logging

log = logging.getLogger(__name__)

def checkLocales(program_name, locale):
    """
    This function checks if the ``.mo`` file is present for the ``program_name``.
    The ``.mo`` file is the binary version of a ``.po`` file.

    :param program_name: The program which is to be launched.
    :param locale: The locale in which program is to be launched.
    :type program_name: str
    :type locale: str
    :returns: ``True`` if file is present. ``False`` if absent.
    :rtype: boolean
    """

    # Create a path for the .mo file.
    path = "/usr/share/locale/"+locale+"/LC_MESSAGES/"+program_name+".mo"

    if (os.path.isfile(path)):           # If file does not exist
        log.info(".mo file present.")
        return True
    else:
        log.error(".mo file not present.")
        return False
