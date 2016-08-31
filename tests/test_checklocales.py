from autotest import checklocales


def test_checkLocales():
    locale_absent = checklocales.checkLocales("yelp", "de")
    # locale_absent must be true if locale is present.
    assert locale_absent
