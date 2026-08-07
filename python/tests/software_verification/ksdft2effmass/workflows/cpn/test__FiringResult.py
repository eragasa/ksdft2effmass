r"""Software verification of ``FiringResult``.

Facet and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``FiringResult``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Intrinsic and cross-object scope
--------------------------------
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


def test_constructor__fields__audit_fields_are_intrinsically_coherent(
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
    with pytest.raises(ValueError):
        FiringResult(
            "execute",
            matching,
            0,
            CpnMarking(1, executable_net.model_id, 1, places),
            ("",),
            (),
            (),
        )
    with pytest.raises(ValueError):
        FiringResult(
            "execute",
            matching,
            0,
            CpnMarking(1, executable_net.model_id, 1, places),
            ("duplicate", "duplicate"),
            (),
            (),
        )


def make_valid_firing_result(executable_net: CpnNetDefinition) -> FiringResult:
    """Evidence ID
    -----------
    Owns no identifier; supports SV-CPN-070, SV-CPN-072, SV-CPN-073, SV-CPN-089,
    SV-CPN-103.
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


def test_constructor__result_requires__preserves_valid_state(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-070

    Requirement
    -----------
    ``FiringResult`` preserves the documented exact valid-state behavior for its
    ``result_requires`` contract.

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
    CpnMarking(1, executable_net.model_id, 1, executable_net.initial_marking.places)
    TransitionBinding("execute", ())
    assert make_valid_firing_result(executable_net).transition_id == "execute"


def test_constructor__result_requires__rejects_wrong_types(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-128

    Requirement
    -----------
    ``FiringResult`` rejects wrong semantic types for its ``result_requires`` contract.

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
    marking = CpnMarking(
        1, executable_net.model_id, 1, executable_net.initial_marking.places
    )
    binding = TransitionBinding("execute", ())
    with pytest.raises(TypeError):
        SUT(1, binding, 0, marking, (), (), ())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("execute", "bad", 0, marking, (), (), ())  # type: ignore[arg-type]


def test_constructor__result_requires__rejects_invalid_values(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-101

    Requirement
    -----------
    ``FiringResult`` rejects malformed values of accepted semantic
    types for its
    ``result_requires`` contract.

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
    marking = CpnMarking(
        1, executable_net.model_id, 1, executable_net.initial_marking.places
    )
    binding = TransitionBinding("execute", ())
    with pytest.raises(ValueError, match="transition_id must not be empty"):
        SUT("", binding, 0, marking, (), (), ())


def test_constructor__previous_revision__rejects_wrong_types(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-071

    Requirement
    -----------
    ``FiringResult`` rejects wrong semantic types at the public
    constructor boundary for its
    ``previous_revision`` contract.

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
    marking = CpnMarking(
        1, executable_net.model_id, 0, executable_net.initial_marking.places
    )
    binding = TransitionBinding("execute", ())
    with pytest.raises(TypeError):
        SUT("execute", binding, True, marking, (), (), ())
    with pytest.raises(TypeError):
        SUT("execute", binding, 0.0, marking, (), (), ())  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="marking"):
        SUT("execute", binding, 0, "marking", (), (), ())  # type: ignore[arg-type]


def test_constructor__previous_revision__rejects_invalid_values(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-102

    Requirement
    -----------
    ``FiringResult`` rejects malformed values of accepted semantic
    types for its
    ``previous_revision`` contract.

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
    marking = CpnMarking(
        1, executable_net.model_id, 0, executable_net.initial_marking.places
    )
    binding = TransitionBinding("execute", ())
    with pytest.raises(ValueError):
        SUT("execute", binding, -1, marking, (), (), ())


def test_constructor__fields__result_revision_boundary_is_coherent(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-084

    Requirement
    -----------
    ``FiringResult`` preserves the exact accepted state for its
    ``fields`` contract.

    Method
    ------
    Construct the public SUT and inspect retained exact public outcomes.

    Oracle
    ------
    The documented public invariant and fixed synthetic inputs provide the independent
    exact state oracle.

    Acceptance
    ----------
    Every retained exact state assertion holds.

    Interpretation
    --------------
    Pass supports only this accepted-state partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    maximum = 2**63 - 1
    binding = TransitionBinding("execute", ())
    marking = CpnMarking(
        1, executable_net.model_id, maximum, executable_net.initial_marking.places
    )
    result = SUT("execute", binding, maximum - 1, marking, (), (), ())
    assert result.previous_revision == maximum - 1
    assert result.marking.revision == maximum


def test_constructor__fields__rejects_invalid_state(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-149

    Requirement
    -----------
    ``FiringResult`` rejects the documented invalid state for its
    ``fields`` contract.

    Method
    ------
    Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle
    ------
    The documented public invariant and fixed synthetic inputs provide the independent
    exact error-taxonomy oracle.

    Acceptance
    ----------
    Every retained invalid call raises the documented exact public exception.

    Interpretation
    --------------
    Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    maximum = 2**63 - 1
    binding = TransitionBinding("execute", ())
    marking = CpnMarking(
        1, executable_net.model_id, maximum, executable_net.initial_marking.places
    )
    SUT("execute", binding, maximum - 1, marking, (), (), ())
    with pytest.raises(ValueError, match="signed i64"):
        SUT("execute", binding, maximum + 1, marking, (), (), ())


@pytest.mark.parametrize(
    ("consumed", "read"),
    (
        pytest.param(["x"], (), id="consumed_list_wrong_type"),
        pytest.param((), ["x"], id="read_list_wrong_type"),
        pytest.param((1,), (), id="consumed_item_wrong_type"),
        pytest.param((), (1,), id="read_item_wrong_type"),
    ),
)
def test_constructor__audit_id_sequence_types__rejects_wrong_types(
    executable_net: CpnNetDefinition,
    consumed: Any,
    read: Any,
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
    base = make_valid_firing_result(executable_net)
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


@pytest.mark.parametrize(
    ("consumed", "read"),
    (
        pytest.param(("",), (), id="consumed_empty_identifier"),
        pytest.param((), ("",), id="read_empty_identifier"),
        pytest.param(("x", "x"), (), id="consumed_duplicate_identifier"),
        pytest.param((), ("x", "x"), id="read_duplicate_identifier"),
    ),
)
def test_constructor__audit_id_sequence_values__rejects_empty_or_duplicate_ids(
    executable_net: CpnNetDefinition,
    consumed: tuple[str, ...],
    read: tuple[str, ...],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-089

    Requirement
    -----------
    Consumed and read audit identifiers must be nonempty and unique per sequence.

    Method
    ------
    Construct the public result with one named invalid value partition and no warnings.

    Oracle
    ------
    The public nonempty-unique identifier invariant fixes each rejected tuple.

    Acceptance
    ----------
    Construction raises exactly ``ValueError`` for every explicit parameter case.

    Interpretation
    --------------
    Pass supports value validation; failure permits ambiguous firing audit identities.

    Limitations
    -----------
    Synthetic identifiers exclude engine execution, scientific validation, UQ, physical
    correctness, persistence, portability, and cross-language conformance.
    """
    base = make_valid_firing_result(executable_net)
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


def test_constructor__produced_tokens__rejects_wrong_types(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-073

    Requirement
    -----------
    ``FiringResult`` rejects wrong semantic types at the public
    constructor boundary for its
    ``produced_tokens`` contract.

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
    base = make_valid_firing_result(executable_net)
    with pytest.raises(TypeError):
        SUT(base.transition_id, base.binding, 0, base.marking, (), (), ["bad"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(base.transition_id, base.binding, 0, base.marking, (), (), ("bad",))  # type: ignore[arg-type]


def test_constructor__produced_tokens__rejects_invalid_values(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-103

    Requirement
    -----------
    ``FiringResult`` rejects malformed values of accepted semantic
    types for its
    ``produced_tokens`` contract.

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
    base = make_valid_firing_result(executable_net)
    token = executable_net.initial_marking.places[-1].tokens[0]
    with pytest.raises(ValueError):
        SUT(base.transition_id, base.binding, 0, base.marking, (), (), (token, token))
