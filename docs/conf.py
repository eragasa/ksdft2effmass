import os
import sys

from pygments.lexers.special import TextLexer

sys.path.insert(0, os.path.abspath("../python/src"))

project = "ksdft2effmass"
author = "Eugene J. Ragasa"
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.napoleon"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Keep every maintained RST page and collect the first-level section indexes,
# version-isolated architecture, bounded Markdown user guide, and current CPN
# concept page.
include_patterns = [
    "*.rst",
    "**/*.rst",
    "architecture/*.md",
    "architecture/v1/*.md",
    "architecture/v1/**/*.md",
    "architecture/v2/*.md",
    "architecture/v2/**/*.md",
    "architecture/migration/*.md",
    "architecture/migration/**/*.md",
    "computational/index.md",
    "development/ksdft2effmass.development.installation.md",
    "meetings/index.md",
    "proofs/index.md",
    "publications/index.md",
    "research/index.md",
    "user-guide/*.md",
    "concepts/cpn-contract.md",
]

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
