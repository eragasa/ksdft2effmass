#!/usr/bin/env python3
"""Audit the retained parent request against authenticated historical Git objects."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from importlib.metadata import version
from pathlib import Path
from typing import cast

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    ParentQualificationRequestJsonSerializer,
)
from ksdft2effmass.solidstate import ScalarHoppingModel

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)

CALCULATION_FAMILY = "periodic2d-rank-defect"
EXECUTION_ID = "parent-qualification-v1"
IMPLEMENTATION_IDENTITY_REVISION = "12a5540ef196fe2a188271977d1f67fbe85eb9bc"
AUDIT_SCRIPT_PATH = (
    "calculations/periodic2d_rank_defect/run_09_audit_parent_qualification_source.py"
)


def canonical_json(payload: dict[str, JsonValue]) -> bytes:
    """Encode one deterministic retained JSON record."""
    return (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def historical_bytes(root: Path, revision: str, path: str) -> bytes:
    """Read one exact historical Git object without restoring its source tree."""
    completed = subprocess.run(
        ("git", "show", f"{revision}:{path}"),
        cwd=root,
        check=True,
        capture_output=True,
    )
    return completed.stdout


def json_object(content: bytes, name: str) -> dict[str, JsonValue]:
    """Decode one JSON object through a closed recursive representation."""
    value = cast(JsonValue, json.loads(content))
    if type(value) is not dict:
        raise ValueError(f"{name} must contain one JSON object")
    return value


def require_object(value: JsonValue, name: str) -> dict[str, JsonValue]:
    """Return one required JSON object."""
    if type(value) is not dict:
        raise ValueError(f"{name} must be an object")
    return value


def require_list(value: JsonValue, name: str) -> list[JsonValue]:
    """Return one required JSON array."""
    if type(value) is not list:
        raise ValueError(f"{name} must be an array")
    return value


def require_float(value: JsonValue, name: str) -> float:
    """Return one required JSON float or integer as an exact float."""
    if type(value) not in {int, float}:
        raise ValueError(f"{name} must be real")
    return float(cast(int | float, value))


def require_int(value: JsonValue, name: str) -> int:
    """Return one required built-in integer."""
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    return value


def model_records(model: ScalarHoppingModel) -> list[list[int | float]]:
    """Return one model in the historical compact hopping representation."""
    records: list[list[int | float]] = []
    for term in model.terms:
        components = term.displacement.components
        if len(components) != 2:
            raise AssertionError("two-dimensional hopping displacement was lost")
        records.append(
            [components[0], components[1], float(term.real), float(term.imaginary)]
        )
    return records


def historical_records(values: JsonValue, name: str) -> list[list[int | float]]:
    """Extract historical hopping records in canonical displacement order."""
    result: list[list[int | float]] = []
    for index, value in enumerate(require_list(values, name)):
        record = require_object(value, f"{name}[{index}]")
        result.append(
            [
                require_int(record.get("rx"), "rx"),
                require_int(record.get("ry"), "ry"),
                require_float(record.get("real"), "real"),
                require_float(record.get("imag"), "imag"),
            ]
        )
    return result


def hopping_digest(records: list[list[int | float]]) -> str:
    """Return the historical compact hopping digest."""
    return hashlib.sha256(
        json.dumps(records, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def write_exclusive(path: Path, payload: bytes) -> None:
    """Create one audit artifact without replacement."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(payload)


