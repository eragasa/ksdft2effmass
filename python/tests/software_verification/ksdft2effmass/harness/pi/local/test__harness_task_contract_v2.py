r"""Software verification of HarnessTask version-2 cross-surface contract.

Facet and represented meaning

The module verifies cross-interface JSON, schema, resource, rendering, comparison,
packet, compatibility, and public-export agreement for the accepted local Task model.

Intrinsic and cross-object scope

The evidence owns the cohesive version-2 contract artifact rather than any second
public class. Class-owned modules separately establish all 21 public identities.

VVUQ and scientific exclusions

Passing establishes only documented software-contract behavior using synthetic data.
It does not migrate a Task, activate work, validate science, or provide human
acceptance.
"""

import base64
import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any, cast

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

import ksdft2effmass.harness.pi.local as local_api
from ksdft2effmass.harness.pi import (
    HumanReviewDecision,
    TaskStateInspectionRequest,
    TaskStateInspector,
)
from ksdft2effmass.harness.pi.local import (
    HarnessTaskDeserializer,
    HarnessTaskDocumentation,
    HarnessTaskDocumentationComparator,
    HarnessTaskDocumentationContent,
    HarnessTaskDocumentationRenderer,
    HarnessTaskGraphValidator,
    HarnessTaskMigrationDisposition,
    HarnessTaskMigrationFileDispositionRecorder,
    HarnessTaskMigrationReviewPacketPreparer,
    HarnessTaskProjectionProfile,
    HarnessTaskSerializer,
    TaskRecordAdapter,
)

from .conftest import repository_root
from .task_model_examples import identity, make_request, make_task

pytestmark = pytest.mark.software_verification

_PUBLIC_NAMES = (
    "HarnessTask",
    "HarnessTaskSerializer",
    "HarnessTaskDeserializer",
    "HarnessTaskGraphValidator",
    "HarnessTaskDocumentSource",
    "HarnessTaskSourceDisposition",
    "HarnessTaskSourceMapping",
    "HarnessTaskDocumentationContent",
    "HarnessTaskProjectionProfile",
    "HarnessTaskDocumentation",
    "HarnessTaskDocumentationRenderer",
    "HarnessTaskDocumentationComparator",
    "HarnessTaskDocumentationComparisonResult",
    "HarnessTaskMigrationReviewPacketRequest",
    "HarnessTaskMigrationReviewPacketPreparer",
    "HarnessTaskMigrationReviewPacket",
    "HarnessTaskMigrationReviewDocument",
    "HarnessTaskMigrationReviewPacketRenderer",
    "HarnessTaskMigrationDisposition",
    "HarnessTaskMigrationFileDisposition",
    "HarnessTaskMigrationFileDispositionRecorder",
)


def test_public_api__corrected_table__exports_exact_twenty_one_interfaces() -> None:
    """Evidence ID: ``SV-HT-020``.

    Requirement: The local public surface exposes the accepted 19 HarnessTask
    interfaces plus the two explicitly corrected human-review rendering interfaces.

    Method: Resolve the frozen names through the maintained public module and compare
    them with the task-model module's public class definitions.

    Oracle: The accepted Stage-1 table and bounded Stage-2A rendering correction supply
    the exact ordered names.

    Acceptance: All 21 names resolve to classes and no additional public class is
    defined by ``task_model``.

    Interpretation: Failure identifies missing, renamed, or accidental public API.

    Limitations: Existing unrelated local exports are intentionally outside this check.
    """
    assert len(_PUBLIC_NAMES) == 21
    assert all(isinstance(getattr(local_api, name), type) for name in _PUBLIC_NAMES)
    task_model = __import__(
        "ksdft2effmass.harness.pi.local.task_model", fromlist=["unused"]
    )
    defined = {
        name
        for name, value in vars(task_model).items()
        if isinstance(value, type)
        and value.__module__ == task_model.__name__
        and not name.startswith("_")
    }
    assert defined == set(_PUBLIC_NAMES)
    assert (
        task_model.HarnessTaskDocumentationComparisonResult.__annotations__["status"]
        == "Identifier"
    )


