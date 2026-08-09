r"""Software verification of package wheel.

Facet and represented meaning

-----------------------------
This artifact-owned software verification represents the built Python wheel. The fixed
provenance runtime-module inventory is the content oracle, Python ZIP/wheel path
semantics are the archive oracle, and isolated ``python -I -S`` execution is the import
oracle.

Intrinsic and cross-object scope

--------------------------------
The built wheel is the owned artifact. Public API inventory is owned separately by
``test__public_api.py``; dependency direction is owned separately by
``test__import_dependency_direction.py``. Controlled setup builds one local wheel for
the independent content and import owners.

VVUQ and scientific exclusions

------------------------------
Passing applies only to the current interpreter, platform, and already provisioned
local build tools. It does not establish publication, release readiness, installation
across supported platforms, dependency availability outside the controlled
environment, numerical verification, scientific validation, UQ, provenance truth, or
external-tool execution.
"""

from __future__ import annotations

import os
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

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


def select_provenance_python_entries(
    archive_paths: set[PurePosixPath] | frozenset[PurePosixPath],
) -> set[str]:
    """Evidence ID: Owns no identifier; supports SV-PROV-072.

    Requirement: Wheel-content evidence observes every Python source entry recursively
    beneath the
    provenance package rather than only its direct children.

    Method: Apply ``PurePosixPath.is_relative_to`` and the ``.py`` suffix to controlled
    or real
    wheel archive paths.

    Oracle: POSIX path ancestry beneath ``ksdft2effmass/provenance`` and the exact
    ``.py``
    suffix independently define the selected archive entries.

    Acceptance: Return the POSIX strings of all and only Python entries recursively
    beneath the
    provenance package.

    Interpretation: Missing nested entries indicates an incomplete content oracle; extra
    entries
    indicate selection outside the owned package subtree or source-file type.

    Limitations: Selection alone does not establish the expected inventory, wheel
    validity,
    importability, publication readiness, or behavior of selected modules.
    """
    provenance_package = PurePosixPath("ksdft2effmass/provenance")
    return {
        path.as_posix()
        for path in archive_paths
        if path.is_relative_to(provenance_package) and path.suffix == ".py"
    }


