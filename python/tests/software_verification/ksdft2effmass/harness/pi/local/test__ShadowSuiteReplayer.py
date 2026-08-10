r"""Software verification of ``ShadowSuiteReplayer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies fail-closed aggregation of already supplied shadow-pair results.

Intrinsic and cross-object scope

``ShadowSuiteReplayer`` owns aggregation; ``ShadowPairComparator`` supplies setup
results.

VVUQ and scientific exclusions

Passing establishes represented replay behavior only, not scientific validation or UQ.
"""

import pytest

from ksdft2effmass.harness.pi.local import (
    ShadowObservation,
    ShadowPairComparator,
    ShadowSuiteReplayer,
)

from .conftest import local_context, repository_root

pytestmark = pytest.mark.software_verification
SUT = ShadowSuiteReplayer


def observation(name: str, inventory: tuple[str, ...] = ()) -> ShadowObservation:
    """Evidence ID: Owns no identifier; supports SV-HL-012.

    Requirement: Replay evidence requires explicit immutable observation inputs.

    Method: Construct one passing observation from a name and literal inventory.

    Oracle: The supplied arguments exactly determine the setup record.

    Acceptance: Return the corresponding ``ShadowObservation`` unchanged by policy.

    Interpretation: Failure indicates controlled setup drift.

    Limitations: This helper owns no independent evidence claim.
    """
    return ShadowObservation(name, "PASS", (), (), inventory, 0, None)


def test_method__execute__fails_closed_for_defect_and_deferred_pairs() -> None:
    """Evidence ID: SV-HL-012

    Requirement: Aggregation sorts pairs and fails when any pair is defect or deferred.

    Method: Aggregate one equivalent, one defect, and one cited deferred supplied
    result.

    Oracle: H4 prohibits authoritative routing for defect or deferred comparisons.

    Acceptance: Pair IDs are ``a,b,c``; status is FAIL; issue codes are exactly defect
    and deferred.

    Interpretation: Failure indicates unsafe aggregation or ordering drift.

    Limitations: No command is launched; scientific validity, numerical verification,
    and UQ are excluded.
    """
    comparator = ShadowPairComparator()
    base = observation("legacy")
    defect = comparator.execute("b", base, observation("local", ("x",)))
    deferred = comparator.execute(
        "c",
        base,
        observation("local", ("y",)),
        (("inventory", "deferred", "pending profile handoff"),),
    )
    equivalent = comparator.execute("a", base, observation("local"))
    result = ShadowSuiteReplayer().execute(
        (deferred, defect, equivalent),
        repository_root(),
        local_context(),
        "label:H4-current-tree",
    )
    assert [item.pair_id for item in result.pairs] == ["a", "b", "c"]
    assert result.validation.status == "FAIL"
    assert {item.code for item in result.validation.issues} == {
        "PIHL.SHADOW.DEFECT",
        "PIHL.SHADOW.DEFERRED",
    }
