import gi
import subprocess
import autotest.checkgtk as checkgtk
import autotest.checklocales as checklocales
import autotest.qualitychecks as qualitychecks
import autotest.extractpot as extractpot
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import logging
from autotest import template_dict
import shlex
import jinja2
import datetime
import os

log = logging.getLogger(__name__)

locales = ['pt_BR',
           'zh_CN',
           'zh_TW',
           'ja',
           'ko',
           'fr',
           'de',
           'it',
           'ru',
           'es'
           ]


def build_report(template_dict):
    report_dir = os.path.abspath('reports')
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(report_dir))

    template = jinja_env.get_template('report_template.html')
    report = template.render(template_dict)

    with open(os.path.join(report_dir, 'report.html'), 'w') as f:
        f.write(report)


class Handler:

    # To end program when close button is pressed.
    def on_close(self, *args):
        Gtk.main_quit(*args)

    def hide_window(self, window, event):
        window.hide()
        return True

    # To open Nautilus window to view pofilter files.
    def open_pofilter_dir(self, button):
        subprocess.Popen("nautilus ~/.autotest/pofilter_files", shell=True)

    # To open Nautilus window to view .pot files.
    def open_pot_dir(self, button):
        subprocess.Popen("nautilus ~/.autotest/pot_files", shell=True)

    # Start program when the start button is clicked.
    def on_start(self, button):
        # builder.get_object used to get reference of gui objects.
        prgmNameEntry = builder.get_object("prgmName")
        localeCombo = builder.get_object("localeComboBox")
        displayTextView = builder.get_object("displayTests")

        # Set some frequently used variables
        program_name = prgmNameEntry.get_text().strip()
        template_dict['app_name'] = program_name
        locale = localeCombo.get_active_text()
        template_dict['lang_code'] = locale
        locale_id = localeCombo.get_active()
        command = 'rpm -qa ' + program_name + ' --queryformat %{VERSION}\ %{RELEASE}\ %{ARCH}'
        command = shlex.split(command)
        ver, rel, arch = subprocess.check_output(command).split()
        template_dict['app_ver'] = ver
        template_dict['app_rel'] = rel
        template_dict['sys_arch'] = arch
        template_dict['rep_date'] = datetime.datetime.now().strftime("%Y-%m-%d")

        autoTestWindow.present()
        displayTextView.get_buffer().set_text("")

        # Start the program in given locale.
        isGtk = 0
        isGtk = checkgtk.checkGtk(program_name, locale)
        if (builder.get_object("gtkCheckBtn").get_active()):
            if isGtk == 0:
                end_iter = displayTextView.get_buffer().get_end_iter()
                displayTextView.get_buffer().insert(end_iter, "Program is GTK.\n")
                template_dict['isGtk'] = isGtk
            else:
                end_iter = displayTextView.get_buffer().get_end_iter()
                displayTextView.get_buffer().insert(end_iter, "Program is non-GTK.\n")
                template_dict['isGtk'] = isGtk

        # Check the presence of l10n files for all locales.
        if (builder.get_object("localeCheckBtn").get_active()):
            locale_present = checklocales.checkLocales(program_name, locales[locale_id])
            if locale_present:
                end_iter = displayTextView.get_buffer().get_end_iter()
                displayTextView.get_buffer().insert(end_iter, "Required locale is present.\n")
                template_dict['po_exist'] = True
            else:
                end_iter = displayTextView.get_buffer().get_end_iter()
                displayTextView.get_buffer().insert(end_iter, "Required locale is not present.\n")
                template_dict['po_exist'] = True

        # Extract the .po file and run pofilter on it.
        if (builder.get_object("pofilterCheckBtn").get_active()):
            qualitychecks.extractPoFiles(program_name, locales[locale_id])
            qualitychecks.runPofilter(program_name, locales[locale_id])
            end_iter = displayTextView.get_buffer().get_end_iter()
            displayTextView.get_buffer().insert(end_iter, "Pofilter run successfully.\n")
            btnPofilter = builder.get_object("pofilterBtn")
            btnPofilter.set_sensitive(True)
            template_dict['pot_exist'] = True

        # Extract .pot file and get translation stats.
        if (builder.get_object("statCheckBtn").get_active()):
            extract_pot = extractpot.ExtractPot(program_name, locales[locale_id])
            extract_pot.extractPot()
            stat_dict = extract_pot.getStats()
            end_iter = displayTextView.get_buffer().get_end_iter()
            displayTextView.get_buffer().insert(end_iter, str(stat_dict) + "\n")
            btnPotDir = builder.get_object("potDirBtn")
            btnPotDir.set_sensitive(True)
            template_dict['translated'] = stat_dict['translated']
            template_dict['fuzzy'] = stat_dict['fuzzy']
            template_dict['untranslated'] = stat_dict['untranslated']
            template_dict['per_translated'] = (float(stat_dict['translated']) / float(stat_dict['total'])) * 100
            template_dict['per_fuzzy'] = (float(stat_dict['fuzzy']) / float(stat_dict['total'])) * 100
            template_dict['per_untranslated'] = (float(stat_dict['untranslated']) / float(stat_dict['total'])) * 100

        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        build_report(template_dict)

builder = Gtk.Builder()
builder.add_from_file("autotest/autotest.glade")
builder.connect_signals(Handler())

configTestWindow = builder.get_object("configTest")
autoTestWindow = builder.get_object("autoTest")
configTestWindow.show_all()

Gtk.main()
