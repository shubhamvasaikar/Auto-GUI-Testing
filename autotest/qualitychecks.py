import os
import subprocess
import polib
import shlex
import logging

log = logging.getLogger(__name__)


def extractPoFiles(program_name, locale):
    """ Generate all the .po files from the
        .mo files.
    """

    home_dir = os.path.expanduser('~')
    output_dir = home_dir+"/.autotest/pot_files"  # Path to store .po files

    # Create directory for .po files.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        log.info("Directory %s created.", output_dir)

    mo_path = "/usr/share/locale/"+locale+"/LC_MESSAGES/"+program_name+".mo"
    po_path = output_dir+"/"+locale+"."+program_name+".po"

    # Use polib to convert .mo files to .po files.
    mo = polib.mofile(mo_path)
    mo.save_as_pofile(po_path)
    log.info(".po file saved at %s.", po_path)


def runPofilter(program_name, locale):
    """ Run pofilter on all generated .po files.
    """

    home_dir = os.path.expanduser('~')
    input_dir = home_dir+"/.autotest/pot_files"  # Path for .po files
    output_dir = home_dir+"/.autotest/pofilter_files"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        log.info("Directory %s created.", output_dir)

    input_path = input_dir+"/"+locale+"."+program_name+".po"
    output_path = output_dir+"/filter."+locale+"."+program_name+".po"

    # pofilter is obtained from translate-toolkit.
    # pofilter is used to run various quality checks on .po files.
    command = "pofilter -i "+input_path+" -o "+output_path
    command = shlex.split(command)
    subprocess.call(command)
