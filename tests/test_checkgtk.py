from autotest import checkgtk

def test_checkGtk():
    assert checkgtk.checkGtk('yelp', 'fr_FR') == 0  #Return a 0 exit status for a valid program.
