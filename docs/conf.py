import os
import sys

sys.path.insert(0, os.path.abspath("../python/src"))

project = "ksdft2effmass"
author = "Eugene J. Ragasa"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

autodoc_typehints = "none"
napoleon_google_docstring = False
napoleon_numpy_docstring = True
nitpicky = False
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "alabaster"
