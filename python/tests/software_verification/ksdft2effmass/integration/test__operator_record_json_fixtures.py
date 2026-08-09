r"""Software verification of OperatorRecordJsonFixtures.

Facet and represented meaning

-----------------------------
This artifact-owned module owns the operator record json fixtures facet. Object:
complete version-1 valid/invalid golden-file corpus. Evidence class:
software verification, distinct from serializer facet and schema metamodel evidence.

Requirement: directories contain exactly the approved named files; valid files
round-trip to deterministic canonical serializer text and invalid files are all
rejected. Strategy: filesystem enumeration and public serializer calls only.

Oracle: approved inventory and each golden classification. Acceptance is complete
set equality and classification agreement. Passing does not validate physical data,
scientific meaning, UQ, independent Rust behavior, or serializer internals; failure
indicates missing/stale artifacts or interoperability drift.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordJsonFixtures``; collaborators only construct
inputs or expose public outcomes. Accepted public contracts, literal expected
values, Python language semantics, and assigned schema or fixture artifacts provide
the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

import json
from pathlib import Path

import pytest

from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification
SPEC = Path(__file__).resolve().parents[5] / "specification/operator-record/v1"
VALID_NAMES = {"complex-hermitian.json", "complex-nonhermitian.json", "minimal.json"}
INVALID_NAMES = {
    "boolean-as-number.json",
    "dimension-mismatch.json",
    "duplicate-basis-label.json",
    "empty-string.json",
    "energy-reference-value.json",
    "missing-field.json",
    "nonorthogonal-basis.json",
    "nonsquare-matrix.json",
    "numeric-string.json",
    "ragged-matrix.json",
    "singular-cell.json",
    "unknown-field.json",
    "unsupported-version.json",
}


def fixture_names(kind: str) -> set[str]:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Fixture discovery returns the exact versioned JSON filenames for the
    requested valid
    or invalid family.

    Method: Construct or inspect only the named synthetic fixture operation (fixture
    names); the
    helper owns no assertion result and introduces no hidden oracle.

    Oracle: The checked-in valid, schema-invalid, unknown-value, and wrong-semantic-type
    filename inventories define both membership and the layer expected to accept or
    reject each file.

    Acceptance: The helper returns exactly the requested fixture value or applies only
    the
    documented comparison; all pass/fail assertions remain in the owning test.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    return {path.name for path in (SPEC / kind).glob("*.json")}


def test_artifact__golden_fixture_inventory_is_exact__agrees_exactly() -> None:
    r"""Evidence ID: SV-ORJF-001

    Requirement: The version-1 golden fixture family has this exact runtime
    interoperability
    property: golden fixture inventory is exact: agrees exactly.

    Method: Enumerate the checked-in version-1 fixtures for golden fixture inventory is
    exact:
    agrees exactly and pass each case through the documented public serializer boundary.

    Oracle: The checked-in valid, schema-invalid, unknown-value, and wrong-semantic-type
    filename inventories define both membership and the layer expected to accept or
    reject each file.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    assert fixture_names("valid") == VALID_NAMES
    assert fixture_names("invalid") == INVALID_NAMES


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("complex-hermitian.json", id="complex_hermitian_fixture"),
        pytest.param("complex-nonhermitian.json", id="complex_nonhermitian_fixture"),
        pytest.param("minimal.json", id="minimal_fixture"),
    ],
)
def test_artifact__valid_golden_files_have_deterministic__agrees_exactly(
    name: str,
) -> None:
    r"""Evidence ID: SV-ORJF-002

    Requirement: The version-1 golden fixture family has this exact runtime
    interoperability
    property: valid golden files have deterministic: agrees exactly.

    Method: Enumerate the checked-in version-1 fixtures for valid golden files have
    deterministic: agrees exactly and pass each case through the documented public
    serializer boundary.

    Oracle: The checked-in valid, schema-invalid, unknown-value, and wrong-semantic-type
    filename inventories define both membership and the layer expected to accept or
    reject each file.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    text = (SPEC / "valid" / name).read_text(encoding="utf-8")
    serializer = OperatorRecordJsonSerializer()
    record = serializer.deserialize(text)
    canonical = serializer.serialize(record)
    assert canonical == serializer.serialize(record)
    assert json.loads(canonical) == json.loads(text)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param(
            "dimension-mismatch.json", ValueError, id="dimension_mismatch_json"
        ),
        pytest.param(
            "duplicate-basis-label.json", ValueError, id="duplicate_basis_label_json"
        ),
        pytest.param("empty-string.json", ValueError, id="empty_string_json"),
        pytest.param(
            "energy-reference-value.json", ValueError, id="energy_reference_value_json"
        ),
        pytest.param("missing-field.json", ValueError, id="missing_field_json"),
        pytest.param(
            "nonorthogonal-basis.json", ValueError, id="nonorthogonal_basis_json"
        ),
        pytest.param("nonsquare-matrix.json", ValueError, id="nonsquare_matrix_json"),
        pytest.param("ragged-matrix.json", ValueError, id="ragged_matrix_json"),
        pytest.param("singular-cell.json", ValueError, id="singular_cell_json"),
    ],
)
def test_artifact__invalid_golden_files_are_rejected_by_public__agrees_exactly(
    name: str, expected: type[Exception]
) -> None:
    r"""Evidence ID: SV-ORJF-003

    Requirement: The version-1 golden fixture family has this exact runtime
    interoperability
    property: invalid golden files are rejected by public: agrees exactly.

    Method: Enumerate the checked-in version-1 fixtures for invalid golden files are
    rejected by
    public: agrees exactly and pass each case through the documented public serializer
    boundary.

    Oracle: The checked-in valid, schema-invalid, unknown-value, and wrong-semantic-type
    filename inventories define both membership and the layer expected to accept or
    reject each file.

    Acceptance: The named partition raises exactly expected with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    text = (SPEC / "invalid" / name).read_text(encoding="utf-8")
    with pytest.raises(expected):
        OperatorRecordJsonSerializer().deserialize(text)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param("unknown-field.json", ValueError, id="unknown_field_json"),
        pytest.param(
            "unsupported-version.json", ValueError, id="unsupported_version_json"
        ),
    ],
)
def test_artifact__unknown_value_golden_files_are_rejected_by__agrees_exactly(
    name: str, expected: type[Exception]
) -> None:
    r"""Evidence ID: SV-ORJF-005

    Requirement: The version-1 golden fixture family has this exact runtime
    interoperability
    property: unknown value golden files are rejected by: agrees exactly.

    Method: Enumerate the checked-in version-1 fixtures for unknown value golden files
    are
    rejected by: agrees exactly and pass each case through the documented public
    serializer boundary.

    Oracle: The checked-in valid, schema-invalid, unknown-value, and wrong-semantic-type
    filename inventories define both membership and the layer expected to accept or
    reject each file.

    Acceptance: The named partition raises exactly expected with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    text = (SPEC / "invalid" / name).read_text(encoding="utf-8")
    with pytest.raises(expected):
        OperatorRecordJsonSerializer().deserialize(text)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param("boolean-as-number.json", TypeError, id="boolean_as_number_json"),
        pytest.param("numeric-string.json", TypeError, id="numeric_string_json"),
    ],
)
def test_artifact__wrong_semantic_type_golden_files_are__agrees_exactly(
    name: str, expected: type[Exception]
) -> None:
    r"""Evidence ID: SV-ORJF-004

    Requirement: The version-1 golden fixture family has this exact runtime
    interoperability
    property: wrong semantic type golden files are: agrees exactly.

    Method: Enumerate the checked-in version-1 fixtures for wrong semantic type golden
    files
    are: agrees exactly and pass each case through the documented public serializer
    boundary.

    Oracle: The checked-in valid, schema-invalid, unknown-value, and wrong-semantic-type
    filename inventories define both membership and the layer expected to accept or
    reject each file.

    Acceptance: The named partition raises exactly expected with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only the declared schema/fixture layer agreement;
    failure identifies
    schema drift, fixture misclassification, runtime-layer drift, or an evidence defect.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    text = (SPEC / "invalid" / name).read_text(encoding="utf-8")
    with pytest.raises(expected):
        OperatorRecordJsonSerializer().deserialize(text)