@pytest.fixture(scope="module")
def built_provenance_wheel(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Evidence ID: Owns no identifier; supports SV-PROV-072 and SV-PROV-395.

    Requirement: Both wheel evidence owners receive the same locally built artifact
    without index or
    dependency access during the build subprocess.

    Method: Invoke the current interpreter's pip once with no dependencies, no build
    isolation,
    no index, inherited environment, and explicit index-disabling variables.

    Oracle: A zero pip exit status and exactly one project wheel define successful
    setup.

    Acceptance: The offline command finishes within 120 seconds and yields exactly one
    wheel whose
    filename identifies this project in an isolated temporary directory.

    Interpretation: Failure indicates missing preinstalled build tooling, local build
    configuration, or
    wheel production setup; it is not archive-content or isolated-import evidence.

    Limitations: The environment must already contain compatible pip, setuptools, and
    wheel; setup
    does not establish publication, release readiness, or platform coverage.
    """
    wheel_dir = tmp_path_factory.mktemp("provenance-wheel")
    environment = os.environ.copy()
    environment.update(
        {
            "PIP_NO_INDEX": "1",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        }
    )
    build = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--no-build-isolation",
            "--no-index",
            "--wheel-dir",
            str(wheel_dir),
            str(PYTHON_ROOT),
        ],
        cwd=wheel_dir,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert build.returncode == 0, build.stderr
    wheels = tuple(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1, wheels
    wheel = wheels[0]
    assert wheel.name.startswith("ksdft2effmass-"), wheel
    return wheel


def test_artifact__wheel_content__matches_exact_runtime_inventory_and_excludes_tests(
    built_provenance_wheel: Path,
) -> None:
    """Evidence ID: SV-PROV-072

    Requirement: The wheel contains exactly every accepted Python source entry
    recursively below
    ``ksdft2effmass/provenance/`` and no archive entry whose path has an exact ``tests``
    component.

    Method: Apply the same recursive provenance-subtree selector to controlled direct
    and nested
    paths and to the built wheel ZIP names, then inspect every real archive name by
    POSIX path components.

    Oracle: EXPECTED_WHEEL_MODULES, the controlled four-entry observation, and Python
    ZIP/wheel
    POSIX path semantics fix the independent content inventory and test-tree exclusion.

    Acceptance: The selector observes the expected direct module, an unexpected direct
    module, a
    nested ``__init__.py``, and a nested ordinary module; real-wheel provenance Python
    entries equal EXPECTED_WHEEL_MODULES exactly; and no archive path contains an exact
    ``tests`` component.

    Interpretation: Failure indicates a nonrecursive selector or unexpected, missing, or
    misplaced wheel
    content rather than build setup or import execution behavior.

    Limitations: Non-Python package data semantics, installation, publication, other
    platforms, and
    scientific behavior are excluded.
    """
    controlled_archive_paths = {
        PurePosixPath("ksdft2effmass/provenance/actions.py"),
        PurePosixPath("ksdft2effmass/provenance/legacy.py"),
        PurePosixPath("ksdft2effmass/provenance/legacy/__init__.py"),
        PurePosixPath("ksdft2effmass/provenance/legacy/adapter.py"),
    }
    assert select_provenance_python_entries(controlled_archive_paths) == {
        path.as_posix() for path in controlled_archive_paths
    }

    with zipfile.ZipFile(built_provenance_wheel) as archive:
        archive_paths = {PurePosixPath(name) for name in archive.namelist()}
    observed_provenance_modules = select_provenance_python_entries(archive_paths)
    assert observed_provenance_modules == EXPECTED_WHEEL_MODULES
    assert all("tests" not in path.parts for path in archive_paths)


def test_artifact__wheel_import__succeeds_without_ambient_site_packages(
    built_provenance_wheel: Path,
) -> None:
    """Evidence ID: SV-PROV-395

    Requirement: The built wheel supplies the provenance package to an interpreter using
    only the
    wheel plus the Python standard library, without ambient site-packages.

    Method: Run the current interpreter with ``-I -S``, prepend the exact wheel to
    ``sys.path``,
    import provenance, and print its file origin and one stable public sentinel.

    Oracle: Isolated Python import semantics, the exact wheel path, the package
    ``__init__.py``
    suffix, and ``ArtifactIdentity`` class name define the independent import oracle.

    Acceptance: The subprocess exits zero within 30 seconds; its origin is lexically the
    exact wheel
    plus ``ksdft2effmass/provenance/__init__.py``; its sentinel is ``ArtifactIdentity``.

    Interpretation: Failure indicates isolated import, wheel origin, or sentinel drift
    rather than
    archive inventory, general installation, or release failure.

    Limitations: This covers one current interpreter and platform, excludes dependency
    availability
    elsewhere, and does not duplicate the complete public API inventory.
    """
    wheel = built_provenance_wheel.resolve()
    code = "\n".join(
        (
            "import sys",
            "sys.path.insert(0, sys.argv[1])",
            "import ksdft2effmass.provenance as provenance",
            "print(provenance.__file__)",
            "print(provenance.ArtifactIdentity.__name__)",
        )
    )
    imported = subprocess.run(
        [sys.executable, "-I", "-S", "-c", code, str(wheel)],
        cwd=wheel.parent,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert imported.returncode == 0, imported.stderr
    lines = imported.stdout.splitlines()
    assert len(lines) == 2, lines
    wheel_prefix = f"{wheel.as_posix()}/"
    assert lines[0].startswith(wheel_prefix)
    assert lines[0][len(wheel_prefix) :] == "ksdft2effmass/provenance/__init__.py"
    assert lines[1] == "ArtifactIdentity"
