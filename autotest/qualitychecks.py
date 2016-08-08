import os
import subprocess


def extractPoFiles(program_name, locale):
    """ Generate all the .po files from the
        .mo files.
    """

    home_dir = os.path.expanduser('~')
    output_dir = home_dir+"/.autotest/pofiles"  # Path to store .po files
    
    # Create directory for .po files.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_path = "/usr/share/locale/"+locale+"/LC_MESSAGES/"+program_name+".mo"
    output_path = output_dir+"/"+locale+"."+program_name+".po"

    # msgunfmt is used to convert .mo files to .po files.
    command = "msgunfmt "+input_path+" > "+output_path
    subprocess.call(command, shell=True)


def runPofilter(program_name, locale):
    """ Run pofilter on all generated .po files.
    """

    home_dir = os.path.expanduser('~')
    input_dir = home_dir+"/.autotest/pofiles"  # Path for .po files
    output_dir = home_dir+"/.autotest/pofilter_files"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_path = input_dir+"/"+locale+"."+program_name+".po"
    output_path = output_dir+"/filter."+locale+"."+program_name+".po"

    # pofilter is obtained from translate-toolkit.
    # pofilter is used to run various quality checks on .po files.
    command = "pofilter -i "+input_path+" -o "+output_path
    subprocess.call(command, shell=True)
