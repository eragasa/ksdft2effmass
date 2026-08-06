r"""Software verification of ``ExternalExecutionStatus``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies the closed one-member wire vocabulary,
``StrEnum`` inheritance, exact name and value, declaration order, absence of
aliases, value construction, name lookup, and rejection behavior.

Intrinsic and cross-object scope
--------------------------------
The sole SUT is ``ExternalExecutionStatus``. The literal version-1 vocabulary
``COMPLETED = "completed"`` and Python enum semantics provide exact oracles.
No collaborator is a co-owner, and construction and lookup perform no I/O.

VVUQ and scientific exclusions
------------------------------
``ExternalExecutionStatus.COMPLETED`` means only that the external boundary
completed. It does not establish solver convergence, parsing correctness,
numerical acceptance, scientific validation, UQ, external-tool correctness, or
provenance truth.
"""

from enum import StrEnum
from typing import Any, cast

import pytest

from ksdft2effmass.provenance import ExternalExecutionStatus

SUT = ExternalExecutionStatus
pytestmark = pytest.mark.software_verification


def test_field__wire_vocabulary__has_exact_order_name_value_and_count() -> None:
    """Evidence ID
    SV-PROV-042
    Requirement
    The enum is an alias-free StrEnum with only ``COMPLETED = "completed"``.
    Method
    Inspect inheritance, iteration, the public member mapping, and member counts.
    Oracle
    The accepted version-1 vocabulary contains the single literal name/value pair.
    Acceptance
    Inheritance, order, name, value, member keys, alias absence, and count are exact.
    Interpretation
    Passing establishes the exact closed one-member execution-status vocabulary.
    Limitations
    This test does not exercise lookup or establish any execution outcome quality.
    """
    expected = (("COMPLETED", "completed"),)
    assert issubclass(SUT, StrEnum)
    assert tuple((member.name, member.value) for member in SUT) == expected
    assert tuple(SUT.__members__) == ("COMPLETED",)
    assert len(SUT.__members__) == 1
    assert len(tuple(SUT)) == 1


def test_method__call__constructs_completed_member_from_wire_value() -> None:
    """Evidence ID
    SV-PROV-182
    Requirement
    The exact wire value ``completed`` constructs the sole canonical member.
    Method
    Call the public enum value constructor with the accepted literal wire value.
    Oracle
    The literal public member ``ExternalExecutionStatus.COMPLETED`` is canonical.
    Acceptance
    Value construction returns that member by identity.
    Interpretation
    Passing establishes that the exact wire value constructs the completion member.
    Limitations
    Construction does not establish convergence, parsing, or external-tool correctness.
    """
    assert ExternalExecutionStatus("completed") is ExternalExecutionStatus.COMPLETED


def test_method__getitem__returns_completed_member_from_declared_name() -> None:
    """Evidence ID
    SV-PROV-282
    Requirement
    The declared name ``COMPLETED`` resolves to the sole canonical member.
    Method
    Apply public bracketed name lookup with the exact declared literal name.
    Oracle
    The literal public member ``ExternalExecutionStatus.COMPLETED`` is canonical.
    Acceptance
    Name lookup returns that member by identity.
    Interpretation
    Passing establishes exact declared-name lookup for the completion member.
    Limitations
    Name lookup does not establish execution correctness or provenance truth.
    """
    assert ExternalExecutionStatus["COMPLETED"] is ExternalExecutionStatus.COMPLETED


def test_method__call__rejects_unknown_wire_value() -> None:
    """Evidence ID
    SV-PROV-183
    Requirement
    Unknown text cannot construct a member of the closed wire vocabulary.
    Method
    Call value construction with the fixed absent string ``unknown``.
    Oracle
    The sole accepted wire value is ``completed``; ``unknown`` is absent.
    Acceptance
    Construction raises exactly ``ValueError``.
    Interpretation
    Passing establishes rejection of unknown textual wire values.
    Limitations
    Wrong semantic types and name lookup are separate evidence owners.
    """
    with pytest.raises(ValueError):
        ExternalExecutionStatus("unknown")


def test_method__call__rejects_wrong_semantic_type() -> None:
    """Evidence ID
    SV-PROV-283
    Requirement
    Integer input cannot construct a member of the string-valued vocabulary.
    Method
    Call value construction with integer one through the invalid public boundary.
    Oracle
    Python enum construction finds no integer in the one-string-value vocabulary.
    Acceptance
    Construction raises exactly ``ValueError``.
    Interpretation
    Passing establishes rejection of the independently wrong-type input partition.
    Limitations
    This records enum ``ValueError`` behavior, not record-constructor type policy.
    """
    with pytest.raises(ValueError):
        ExternalExecutionStatus(cast(Any, 1))


def test_method__getitem__rejects_unknown_member_name() -> None:
    """Evidence ID
    SV-PROV-184
    Requirement
    An undeclared member name cannot resolve through bracketed name lookup.
    Method
    Apply public name lookup with the fixed absent name ``UNKNOWN``.
    Oracle
    The sole declared name is ``COMPLETED``; ``UNKNOWN`` is absent.
    Acceptance
    Name lookup raises exactly ``KeyError``.
    Interpretation
    Passing establishes rejection of names outside the closed declaration.
    Limitations
    This does not test value construction or case normalization.
    """
    with pytest.raises(KeyError):
        ExternalExecutionStatus["UNKNOWN"]
