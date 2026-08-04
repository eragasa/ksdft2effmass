"""Software verification for ``TransitionEnablementResult`` as sole primary SUT.

Public construction is checked against exact transition and binding coherence.
Passing verifies only ResultObject invariants; science, numerics, UQ, persistence,
and Rust conformance are excluded.
"""

import pytest

from ksdft2effmass.workflows.cpn import TransitionBinding, TransitionEnablementResult

pytestmark = pytest.mark.software_verification

SUT = TransitionEnablementResult


def test_cpn_sv_p1_038_bindings_match_transition_and_are_unique() -> None:
    """SV-CPN-038: enforce coherent deterministic enablement bindings.

    Requirement: every binding names the result transition and occurs once.
    Method: construct results with a mismatched binding and a duplicated matching
    binding. Oracle: exact transition-string equality and tuple uniqueness.
    Acceptance: each state raises its documented ``ValueError``. Failure permits
    contradictory or duplicate enabled choices. Limitation: enumeration itself is
    owned by ``TransitionEnabler`` and is not re-tested here.
    """
    with pytest.raises(ValueError, match="enablement binding"):
        TransitionEnablementResult("execute", (TransitionBinding("other", ()),))
    binding = TransitionBinding("execute", ())
    with pytest.raises(ValueError, match="bindings must be unique"):
        TransitionEnablementResult("execute", (binding, binding))


def test_cpn_sv_p1_077_enablement_container_requires_public_types() -> None:
    """SV-CPN-077: require nonempty transition identity and immutable binding tuple.

    Empty enabled choices are a valid public result and the positive oracle.
    Acceptance rejects empty identity with ``ValueError`` and mutable/foreign binding
    collections with ``TypeError``. Failure permits unstable enablement results.
    """
    assert SUT("t", ()).bindings == ()
    with pytest.raises(TypeError):
        SUT(1, ())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("", ())
    with pytest.raises(TypeError):
        SUT("t", [])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("t", ("bad",))  # type: ignore[arg-type]
