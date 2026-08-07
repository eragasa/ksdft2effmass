r"""Software verification of local routing and shadow.

Facet and represented meaning
Software verification of explicit routing, rollback, shadow comparison ordering, and
fail-closed replay aggregation.

Intrinsic and cross-object scope
The artifact owner is the local shadow-routing boundary; exact route truth tables and
difference classifications come from accepted H4 behavior.

VVUQ and scientific exclusions
Passing establishes deterministic software routing only, not numerical verification,
scientific validation, UQ, physical correctness, or cross-language conformance.
"""

from typing import Any

import pytest

from ksdft2effmass.harness.pi.local import (
    CompareShadowPair,
    ReplayShadowSuite,
    RollBackValidationRoute,
    RouteConfiguration,
    SelectValidationRoute,
    ShadowObservation,
    ValidationRoute,
)

from .conftest import local_context, repository_root

pytestmark = pytest.mark.software_verification


def observation(
    name: str,
    *,
    status: str = "PASS",
    exit_status: int = 0,
    inventory: tuple[str, ...] = (),
) -> ShadowObservation:
    """Evidence ID
    Owns no identifier; supports SV-HL-009.
    Requirement
    Provide explicit setup mechanics for the local routing and shadow evidence without
    owning an independent result.
    Method
    Construct the named public input partition and invoke the declared owner without
    ambient discovery.
    Oracle
    The fixed public contract and literal record partition determine the exact expected
    result independently.
    Acceptance
    The named exact value, ordering, issue, or exception partition must hold without
    tolerance.
    Interpretation
    Failure identifies public-contract drift, stale controlled input, or an
    implementation defect.
    Limitations
    This is deterministic software verification only; numerical verification, scientific
    validation, UQ, physical correctness, portability, and cross-language claims are
    excluded.
    """
    return ShadowObservation(name, status, (), (), inventory, exit_status, None)


def test_method__route_selection__implements_truth_table_and_legacy_rollback() -> None:
    """Evidence ID
    SV-HL-009
    Requirement
    Legacy, shadow, and local routes have an explicit truth table and every rollback
    selects retained legacy authority.
    Method
    Execute SelectValidationRoute for all enum members and RollBackValidationRoute from
    local and shadow configurations.
    Oracle
    The H4 routing contract fixes legacy=(1,0,legacy), shadow=(1,1,legacy),
    local=(0,1,local).
    Acceptance
    Returned booleans and authority exactly match the table and rollback always returns
    legacy/legacy.
    Interpretation
    Failure indicates unsafe authority selection or rollback regression.
    Limitations
    No command is executed and operational deployment, science, numerical results, UQ,
    and portability are excluded.
    """
    action = SelectValidationRoute()
    actual = {
        route: action.execute(RouteConfiguration(route)) for route in ValidationRoute
    }
    assert (
        actual[ValidationRoute.LEGACY].run_legacy,
        actual[ValidationRoute.LEGACY].run_local,
        actual[ValidationRoute.LEGACY].authoritative_route,
    ) == (True, False, ValidationRoute.LEGACY)
    assert (
        actual[ValidationRoute.SHADOW].run_legacy,
        actual[ValidationRoute.SHADOW].run_local,
        actual[ValidationRoute.SHADOW].authoritative_route,
    ) == (True, True, ValidationRoute.LEGACY)
    assert (
        actual[ValidationRoute.LOCAL].run_legacy,
        actual[ValidationRoute.LOCAL].run_local,
        actual[ValidationRoute.LOCAL].authoritative_route,
    ) == (False, True, ValidationRoute.LOCAL)

    def exercise_route_case_90_1(route: Any) -> Any:
        rolled = RollBackValidationRoute().execute(RouteConfiguration(route))
        assert rolled.route is rolled.rollback_route is ValidationRoute.LEGACY

    _ = [
        exercise_route_case_90_1(route)
        for route in ((ValidationRoute.SHADOW, ValidationRoute.LOCAL))
    ]


