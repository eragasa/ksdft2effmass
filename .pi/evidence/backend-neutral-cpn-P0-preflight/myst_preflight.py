"""Build a disposable mixed RST/MyST documentation project for P0.

The script creates and removes all source and generated HTML outside the
repository. It does not modify the maintained Sphinx configuration.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def _write_sources(source: Path) -> None:
    """Write the representative disposable documentation sources."""

    (source / "conf.py").write_text(
        "project = 'P0 disposable MyST preflight'\n"
        "extensions = ['myst_parser']\n"
        "myst_enable_extensions = ['dollarmath']\n"
        "myst_heading_anchors = 3\n"
        "exclude_patterns = ['_build']\n"
        "html_theme = 'alabaster'\n",
        encoding="utf-8",
    )
    (source / "index.rst").write_text(
        "P0 disposable documentation\n"
        "===========================\n\n"
        "This RST index links to the Markdown page: :doc:`guide`.\n\n"
        ".. toctree::\n"
        "   :maxdepth: 2\n\n"
        "   guide\n",
        encoding="utf-8",
    )
    (source / "guide.md").write_text(
        "# MyST and Obsidian-style source\n\n"
        "Inline mathematics $E = \\hbar^2 k^2/(2m)$ remains readable in "
        "Obsidian.\n\n"
        "$$\n\\varepsilon_{\\mathrm H} = "
        "\\max_{i,j}|H_{ij}-H_{ji}^{*}|\n$$\n\n"
        "```python\nvalue = 3\nassert value > 0\n```\n\n"
        "A repository-style [relative link](details.md#unicode-and-tables) "
        "resolves to another Markdown document.\n\n"
        "```{toctree}\n:maxdepth: 1\n\ndetails\n```\n",
        encoding="utf-8",
    )
    (source / "details.md").write_text(
        "# Details\n\n"
        "## Unicode and tables\n\n"
        "Unicode scientific symbols: ε, Δ, Γ, ψ, Å, and ħ.\n\n"
        "| Quantity | Symbol |\n| --- | --- |\n| residual | ε |\n\n"
        "A nested fence is represented portably:\n\n"
        "````markdown\n```python\nprint('nested')\n```\n````\n\n"
        "Raw inline HTML retained by CommonMark: <span>scientific note</span>.\n\n"
        "Return to the [guide](guide.md).\n",
        encoding="utf-8",
    )


def _run_build(workspace: Path) -> dict[str, Any]:
    """Run Sphinx with warnings treated as errors and inspect generated files."""

    source = workspace / "source"
    output = workspace / "html"
    doctree = workspace / "doctrees"
    source.mkdir()
    _write_sources(source)
    command = [
        sys.executable,
        "-m",
        "sphinx",
        "-W",
        "--keep-going",
        "-b",
        "html",
        "-d",
        str(doctree),
        str(source),
        str(output),
    ]
    process = subprocess.run(command, check=False, capture_output=True, text=True)
    generated = sorted(
        str(path.relative_to(output)) for path in output.rglob("*") if path.is_file()
    )
    expected_pages = [
        output / "index.html",
        output / "guide.html",
        output / "details.html",
    ]
    missing_pages = [str(path) for path in expected_pages if not path.is_file()]
    if process.returncode != 0 or missing_pages:
        raise RuntimeError(
            json.dumps(
                {
                    "command": command,
                    "exit_status": process.returncode,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                    "missing_pages": missing_pages,
                },
                indent=2,
            )
        )
    guide_html = (output / "guide.html").read_text(encoding="utf-8")
    details_html = (output / "details.html").read_text(encoding="utf-8")
    assertions = {
        "inline_math_rendered": "math notranslate nohighlight" in guide_html,
        "display_math_rendered": "varepsilon" in guide_html,
        "fenced_python_rendered": "highlight-python" in guide_html,
        "relative_link_resolved": "details.html#unicode-and-tables" in guide_html,
        "unicode_preserved": "Å" in details_html and "ħ" in details_html,
        "table_rendered": "<table" in details_html,
        "nested_fence_rendered_as_markdown_code": all(
            fragment in details_html
            for fragment in (
                '<div class="highlight-markdown notranslate">',
                '<span class="sb">```python</span>',
                '<span class="nb">print</span>',
                "&#39;nested&#39;",
            )
        ),
        "raw_html_preserved_as_element": (
            "<span>scientific note</span>" in details_html
        ),
        "mixed_navigation_rendered": "guide.html"
        in (output / "index.html").read_text(encoding="utf-8"),
    }
    if not all(assertions.values()):
        raise AssertionError(f"generated HTML assertions failed: {assertions}")
    temporary_paths = {str(workspace), str(workspace.resolve())}

    def normalize(value: str) -> str:
        """Replace disposable workspace spellings with one stable marker."""

        for temporary_path in sorted(temporary_paths, key=len, reverse=True):
            value = value.replace(temporary_path, "<temp>")
        return value

    return {
        "command": [normalize(part) for part in command],
        "exit_status": process.returncode,
        "stdout_summary": "Sphinx build succeeded with no warnings.",
        "stderr": normalize(process.stderr),
        "extensions": ["myst_parser"],
        "myst_enable_extensions": ["dollarmath"],
        "myst_heading_anchors": 3,
        "source_inventory": ["index.rst", "guide.md", "details.md"],
        "generated_inventory": generated,
        "assertions": assertions,
        "warnings": [],
        "limitations": [
            "This minimal build does not establish compatibility of every "
            "maintained Markdown page.",
            "Mermaid was not rendered in the minimal build; maintained Mermaid "
            "fences need a lexer or rendering-extension decision to avoid "
            "warnings-as-errors.",
            "Obsidian authoring compatibility was checked for portable source "
            "syntax, not by executing Obsidian.",
        ],
    }


def main() -> int:
    """Build the disposable project and write compact structured evidence."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ksdft2effmass-p0-myst-") as path:
        build = _run_build(Path(path))
    result = {
        "schema_version": 1,
        "status": "PASS",
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "myst_parser_distribution": importlib.metadata.version("myst-parser"),
            "myst_parser_import": importlib.metadata.version("myst-parser"),
            "sphinx_version": importlib.metadata.version("Sphinx"),
        },
        "build": build,
        "classification": (
            "documentation software preflight; not scientific validation or UQ"
        ),
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
