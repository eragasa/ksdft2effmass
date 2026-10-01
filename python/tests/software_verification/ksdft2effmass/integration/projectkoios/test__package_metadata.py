r"""Software verification of the Project Koios optional dependency metadata.

Evidence profile: routine

Bounded artifact scope: built ksdft2effmass wheel and source-distribution metadata for
the ``project-koios-citation`` optional extra.

Facet and represented meaning

The distribution metadata represents the exact unreleased Project Koios core and
References source revisions required by the optional citation adapter.

Intrinsic and cross-object scope

Evidence covers PEP 508 requirements retained by both built distribution forms.  It
does not test package publication, remote availability, dependency installation, or
adapter behavior, which is owned by its class-owned module.

VVUQ and scientific exclusions

This is packaging software verification.  It establishes no release status,
publication, bibliographic correctness, scientific validation, UQ, or human
acceptance.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

import pytest

pytestmark = pytest.mark.software_verification

_REPOSITORY_ROOT = Path(__file__).resolve().parents[6]
_PYTHON_ROOT = _REPOSITORY_ROOT / "python"
_CORE_REQUIREMENT = (
    "Requires-Dist: projectkoios @ "
    "git+https://github.com/eragasa/projectkoios.git"
    "@233f36900b9b44c943ecc5e27f2968ad4bee97ad ; "
    'extra == "project-koios-citation"'
)
_REFERENCES_REQUIREMENT = (
    "Requires-Dist: projectkoios-references @ "
    "git+https://github.com/eragasa/projectkoios-references.git"
    "@f1ca7b4aee552af131ff7af7d1408d33dd338c93 ; "
    'extra == "project-koios-citation"'
)


class TestProjectKoiosCitationDependencyMetadata:
    """Own evidence for exact optional VCS requirements in distribution metadata."""

    def test_artifact__distribution_metadata__retains_exact_vcs_revisions(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-KOIOS-CITATION-PACKAGE-METADATA-001

        Requirement: Both distributable forms must retain exact PEP 508 VCS
        requirements for the approved Project Koios core and References revisions;
        repository-local uv source overrides or ambiguous version-only requirements
        are insufficient.

        Acceptance: Independently built wheel ``METADATA`` and sdist ``PKG-INFO``
        each contain exactly the two approved direct-VCS requirements for the
        ``project-koios-citation`` extra and contain no bare ``==0.0.0`` requirement
        for either package.
        """
        isolated_python_root = self.copy_project_to_private_directory(tmp_path)
        distribution_directory = tmp_path / "distributions"
        distribution_directory.mkdir()
        environment = os.environ.copy()
        environment.update(
            {
                "PIP_NO_INDEX": "1",
                "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            }
        )
        wheel_build = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                "--no-deps",
                "--no-build-isolation",
                "--no-index",
                "--wheel-dir",
                str(distribution_directory),
                str(isolated_python_root),
            ],
            cwd=tmp_path,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        sdist_build = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys; "
                    "from setuptools.build_meta import build_sdist; "
                    "build_sdist(sys.argv[1])"
                ),
                str(distribution_directory),
            ],
            cwd=isolated_python_root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )

        assert wheel_build.returncode == 0, wheel_build.stderr
        assert sdist_build.returncode == 0, sdist_build.stderr
        wheels = tuple(distribution_directory.glob("ksdft2effmass-*.whl"))
        sdists = tuple(distribution_directory.glob("ksdft2effmass-*.tar.gz"))
        assert len(wheels) == 1
        assert len(sdists) == 1
        wheel_requirements = self.projectkoios_requirements(
            self.wheel_metadata(wheels[0])
        )
        sdist_requirements = self.projectkoios_requirements(
            self.sdist_metadata(sdists[0])
        )
        expected = {_CORE_REQUIREMENT, _REFERENCES_REQUIREMENT}

        assert wheel_requirements == expected
        assert sdist_requirements == expected
        assert all("==0.0.0" not in value for value in wheel_requirements)
        assert all("==0.0.0" not in value for value in sdist_requirements)

    @staticmethod
    def copy_project_to_private_directory(tmp_path: Path) -> Path:
        """Copy only build inputs beneath the pytest-owned private directory."""
        isolated_repository_root = tmp_path / "repository"
        isolated_python_root = isolated_repository_root / "python"
        isolated_python_root.mkdir(parents=True)
        shutil.copy2(_PYTHON_ROOT / "pyproject.toml", isolated_python_root)
        shutil.copytree(
            _PYTHON_ROOT / "src",
            isolated_python_root / "src",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        return isolated_python_root

    @staticmethod
    def wheel_metadata(wheel: Path) -> str:
        """Read the sole wheel core-metadata document as UTF-8."""
        with zipfile.ZipFile(wheel) as archive:
            metadata_names = tuple(
                name
                for name in archive.namelist()
                if name.endswith(".dist-info/METADATA")
            )
            if len(metadata_names) != 1:
                raise ValueError("wheel must contain exactly one METADATA document")
            return archive.read(metadata_names[0]).decode("utf-8")

    @staticmethod
    def sdist_metadata(sdist: Path) -> str:
        """Read the sole top-level sdist core-metadata document as UTF-8."""
        with tarfile.open(sdist, "r:gz") as archive:
            metadata_members = tuple(
                member
                for member in archive.getmembers()
                if len(PurePosixPath(member.name).parts) == 2
                and member.name.endswith("/PKG-INFO")
            )
            if len(metadata_members) != 1:
                raise ValueError("sdist must contain exactly one top-level PKG-INFO")
            stream = archive.extractfile(metadata_members[0])
            if stream is None:
                raise ValueError("sdist PKG-INFO is not a readable regular file")
            return stream.read().decode("utf-8")

    @staticmethod
    def projectkoios_requirements(metadata: str) -> set[str]:
        """Select only Project Koios ``Requires-Dist`` metadata lines."""
        return {
            line
            for line in metadata.splitlines()
            if line.startswith("Requires-Dist: projectkoios")
        }
