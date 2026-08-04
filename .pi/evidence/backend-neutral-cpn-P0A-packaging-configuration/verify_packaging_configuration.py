"""Verify the bounded P0A dependency, documentation, notice, and wheel policy."""

from __future__ import annotations

import argparse
import json
import runpy
import tomllib
from email.parser import BytesParser
from pathlib import Path
from zipfile import ZipFile

EXPECTED_USER_GUIDE = {
    "abinit",
    "colored-petri-nets",
    "cross-backend-verification",
    "dft-backends",
    "external-dependencies",
    "index",
    "installation",
    "paw-and-pseudopotential-backends",
    "provenance-and-artifacts",
    "quantum-espresso",
    "troubleshooting",
    "wannier90",
    "workflow-model",
}


def _require(condition: bool, message: str) -> None:
    """Raise an unconditional verification failure when a gate is false."""

    if not condition:
        raise ValueError(message)


def _verify_wheel(wheel: Path) -> dict[str, object]:
    """Return bounded wheel metadata and reject bundled SNAKES content."""

    with ZipFile(wheel) as archive:
        names = archive.namelist()
        lowered = [name.lower() for name in names]
        metadata_name = next(
            name for name in names if name.endswith(".dist-info/METADATA")
        )
        metadata = BytesParser().parsebytes(archive.read(metadata_name))

    prohibited = [
        name
        for name in lowered
        if name.startswith("snakes/")
        or ("snakes-" in name and ".dist-info/" in name)
        or ("snakes-" in name and ".data/" in name)
        or "share/doc/python-snakes/" in name
        or name.endswith(("/abcd", "/snkc", "/snkd"))
        or (
            "snakes" in name
            and (name.endswith("/licence.md") or name.endswith("/copying"))
        )
    ]
    if prohibited:
        raise ValueError(
            f"project wheel bundles prohibited SNAKES content: {prohibited}"
        )

    requires = metadata.get_all("Requires-Dist") or []
    expected_fragments = (
        'SNAKES<0.10,>=0.9.33; extra == "workflow"',
        'myst-parser<6,>=5.1; extra == "docs"',
        'sphinx<10,>=8; extra == "docs"',
    )
    for fragment in expected_fragments:
        if fragment not in requires:
            raise ValueError(f"wheel metadata lacks {fragment!r}")
    if any("graphviz" in requirement.lower() for requirement in requires):
        raise ValueError("Graphviz must not occur in project wheel metadata")

    return {
        "member_count": len(names),
        "prohibited_snakes_members": prohibited,
        "provides_extras": metadata.get_all("Provides-Extra") or [],
        "requires_dist": requires,
    }