def test_method__shadow_classification__orders_differences_and_citations() -> None:
    """Evidence ID
    SV-HL-010
    Requirement
    Every normalized difference is lexically ordered and classified equivalent, cited
    intentional/deferred, or uncited defect.
    Method
    Compare equal observations, one approved inventory difference, one uncited
    difference, and simultaneous status/exit differences.
    Oracle
    CompareShadowPair and ShadowPairResult publicly require sorted difference keys and
    explicit authority for nondefect exceptions.
    Acceptance
    Equal is equivalent; cited inventory is intentional; uncited inventory is defect;
    simultaneous keys return the sorted tuple (exit_status, status) without raising.
    Interpretation
    Failure identifies classification/order defects or stale accepted-rule
    transcription.
    Limitations
    Rule authority authenticity is represented by a fixed citation string; commands,
    science, numerical verification, UQ, and portability are excluded.
    """
    compare = CompareShadowPair()
    base = observation("legacy")
    assert (
        compare.execute("equal", base, observation("local")).classification
        == "equivalent"
    )
    intentional = compare.execute(
        "i",
        base,
        observation("local", inventory=("x",)),
        (("inventory", "intentional", "H4 canonical rename"),),
    )
    assert intentional.classification == "intentional"
    assert (
        compare.execute(
            "d", base, observation("local", inventory=("x",))
        ).classification
        == "defect"
    )
    ordered = compare.execute(
        "order", base, observation("local", status="FAIL", exit_status=1)
    )
    assert ordered.differences == ("exit_status", "status")


def test_method__shadow_rules__reject_uncited_or_mixed_exceptions() -> None:
    """Evidence ID
    SV-HL-011
    Requirement
    Exception rules cannot silently waive defects and mixed classifications cannot
    become authoritative.
    Method
    Supply an empty citation, an illegal equivalent rule, and mixed intentional/deferred
    rules for two differences.
    Oracle
    The public rule contract permits only cited intentional/deferred triples and
    requires one classification for every observed difference.
    Acceptance
    Invalid rules raise ValueError and mixed rules produce defect.
    Interpretation
    Failure indicates silent waiver or permissive authoritative routing.
    Limitations
    Citation governance beyond nonempty representation, science, numerical verification,
    UQ, and portability are excluded.
    """
    compare = CompareShadowPair()
    base = observation("legacy")
    with pytest.raises(ValueError):
        compare.execute(
            "x",
            base,
            observation("local", inventory=("x",)),
            (("inventory", "intentional", ""),),
        )
    with pytest.raises(ValueError):
        compare.execute(
            "x",
            base,
            observation("local", inventory=("x",)),
            (("inventory", "equivalent", "authority"),),
        )
    local = ShadowObservation(
        "local",
        "PASS",
        (("CODE", "ERROR", None, None, ()),),
        (("state", ("x",)),),
        (),
        0,
        None,
    )
    result = compare.execute(
        "x",
        base,
        local,
        (("issue_facts", "deferred", "A"), ("state_facts", "intentional", "B")),
    )
    assert result.classification == "defect"


def test_workflow__shadow_replay__fails_closed_for_defect_and_deferred() -> None:
    """Evidence ID
    SV-HL-012
    Requirement
    Replay sorts pairs and prevents defect or deferred observations from passing
    authoritative assessment.
    Method
    Aggregate one equivalent, one defect, and one cited deferred pair against the
    explicit current-tree root and context.
    Oracle
    H4 excludes defect/deferred authoritative routing and fixes PIHL.SHADOW
    classification diagnostics.
    Acceptance
    Pair IDs sort lexically, validation is FAIL, and issue codes are exactly
    PIHL.SHADOW.DEFECT and PIHL.SHADOW.DEFERRED.
    Interpretation
    Failure indicates unsafe aggregation, order drift, or context-fixture error.
    Limitations
    External commands are represented rather than launched; scientific, numerical, UQ,
    and portability conclusions are excluded.
    """
    compare = CompareShadowPair()
    base = observation("legacy")
    defect = compare.execute("b", base, observation("local", inventory=("x",)))
    deferred = compare.execute(
        "c",
        base,
        observation("local", inventory=("y",)),
        (("inventory", "deferred", "pending profile handoff"),),
    )
    equal = compare.execute("a", base, observation("local"))
    result = ReplayShadowSuite().execute(
        (deferred, defect, equal),
        repository_root(),
        local_context(),
        "label:H4-current-tree",
    )
    assert [x.pair_id for x in result.pairs] == ["a", "b", "c"]
    assert result.validation.status == "FAIL"
    assert {x.code for x in result.validation.issues} == {
        "PIHL.SHADOW.DEFECT",
        "PIHL.SHADOW.DEFERRED",
    }
