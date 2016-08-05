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

    def hide_window(self, window, event):
        window.hide()
        return True

    # To open Nautilus window to view pofilter files.
    def open_pofilter_dir(self, button):
        subprocess.Popen("nautilus ~/.autotest/pofilter_files", shell=True)

    # Start program when the start button is clicked.
    def on_start(self, button):
        # builder.get_object used to get reference of gui objects.
        prgmNameEntry = builder.get_object("prgmName")
        localeCombo = builder.get_object("localeComboBox")
        displayTextView = builder.get_object("displayTests")
        locale_absent = None

        # Set some frequently used variables
        program_name = prgmNameEntry.get_text()
        locale = localeCombo.get_active_text()

        autoTestWindow.present()
        displayTextView.get_buffer().set_text("")

        # Start the program in given locale.
        isGtk = 0
        isGtk = checkgtk.checkGtk(program_name, locale)
        if (builder.get_object("gtkCheckBtn").get_active()):
            if isGtk == 0:
                end_iter = displayTextView.get_buffer().get_end_iter()
                displayTextView.get_buffer().insert(end_iter, "Program is GTK.\n")
            else:
                end_iter = displayTextView.get_buffer().get_end_iter()
                displayTextView.get_buffer().insert(end_iter, "Program is non-GTK.\n")

        # Check the presence of l10n files for all locales
        if (builder.get_object("localeCheckBtn").get_active()):
            locale_absent = checklocales.checkLocales(program_name)
            if len(locale_absent) == 0:
                end_iter = displayTextView.get_buffer().get_end_iter()
                displayTextView.get_buffer().insert(end_iter, "All locales are present.\n")
            else:
                locale_absent = ', '.join(locale_absent)
                end_iter = displayTextView.get_buffer().get_end_iter()
                displayTextView.get_buffer().insert(end_iter, "These locales are not present: "+locale_absent+"\n")

        if (builder.get_object("pofilterCheckBtn").get_active()):
            qualitychecks.extractPoFiles(program_name, locale_absent)
            qualitychecks.runPofilter(program_name, locale_absent)
            end_iter = displayTextView.get_buffer().get_end_iter()
            displayTextView.get_buffer().insert(end_iter, "Pofilter run successfully.\n")
            btnPofilter = builder.get_object("pofilterBtn")
            btnPofilter.set_sensitive(True)

builder = Gtk.Builder()
builder.add_from_file("autotest.glade")
builder.connect_signals(Handler())

configTestWindow = builder.get_object("configTest")
autoTestWindow = builder.get_object("autoTest")
configTestWindow.show_all()

Gtk.main()
