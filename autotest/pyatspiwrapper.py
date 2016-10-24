import pyatspi
from pyatspi import utils, role


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
    # predicate = lambda x: x.getRole() == role.ROLE_PUSH_BUTTON
    buttons = utils.findAllDescendants(app, lambda x: x.getRole() == role.ROLE_PUSH_BUTTON)

    for button in buttons:
        button.do_action(0)

    strings = []

    traverse(app, strings)

    strings = [s for s in strings if s]
    return strings
