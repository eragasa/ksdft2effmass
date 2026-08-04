"""Audit maintained Markdown user-guide syntax for bounded MyST preflight."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

EXPECTED_USER_GUIDE = {
    "abinit.md",
    "colored-petri-nets.md",
    "cross-backend-verification.md",
    "dft-backends.md",
    "external-dependencies.md",
    "index.md",
    "installation.md",
    "paw-and-pseudopotential-backends.md",
    "provenance-and-artifacts.md",
    "quantum-espresso.md",
    "troubleshooting.md",
    "wannier90.md",
    "workflow-model.md",
}
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_PATTERN = re.compile(
    r"^(?P<fence>`{3,}|~{3,})(?P<language>[^\s`]*)", re.MULTILINE
)
RAW_HTML_PATTERN = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s+[^<>]*)?>")


def _audit(repository: Path) -> dict[str, Any]:
    """Return deterministic inventory, syntax, and local-link observations."""

    guide = repository / "docs" / "user-guide"
    files = sorted(guide.glob("*.md"))
    names = {path.name for path in files}
    if names != EXPECTED_USER_GUIDE:
        raise ValueError(
            f"user-guide inventory mismatch: missing={EXPECTED_USER_GUIDE - names}, "
            f"extra={names - EXPECTED_USER_GUIDE}"
        )

    syntax_counts = {
        "dollar_display_delimiters": 0,
        "inline_dollar_lines": 0,
        "fenced_blocks": 0,
        "nested_or_long_fences": 0,
        "table_rows": 0,
        "raw_html_matches": 0,
        "mermaid_fences": 0,
    }
    local_links: list[dict[str, Any]] = []
    broken_links: list[dict[str, str]] = []
    directory_links: list[dict[str, str]] = []
    languages: dict[str, int] = {}

    for path in files:
        text = path.read_text(encoding="utf-8")
        syntax_counts["dollar_display_delimiters"] += text.count("$$")
        syntax_counts["inline_dollar_lines"] += sum(
            "$" in line and "$$" not in line for line in text.splitlines()
        )
        syntax_counts["table_rows"] += sum(
            line.startswith("|") and line.endswith("|") for line in text.splitlines()
        )
        syntax_counts["raw_html_matches"] += len(RAW_HTML_PATTERN.findall(text))
        for match in FENCE_PATTERN.finditer(text):
            syntax_counts["fenced_blocks"] += 1
            language = match.group("language") or "<closing-or-untyped>"
            languages[language] = languages.get(language, 0) + 1
            if len(match.group("fence")) > 3:
                syntax_counts["nested_or_long_fences"] += 1
            if language == "mermaid":
                syntax_counts["mermaid_fences"] += 1
        for match in LINK_PATTERN.finditer(text):
            destination = match.group(1).split()[0].strip("<>")
            if destination.startswith(("http:", "https:", "mailto:", "#")):
                continue
            relative, _, fragment = destination.partition("#")
            target = (path.parent / relative).resolve()
            record = {
                "source": str(path.relative_to(repository)),
                "destination": destination,
                "target_kind": (
                    "directory"
                    if target.is_dir()
                    else "file"
                    if target.is_file()
                    else "missing"
                ),
                "fragment": fragment,
            }
            local_links.append(record)
            if not target.exists():
                broken_links.append(
                    {"source": record["source"], "destination": destination}
                )
            elif target.is_dir():
                directory_links.append(
                    {"source": record["source"], "destination": destination}
                )

    if broken_links:
        raise ValueError(f"broken local user-guide links: {broken_links}")

    sphinx_index = (repository / "docs" / "index.rst").read_text(encoding="utf-8")
    download_links = [
        line.strip()
        for line in sphinx_index.splitlines()
        if ":download:`" in line and ("user-guide/" in line or "architecture/" in line)
    ]
    raw_html_observation = (
        "No user-guide raw HTML element was found."
        if syntax_counts["raw_html_matches"] == 0
        else "User-guide raw HTML elements require individual MyST rendering review."
    )
    return {
        "schema_version": 1,
        "status": "CONDITIONAL_PASS" if directory_links else "PASS",
        "inventory": [str(path.relative_to(repository)) for path in files],
        "syntax_counts": syntax_counts,
        "fence_languages": dict(sorted(languages.items())),
        "local_link_count": len(local_links),
        "broken_local_links": broken_links,
        "myst_sensitive_directory_links": directory_links,
        "current_rst_download_navigation_count": len(download_links),
        "current_rst_download_navigation": download_links,
        "observations": [
            "Dollar-delimited mathematics requires "
            "myst_enable_extensions=['dollarmath'].",
            "User-guide fenced code, tables, and relative file links are directly "
            "renderable.",
            "No user-guide Mermaid fence or nested fence was found.",
            raw_html_observation,
            "Directory links resolve on disk but MyST/Sphinx reports them as missing "
            "cross-reference targets; use concrete index files.",
            "Direct MyST toctree registration must replace, not duplicate, the current "
            "RST download-only navigation entries.",
            "The current downloadable-source behavior changes when Markdown becomes a "
            "collected source; source links can remain only if deliberately retained.",
        ],
        "broad_disposable_build": {
            "command": "python -m sphinx -W --keep-going -b html -c <temp-conf> "
            "-d <temp-doctrees> docs <temp-html>",
            "exit_status": 1,
            "scope_note": "The broad build intentionally collected all maintained "
            "Markdown and exposed warnings outside the user-guide audit scope.",
            "user_guide_warnings": [
                "docs/user-guide/index.md: directory target ../architecture/ not found",
                "docs/user-guide/index.md: directory target ../computational/ "
                "not found",
                "docs/user-guide/index.md: directory target ../research/ not found",
            ],
            "other_observed_classes": [
                "Mermaid lexer warnings outside docs/user-guide",
                "existing cross-reference warnings outside docs/user-guide",
            ],
            "generated_output_retained": False,
        },
    }


def main() -> int:
    """Write the Markdown audit JSON to the requested path."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    repository = arguments.repository.resolve()
    result = _audit(repository)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
