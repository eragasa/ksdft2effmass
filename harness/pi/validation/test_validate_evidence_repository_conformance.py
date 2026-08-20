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
from types import SimpleNamespace

import pytest

from ksdft2effmass.harness.cli import (
    validate_evidence_repository_conformance as command_owner,
)

ROOT = Path(__file__).resolve().parents[3]
GATE = (
    sys.executable,
    "-m",
    "ksdft2effmass.harness.cli",
    "validate-evidence-repository-conformance",
)


def test_artifact__repository_gate__accepts_complete_current_inventory() -> None:
    """Evidence ID: Owns no maintained identifier; harness-level regression only.

    Requirement: The repository gate accepts the exact maintained module and node
    inventory.

    Method: Execute the gate from the repository root and inspect its canonical JSON.

    Oracle: The synchronized generated inventory independently records the expected
    source-derived module and node projection counts.

    Acceptance: Exit and status pass, source-derived counts equal the synchronized
    comparison target, the owner count is nonzero, and no finding is emitted.

    Interpretation: Failure indicates inventory, identity, collection, or gate drift.

    Limitations: Structural agreement does not establish semantic quality or human
    acceptance.
    """
    completed = subprocess.run(
        [*GATE, "--repository-root", str(ROOT)],
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
    assert result["counts"]["discovered_modules"] == inventory["expected_module_count"]
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


def test_command_forwards_one_request_to_repository_operation_owner(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    observed: list[object] = []
    result = SimpleNamespace(
        status="PASS",
        claim_boundary=("human acceptance",),
        baseline_modules=1,
        baseline_collected_nodes=2,
        discovered_modules=3,
        collected_nodes=4,
        unique_evidence_owners=5,
        findings=(),
    )

    def execute_literal(self: object, request: object) -> object:
        observed.append(request)
        return result

    monkeypatch.setattr(
        command_owner._EvidenceRepositoryConformanceValidator,
        "execute",
        execute_literal,
    )
    assert command_owner.run(["--repository-root", str(ROOT)]) == 0
    assert len(observed) == 1
    assert observed[0].repository_root == ROOT
    assert json.loads(capsys.readouterr().out)["counts"] == {
        "baseline_collected_nodes": 2,
        "baseline_modules": 1,
        "collected_nodes": 4,
        "discovered_modules": 3,
        "findings": 0,
    }


def test_command_maps_expected_owner_input_error_to_exit_two(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def reject_input(self: object, request: object) -> object:
        raise ValueError("controlled source input")

    monkeypatch.setattr(
        command_owner._EvidenceRepositoryConformanceValidator,
        "execute",
        reject_input,
    )
    assert command_owner.run(["--repository-root", str(ROOT)]) == 2
    assert json.loads(capsys.readouterr().out) == {
        "error": "controlled source input",
        "schema_version": 1,
        "status": "INVALID_INPUT",
    }
