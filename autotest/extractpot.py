import urllib
import os
import getpass
import subprocess
import tarfile
import shlex
import logging

log = logging.getLogger(__name__)


class ExtractPot:
    """This class is used to extract the pot file.
       It works by downloading the src package from
       Koji and unpacking the rpm and extracting the .pot file.
       Then translation statistics are generated.
    """

    def __init__(self, program_name, locale):
        self.program_name = program_name
        self.locale = locale

        self.user = getpass.getuser()
        self.home = ""

        if self.user != "root":
            self.home = "/home/"+self.user
        else:
            self.home = "/root"

        self.srpm_dir = self.home+"/.autotest/srpm"
        self.srpm_path = self.srpm_dir+"/"+self.program_name+".src.rpm"

        if not os.path.exists(self.home+"/.autotest/pot_files"):
            os.makedirs(self.home+"/.autotest/pot_files")

        if not os.path.exists(self.home+"/.autotest/srpm"):
            os.makedirs(self.home+"/.autotest/srpm")


    def extractPot(self):
        """Download the src.rpm from Koji package repo.
           Unpack the downloaded RPM and generate the .pot file.
           .pot file is then moved to ~/.autotest/pot_files.
        """

        top_url = "https://kojipkgs.fedoraproject.org/packages"
        pkg_path = subprocess.check_output(['rpm -qa '+self.program_name+' --queryformat %{NAME}/%{VERSION}/%{RELEASE}'], shell=True)
        pkg_name = subprocess.check_output(['rpm -qa '+self.program_name+' --queryformat %{NAME}-%{VERSION}-%{RELEASE}'], shell=True)
        tar_name = subprocess.check_output(['rpm -qa '+self.program_name+' --queryformat %{NAME}-%{VERSION}'], shell=True)
        pkg_url = top_url+"/"+pkg_path+"/src/"+pkg_name+".src.rpm"
        log.info("Download URL: %s", pkg_url)

        if not os.path.isfile(self.srpm_path):
            urllib.urlretrieve(pkg_url, self.srpm_path)
            log.info("src.rpm downloaded.")
        else:
            log.info("src.rpm already present, not downloading.")

        os.chdir(self.srpm_dir)

        command = "rpm2cpio "+self.program_name+".src.rpm"
        command = shlex.split(command)
        rpm2cpio = subprocess.Popen(command, stdout=subprocess.PIPE)
        command = "cpio -idm"
        command = shlex.split(command)
        subprocess.call(command, stdin=rpm2cpio.stdout)

        command = "tar -xf "+tar_name+".tar.xz"
        command = shlex.split(command)
        subprocess.call(command)
        log.info("src.rpm unpacked in %s", self.srpm_dir)

        os.chdir(self.srpm_dir+"/"+tar_name+"/po")

        command = "intltool-update -p"
        command = shlex.split(command)
        subprocess.call(command)
        log.info("TODO insert command output here.")

        pot_name = self.program_name+".pot"

        os.rename(pot_name, self.home+"/.autotest/pot_files/"+pot_name)

        os.chdir(os.path.abspath(os.path.dirname(__file__)))


    def getStats(self):
        """Get the translaton statistics on the .po file
           using the msgfmt utility.
        """
        path = self.home+"/.autotest/pot_files"
        os.chdir(path)
        po_file = self.locale+"."+self.program_name+".po"
        pot_name = self.program_name+".pot"

        command = "intltool-update --dist --gettext-package="+self.program_name+" "+self.locale+"."+self.program_name
        command = shlex.split(command)
        subprocess.call(command)
        log.info("TODO insert command output here.")

        command = "msgfmt --statistics "+po_file+" -o -"
        command = shlex.split(command)
        stats = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = stats.communicate()

        os.chdir(os.path.abspath(os.path.dirname(__file__)))

        return err


def test_extractPot():
    e = ExtractPot("yelp", "fr")
    e.extractPot()
    stats = e.getStats()
    assert os.path.isfile(e.home+"/.autotest/pot_files/yelp.pot")
