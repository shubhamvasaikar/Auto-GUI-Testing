from autotest import extractpot
import os


def test_extractPot():
    e = extractpot.ExtractPot("yelp", "fr")
    e.extractPot()
    stats = e.getStats()
    assert os.path.isfile(e.home+"/.autotest/pot_files/yelp.pot")
