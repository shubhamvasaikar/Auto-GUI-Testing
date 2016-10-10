import pyatspi


def getAppReference(program_name):
    desktop = pyatspi.Registry.getDesktop(0)

    for app in desktop:
        if program_name in app.name:
            return app


def getAppStrings(app, li):
    name = app.name.decode('utf-8')
    li.append(name)

    for tree in app:
        getAppStrings(tree, li)
