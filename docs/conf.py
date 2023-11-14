import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "py-cdhit"
author = "yuanx749"
copyright = "2023, yuanx749"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "myst_nb",
    "sphinx_copybutton",
]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
templates_path = ["_templates"]
default_role = "obj"
add_module_names = False

html_theme = "furo"
html_title = project

autodoc_default_options = {
    "member-order": "bysource",
    "inherited-members": True,
    "imported-members": True,
}
autodoc_mock_imports = ["pandas"]

autosummary_imported_members = True
autosummary_ignore_module_all = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
}

nb_execution_mode = "off"
