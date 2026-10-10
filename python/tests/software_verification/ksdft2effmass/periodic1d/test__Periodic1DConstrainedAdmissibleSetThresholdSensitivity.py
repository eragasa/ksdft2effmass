"""Adversarial verification for retained M3 threshold-sensitivity evidence."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DConstrainedAdmissibleSetThresholdSensitivity:
    """Verify source correlation and the decisive axis-aligned premises."""

    @staticmethod
    def repository() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[5]

    @classmethod
    def source_directory(cls) -> Path:
        """Return the retained M3 source package."""
        return (
            cls.repository()
            / "calculations/ICMSEP2026/conference/paper_1"
            / "constrained-admissible-sets"
        )

    @classmethod
    def sensitivity_directory(cls) -> Path:
        """Return the retained post-hoc sensitivity package."""
        return (
            cls.repository()
            / "calculations/ICMSEP2026/conference/paper_1"
            / "constrained-admissible-sets-threshold-sensitivity"
        )

    @classmethod
    def copied_packages(cls, tmp_path: Path) -> tuple[Path, Path]:
        """Copy both correlated packages beneath a temporary repository root."""
        paper_directory = tmp_path / "calculations/ICMSEP2026/conference/paper_1"
        source = paper_directory / "constrained-admissible-sets"
        sensitivity = (
            paper_directory / "constrained-admissible-sets-threshold-sensitivity"
        )
        shutil.copytree(cls.source_directory(), source)
        shutil.copytree(cls.sensitivity_directory(), sensitivity)
        return source, sensitivity

    @staticmethod
    def digest(path: Path) -> str:
        """Return one SHA-256 digest."""
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @classmethod
    def correlate_mutated_source(
        cls,
        source: Path,
        sensitivity: Path,
        *,
        update_manifest_entry: bool,
    ) -> None:
        """Update declared digests, optionally preserving manifest correlation."""
        source_result = source / "result.json"
        source_digest = cls.digest(source_result)
        input_path = sensitivity / "input.json"
        input_document = json.loads(input_path.read_text())
        input_document["source_result_sha256"] = source_digest
        manifest_path = source / "SHA256SUMS"
        if update_manifest_entry:
            lines = manifest_path.read_text().splitlines()
            matching = [
                index
                for index, line in enumerate(lines)
                if line.endswith("  result.json")
            ]
            assert len(matching) == 1
            lines[matching[0]] = f"{source_digest}  result.json"
            manifest_path.write_text("\n".join(lines) + "\n")
        input_document["source_package_sha256sums_sha256"] = cls.digest(manifest_path)
        input_path.write_text(
            json.dumps(input_document, indent=2, sort_keys=True) + "\n"
        )

    @staticmethod
    def run_verifier(sensitivity: Path) -> subprocess.CompletedProcess[str]:
        """Run the copied standalone sensitivity verifier."""
        return subprocess.run(
            [sys.executable, "verify_result.py"],
            cwd=sensitivity,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_retained_verifier__rejects_source_manifest_miscorrelation(
        self, tmp_path: Path
    ) -> None:
        """The input digest cannot replace correlation to the source manifest entry."""
        source, sensitivity = self.copied_packages(tmp_path)
        result_path = source / "result.json"
        result = json.loads(result_path.read_text())
        result["training_quadratic_losses"]["spectral"]["center"][0] = 0.2
        result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        self.correlate_mutated_source(
            source,
            sensitivity,
            update_manifest_entry=False,
        )

        completed = self.run_verifier(sensitivity)

        assert completed.returncode != 0
        assert "manifest/result correlation mismatch" in completed.stderr

    @pytest.mark.parametrize(
        "tamper",
        (
            "nonzero-spectral-shift-center",
            "nonzero-upper-cross-curvature",
            "nonzero-lower-cross-curvature",
            "symmetric-nonzero-cross-curvature",
            "nonpositive-curvature",
        ),
    )
    def test_retained_verifier__rejects_invalid_quadratic_premise(
        self,
        tmp_path: Path,
        tamper: str,
    ) -> None:
        """Every decisive axis-alignment and curvature premise is checked."""
        source, sensitivity = self.copied_packages(tmp_path)
        result_path = source / "result.json"
        result = json.loads(result_path.read_text())
        spectral = result["training_quadratic_losses"]["spectral"]
        if tamper == "nonzero-spectral-shift-center":
            spectral["center"][0] = 0.2
        elif tamper == "nonzero-upper-cross-curvature":
            spectral["quadratic_matrix"][0][1] = 0.1
        elif tamper == "nonzero-lower-cross-curvature":
            spectral["quadratic_matrix"][1][0] = 0.1
        elif tamper == "symmetric-nonzero-cross-curvature":
            spectral["quadratic_matrix"][0][1] = 0.1
            spectral["quadratic_matrix"][1][0] = 0.1
        else:
            spectral["quadratic_matrix"][0][0] = -1.0
        result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        self.correlate_mutated_source(
            source,
            sensitivity,
            update_manifest_entry=True,
        )

        completed = self.run_verifier(sensitivity)

        assert completed.returncode != 0
        assert "ValueError" in completed.stderr
