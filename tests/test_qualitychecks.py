from autotest import qualitychecks
import os


def test_extractPoFile():
    qualitychecks.extractPoFiles("yelp", "fr")
    assert os.path.isfile("/home/svasaika/.autotest/pot_files/fr.yelp.po")


def test_runPofilter():
    qualitychecks.runPofilter("yelp", "fr")
    assert os.path.isfile("/home/svasaika/.autotest/pofilter_files/filter.fr.yelp.po")
