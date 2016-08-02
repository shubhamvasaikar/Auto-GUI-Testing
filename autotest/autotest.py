import gi
import checkgtk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:

    # To end program when close button is pressed.
    def on_close(self, *args):
        Gtk.main_quit(*args)

    # Start program when the start button is clicked.
    def on_start(self, button):
        # builder.get_object used to get reference of gui objects.
        prgmNameEntry = builder.get_object("prgmName")
        localeEntry = builder.get_object("locale")
        displayEntry = builder.get_object("display")

        # Start the program in given locale.
        isGtk = checkgtk.checkGtk(prgmNameEntry.get_text(), localeEntry.get_text())
        if isGtk == 0:
            displayEntry.set_text("Program is GTK.")
        else:
            displayEntry.set_text("Program is non-GTK.")

builder = Gtk.Builder()
builder.add_from_file("autotest.glade")
builder.connect_signals(Handler())

window = builder.get_object("mainWindow")
window.show_all()

Gtk.main()
