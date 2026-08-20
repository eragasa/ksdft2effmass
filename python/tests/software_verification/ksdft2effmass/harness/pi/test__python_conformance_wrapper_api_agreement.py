r"""Software verification of Python conformance wrapper/API agreement.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies the conformance package surface and thin command relation.

Intrinsic and cross-object scope

The primary artifact is wrapper/API agreement; controlled source and JSON bytes are
shared inputs, and the public result fields define the exact comparison projection.

VVUQ and scientific exclusions

Passing establishes command/API software parity only, not semantic test quality,
numerical verification, scientific validation, UQ, portability, or acceptance.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

import ksdft2effmass.harness.pi as root_api
import ksdft2effmass.harness.pi.conformance as conformance_api
import ksdft2effmass.harness.pi.conformance.python as api
from ksdft2effmass.harness.cli import validate_python_conformance as command_owner
from ksdft2effmass.harness.pi.conformance.python import (
    PythonConformanceFinding,
    PythonConformanceRequest,
    PythonConformanceResult,
    PythonConformanceValidator,
    PythonModuleSource,
)

pytestmark = pytest.mark.software_verification
ROOT = Path(__file__).resolve().parents[6]
COMMAND = (
    sys.executable,
    "-m",
    "ksdft2effmass.harness.cli",
    "validate-python-conformance",
)
PUBLIC_NAMES = (
    "PythonModuleSource",
    "PythonConformanceRequest",
    "PythonConformanceFinding",
    "PythonConformanceResult",
    "PythonConformanceValidator",
)
VALID_SOURCE = b'''r"""Software verification of wrapper agreement artifact.

Facet and represented meaning

This fixture represents one exact software artifact.

Intrinsic and cross-object scope

The controlled artifact and literal equality supply the complete oracle.

VVUQ and scientific exclusions

