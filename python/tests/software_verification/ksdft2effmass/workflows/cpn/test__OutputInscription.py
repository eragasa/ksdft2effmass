r"""Software verification of ``OutputInscription``.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public ``OutputInscription``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
``OutputInscription`` is the sole primary SUT. Tests exercise its documented public
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

from ksdft2effmass.workflows.cpn import OutputInscription

SUT = OutputInscription


def test_constructor__output_inscription__rejects_wrong_types() -> None:
    """Evidence ID: SV-CPN-049

    Requirement: ``OutputInscription`` rejects wrong semantic types at the public
    constructor boundary for its
    ``output_inscription`` contract.

    Method: Exercise each preserved synthetic wrong-type input through the public SUT
    with
    no warning acceptance or private-state mutation.

    Oracle: The documented public exact-type taxonomy and Python exception taxonomy
    independently require ``TypeError`` for these inputs.

    Acceptance: Every preserved partition assertion raises exactly ``TypeError``;
    retained
    exact setup and state assertions also hold.

    Interpretation: Pass supports only this named type partition; failure may identify
    implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations: Synthetic cases exclude unexercised inputs, engine execution,
    persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError):
        SUT([])  # type: ignore[arg-type]


def test_constructor__output_inscription__rejects_invalid_values() -> None:
    """Evidence ID: SV-CPN-107

    Requirement: ``OutputInscription`` rejects malformed values of accepted semantic
    types for its
    ``output_inscription`` contract.

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
    with pytest.raises(ValueError, match="must not be empty"):
        SUT(())


pytestmark = pytest.mark.software_verification
