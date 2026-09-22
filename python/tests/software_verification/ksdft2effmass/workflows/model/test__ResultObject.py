r"""Software verification of ``ResultObject``.

Evidence profile: routine

Bounded artifact scope: the public ``ResultObject`` structural protocol.

Facet and represented meaning

The protocol identifies immutable workflow-facing results owned by concrete domains.

Intrinsic and cross-object scope

Tests cover runtime structural conformance and required nominal identity presence.

VVUQ and scientific exclusions

This is software verification. Protocol conformance establishes no result truth,
scientific validity, uncertainty quantification, or human acceptance.
"""

from dataclasses import dataclass

import pytest

from ksdft2effmass.workflows import ResultObject, ResultObjectIdentity

pytestmark = pytest.mark.software_verification
SUT = ResultObject


def test_protocol__identity__accepts_independent_structural_implementation() -> None:
    """Test structural conformance without nominal inheritance.

    Evidence ID: SV-WFM-RESULT-PROTOCOL-001

    Requirement: A concrete domain result conforms by exposing its exact immutable
    ``ResultObjectIdentity`` property.

    Acceptance: An independent frozen class satisfies ``isinstance`` at runtime.
    """

    @dataclass(frozen=True, slots=True)
    class ConcreteResult:
        identity: ResultObjectIdentity

    assert isinstance(ConcreteResult(ResultObjectIdentity("result.one")), SUT)


def test_protocol__identity__rejects_object_without_identity_member() -> None:
    """Test the required structural member of ``ResultObject``.

    Evidence ID: SV-WFM-RESULT-PROTOCOL-002

    Requirement: A result must expose an ``identity`` member.

    Acceptance: A plain object does not satisfy the runtime-checkable protocol.
    """
    assert not isinstance(object(), SUT)
