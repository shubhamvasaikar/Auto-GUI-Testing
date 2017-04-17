import logging
import logging.config

formatter = "%(asctime)s - %(levelname)-6s: %(name)s: %(message)s"
logging.basicConfig(filename="autotest.log", filemode='w', format=formatter, level=logging.NOTSET)
logging.getLogger(__name__)

template_dict = {
    'app_name': '',
    'lang_code': '',
    'app_ver': '',
    'app_rel': '',
    'sys_arch': '',
    'rep_date': '',
    'isGtk': 0,
    'po_exist': True,
    'pot_exist': True,
    'translated': 0,
    'fuzzy': 0,
    'untranslated': 0,
    'per_translated': 0,
    'per_fuzzy': 0,
    'per_untranslated': 0,
    'untranslated_list': [],
    'bad_renders_list': [],
}
