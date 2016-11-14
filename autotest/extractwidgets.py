import pyatspiwrapper
import os

global count
count = 0


def extractWidgets(app_name):
    app = pyatspiwrapper.getAppReference(app_name)
    os.chdir("/home/svasaika/.autotest/images/gedit/")
    app = app[0]

    pyatspiwrapper.getWidgetLocations(app, count)
    print "done."
