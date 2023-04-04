# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RANDFIG'
copyright = '2023, Jeremiah Poveda Martínez'
author = 'Jeremiah Poveda Martínez'
release = '1.1.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

import sys, os
sys.path.insert(0, os.path.abspath('../randfig'))

extensions.append('sphinx.ext.autodoc')
extensions.append('sphinx.ext.napoleon')
extensions.append('sphinx_exec_code')

napoleon_include_init_with_doc = True
html_theme = "pydata_sphinx_theme"