def audit(execution_root: Path) -> None:
    """Authenticate exact request projections and append a provenance amendment."""
    execution_root = execution_root.resolve(strict=True)
    calculation_root = Path(__file__).resolve().parent
    repository_root = calculation_root.parent.parent.resolve()
    request_path = execution_root / "inputs/request.json"
    manifest_path = execution_root / "manifest.json"
    audit_path = execution_root / "source-projection-audit.json"
    amendment_path = execution_root / "manifest-amendment-v1.json"
    for output_path in (audit_path, amendment_path):
        if output_path.exists():
            raise FileExistsError(f"refusing to overwrite {output_path}")
    request_bytes = request_path.read_bytes()
    definition = ParentQualificationRequestJsonSerializer().deserialize(request_bytes)
    source_by_role = {source.role: source for source in definition.sources}
    expected_paths = {
        "accepted_periodic_parent_input": (
            "calculations/research-monograph/periodic-2d/input.json"
        ),
        "accepted_periodic_parent_result": (
            "calculations/research-monograph/periodic-2d/result.json"
        ),
        "accepted_stage_b_parent_and_route_evidence": (
            "calculations/research-monograph/impurity-defect-2d/stage-b-result.json"
        ),
        "accepted_stage_c_numerical_verification_result": (
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-result.json"
        ),
    }
    if set(source_by_role) != set(expected_paths):
        raise ValueError("parent qualification source-role inventory differs")
    historical: dict[str, dict[str, JsonValue]] = {}
    source_records: list[JsonValue] = []
    for role, source_path in expected_paths.items():
        binding = source_by_role[role]
        if binding.path != source_path:
            raise ValueError(f"historical source path differs for {role}")
        content = historical_bytes(
            repository_root, definition.source_revision, source_path
        )
        digest = hashlib.sha256(content).hexdigest()
        if digest != binding.sha256:
            raise ValueError(f"historical source identity differs for {role}")
        historical[role] = json_object(content, role)
        source_records.append(
            {
                "role": role,
                "path": source_path,
                "sha256": digest,
                "bytes": len(content),
            }
        )

    stage_b = historical["accepted_stage_b_parent_and_route_evidence"]
    periodic_result = historical["accepted_periodic_parent_result"]
    periodic_input = historical["accepted_periodic_parent_input"]
    stage_c = historical["accepted_stage_c_numerical_verification_result"]
    compact_source = historical_records(stage_b.get("input_hoppings"), "input_hoppings")
    compact_request = model_records(definition.isotropic_parent)
    if compact_source != compact_request:
        raise ValueError("isotropic compact parent projection differs from Stage B")
    continuation = require_list(
        periodic_result.get("coupling_continuation"), "coupling_continuation"
    )
    zero_coupling: dict[str, JsonValue] | None = None
    for index, value in enumerate(continuation):
        record = require_object(value, f"coupling_continuation[{index}]")
        if require_float(record.get("lambda_xy"), "lambda_xy") == 0.0:
            zero_coupling = record
            break
    if zero_coupling is None:
        raise ValueError("accepted periodic result lacks lambda_xy=0 parent")
    full_source = historical_records(
        zero_coupling.get("hopping_coefficients"), "hopping_coefficients"
    )
    full_request = model_records(definition.isotropic_pretruncation_parent)
    if full_source != full_request:
        raise ValueError("isotropic pretruncation projection differs")
    anisotropic_input = require_object(
        periodic_input.get("anisotropic_control"), "anisotropic_control"
    )
    observed_parameters = (
        require_float(anisotropic_input.get("lambda_x"), "lambda_x"),
        require_float(anisotropic_input.get("lambda_y"), "lambda_y"),
        require_float(anisotropic_input.get("lambda_xy"), "lambda_xy"),
    )
    if observed_parameters != (
        definition.anisotropic_lambda_x,
        definition.anisotropic_lambda_y,
        definition.anisotropic_lambda_xy,
    ):
        raise ValueError("anisotropic parameter projection differs")
    if (
        require_int(
            periodic_input.get("plane_wave_reference_cutoff"),
            "plane_wave_reference_cutoff",
        )
        != definition.plane_wave_cutoff
    ):
        raise ValueError("plane-wave cutoff projection differs")
    if (
        require_int(periodic_input.get("reciprocal_mesh_size"), "reciprocal_mesh_size")
        != definition.reciprocal_mesh_size
    ):
        raise ValueError("reciprocal mesh projection differs")
    summary = require_object(stage_c.get("summary"), "Stage C summary")
    if summary.get("all_criteria_passed") is not True:
        raise ValueError("historical accepted Stage C criteria did not all pass")
    schedules = require_list(stage_c.get("schedules"), "Stage C schedules")
    preprocessing = require_object(
        require_object(schedules[0], "schedule[0]").get("preprocessing"),
        "preprocessing",
    )
    historical_parent_digests = {
        "isotropic_lambda_0p5_0p5_0": require_object(
            preprocessing.get("isotropic"), "isotropic preprocessing"
        ).get("sha256"),
        "anisotropic_lambda_0p3_0p7_0": require_object(
            preprocessing.get("compact"), "compact preprocessing"
        ).get("sha256"),
        "anisotropic_lambda_0p7_0p3_0": require_object(
            preprocessing.get("axis_swapped"), "axis-swapped preprocessing"
        ).get("sha256"),
    }
    if historical_parent_digests != dict(definition.expected_parent_digests):
        raise ValueError("expected compact parent identities differ from Stage C")
    pretruncation_digest = require_object(
        preprocessing.get("pretruncation"), "pretruncation"
    ).get("sha256")
    if type(pretruncation_digest) is not str:
        raise ValueError("historical anisotropic pretruncation identity is absent")

    # The amendment authenticates the implementation snapshot that produced it,
    # not whichever mutable source files happen to be checked out during replay.
    retained_audit_script = historical_bytes(
        repository_root,
        IMPLEMENTATION_IDENTITY_REVISION,
        AUDIT_SCRIPT_PATH,
    )
    audit_payload = canonical_json(
        {
            "schema_version": 1,
            "record_type": ("periodic2d_rank_defect_parent_qualification_source_audit"),
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "outcome": "passed",
            "source_revision": definition.source_revision,
            "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
            "audit_script_sha256": hashlib.sha256(retained_audit_script).hexdigest(),
            "sources": source_records,
            "projection_checks": {
                "isotropic_compact_exact_record_match": True,
                "isotropic_compact_count": len(compact_request),
                "isotropic_compact_digest": hopping_digest(compact_request),
                "isotropic_pretruncation_exact_record_match": True,
                "isotropic_pretruncation_count": len(full_request),
                "isotropic_pretruncation_digest": hopping_digest(full_request),
                "anisotropic_parameters_exact_match": True,
                "anisotropic_pretruncation_digest": pretruncation_digest,
                "compact_parent_digests_match_stage_c": True,
                "historical_stage_c_all_criteria_passed": True,
            },
            "software_versions": {
                "ksdft2effmass": version("ksdft2effmass"),
                "projectkoios_physkit": version("projectkoios-physkit"),
                "numpy": version("numpy"),
                "scipy": version("scipy"),
                "matplotlib": version("matplotlib"),
            },
            "claim_boundary": (
                "Read-only authentication of a compact historical synthetic parent "
                "projection; no new parent calculation, defect campaign, material "
                "validation, convergence claim, or protected execution."
            ),
        }
    )
    write_exclusive(audit_path, audit_payload)

    implementation_paths = (
        Path(
            "python/src/ksdft2effmass/campaigns/research_monograph/"
            "impurity_defect_2d/parent_qualification.py"
        ),
        Path(
            "python/src/ksdft2effmass/campaigns/research_monograph/"
            "impurity_defect_2d/parent_qualification_calculation.py"
        ),
        Path(
            "python/src/ksdft2effmass/campaigns/research_monograph/"
            "impurity_defect_2d/parent_qualification_serialization.py"
        ),
        Path(
            "python/src/ksdft2effmass/campaigns/research_monograph/"
            "impurity_defect_2d/parent_qualification_verification.py"
        ),
        Path(
            "python/src/ksdft2effmass/campaigns/research_monograph/"
            "impurity_defect_2d/parent_qualification_workflows.py"
        ),
        Path("calculations/periodic2d_rank_defect/run_07_qualify_parents.py"),
        Path(
            "calculations/periodic2d_rank_defect/run_08_verify_parent_qualification.py"
        ),
        Path(AUDIT_SCRIPT_PATH),
    )
    added_artifacts: list[JsonValue] = [
        {
            "path": audit_path.relative_to(execution_root).as_posix(),
            "bytes": len(audit_payload),
            "sha256": hashlib.sha256(audit_payload).hexdigest(),
        }
    ]
    for relative in implementation_paths:
        content = historical_bytes(
            repository_root,
            IMPLEMENTATION_IDENTITY_REVISION,
            relative.as_posix(),
        )
        added_artifacts.append(
            {
                "path": relative.as_posix(),
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    original_manifest = manifest_path.read_bytes()
    amendment = canonical_json(
        {
            "schema_version": 1,
            "record_type": (
                "periodic2d_rank_defect_parent_qualification_manifest_amendment"
            ),
            "execution_id": EXECUTION_ID,
            "amendment_id": "source-projection-and-implementation-identities-v1",
            "additive_only": True,
            "original_manifest_sha256": hashlib.sha256(original_manifest).hexdigest(),
            "added_artifacts": added_artifacts,
        }
    )
    write_exclusive(amendment_path, amendment)


def main() -> None:
    """Parse one retained execution root and audit its source projection."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--execution-root", type=Path, required=True)
    arguments = parser.parse_args()
    audit(arguments.execution_root)


if __name__ == "__main__":
    main()
