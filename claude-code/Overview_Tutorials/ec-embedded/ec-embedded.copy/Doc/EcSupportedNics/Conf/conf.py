# -*- coding: utf-8 -*-
#
# Project specific configuration file for the Sphinx documentation builder.
#

# -- Import common options for all projects ----------------------------------
from conf import *

# -- Project information -----------------------------------------------------
project = 'Supported NICs'

# -- Options for HTML output -------------------------------------------------

html_theme_options['nav_title'] = project + ' V' + version

html_css_files = html_css_files + [
    'https://cdn.datatables.net/1.10.23/css/jquery.dataTables.min.css'
    ]
html_js_files = [
    'https://cdn.datatables.net/1.10.23/js/jquery.dataTables.min.js',
    'main.js' 
]

## -- Options for LaTeX output ------------------------------------------------
#latex_headerlogo = '../../Common/Media/'+ project + '.png'
#latex_additional_files = [latex_headerlogo]
#latex_preamble = r'\newcommand{{\headerlogo}}{{{}}}'''.format(Path(latex_headerlogo).name)
#latex_preamble += open(latex_custom_pagestyle, "r", encoding="utf8").read()

#latex_elements['releasename'] = project
#latex_elements['preamble'] = latex_preamble
#latex_documents = [
#    (master_doc, 'EcSupportedNics.tex', 'Supported-NICs',
#     author, 'manual'),
#]

# -- Extension configuration -------------------------------------------------

breathe_projects = { "Supported-NICs": "../_build/doxygen/xml/" }
breathe_default_project = "Supported-NICs"