def test_artifact__canonical_json__matches_hand_authored_wire_rules() -> None:
    """Evidence ID: ``SV-HT-021``.

    Requirement: Version-2 canonical JSON has the exact 16 keys, UTF-8 representation,
    two-space indentation, array conversion, and one final LF.

    Method: Serialize a Task, parse it independently with ``json``, and deserialize it.

    Oracle: The frozen field table and Python JSON formatting rules are exact.

    Acceptance: Key order equals dataclass order, Unicode is literal, tuples are arrays,
    bytes have one final LF, and the Task round-trips exactly.

    Interpretation: Failure identifies wire-format or round-trip drift.

    Limitations: JSON Schema agreement is tested separately.
    """
    task = make_task(title="Unicode café")
    payload = HarnessTaskSerializer().execute(task)
    decoded = json.loads(payload)
    assert list(decoded) == list(task.__dataclass_fields__)
    assert b"caf\xc3\xa9" in payload
    assert type(decoded["authorized_scope"]) is list
    assert payload.endswith(b"\n") and not payload.endswith(b"\n\n")
    assert HarnessTaskDeserializer().execute(payload) == task


def fixture_matches_expectation(
    root: Path,
    validator: Draft202012Validator,
    relative: str,
    layer: str,
) -> bool:
    """Evidence ID: Owns no identifier; supports SV-HT-022.

    Requirement: Fixture-family evidence needs one explicit per-file oracle.

    Method: Apply schema validation and, for runtime cases, strict deserialization.

    Oracle: The declared layer selects the expected isolated failure boundary.

    Acceptance: Return true exactly when the fixture behaves as declared.

    Interpretation: False identifies schema/runtime fixture disagreement.

    Limitations: This helper owns no independent evidence claim.
    """
    payload = (root / relative).read_bytes()
    schema_errors = list(validator.iter_errors(json.loads(payload)))
    if layer == "valid":
        return not schema_errors and (
            HarnessTaskSerializer().execute(HarnessTaskDeserializer().execute(payload))
            == payload
        )
    if layer == "schema":
        return bool(schema_errors)
    if schema_errors:
        return False
    try:
        HarnessTaskDeserializer().execute(payload)
    except TypeError, ValueError:
        return True
    return False


def test_artifact__fixture_family__is_complete_and_isolated() -> None:
    """Evidence ID: ``SV-HT-022``.

    Requirement: Every indexed valid fixture passes schema and runtime construction;
    every invalid fixture fails at its declared schema or runtime layer.

    Method: Load the explicit fixture index, apply Draft 2020-12 validation, then invoke
    the deserializer where the declared layer is runtime.

    Oracle: The index is a hand-maintained partition and each invalid file contains one
    named isolated defect.

    Acceptance: All discovered files are indexed and every partition has the expected
    pass/fail outcome.

    Interpretation: Failure identifies schema/runtime drift or orphaned fixtures.

    Limitations: JSON Schema cannot express Unicode NFC normalization; that case is
    intentionally runtime-owned.
    """
    root = repository_root() / "harness/local/fixtures/task-record-v2"
    index = json.loads((root / "fixture-index.json").read_text())
    schema = json.loads(
        (
            repository_root() / "harness/local/schemas/task-record-v2.schema.json"
        ).read_text()
    )
    validator = Draft202012Validator(schema)
    indexed = set(index["valid"]) | set(index["invalid"])
    discovered = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*.json")
        if path.name != "fixture-index.json"
    }
    assert indexed == discovered
    assert all(
        fixture_matches_expectation(root, validator, relative, "valid")
        for relative in index["valid"]
    )
    assert all(
        fixture_matches_expectation(root, validator, relative, expectation["layer"])
        for relative, expectation in index["invalid"].items()
    )


