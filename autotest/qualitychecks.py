import os
import subprocess
import polib


def extractPoFiles(program_name, locale):
    """ Generate all the .po files from the
        .mo files.
    """

    home_dir = os.path.expanduser('~')
    output_dir = home_dir+"/.autotest/pot_files"  # Path to store .po files

    # Create directory for .po files.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mo_path = "/usr/share/locale/"+locale+"/LC_MESSAGES/"+program_name+".mo"
    po_path = output_dir+"/"+locale+"."+program_name+".po"

    # Use polib to convert .mo files to .po files.
    mo = polib.mofile(mo_path)
    mo.save_as_pofile(po_path)


def runPofilter(program_name, locale):
    """ Run pofilter on all generated .po files.
    """

    home_dir = os.path.expanduser('~')
    input_dir = home_dir+"/.autotest/pot_files"  # Path for .po files
    output_dir = home_dir+"/.autotest/pofilter_files"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_path = input_dir+"/"+locale+"."+program_name+".po"
    output_path = output_dir+"/filter."+locale+"."+program_name+".po"

    # pofilter is obtained from translate-toolkit.
    # pofilter is used to run various quality checks on .po files.
    command = "pofilter -i "+input_path+" -o "+output_path
    subprocess.call(command, shell=True)


def test_extractPoFile():
    extractPoFiles("yelp", "fr")
    assert os.path.isfile("/home/svasaika/.autotest/pot_files/fr.yelp.po")


def test_runPofilter():
    runPofilter("yelp", "fr")
    assert os.path.isfile("/home/svasaika/.autotest/pofilter_files/filter.fr.yelp.po")
