r"""Software verification of audit evidence identifiers command API agreement.

Facet and represented meaning
Software verification of the thin project-local command projection of the public
``AuditEvidenceIdentifiers`` ActionObject.

Intrinsic and cross-object scope
The primary owner is the explicit-root, explicit-inventory command/API artifact.
Argument parsing, profile loading, inventory identity, projection, exit status, root
confinement, and nonmutation are in scope.

VVUQ and scientific exclusions
Passing establishes structural command/API agreement only. Semantic cohesion, oracle
independence, numerical correctness, scientific validation, uncertainty quantification,
and human acceptance are excluded.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import (
    AuditEvidenceIdentifiers,
    DeserializeJsonRecord,
    ProjectProfile,
    WireRecordKind,
)
from ksdft2effmass.harness.pi.local.audit_evidence_identifiers import main

pytestmark = pytest.mark.software_verification


def valid_source(identifier: str = "VX-A-001") -> bytes:
    """Evidence ID
    Owns no identifier; supports command/API evidence.
    Requirement
    Command tests require one convention-compliant marked module.
    Method
    Interpolate one controlled identifier into fixed source bytes.
    Oracle
    The accepted field and marker grammar defines valid support input.
    Acceptance
    Return deterministic UTF-8 Python bytes.
    Interpretation
    Failure identifies setup rather than command behavior.
    Limitations
    This helper owns no independent evidence claim.
    """
    return (
        "import pytest\n"
        "pytestmark = pytest.mark.verification_alpha\n"
        "def test_owner():\n"
        '    """Evidence ID\n'
        f"    ``{identifier}``.\n"
        "    Requirement\n"
        '    Exact controlled behavior.\n    """\n'
    ).encode()


def prepare_inputs(root: Path, payload: bytes) -> tuple[Path, Path, str]:
    """Evidence ID
    Owns no identifier; supports command/API evidence.
    Requirement
    CLI tests require explicit profile, inventory, and module files.
    Method
    Write controlled files beneath a temporary supplied root.
    Oracle
    Public profile bytes and SHA-256 define exact support inputs.
    Acceptance
    Return profile path, inventory path, and module-relative path.
    Interpretation
    Failure identifies invalid setup.
    Limitations
    Writes are confined to the controlled temporary tree.
    """
    repository = Path(__file__).resolve().parents[7]
    profile_bytes = (
        repository / "harness/pi/fixtures/valid/project-profile.json"
    ).read_bytes()
    profile_path = root / "profile.json"
    profile_path.write_bytes(profile_bytes)
    relative = "tests/classification-alpha/test_owner.py"
    module_path = root / relative
    module_path.parent.mkdir(parents=True)
    module_path.write_bytes(payload)
    inventory = {
        "expected_module_count": 1,
        "modules": [
            {
                "content_sha256": hashlib.sha256(payload).hexdigest(),
                "path": relative,
            }
        ],
    }
    inventory_path = root / "inventory.json"
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
    return profile_path, inventory_path, relative


def file_snapshot(root: Path) -> dict[str, bytes]:
    """Evidence ID
    Owns no identifier; supports command/API evidence.
    Requirement
    Nonmutation assertions require exact controlled-tree bytes.
    Method
    Read regular files beneath the temporary test root.
    Oracle
    Relative path and byte equality are exact.
    Acceptance
    Return a path-sorted byte mapping.
    Interpretation
    Failure identifies snapshot setup drift.
    Limitations
    This helper is used only on controlled temporary trees.
    """
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_artifact__command_api__agrees_on_success_and_exact_inventory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID
    ``SV-HARNESS-119``.
    Requirement
    The CLI and ActionObject agree for the exact inventory without discovery or writes.
    Method
    Create one inventoried valid module plus an unlisted invalid module, change to a
    nonrepository CWD, invoke main, and compare its JSON with direct API output.
    Oracle
    The public ActionObject and exact input bytes independently fix the projection.
    Acceptance
    Exit is zero; status, occurrence, ID, path, line, and counts agree; the unlisted
    file is ignored; all controlled bytes remain unchanged.
    Interpretation
    Failure indicates projection, inventory, discovery, CWD, or mutation drift.
    Limitations
    Direct main invocation excludes interpreter installation behavior.
    """
    root = tmp_path / "explicit-root"
    root.mkdir()
    profile_path, inventory_path, relative = prepare_inputs(root, valid_source())
    unlisted = root / "tests/classification-alpha/test_unlisted.py"
    unlisted.write_bytes(b"not python !")
    before = file_snapshot(root)

    decoded = DeserializeJsonRecord().execute(
        WireRecordKind.ProjectProfile, profile_path.read_bytes()
    )
    assert isinstance(decoded.record, ProjectProfile)
    direct = AuditEvidenceIdentifiers().execute(
        ((relative, (root / relative).read_bytes()),), decoded.record
    )

    outside = tmp_path / "outside-cwd"
    outside.mkdir()
    monkeypatch.chdir(outside)
    exit_status = main(
        (
            "--root",
            str(root.resolve()),
            "--profile",
            "profile.json",
            "--inventory",
            "inventory.json",
        )
    )
    output = json.loads(capsys.readouterr().out)

    assert exit_status == 0
    assert output["status"] == direct.validation.status == "PASS"
    assert output["occurrences"] == [
        {"evidence_id": "VX-A-001", "line": 3, "path": relative}
    ]
    assert output["counts"] == {
        "inventoried_modules": 1,
        "issues": 0,
        "issues_by_code": {},
        "occurrences": 1,
        "unique_evidence_ids": 1,
    }
    assert file_snapshot(root) == before


def test_artifact__command_request__rejects_empty_inventory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID
    ``SV-HARNESS-154``.
    Requirement
    The command rejects an explicit zero-module inventory before performing an audit.
    Method
    Supply ``expected_module_count`` zero with an empty modules array, prevent any
    ActionObject execution, snapshot the inputs, and invoke the maintained command.
    Oracle
    The accepted command contract requires canonical ERROR JSON, exit 2, and the
    stable message ``modules must be nonempty`` for an empty inventory.
    Acceptance
    The exact canonical payload and exit status are returned, the audit is not
    invoked, and every controlled input byte remains unchanged.
    Interpretation
    Failure identifies empty-inventory fail-open, audit invocation, or input mutation.
    Limitations
    Nonempty inventory identity and audit-result projection are covered separately.
    """
    root = tmp_path / "root"
    root.mkdir()
    profile_path, inventory_path, _ = prepare_inputs(root, valid_source())
    inventory_path.write_text(
        json.dumps({"expected_module_count": 0, "modules": []}), encoding="utf-8"
    )
    before_profile = profile_path.read_bytes()
    before_inventory = inventory_path.read_bytes()

    def fail_if_audit_runs(*args: object, **kwargs: object) -> None:
        raise AssertionError("audit must not run for an empty inventory")

    monkeypatch.setattr(AuditEvidenceIdentifiers, "execute", fail_if_audit_runs)
    exit_status = main(
        (
            "--root",
            str(root.resolve()),
            "--profile",
            "profile.json",
            "--inventory",
            "inventory.json",
        )
    )
    rendered = capsys.readouterr().out

    assert exit_status == 2
    assert rendered == (
        '{"error":"modules must be nonempty","schema_version":1,"status":"ERROR"}\n'
    )
    assert json.loads(rendered) == {
        "error": "modules must be nonempty",
        "schema_version": 1,
        "status": "ERROR",
    }
    assert "counts" not in json.loads(rendered)
    assert "occurrences" not in json.loads(rendered)
    assert profile_path.read_bytes() == before_profile
    assert inventory_path.read_bytes() == before_inventory


