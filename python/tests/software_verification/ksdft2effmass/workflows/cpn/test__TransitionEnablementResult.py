r"""Software verification of ``TransitionEnablementResult``.

Facet and represented meaning
--------------------------------------
This module provides software-verification evidence for the public
``TransitionEnablementResult`` software surface and its finite, exact CPN routing
representation. It does not represent a physical observable or numerical approximation.

Intrinsic and cross-object scope
--------------------------------
``TransitionEnablementResult`` is the sole primary SUT. Tests exercise its documented
public contract with synthetic routing inputs; exact constructor, language, enum,
ordering, and error-taxonomy rules provide the independent oracles. Collaborators only
construct inputs or expose public outcomes.

VVUQ and scientific exclusions
------------------------------
Passing means the named software contracts hold; failure may identify an implementation,
fixture, oracle transcription, environment, or public-contract inconsistency. This
module excludes numerical verification, scientific validation, uncertainty
quantification, physical correctness, persistence and engine-adapter behavior, and
cross-language conformance."""

import pytest

from ksdft2effmass.workflows.cpn import TransitionBinding, TransitionEnablementResult

pytestmark = pytest.mark.software_verification

SUT = TransitionEnablementResult


def test_constructor__fields__bindings_match_transition_and_are_unique() -> None:
    """Evidence ID
    -----------
    SV-CPN-038

    Requirement
    -----------
    enforce coherent deterministic enablement bindings.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: enforce coherent deterministic enablement
    bindings. Requirement: every binding names the result transition and occurs once.
    Method: construct results with a mismatched binding and a duplicated matching
    binding. Oracle: exact transition-string equality and tuple uniqueness. Acceptance:
    each state raises its documented ``ValueError``. Failure permits contradictory or
    duplicate enabled choices. Limitation: enumeration itself is owned by
    ``TransitionEnabler`` and is not re-tested here.

    Oracle
    ------
    The documented public rule that the SUT must enforce coherent deterministic
    enablement bindings is the contract oracle; fixed synthetic values, Python exact
    type/value semantics, and the public error taxonomy provide independently
    inspectable expected outcomes where used.

    Acceptance
    ----------
    Every preserved exact equality, identity, ordering, representation, and expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation
    --------------
    Pass supports only this named software contract. Failure may indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations
    -----------
    The case excludes unexercised inputs and dependencies, physical conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    with pytest.raises(ValueError, match="enablement binding"):
        TransitionEnablementResult("execute", (TransitionBinding("other", ()),))
    binding = TransitionBinding("execute", ())
    with pytest.raises(ValueError, match="bindings must be unique"):
        TransitionEnablementResult("execute", (binding, binding))


def test_constructor__enablement_container__preserves_valid_state() -> None:
    """Evidence ID
    -----------
    SV-CPN-077

    Requirement
    -----------
    ``TransitionEnablementResult`` preserves the documented exact valid-state
    behavior for its ``enablement_container`` contract.

    Method
    ------
    Construct the public SUT with the retained valid synthetic inputs and inspect
    exact public state.

    Oracle
    ------
    The fixed inputs and documented canonical public representation provide the
    independent exact oracle.

    Acceptance
    ----------
    Every retained exact identity, equality, ordering, type, and represented-state
    assertion holds.

    Interpretation
    --------------
    Pass supports this valid-state mapping; failure may identify implementation,
    fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    assert SUT("t", ()).bindings == ()


def test_constructor__enablement_container__rejects_wrong_types() -> None:
    """Evidence ID
    -----------
    SV-CPN-131

    Requirement
    -----------
    ``TransitionEnablementResult`` rejects wrong semantic types for its
    ``enablement_container`` contract.

    Method
    ------
    Exercise every retained synthetic wrong-type input through the public SUT
    without private mutation.

    Oracle
    ------
    The documented exact-type taxonomy independently requires ``TypeError`` for
    every retained call.

    Acceptance
    ----------
    Every retained wrong-type call raises exactly ``TypeError``.

    Interpretation
    --------------
    Pass supports this type partition; failure may identify implementation, fixture,
    oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError):
        SUT(1, ())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("t", [])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("t", ("bad",))  # type: ignore[arg-type]


def test_constructor__enablement_container__rejects_invalid_values() -> None:
    """Evidence ID
    -----------
    SV-CPN-106

    Requirement
    -----------
    ``TransitionEnablementResult`` rejects malformed values of accepted semantic
    types for its
    ``enablement_container`` contract.

    Method
    ------
    Exercise each preserved synthetic invalid-value input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``ValueError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named value partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(ValueError):
        SUT("", ())
