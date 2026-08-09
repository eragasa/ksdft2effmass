r"""Software verification of ``VerificationObservation``.

Facet and represented meaning

-----------------------------
This class-owned evidence verifies exact capability-observation fields,
intrinsic identifiers, exact enum typing, canonical evidence tuples, frozen
state, equality, and lifecycle separation.

Intrinsic and cross-object scope

--------------------------------
The sole SUT is ``VerificationObservation``; ``VerificationStatus`` is a typed
constructor input, not a co-owner. Public fields, literal grammars, tuple
relations, and frozen-dataclass semantics provide exact oracles. No I/O or
warnings are expected.

VVUQ and scientific exclusions

------------------------------
Passing establishes only immutable metadata behavior for an already-observed
capability verification. VERIFIED does not imply execution, convergence,
numerical acceptance, physical correctness, scientific validation, UQ,
portability, or cross-language agreement.
"""

from dataclasses import FrozenInstanceError, astuple, fields
from typing import Any

import pytest

from ksdft2effmass.provenance import VerificationObservation, VerificationStatus

SUT = VerificationObservation
pytestmark = pytest.mark.software_verification

FROZEN_FIELDS = (
    "verification_id",
    "installation_id",
    "capability_id",
    "status",
    "evidence_artifact_ids",
    "provenance_id",
)
EQUALITY_FIELDS = (
    "verification_id",
    "installation_id",
    "capability_id",
    "status",
    "evidence_artifact_ids",
    "provenance_id",
)

IDENTIFIER_FIELDS = (
    "verification_id",
    "installation_id",
    "capability_id",
    "provenance_id",
)
PUBLIC_FIELDS = (
    "verification_id",
    "installation_id",
    "capability_id",
    "status",
    "evidence_artifact_ids",
    "provenance_id",
)


def make_verification_observation(**overrides: Any) -> VerificationObservation:
    """Evidence ID: Owns no identifier; supports VerificationObservation evidence in
    this module.

    Requirement: Tests need explicit valid synthetic baseline state with one-field
    overrides.

    Method: Build all six public constructor arguments and replace only named overrides.

    Oracle: Literal identifiers, enum member, and sorted tuple satisfy accepted
    invariants.

    Acceptance: Return direct SUT construction; perform no assertion, I/O, or
    normalization.

    Interpretation: Helper failure indicates invalid setup or constructor drift, not
    evidence.

    Limitations: The helper permits deliberately invalid typed overrides for rejection
    tests.
    """
    values: dict[str, Any] = {
        "verification_id": "verify-1",
        "installation_id": "install-1",
        "capability_id": "cap-1",
        "status": VerificationStatus.VERIFIED,
        "evidence_artifact_ids": ("evidence-1", "evidence-2"),
        "provenance_id": "prov-1",
    }
    values.update(overrides)
    return SUT(**values)


