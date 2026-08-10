r"""Software verification of ``PythonConformanceRequest``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies the closed explicit-input request and its optional migration state.

Intrinsic and cross-object scope

The sole SUT is ``PythonConformanceRequest``; ``PythonModuleSource`` is an
input collaborator and the public request state table supplies exact oracles.

VVUQ and scientific exclusions

Passing establishes request software semantics only, not validation findings,
filesystem truth, numerical verification, scientific validation, UQ, or acceptance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness.pi.evidence import (
    PythonConformanceRequest,
    PythonModuleSource,
)

pytestmark = pytest.mark.software_verification
SUT = PythonConformanceRequest
SOURCE = PythonModuleSource("module.py", b"pass\n")


def test_constructor__explicit_inputs__preserves_payloads_and_migration() -> None:
    """Evidence ID: SV-TEV-005

    Requirement: The request preserves its closed source, ownership, and migration
    inputs.

    Method: Construct one request containing exact bytes and diagnostic paths.

    Oracle: The literal inputs independently fix every public field value.

    Acceptance: Every field equals the supplied value exactly and sources remain a
    tuple.

    Interpretation: Failure identifies construction or represented-state drift.

    Limitations: Payload syntax and validation behavior are excluded.
    """
    value = SUT((SOURCE,), "owners.json", b"{}", None, "migration.json", b"{}", None)
    assert value.sources == (SOURCE,)
    assert value.ownership_path == "owners.json"
    assert value.ownership_payload == b"{}"
    assert value.ownership_read_error is None
    assert value.migration_path == "migration.json"
    assert value.migration_payload == b"{}"
    assert value.migration_read_error is None


def test_field__immutable_state__rejects_reassignment() -> None:
    """Evidence ID: SV-TEV-006

    Requirement: A constructed request is operationally immutable.

    Method: Construct a minimal request and attempt public ownership-path reassignment.

    Oracle: Frozen dataclass semantics require reassignment to raise
    FrozenInstanceError.

    Acceptance: Reassignment raises exactly FrozenInstanceError.

    Interpretation: Failure identifies loss of the immutable request boundary.

    Limitations: External byte identity and collaborator internals are excluded.
    """
    value = SUT((SOURCE,), "owners.json", b"{}")
    with pytest.raises(FrozenInstanceError):
        value.ownership_path = "other.json"  # type: ignore[misc]


@pytest.mark.parametrize(
    "arguments",
    (
        pytest.param(([], "owners.json", b"{}"), id="list_sources_wrong_type"),
        pytest.param(
            ((object(),), "owners.json", b"{}"), id="foreign_source_wrong_type"
        ),
        pytest.param(((SOURCE,), 1, b"{}"), id="integer_ownership_path_wrong_type"),
        pytest.param(
            ((SOURCE,), "owners.json", "{}"), id="string_ownership_payload_wrong_type"
        ),
    ),
)
def test_constructor__required_types__rejects_wrong_semantic_types(
    arguments: tuple[object, ...],
) -> None:
    """Evidence ID: SV-TEV-007

    Requirement: Required request inputs reject values outside their declared semantic
    types.

    Method: Supply one wrong semantic type in each controlled required-input partition.

    Oracle: The public request contract assigns TypeError to semantic type violations.

    Acceptance: Every declared partition raises TypeError.

    Interpretation: Failure identifies public type-policy or constructor drift.

    Limitations: Optional-field type partitions and correct-type conflicts are excluded.
    """
    with pytest.raises(TypeError):
        SUT(*arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "arguments",
    (
        pytest.param(((), "owners.json", b"{}"), id="empty_sources"),
        pytest.param(
            ((SOURCE,), "owners.json", None, None), id="ownership_without_outcome"
        ),
        pytest.param(
            ((SOURCE,), "owners.json", b"{}", "error"), id="ownership_payload_and_error"
        ),
        pytest.param(
            ((SOURCE,), "owners.json", b"{}", None, None, b"{}", None),
            id="migration_payload_without_path",
        ),
        pytest.param(
            ((SOURCE,), "owners.json", b"{}", None, "migration.json", None, None),
            id="migration_without_outcome",
        ),
    ),
)
def test_constructor__closed_input_state__rejects_conflicting_values(
    arguments: tuple[object, ...],
) -> None:
    """Evidence ID: SV-TEV-008

    Requirement: Empty sources and contradictory payload/read-error states are invalid.

    Method: Construct each controlled correct-type state-table violation.

    Oracle: The public contract requires nonempty sources and exactly one outcome for
    each
    present metadata input.

    Acceptance: Every declared partition raises ValueError.

    Interpretation: Failure identifies request invariant or contract drift.

    Limitations: Payload contents and cross-path ownership coverage are excluded.
    """
    with pytest.raises(ValueError):
        SUT(*arguments)  # type: ignore[arg-type]
