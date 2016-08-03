import gi
import subprocess
import checkgtk
import checklocales
import qualitychecks
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:

    # To end program when close button is pressed.
    def on_close(self, *args):
        Gtk.main_quit(*args)

    # To open Nautilus window to view pofilter files.
    def open_pofilter_dir(self, button):
        subprocess.Popen("nautilus ~/.autotest/pofilter_files", shell=True)

    # Start program when the start button is clicked.
    def on_start(self, button):
        # builder.get_object used to get reference of gui objects.
        prgmNameEntry = builder.get_object("prgmName")
        localeEntry = builder.get_object("locale")
        label0Entry = builder.get_object("label0")
        label1Entry = builder.get_object("label1")
        labelPofilter = builder.get_object("labelPofilter")
        btnPofilter = builder.get_object("btnPofilter")

        # Set some frequently used variables
        program_name = prgmNameEntry.get_text()
        locale = localeEntry.get_text()

        # Start the program in given locale.
        isGtk = 0
        isGtk = checkgtk.checkGtk(program_name, locale)
        if isGtk == 0:
            label0Entry.set_text("Program is GTK.")
        else:
            label0Entry.set_text("Program is non-GTK.")

        # Check the presence of l10n files for all locales
        locale_absent = checklocales.checkLocales(program_name)
        if len(locale_absent) == 0:
            label1Entry.set_text("All supported locales present.")
        else:
            locale_absent = ', '.join(locale_absent)
            label1Entry.set_text("These locales are not present: "+locale_absent)

        qualitychecks.extractPoFiles(program_name, locale_absent)
        qualitychecks.runPofilter(program_name, locale_absent)
        labelPofilter.set_text("Pofilter run successfully.")
        btnPofilter.set_sensitive(True)

builder = Gtk.Builder()
builder.add_from_file("autotest.glade")
builder.connect_signals(Handler())

window = builder.get_object("mainWindow")
window.show_all()

Gtk.main()