@pytest.mark.parametrize(
    "field,value",
    (
        pytest.param("task_id", "a/b", id="identifier_slash_rejected"),
        pytest.param(
            "status", "active:", id="identifier_trailing_punctuation_rejected"
        ),
        pytest.param("documentation_path", "CON.txt", id="device_name_rejected"),
        pytest.param("intake_path", "C:/input.md", id="drive_prefix_rejected"),
        pytest.param(
            "documentation_path", "docs/a\u2028b.md", id="line_separator_rejected"
        ),
        pytest.param("documentation_path", "docs/cafe\u0301.md", id="non_nfc_rejected"),
    ),
)
def test_constructor__lexical_rejections__match_identifier_and_resource_path(
    field: str, value: str
) -> None:
    """Evidence ID: ``SV-HT-023``.

    Requirement: Runtime uses the frozen local Identifier grammar and the accepted
    reusable ResourcePath rejection contract.

    Method: Replace one otherwise valid field with one semantic invalid partition.

    Oracle: The accepted regex and generic ResourcePath algorithm define exact rejects.

    Acceptance: Every invalid Identifier or ResourcePath raises ``ValueError``.

    Interpretation: Failure identifies runtime/schema lexical disagreement.

    Limitations: Type errors are exercised by class-owned constructor evidence.
    """
    with pytest.raises(ValueError):
        make_task(**{field: value})


def test_method__multi_defect_precedence__is_code_path_detail_lexical() -> None:
    """Evidence ID: ``SV-HT-024``.

    Requirement: Graph diagnostics use exact PIHL.TASK codes and deterministic
    ``(code, path, detail)`` precedence.

    Method: Supply a parent cycle, a missing prerequisite, and duplicate paths.

    Oracle: The Stage-2 hardening rule fixes lexical code/path/detail ordering.

    Acceptance: Returned issues equal the exact expected ordered tuples.

    Interpretation: Failure identifies code vocabulary or precedence drift.

    Limitations: Status lifecycle meaning is intentionally opaque.
    """
    first = make_task(
        task_id="a", parent_task_id="b", intake_path="same", documentation_path="same"
    )
    second = make_task(
        task_id="b",
        parent_task_id="a",
        task_prerequisite_ids=("missing",),
        intake_path="same",
        documentation_path="same",
    )
    issues = HarnessTaskGraphValidator().execute((first, second)).issues
    assert tuple((item.code, item.path, item.detail) for item in issues) == (
        ("PIHL.TASK.DOCUMENTATION_PATH_DUPLICATE", "same", "a,b"),
        ("PIHL.TASK.INTAKE_PATH_DUPLICATE", "same", "a,b"),
        ("PIHL.TASK.PARENT_CYCLE", None, "a,b"),
        ("PIHL.TASK.PREREQUISITE_MISSING", "same", "missing"),
    )


@pytest.mark.parametrize(
    "invalid_template",
    (
        pytest.param(
            b"{{content.opaque}}{{content.opaque}}\n",
            id="duplicate_content_token_rejected",
        ),
        pytest.param(b"{{content.unknown}}\n", id="unknown_content_token_rejected"),
        pytest.param(b"{{unknown.token}}\n", id="unknown_token_kind_rejected"),
        pytest.param(b"{{content.opaque}}\n\n", id="final_lf_policy_rejected"),
    ),
)
def test_method__explicit_template__preserves_opaque_bytes_and_parses_once(
    invalid_template: bytes,
) -> None:
    """Evidence ID: ``SV-HT-025``.

    Requirement: Renderer parses only UTF-8 template bytes, substitutes each content
    token exactly once, and preserves opaque block bytes without reparsing.

    Method: Render a non-UTF-8 block containing token-like braces and test malformed,
    duplicate, and final-LF template partitions.

    Oracle: Literal expected bytes and token cardinality provide independent oracles.

    Acceptance: Opaque bytes are exact; invalid template partitions raise ValueError.

    Interpretation: Failure identifies template parsing or opaque preservation drift.

    Limitations: Rendered meaning still requires human review.
    """
    task = make_task()
    block = b"opaque \xff {{task.title}}"
    content = HarnessTaskDocumentationContent(
        identity(block), task.documentation_path, ("opaque",), (block,)
    )
    template = b"# {{task.title}}\n{{content.opaque}}\n"
    profile = HarnessTaskProjectionProfile(
        1, "profile", template, identity(template), True
    )
    rendered = HarnessTaskDocumentationRenderer().execute(task, content, profile)
    assert rendered.content == b"# Example Task\n" + block + b"\n"
    invalid_profile = HarnessTaskProjectionProfile(
        1,
        "invalid-profile",
        invalid_template,
        identity(invalid_template),
        True,
    )
    with pytest.raises(ValueError):
        HarnessTaskDocumentationRenderer().execute(task, content, invalid_profile)


