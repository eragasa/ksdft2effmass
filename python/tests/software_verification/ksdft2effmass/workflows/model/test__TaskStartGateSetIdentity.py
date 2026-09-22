r"""Software verification of ``TaskStartGateSetIdentity``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskStartGateSetIdentity`` identity contract.

Facet and represented meaning

The class nominally identifies one Task start-gate policy without selecting a wire
grammar.

Intrinsic and cross-object scope

Tests cover exact built-in string validation, nonempty state, and immutability only.

VVUQ and scientific exclusions

This is software verification. It establishes no execution, scientific validity,
uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.workflows import TaskStartGateSetIdentity

pytestmark = pytest.mark.software_verification
SUT = TaskStartGateSetIdentity


def test_constructor__value__requires_nonempty_exact_string() -> None:
    """Test the exact lexical boundary of ``TaskStartGateSetIdentity.value``.

    Evidence ID: SV-WFM-IDENTITY-013

    Requirement: ``value`` is an exact nonempty built-in string.

    Acceptance: A nonempty string is retained, an integer raises ``TypeError``, and
    an empty string raises ``ValueError``.
    """
    value = SUT("identity.one")
    assert value.value == "identity.one"
    with pytest.raises(TypeError):
        SUT(1)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("")


def test_method__setattr__rejects_identity_mutation() -> None:
    """Test that ``TaskStartGateSetIdentity`` is operationally immutable.

    Evidence ID: SV-WFM-IDENTITY-014

    Requirement: A constructed identity cannot be changed through assignment.

    Acceptance: Assigning ``value`` raises ``FrozenInstanceError`` and leaves the
    original value unchanged.
    """
    value = SUT("identity.one")
    with pytest.raises(FrozenInstanceError):
        value.value = "identity.two"  # type: ignore[misc]
    assert value.value == "identity.one"
