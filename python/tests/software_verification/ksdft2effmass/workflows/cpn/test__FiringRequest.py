r"""Software verification of ``FiringRequest``.

Facet and represented meaning
--------------------------------
Software verification of the ``FiringRequest`` public request contract.

Software-verification evidence covers the public ``FiringRequest`` DataObject, a finite
software representation of a requested CPN transition firing. The synthetic cases
represent workflow-control state, not a physical model or mathematical operator.

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``FiringRequest``. The owned contract comprises public
constructor typing, nonempty transition identity, and exact output-token identity tuple
invariants. The oracle is the documented request contract and Python exception taxonomy;
``TransitionBinding`` is only a typed constructor collaborator.

VVUQ and scientific exclusions
------------------------------
Passing confirms only the stated represented-software behavior; failure may indicate
production, fixture, oracle, exception-taxonomy, or public-contract drift. This module
does not provide numerical verification, scientific validation, uncertainty
quantification, physical-correctness, persistence, transition enablement, firing
execution, or cross-language evidence."""

import pytest

from ksdft2effmass.workflows.cpn import FiringRequest, TransitionBinding

pytestmark = pytest.mark.software_verification

SUT = FiringRequest


def test_constructor__output_token_ids__rejects_duplicates() -> None:
    """Verify duplicate output-token identity rejection.

    Evidence ID
    SV-CPN-037

    Requirement
    Public ``FiringRequest`` construction must reject an output-token identity tuple
    containing the same exact string more than once.

    Method
    Construct a request with a valid synthetic transition identity, a typed empty
    ``TransitionBinding``, and two caller-supplied ``"duplicate"`` output identities. No
    warnings are expected.

    Oracle
    Exact tuple membership shows that the two Unicode strings are equal, while the
    documented request uniqueness invariant independently makes repeated output
    identities invalid.

    Acceptance
    Construction raises ``ValueError`` with text matching ``unique identities``.

    Interpretation
    A pass confirms request-owned duplicate rejection. A failure may reflect
    constructor, collaborator, message, exception-taxonomy, oracle, or contract drift
    and could permit contradictory output allocation.

    Limitations
    The synthetic case excludes caller identity-generation policy, the current marking,
    output-count validation, firing execution, numerical verification, physical
    correctness, scientific validation, UQ, and cross-language behavior."""
    with pytest.raises(ValueError, match="unique identities"):
        FiringRequest(
            "execute",
            TransitionBinding("execute", ()),
            ("duplicate", "duplicate"),
        )


def test_constructor__transition_state__preserves_valid_state() -> None:
    """Evidence ID
    -----------
    SV-CPN-068

    Requirement
    -----------
    ``FiringRequest`` preserves the documented exact valid-state behavior for its
    ``transition_state`` contract.

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
    binding = TransitionBinding("t", ())
    assert SUT("t", binding, ()).binding is binding


def test_constructor__transition_state__rejects_wrong_types() -> None:
    """Evidence ID
    -----------
    SV-CPN-123

    Requirement
    -----------
    ``FiringRequest`` rejects wrong semantic types for its ``transition_state``
    contract.

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
    binding = TransitionBinding("t", ())
    with pytest.raises(TypeError):
        SUT(1, binding, ())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("t", "binding", ())  # type: ignore[arg-type]


def test_constructor__transition_state__rejects_invalid_values() -> None:
    """Evidence ID
    -----------
    SV-CPN-095

    Requirement
    -----------
    ``FiringRequest`` rejects malformed values of accepted semantic
    types for its
    ``transition_state`` contract.

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
    binding = TransitionBinding("t", ())
    with pytest.raises(ValueError):
        SUT("", binding, ())


def test_field__output_token_ids__rejects_wrong_types() -> None:
    """Evidence ID
    -----------
    SV-CPN-069

    Requirement
    -----------
    ``FiringRequest`` rejects wrong semantic types at the public
    constructor boundary for its
    ``output_token_ids`` contract.

    Method
    ------
    Exercise each preserved synthetic wrong-type input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public exact-type taxonomy and Python exception taxonomy
    independently require ``TypeError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``TypeError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named type partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    binding = TransitionBinding("t", ())
    with pytest.raises(TypeError):
        SUT("t", binding, ["id"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("t", binding, (1,))  # type: ignore[arg-type]


def test_field__output_token_ids__rejects_invalid_values() -> None:
    """Evidence ID
    -----------
    SV-CPN-096

    Requirement
    -----------
    ``FiringRequest`` rejects malformed values of accepted semantic
    types for its
    ``output_token_ids`` contract.

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
    binding = TransitionBinding("t", ())
    with pytest.raises(ValueError):
        SUT("t", binding, ("",))
