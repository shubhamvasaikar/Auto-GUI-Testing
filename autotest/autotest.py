import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import checkgtk

class Handler:
    def on_MyWindow_delete_event(self, *args):
        Gtk.main_quit(*args)

    def on_startButton_clicked(self, button):
        prgmNameEntry = builder.get_object("prgmName")
        displayEntry = builder.get_object("display")
        isGtk = checkgtk.checkGtk(prgmNameEntry.get_text())
        if isGtk == 0:
            displayEntry.set_text("Program is GTK.")
        else:
            displayEntry.set_text("Program is non-GTK.")

builder = Gtk.Builder()
builder.add_from_file("autotest.glade")
builder.connect_signals(Handler())

window = builder.get_object("MyWindow")
window.show_all()

Gtk.main()
