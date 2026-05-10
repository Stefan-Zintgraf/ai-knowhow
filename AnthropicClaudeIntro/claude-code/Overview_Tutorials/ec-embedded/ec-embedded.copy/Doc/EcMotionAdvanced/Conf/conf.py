# -*- coding: utf-8 -*-
#
# Project specific configuration file for the Sphinx documentation builder.
#

# -- Import common options for all projects ----------------------------------
from conf import *

sys.path.append(os.path.abspath("."))

# -- Project information -----------------------------------------------------
project = 'EC-Motion-Advanced'

ecmotion_doc_type = os.getenv('ECMOTION_DOCTYPE', "User Manual")
ecmotion_atnumber = os.getenv('ECMOTION_ATNUMBER', '').strip('" ')

# -- General configuration ---------------------------------------------------

rst_epilog = """
.. |Product| replace:: EC-Motion-Advanced
"""
tags.add('EcMotionAdvanced')

ecdemo_cmdline = ['INCLUDE_ECMASTERDEMOMOTION']

# -- Options for HTML output -------------------------------------------------
html_theme_options['nav_title'] = project

# -- Options for LaTeX output ------------------------------------------------
latex_headerlogo = '../../Common/Media/'+ project + '.png'
latex_additional_files = [latex_headerlogo]
latex_preamble  = r'\newcommand{{\headerlogo}}{{{}}}'''.format(Path(latex_headerlogo).name)
latex_preamble += r'\newcommand{{\atnumber}}{{{}}}'''.format(ecmotion_atnumber)
latex_preamble += open(latex_custom_pagestyle, 'r', encoding='utf8').read()

latex_elements['releasename'] = project
latex_elements['preamble'] = latex_preamble

latex_filename = project + '_' + ecmotion_doc_type.strip('"').replace(' ', '')
latex_title = ecmotion_doc_type

latex_documents = [
    (master_doc, latex_filename + ".tex", latex_title,
     author, "manual"),
]

# -- Extension configuration -------------------------------------------------
breathe_projects = { "EC-Motion-Advanced": "../_build/doxygen/xml/" }
breathe_default_project = "EC-Motion-Advanced"
panels_add_bootstrap_css = False

numfig = True