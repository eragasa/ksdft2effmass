"""Integration tests for the retained Mathieu1D package verifier."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]


class TestMathieu1dPackageVerifier:
    """Establish Git-bound predecessor recovery without filesystem restoration."""

    def test_execute__verifies_removed_predecessor_from_recorded_git_tree(
        self,
    ) -> None:
        """The retained package remains verifiable after predecessor removal."""
        calculation = Path(__file__).resolve().parents[1]
        completed = subprocess.run(
            [sys.executable, str(calculation / "run_02_experiment_verification.py")],
            cwd=calculation,
            check=True,
            capture_output=True,
            text=True,
        )

        assert completed.stderr == ""
        assert completed.stdout.endswith("package-verification: pass\n")
