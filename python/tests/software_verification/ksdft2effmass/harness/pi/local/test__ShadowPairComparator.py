r"""Software verification of ``ShadowPairComparator``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies classification and ordering of supplied shadow observations.

Intrinsic and cross-object scope

``ShadowPairComparator`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes represented comparison behavior only, not scientific validation or
UQ.
"""

import pytest

from ksdft2effmass.harness.pi.local import ShadowObservation, ShadowPairComparator

pytestmark = pytest.mark.software_verification
SUT = ShadowPairComparator


def observation(
    name: str,
    *,
    status: str = "PASS",
    exit_status: int = 0,
    inventory: tuple[str, ...] = (),
) -> ShadowObservation:
    """Evidence ID: Owns no identifier; supports SV-HL-010 and SV-HL-011.

    Requirement: Comparator tests require explicit immutable observation inputs.

    Method: Construct one public observation from literal supplied fields.

    Oracle: The supplied arguments exactly determine the setup record.

    Acceptance: Return the corresponding ``ShadowObservation`` unchanged by policy.

    Interpretation: Failure indicates controlled setup drift.

    Limitations: This helper owns no independent evidence claim.
    """
    return ShadowObservation(name, status, (), (), inventory, exit_status, None)


def test_method__execute__orders_differences_and_applies_cited_classification() -> None:
    """Evidence ID: SV-HL-010

    Requirement: Differences are sorted and classified as equivalent, cited intentional,
    or defect.

    Method: Compare equal, cited inventory, uncited inventory, and simultaneous
    status/exit cases.

    Oracle: The public comparison contract requires lexical keys and authority for
    exceptions.

    Acceptance: Classifications and the ``("exit_status", "status")`` ordering match
    exactly.

    Interpretation: Failure indicates ordering or classification drift.

    Limitations: Citation authenticity, command execution, scientific validity, and UQ
    are excluded.
    """
    comparator = ShadowPairComparator()
    base = observation("legacy")
    assert (
        comparator.execute("equal", base, observation("local")).classification
        == "equivalent"
    )
    intentional = comparator.execute(
        "intentional",
        base,
        observation("local", inventory=("x",)),
        (("inventory", "intentional", "H4 canonical rename"),),
    )
    assert intentional.classification == "intentional"
    assert (
        comparator.execute(
            "defect", base, observation("local", inventory=("x",))
        ).classification
        == "defect"
    )
    ordered = comparator.execute(
        "ordered", base, observation("local", status="FAIL", exit_status=1)
    )
    assert ordered.differences == ("exit_status", "status")


def test_method__execute__rejects_uncited_rules_and_mixed_exceptions() -> None:
    """Evidence ID: SV-HL-011

    Requirement: Exception rules cannot waive defects without citations or mix
    classifications.

    Method: Supply an empty citation, an illegal equivalent rule, and mixed valid
    exception rules.

    Oracle: The public rule contract permits only cited intentional or deferred
    classifications.

    Acceptance: Invalid rules raise ``ValueError`` and mixed rules yield ``defect``.

    Interpretation: Failure indicates a silent waiver or permissive authority decision.

    Limitations: Citation governance, command execution, scientific validity, and UQ are
    excluded.
    """
    comparator = ShadowPairComparator()
    base = observation("legacy")
    with pytest.raises(ValueError):
        comparator.execute(
            "empty",
            base,
            observation("local", inventory=("x",)),
            (("inventory", "intentional", ""),),
        )
    with pytest.raises(ValueError):
        comparator.execute(
            "illegal",
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
    result = comparator.execute(
        "mixed",
        base,
        local,
        (("issue_facts", "deferred", "A"), ("state_facts", "intentional", "B")),
    )
    assert result.classification == "defect"
