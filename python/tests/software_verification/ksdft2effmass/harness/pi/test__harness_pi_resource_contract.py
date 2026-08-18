r"""Software verification of harness pi resource contract.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of schema, fixture, and canonical-byte agreement; no physical
model, mathematical operator, or numerical representation is represented.

Intrinsic and cross-object scope

The primary owner is the maintained resource-contract artifact. Retained schemas,
fixtures, and canonical vectors are read-only independent oracles for the public Python
wire actions.

VVUQ and scientific exclusions

Passing establishes only exact textual software agreement. Numerical verification,
scientific validation, uncertainty quantification, physical correctness, and completed
Rust conformance are excluded.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from referencing import Registry, Resource

from ksdft2effmass.harness.pi import (
    JsonRecordDeserializer,
    JsonRecordSerializer,
    WireRecordKind,
)

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification


def test_artifact__canonical_vectors__agree_with_exact_python_bytes() -> None:
    """Evidence ID: SV-HARNESS-036

    Requirement: Every retained canonical vector decodes and re-encodes to its exact
    RFC
    8785-plus-LF bytes and SHA-256 identity.

    Method: Consume all indexed vectors, caller-select each public record kind, decode,
    encode, and hash using the public actions.

    Oracle: The retained canonical-json-vectors file independently fixes record kinds,
    byte
    strings, and digests.

    Acceptance: All sixteen payloads produce PASS, byte-for-byte equality, and the
    exact
    indexed lowercase SHA-256 digest.

    Interpretation: Failure identifies a Python codec, retained vector, accepted
    contract, or environment discrepancy for independent review.

    Limitations: This is textual software verification only; it does not establish Rust
    conformance, numerical correctness, scientific validation, or UQ.
    """
    index_path = ROOT / "harness/pi/fixtures/canonical/canonical-json-vectors.json"
    vectors = json.loads(index_path.read_text(encoding="utf-8"))["vectors"]
    assert len(vectors) == 16

    def exercise_vector_case_63_8(vector: Any) -> Any:
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
        decoded = JsonRecordDeserializer().execute(
            WireRecordKind(vector["record_kind"]), payload
        )
        assert decoded.validation.status == "PASS", vector["vector_id"]
        assert decoded.record is not None
        encoded = JsonRecordSerializer().execute(decoded.record)
        expected = vector["canonical_json"].encode()
        assert encoded.payload == expected, vector["vector_id"]
        assert hashlib.sha256(expected).hexdigest() == vector["canonical_sha256"]
        assert encoded.content_identity is not None
        assert encoded.content_identity.digest == vector["canonical_sha256"]

    _ = [exercise_vector_case_63_8(vector) for vector in (vectors)]


def test_artifact__schema_fixtures__agree_with_python_acceptance_partition() -> None:
    """Evidence ID: SV-HARNESS-037

    Requirement: All sixteen retained valid record fixtures are schema-valid and
    Python-decodable,
    while every indexed schema-invalid fixture is rejected by both boundaries.

    Method: Pair record schemas with same-stem valid and invalid fixtures, run Draft
    2020-12
    validation, then invoke strict public decoding.

    Oracle: The retained fixture index and record schemas define the independent
    acceptance partition.

    Acceptance: Each valid fixture has no schema errors and decodes PASS; each invalid
    fixture
    has schema errors and decodes FAIL with no record.

    Interpretation: Failure identifies schema/Python drift, a fixture defect, or a
    contract
    discrepancy rather than proving which artifact is wrong.

    Limitations: Relational action behavior and scientific meaning are outside this
    exact
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
        for path in (ROOT / "harness/pi/schemas").rglob("*.schema.json")
    }

    def exercise_stem_case_123_7(stem: Any) -> Any:
        schema = schemas[stem]
        valid_path = ROOT / f"harness/pi/fixtures/valid/{stem}.json"
        invalid_path = ROOT / f"harness/pi/fixtures/invalid/schema/{stem}.json"
        valid = json.loads(valid_path.read_text())
        invalid = json.loads(invalid_path.read_text())
        validator = Draft202012Validator(schema, registry=registry)
        assert not list(validator.iter_errors(valid)), stem
        assert list(validator.iter_errors(invalid)), stem
        kind = WireRecordKind("".join(part.title() for part in stem.split("-")))
        assert (
            JsonRecordDeserializer()
            .execute(kind, valid_path.read_bytes())
            .validation.status
            == "PASS"
        )
        rejected = JsonRecordDeserializer().execute(kind, invalid_path.read_bytes())
        assert rejected.validation.status == "FAIL"
        assert rejected.record is None

    _ = [exercise_stem_case_123_7(stem) for stem in (stems)]


