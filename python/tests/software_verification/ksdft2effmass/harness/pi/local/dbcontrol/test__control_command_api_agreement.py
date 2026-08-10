r"""Software verification of maintained harness control command/API agreement.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the cohesive control command/API agreement artifact.

Intrinsic and cross-object scope

The command rendering is compared with a literal public Action result at the closest
mirrored package seam.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import json
import sys
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessControlMigrationRequest,
    HarnessControlMigrationResult,
    HarnessControlVerificationResult,
    control_cli,
)
from ksdft2effmass.harness.pi.local.dbcontrol.migration import HarnessControlMigrator
from ksdft2effmass.harness.pi.local.dbcontrol.verification import HarnessControlVerifier

pytestmark = pytest.mark.software_verification


def test_artifact__migrate_command__forwards_explicit_ownership_input(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.command.migrate-forwards-explicit-ownership-input

    Requirement: The maintained migrate command forwards its repository-relative evidence ownership and canonical resource paths through the public request without changing migration signatures.

    Method: Invoke the command with an explicit root, ownership, profile, manifests, and resource roots while replacing the public migrator with a literal-result seam.

    Oracle: The command arguments define the exact repository-relative request values.

    Acceptance: Exit status is zero, the captured request preserves the resolved root and every exact relative path, and JSON rendering uses the public result fields.

    Interpretation: Failure indicates CLI/API dispatch drift or loss of explicit input confinement.

    Limitations: Ownership conformance and persistence are owned by migrator evidence.
    """  # noqa: E501
    expected = HarnessControlMigrationResult(2, "digest", (), (), ())
    observed: list[HarnessControlMigrationRequest] = []

    def execute_literal(
        self: HarnessControlMigrator, request: HarnessControlMigrationRequest
    ) -> HarnessControlMigrationResult:
        observed.append(request)
        return expected

    monkeypatch.setattr(HarnessControlMigrator, "execute", execute_literal)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "control_cli",
            "migrate",
            "--repository-root",
            str(tmp_path.resolve()),
            "--evidence-module-ownership",
            "updates/modules.json",
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
    assert control_cli.main() == 0
    request = observed[0]
    assert request.repository_root == tmp_path.resolve()
    assert request.evidence_module_ownership_path == Path("updates/modules.json")
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

    Requirement: The verify command rejects both evidence and resource inputs with an
    accurate migration-only diagnostic.

    Method: Invoke verify with one explicit resource profile option and capture the
    parser failure text.

    Oracle: Resource profiles participate only in migration, while verification accepts
    only the repository root.

    Acceptance: Parsing raises ``SystemExit`` with status two and stderr says evidence
    and resource inputs are valid only with migrate.

    Interpretation: Failure indicates inaccurate CLI guidance or a widened verifier API.

    Limitations: Successful verification rendering is covered separately.
    """  # noqa: E501
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "control_cli",
            "verify",
            "--repository-root",
            str(tmp_path.resolve()),
            "--resource-profile",
            "harness/local/profiles/project.json",
        ],
    )
    with pytest.raises(SystemExit) as raised:
        control_cli.main()
    assert raised.value.code == 2
    assert (
        "evidence and resource inputs are valid only with migrate"
        in capsys.readouterr().err
    )


def test_artifact__verify_command__agrees_with_public_result(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.command.verify-agrees-with-api

    Requirement: The maintained verify command renders every public verifier result
    field without changing names or values and exits successfully.

    Method: Supply one immutable literal verifier result, invoke the maintained command
    with an explicit absolute root, and parse its JSON output independently.

    Oracle: The seven literal dataclass field values define the public API result.

    Acceptance: Exit status is zero and rendered JSON equals the exact literal mapping.

    Interpretation: Failure indicates command/API rendering or dispatch drift.

    Limitations: SQLite reconstruction is owned by verifier evidence and is not repeated.
    """  # noqa: E501
    expected = HarnessControlVerificationResult("ok", 0, "a", "b", "c", "d", True)
    monkeypatch.setattr(HarnessControlVerifier, "execute", lambda self, root: expected)
    monkeypatch.setattr(
        sys,
        "argv",
        ["control_cli", "verify", "--repository-root", str(tmp_path.resolve())],
    )
    assert control_cli.main() == 0
    assert json.loads(capsys.readouterr().out) == {
        "integrity_check": "ok",
        "foreign_key_issue_count": 0,
        "semantic_digest": "a",
        "reconstructed_semantic_digest": "b",
        "raw_database_sha256": "c",
        "reconstructed_database_sha256": "d",
        "projections_identical": True,
    }
