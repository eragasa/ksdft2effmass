"""Focused regression tests for the repository-wide test-evidence completion gate."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GATE = ROOT / "harness/local/validation/validate_repository_test_evidence.py"


def test_repository_gate_accepts_the_complete_current_inventory() -> None:
    """Require exact current inventory, structural, identity, and collection closure."""
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
    assert result["counts"]["discovered_modules"] == 182
    assert result["counts"]["baseline_collected_nodes"] == 2383
    assert result["counts"]["collected_nodes"] == 2569
    assert result["counts"]["findings"] == 0
    assert result["findings"] == []
    assert result["structural_result"]["status"] == "PASS"
    assert result["structural_result"]["counts"]["unique_evidence_owners"] == 1021
    assert "semantic cohesion" in result["claim_boundary"]
    assert "human acceptance" in result["claim_boundary"]