def test_method__coverage_and_preservation__separates_mechanical_claims() -> None:
    """Evidence ID: ``SV-HT-026``.

    Requirement: Comparator reports exact bytes, mapped differences, source coverage
    gaps, and ordered documentation-block preservation without semantic claims.

    Method: Compare exact, inserted, and changed-documentation outputs against explicit
    half-open mappings.

    Oracle: Hand-calculated source ranges and literal bytes define expected statuses.

    Acceptance: Statuses are EXACT, MAPPED_DIFFERENCES, and UNMAPPED_DIFFERENCES with
    exact affected source range for the changed block.

    Interpretation: Failure identifies diff, coverage, or preservation drift.

    Limitations: A mapped result is not semantic correctness or human acceptance.
    """
    request = make_request()
    comparator = HarnessTaskDocumentationComparator()
    assert (
        comparator.execute(
            request.source, request.rendered_documentation, request.mappings
        ).status
        == "EXACT"
    )
    inserted_bytes = b"prefix" + request.rendered_documentation.content
    inserted = HarnessTaskDocumentation(
        request.rendered_documentation.path,
        inserted_bytes,
        identity(inserted_bytes),
    )
    assert comparator.execute(request.source, inserted, request.mappings).status == (
        "MAPPED_DIFFERENCES"
    )
    changed_bytes = b"changed\n"
    changed = HarnessTaskDocumentation(
        request.rendered_documentation.path, changed_bytes, identity(changed_bytes)
    )
    result = comparator.execute(request.source, changed, request.mappings)
    assert result.status == "UNMAPPED_DIFFERENCES"
    assert result.unmapped_spans == ((0, request.source.byte_count),)


def test_method__one_field_mutations__fail_closed_without_io() -> None:
    """Evidence ID: ``SV-HT-027``.

    Requirement: Packet preparation recomputes canonical JSON, rendering, comparison,
    mapping coverage, content blocks, and generic packet compatibility.

    Method: Prepare one valid request then mutate independent canonical and mapping
    fields.

    Oracle: Independently reconstructed ActionObject outputs define exact agreement.

    Acceptance: Valid input returns one equal packet; each mutation raises ValueError.

    Interpretation: Failure identifies permissive packet compatibility.

    Limitations: Preparation records no disposition and performs no migration.
    """
    request = make_request()
    preparer = HarnessTaskMigrationReviewPacketPreparer()
    assert preparer.execute(request).request == request
    with pytest.raises(ValueError, match="canonical_task_json"):
        preparer.execute(replace(request, canonical_task_json=b"{}\n"))
    duplicate = replace(request, mappings=request.mappings + request.mappings)
    with pytest.raises(ValueError, match="mapping IDs"):
        preparer.execute(duplicate)


@pytest.mark.parametrize(
    "generic,migration",
    (
        pytest.param("accepted", "ACCEPT_FILE_MIGRATION", id="accepted"),
        pytest.param(
            "bounded_correction", "REVISE_CONTRACT_OR_MAPPING", id="correction"
        ),
        pytest.param("rejected", "RETAIN_DOCUMENTATION_OWNERSHIP", id="retained"),
        pytest.param("deferred", "DEFER_FILE", id="deferred"),
    ),
)
def test_method__compatibility_table__maps_all_four_rows(
    generic: str, migration: str
) -> None:
    """Evidence ID: ``SV-HT-028``.

    Requirement: File disposition recording uses the frozen four-row mapping while the
    generic human decision remains authoritative.

    Method: Construct each explicit generic decision and corresponding migration enum.

    Oracle: The accepted compatibility table supplies all exact pairs.

    Acceptance: Each pair records successfully and retains the exact packet.

    Interpretation: Failure identifies disposition-table or packet-binding drift.

    Limitations: Synthetic decisions do not establish actual human authority.
    """
    packet = HarnessTaskMigrationReviewPacketPreparer().execute(make_request())
    scope = ("Revise mapping.",) if generic == "bounded_correction" else ()
    decision = HumanReviewDecision(
        packet.request.human_review_packet, "Synthetic response", generic, scope
    )
    result = HarnessTaskMigrationFileDispositionRecorder().execute(
        packet, decision, HarnessTaskMigrationDisposition(migration)
    )
    assert result.packet is packet