def test_constructor__field_mapping__stores_exact_values_order_and_builtin_types() -> (
    None
):
    """Evidence ID: SV-PROV-034

    Requirement: Construction stores six public fields unchanged in declared order and
    exact types.

    Method: Construct complete synthetic verification metadata and inspect public state.

    Oracle: The accepted field sequence and fixed literals define exact values and
    types.

    Acceptance: Names and values match; status is exact enum and evidence is exact
    built-in tuple.

    Interpretation: Failure identifies mapping, ordering, coercion, setup, or contract
    drift.

    Limitations: Stored metadata does not establish execution or scientific correctness.
    """
    record = make_verification_observation()
    assert tuple(field.name for field in fields(record)) == PUBLIC_FIELDS
    assert astuple(record) == (
        "verify-1",
        "install-1",
        "cap-1",
        VerificationStatus.VERIFIED,
        ("evidence-1", "evidence-2"),
        "prov-1",
    )
    assert (
        type(record.verification_id),
        type(record.installation_id),
        type(record.capability_id),
        type(record.status),
        type(record.evidence_artifact_ids),
        type(record.provenance_id),
    ) == (str, str, str, VerificationStatus, tuple, str)


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param(
            "verification_id", "alpha-1", id="verification_id_ordinary_identifier"
        ),
        pytest.param(
            "installation_id", "alpha-1", id="installation_id_ordinary_identifier"
        ),
        pytest.param(
            "capability_id", "alpha-1", id="capability_id_ordinary_identifier"
        ),
        pytest.param(
            "provenance_id", "alpha-1", id="provenance_id_ordinary_identifier"
        ),
        pytest.param("verification_id", "A", id="verification_id_minimum_length_1"),
        pytest.param("installation_id", "A", id="installation_id_minimum_length_1"),
        pytest.param("capability_id", "A", id="capability_id_minimum_length_1"),
        pytest.param("provenance_id", "A", id="provenance_id_minimum_length_1"),
        pytest.param(
            "verification_id", "A" * 128, id="verification_id_maximum_length_128"
        ),
        pytest.param(
            "installation_id", "A" * 128, id="installation_id_maximum_length_128"
        ),
        pytest.param("capability_id", "A" * 128, id="capability_id_maximum_length_128"),
        pytest.param("provenance_id", "A" * 128, id="provenance_id_maximum_length_128"),
    ],
)
def test_constructor__identifier_boundaries__accept_valid_partition(
    field_name: str, value: str
) -> None:
    """Evidence ID: SV-PROV-261

    Requirement: Every identifier field accepts ordinary, length-one, and length-128
    text.

    Method: Override one named field with one explicit valid lexical-length partition.

    Oracle: The grammar permits an alphanumeric lead and 127 permitted continuations.

    Acceptance: Construction stores the selected built-in string exactly without
    coercion.

    Interpretation: Failure identifies field-specific rejection, boundary, setup, or
    grammar drift.

    Limitations: Synthetic ASCII identifiers do not establish external referential
    integrity.
    """
    record = make_verification_observation(**{field_name: value})
    assert getattr(record, field_name) == value
    assert type(getattr(record, field_name)) is str


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("verification_id", id="verification_id_bytes_wrong_type"),
        pytest.param("installation_id", id="installation_id_bytes_wrong_type"),
        pytest.param("capability_id", id="capability_id_bytes_wrong_type"),
        pytest.param("provenance_id", id="provenance_id_bytes_wrong_type"),
    ],
)
def test_constructor__identifier_type__rejects_wrong_semantic_type(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-213

    Requirement: Every identifier requires exact built-in str and performs no coercion.

    Method: Supply bytes to one named identifier with every other field valid.

    Oracle: Bytes is distinct from the accepted built-in string semantic type.

    Acceptance: Every field partition raises exactly TypeError.

    Interpretation: Failure identifies coercion, field-coverage, validation-order, or
    contract drift.

    Limitations: Identifier value grammar is tested separately.
    """
    with pytest.raises(TypeError):
        make_verification_observation(**{field_name: b"identifier"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("verification_id", id="verification_id_empty_identifier"),
        pytest.param("installation_id", id="installation_id_empty_identifier"),
        pytest.param("capability_id", id="capability_id_empty_identifier"),
        pytest.param("provenance_id", id="provenance_id_empty_identifier"),
    ],
)
def test_constructor__identifier_nonempty__rejects_empty_text(field_name: str) -> None:
    """Evidence ID: SV-PROV-262

    Requirement: Every identifier field rejects empty built-in string text.

    Method: Supply empty text to one named field with otherwise valid state.

    Oracle: The accepted identifier length is inclusively 1 through 128.

    Acceptance: Every field partition raises exactly ValueError.

    Interpretation: Failure identifies missing nonempty enforcement or field-coverage
    drift.

    Limitations: Wrong types and nonempty malformed text are separate partitions.
    """
    with pytest.raises(ValueError):
        make_verification_observation(**{field_name: ""})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("verification_id", id="verification_id_embedded_space"),
        pytest.param("installation_id", id="installation_id_embedded_space"),
        pytest.param("capability_id", id="capability_id_embedded_space"),
        pytest.param("provenance_id", id="provenance_id_embedded_space"),
    ],
)
def test_constructor__identifier_grammar__rejects_embedded_space(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-263

    Requirement: Every identifier field rejects an embedded ASCII space.

    Method: Supply ``bad id`` to one named field with otherwise valid state.

    Oracle: Space is absent from the portable continuation character set.

    Acceptance: Every field partition raises exactly ValueError.

    Interpretation: Failure identifies grammar widening, field coverage, setup, or
    contract drift.

    Limitations: Leading-character, Unicode, and length partitions are separate.
    """
    with pytest.raises(ValueError):
        make_verification_observation(**{field_name: "bad id"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("verification_id", id="verification_id_invalid_leading_hyphen"),
        pytest.param("installation_id", id="installation_id_invalid_leading_hyphen"),
        pytest.param("capability_id", id="capability_id_invalid_leading_hyphen"),
        pytest.param("provenance_id", id="provenance_id_invalid_leading_hyphen"),
    ],
)
def test_constructor__identifier_leading_character__rejects_non_alphanumeric(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-264

    Requirement: Every identifier must begin with an ASCII alphanumeric character.

    Method: Supply a leading-hyphen identifier to one named field.

    Oracle: Hyphen is permitted only after the first grammar position.

    Acceptance: Every field partition raises exactly ValueError.

    Interpretation: Failure identifies leading-character or field-specific enforcement
    drift.

    Limitations: This does not enumerate every excluded leading character.
    """
    with pytest.raises(ValueError):
        make_verification_observation(**{field_name: "-identifier"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("verification_id", id="verification_id_unicode_surrogate"),
        pytest.param("installation_id", id="installation_id_unicode_surrogate"),
        pytest.param("capability_id", id="capability_id_unicode_surrogate"),
        pytest.param("provenance_id", id="provenance_id_unicode_surrogate"),
    ],
)
def test_constructor__identifier_unicode__rejects_surrogate(field_name: str) -> None:
    """Evidence ID: SV-PROV-265

    Requirement: Every identifier field rejects Unicode surrogate code points.

    Method: Supply a string containing U+D800 to one named field.

    Oracle: The public Unicode invariant explicitly excludes the surrogate range.

    Acceptance: Every field partition raises exactly ValueError.

    Interpretation: Failure identifies unsafe Unicode admission or validation-order
    drift.

    Limitations: NFC and portable ASCII grammar are separate requirements.
    """
    with pytest.raises(ValueError):
        make_verification_observation(**{field_name: "A\ud800"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("verification_id", id="verification_id_decomposed_non_nfc"),
        pytest.param("installation_id", id="installation_id_decomposed_non_nfc"),
        pytest.param("capability_id", id="capability_id_decomposed_non_nfc"),
        pytest.param("provenance_id", id="provenance_id_decomposed_non_nfc"),
    ],
)
def test_constructor__identifier_unicode__rejects_non_nfc(field_name: str) -> None:
    """Evidence ID: SV-PROV-266

    Requirement: Every identifier field rejects non-NFC text.

    Method: Supply decomposed ``A`` plus combining ring to one named field.

    Oracle: Unicode NFC normalization changes the supplied string.

    Acceptance: Every field partition raises exactly ValueError at the NFC boundary.

    Interpretation: Failure identifies normalization enforcement, ordering, or
    field-coverage drift.

    Limitations: The input would also fail the later portable ASCII grammar.
    """
    with pytest.raises(ValueError):
        make_verification_observation(**{field_name: "A\u030a"})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("verification_id", id="verification_id_overlength_129"),
        pytest.param("installation_id", id="installation_id_overlength_129"),
        pytest.param("capability_id", id="capability_id_overlength_129"),
        pytest.param("provenance_id", id="provenance_id_overlength_129"),
    ],
)
def test_constructor__identifier_length__rejects_129_characters(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-267

    Requirement: Every identifier field rejects length 129 above the inclusive maximum
    128.

    Method: Supply 129 otherwise valid ASCII identifier characters to one named field.

    Oracle: The accepted portable grammar permits at most 128 characters.

    Acceptance: Every field partition raises exactly ValueError.

    Interpretation: Failure identifies an off-by-one bound, field coverage, or contract
    drift.

    Limitations: This lexical bound does not establish external-system compatibility.
    """
    with pytest.raises(ValueError):
        make_verification_observation(**{field_name: "A" * 129})


@pytest.mark.parametrize(
    "status",
    [
        pytest.param(VerificationStatus.VERIFIED, id="status_verified_member"),
        pytest.param(VerificationStatus.REJECTED, id="status_rejected_member"),
        pytest.param(VerificationStatus.UNAVAILABLE, id="status_unavailable_member"),
    ],
)
def test_constructor__status_members__accepts_exact_enum(
    status: VerificationStatus,
) -> None:
    """Evidence ID: SV-PROV-268

    Requirement: Status accepts each of the three exact VerificationStatus members.

    Method: Construct one explicit enum-member partition with otherwise valid state.

    Oracle: The accepted status domain is the complete three-member public enum.

    Acceptance: Construction preserves exact enum identity and type without coercion.

    Interpretation: Failure identifies member rejection, coercion, setup, or contract
    drift.

    Limitations: Enum meaning does not establish tool execution or scientific
    correctness.
    """
    record = make_verification_observation(status=status)
    assert record.status is status
    assert type(record.status) is VerificationStatus


@pytest.mark.parametrize(
    "status",
    [
        pytest.param("verified", id="status_verified_wire_string_lookalike"),
        pytest.param("rejected", id="status_rejected_wire_string_lookalike"),
        pytest.param("unavailable", id="status_unavailable_wire_string_lookalike"),
    ],
)
def test_constructor__status_type__rejects_each_wire_string_lookalike(
    status: str,
) -> None:
    """Evidence ID: SV-PROV-212

    Requirement: Status rejects every raw wire-string lookalike instead of coercing it.

    Method: Supply one of the three enum values as a built-in string.

    Oracle: The accepted semantic type is VerificationStatus, not its str base value.

    Acceptance: Every lookalike partition raises exactly TypeError.

    Interpretation: Failure identifies implicit enum coercion or type-contract drift.

    Limitations: Enum value construction is owned by VerificationStatus evidence.
    """
    with pytest.raises(TypeError):
        make_verification_observation(status=status)


def test_constructor__status_type__rejects_unrelated_integer() -> None:
    """Evidence ID: SV-PROV-269

    Requirement: Status rejects a non-enum, non-string semantic type.

    Method: Supply integer one through the deliberate invalid constructor boundary.

    Oracle: Integer is not an instance of VerificationStatus.

    Acceptance: Construction raises exactly TypeError.

    Interpretation: Failure identifies accidental broad type admission or contract
    drift.

    Limitations: Other arbitrary object types are not exhaustively sampled.
    """
    with pytest.raises(TypeError):
        make_verification_observation(status=1)


@pytest.mark.parametrize(
    "evidence_ids",
    [
        pytest.param((), id="evidence_artifact_ids_empty_tuple"),
        pytest.param(("evidence-1",), id="evidence_artifact_ids_singleton_tuple"),
        pytest.param(
            ("evidence-1", "evidence-2"),
            id="evidence_artifact_ids_sorted_pair",
        ),
    ],
)
def test_constructor__evidence_artifact_ids_valid_states__preserves_tuple(
    evidence_ids: tuple[str, ...],
) -> None:
    """Evidence ID: SV-PROV-035

    Requirement: Artifact references accept empty, singleton, and unique lexically
    sorted tuples.

    Method: Construct one explicit canonical-cardinality partition.

    Oracle: The accepted tuple relation directly identifies these three valid states.

    Acceptance: Construction preserves exact tuple value and built-in tuple type.

    Interpretation: Failure identifies cardinality, ordering, uniqueness, or storage
    drift.

    Limitations: Artifact existence and contents are not opened or validated.
    """
    record = make_verification_observation(evidence_artifact_ids=evidence_ids)
    assert record.evidence_artifact_ids == evidence_ids
    assert type(record.evidence_artifact_ids) is tuple


def test_constructor__evidence_artifact_ids_container__rejects_list() -> None:
    """Evidence ID: SV-PROV-211

    Requirement: Evidence artifact IDs require exact built-in tuple container type.

    Method: Supply a list containing one otherwise valid identifier.

    Oracle: List is distinct from the accepted built-in immutable tuple.

    Acceptance: Construction raises exactly TypeError before member validation.

    Interpretation: Failure identifies container coercion or type-contract drift.

    Limitations: Tuple member and tuple relation invariants are tested separately.
    """
    with pytest.raises(TypeError):
        make_verification_observation(evidence_artifact_ids=["evidence-1"])


def test_constructor__evidence_artifact_ids_member_type__rejects_integer() -> None:
    """Evidence ID: SV-PROV-270

    Requirement: Every evidence tuple member requires exact built-in str.

    Method: Supply a built-in tuple containing integer one.

    Oracle: Integer is distinct from the accepted member semantic type.

    Acceptance: Construction raises exactly TypeError.

    Interpretation: Failure identifies member coercion or type-contract drift.

    Limitations: Invalid string values and tuple relations are separate requirements.
    """
    with pytest.raises(TypeError):
        make_verification_observation(evidence_artifact_ids=(1,))


def test_constructor__evidence_artifact_ids_member_nonempty__rejects_empty() -> None:
    """Evidence ID: SV-PROV-271

    Requirement: Every evidence tuple member must be nonempty.

    Method: Supply a singleton tuple containing empty built-in string text.

    Oracle: The accepted identifier length is inclusively 1 through 128.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies missing member nonempty enforcement or contract
    drift.

    Limitations: Other member grammar partitions are tested separately.
    """
    with pytest.raises(ValueError):
        make_verification_observation(evidence_artifact_ids=("",))


def test_constructor__evidence_artifact_ids_member_grammar__rejects_space() -> None:
    """Evidence ID: SV-PROV-272

    Requirement: Every evidence tuple member must satisfy portable identifier grammar.

    Method: Supply a singleton tuple containing ``bad id``.

    Oracle: Embedded space is absent from the accepted character set.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies member grammar widening or contract drift.

    Limitations: Leading-character, Unicode, and length partitions are separate.
    """
    with pytest.raises(ValueError):
        make_verification_observation(evidence_artifact_ids=("bad id",))


def test_constructor__evidence_artifact_ids_member_leading__rejects_hyphen() -> None:
    """Evidence ID: SV-PROV-273

    Requirement: Every evidence tuple member begins with an ASCII alphanumeric
    character.

    Method: Supply a singleton tuple containing a leading-hyphen identifier.

    Oracle: Hyphen is permitted only after the first identifier position.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies leading-character grammar widening or contract
    drift.

    Limitations: Other invalid leading characters are not exhaustively sampled.
    """
    with pytest.raises(ValueError):
        make_verification_observation(evidence_artifact_ids=("-evidence",))


def test_constructor__evidence_artifact_ids_member_unicode__rejects_surrogate() -> None:
    """Evidence ID: SV-PROV-274

    Requirement: Every evidence tuple member rejects Unicode surrogate code points.

    Method: Supply a singleton tuple containing U+D800.

    Oracle: The public Unicode invariant explicitly excludes the surrogate range.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies unsafe Unicode admission or validation-order
    drift.

    Limitations: NFC and portable ASCII grammar are separate requirements.
    """
    with pytest.raises(ValueError):
        make_verification_observation(evidence_artifact_ids=("A\ud800",))


def test_constructor__evidence_artifact_ids_member_unicode__rejects_non_nfc() -> None:
    """Evidence ID: SV-PROV-275

    Requirement: Every evidence tuple member rejects non-NFC text.

    Method: Supply decomposed ``A`` plus combining ring in a singleton tuple.

    Oracle: Unicode NFC normalization changes the supplied string.

    Acceptance: Construction raises exactly ValueError at the NFC boundary.

    Interpretation: Failure identifies missing member normalization enforcement or
    ordering drift.

    Limitations: The input would also fail the later portable ASCII grammar.
    """
    with pytest.raises(ValueError):
        make_verification_observation(evidence_artifact_ids=("A\u030a",))


def test_constructor__evidence_artifact_ids_member_length__rejects_129() -> None:
    """Evidence ID: SV-PROV-276

    Requirement: Every evidence tuple member rejects length 129 above maximum 128.

    Method: Supply a singleton tuple containing 129 valid ASCII characters.

    Oracle: The accepted identifier grammar permits at most 128 characters.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies an off-by-one member bound or contract drift.

    Limitations: This lexical limit does not establish artifact-store compatibility.
    """
    with pytest.raises(ValueError):
        make_verification_observation(evidence_artifact_ids=("A" * 129,))


def test_constructor__evidence_artifact_ids_ordering__rejects_reverse_order() -> None:
    """Evidence ID: SV-PROV-277

    Requirement: Multiple evidence identifiers must be in ascending lexical order.

    Method: Supply two valid unique identifiers in reverse lexical order.

    Oracle: Python string ordering places ``evidence-1`` before ``evidence-2``.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies missing canonical-order enforcement or contract
    drift.

    Limitations: Member validity and duplicate rejection are tested separately.
    """
    with pytest.raises(ValueError):
        make_verification_observation(
            evidence_artifact_ids=("evidence-2", "evidence-1")
        )


def test_constructor__evidence_artifact_ids_uniqueness__rejects_duplicate() -> None:
    """Evidence ID: SV-PROV-278

    Requirement: Evidence identifier tuples must contain unique members.

    Method: Supply two identical valid identifiers in lexical order.

    Oracle: A repeated literal yields tuple cardinality two but set cardinality one.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Failure identifies missing duplicate enforcement or contract drift.

    Limitations: Ordering and member validity are tested separately.
    """
    with pytest.raises(ValueError):
        make_verification_observation(
            evidence_artifact_ids=("evidence-1", "evidence-1")
        )


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("verification_id", id="verification_id_frozen_reassignment"),
        pytest.param("installation_id", id="installation_id_frozen_reassignment"),
        pytest.param("capability_id", id="capability_id_frozen_reassignment"),
        pytest.param("status", id="status_frozen_reassignment"),
        pytest.param(
            "evidence_artifact_ids", id="evidence_artifact_ids_frozen_reassignment"
        ),
        pytest.param("provenance_id", id="provenance_id_frozen_reassignment"),
    ],
)
def test_field__frozen_reassignment__rejects_every_public_field(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-215

    Requirement: Every public verification field is frozen after construction.

    Method: Reassign one semantically identified public field on a valid record.

    Oracle: The accepted frozen-dataclass contract forbids all field reassignment.

    Acceptance: Every field partition raises exactly FrozenInstanceError.

    Interpretation: Failure identifies mutable public state or incorrect field
    inventory.

    Limitations: This tests reassignment, not mutation of unrelated external artifacts.
    """
    record = make_verification_observation()
    with pytest.raises(FrozenInstanceError):
        setattr(record, field_name, getattr(record, field_name))


@pytest.mark.parametrize(
    ("field_name", "changed_value"),
    [
        pytest.param("verification_id", "verify-2", id="verification_id_different"),
        pytest.param("installation_id", "install-2", id="installation_id_different"),
        pytest.param("capability_id", "cap-2", id="capability_id_different"),
        pytest.param(
            "status", VerificationStatus.REJECTED, id="status_verified_to_rejected"
        ),
        pytest.param(
            "evidence_artifact_ids",
            ("evidence-1",),
            id="evidence_artifact_ids_different_tuple",
        ),
        pytest.param("provenance_id", "prov-2", id="provenance_id_different"),
    ],
)
def test_method__eq__distinguishes_each_public_field(
    field_name: str, changed_value: object
) -> None:
    """Evidence ID: SV-PROV-216

    Requirement: Equality compares every public field in complete represented state.

    Method: Compare a baseline with an identical record and one named one-field change.

    Oracle: Frozen dataclass equality is exact complete represented-state equality.

    Acceptance: Identical state is equal and every one-field change is unequal.

    Interpretation: Failure identifies omitted equality state, bad setup, or contract
    drift.

    Limitations: Equality does not establish referential integrity or scientific
    equivalence.
    """
    baseline = make_verification_observation()
    assert baseline == make_verification_observation()
    assert baseline != make_verification_observation(**{field_name: changed_value})


@pytest.mark.parametrize(
    ("left", "right"),
    [
        pytest.param(
            VerificationStatus.VERIFIED,
            VerificationStatus.REJECTED,
            id="status_verified_vs_rejected",
        ),
        pytest.param(
            VerificationStatus.VERIFIED,
            VerificationStatus.UNAVAILABLE,
            id="status_verified_vs_unavailable",
        ),
        pytest.param(
            VerificationStatus.REJECTED,
            VerificationStatus.UNAVAILABLE,
            id="status_rejected_vs_unavailable",
        ),
    ],
)
def test_method__eq__distinguishes_all_status_members(
    left: VerificationStatus, right: VerificationStatus
) -> None:
    """Evidence ID: SV-PROV-279

    Requirement: Each distinct status member produces a distinct verification state.

    Method: Compare records differing only by one of the three unordered status pairs.

    Oracle: The public enum members are distinct and status participates in equality.

    Acceptance: Every status pair compares unequal in both operand directions.

    Interpretation: Failure identifies collapsed status equality or setup drift.

    Limitations: Status distinction does not imply execution or scientific correctness.
    """
    left_record = make_verification_observation(status=left)
    right_record = make_verification_observation(status=right)
    assert left_record != right_record
    assert right_record != left_record


@pytest.mark.parametrize(
    ("left", "right"),
    [
        pytest.param(
            (), ("evidence-1",), id="evidence_artifact_ids_empty_vs_singleton"
        ),
        pytest.param(
            ("evidence-1",),
            ("evidence-1", "evidence-2"),
            id="evidence_artifact_ids_singleton_vs_sorted_pair",
        ),
    ],
)
def test_method__eq__distinguishes_evidence_tuples(
    left: tuple[str, ...], right: tuple[str, ...]
) -> None:
    """Evidence ID: SV-PROV-280

    Requirement: Distinct valid evidence tuples produce distinct verification states.

    Method: Compare records differing only in explicit valid tuple cardinality
    partitions.

    Oracle: Exact tuple value participates in frozen dataclass equality.

    Acceptance: Each pair compares unequal in both operand directions.

    Interpretation: Failure identifies omitted evidence state or setup drift.

    Limitations: Artifact contents and semantic equivalence are not assessed.
    """
    left_record = make_verification_observation(evidence_artifact_ids=left)
    right_record = make_verification_observation(evidence_artifact_ids=right)
    assert left_record != right_record
    assert right_record != left_record


def test_method__eq__returns_unequal_for_unrelated_object() -> None:
    """Evidence ID: SV-PROV-281

    Requirement: VerificationObservation is unequal to an unrelated object.

    Method: Compare a valid record with a plain object through public equality.

    Oracle: Dataclass equality returns NotImplemented for another class, yielding false.

    Acceptance: The equality expression is exactly false.

    Interpretation: Failure identifies unexpected cross-type equality or contract drift.

    Limitations: Equality against subclasses or proxies is not covered.
    """
    assert not (make_verification_observation() == object())


def test_field__lifecycle_boundary__excludes_later_execution_and_science_state() -> (
    None
):
    """Evidence ID: SV-PROV-214

    Requirement: Capability verification metadata is distinct from later lifecycle
    decisions.

    Method: Compare the exact public inventory with explicit fields for installation
    declaration, execution authorization/completion, parsing, convergence,
    numerical acceptance, scientific validation, and UQ.

    Oracle: The accepted lifecycle assigns none of those states to this observation
    record.

    Acceptance: The public field set is disjoint from every later or separate lifecycle
    field.

    Interpretation: Failure identifies lifecycle ownership leakage or field-inventory
    drift.

    Limitations: Field absence does not verify the separate lifecycle objects or
    actions.
    """
    assert set(PUBLIC_FIELDS).isdisjoint(
        {
            "installation_declaration",
            "execution_authorization",
            "execution_completion",
            "parsed_result",
            "converged",
            "numerically_accepted",
            "scientifically_validated",
            "uncertainty_quantification",
        }
    )
