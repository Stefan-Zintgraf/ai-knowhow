# -*- coding: utf-8 -*-
#
# Project specific configuration file for the Sphinx documentation builder.
#

# -- Import common options for all projects ----------------------------------
from conf import *

sys.path.append(os.path.abspath("."))


# -- Project information -----------------------------------------------------
productname = os.getenv('PRODUCTNAME', 'EcWrapperRust')

project = productname + ' Rust'
title = 'Rust Programming Interface'

# -- General configuration ---------------------------------------------------


# -- Options for HTML output -------------------------------------------------
html_theme_options['nav_title'] = project


# -- Options for LaTeX output ------------------------------------------------
latex_headerlogo = '../../Common/Media/' + productname + '.png'
latex_additional_files = [latex_headerlogo]
latex_preamble = r'\newcommand{{\headerlogo}}{{{}}}'''.format(Path(latex_headerlogo).name)
latex_preamble += open(latex_custom_pagestyle, "r", encoding="utf8").read()

latex_elements['releasename'] = productname
latex_elements['preamble'] = latex_preamble

latex_documents = [
    (master_doc, productname + '_Rust.tex', title,
     author, 'manual'),
]
