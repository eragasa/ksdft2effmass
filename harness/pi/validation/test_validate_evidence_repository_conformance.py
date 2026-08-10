r"""Regression tests for the repository-wide evidence completion gate.

Facet and represented meaning

The module verifies agreement between the maintained inventory and repository gate.

Intrinsic and cross-object scope

The repository gate command is the artifact owner; exact current counts are in scope.

VVUQ and scientific exclusions

Passing establishes structural software agreement only, not scientific validation or UQ.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GATE = ROOT / "harness/local/validation/validate_evidence_repository_conformance.py"


def test_artifact__repository_gate__accepts_complete_current_inventory() -> None:
    """Evidence ID: Owns no maintained identifier; harness-level regression only.

    Requirement: The repository gate accepts the exact maintained module and node inventory.

    Method: Execute the gate from the repository root and inspect its canonical JSON.

    Oracle: The maintained inventory declares 245 modules, 2,923 nodes, and 1,211 owners.

    Acceptance: Exit and status pass, counts match exactly, and no finding is emitted.

    Interpretation: Failure indicates inventory, identity, collection, or gate drift.

    Limitations: Structural agreement does not establish semantic quality or human acceptance.
    """
    completed = subprocess.run(
        [sys.executable, str(GATE)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    result = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert result["status"] == "PASS"
    assert result["counts"]["baseline_modules"] == 182
    assert result["counts"]["discovered_modules"] == 245
    assert result["counts"]["baseline_collected_nodes"] == 2383
    assert result["counts"]["collected_nodes"] == 2923
    assert result["counts"]["findings"] == 0
    assert result["findings"] == []
    assert result["structural_result"]["status"] == "PASS"
    assert result["structural_result"]["counts"]["unique_evidence_owners"] == 1211
    assert "semantic cohesion" in result["claim_boundary"]
    assert "human acceptance" in result["claim_boundary"]
