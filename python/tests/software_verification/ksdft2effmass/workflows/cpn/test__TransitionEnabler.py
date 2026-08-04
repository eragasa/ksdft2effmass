"""Software verification for ``TransitionEnabler`` as the sole primary SUT.

Evidence class: software verification. Requirement and strategy are stated per
case; public construction/execution supplies the method and exact state or the
documented exception taxonomy supplies the independent oracle. Passing verifies
only the named class contract. It does not provide numerical verification,
scientific validation, uncertainty quantification, persistence, SNAKES-adapter,
Rust-conformance, or scientific-execution evidence. Collaborators are synthetic
setup only.
"""

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


def test_cpn_sv_p1_015_enablement_synchronizes_multiple_inputs(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-015: synchronization across consume and read inputs.

    Requirement
    -----------
    The version-1 P1 contract requires synchronization across consume and read
    inputs.

    Method
    ------
    Call ``TransitionEnabler.execute`` for ``execute`` on the base marking with work
    and authorization tokens sharing ``run-1``.

    Independent oracle
    ------------------
    The pure equality guard and one candidate at each input analytically yield one
    complete binding.

    Acceptance criterion
    --------------------
    Exactly one binding is returned with variables ordered ``authorization, work``.

    Failure interpretation
    ----------------------
    A different count/order means synchronization or deterministic canonicalization
    regressed.

    Limitations
    -----------
    No external execution occurs when a transition is enabled.
    """
    result = TransitionEnabler().execute(
        executable_net, executable_net.initial_marking, "execute"
    )
    assert len(result.bindings) == 1
    assert tuple(item.variable for item in result.bindings[0].assignments) == (
        "authorization",
        "work",
    )


def test_cpn_sv_p1_016_enablement_returns_deterministic_multiset_choices(
    token_factory: Callable[..., CpnToken], executable_net: CpnNetDefinition
) -> None:
    """SV-CPN-016: deterministic enumeration of multiset choices.

    Requirement
    -----------
    The version-1 P1 contract requires deterministic enumeration of multiset
    choices.

    Method
    ------
    Replace the ready marking with ``work-b`` and ``work-a`` and call
    ``TransitionEnabler.execute``.

    Independent oracle
    ------------------
    The two independently identified compatible work tokens form exactly two
    choices; lexical token ID is the ordering oracle.

    Acceptance criterion
    --------------------
    Returned work token IDs are exactly ``['work-a', 'work-b']``.

    Failure interpretation
    ----------------------
    Failure indicates a lost choice, duplicate choice, or nondeterministic order.

    Limitations
    -----------
    The case covers one varying input, not reachability exploration.
    """
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


def test_cpn_sv_p1_024_unknown_transition_retains_structured_detail(
    executable_net: cpn.CpnNetDefinition,
) -> None:
    """SV-CPN-024: structured unknown-transition failure.

    Requirement
    -----------
    The version-1 P1 contract requires structured unknown-transition failure.

    Method
    ------
    Call ``TransitionEnabler.execute`` with transition ID ``missing`` on a valid net
    and marking.

    Independent oracle
    ------------------
    The net transition registry contains only ``execute``.

    Acceptance criterion
    --------------------
    ``CpnBindingError.detail`` carries code ``UNKNOWN_TRANSITION`` and transition ID
    ``missing``.

    Failure interpretation
    ----------------------
    Failure loses machine-readable context or accepts an undefined transition.

    Limitations
    -----------
    No binding enumeration occurs for the missing transition.
    """
    with pytest.raises(cpn.CpnBindingError) as error:
        cpn.TransitionEnabler().execute(
            executable_net, executable_net.initial_marking, "missing"
        )
    assert error.value.detail.code is cpn.CpnErrorCode.UNKNOWN_TRANSITION
    assert error.value.detail.transition_id == "missing"


def test_cpn_sv_p1_025_invalid_marking_translates_to_structured_error(
    executable_net: cpn.CpnNetDefinition,
) -> None:
    """SV-CPN-025: operational translation of an invalid marking.

    Requirement
    -----------
    The version-1 P1 contract requires operational translation of an invalid
    marking.

    Method
    ------
    Pass a one-place marking to ``TransitionEnabler.execute`` with the valid
    three-place net.

    Independent oracle
    ------------------
    ``CpnMarkingValidator`` independently identifies that the complete place set is
    absent.

    Acceptance criterion
    --------------------
    The ActionObject raises ``CpnMarkingError`` with detail code
    ``INVALID_MARKING``.

    Failure interpretation
    ----------------------
    Attribute errors or unstructured failures would violate operational translation.

    Limitations
    -----------
    The underlying issue list is covered separately.
    """
    marking = cpn.CpnMarking(
        1, executable_net.model_id, 0, (cpn.PlaceMarking("ready", ()),)
    )
    with pytest.raises(cpn.CpnMarkingError) as error:
        cpn.TransitionEnabler().execute(executable_net, marking, "execute")
    assert error.value.detail.code is cpn.CpnErrorCode.INVALID_MARKING


def test_cpn_sv_p1_026_invalid_definition_translates_to_structured_error(
    executable_net: cpn.CpnNetDefinition,
) -> None:
    """SV-CPN-026: operational translation of an invalid definition.

    Requirement
    -----------
    The version-1 P1 contract requires operational translation of an invalid
    definition.

    Method
    ------
    Replace one place's allowed colors with unknown ``missing`` and call
    ``TransitionEnabler.execute``.

    Independent oracle
    ------------------
    Cross-object definition validation independently reports the unknown color
    reference.

    Acceptance criterion
    --------------------
    The ActionObject raises ``CpnDefinitionError`` with code ``INVALID_DEFINITION``.

    Failure interpretation
    ----------------------
    Success or an unrelated exception means invalid definitions bypass structured
    translation.

    Limitations
    -----------
    This is definition software verification, not a physical model check.
    """
    bad_place = replace(executable_net.places[0], allowed_color_ids=("missing",))
    bad_net = replace(executable_net, places=(bad_place,) + executable_net.places[1:])
    with pytest.raises(cpn.CpnDefinitionError) as error:
        cpn.TransitionEnabler().execute(bad_net, bad_net.initial_marking, "execute")
    assert error.value.detail.code is cpn.CpnErrorCode.INVALID_DEFINITION
