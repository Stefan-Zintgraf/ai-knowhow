# -*- coding: utf-8 -*-
#
# Project specific configuration file for the Sphinx documentation builder.
#

# -- Import common options for all projects ----------------------------------
from conf import *

# -- Project information -----------------------------------------------------
project = 'EC-Simulator'
product = 'EC-Simulator'

ecsimulator_doc_type = os.getenv('ECSIMULATOR_DOCTYPE', "User Manual")
edition = os.getenv('ECSIMULATOR_EDITION', "HiL")
ecsimulator_atnumber = os.getenv('ECSIMULATOR_ATNUMBER', '').strip('" ')

# Replacements
rst_epilog = """
.. |Product| replace:: EC-Simulator
.. |StrongProduct| replace:: **EC-Simulator**
.. |R| unicode:: U+00AE
"""
tags.add('EcSimulator')

if edition == 'HiL':
  tags.add('EcSimulatorHiL')
  rst_epilog += """
.. |Edition| replace:: HiL
.. |StrongEdition| replace:: **HiL**
.. |FileEdition| replace:: :file:`HiL`
.. |LcEdition| replace:: Hil
.. |EcatInitStack| replace:: :cpp:func:`esInitSimulator`
.. |EcatDeinitStack| replace:: :cpp:func:`esDeinitSimulator`
"""
else:
  tags.add('EcSimulatorSiL')
  rst_epilog += """
.. |Edition| replace:: SiL
.. |StrongEdition| replace:: **SiL**
.. |FileEdition| replace:: :file:`SiL`
.. |LcEdition| replace:: Sil
.. |EcatInitStack| replace:: :cpp:func:`emInitMaster`
.. |EcatDeinitStack| replace:: :cpp:func:`emDeinitMaster`
"""

ecdemo_cmdline = ['INCLUDE_ECSIMULATORHILDEMO', 'INCLUDE_EMLL_ALL']

# -- Options for HTML output -------------------------------------------------
html_theme_options['nav_title'] = project

# -- Options for LaTeX output ------------------------------------------------
latex_headerlogo = '../../Common/Media/'+ project + '.png'
latex_additional_files = [latex_headerlogo]
latex_preamble  = r'\newcommand{{\headerlogo}}{{{}}}'''.format(Path(latex_headerlogo).name)
latex_preamble += r'\newcommand{{\atnumber}}{{{}}}'''.format(ecsimulator_atnumber)
latex_preamble += open(latex_custom_pagestyle, 'r', encoding='utf8').read()

latex_elements['releasename'] = project
latex_elements['preamble'] = latex_preamble

if "Release Notes" in ecsimulator_doc_type:
    release = 'V' + atem_version['major'] + '.' + atem_version['minor'] + '.' + atem_version['servpack'] + '.' + atem_version['build']

latex_filename = 'EC-Simulator_' + ecsimulator_doc_type.strip('"').replace(' ', '')
latex_title = ecsimulator_doc_type

latex_documents = [
    (master_doc, latex_filename + ".tex", latex_title,
     author, "manual"),
]

# -- Extension configuration -------------------------------------------------
breathe_projects = { "EC-Simulator": "../_build/doxygen/xml/" }
breathe_default_project = "EC-Simulator"
panels_add_bootstrap_css = False