def test_artifact__command_api__maps_failed_audit_to_exit_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID
    ``SV-HARNESS-120``.
    Requirement
    An ActionObject audit failure returns deterministic JSON and exit 1.
    Method
    Inventory one marked module with an empty Evidence ID field.
    Oracle
    The public grammar and command exit contract fix FAIL and ID_INVALID.
    Acceptance
    Exit is one with one ID_INVALID finding and no occurrences.
    Interpretation
    Failure indicates audit-status or exit-translation drift.
    Limitations
    Invalid command construction is covered separately.
    """
    root = tmp_path / "root"
    root.mkdir()
    payload = valid_source().replace(b"``VX-A-001``.", b"")
    prepare_inputs(root, payload)
    exit_status = main(
        (
            "--root",
            str(root.resolve()),
            "--profile",
            "profile.json",
            "--inventory",
            "inventory.json",
        )
    )
    output = json.loads(capsys.readouterr().out)
    assert exit_status == 1
    assert output["status"] == "FAIL"
    assert output["occurrences"] == []
    assert output["counts"]["issues_by_code"] == {"PIH.EVIDENCE.ID_INVALID": 1}


@pytest.mark.parametrize(
    "partition",
    (
        pytest.param("profile_outside_root", id="profile_outside_root"),
        pytest.param("inventory_identity_mismatch", id="inventory_identity_mismatch"),
    ),
)
def test_artifact__command_request__rejects_invalid_confined_inputs(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    partition: str,
) -> None:
    """Evidence ID
    ``SV-HARNESS-121``.
    Requirement
    Invalid or root-escaping explicit requests fail before ActionObject execution.
    Method
    Supply either an outside-root profile or a stale inventoried content identity.
    Oracle
    Lexical explicit-root confinement and SHA-256 equality are exact request rules.
    Acceptance
    Each partition returns exit 2 and deterministic ERROR JSON.
    Interpretation
    Failure indicates path-confinement or inventory-identity drift.
    Limitations
    Operating-system permission failures are not simulated.
    """
    root = tmp_path / "root"
    root.mkdir()
    profile_path, inventory_path, relative = prepare_inputs(root, valid_source())
    profile_arg = "profile.json"
    if partition == "profile_outside_root":
        outside = tmp_path / "outside-profile.json"
        outside.write_bytes(profile_path.read_bytes())
        profile_arg = str(outside.resolve())
    else:
        (root / relative).write_bytes(valid_source("VX-A-002"))

    exit_status = main(
        (
            "--root",
            str(root.resolve()),
            "--profile",
            profile_arg,
            "--inventory",
            str(inventory_path.relative_to(root)),
        )
    )
    output = json.loads(capsys.readouterr().out)
    assert exit_status == 2
    assert output["status"] == "ERROR"


def test_artifact__command_request__requires_absolute_root_without_mutation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID
    ``SV-HARNESS-122``.
    Requirement
    The command rejects an implicit relative root and never mutates request files.
    Method
    Prepare valid inputs, snapshot them, and invoke main with a relative root.
    Oracle
    The documented explicit absolute-root contract is exact.
    Acceptance
    Exit is two, status is ERROR, and every file remains byte-identical.
    Interpretation
    Failure indicates implicit-CWD behavior or command-side mutation.
    Limitations
    The ActionObject itself has no filesystem boundary.
    """
    root = tmp_path / "root"
    root.mkdir()
    prepare_inputs(root, valid_source())
    before = file_snapshot(root)
    exit_status = main(
        (
            "--root",
            "root",
            "--profile",
            "profile.json",
            "--inventory",
            "inventory.json",
        )
    )
    output = json.loads(capsys.readouterr().out)
    assert exit_status == 2
    assert output["status"] == "ERROR"
    assert file_snapshot(root) == before
