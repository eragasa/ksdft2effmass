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
GATE = ROOT / "python/src/cli/validate_evidence_repository_conformance.py"


def test_artifact__repository_gate__accepts_complete_current_inventory() -> None:
    """Evidence ID: Owns no maintained identifier; harness-level regression only.

    Requirement: The repository gate accepts the exact maintained module and node inventory.

    Method: Execute the gate from the repository root and inspect its canonical JSON.

    Oracle: The synchronized generated inventory independently records the expected
    source-derived module and node projection counts.

    Acceptance: Exit and status pass, source-derived counts equal the synchronized
    comparison target, the owner count is nonzero, and no finding is emitted.

    Interpretation: Failure indicates inventory, identity, collection, or gate drift.

    Limitations: Structural agreement does not establish semantic quality or human acceptance.
    """
    completed = subprocess.run(
        [sys.executable, str(GATE), "--repository-root", str(ROOT)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    result = json.loads(completed.stdout)
    inventory = json.loads(
        (ROOT / ".pi/evidence/python-conformance/module-inventory.json").read_text()
    )
    assert completed.returncode == 0
    assert result["status"] == "PASS"
    assert result["counts"]["baseline_modules"] == 182
    assert (
        result["counts"]["discovered_modules"]
        == inventory["expected_module_count"]
    )
    assert result["counts"]["baseline_collected_nodes"] == 2383
    assert (
        result["counts"]["collected_nodes"]
        == inventory["expected_collected_node_count"]
    )
    assert result["counts"]["findings"] == 0
    assert result["findings"] == []
    assert result["structural_result"]["status"] == "PASS"
    assert result["structural_result"]["counts"]["unique_evidence_owners"] > 0
    assert "semantic cohesion" in result["claim_boundary"]
    assert "human acceptance" in result["claim_boundary"]