Passing establishes software structure only, not validation or UQ.
"""


def test_artifact__literal_value__equals_itself():
    """Evidence ID: SV-TEV-WRAP-FIX-001

    Requirement: The literal value equals itself.

    Method: Compare one controlled integer literal.

    Oracle: Python integer equality fixes the result.

    Acceptance: Equality is exactly true.

    Interpretation: Failure identifies fixture drift.

    Limitations: No scientific, numerical, or UQ claim is made.
    """
    assert 1 == 1
'''
INVALID_SOURCE = b'"""bad"""\n\ndef test_bad():\n    pass\n'
INCOMPLETE_MIGRATION = json.dumps(
    {
        "schema_version": 1,
        "expected_old_node_ids": ["old.py::test_old"],
        "expected_new_node_ids": ["new.py::test_new"],
        "mappings": [],
    },
    separators=(",", ":"),
).encode()


def test_public_api__exports__uses_direct_names_and_exact_defining_module() -> None:
    """Evidence ID: SV-TEV-023

    Requirement: The public conformance package exposes its Python records, results,
    and Action only from the ``conformance.python`` owning package.

    Method: Compare direct imports, package attributes, ``__all__``, and ``__module__``.

    Oracle: The accepted source-based evidence contract fixes the exact names and
    ``conformance.python`` defining module.

    Acceptance: Package and owner ``__all__`` values are exact, direct imports and
    defining modules agree, and the retired evidence facade and old object aliases are
    absent.

    Interpretation: Failure identifies package-export or placement drift.

    Limitations: Import agreement does not establish behavior or release compatibility.
    """
    imported = (
        PythonModuleSource,
        PythonConformanceRequest,
        PythonConformanceFinding,
        PythonConformanceResult,
        PythonConformanceValidator,
    )
    assert root_api.conformance is conformance_api
    assert conformance_api.__all__ == ("python",)
    assert conformance_api.python is api
    assert api.__all__ == PUBLIC_NAMES
    assert imported == tuple(getattr(api, name) for name in PUBLIC_NAMES)
    assert {value.__module__ for value in imported} == {
        "ksdft2effmass.harness.pi.conformance.python"
    }
    assert importlib.util.find_spec("ksdft2effmass.harness.pi.evidence") is None
    assert importlib.util.find_spec("ksdft2effmass.harness.pi.test_evidence") is None
    old_names = {
        "AuditEvidenceIdentifiers",
        "EvidenceAuditResult",
        "PythonTestEvidenceFinding",
        "PythonTestEvidenceRequest",
        "PythonTestEvidenceSource",
        "PythonTestEvidenceValidationResult",
        "ValidatePythonTestEvidence",
    }
    assert not any(hasattr(api, name) for name in old_names)
    assert not hasattr(root_api, "evidence")
    assert not any(hasattr(root_api, name) for name in old_names | set(PUBLIC_NAMES))


@pytest.mark.parametrize(
    ("payload", "migration_payload", "expected_status"),
    (
        pytest.param(VALID_SOURCE, None, "PASS", id="controlled_valid_source"),
        pytest.param(
            INVALID_SOURCE,
            None,
            "FAIL",
            id="representative_invalid_source",
        ),
        pytest.param(
            VALID_SOURCE,
            INCOMPLETE_MIGRATION,
            "FAIL",
            id="incomplete_migration_mapping",
        ),
    ),
)
def test_artifact__wrapper_api_projection__has_exact_parity(
    payload: bytes,
    migration_payload: bytes | None,
    expected_status: str,
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-TEV-024

    Requirement: The wrapper and public action have exact status, finding, ordering,
    count, path,
    JSON-shape, and exit-status parity on the same controlled cases.

    Method: Write shared explicit bytes for the compatibility command, execute it, and
    independently execute the public action over those identical bytes.

    Oracle: The thin-wrapper contract requires its JSON to be the lossless public result
    projection and exit zero exactly for PASS.

    Acceptance: Parsed command JSON equals the literal public-field projection, path and
    code
    order match, and exit status matches both status and the declared case.

    Interpretation: Failure identifies wrapper translation, command, API, or fixture
    drift.

    Limitations: Temporary-file orchestration is tested; no repository discovery is
    implied.
    """
    module = tmp_path / "test__wrapper_agreement.py"
    module.write_bytes(payload)
    ownership = tmp_path / "ownership.json"
    ownership_payload = json.dumps(
        {
            "schema_version": 1,
            "modules": [
                {
                    "path": module.as_posix(),
                    "mode": "artifact_owned",
                    "evidence_class": "software_verification",
                    "artifact": "wrapper agreement artifact",
                }
            ],
        },
        separators=(",", ":"),
    ).encode()
    ownership.write_bytes(ownership_payload)
    migration = tmp_path / "migration.json"
    arguments = [
        *COMMAND,
        "--ownership",
        str(ownership),
    ]
    if migration_payload is not None:
        migration.write_bytes(migration_payload)
        arguments.extend(("--migration-map", str(migration)))
    arguments.append(str(module))
    completed = subprocess.run(
        arguments,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    command_value = json.loads(completed.stdout)
    result = PythonConformanceValidator().execute(
        PythonConformanceRequest(
            (PythonModuleSource(module.as_posix(), payload),),
            ownership.as_posix(),
            ownership_payload,
            None,
            migration.as_posix() if migration_payload is not None else None,
            migration_payload,
        )
    )
    expected = {
        "claim_boundary": list(result.claim_boundary),
        "counts": {
            "artifact_owned_modules": result.artifact_owned_modules,
            "class_owned_modules": result.class_owned_modules,
            "evidence_class_modules": dict(result.evidence_class_modules),
            "findings_by_code": dict(result.findings_by_code),
            "helper_functions": result.helper_functions,
            "modules": result.modules,
            "parameterized_functions": result.parameterized_functions,
            "static_collected_parameter_cases": result.static_collected_parameter_cases,
            "test_functions": result.test_functions,
            "unique_evidence_owners": result.unique_evidence_owners,
        },
        "findings": [
            {
                **{
                    "code": item.code,
                    "message": item.message,
                    "path": item.path,
                    "severity": item.severity,
                },
                **({"line": item.line} if item.line is not None else {}),
            }
            for item in result.findings
        ],
        "paths": list(result.paths),
        "schema_version": result.schema_version,
        "status": result.status,
    }
    assert command_value == expected
    assert command_value["status"] == expected_status
    assert [item["code"] for item in command_value["findings"]] == [
        item.code for item in result.findings
    ]
    assert completed.returncode == (0 if result.status == "PASS" else 1)


def test_artifact__wrapper_json__is_deterministic_for_identical_command() -> None:
    """Evidence ID: SV-TEV-025

    Requirement: Repeating the same compatibility command emits identical canonical JSON
    bytes.

    Method: Run the wrapper twice against the same accepted repository fixture and
    ownership.

    Oracle: The command contract fixes sorted compact JSON and deterministic validation
    order.

    Acceptance: Both executions pass and stdout bytes are exactly equal with no stderr.

    Interpretation: Failure identifies nondeterministic validation or serialization
    drift.

    Limitations: This does not establish equality across Python versions or operating
    systems.
    """
    arguments = [
        *COMMAND,
        "--ownership",
        "harness/pi/fixtures/evidence/python-conformance/valid/ownership.json",
        "harness/pi/fixtures/evidence/python-conformance/valid/test__ExampleRecord.py",
    ]
    first = subprocess.run(
        arguments,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    second = subprocess.run(
        arguments,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr == ""


def test_artifact__command_dispatch__forwards_exact_inputs_to_operation_owner(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Evidence ID: software-verification.harness.python-conformance.command-owner

    Requirement: The CLI forwards selected module and metadata paths to one complete
    conformance-operation owner without parsing or synthesizing evidence metadata.

    Method: Replace the operation owner with a recorder returning one literal passing
    result and invoke the command adapter with four distinct paths.

    Oracle: The explicit argument literals fix the exact ActionObject call.

    Acceptance: One owner call receives the exact path tuple and optional paths; the
    command returns zero and renders the supplied PASS result.

    Interpretation: Failure identifies command-owned domain transformation or routing
    drift.

    Limitations: File reading and conformance semantics remain with focused owner/API
    evidence.
    """
    module = tmp_path / "test__Example.py"
    ownership = tmp_path / "ownership.json"
    migration = tmp_path / "migration.json"
    profile = tmp_path / "profile.json"
    observed: list[object] = []
    result = SimpleNamespace(
        claim_boundary=(),
        artifact_owned_modules=0,
        class_owned_modules=0,
        evidence_class_modules=(),
        findings_by_code=(),
        helper_functions=0,
        modules=1,
        parameterized_functions=0,
        static_collected_parameter_cases=0,
        test_functions=0,
        unique_evidence_owners=0,
        findings=(),
        paths=(module.as_posix(),),
        schema_version=1,
        status="PASS",
    )

    def execute_literal(
        self: object,
        paths: tuple[Path, ...],
        ownership_path: Path | None,
        migration_path: Path | None,
        profile_path: Path | None,
    ) -> object:
        observed.append((paths, ownership_path, migration_path, profile_path))
        return result

    monkeypatch.setattr(
        command_owner._PythonConformanceCommandValidator,
        "execute",
        execute_literal,
    )
    exit_status = command_owner.run(
        [
            "--ownership",
            str(ownership),
            "--migration-map",
            str(migration),
            "--profile-matrix",
            str(profile),
            str(module),
        ]
    )
    assert observed == [((module,), ownership, migration, profile)]
    assert exit_status == 0
    assert json.loads(capsys.readouterr().out)["status"] == "PASS"
