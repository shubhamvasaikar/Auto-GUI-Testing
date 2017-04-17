# -*- coding: utf-8 -*-

import subprocess
import autotest.checkgtk as checkgtk
import autotest.checklocales as checklocales
import autotest.qualitychecks as qualitychecks
import autotest.extractpot as extractpot
import autotest.translationcheck as translationcheck
import autotest.extractwidgets as extractwidgets
import logging
from autotest import template_dict
import shlex
import jinja2
import datetime
import os
import time

log = logging.getLogger(__name__)

locales = {'pt_BR': 'pt_BR',
           'zh_CN': 'zh_CN',
           'zh_TW': 'zh_TW',
           'ja_JP': 'ja',
           'ko_KR': 'ko',
           'fr_FR': 'fr',
           'de_DE': 'de',
           'it_IT': 'it',
           'ru_RU': 'ru',
           'es_ES': 'es'
           }


def build_report(app_name, template_dict):
    report_dir = os.path.abspath('./autotest/reports/')
    print report_dir
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(report_dir))

    template = jinja_env.get_template('report_template.html')
    report = template.render(template_dict)

    with open(os.path.join(report_dir, app_name + ".report.html"), 'w') as f:
        f.write(report.encode('utf-8'))


def run(app_name, locale):
    # Set some frequently used variables
    template_dict['app_name'] = app_name
    template_dict['lang_code'] = locale
    locale_id = locales[locale]
    template_dict['app_ver'] = '0.0.1'
    template_dict['app_rel'] = 'f25'
    template_dict['sys_arch'] = 'x86_64'
    template_dict['rep_date'] = datetime.datetime.now().strftime("%Y-%m-%d")

    # Start the program in given locale.
    isGtk = checkgtk.checkGtk(app_name, locale)
    template_dict['isGtk'] = isGtk

    # Check the presence of l10n files for all locales.
    locale_present = checklocales.checkLocales(app_name, locale_id)
    if locale_present:
        template_dict['po_exist'] = True
    else:
        template_dict['po_exist'] = False

    # Extract the .po file and run pofilter on it.
    qualitychecks.extractPoFiles(app_name, locale_id)
    qualitychecks.runPofilter(app_name, locale_id)
    template_dict['pot_exist'] = True

    # Extract .pot file and get translation stats.
    extract_pot = extractpot.ExtractPot(app_name, locale_id)
    stat_dict = extract_pot.getStats()
    template_dict['translated'] = stat_dict["translated"]
    template_dict['fuzzy'] = stat_dict['fuzzy']
    template_dict['untranslated'] = stat_dict['untranslated']
    template_dict['per_translated'] = (float(stat_dict['translated']) / float(stat_dict['total'])) * 100
    template_dict['per_fuzzy'] = (float(stat_dict['fuzzy']) / float(stat_dict['total'])) * 100
    template_dict['per_untranslated'] = (float(stat_dict['untranslated']) / float(stat_dict['total'])) * 100

    # Check for translation errors.
    template_dict['untranslated_list'] = translationcheck.checkTranslations(app_name, locale)
    checkgtk.kill(app_name)

    # Check for bad rendering and save screenshots.
    checkgtk.checkGtk(app_name, locale)
    extract_widgets = extractwidgets.ExtractWidgets(app_name, locale)
    extract_widgets.extractWidgets()
    extract_widgets.cleanImages()
    template_dict['bad_renders_list'] = extract_widgets.checkRendering()
    checkgtk.kill(app_name)

    # Build Report
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    build_report(template_dict)