def test_artifact__diagnostic_path_corpus__matches_python_construction() -> None:
    """Evidence ID: SV-HARNESS-038

    Requirement: The complete retained DiagnosticPath valid/invalid corpus agrees
    with Python
    ValidationIssue construction without normalization.

    Method: Construct the public issue from each indexed lexical spelling, including the
    escaped surrogate case, and observe exact retention or ValueError code text.

    Oracle: The retained DiagnosticPath oracle index fixes every spelling and expected
    issue code independently of production implementation.

    Acceptance: All four valid cases retain their exact path or None; all nineteen
    invalid cases
    raise ValueError containing the indexed code.

    Interpretation: Failure identifies lexical-contract drift in source or retained
    evidence.

    Limitations: DiagnosticPath is lexical only; this test makes no filesystem
    existence,
    resource-kind, or Rust-runtime claim.
    """
    from ksdft2effmass.harness.pi import ValidationIssue

    corpus = json.loads(
        (ROOT / "harness/pi/fixtures/diagnostic-path/oracle-index.json").read_text()
    )

    def exercise_case_case_169_6(case: Any) -> Any:
        issue = ValidationIssue(
            1, "PIH.PATH.MISSING", "ERROR", None, case["path"], (), "x"
        )
        assert issue.path == case["path"]

    _ = [exercise_case_case_169_6(case) for case in (corpus["valid"])]

    def exercise_case_case_174_5(case: Any) -> Any:
        path = case.get("path")
        if path is None:
            path = case["path_escaped"].encode().decode("unicode_escape")
        with pytest.raises(ValueError, match=case["expected"].replace(".", "\\.")):
            ValidationIssue(1, "PIH.PATH.MISSING", "ERROR", None, path, (), "x")

    _ = [exercise_case_case_174_5(case) for case in (corpus["invalid"])]


def decode_public_case_record(kind: WireRecordKind, value: object) -> object:
    """Evidence ID: Owns no identifier; supports SV-HARNESS-036.

    Requirement: Case records must be constructed only through the public wire boundary.

    Method: Encode retained JSON data and call the selected public decoder.

    Oracle: The retained case document fixes the supplied represented value.

    Acceptance: Decoding passes and returns a complete record.

    Interpretation: Failure indicates fixture, contract, or decoder disagreement.

    Limitations: This helper makes no independent evidence claim.
    """
    payload = (json.dumps(value, ensure_ascii=False) + "\n").encode()
    result = JsonRecordDeserializer().execute(kind, payload)
    assert result.validation.status == "PASS"
    assert result.record is not None
    return result.record


