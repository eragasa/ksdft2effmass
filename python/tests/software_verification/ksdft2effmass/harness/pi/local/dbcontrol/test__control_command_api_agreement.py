r"""Software verification of maintained Harness projection command/API agreement.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the cohesive projection command/API agreement artifact.

Intrinsic and cross-object scope

The command rendering is compared with a literal private projection result at the
closest mirrored package seam.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import json
import sys
from pathlib import Path

import pytest

from ksdft2effmass.harness import HarnessConfigurationResolver
from ksdft2effmass.harness.cli import harness_projection as projection_cli
from ksdft2effmass.harness.pi.local.control.inputs import (
    _HarnessProjectionInputResolver,
    _HarnessProjectionInputs,
)
from ksdft2effmass.harness.pi.local.dbcontrol.migration import (
    _HarnessProjectionSynchronizer,
)
from ksdft2effmass.harness.pi.local.dbcontrol.records import (
    _HarnessProjectionRequest,
    _HarnessProjectionSyncResult,
    _HarnessProjectionVerificationFinding,
    _HarnessProjectionVerificationResult,
)
from ksdft2effmass.harness.pi.local.dbcontrol.verification import (
    _HarnessProjectionVerifier,
)

pytestmark = pytest.mark.software_verification


def test_artifact__migrate_command__forwards_explicit_source_inputs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.command.migrate-forwards-explicit-ownership-input

    Requirement: The maintained sync command forwards one resolved configuration and
    configured source observations through the private request.

    Method: Inject a request resolved from the exact repository configuration sources,
    invoke sync with only the repository root, and replace synchronization at its seam.

    Oracle: The resolved aggregate defines every configuration-owned request value.

    Acceptance: Exit status is zero, the request preserves the exact configuration and
    derived paths, and JSON rendering uses the projection result fields.

    Interpretation: Failure indicates CLI/API dispatch drift or loss of explicit input confinement.

    Limitations: Source conformance and persistence are owned by migrator evidence.
    """  # noqa: E501
    expected = _HarnessProjectionSyncResult(2, "digest", (), (), ())
    observed: list[_HarnessProjectionRequest] = []

    def execute_literal(
        self: _HarnessProjectionSynchronizer, request: _HarnessProjectionRequest
    ) -> _HarnessProjectionSyncResult:
        observed.append(request)
        return expected

    monkeypatch.setattr(_HarnessProjectionSynchronizer, "execute", execute_literal)
    repository = Path(__file__).resolve().parents[8]
    resolution = HarnessConfigurationResolver().execute(
        "harness/configuration.json",
        (repository / "harness/configuration.json").read_bytes(),
        ".pi/settings.json",
        (repository / ".pi/settings.json").read_bytes(),
    )
    assert resolution.configuration is not None
    canonical_request = _HarnessProjectionRequest(
        tmp_path.resolve(),
        harness_configuration=resolution.configuration,
        evidence_module_paths=(Path("python/tests/test_example.py"),),
    )
    monkeypatch.setattr(
        _HarnessProjectionInputResolver,
        "execute",
        lambda self, root: _HarnessProjectionInputs(canonical_request),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["harness_projection", "sync", "--repository-root", str(tmp_path.resolve())],
    )
    assert projection_cli.run() == 0
    request = observed[0]
    assert request.repository_root == tmp_path.resolve()
    assert request.harness_configuration is resolution.configuration
    assert request.pi_harness_configuration is resolution.configuration.pi
    assert request.evidence_profile_matrix_path == Path(
        "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
    )
    assert request.evidence_module_paths == (Path("python/tests/test_example.py"),)
    assert request.evidence_migration_path == Path(
        ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
    )
    assert request.resource_profile_path == Path(
        "harness/local/profiles/ksdft2effmass-v2.json"
    )
    assert request.generic_resource_manifest_path == Path(
        "harness/pi/resource-manifest.json"
    )
    assert request.generic_resource_root_path == Path("harness/pi")
    assert request.local_resource_manifest_path == Path(
        "harness/local/resource-manifest.json"
    )
    assert request.local_resource_root_path == Path("harness/local")
    assert json.loads(capsys.readouterr().out) == {
        "schema_version": 2,
        "semantic_digest": "digest",
        "counts": [],
        "unresolved_naming_issues": [],
        "projection_paths": [],
    }


