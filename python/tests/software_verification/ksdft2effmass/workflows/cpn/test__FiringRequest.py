"""Software verification for ``FiringRequest`` as the sole primary SUT.

The synthetic case checks request-owned output identity coherence through the
public constructor. Exact rejection is the oracle. Passing is neither numerical
verification, scientific validation, UQ, persistence, nor Rust conformance.
"""

import pytest

from ksdft2effmass.workflows.cpn import FiringRequest, TransitionBinding

pytestmark = pytest.mark.software_verification

SUT = FiringRequest


def test_cpn_sv_p1_037_output_token_ids_are_unique() -> None:
    """SV-CPN-037: reject duplicate caller-supplied output identities.

    Requirement: one request cannot assign the same identity twice. Method:
    construct a request with two ``duplicate`` entries and a valid empty binding.
    Oracle: tuple uniqueness by exact string equality. Acceptance: ``ValueError``
    mentions unique identities. Failure permits contradictory output allocation.
    Limitation: caller identity-generation policy and current marking are excluded.
    """
    with pytest.raises(ValueError, match="unique identities"):
        FiringRequest(
            "execute",
            TransitionBinding("execute", ()),
            ("duplicate", "duplicate"),
        )


def test_cpn_sv_p1_068_request_requires_matching_typed_transition_state() -> None:
    """SV-CPN-068: require a nonempty transition identity and typed binding.

    Public construction is the method and declared field types are the oracle.
    Acceptance retains valid collaborators, rejects foreign binding with ``TypeError``,
    and empty identity with ``ValueError``. Cross-object matching is not intrinsic.
    """
    binding = TransitionBinding("t", ())
    assert SUT("t", binding, ()).binding is binding
    with pytest.raises(TypeError):
        SUT(1, binding, ())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("t", "binding", ())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("", binding, ())


def test_cpn_sv_p1_069_output_ids_require_nonempty_exact_string_tuple() -> None:
    """SV-CPN-069: constrain output identities to an immutable nonempty-string tuple.

    Public controlled-invalid inputs exercise the boundary; declared wire shape is
    the oracle. Acceptance distinguishes ``TypeError`` from empty-ID ``ValueError``.
    Failure permits mutable or unusable output allocation.
    """
    binding = TransitionBinding("t", ())
    with pytest.raises(TypeError):
        SUT("t", binding, ["id"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("t", binding, (1,))  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("t", binding, ("",))
