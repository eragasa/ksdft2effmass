"""Evidence class and represented meaning
--------------------------------------
This module provides software-verification evidence for the public ``TransitionEnabler``
software surface and its finite, exact CPN routing representation. It does not represent
a physical observable or numerical approximation.

Owned contract, oracle, and scope
---------------------------------
``TransitionEnabler`` is the sole primary SUT. Tests exercise its documented public
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

from collections.abc import Callable
from dataclasses import replace

import pytest

import ksdft2effmass.workflows.cpn as cpn
from ksdft2effmass.workflows.cpn import (
    CpnMarking,
    CpnNetDefinition,
    CpnToken,
    PlaceMarking,
    TransitionEnabler,
)

pytestmark = pytest.mark.software_verification

SUT = TransitionEnabler


def test_method__contract__enablement_synchronizes_multiple_inputs(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-015

    Requirement
    -----------
    synchronization across consume and read inputs.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: synchronization across consume and read
    inputs. Prior requirement detail: The version-1 P1 contract requires synchronization
    across consume and read inputs. Prior method detail: Call
    ``TransitionEnabler.execute`` for ``execute`` on the base marking with work and
    authorization tokens sharing ``run-1``. Prior independent oracle detail: The pure
    equality guard and one candidate at each input analytically yield one complete
    binding. Prior acceptance criterion detail: Exactly one binding is returned with
    variables ordered ``authorization, work``. Prior failure interpretation detail: A
    different count/order means synchronization or deterministic canonicalization
    regressed. Prior limitations detail: No external execution occurs when a transition
    is enabled.

    Oracle
    ------
    The documented public rule that the SUT must synchronization across consume and read
    inputs is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

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
    result = TransitionEnabler().execute(
        executable_net, executable_net.initial_marking, "execute"
    )
    assert len(result.bindings) == 1
    assert tuple(item.variable for item in result.bindings[0].assignments) == (
        "authorization",
        "work",
    )


def test_method__contract__enablement_returns_deterministic_multiset_choices(
    token_factory: Callable[..., CpnToken], executable_net: CpnNetDefinition
) -> None:
    """Evidence ID
    -----------
    SV-CPN-016

    Requirement
    -----------
    deterministic enumeration of multiset choices.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: deterministic enumeration of multiset
    choices. Prior requirement detail: The version-1 P1 contract requires deterministic
    enumeration of multiset choices. Prior method detail: Replace the ready marking with
    ``work-b`` and ``work-a`` and call ``TransitionEnabler.execute``. Prior independent
    oracle detail: The two independently identified compatible work tokens form exactly
    two choices; lexical token ID is the ordering oracle. Prior acceptance criterion
    detail: Returned work token IDs are exactly ``['work-a', 'work-b']``. Prior failure
    interpretation detail: Failure indicates a lost choice, duplicate choice, or
    nondeterministic order. Prior limitations detail: The case covers one varying input,
    not reachability exploration.

    Oracle
    ------
    The documented public rule that the SUT must deterministic enumeration of multiset
    choices is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

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
    places = tuple(
        PlaceMarking(
            place.place_id,
            (token_factory("work-b"), token_factory("work-a"))
            if place.place_id == "ready"
            else place.tokens,
        )
        for place in executable_net.initial_marking.places
    )
    marking = CpnMarking(1, executable_net.model_id, 0, places)
    result = TransitionEnabler().execute(executable_net, marking, "execute")
    assert [binding.assignments[1].token_id for binding in result.bindings] == [
        "work-a",
        "work-b",
    ]


def test_method__contract__unknown_transition_retains_structured_detail(
    executable_net: cpn.CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-024

    Requirement
    -----------
    structured unknown-transition failure.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: structured unknown-transition failure.
    Prior requirement detail: The version-1 P1 contract requires structured
    unknown-transition failure. Prior method detail: Call ``TransitionEnabler.execute``
    with transition ID ``missing`` on a valid net and marking. Prior independent oracle
    detail: The net transition registry contains only ``execute``. Prior acceptance
    criterion detail: ``CpnBindingError.detail`` carries code ``UNKNOWN_TRANSITION`` and
    transition ID ``missing``. Prior failure interpretation detail: Failure loses
    machine-readable context or accepts an undefined transition. Prior limitations
    detail: No binding enumeration occurs for the missing transition.

    Oracle
    ------
    The documented public rule that the SUT must structured unknown-transition failure
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
    with pytest.raises(cpn.CpnBindingError) as error:
        cpn.TransitionEnabler().execute(
            executable_net, executable_net.initial_marking, "missing"
        )
    assert error.value.detail.code is cpn.CpnErrorCode.UNKNOWN_TRANSITION
    assert error.value.detail.transition_id == "missing"


def test_method__contract__invalid_marking_translates_to_structured_error(
    executable_net: cpn.CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-025

    Requirement
    -----------
    operational translation of an invalid marking.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: operational translation of an invalid
    marking. Prior requirement detail: The version-1 P1 contract requires operational
    translation of an invalid marking. Prior method detail: Pass a one-place marking to
    ``TransitionEnabler.execute`` with the valid three-place net. Prior independent
    oracle detail: ``CpnMarkingValidator`` independently identifies that the complete
    place set is absent. Prior acceptance criterion detail: The ActionObject raises
    ``CpnMarkingError`` with detail code ``INVALID_MARKING``. Prior failure
    interpretation detail: Attribute errors or unstructured failures would violate
    operational translation. Prior limitations detail: The underlying issue list is
    covered separately.

    Oracle
    ------
    The documented public rule that the SUT must operational translation of an invalid
    marking is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

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
    marking = cpn.CpnMarking(
        1, executable_net.model_id, 0, (cpn.PlaceMarking("ready", ()),)
    )
    with pytest.raises(cpn.CpnMarkingError) as error:
        cpn.TransitionEnabler().execute(executable_net, marking, "execute")
    assert error.value.detail.code is cpn.CpnErrorCode.INVALID_MARKING


def test_method__contract__invalid_definition_translates_to_structured_error(
    executable_net: cpn.CpnNetDefinition,
) -> None:
    """Evidence ID
    -----------
    SV-CPN-026

    Requirement
    -----------
    operational translation of an invalid definition.

    Method
    ------
    Exercise the primary SUT through the public construction or operation boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: operational translation of an invalid
    definition. Prior requirement detail: The version-1 P1 contract requires operational
    translation of an invalid definition. Prior method detail: Replace one place's
    allowed colors with unknown ``missing`` and call ``TransitionEnabler.execute``.
    Prior independent oracle detail: Cross-object definition validation independently
    reports the unknown color reference. Prior acceptance criterion detail: The
    ActionObject raises ``CpnDefinitionError`` with code ``INVALID_DEFINITION``. Prior
    failure interpretation detail: Success or an unrelated exception means invalid
    definitions bypass structured translation. Prior limitations detail: This is
    definition software verification, not a physical model check.

    Oracle
    ------
    The documented public rule that the SUT must operational translation of an invalid
    definition is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

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
    bad_place = replace(executable_net.places[0], allowed_color_ids=("missing",))
    bad_net = replace(executable_net, places=(bad_place,) + executable_net.places[1:])
    with pytest.raises(cpn.CpnDefinitionError) as error:
        cpn.TransitionEnabler().execute(bad_net, bad_net.initial_marking, "execute")
    assert error.value.detail.code is cpn.CpnErrorCode.INVALID_DEFINITION