def test_artifact__verify_command__rejects_migration_only_inputs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.command.verify-rejects-migration-only-inputs

    Requirement: Superseded per-source configuration flags are absent from both
    maintained command actions.

    Method: Invoke check with the retired Pi settings option and capture parser output.

    Oracle: Both actions accept only their action and explicit repository root.

    Acceptance: Parsing raises ``SystemExit`` with status two and identifies the option
    as unrecognized.

    Interpretation: Failure indicates inaccurate CLI guidance or a widened verifier API.

    Limitations: Successful verification rendering is covered separately.
    """  # noqa: E501
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "harness_projection",
            "check",
            "--repository-root",
            str(tmp_path.resolve()),
            "--pi-settings",
            ".pi/settings.json",
        ],
    )
    with pytest.raises(SystemExit) as raised:
        projection_cli.run()
    assert raised.value.code == 2
    assert "unrecognized arguments: --pi-settings" in capsys.readouterr().err


def test_artifact__verify_command__agrees_with_projection_result(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.command.verify-agrees-with-api

    Requirement: The maintained check command renders every private verification
    result field without changing names or values and exits successfully.

    Method: Supply one immutable literal verifier result, invoke the maintained command
    with an explicit absolute root, and parse its JSON output independently.

    Oracle: The literal dataclass field values define the command result.

    Acceptance: Exit status is zero and rendered JSON equals the exact literal mapping.

    Interpretation: Failure indicates command/API rendering or dispatch drift.

    Limitations: SQLite reconstruction is owned by verifier evidence and is not repeated.
    """  # noqa: E501
    expected = _HarnessProjectionVerificationResult("ok", 0, "a", "a", "c", "c", True)
    monkeypatch.setattr(
        _HarnessProjectionVerifier, "execute", lambda self, root: expected
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["harness_projection", "check", "--repository-root", str(tmp_path.resolve())],
    )
    assert projection_cli.run() == 0
    assert json.loads(capsys.readouterr().out) == {
        "integrity_check": "ok",
        "foreign_key_issue_count": 0,
        "semantic_digest": "a",
        "reconstructed_semantic_digest": "a",
        "raw_database_sha256": "c",
        "reconstructed_database_sha256": "c",
        "projections_identical": True,
        "schema_version_agrees": True,
        "sql_identical": True,
        "manifest_identical": True,
        "findings": [],
    }


def test_artifact__verify_command__returns_literal_failure_for_reported_drift(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.command.verify-drift-exit-status

    Requirement: Reported drift returns exit one and preserves every result and nested
    finding field in deterministic JSON order.

    Method: Supply one literal structured drift result and compare output with an
    independently written complete mapping.

    Oracle: The documented verifier fields and changed-artifact finding are fixed
    literals independent of production rendering.

    Acceptance: Exit is one and the complete parsed JSON mapping is exact.

    Interpretation: Failure permits drift to pass or loses structured output.

    Limitations: Drift detection itself belongs to verifier evidence.
    """  # noqa: E501
    finding = _HarnessProjectionVerificationFinding(
        "changed_artifact", "harness/task-graph.json", "candidate differs"
    )
    expected = _HarnessProjectionVerificationResult(
        "ok", 0, "a", "a", "c", "d", False, True, True, True, (finding,)
    )
    monkeypatch.setattr(
        _HarnessProjectionVerifier, "execute", lambda self, root: expected
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["harness_projection", "check", "--repository-root", str(tmp_path.resolve())],
    )
    assert projection_cli.run() == 1
    assert json.loads(capsys.readouterr().out) == {
        "integrity_check": "ok",
        "foreign_key_issue_count": 0,
        "semantic_digest": "a",
        "reconstructed_semantic_digest": "a",
        "raw_database_sha256": "c",
        "reconstructed_database_sha256": "d",
        "projections_identical": False,
        "schema_version_agrees": True,
        "sql_identical": True,
        "manifest_identical": True,
        "findings": [
            {
                "code": "changed_artifact",
                "path": "harness/task-graph.json",
                "message": "candidate differs",
            }
        ],
    }


def test_artifact__verify_command__unexpected_failure_returns_exit_three(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.command.unexpected-exit-three

    Requirement: Unexpected verifier failures are translated only at the command
    boundary to exit three and structured internal-error output.

    Method: Inject one runtime failure at the private verifier seam.

    Oracle: The maintained command exit contract reserves three for internal errors.

    Acceptance: Exit is three and output contains exact status and error type.

    Interpretation: Failure leaks or misclassifies an unexpected boundary failure.

    Limitations: Expected drift is covered separately.
    """  # noqa: E501

    def fail(self: object, root: Path) -> _HarnessProjectionVerificationResult:
        raise RuntimeError("injected failure")

    monkeypatch.setattr(_HarnessProjectionVerifier, "execute", fail)
    monkeypatch.setattr(
        sys,
        "argv",
        ["harness_projection", "check", "--repository-root", str(tmp_path.resolve())],
    )
    assert projection_cli.run() == 3
    assert json.loads(capsys.readouterr().out) == {
        "error": "RuntimeError: injected failure",
        "status": "INTERNAL_ERROR",
    }