def test_artifact__profile_manifest__bind_sole_template_bytes() -> None:
    """Evidence ID: ``SV-HT-029``.

    Requirement: The project resource graph binds schema, fixtures, oracle index, and
    one base64 encoding of the profile's authoritative template bytes.

    Method: Decode profile bytes, recalculate SHA-256, and inspect explicit manifest
    dependency edges.

    Oracle: ``hashlib.sha256`` and the accepted resource relationship table are exact.

    Acceptance: Identity matches and required dependency edges are present.

    Interpretation: Failure identifies stale identity or resource-graph drift.

    Limitations: Resource agreement does not establish documentation meaning.
    """
    root = repository_root() / "harness/local"
    profile = json.loads(
        (root / "projections/harness-task-documentation-v2.json").read_text()
    )
    template = base64.b64decode(profile["template_bytes_base64"], validate=True)
    assert (
        hashlib.sha256(template).hexdigest() == profile["template_identity"]["digest"]
    )
    manifest = json.loads((root / "resource-manifest.json").read_text())
    resources = {item["resource_id"]: item for item in manifest["resources"]}
    assert resources["ksdft2effmass.local.harness-task-documentation.v2"][
        "dependency_ids"
    ] == ["ksdft2effmass.local.task-record.v2"]
    assert resources["ksdft2effmass.local.oracle-index.v1"]["dependency_ids"] == [
        "ksdft2effmass.local.task-record-v2.fixture-index"
    ]


def test_artifact__mixed_task_formats__adapt_in_one_explicit_chain() -> None:
    """Evidence ID: ``SV-HT-031``.

    Requirement: One explicit chain may select Markdown, version-1 JSON, and
    version-2 JSON Tasks without transferring Task authority into the chain.

    Method: Adapt three synthetic records together and then duplicate JSON-owned
    status into the version-2 chain entry.

    Oracle: Existing Markdown/v1 compatibility and the accepted v2 dispatch define
    exact identities, statuses, and failure on duplicated chain authority.

    Acceptance: The mixed chain returns three ordered references; duplicated v2
    status fails closed.

    Interpretation: Failure identifies mixed-format dispatch or authority drift.

    Limitations: Synthetic records do not migrate any maintained Task.
    """
    markdown_path = "records/markdown.md"
    v1_path = "records/version-one.json"
    v2_path = "records/version-two.json"
    markdown = (markdown_path, b"# Markdown Task\n\nStatus: completed\n")
    v1 = {
        "schema_version": 1,
        "task_id": "format.v1",
        "title": "Version one",
        "status": "completed",
        "parent_task_id": None,
        "task_prerequisite_ids": [],
        "external_prerequisite_ids": [],
        "explicit_activation_required": False,
        "objective": "Retain v1 compatibility.",
        "authority_reference_paths": ["records/decision.md"],
        "authorized_scope": ["Adapt synthetic data."],
        "completion_criteria": ["Reference is produced."],
        "exclusions": ["No migration."],
        "intake_path": "records/v1.intake.md",
    }
    v2 = make_task(task_id="format.v2", status="active")
    chain: dict[str, Any] = {
        "active_task": v2.task_id,
        "automatic_successor_activation": False,
        "explicitly_activated_task_ids": [v2.task_id],
        "task_sequence": [
            {
                "id": "format.markdown",
                "record": markdown_path,
                "status": "completed",
                "prerequisites": [],
            },
            {"id": "format.v1", "record": v1_path},
            {"id": v2.task_id, "record": v2_path},
        ],
    }
    documents = (
        markdown,
        (v1_path, json.dumps(v1).encode()),
        (v2_path, HarnessTaskSerializer().execute(v2)),
    )
    adapted = TaskRecordAdapter().execute(documents, json.dumps(chain).encode(), b"{}")
    assert adapted.validation.status == "PASS"
    assert tuple(item.task_id for item in cast(Any, adapted.value)) == (
        "format.markdown",
        "format.v1",
        "format.v2",
    )
    chain["task_sequence"][2]["status"] = "active"
    duplicated = TaskRecordAdapter().execute(
        documents, json.dumps(chain).encode(), b"{}"
    )
    assert duplicated.validation.status == "FAIL"
    assert "duplicated" in duplicated.validation.issues[0].detail


