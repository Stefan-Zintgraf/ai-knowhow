# -*- coding: utf-8 -*-
#
# Project specific configuration file for the Sphinx documentation builder.
#

# -- Import common options for all projects ----------------------------------
from conf import *

sys.path.append(os.path.abspath("."))

# -- Project information -----------------------------------------------------
project = 'EC-Daq'

ecdaq_doc_type = os.getenv('ECDAQ_DOCTYPE', "User Manual")
ecdaq_atnumber = os.getenv('ECDAQ_ATNUMBER', '').strip('" ')

# -- General configuration ---------------------------------------------------

rst_epilog = """
.. |Product| replace:: EC-Daq
"""
tags.add('EcDaq')

ecdemo_cmdline = ['INCLUDE_ECMASTERDEMODAQ', 
                  'INCLUDE_EMLLINTELGBE', 'INCLUDE_EMLLNDIS', 'INCLUDE_EMLLSOCKRAW', 'INCLUDE_EMLLSNARF', 'INCLUDE_EMLLWINPCAP']

# -- Options for HTML output -------------------------------------------------
html_theme_options['nav_title'] = project

# -- Options for LaTeX output ------------------------------------------------
latex_headerlogo = '../../Common/Media/EC-Master.png'
latex_additional_files = [latex_headerlogo]
latex_preamble  = r'\newcommand{{\headerlogo}}{{{}}}'''.format(Path(latex_headerlogo).name)
latex_preamble += r'\newcommand{{\atnumber}}{{{}}}'''.format(ecdaq_atnumber)
latex_preamble += open(latex_custom_pagestyle, 'r', encoding='utf8').read()

latex_elements['releasename'] = project
latex_elements['preamble'] = latex_preamble

latex_filename = project + '_' + ecdaq_doc_type.strip('"').replace(' ', '')
latex_title = ecdaq_doc_type

latex_documents = [
    (master_doc, latex_filename + ".tex", latex_title,
     author, "manual"),
]

# -- Extension configuration -------------------------------------------------
breathe_projects = { "EC-Daq": "../_build/doxygen/xml/" }
breathe_default_project = "EC-Daq"
panels_add_bootstrap_css = False
