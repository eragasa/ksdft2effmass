"""Software verification for ``TransitionDefinition`` as the sole primary SUT.

Synthetic public construction checks only owner-intrinsic contract invariants.
Documented field rules and exact exception taxonomy are independent oracles.
Passing is not numerical verification, scientific validation, uncertainty
quantification, persistence, engine-adapter, or Rust-conformance evidence.
"""

import pytest

from ksdft2effmass.workflows.cpn import (
    GuardExpression,
    GuardOperator,
    TransitionDefinition,
)

SUT = TransitionDefinition


def test_cpn_sv_p1_057_transition_requires_identity_description_and_guard() -> None:
    """SV-CPN-057: require a named documented transition and pure guard.

    A constant public guard is the collaborator and declared types are the oracle.
    Acceptance retains it, rejects empty identity with ``ValueError``, and a Boolean
    guard with ``TypeError``. Failure admits malformed transition definitions.
    """
    guard = GuardExpression(GuardOperator.TRUE)
    assert SUT("t", "transition", guard).guard is guard
    with pytest.raises(ValueError):
        SUT("", "transition", guard)
    with pytest.raises(TypeError):
        SUT("t", "transition", True)  # type: ignore[arg-type]


pytestmark = pytest.mark.software_verification
