"""Revision-bound historical and working-composition citation test inputs.

All repositories below are temporary local fixtures. A fixture commit binds copied
working bytes only; it is not the research repository's revision or acceptance.
"""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

from ksdft2effmass.publications.manuscript import (
    LatexManuscriptAuditor,
    LatexManuscriptAuditRequest,
)


@pytest.fixture(scope="session")
def citation_baseline_repository(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Check out the maintained baseline revision without changing the source repo."""
    source = Path(__file__).resolve().parents[7]
    revision = (
        (Path(__file__).parent / "resources/baseline-revision.txt")
        .read_text(encoding="ascii")
        .strip()
    )
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise ValueError("citation baseline must identify one exact Git commit")
    root = tmp_path_factory.mktemp("citation-baseline") / "repository"
    subprocess.run(
        [
            "git",
            "clone",
            "--quiet",
            "--shared",
            "--no-checkout",
            str(source),
            str(root),
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "core.hooksPath=/dev/null",
            "checkout",
            "--quiet",
            "--detach",
            revision,
        ],
        check=True,
        capture_output=True,
    )
    actual = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != revision:
        raise ValueError("citation fixture checkout does not match its frozen revision")
    return root


@pytest.fixture(scope="session")
def expanded_monograph_repository(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Bind the actual working composition to its own explicitly local fixture HEAD."""
    source = Path(__file__).resolve().parents[7]
    monograph = source / "docs/publications/research-monograph"
    audit = LatexManuscriptAuditor().execute(
        LatexManuscriptAuditRequest(
            monograph, monograph / "manuscript/manuscript.tex", ()
        )
    )
    if not audit.passes:
        raise ValueError(f"working monograph has structural findings: {audit.issues}")
    root = tmp_path_factory.mktemp("expanded-citation-composition")
    for path in audit.source_paths:
        target = root / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "--", "docs"], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "core.hooksPath=/dev/null",
            "-c",
            "user.name=Citation Fixture",
            "-c",
            "user.email=citation-fixture@example.invalid",
            "commit",
            "--quiet",
            "--no-gpg-sign",
            "-m",
            "local working-byte fixture",
        ],
        check=True,
    )
    return root
