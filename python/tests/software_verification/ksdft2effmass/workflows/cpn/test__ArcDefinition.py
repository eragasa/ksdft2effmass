r"""Software verification of ``ArcDefinition``.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``ArcDefinition``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
``ArcDefinition`` is the sole primary SUT. Tests exercise its documented public contract
with synthetic routing inputs; exact constructor, language, enum, ordering, and
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

from ksdft2effmass.workflows.cpn import (
    ArcDefinition,
    ArcDirection,
    InputArcMode,
    InputInscription,
    TokenPattern,
)

SUT = ArcDefinition


def test_constructor__fields__direction_selects_exactly_one_inscription() -> None:
    """Evidence ID: SV-CPN-040

    Requirement: ``ArcDefinition`` preserves the exact accepted state for its
    ``fields`` contract.

    Method: Construct the public SUT and inspect retained exact public outcomes.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact state oracle.

    Acceptance: Every retained exact state assertion holds.

    Interpretation: Pass supports only this accepted-state partition; failure may
    identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    inscription = InputInscription(InputArcMode.CONSUME, (TokenPattern("v", ("c",)),))
    assert (
        SUT(
            "a", "p", "t", ArcDirection.INPUT, input_inscription=inscription
        ).input_inscription
        == inscription
    )


def test_constructor__fields__rejects_invalid_state() -> None:
    """Evidence ID: SV-CPN-145

    Requirement: ``ArcDefinition`` rejects the documented invalid state for its
    ``fields`` contract.

    Method: Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle: The documented public invariant and fixed synthetic inputs provide the
    independent
    exact error-taxonomy oracle.

    Acceptance: Every retained invalid call raises the documented exact public
    exception.

    Interpretation: Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    inscription = InputInscription(InputArcMode.CONSUME, (TokenPattern("v", ("c",)),))
    with pytest.raises(ValueError, match="match arc direction"):
        SUT("a", "p", "t", ArcDirection.OUTPUT, input_inscription=inscription)


pytestmark = pytest.mark.software_verification
