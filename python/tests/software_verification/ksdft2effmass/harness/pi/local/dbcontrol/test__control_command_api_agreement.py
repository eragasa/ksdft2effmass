r"""Software verification of maintained Harness projection command/API agreement.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the cohesive projection command/API agreement artifact.

Intrinsic and cross-object scope

The command rendering is compared with a literal public Action result at the closest
mirrored package seam.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessControlMigrationRequest,
    HarnessControlMigrationResult,
    HarnessControlVerificationFinding,
    HarnessControlVerificationResult,
)
from ksdft2effmass.harness.pi.local.dbcontrol.migration import HarnessControlMigrator
from ksdft2effmass.harness.pi.local.dbcontrol.verification import HarnessControlVerifier

pytestmark = pytest.mark.software_verification


def load_projection_cli() -> ModuleType:
    """Evidence ID: Owns no identifier; supports projection command/API evidence.

    Requirement: Command/API tests require the maintained nonpackage script module.

    Method: Load the exact repository script through the standard import loader.

    Oracle: The task-authorized CLI path fixes the selected module.

    Acceptance: Return the loaded module with its real ``main`` function.

    Interpretation: Failure identifies test setup or script import drift.

    Limitations: This helper owns no independent evidence result.
    """  # noqa: E501
    path = Path(__file__).resolve().parents[8] / "python/src/cli/harness_projection.py"
    spec = importlib.util.spec_from_file_location("harness_projection_cli", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


projection_cli = load_projection_cli()


def test_artifact__migrate_command__forwards_explicit_source_inputs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.command.migrate-forwards-explicit-ownership-input

    Requirement: The maintained sync command forwards its repository-relative canonical evidence and resource paths through the public request without changing migration signatures.

    Method: Invoke the command with an explicit root, profile matrix, test source, migration map, profile, manifests, and resource roots while replacing the public migrator with a literal-result seam.

    Oracle: The command arguments define the exact repository-relative request values.

    Acceptance: Exit status is zero, the captured request preserves the resolved root and every exact relative path, and JSON rendering uses the public result fields.

    Interpretation: Failure indicates CLI/API dispatch drift or loss of explicit input confinement.

    Limitations: Source conformance and persistence are owned by migrator evidence.
    """  # noqa: E501
    expected = HarnessControlMigrationResult(2, "digest", (), (), ())
    observed: list[HarnessControlMigrationRequest] = []

    def execute_literal(
        self: HarnessControlMigrator, request: HarnessControlMigrationRequest
    ) -> HarnessControlMigrationResult:
        observed.append(request)
        return expected

    monkeypatch.setattr(HarnessControlMigrator, "execute", execute_literal)
    settings = tmp_path / ".pi/settings.json"
    settings.parent.mkdir(parents=True)
    settings.write_text(
        '{"subagents":{"agentOverrides":{"example.disabled":{"disabled":true}}}}'
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "harness_control",
            "sync",
            "--repository-root",
            str(tmp_path.resolve()),
            "--pi-settings",
            ".pi/settings.json",
            "--evidence-profile-matrix",
            "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json",
            "--evidence-module",
            "python/tests/test_example.py",
            "--evidence-migration",
            ".pi/evidence/python-conformance/r2.3-private-owner-migration.json",
            "--resource-profile",
            "harness/local/profiles/project.json",
            "--generic-resource-manifest",
            "harness/pi/resource-manifest.json",
            "--generic-resource-root",
            "harness/pi",
            "--local-resource-manifest",
            "harness/local/resource-manifest.json",
            "--local-resource-root",
            "harness/local",
        ],
    )
    assert projection_cli.main() == 0
    request = observed[0]
    assert request.repository_root == tmp_path.resolve()
    assert request.pi_harness_configuration.disabled_agent_runtime_names == (
        "example.disabled",
    )
    assert request.evidence_profile_matrix_path == Path(
        "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
    )
    assert request.evidence_module_paths == (Path("python/tests/test_example.py"),)
    assert request.evidence_migration_path == Path(
        ".pi/evidence/python-conformance/r2.3-private-owner-migration.json"
    )
    assert request.resource_profile_path == Path("harness/local/profiles/project.json")
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

    Requirement: The check command rejects configuration, evidence, and resource
    inputs with an accurate synchronization-only diagnostic.

    Method: Invoke check with one explicit Pi settings option and capture the parser
    failure text.

    Oracle: Project configuration participates only in synchronization, while checking
    accepts only the repository root.

    Acceptance: Parsing raises ``SystemExit`` with status two and stderr names
    configuration, evidence, and resource inputs as synchronization-only.

    Interpretation: Failure indicates inaccurate CLI guidance or a widened verifier API.

    Limitations: Successful verification rendering is covered separately.
    """  # noqa: E501
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "harness_control",
            "check",
            "--repository-root",
            str(tmp_path.resolve()),
            "--pi-settings",
            ".pi/settings.json",
        ],
    )
    with pytest.raises(SystemExit) as raised:
        projection_cli.main()
    assert raised.value.code == 2
    assert (
        "configuration, evidence, and resource inputs are valid only with sync"
        in capsys.readouterr().err
    )


def test_artifact__verify_command__agrees_with_public_result(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.command.verify-agrees-with-api

    Requirement: The maintained check command renders every public verifier result
    field without changing names or values and exits successfully.

    Method: Supply one immutable literal verifier result, invoke the maintained command
    with an explicit absolute root, and parse its JSON output independently.

    Oracle: The literal dataclass field values define the public API result.

    Acceptance: Exit status is zero and rendered JSON equals the exact literal mapping.

    Interpretation: Failure indicates command/API rendering or dispatch drift.

    Limitations: SQLite reconstruction is owned by verifier evidence and is not repeated.
    """  # noqa: E501
    expected = HarnessControlVerificationResult("ok", 0, "a", "a", "c", "c", True)
    monkeypatch.setattr(HarnessControlVerifier, "execute", lambda self, root: expected)
    monkeypatch.setattr(
        sys,
        "argv",
        ["harness_control", "check", "--repository-root", str(tmp_path.resolve())],
    )
    assert projection_cli.main() == 0
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
    finding = HarnessControlVerificationFinding(
        "changed_artifact", "harness/task-graph.json", "candidate differs"
    )
    expected = HarnessControlVerificationResult(
        "ok", 0, "a", "a", "c", "d", False, True, True, True, (finding,)
    )
    monkeypatch.setattr(HarnessControlVerifier, "execute", lambda self, root: expected)
    monkeypatch.setattr(
        sys,
        "argv",
        ["harness_control", "check", "--repository-root", str(tmp_path.resolve())],
    )
    assert projection_cli.main() == 1
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

    Method: Inject one runtime failure at the public verifier seam.

    Oracle: The maintained command exit contract reserves three for internal errors.

    Acceptance: Exit is three and output contains exact status and error type.

    Interpretation: Failure leaks or misclassifies an unexpected boundary failure.

    Limitations: Expected drift is covered separately.
    """  # noqa: E501

    def fail(self: object, root: Path) -> HarnessControlVerificationResult:
        raise RuntimeError("injected failure")

    monkeypatch.setattr(HarnessControlVerifier, "execute", fail)
    monkeypatch.setattr(
        sys,
        "argv",
        ["harness_control", "check", "--repository-root", str(tmp_path.resolve())],
    )
    assert projection_cli.main() == 3
    assert json.loads(capsys.readouterr().out) == {
        "error": "RuntimeError: injected failure",
        "status": "INTERNAL_ERROR",
    }
