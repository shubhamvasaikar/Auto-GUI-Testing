# -*- coding: utf-8 -*-

import pyatspiwrapper
import os
import getpass
import shutil
from PIL import Image

global count
count = 0


class ExtractWidgets:
    def __init__(self, program_name, locale):
        self.program_name = program_name
        self.locale = locale

        self.user = getpass.getuser()
        self.home = ""

        if self.user != "root":
            self.home = "/home/" + self.user
        else:
            self.home = "/root"

        self.images_dir = self.home + "/.autotest/images/" + self.program_name

        self.extracted_strings = self.home + "/.autotest/extracted_strings/" + self.program_name + "." + self.locale

        if not os.path.exists(self.images_dir):
            shutil.rmtree(self.images_dir)
            os.makedirs(self.images_dir)

    def extractWidgets(self):
        app = pyatspiwrapper.getAppReference(self.program_name)
        os.chdir(self.images_dir)
        app = app[0]

        pyatspiwrapper.getWidgetLocations(app, count)
        print "done."

    def cleanImages(self):
        os.chdir(self.images_dir)
        images = os.listdir('./')
        for image in images:
            im = Image.open(image)
            im = im.resize((im.width * 3, im.height * 3), Image.ANTIALIAS)
            im = im.convert('L')
            im = im.point(lambda x: 0 if x < 175 else 255, '1')
            im.save(image)

    def checkRendering(self):
        with open(self.extracted_strings, 'r') as f:
            app_strings = f.readlines()

        bad_renders = []

        for line in app_strings:
            line = line.decode('utf-8')
            if u'◌' in line:
                bad_renders.append(line)

        return bad_renders
