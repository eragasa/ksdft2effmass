"""Software verification for ``CpnMarkingValidator`` as the sole primary SUT.

Evidence class: software verification. Requirement and strategy are stated per
case; public construction/execution supplies the method and exact state or the
documented exception taxonomy supplies the independent oracle. Passing verifies
only the named class contract. It does not provide numerical verification,
scientific validation, uncertainty quantification, persistence, SNAKES-adapter,
Rust-conformance, or scientific-execution evidence. Collaborators are synthetic
setup only.
"""

from collections.abc import Callable

import pytest

from ksdft2effmass.workflows.cpn import (
    CpnIssueCode,
    CpnMarking,
    CpnMarkingValidator,
    CpnNetDefinition,
    CpnToken,
    PlaceMarking,
)

pytestmark = pytest.mark.software_verification

SUT = CpnMarkingValidator


def test_cpn_sv_p1_036_accepts_complete_multiset_marking(
    token_factory: Callable[..., CpnToken], executable_net: CpnNetDefinition
) -> None:
    """SV-CPN-036: accept a complete two-token multiset marking.

    Requirement: validation preserves multiplicity rather than collapsing a place
    to Boolean occupancy. Method: validate a complete marking containing two
    independently identified work tokens. Oracle: every place exists, both token
    colors are admitted, and identities are unique. Acceptance: ``is_valid`` is
    true. Failure means a contract-valid multiset was rejected. Limitation: durable
    marking storage and reachability are excluded.
    """
    marking = CpnMarking(
        1,
        executable_net.model_id,
        0,
        (
            PlaceMarking("ready", (token_factory("work-b"), token_factory("work-a"))),
            PlaceMarking("completed", ()),
            PlaceMarking("authorization", (token_factory("auth", "authorization"),)),
        ),
    )
    assert CpnMarkingValidator().execute(executable_net, marking).is_valid


def test_cpn_sv_p1_013_wrong_complete_place_set_has_stable_code(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-013: complete place-set validation.

    Requirement
    -----------
    The version-1 P1 contract requires complete place-set validation.

    Method
    ------
    Validate a marking containing only the ``ready`` place against the three-place
    executable net.

    Independent oracle
    ------------------
    Set comparison with the net's declared places independently shows authorization
    and completed are absent.

    Acceptance criterion
    --------------------
    The result contains authoritative code ``PLACE_SET_MISMATCH``.

    Failure interpretation
    ----------------------
    Absence of that code means incomplete markings can pass compatibility
    validation.

    Limitations
    -----------
    This case does not test token colors.
    """
    marking = CpnMarking(1, executable_net.model_id, 0, (PlaceMarking("ready", ()),))
    result = CpnMarkingValidator().execute(executable_net, marking)
    assert CpnIssueCode.PLACE_SET_MISMATCH in {issue.code for issue in result.issues}


def test_cpn_sv_p1_014_unknown_color_reference_is_structured(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-014: structured unknown-color diagnostics.

    Requirement
    -----------
    The version-1 P1 contract requires structured unknown-color diagnostics.

    Method
    ------
    Construct a token with color ``unknown`` in ``ready`` and call
    ``CpnMarkingValidator.execute``.

    Independent oracle
    ------------------
    The net color registry lacks ``unknown`` and the ready place admits only
    ``work``.

    Acceptance criterion
    --------------------
    Both ``UNKNOWN_COLOR`` and ``TOKEN_COLOR_MISMATCH`` occur in the issue-code set.

    Failure interpretation
    ----------------------
    Missing either code loses global-color or place-color diagnostic coverage.

    Limitations
    -----------
    The test does not infer payload or physical type compatibility.
    """
    token = executable_net.initial_marking.places[2].tokens[0]
    wrong = CpnToken(
        token.token_id,
        "unknown",
        token.workflow_id,
        token.run_id,
        token.parent_run_id,
        token.attempt_id,
        token.retry_parent_attempt_id,
        token.iteration_index,
        token.payload_type_id,
        token.payload_id,
        token.payload_schema_version,
        token.provenance_ids,
        token.parent_token_ids,
        token.correlation_id,
        token.authorization_id,
        token.outcome,
    )
    places = tuple(
        PlaceMarking(
            place.place_id, (wrong,) if place.place_id == "ready" else place.tokens
        )
        for place in executable_net.initial_marking.places
    )
    result = CpnMarkingValidator().execute(
        executable_net, CpnMarking(1, executable_net.model_id, 0, places)
    )
    codes = {issue.code for issue in result.issues}
    assert {CpnIssueCode.UNKNOWN_COLOR, CpnIssueCode.TOKEN_COLOR_MISMATCH} <= codes
