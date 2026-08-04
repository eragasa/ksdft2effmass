"""Software verification for ``FiringResult`` as the sole primary SUT.

Synthetic public construction checks result-owned audit coherence. Exact field
relations are the oracle. Passing provides no numerical verification, scientific
validation, UQ, persistence, adapter, or Rust-conformance evidence.
"""

from typing import Any

import pytest

from ksdft2effmass.workflows.cpn import (
    CpnMarking,
    CpnNetDefinition,
    FiringResult,
    TransitionBinding,
)

pytestmark = pytest.mark.software_verification

SUT = FiringResult


def test_cpn_sv_p1_039_audit_fields_are_intrinsically_coherent(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-039: reject contradictory firing audit state.

    Requirement: binding identity, successor revision, produced identities, and
    audit-ID tuples agree internally. Method: independently violate each relation
    through the public constructor. Oracle: exact transition equality, revision
    ``previous + 1``, uniqueness, and nonempty IDs. Acceptance: each construction
    raises ``ValueError``. Failure permits an incoherent immutable audit result.
    Limitation: transition execution and persistence are not evaluated.
    """
    places = executable_net.initial_marking.places
    matching = TransitionBinding("execute", ())
    with pytest.raises(ValueError, match="binding must match"):
        FiringResult(
            "execute",
            TransitionBinding("other", ()),
            0,
            CpnMarking(1, executable_net.model_id, 1, places),
            (),
            (),
            (),
        )
    with pytest.raises(ValueError, match="marking revision"):
        FiringResult(
            "execute",
            matching,
            4,
            CpnMarking(1, executable_net.model_id, 1, places),
            (),
            (),
            (),
        )
    produced = executable_net.initial_marking.places[2].tokens[0]
    with pytest.raises(ValueError, match="produced token identities"):
        FiringResult(
            "execute",
            matching,
            0,
            CpnMarking(1, executable_net.model_id, 1, places),
            (),
            (),
            (produced, produced),
        )
    for invalid_ids in (("",), ("duplicate", "duplicate")):
        with pytest.raises(ValueError):
            FiringResult(
                "execute",
                matching,
                0,
                CpnMarking(1, executable_net.model_id, 1, places),
                invalid_ids,
                (),
                (),
            )


def _valid_result(executable_net: CpnNetDefinition) -> FiringResult:
    return SUT(
        "execute",
        TransitionBinding("execute", ()),
        0,
        CpnMarking(
            1, executable_net.model_id, 1, executable_net.initial_marking.places
        ),
        (),
        (),
        (),
    )


def test_cpn_sv_p1_070_result_requires_transition_and_binding_types(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-070: require nonempty transition identity and typed binding.

    A valid synthetic result supplies the positive oracle. Acceptance rejects empty
    transition with ``ValueError`` and foreign binding with ``TypeError``. Failure
    permits an audit result without a usable firing identity.
    """
    assert _valid_result(executable_net).transition_id == "execute"
    marking = CpnMarking(
        1, executable_net.model_id, 1, executable_net.initial_marking.places
    )
    binding = TransitionBinding("execute", ())
    with pytest.raises(TypeError):
        SUT(1, binding, 0, marking, (), (), ())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="transition_id must not be empty"):
        SUT("", binding, 0, marking, (), (), ())
    with pytest.raises(TypeError):
        SUT("execute", "bad", 0, marking, (), (), ())  # type: ignore[arg-type]


def test_cpn_sv_p1_071_previous_revision_requires_nonnegative_exact_integer(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-071: enforce the resolved previous-revision lower boundary.

    Exact built-in integer and nonnegative rules are the oracle. Acceptance rejects
    Boolean with ``TypeError`` and negative one with ``ValueError``. Upper-bound
    result coherence and operational revision overflow are covered separately.
    """
    marking = CpnMarking(
        1, executable_net.model_id, 0, executable_net.initial_marking.places
    )
    binding = TransitionBinding("execute", ())
    with pytest.raises(TypeError):
        SUT("execute", binding, True, marking, (), (), ())
    with pytest.raises(TypeError):
        SUT("execute", binding, 0.0, marking, (), (), ())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT("execute", binding, -1, marking, (), (), ())
    with pytest.raises(TypeError, match="marking"):
        SUT("execute", binding, 0, "marking", (), (), ())  # type: ignore[arg-type]


def test_cpn_sv_p1_084_result_revision_boundary_is_coherent(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-084: preserve the largest constructible firing-result revisions.

    Requirement: result revision controls use nonnegative signed-i64 values while
    retaining the exact successor relation. Method: construct a result with prior
    ``2**63 - 2`` and successor ``2**63 - 1``, then submit prior ``2**63``.
    Oracle: fixed-width bounds plus the independent ``successor = prior + 1``
    invariant. Acceptance preserves both maximum-scale controls and rejects the
    out-of-range prior with ``ValueError``. Prior ``2**63 - 1`` is valid marking
    input but intentionally has no FiringResult successor; TransitionFirer owns its
    structured overflow. No scientific result or automatic iteration is inferred.
    """
    maximum = 2**63 - 1
    binding = TransitionBinding("execute", ())
    marking = CpnMarking(
        1, executable_net.model_id, maximum, executable_net.initial_marking.places
    )
    result = SUT("execute", binding, maximum - 1, marking, (), (), ())
    assert result.previous_revision == maximum - 1
    assert result.marking.revision == maximum
    with pytest.raises(ValueError, match="signed i64"):
        SUT("execute", binding, maximum + 1, marking, (), (), ())


def test_cpn_sv_p1_072_audit_id_sequences_require_unique_nonempty_strings(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-072: enforce immutable unique consumed/read identity sequences.

    Public controlled-invalid construction is compared with exact tuple and identity
    invariants. Acceptance requires type/value rejection. Failure corrupts audit
    provenance; firing behavior and scientific provenance are excluded.
    """
    base = _valid_result(executable_net)
    invalid_pairs: tuple[tuple[Any, Any], ...] = (
        (["x"], ()),
        ((), ["x"]),
        ((1,), ()),
        ((), (1,)),
    )
    for consumed, read in invalid_pairs:
        with pytest.raises(TypeError):
            SUT(
                base.transition_id,
                base.binding,
                base.previous_revision,
                base.marking,
                consumed,
                read,
                (),
            )
    for consumed, read in (
        (("",), ()),
        ((), ("",)),
        (("x", "x"), ()),
        ((), ("x", "x")),
    ):
        with pytest.raises(ValueError):
            SUT(
                base.transition_id,
                base.binding,
                base.previous_revision,
                base.marking,
                consumed,
                read,
                (),
            )


def test_cpn_sv_p1_073_produced_tokens_require_typed_unique_tuple(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-073: constrain produced tokens to unique typed immutable objects.

    A token collaborator is used only as fixture; exact tuple/item type and token-ID
    uniqueness are the oracles. Acceptance raises ``TypeError`` or ``ValueError``.
    Failure permits contradictory successor audit state.
    """
    base = _valid_result(executable_net)
    with pytest.raises(TypeError):
        SUT(base.transition_id, base.binding, 0, base.marking, (), (), ["bad"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(base.transition_id, base.binding, 0, base.marking, (), (), ("bad",))  # type: ignore[arg-type]
    token = executable_net.initial_marking.places[-1].tokens[0]
    with pytest.raises(ValueError):
        SUT(base.transition_id, base.binding, 0, base.marking, (), (), (token, token))
