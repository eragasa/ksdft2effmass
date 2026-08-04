import os
import sys

sys.path.insert(0, os.path.abspath("../python/src"))

project = "ksdft2effmass"
author = "Eugene J. Ragasa"
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.napoleon"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Keep every maintained RST page and collect only the bounded Markdown user
# guide. Architecture, computational, research, paper, meeting, and conference
# Markdown remain repository/Obsidian sources rather than implicit Sphinx input.
include_patterns = [
    "*.rst",
    "**/*.rst",
    "user-guide/*.md",
    "concepts/cpn-contract.md",
    "api/workflows-cpn.md",
]

myst_enable_extensions = ["dollarmath"]
myst_heading_anchors = 3

autodoc_typehints = "none"
napoleon_google_docstring = False
napoleon_numpy_docstring = True
nitpicky = False
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "alabaster"