def test_artifact__resource_resolution_corpus__matches_structured_actions(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-046

    Requirement: Every retained resource-resolution and overlay case has its declared
    Action result.

    Method: Copy the retained fixture roots, apply declared symlinks, decode records
    publicly, and run manifest validation or resource resolution with explicit roots.

    Oracle: The retained oracle index fixes all 19 acceptance partitions and codes.

    Acceptance: Status and sole expected code match; PASS selects the declared
    layer/path;
    FAIL returns no partial path or reference.

    Interpretation: Failure indicates action, fixture, setup, or accepted-contract
    disagreement.

    Limitations: The disposable filesystem checks software confinement, not provenance.
    """
    import shutil
    from collections import Counter

    from ksdft2effmass.harness.pi import (
        JsonRecordSerializer,
        ProjectProfile,
        ResourceManifest,
        ResourceManifestValidator,
        ResourceResolver,
    )

    base = ROOT / "harness/pi/fixtures/resource-resolution"
    index = json.loads((base / "oracle-index.json").read_text())
    assert len(index["cases"]) == 19

    def exercise_oracle_case_239_4(oracle: Any) -> Any:
        case = json.loads((base / "cases" / f"{oracle['case_id']}.json").read_text())
        work = tmp_path / oracle["case_id"]
        shutil.copytree(base / "roots", work)
        setup = case.get("temporary_tree_setup", {})

        def exercise_operation_case_244_3(operation: Any) -> Any:
            link = work / operation["path"]
            link.symlink_to(
                operation["target"],
                target_is_directory=operation["target_is_directory"],
            )

        _ = [
            exercise_operation_case_244_3(operation)
            for operation in setup.get("operations", [])
        ]
        generic = decode_public_case_record(
            WireRecordKind.ResourceManifest, case["generic_manifest"]
        )
        profile = decode_public_case_record(
            WireRecordKind.ProjectProfile, case["profile"]
        )
        assert isinstance(generic, ResourceManifest)
        assert isinstance(profile, ProjectProfile)
        generic_serialized = JsonRecordSerializer().execute(generic)
        generic_identity = generic_serialized.content_identity
        assert generic_identity is not None
        local_data = case["local_manifest"]
        local = (
            decode_public_case_record(WireRecordKind.ResourceManifest, local_data)
            if local_data is not None
            else None
        )
        assert local is None or isinstance(local, ResourceManifest)
        local_serialized = (
            JsonRecordSerializer().execute(local) if local is not None else None
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

            def exercise_candidate_and_serialized_case_278_2(
                candidate: Any, serialized: Any
            ) -> Any:
                assert serialized.validation.status == "PASS"
                assert serialized.payload is not None
                round_trip = JsonRecordDeserializer().execute(
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

            _ = [
                exercise_candidate_and_serialized_case_278_2(candidate, serialized)
                for candidate, serialized in candidates
            ]
            validation = ResourceManifestValidator().execute(
                generic, generic_identity, local, local_identity, profile
            )
            assert validation.status == expected["status"], oracle["case_id"]
            assert expected["issue_code"] in {issue.code for issue in validation.issues}
            return
        result = ResourceResolver().execute(
            case["resource_id"],
            work / case["generic_root"].removeprefix("roots/"),
            generic,
            generic_identity,
            work / case["local_root"].removeprefix("roots/")
            if case["local_root"] is not None
            else None,
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

    _ = [exercise_oracle_case_239_4(oracle) for oracle in (index["cases"])]


def test_artifact__semantic_invariant_corpus__matches_wire_partition() -> None:
    """Evidence ID: SV-HARNESS-047

    Requirement: All retained semantic-invariant cases honor the declared schema/wire
    boundary.

    Method: Consume every indexed case and invoke public decoding where the retained
    oracle requires it.

    Oracle: The retained seven-case index fixes schema and semantic expectations.

    Acceptance: Schema-rejected cases are not decoded; each decoded semantic case
    returns its
    exact declared status/code partition and record presence.

    Interpretation: Failure identifies retained-schema/decoder contract drift.

    Limitations: Relational manifest acceptance is owned by the resource-resolution
    evidence.
    """
    base = ROOT / "harness/pi/fixtures/semantic-invariants"
    index = json.loads((base / "oracle-index.json").read_text())
    assert len(index["cases"]) == 7
    seen = set()

    def exercise_case_case_365_1(case: Any) -> Any:
        seen.add(case["case_id"])
        payload = (base / case["instance_path"]).read_bytes()
        expectation = case["semantic_validator_expectation"]
        if expectation["stage"] == "not_run":
            return
        result = JsonRecordDeserializer().execute(
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

    _ = [exercise_case_case_365_1(case) for case in (index["cases"])]
    assert len(seen) == 7


def test_artifact__manifest_coverage__matches_explicit_textual_resource_roots() -> None:
    """Evidence ID: SV-HARNESS-172

    Requirement: Generic and local manifests exactly cover their declared textual
    resource families, select one local profile, and contain valid UTF-8 resources.

    Method: Compare manifest paths with the bounded declarative roots and decode each
    selected resource without invoking repository discovery.

    Oracle: The maintained resource layout fixes generic schemas/skills and local
    extensions/profiles/projections/schemas/validation as the complete families.

    Acceptance: Declared and bounded path sets are equal, one profile is selected, and
    every selected resource is a nonsymlink regular UTF-8 file.

    Interpretation: Failure identifies manifest coverage, stale registration, path-kind,
    or textual encoding drift.

    Limitations: This establishes bounded textual resource coverage only; runtime Action
    behavior, authorization, scientific validity, and UQ are excluded.
    """
    roots = (
        (
            ROOT / "harness/pi",
            ("evidence", "schemas", "skills"),
        ),
        (
            ROOT / "harness/local",
            (
                "extensions",
                "fixtures/oracle-index.json",
                "fixtures/task-record-v3",
                "fixtures/task-selection-v1",
                "profiles",
                "projections",
                "schemas",
                "validation",
            ),
        ),
    )
    manifests = tuple(
        (root, json.loads((root / "resource-manifest.json").read_text()), families)
        for root, families in roots
    )
    declared_sets = tuple(
        {item["path"] for item in manifest["resources"]} for _, manifest, _ in manifests
    )
    actual_sets = tuple(
        {
            path.relative_to(root).as_posix()
            for family in families
            for path in (
                (root / family,)
                if (root / family).is_file()
                else (root / family).rglob("*")
            )
            if path.is_file() and "__pycache__" not in path.parts
        }
        for root, _, families in manifests
    )
    assert declared_sets == actual_sets
    selected_paths = tuple(
        root / relative
        for (root, _, _), declared in zip(manifests, declared_sets, strict=True)
        for relative in declared
    )
    assert all(path.is_file() and not path.is_symlink() for path in selected_paths)
    assert all(path.read_text(encoding="utf-8") is not None for path in selected_paths)
    local = manifests[1][1]
    assert sum(item["path"].startswith("profiles/") for item in local["resources"]) == 1


def test_artifact__resource_documentation__retains_current_contract_concepts() -> None:
    """Evidence ID: SV-HARNESS-173

    Requirement: Maintained generic/local resource and skill documentation retains its
    current contract concepts without relying on phase completion prose.

    Method: Read the three maintained documentation surfaces and the test-evidence
    convention reference, then compare required concept phrases.

    Oracle: Current resource ownership, path, claim-boundary, and maintained
    test-evidence contracts fix the required concepts independently of the retired
    validator.

    Acceptance: Every required concept is present and both superseded evidence headings
    remain expressly prohibited by the maintained reference.

    Interpretation: Failure identifies maintained documentation or skill-reference
    drift.

    Limitations: Concept presence does not establish prose quality, Action correctness,
    authorization, scientific validation, or UQ.
    """
    requirements = {
        ROOT / "harness/pi/docs/resources.md": (
            "root explicitly",
            "extend",
            "symlink",
            "SHA-256",
            "DiagnosticPath",
            "human acceptance",
        ),
        ROOT / "harness/pi/docs/evidence-grammar.md": (
            "class_owned",
            "artifact_owned",
            "software verification",
            "numerical verification",
            "scientific validation",
            "uncertainty quantification",
        ),
        ROOT / "harness/local/docs/project-profile.md": (
            "explicit",
            "extend_only",
            "namespace",
            "marker",
            "compatibility",
            "local",
        ),
    }
    texts = {path: path.read_text(encoding="utf-8").casefold() for path in requirements}
    assert all(
        concept.casefold() in texts[path]
        for path, concepts in requirements.items()
        for concept in concepts
    )
    conventions = (
        ROOT
        / "harness/pi/skills/develop-python-test-evidence/references"
        / "test-evidence-conventions.md"
    ).read_text(encoding="utf-8")
    assert all(
        heading in conventions
        for heading in (
            "Facet and represented meaning",
            "Intrinsic and cross-object scope",
            "VVUQ and scientific exclusions",
        )
    )
    assert "superseded and prohibited" in conventions
    assert "Evidence class and represented meaning" in conventions
    assert "Owned contract, oracle, and scope" in conventions