def main() -> int:
    """Run deterministic repository and optional wheel assertions."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--wheel", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repository = args.repository.resolve()

    pyproject = tomllib.loads((repository / "python/pyproject.toml").read_text())
    extras = pyproject["project"]["optional-dependencies"]
    _require(
        extras["workflow"] == ["SNAKES>=0.9.33,<0.10"],
        "workflow extra differs from the authorized SNAKES range",
    )
    _require(
        extras["docs"] == ["myst-parser>=5.1,<6", "sphinx>=8,<10"],
        "docs extra differs from the authorized MyST/Sphinx ranges",
    )
    _require(
        not any(
            "snakes" in item.lower() for item in pyproject["project"]["dependencies"]
        ),
        "SNAKES must be absent from core dependencies",
    )
    _require(
        not any("snakes" in item.lower() for item in extras["dev"]),
        "SNAKES must be absent from development-only dependencies",
    )
    _require(
        not any(
            "graphviz" in item.lower()
            for requirements in [
                pyproject["project"]["dependencies"],
                *extras.values(),
            ]
            for item in requirements
        ),
        "Graphviz must be absent from Python dependency metadata",
    )

    lock = tomllib.loads((repository / "python/uv.lock").read_text())
    locked = {package["name"]: package for package in lock["package"]}
    for name, version in (
        ("snakes", "0.9.33"),
        ("myst-parser", "5.1.0"),
        ("sphinx", "9.1.0"),
    ):
        _require(locked[name]["version"] == version, f"unexpected locked {name}")

    config = runpy.run_path(str(repository / "docs/conf.py"))
    _require(
        config["extensions"]
        == ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.napoleon"],
        "unexpected Sphinx extension list",
    )
    _require(
        config["source_suffix"] == {".rst": "restructuredtext", ".md": "markdown"},
        "unexpected Sphinx source suffix policy",
    )
    _require(
        config["include_patterns"] == ["*.rst", "**/*.rst", "user-guide/*.md"],
        "unexpected Sphinx source collection policy",
    )
    _require(
        config["myst_enable_extensions"] == ["dollarmath"],
        "unexpected MyST extension policy",
    )
    _require(config["myst_heading_anchors"] == 3, "unexpected heading-anchor depth")

    user_guide = repository / "docs/user-guide"
    markdown_names = {path.stem for path in user_guide.glob("*.md")}
    _require(markdown_names == EXPECTED_USER_GUIDE, "user-guide inventory changed")

    index_text = (repository / "docs/index.rst").read_text()
    navigated = {
        line.strip().removeprefix("user-guide/")
        for line in index_text.splitlines()
        if line.strip().startswith("user-guide/")
    }
    _require(navigated == EXPECTED_USER_GUIDE, "user-guide toctree is incomplete")
    _require(
        ":download:`User guide" not in index_text,
        "obsolete user-guide download navigation remains",
    )
    _require(
        "Uncollected Markdown records" in index_text,
        "uncollected Markdown policy is undocumented",
    )

    relative_markdown_links = []
    directory_links = []
    for path in sorted(user_guide.glob("*.md")):
        for target in _markdown_targets(path.read_text()):
            clean_target = target.split("#", 1)[0]
            if (
                not clean_target
                or "://" in clean_target
                or clean_target.startswith("mailto:")
            ):
                continue
            destination = (path.parent / clean_target).resolve()
            if not destination.exists():
                raise ValueError(f"broken local link in {path}: {target}")
            if destination.is_dir():
                directory_links.append(f"{path.relative_to(repository)}:{target}")
            if (
                clean_target.endswith(".md")
                and destination.parent != user_guide.resolve()
            ):
                relative_markdown_links.append(
                    f"{path.relative_to(repository)}:{target}"
                )
    _require(not directory_links, f"directory links remain: {directory_links}")
    _require(
        not relative_markdown_links,
        f"relative links enter excluded Markdown: {relative_markdown_links}",
    )

    notice = (repository / "THIRD_PARTY_NOTICES.md").read_text()
    for required in (
        "Distribution name: `SNAKES`",
        "Import name: `snakes`",
        "`>=0.9.33,<0.10`",
        "Franck Pommereau",
        "https://codeberg.org/fpom/snakes",
        "`LGPL-2.1-or-later`",
        "LGPL version 3 text",
        "Apache-2.0",
        "new human license checkpoint",
    ):
        if required not in notice:
            raise ValueError(f"third-party notice lacks {required!r}")

    result = {
        "schema_version": 1,
        "task_id": "backend-neutral-cpn-P0A-packaging-configuration",
        "status": "PASS",
        "dependency_policy": {
            "core_dependencies": pyproject["project"]["dependencies"],
            "workflow_extra": extras["workflow"],
            "docs_extra": extras["docs"],
            "graphviz_in_wheel_metadata": False,
        },
        "locked_versions": {
            name: locked[name]["version"]
            for name in ("snakes", "myst-parser", "sphinx")
        },
        "documentation_policy": {
            "include_patterns": config["include_patterns"],
            "user_guide_markdown_count": len(EXPECTED_USER_GUIDE),
            "explicit_navigation_count": len(navigated),
            "directory_link_count": len(directory_links),
            "relative_links_to_excluded_markdown_count": len(relative_markdown_links),
            "obsolete_user_guide_download_navigation": False,
        },
        "notice_policy": "PASS",
        "wheel": _verify_wheel(args.wheel) if args.wheel else None,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.output}")
    return 0


def _markdown_targets(text: str) -> list[str]:
    """Extract ordinary inline Markdown link targets without external packages."""

    targets = []
    index = 0
    while True:
        start = text.find("](", index)
        if start < 0:
            return targets
        end = text.find(")", start + 2)
        if end < 0:
            return targets
        targets.append(text[start + 2 : end])
        index = end + 1


if __name__ == "__main__":
    raise SystemExit(main())
