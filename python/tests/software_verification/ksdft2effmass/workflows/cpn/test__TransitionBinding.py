r"""Software verification of ``TransitionBinding``.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``TransitionBinding``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
``TransitionBinding`` is the sole primary SUT. Tests exercise its documented public
contract with synthetic routing inputs; exact constructor, language, enum, ordering, and
error-taxonomy rules provide the independent oracles. Collaborators only construct
inputs or expose public outcomes.

VVUQ and scientific exclusions

------------------------------
Passing means the named software contracts hold; failure may identify an implementation,
fixture, oracle transcription, environment, or public-contract inconsistency. This
module excludes numerical verification, scientific validation, uncertainty
quantification, physical correctness, persistence and engine-adapter behavior, and
cross-language conformance."""

import pytest

from ksdft2effmass.workflows.cpn import TokenBinding, TransitionBinding

SUT = TransitionBinding


def test_constructor__transition_binding__preserves_valid_state() -> None:
    """Evidence ID: SV-CPN-056

    Requirement: ``TransitionBinding`` preserves the documented exact valid-state
    behavior for
    its ``transition_binding`` contract.

    Method: Construct the public SUT with the retained valid synthetic inputs and
    inspect
    exact public state.

    Oracle: The fixed inputs and documented canonical public representation provide the
    independent exact oracle.

    Acceptance: Every retained exact identity, equality, ordering, type, and
    represented-state
    assertion holds.

    Interpretation: Pass supports this valid-state mapping; failure may identify
    implementation,
    fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    a, b = TokenBinding("a", "1"), TokenBinding("b", "2")
    assert SUT("t", (b, a)).assignments == (a, b)


def test_constructor__transition_binding__rejects_wrong_types() -> None:
    """Evidence ID: SV-CPN-138

    Requirement: ``TransitionBinding`` rejects wrong semantic types for its
    ``transition_binding`` contract.

    Method: Exercise every retained synthetic wrong-type input through the public SUT
    without private mutation.

    Oracle: The documented exact-type taxonomy independently requires ``TypeError`` for
    every retained call.

    Acceptance: Every retained wrong-type call raises exactly ``TypeError``.

    Interpretation: Pass supports this type partition; failure may identify
    implementation, fixture,
    oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    a, _b = TokenBinding("a", "1"), TokenBinding("b", "2")
    with pytest.raises(TypeError):
        SUT("t", [a])  # type: ignore[arg-type]


def test_constructor__transition_binding__rejects_invalid_values() -> None:
    """Evidence ID: SV-CPN-118

    Requirement: ``TransitionBinding`` rejects malformed values of accepted semantic
    types for its
    ``transition_binding`` contract.

    Method: Exercise each preserved synthetic invalid-value input through the public SUT
    with
    no warning acceptance or private-state mutation.

    Oracle: The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance: Every preserved partition assertion raises exactly ``ValueError``;
    retained
    exact setup and state assertions also hold.

    Interpretation: Pass supports only this named value partition; failure may identify
    implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    a = TokenBinding("a", "1")
    with pytest.raises(ValueError):
        SUT("t", (a, TokenBinding("a", "2")))


pytestmark = pytest.mark.software_verification
