"""Run the bounded validator-migration completion checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYTHON = ROOT / "python/.venv/bin/python"
TEST_ROOT = "python/tests/software_verification/ksdft2effmass/harness/pi"


def main() -> int:
    commands = (
        (
            str(PYTHON),
            "-m",
            "pytest",
            "-q",
            "harness/pi/validation/test_validate_python_test_evidence.py",
            f"{TEST_ROOT}/test__PythonTestEvidenceSource.py",
            f"{TEST_ROOT}/test__PythonTestEvidenceRequest.py",
            f"{TEST_ROOT}/test__PythonTestEvidenceFinding.py",
            f"{TEST_ROOT}/test__PythonTestEvidenceValidationResult.py",
            f"{TEST_ROOT}/test__ValidatePythonTestEvidence.py",
            f"{TEST_ROOT}/test__python_test_evidence_wrapper_api_agreement.py",
            f"{TEST_ROOT}/test__harness_pi_public_api.py",
            f"{TEST_ROOT}/test__harness_pi_generic_local_dependency_direction.py",
        ),
        (
            str(PYTHON),
            "-m",
            "pytest",
            "-q",
            f"{TEST_ROOT}/local/test__local_context_dependency_and_nonmutation.py",
            "-k",
            "generic_local_dependency",
        ),
        (
            str(PYTHON),
            "-m",
            "ruff",
            "check",
            "python/src/ksdft2effmass/harness/pi/test_evidence.py",
            "harness/pi/validation/validate_python_test_evidence.py",
        ),
    )
    for command in commands:
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
