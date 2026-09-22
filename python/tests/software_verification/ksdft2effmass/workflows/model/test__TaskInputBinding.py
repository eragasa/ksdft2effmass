r"""Software verification of ``TaskInputBinding``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskInputBinding`` DataObject.

Facet and represented meaning

The class binds one concrete Task input name to one existing ResultObject.

Intrinsic and cross-object scope

Tests cover exact name validation and structural ResultObject identity admission.

VVUQ and scientific exclusions

This is software verification. It establishes no result provenance, scientific
validity, Task execution, uncertainty quantification, or human acceptance.
"""

from dataclasses import dataclass

import pytest

from ksdft2effmass.workflows import (
    ResultObjectIdentity,
    TaskInputBinding,
)

pytestmark = pytest.mark.software_verification
SUT = TaskInputBinding


def test_constructor__fields__accepts_named_structural_result_object() -> None:
    """Test the valid name-to-result binding contract.

    Evidence ID: SV-WFM-INPUT-001

    Requirement: A binding accepts a nonempty name and a structurally conforming
    object whose identity is exactly ``ResultObjectIdentity``.

    Acceptance: Construction retains the supplied name and result object.
    """

    @dataclass(frozen=True, slots=True)
    class ConcreteResult:
        identity: ResultObjectIdentity

    result = ConcreteResult(ResultObjectIdentity("result.one"))
    value = SUT("input.one", result)
    assert value.name == "input.one"
    assert value.result is result


def test_constructor__fields__rejects_invalid_name_or_result_contract() -> None:
    """Test every intrinsic rejection boundary of ``TaskInputBinding``.

    Evidence ID: SV-WFM-INPUT-002

    Requirement: The name is an exact nonempty string and the result exposes the
    exact Workflow-owned nominal identity type.

    Acceptance: A non-string name, empty name, absent identity, and wrong identity
    type each raise the documented ``TypeError`` or ``ValueError``.
    """

    @dataclass(frozen=True, slots=True)
    class ConcreteResult:
        identity: ResultObjectIdentity

    @dataclass(frozen=True, slots=True)
    class WrongIdentityResult:
        identity: str

    result = ConcreteResult(ResultObjectIdentity("result.one"))
    with pytest.raises(TypeError):
        SUT(1, result)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("", result)
    with pytest.raises(TypeError):
        SUT("input.one", object())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("input.one", WrongIdentityResult("result.one"))  # type: ignore[arg-type]
