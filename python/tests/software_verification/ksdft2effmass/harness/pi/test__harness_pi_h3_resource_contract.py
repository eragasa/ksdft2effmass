"""Evidence class and represented meaning
Software verification of Python/H3 schema, fixture, and canonical-byte agreement; no
physical model, mathematical operator, or numerical representation is represented.

Owned contract, oracle, and scope
The primary owner is the accepted H3 resource contract. Accepted schemas, fixtures, and
canonical vectors are read-only independent oracles for the public Python wire actions.

VVUQ and scientific exclusions
Passing establishes only exact textual software agreement. Numerical verification,
scientific validation, uncertainty quantification, physical correctness, and completed
Rust conformance are excluded.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from referencing import Registry, Resource

from ksdft2effmass.harness.pi import (
    DeserializeJsonRecord,
    SerializeJsonRecord,
    WireRecordKind,
)

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification


def test_artifact__canonical_vectors__agree_with_exact_python_bytes() -> None:
    """Evidence ID
    SV-HARNESS-036
    Requirement
    Every accepted H3 canonical vector decodes and re-encodes to its exact RFC
    8785-plus-LF bytes and SHA-256 identity.
    Method
    Consume all indexed vectors, caller-select each public record kind, decode,
    encode, and hash using the public actions.
    Oracle
    H3's accepted canonical-json-vectors file independently fixes record kinds, byte
    strings, and digests.
    Acceptance
    All seventeen payloads produce PASS, byte-for-byte equality, and the exact
    indexed lowercase SHA-256 digest.
    Interpretation
    Failure identifies a Python codec, H3 vector, accepted contract, or environment
    discrepancy for independent review.
    Limitations
    This is textual software verification only; it does not establish Rust
    conformance, numerical correctness, scientific validation, or UQ.
    """
    index_path = ROOT / "harness/pi/fixtures/canonical/canonical-json-vectors.json"
    vectors = json.loads(index_path.read_text(encoding="utf-8"))["vectors"]
    assert len(vectors) == 17
    for vector in vectors:
        payload = (
            (index_path.parent / vector["instance_path"]).read_bytes()
            if "instance_path" in vector
            else (
                json.dumps(
                    vector["instance"], ensure_ascii=False, separators=(",", ":")
                )
                + "\n"
            ).encode()
        )
        decoded = DeserializeJsonRecord().execute(
            WireRecordKind(vector["record_kind"]), payload
        )
        assert decoded.validation.status == "PASS", vector["vector_id"]
        assert decoded.record is not None
        encoded = SerializeJsonRecord().execute(decoded.record)
        expected = vector["canonical_json"].encode()
        assert encoded.payload == expected, vector["vector_id"]
        assert hashlib.sha256(expected).hexdigest() == vector["canonical_sha256"]
        assert encoded.content_identity is not None
        assert encoded.content_identity.digest == vector["canonical_sha256"]


def test_artifact__schema_fixtures__agree_with_python_acceptance_partition() -> None:
    """Evidence ID
    SV-HARNESS-037
    Requirement
    All sixteen H3 valid record fixtures are schema-valid and Python-decodable,
    while every indexed schema-invalid fixture is rejected by both boundaries.
    Method
    Pair record schemas with same-stem valid and invalid fixtures, run Draft 2020-12
    validation, then invoke strict public decoding.
    Oracle
    The accepted H3 fixture index and record schemas define the independent
    acceptance partition.
    Acceptance
    Each valid fixture has no schema errors and decodes PASS; each invalid fixture
    has schema errors and decodes FAIL with no record.
    Interpretation
    Failure identifies schema/Python drift, a fixture defect, or a contract
    discrepancy rather than proving which artifact is wrong.
    Limitations
    Relational action behavior and scientific meaning are outside this exact
    schema/wire partition check.
    """
    stems = json.loads(
        (ROOT / "harness/pi/fixtures/fixture-index.json").read_text(encoding="utf-8")
    )["public_json_record_schemas"]
    schema_documents = [
        json.loads(path.read_text())
        for path in (ROOT / "harness/pi/schemas").rglob("*.schema.json")
    ]
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schema_documents
    )
    schemas = {
        path.stem.removesuffix(".schema"): json.loads(path.read_text())
        for path in (ROOT / "harness/pi/schemas/records").glob("*.schema.json")
    }
    for stem in stems:
        schema = schemas[stem]
        valid = json.loads(Path(f"harness/pi/fixtures/valid/{stem}.json").read_text())
        invalid_path = Path(f"harness/pi/fixtures/invalid/schema/{stem}.json")
        invalid = json.loads(invalid_path.read_text())
        validator = Draft202012Validator(schema, registry=registry)
        assert not list(validator.iter_errors(valid)), stem
        assert list(validator.iter_errors(invalid)), stem
        kind = WireRecordKind("".join(part.title() for part in stem.split("-")))
        assert (
            DeserializeJsonRecord()
            .execute(kind, Path(f"harness/pi/fixtures/valid/{stem}.json").read_bytes())
            .validation.status
            == "PASS"
        )
        rejected = DeserializeJsonRecord().execute(kind, invalid_path.read_bytes())
        assert rejected.validation.status == "FAIL"
        assert rejected.record is None


def test_artifact__diagnostic_path_corpus__matches_python_construction() -> None:
    """Evidence ID
    SV-HARNESS-038
    Requirement
    The complete accepted H3 DiagnosticPath valid/invalid corpus agrees with Python
    ValidationIssue construction without normalization.
    Method
    Construct the public issue from each indexed lexical spelling, including the
    escaped surrogate case, and observe exact retention or ValueError code text.
    Oracle
    H3's accepted DiagnosticPath oracle index fixes every spelling and expected
    issue code independently of production implementation.
    Acceptance
    All four valid cases retain their exact path or None; all nineteen invalid cases
    raise ValueError containing the indexed code.
    Interpretation
    Failure identifies lexical-contract drift in source or accepted H3 evidence.
    Limitations
    DiagnosticPath is lexical only; this test makes no filesystem existence,
    resource-kind, or Rust-runtime claim.
    """
    from ksdft2effmass.harness.pi import ValidationIssue

    corpus = json.loads(
        (ROOT / "harness/pi/fixtures/diagnostic-path/oracle-index.json").read_text()
    )
    for case in corpus["valid"]:
        issue = ValidationIssue(
            1, "PIH.PATH.MISSING", "ERROR", None, case["path"], (), "x"
        )
        assert issue.path == case["path"]
    for case in corpus["invalid"]:
        path = case.get("path")
        if path is None:
            path = case["path_escaped"].encode().decode("unicode_escape")
        with pytest.raises(ValueError, match=case["expected"].replace(".", r"\.")):
            ValidationIssue(1, "PIH.PATH.MISSING", "ERROR", None, path, (), "x")


def _decode_case_record(kind: WireRecordKind, value: object) -> object:
    """Evidence ID
    Supports SV-HARNESS-046 and SV-HARNESS-047; owns no separate identifier.
    Requirement
    Case records must be constructed only through the public wire boundary.
    Method
    Encode H3 JSON data and call the selected public decoder.
    Oracle
    The H3 case document fixes the supplied represented value.
    Acceptance
    Decoding passes and returns a complete record.
    Interpretation
    Failure indicates fixture, contract, or decoder disagreement.
    Limitations
    This helper makes no independent evidence claim.
    """
    payload = (json.dumps(value, ensure_ascii=False) + "\n").encode()
    result = DeserializeJsonRecord().execute(kind, payload)
    assert result.validation.status == "PASS"
    assert result.record is not None
    return result.record


def test_artifact__resource_resolution_corpus__matches_structured_actions(
    tmp_path: Path,
) -> None:
    """Evidence ID
    SV-HARNESS-046
    Requirement
    Every H3 resource-resolution and overlay case has its declared action result.
    Method
    Copy the H3 roots, apply declared symlinks, decode records publicly, and run
    manifest validation or resource resolution with explicit roots.
    Oracle
    The accepted H3 oracle index fixes all 19 acceptance partitions and codes.
    Acceptance
    Status and sole expected code match; PASS selects the declared layer/path;
    FAIL returns no partial path or reference.
    Interpretation
    Failure indicates action, fixture, setup, or accepted-contract disagreement.
    Limitations
    The disposable filesystem checks software confinement, not provenance.
    """
    import shutil
    from collections import Counter

    from ksdft2effmass.harness.pi import (
        ProjectProfile,
        ResolveResource,
        ResourceManifest,
        SerializeJsonRecord,
        ValidateResourceManifest,
    )

    base = ROOT / "harness/pi/fixtures/resource-resolution"
    index = json.loads((base / "oracle-index.json").read_text())
    assert len(index["cases"]) == 19
    for oracle in index["cases"]:
        case = json.loads((base / "cases" / f"{oracle['case_id']}.json").read_text())
        work = tmp_path / oracle["case_id"]
        shutil.copytree(base / "roots", work)
        setup = case.get("temporary_tree_setup", {})
        for operation in setup.get("operations", []):
            link = work / operation["path"]
            link.symlink_to(
                operation["target"],
                target_is_directory=operation["target_is_directory"],
            )
        generic = _decode_case_record(
            WireRecordKind.ResourceManifest, case["generic_manifest"]
        )
        profile = _decode_case_record(WireRecordKind.ProjectProfile, case["profile"])
        assert isinstance(generic, ResourceManifest)
        assert isinstance(profile, ProjectProfile)
        generic_serialized = SerializeJsonRecord().execute(generic)
        generic_identity = generic_serialized.content_identity
        assert generic_identity is not None
        local_data = case["local_manifest"]
        local = (
            _decode_case_record(WireRecordKind.ResourceManifest, local_data)
            if local_data is not None
            else None
        )
        assert local is None or isinstance(local, ResourceManifest)
        local_serialized = (
            SerializeJsonRecord().execute(local) if local is not None else None
        )
        local_identity = (
            local_serialized.content_identity if local_serialized is not None else None
        )
        expected = oracle["expected"]
        if case["resource_id"] is None:
            candidates = [(generic, generic_serialized)]
            if local is not None:
                assert local_serialized is not None
                candidates.append((local, local_serialized))
            for candidate, serialized in candidates:
                assert serialized.validation.status == "PASS"
                assert serialized.payload is not None
                round_trip = DeserializeJsonRecord().execute(
                    WireRecordKind.ResourceManifest, serialized.payload
                )
                assert round_trip.validation.status == "PASS"
                assert round_trip.record == candidate
                assert isinstance(round_trip.record, ResourceManifest)
                assert Counter(
                    (resource.resource_id, str(resource.path))
                    for resource in round_trip.record.resources
                ) == Counter(
                    (resource.resource_id, str(resource.path))
                    for resource in candidate.resources
                )
                assert Counter(
                    (resource.resource_id, dependency_id)
                    for resource in round_trip.record.resources
                    for dependency_id in resource.dependency_ids
                ) == Counter(
                    (resource.resource_id, dependency_id)
                    for resource in candidate.resources
                    for dependency_id in resource.dependency_ids
                )
            validation = ValidateResourceManifest().execute(
                generic,
                generic_identity,
                local,
                local_identity,
                profile,
            )
            assert validation.status == expected["status"], oracle["case_id"]
            assert expected["issue_code"] in {issue.code for issue in validation.issues}
            continue
        result = ResolveResource().execute(
            case["resource_id"],
            work / case["generic_root"].removeprefix("roots/"),
            generic,
            generic_identity,
            (
                work / case["local_root"].removeprefix("roots/")
                if case["local_root"] is not None
                else None
            ),
            local,
            local_identity,
            profile,
        )
        assert result.validation.status == expected["status"], oracle["case_id"]
        assert [issue.code for issue in result.validation.issues] == (
            [] if expected["issue_code"] is None else [expected["issue_code"]]
        )
        if expected["status"] == "FAIL":
            assert result.resolved_path is None
            assert result.reference is None
        else:
            assert result.resolved_path is not None
            assert result.reference is not None
            assert (
                result.resolved_path.relative_to(work)
                .as_posix()
                .endswith(oracle["selected_relative_path"])
            )


def test_artifact__semantic_invariant_corpus__matches_wire_partition() -> None:
    """Evidence ID
    SV-HARNESS-047
    Requirement
    All H3 semantic-invariant cases honor the declared schema/wire boundary.
    Method
    Consume every indexed case and invoke public decoding where H3 requires it.
    Oracle
    The accepted seven-case H3 index fixes schema and semantic expectations.
    Acceptance
    Schema-rejected cases are not decoded; each decoded semantic case returns its
    exact declared status/code partition and record presence.
    Interpretation
    Failure identifies H3/schema/decoder contract drift.
    Limitations
    Relational manifest acceptance is owned by the resource-resolution evidence.
    """
    base = ROOT / "harness/pi/fixtures/semantic-invariants"
    index = json.loads((base / "oracle-index.json").read_text())
    assert len(index["cases"]) == 7
    seen = set()
    for case in index["cases"]:
        seen.add(case["case_id"])
        payload = (base / case["instance_path"]).read_bytes()
        expectation = case["semantic_validator_expectation"]
        if expectation["stage"] == "not_run":
            continue
        result = DeserializeJsonRecord().execute(
            WireRecordKind(case["record_kind"]), payload
        )
        assert result.validation.status == expectation["status"]
        if expectation["status"] == "PASS":
            assert result.record is not None
            assert result.validation.issues == ()
        else:
            assert result.record is None
            assert [issue.code for issue in result.validation.issues] == [
                expectation["issue_code"]
            ]
    assert len(seen) == 7
