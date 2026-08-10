r"""Software verification of ``InputInscription``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``InputInscription``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
``InputInscription`` is the sole primary SUT. Tests exercise its documented public
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

from ksdft2effmass.workflows.cpn import InputArcMode, InputInscription, TokenPattern

SUT = InputInscription


def test_constructor__input_inscription__preserves_valid_state() -> None:
    """Evidence ID: SV-CPN-048

    Requirement: ``InputInscription`` preserves the documented exact valid-state
    behavior for its
    ``input_inscription`` contract.

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
    pattern = TokenPattern("v", ("c",))
    assert SUT(InputArcMode.READ, (pattern,)).patterns == (pattern,)


def test_constructor__input_inscription__rejects_wrong_types() -> None:
    """Evidence ID: SV-CPN-125

    Requirement: ``InputInscription`` rejects wrong semantic types for its
    ``input_inscription``
    contract.

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
    pattern = TokenPattern("v", ("c",))
    with pytest.raises(TypeError):
        SUT("read", (pattern,))  # type: ignore[arg-type]


def test_constructor__input_inscription__rejects_invalid_values() -> None:
    """Evidence ID: SV-CPN-098

    Requirement: ``InputInscription`` rejects malformed values of accepted semantic
    types for its
    ``input_inscription`` contract.

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
    with pytest.raises(ValueError):
        SUT(InputArcMode.READ, ())


pytestmark = pytest.mark.software_verification
