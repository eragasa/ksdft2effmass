#!/usr/bin/env python3
"""Replay the maintained artifact-owned P1 pytest contract gates.

The authoritative implementations of SV-CPN-023 and SV-CPN-027 through
SV-CPN-033 are ordinary pytest tests. This evidence script only invokes those
modules; it does not duplicate or own their assertions.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PYTHON_ROOT = REPO_ROOT / "python"
INTEGRATION_ROOT = "tests/software_verification/ksdft2effmass/integration"
ARTIFACT_MODULES = (
    f"{INTEGRATION_ROOT}/test__CpnPublicContract.py",
    f"{INTEGRATION_ROOT}/test__CpnContractSchema.py",
    f"{INTEGRATION_ROOT}/test__CpnJsonFixtures.py",
    f"{INTEGRATION_ROOT}/test__CpnDependencyDirection.py",
    f"{INTEGRATION_ROOT}/test__CpnSnakesIsolation.py",
)


def run_contract_gates() -> None:
    """Run all eight restored gates through ordinary pytest collection."""
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", *ARTIFACT_MODULES],
        cwd=PYTHON_ROOT,
        check=True,
    )


def main() -> int:
    """Execute the artifact-owned gate replay."""
    run_contract_gates()
    print("P1 artifact pytest replay passed: evidence_ids=8 modules=5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
