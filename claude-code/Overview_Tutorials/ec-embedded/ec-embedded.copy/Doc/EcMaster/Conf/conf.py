# -*- coding: utf-8 -*-
#
# Project specific configuration file for the Sphinx documentation builder.
#

# -- Import common options for all projects ----------------------------------
from conf import *

# -- Project information -----------------------------------------------------
project = 'EC-Master'

ecmaster_class = os.getenv('ECMASTER_CLASS', 'B')
ecmaster_fp = os.getenv('ECMASTER_FP', '').strip('\"')
ecmaster_release_notes = os.getenv('ECMASTER_RELEASE_NOTES')
ecmaster_atnumber = os.getenv('ECMASTER_ATNUMBER', '').strip('" ')

# Replacements
rst_epilog = """
.. |Product| replace:: EC-Master
.. |EcatInitStack| replace:: :cpp:func:`emInitMaster`
.. |EcatDeinitStack| replace:: :cpp:func:`emDeinitMaster`
"""
tags.add('EcMaster')

# EcDemo command line includes
if 'A' == ecmaster_class:
    ecdemo_cmdline = ['INCLUDE_ECMASTERDEMODC']
else:
    ecdemo_cmdline = ['INCLUDE_ECMASTERDEMO', 
                      'INCLUDE_EMLL_ALL']

# -- Options for HTML output -------------------------------------------------

html_theme_options['nav_title'] = project

# -- Options for LaTeX output ------------------------------------------------
latex_headerlogo = '../../Common/Media/'+ project + '.png'
latex_additional_files = [latex_headerlogo]
latex_preamble  = r'\newcommand{{\headerlogo}}{{{}}}'''.format(Path(latex_headerlogo).name)
latex_preamble += r'\newcommand{{\atnumber}}{{{}}}'''.format(ecmaster_atnumber)
latex_preamble += open(latex_custom_pagestyle, 'r', encoding='utf8').read()

latex_elements['releasename'] = project
latex_elements['preamble'] = latex_preamble

latex_filename = 'EC-Master'
latex_title = ''

if ecmaster_fp:
    latex_filename += '-FP-' + ecmaster_fp
    latex_title += 'Feature Pack ' + ecmaster_fp
elif ecmaster_release_notes:
    latex_filename += '_ReleaseNotes'
    latex_title += 'Release Notes'
    release = 'V' + atem_version['major'] + '.' + atem_version['minor'] + '.' + atem_version['servpack'] + '.' + atem_version['build']
else:
    latex_filename += '_Class' + ecmaster_class
    latex_title += 'EtherCAT® Master Stack Class ' + ecmaster_class

latex_documents = [
    (master_doc, latex_filename + '.tex', latex_title,
     author, 'manual'),
]

# -- Extension configuration -------------------------------------------------
breathe_projects = { 'EC-Master': '../_build/doxygen/xml/' }
breathe_default_project = 'EC-Master'