@pytest.mark.parametrize(
    "record_kind",
    (
        pytest.param("markdown", id="markdown_record_selected"),
        pytest.param("v1", id="version_one_json_selected"),
        pytest.param("v2", id="version_two_json_selected"),
    ),
)
def test_method__task_state_inspector__preserves_format_selection(
    tmp_path: Path, record_kind: str
) -> None:
    """Evidence ID: ``SV-HT-032``.

    Requirement: TaskStateInspector reads only the chain-selected Markdown, v1 JSON,
    or v2 JSON record and preserves its established status precedence.

    Method: Build one bounded temporary chain per format, inspect it, and introduce a
    v2 identity mismatch.

    Oracle: The generic inspector contract uses chain status for Markdown and exact
    selected JSON identity/status for both JSON versions.

    Acceptance: Every format passes with the expected status and selected path; the v2
    identity mismatch reports REFERENCE_INVALID.

    Interpretation: Failure identifies selected-path or mixed-format inspection drift.

    Limitations: Complete local schema validation remains owned by TaskRecordAdapter.
    """
    task_id = "format.task"
    suffix = "md" if record_kind == "markdown" else "json"
    record_path = f"records/{record_kind}.{suffix}"
    chain_path = "records/chain.json"
    chain = {
        "active_task": None,
        "task_sequence": [
            {
                "id": task_id,
                "record": record_path,
                "status": "chain_status",
                "prerequisites": [],
            }
        ],
    }
    (tmp_path / "records").mkdir()
    (tmp_path / chain_path).write_text(json.dumps(chain))
    if record_kind == "markdown":
        (tmp_path / record_path).write_text("# Task\n\nStatus: ignored prose\n")
        expected_status = "chain_status"
    elif record_kind == "v1":
        (tmp_path / record_path).write_text(
            json.dumps({"task_id": task_id, "status": "v1_status"})
        )
        expected_status = "v1_status"
    else:
        v2 = make_task(task_id=task_id, status="v2_status")
        (tmp_path / record_path).write_bytes(HarnessTaskSerializer().execute(v2))
        expected_status = "v2_status"
    request = TaskStateInspectionRequest(1, tmp_path, chain_path, task_id)
    result = TaskStateInspector().execute(request)
    assert result.validation.status == "PASS"
    assert result.task_status == expected_status
    assert result.task_record_path == record_path
    if record_kind == "v2":
        mismatch = make_task(task_id="different.task", status="v2_status")
        (tmp_path / record_path).write_bytes(HarnessTaskSerializer().execute(mismatch))
        failed = TaskStateInspector().execute(request)
        assert failed.validation.status == "FAIL"
        assert failed.validation.issues[0].code == "PIH.TASK_STATE.REFERENCE_INVALID"


def test_method__version_two_json__preserves_reference_projection() -> None:
    """Evidence ID: ``SV-HT-030``.

    Requirement: ``TaskRecordAdapter`` accepts version-2 JSON while preserving its
    established TaskReference projection and explicit chain agreement.

    Method: Supply canonical v2 Task bytes plus a minimal explicit synthetic chain and
    activation record.

    Oracle: The Task's five projected fields and existing adapter result contract are
    exact.

    Acceptance: Adaptation passes and returns the expected TaskReference values.

    Interpretation: Failure identifies v1/v2 compatibility dispatch drift.

    Limitations: Existing Markdown compatibility remains covered by predecessor tests.
    """
    task = make_task(status="active")
    path = "records/example.task.json"
    chain = {
        "active_task": task.task_id,
        "automatic_successor_activation": False,
        "explicitly_activated_task_ids": [task.task_id],
        "task_sequence": [{"id": task.task_id, "record": path}],
    }
    activation: dict[str, object] = {}
    result = TaskRecordAdapter().execute(
        ((path, HarnessTaskSerializer().execute(task)),),
        json.dumps(chain).encode(),
        json.dumps(activation).encode(),
    )
    assert result.validation.status == "PASS"
    reference = cast(Any, result.value)[0]
    assert (
        reference.task_id,
        reference.task_prerequisite_ids,
        reference.external_prerequisite_ids,
        reference.status,
        reference.explicit_activation_required,
    ) == (task.task_id, (), (), task.status, True)
