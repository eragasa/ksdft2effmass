"""Evidence class and represented meaning
Software verification of the built wheel provenance package content and clean import.
Owned contract, oracle, and scope
The Python wheel artifact is the owner; expected provenance modules and isolated
interpreter import are exact oracles.
VVUQ and scientific exclusions
Evidence excludes publication, installation into the active environment, numerical
verification, scientific validation, UQ, and platform exhaustiveness.
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[6]
PYTHON_ROOT = REPO_ROOT / "python"
pytestmark = pytest.mark.software_verification

EXPECTED_WHEEL_MODULES = {
    "ksdft2effmass/provenance/__init__.py",
    "ksdft2effmass/provenance/actions.py",
    "ksdft2effmass/provenance/external_execution.py",
    "ksdft2effmass/provenance/external_tools.py",
    "ksdft2effmass/provenance/records.py",
    "ksdft2effmass/provenance/serialization.py",
    "ksdft2effmass/provenance/tool_observations.py",
}


def test_artifact__wheel_content__supports_clean_import_without_tests(
    tmp_path: Path,
) -> None:
    """Evidence ID
    SV-PROV-072
    Requirement
    A standard wheel contains every provenance runtime module, excludes provenance
    tests, and imports in an isolated interpreter from the wheel alone.
    Method
    Build locally with pip wheel --no-deps, inspect ZIP names, then run Python -I with
    only the wheel inserted into sys.path; no network or publication occurs.
    Oracle
    Fixed expected module paths, wheel ZIP semantics, and isolated Python import
    behavior are independent checks.
    Acceptance
    Build succeeds, expected paths are present, no test path is present, and clean
    import prints the exact package file prefix and export sentinel.
    Interpretation
    Failure may indicate packaging configuration, build tooling, wheel content, or
    isolated import drift.
    Limitations
    This tests the current platform/interpreter only and does not publish, install
    dependencies, or validate a released artifact.
    """
    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()
    build = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            str(PYTHON_ROOT),
            "--no-deps",
            "--wheel-dir",
            str(wheel_dir),
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stderr
    wheels = tuple(wheel_dir.glob("ksdft2effmass-*.whl"))
    assert len(wheels) == 1
    wheel = wheels[0]
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
    assert EXPECTED_WHEEL_MODULES <= names
    assert "ksdft2effmass/provenance/tools.py" not in names
    assert not any("tests/" in name or name.startswith("tests") for name in names)

    code = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "import ksdft2effmass.provenance as p; "
        "print(p.__file__); print(p.ArtifactIdentity.__name__)"
    )
    imported = subprocess.run(
        [sys.executable, "-I", "-c", code, str(wheel)],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert imported.returncode == 0, imported.stderr
    lines = imported.stdout.splitlines()
    assert lines[0].startswith(str(wheel))
    assert lines[0].endswith("/ksdft2effmass/provenance/__init__.py")
    assert lines[1] == "ArtifactIdentity"
