r"""Software verification of ``ExternalFailureStage``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned evidence verifies the closed failure-stage vocabulary,
``StrEnum`` inheritance, exact ordered names and values, alias absence, value
construction, name lookup, and rejection behavior.

Intrinsic and cross-object scope

--------------------------------
The sole SUT is ``ExternalFailureStage``. Its three members classify where an
already-observed external failure occurred: request acceptance, execution, or
result capture. Literal version-1 vocabulary and Python enum semantics provide
exact oracles; construction and lookup perform no I/O.

VVUQ and scientific exclusions

------------------------------
The enum does not execute or accept requests, retry work, inspect diagnostics,
or classify scientific-model error. It does not establish numerical
verification, scientific validation, UQ, or provenance truth.
"""

from enum import StrEnum
from typing import Any, cast

import pytest

from ksdft2effmass.provenance import ExternalFailureStage

SUT = ExternalFailureStage
pytestmark = pytest.mark.software_verification


def test_field__wire_vocabulary__has_exact_order_names_values_and_count() -> None:
    """Evidence ID: SV-PROV-045

    Requirement: The enum is an alias-free StrEnum with the exact three ordered stages.

    Method: Inspect inheritance, iteration, the public member mapping, and member
    counts.

    Oracle: The accepted version-1 vocabulary fixes all three literal name/value pairs.

    Acceptance: Inheritance, order, names, values, member keys, alias absence, and count
    are exact.

    Interpretation: Passing establishes the closed ordered external-failure-stage
    vocabulary.

    Limitations: This test does not exercise lookup or observe an external failure.
    """
    expected = (
        ("REQUEST_ACCEPTANCE", "request_acceptance"),
        ("EXECUTION", "execution"),
        ("RESULT_CAPTURE", "result_capture"),
    )
    assert issubclass(SUT, StrEnum)
    assert tuple((member.name, member.value) for member in SUT) == expected
    assert tuple(SUT.__members__) == (
        "REQUEST_ACCEPTANCE",
        "EXECUTION",
        "RESULT_CAPTURE",
    )
    assert len(SUT.__members__) == 3
    assert len(tuple(SUT)) == 3


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(
            "request_acceptance",
            ExternalFailureStage.REQUEST_ACCEPTANCE,
            id="request_acceptance_stage",
        ),
        pytest.param(
            "execution",
            ExternalFailureStage.EXECUTION,
            id="execution_stage",
        ),
        pytest.param(
            "result_capture",
            ExternalFailureStage.RESULT_CAPTURE,
            id="result_capture_stage",
        ),
    ],
)
def test_method__call__constructs_each_stage_from_wire_value(
    value: str, expected: ExternalFailureStage
) -> None:
    """Evidence ID: SV-PROV-185

    Requirement: Each exact wire value constructs its corresponding canonical stage
    member.

    Method: Call value construction for each explicit wire-value/member pair.

    Oracle: The expected values are literal public ``ExternalFailureStage`` members.

    Acceptance: Every construction result is the supplied expected member by identity.

    Interpretation: Passing establishes exact value construction for all three failure
    stages.

    Limitations: Construction classifies no real failure and performs no external
    execution.
    """
    assert ExternalFailureStage(value) is expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param(
            "REQUEST_ACCEPTANCE",
            ExternalFailureStage.REQUEST_ACCEPTANCE,
            id="request_acceptance_stage",
        ),
        pytest.param(
            "EXECUTION",
            ExternalFailureStage.EXECUTION,
            id="execution_stage",
        ),
        pytest.param(
            "RESULT_CAPTURE",
            ExternalFailureStage.RESULT_CAPTURE,
            id="result_capture_stage",
        ),
    ],
)
def test_method__getitem__returns_each_stage_from_declared_name(
    name: str, expected: ExternalFailureStage
) -> None:
    """Evidence ID: SV-PROV-284

    Requirement: Each exact declared name resolves to its corresponding canonical stage
    member.

    Method: Apply public bracketed lookup for each explicit name/member pair. A narrow
    typing cast exposes runtime enum subscription to mypy without changing behavior.

    Oracle: The expected values are literal public ``ExternalFailureStage`` members.

    Acceptance: Every name lookup is the supplied expected member by identity.

    Interpretation: Passing establishes exact declared-name lookup for all three failure
    stages.

    Limitations: Lookup does not inspect diagnostics, retry work, or establish
    provenance truth.
    """
    assert cast(Any, SUT)[name] is expected


def test_method__call__rejects_unknown_wire_value() -> None:
    """Evidence ID: SV-PROV-186

    Requirement: Unknown text cannot construct a member of the closed stage vocabulary.

    Method: Call value construction with the fixed absent string ``unknown``.

    Oracle: The accepted three-value vocabulary contains no ``unknown`` value.

    Acceptance: Construction raises exactly ``ValueError``.

    Interpretation: Passing establishes rejection of unknown textual failure-stage
    values.

    Limitations: Wrong semantic types and name lookup are separate evidence owners.
    """
    with pytest.raises(ValueError):
        ExternalFailureStage("unknown")


def test_method__call__rejects_wrong_semantic_type() -> None:
    """Evidence ID: SV-PROV-285

    Requirement: Integer input cannot construct a member of the string-valued stage
    vocabulary.

    Method: Call value construction with integer one through the invalid public
    boundary.

    Oracle: Python enum construction finds no integer among the three string wire
    values.

    Acceptance: Construction raises exactly ``ValueError``.

    Interpretation: Passing establishes rejection of the independent wrong-type input
    partition.

    Limitations: This records enum behavior, not record-constructor semantic-type
    policy.
    """
    with pytest.raises(ValueError):
        ExternalFailureStage(cast(Any, 1))


def test_method__getitem__rejects_unknown_member_name() -> None:
    """Evidence ID: SV-PROV-187

    Requirement: An undeclared member name cannot resolve through bracketed name lookup.

    Method: Apply public name lookup with the fixed absent name ``UNKNOWN``. A narrow
    typing cast exposes runtime enum subscription to mypy without changing behavior.

    Oracle: The three declared names do not include ``UNKNOWN``.

    Acceptance: Name lookup raises exactly ``KeyError``.

    Interpretation: Passing establishes rejection of names outside the closed stage
    declaration.

    Limitations: This does not test value construction or case normalization.
    """
    with pytest.raises(KeyError):
        cast(Any, SUT)["UNKNOWN"]
