"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``FiringResult``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``FiringResult`` is the sole primary SUT. Tests exercise its documented public contract
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


def test_constructor__contract__audit_fields_are_intrinsically_coherent(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-039

    Requirement
    -----------
    reject contradictory firing audit state.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: reject contradictory firing audit state.
    Requirement: binding identity, successor revision, produced identities, and audit-ID
    tuples agree internally. Method: independently violate each relation through the
    public constructor. Oracle: exact transition equality, revision ``previous + 1``,
    uniqueness, and nonempty IDs. Acceptance: each construction raises ``ValueError``.
    Failure permits an incoherent immutable audit result. Limitation: transition
    execution and persistence are not evaluated.

    Oracle
    ------
    The documented public rule that the SUT must reject contradictory firing audit state
    is the contract oracle; fixed synthetic values, Python exact type/value semantics,
    and the public error taxonomy provide independently inspectable expected outcomes
    where used.

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
    """Evidence ID
    -----------
    This helper supports exactly SV-CPN-070, SV-CPN-072, SV-CPN-073 and owns no
    independent evidence ID.

    Requirement
    -----------
    Provide explicit synthetic setup or assertion mechanics without creating an
    independent pass claim.

    Method
    ------
    Construct or transform the public CPN test inputs required by the listed evidence
    owners. Prior helper description: local synthetic setup only.

    Oracle
    ------
    The helper has no independent oracle; each supported test owns and documents the
    applicable contract oracle.

    Acceptance
    ----------
    Return the exact public object or deterministic setup consumed by every listed
    evidence owner, without swallowing exceptions or asserting a separate result.

    Interpretation
    --------------
    A helper failure blocks or invalidates its listed evidence owners but is not an
    independent evidence failure.

    Limitations
    -----------
    The helper is synthetic, supports only the complete identifier list above, owns no
    independent evidence ID, and establishes no numerical verification, scientific
    validation, uncertainty quantification, physical meaning, or cross-language
    conformance."""
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


def test_constructor__contract__result_requires_transition_and_binding_types(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-070

    Requirement
    -----------
    require nonempty transition identity and typed binding.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: require nonempty transition identity and
    typed binding. A valid synthetic result supplies the positive oracle. Acceptance
    rejects empty transition with ``ValueError`` and foreign binding with ``TypeError``.
    Failure permits an audit result without a usable firing identity.

    Oracle
    ------
    The documented public rule that the SUT must require nonempty transition identity
    and typed binding is the contract oracle; fixed synthetic values, Python exact
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


def test_constructor__contract__previous_revision_requires_nonnegative_exact_integer(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-071

    Requirement
    -----------
    enforce the resolved previous-revision lower boundary.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: enforce the resolved previous-revision
    lower boundary. Exact built-in integer and nonnegative rules are the oracle.
    Acceptance rejects Boolean with ``TypeError`` and negative one with ``ValueError``.
    Upper-bound result coherence and operational revision overflow are covered
    separately.

    Oracle
    ------
    The documented public rule that the SUT must enforce the resolved previous-revision
    lower boundary is the contract oracle; fixed synthetic values, Python exact
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


def test_constructor__contract__result_revision_boundary_is_coherent(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-084

    Requirement
    -----------
    firing prior and successor revisions preserve the maximum valid signed-i64 control.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: preserve the largest constructible
    firing-result revisions. Requirement: result revision controls use nonnegative
    signed-i64 values while retaining the exact successor relation. Method: construct a
    result with prior ``2**63 - 2`` and successor ``2**63 - 1``, then submit prior
    ``2**63``. Oracle: fixed-width bounds plus the independent ``successor = prior + 1``
    invariant. Acceptance preserves both maximum-scale controls and rejects the
    out-of-range prior with ``ValueError``. Prior ``2**63 - 1`` is valid marking input
    but intentionally has no FiringResult successor; TransitionFirer owns its structured
    overflow. No scientific result or automatic iteration is inferred.

    Oracle
    ------
    The documented public rule that the SUT must firing prior and successor revisions
    preserve the maximum valid signed-i64 control is the contract oracle; fixed
    synthetic values, Python exact type/value semantics, and the public error taxonomy
    provide independently inspectable expected outcomes where used.

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


def test_constructor__contract__audit_id_sequences_require_unique_nonempty_strings(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-072

    Requirement
    -----------
    enforce immutable unique consumed/read identity sequences.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: enforce immutable unique consumed/read
    identity sequences. Public controlled-invalid construction is compared with exact
    tuple and identity invariants. Acceptance requires type/value rejection. Failure
    corrupts audit provenance; firing behavior and scientific provenance are excluded.

    Oracle
    ------
    The documented public rule that the SUT must enforce immutable unique consumed/read
    identity sequences is the contract oracle; fixed synthetic values, Python exact
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


def test_constructor__contract__produced_tokens_require_typed_unique_tuple(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-073

    Requirement
    -----------
    constrain produced tokens to unique typed immutable objects.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: constrain produced tokens to unique typed
    immutable objects. A token collaborator is used only as fixture; exact tuple/item
    type and token-ID uniqueness are the oracles. Acceptance raises ``TypeError`` or
    ``ValueError``. Failure permits contradictory successor audit state.

    Oracle
    ------
    The documented public rule that the SUT must constrain produced tokens to unique
    typed immutable objects is the contract oracle; fixed synthetic values, Python exact
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
    base = _valid_result(executable_net)
    with pytest.raises(TypeError):
        SUT(base.transition_id, base.binding, 0, base.marking, (), (), ["bad"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(base.transition_id, base.binding, 0, base.marking, (), (), ("bad",))  # type: ignore[arg-type]
    token = executable_net.initial_marking.places[-1].tokens[0]
    with pytest.raises(ValueError):
        SUT(base.transition_id, base.binding, 0, base.marking, (), (), (token, token))
