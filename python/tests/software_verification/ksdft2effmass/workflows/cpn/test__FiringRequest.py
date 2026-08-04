"""Software verification of the ``FiringRequest`` public request contract.

Evidence class and represented meaning
--------------------------------------
Software-verification evidence covers the public ``FiringRequest`` DataObject, a finite
software representation of a requested CPN transition firing. The synthetic cases
represent workflow-control state, not a physical model or mathematical operator.

Owned contract, oracle, and scope
---------------------------------
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


def test_constructor__transition_state__requires_typed_binding_and_identity() -> None:
    """Verify transition identity and binding constructor boundaries.

    Evidence ID
    SV-CPN-068

    Requirement
    Public ``FiringRequest`` construction must require an exact nonempty string
    transition identity and a ``TransitionBinding`` instance, while retaining a valid
    binding by identity.

    Method
    Construct valid synthetic state, then supply an integer transition identity, a
    string in place of the binding, and an empty transition identity through the public
    constructor. No warnings are expected.

    Oracle
    The documented field contract independently admits a nonempty exact string and typed
    binding, assigns wrong semantic types to ``TypeError``, and assigns an empty
    required identity to ``ValueError``.

    Acceptance
    Valid construction retains the exact collaborator object; each wrong-typed input
    raises ``TypeError`` and the empty transition identity raises ``ValueError``.

    Interpretation
    A pass confirms request-owned type and identity enforcement. A failure may indicate
    constructor, collaborator, Python-type, exception-taxonomy, or public-contract
    drift.

    Limitations
    This case does not require the binding's transition identity to match the request,
    inspect token assignments, execute a firing, or establish numerical verification,
    physical correctness, scientific validation, UQ, or portability."""
    binding = TransitionBinding("t", ())
    assert SUT("t", binding, ()).binding is binding
    with pytest.raises(TypeError):
        SUT(1, binding, ())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("t", "binding", ())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("", binding, ())


def test_field__output_token_ids__requires_nonempty_exact_string_tuple() -> None:
    """Verify the exact output-token identity tuple contract.

    Evidence ID
    SV-CPN-069

    Requirement
    The public ``output_token_ids`` field must be an immutable tuple whose every member
    is an exact nonempty string.

    Method
    With valid synthetic transition state, pass a list, a tuple containing an integer,
    and a tuple containing an empty string to the public constructor as
    controlled-invalid inputs. No warnings are expected.

    Oracle
    The documented exact field representation independently excludes mutable lists and
    nonstring members as semantic type errors, and the nonempty identity invariant
    excludes the empty string.

    Acceptance
    The list and integer-member cases raise ``TypeError``; the empty-string member case
    raises ``ValueError``.

    Interpretation
    A pass confirms immutable exact-string output identity storage boundaries. A failure
    may reflect constructor, collaborator, language-type, exception-taxonomy, or
    public-contract drift.

    Limitations
    The case excludes duplicate identities covered separately, Unicode normalization,
    identity registries, marking collisions, firing execution, numerical verification,
    physical correctness, scientific validation, UQ, persistence, and cross-language
    behavior."""
    binding = TransitionBinding("t", ())
    with pytest.raises(TypeError):
        SUT("t", binding, ["id"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("t", binding, (1,))  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("t", binding, ("",))
