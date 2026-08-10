r"""Software verification of ``CpnMarkingValidator``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

--------------------------------------
This module provides software-verification evidence for the public
``CpnMarkingValidator`` software surface and its finite, exact CPN routing
representation. It does not represent a physical observable or numerical approximation.

Intrinsic and cross-object scope

--------------------------------
``CpnMarkingValidator`` is the sole primary SUT. Tests exercise its documented public
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


def test_method__execute__accepts_complete_multiset_marking(
    token_factory: Callable[..., CpnToken], executable_net: CpnNetDefinition
) -> None:
    """Evidence ID: SV-CPN-036

    Requirement: accept a complete two-token multiset marking.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: accept a complete two-token multiset
    marking. Requirement: validation preserves multiplicity rather than collapsing a
    place to Boolean occupancy. Method: validate a complete marking containing two
    independently identified work tokens. Oracle: every place exists, both token colors
    are admitted, and identities are unique. Acceptance: ``is_valid`` is true. Failure
    means a contract-valid multiset was rejected. Limitation: durable marking storage
    and reachability are excluded.

    Oracle: The documented public rule that the SUT must accept a complete two-token
    multiset
    marking is the contract oracle; fixed synthetic values, Python exact type/value
    semantics, and the public error taxonomy provide independently inspectable expected
    outcomes where used.

    Acceptance: Every preserved exact equality, identity, ordering, representation, and
    expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation: Pass supports only this named software contract. Failure may
    indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations: The case excludes unexercised inputs and dependencies, physical
    conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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


def test_method__execute__wrong_complete_place_set_has_stable_code(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID: SV-CPN-013

    Requirement: complete place-set validation.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: complete place-set validation. Prior
    requirement detail: The version-1 P1 contract requires complete place-set
    validation. Prior method detail: Validate a marking containing only the ``ready``
    place against the three-place executable net. Prior independent oracle detail: Set
    comparison with the net's declared places independently shows authorization and
    completed are absent. Prior acceptance criterion detail: The result contains
    authoritative code ``PLACE_SET_MISMATCH``. Prior failure interpretation detail:
    Absence of that code means incomplete markings can pass compatibility validation.
    Prior limitations detail: This case does not test token colors.

    Oracle: The documented public rule that the SUT must complete place-set validation
    is the
    contract oracle; fixed synthetic values, Python exact type/value semantics, and the
    public error taxonomy provide independently inspectable expected outcomes where
    used.

    Acceptance: Every preserved exact equality, identity, ordering, representation, and
    expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation: Pass supports only this named software contract. Failure may
    indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations: The case excludes unexercised inputs and dependencies, physical
    conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
    marking = CpnMarking(1, executable_net.model_id, 0, (PlaceMarking("ready", ()),))
    result = CpnMarkingValidator().execute(executable_net, marking)
    assert CpnIssueCode.PLACE_SET_MISMATCH in {issue.code for issue in result.issues}


def test_method__execute__unknown_color_reference_is_structured(
    executable_net: CpnNetDefinition,
) -> None:
    """Evidence ID: SV-CPN-014

    Requirement: structured unknown-color diagnostics.

    Method: Exercise the primary SUT through the public construction or operation
    boundary using
    the synthetic valid and controlled-invalid inputs retained in the executable body.
    The prior scenario documentation states: structured unknown-color diagnostics. Prior
    requirement detail: The version-1 P1 contract requires structured unknown-color
    diagnostics. Prior method detail: Construct a token with color ``unknown`` in
    ``ready`` and call ``CpnMarkingValidator.execute``. Prior independent oracle detail:
    The net color registry lacks ``unknown`` and the ready place admits only ``work``.
    Prior acceptance criterion detail: Both ``UNKNOWN_COLOR`` and
    ``TOKEN_COLOR_MISMATCH`` occur in the issue-code set. Prior failure interpretation
    detail: Missing either code loses global-color or place-color diagnostic coverage.
    Prior limitations detail: The test does not infer payload or physical type
    compatibility.

    Oracle: The documented public rule that the SUT must structured unknown-color
    diagnostics is
    the contract oracle; fixed synthetic values, Python exact type/value semantics, and
    the public error taxonomy provide independently inspectable expected outcomes where
    used.

    Acceptance: Every preserved exact equality, identity, ordering, representation, and
    expected
    exception type, message, or code assertion must hold. No approximate tolerance or
    warning is accepted unless the preserved executable case explicitly states one.

    Interpretation: Pass supports only this named software contract. Failure may
    indicate a production
    implementation defect, invalid synthetic fixture, oracle transcription error,
    environment issue, or inconsistency in the documented public contract.

    Limitations: The case excludes unexercised inputs and dependencies, physical
    conclusions,
    numerical verification, scientific validation, uncertainty quantification,
    persistence and engine-adapter behavior, and cross-language conformance."""
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
