import pyatspi
from pyatspi import utils, role
import random
import gi
import time
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from PIL import Image


def getAppReference(program_name):
    desktop = pyatspi.Registry.getDesktop(0)

    for app in desktop:
        if program_name in app.name:
            return app


def traverse(app, li):
    name = app.name.decode('utf-8')
    li.append(name)

    for tree in app:
        traverse(tree, li)


def getAppStrings(app):
    # predicate = lambda x: ((x.getRole() == role.ROLE_MENU) or (x.getRole() == role.ROLE_MENU_ITEM))
    buttons = utils.findAllDescendants(app, lambda x: (
    (x.getRole() == role.ROLE_MENU) or (x.getRole() == role.ROLE_MENU_ITEM)))

    for button in buttons:
        button.do_action(0)

    strings = []

    traverse(app, strings)

    strings = [s for s in strings if s]
    return strings


def getWidgetLocations(app, count):
    count += 1
    if count > 5:
        return
    location = app.queryComponent().getPosition(0)
    size = app.queryComponent().getSize()
    x1 = location[0]
    y1 = location[1]
    width = size[0] + (8 - (size[0] % 8))
    height = size[1] + (8 - (size[1] % 8))

    app.queryComponent().grabFocus()
    time.sleep(1)
    im = None
    if (size[0] > 1) and (size[1] > 1):
        im = takeScreenshots(x1, y1, width, height)
        im = im.crop((0, 0, size[0], size[1]))
    if im:
        im.save(app.name + str(random.randint(1, 100)) + '.png')

    if app.getRole() == role.ROLE_PUSH_BUTTON:
        app.do_action(0)

    for tree in app:
        getWidgetLocations(tree, count)


def takeScreenshots(x, y, width, height):
    w = Gdk.get_default_root_window()
    sz = [0, 0]
    sz[0] = w.get_width()
    sz[1] = w.get_height()
    pb = Gdk.pixbuf_get_from_window(w, x, y, width, height)
    # pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
    if pb == None:
        return False
    else:
        width, height = pb.get_width(), pb.get_height()
    return Image.frombytes("RGB", (width, height), pb.get_pixels())
