"""Integration verification for the thin PIAB1D decomposition entry point."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestPiab1dHamiltonianDecomposition:
    """Own direct reusable-class composition without a PIAB1D Workflow."""

    @staticmethod
    def sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def test_script__declared_inputs__writes_only_verified_visualization(
        self, tmp_path: Path
    ) -> None:
        calculation = Path(__file__).resolve().parents[2]
        study_input = calculation / "input.json"
        decomposition_input = calculation / "identifiability-input.json"
        figure = tmp_path / "hamiltonian-decomposition.png"
        study_input_hash = self.sha256(study_input)
        decomposition_input_hash = self.sha256(decomposition_input)

        completed = subprocess.run(
            (
                sys.executable,
                str(calculation / "hamiltonian_decomposition.py"),
                "--study-input",
                str(study_input),
                "--decomposition-input",
                str(decomposition_input),
                "--figure-output",
                str(figure),
            ),
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0, completed.stderr
        assert figure.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        assert self.sha256(study_input) == study_input_hash
        assert self.sha256(decomposition_input) == decomposition_input_hash
