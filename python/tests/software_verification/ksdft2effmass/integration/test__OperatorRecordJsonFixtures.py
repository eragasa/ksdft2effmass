"""Golden operator-record JSON fixture software-verification integration evidence.

Object: complete version-1 valid/invalid golden-file corpus. Evidence class:
software verification, distinct from serializer facet and schema metamodel evidence.
Requirement: directories contain exactly the approved named files; valid files
round-trip to deterministic canonical serializer text and invalid files are all
rejected. Strategy: filesystem enumeration and public serializer calls only.
Oracle: approved inventory and each golden classification. Acceptance is complete
set equality and classification agreement. Passing does not validate physical data,
scientific meaning, UQ, independent Rust behavior, or serializer internals; failure
indicates missing/stale artifacts or interoperability drift.
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
    """Support SV-ORJF-001 by enumerating only golden JSON files.

    Evidence ID: supporting helper (no executable owner). Requirement: inventories
    ignore explanatory README files. Method: nonrecursive ``*.json`` enumeration.
    Oracle: filesystem artifact suffix. Interpretation: provides exact names.
    Limitations: does not parse/classify content or establish scientific validation,
    UQ, serializer correctness, or Rust conformance.
    """
    return {path.name for path in (SPEC / kind).glob("*.json")}


def test_golden_fixture_inventory_is_exact() -> None:
    """Evidence ID: SV-ORJF-001.

    Requirement: all and only approved valid/invalid golden files are present.
    Method: compare filesystem names with independent literal sets. Oracle: approved
    version-1 fixture inventory. Acceptance is exact set equality. Interpretation:
    failure identifies a missing, renamed, or unreviewed fixture. Limitations:
    content semantics, scientific validation, UQ, and Rust conformance are not
    established.
    """
    assert fixture_names("valid") == VALID_NAMES
    assert fixture_names("invalid") == INVALID_NAMES


@pytest.mark.parametrize("name", sorted(VALID_NAMES))
def test_valid_golden_files_have_deterministic_serializer_round_trips(
    name: str,
) -> None:
    """Evidence ID: SV-ORJF-002.

    Requirement: every valid fixture is accepted and canonical serializer output is
    deterministic and value-equivalent to its JSON content. Method: deserialize,
    serialize twice, and compare decoded JSON objects. Oracle: golden valid label
    plus standard parser equality. Acceptance is stable text and equal JSON value.
    Interpretation: failure is fixture/runtime interoperability drift. Limitations:
    object facet internals, scientific validation, UQ, and independent Rust
    conformance are not duplicated or established.
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
        ("boolean-as-number.json", TypeError),
        ("dimension-mismatch.json", ValueError),
        ("duplicate-basis-label.json", ValueError),
        ("empty-string.json", ValueError),
        ("energy-reference-value.json", ValueError),
        ("missing-field.json", ValueError),
        ("nonorthogonal-basis.json", ValueError),
        ("nonsquare-matrix.json", ValueError),
        ("numeric-string.json", TypeError),
        ("ragged-matrix.json", ValueError),
        ("singular-cell.json", ValueError),
        ("unknown-field.json", ValueError),
        ("unsupported-version.json", ValueError),
    ],
    ids=[name.removesuffix(".json") for name in sorted(INVALID_NAMES)],
)
def test_invalid_golden_files_are_rejected_by_public_serializer(
    name: str, expected: type[Exception]
) -> None:
    """Evidence ID: SV-ORJF-003.

    Requirement: every invalid golden file remains rejected by the public boundary.
    Method: enumerate the exact invalid inventory and call deserialize. Oracle: each
    artifact's approved invalid classification and exact exception category.
    Acceptance is the independently listed TypeError or ValueError. Interpretation:
    acceptance or taxonomy drift is a contract failure. Limitations: detailed reason
    ownership remains in serializer/DataObject facets; no scientific validation,
    UQ, or Rust conformance is performed.
    """
    text = (SPEC / "invalid" / name).read_text(encoding="utf-8")
    with pytest.raises(expected):
        OperatorRecordJsonSerializer().deserialize(text)
