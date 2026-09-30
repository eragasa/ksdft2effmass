import os
import sys

from pygments.lexers.special import TextLexer

sys.path.insert(0, os.path.abspath("../../python/src"))

project = "ksdft2effmass"
author = "Eugene J. Ragasa"
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.napoleon"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Every source below doc/sphinx belongs to the Sphinx site. Repository-first
# research, proof, publication, architecture, and computational records remain
# under docs/ and are not parsed by Sphinx.
include_patterns = ["*.rst", "**/*.rst", "**/*.md"]

myst_enable_extensions = ["dollarmath"]
myst_heading_anchors = 3


def setup(app):
    """Register Mermaid fences as literal text for warning-free source builds."""
    from sphinx.highlighting import lexers

    lexers["mermaid"] = TextLexer()


autodoc_typehints = "none"
napoleon_google_docstring = False
napoleon_numpy_docstring = True
nitpicky = False
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "alabaster"
