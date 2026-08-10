r"""Software verification of ``ChainStateEvaluator``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of the public ``ChainStateEvaluator`` surface; no physical model,
mathematical operator, or numerical representation is represented.

Intrinsic and cross-object scope

The sole primary SUT is ``ChainStateEvaluator``.  Accepted H1 field/wire contracts and
read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions

Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.harness.pi import ChainStateEvaluator

pytestmark = pytest.mark.software_verification
SUT = ChainStateEvaluator


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID: SV-HARNESS-032

    Requirement: ChainStateEvaluator is a concrete stateless ActionObject.

    Method: Construct two instances and inspect their public storage boundary.

    Oracle: The accepted H1 action contract requires no retained root, profile, cache,
    client, or mutable state.

    Acceptance: Construction succeeds and instances expose no instance dictionary or
    slots
    containing fields.

    Interpretation: A failure identifies a production, accepted-contract, fixture, or
    environment
    discrepancy requiring independent review.

    Limitations: This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    action = SUT()
    assert not hasattr(action, "__dict__")
    assert SUT.__slots__ == ()


def test_method__execute_valid_and_invalid__returns_exact_partition() -> None:
    """Evidence ID: SV-HARNESS-056

    Requirement: The public action executes one valid and one major invalid partition.

    Method: Invoke execute directly with accepted records and a controlled invalid
    input.

    Oracle: Accepted H1 action semantics and H3 fixtures fix the exact result partition.

    Acceptance: Valid output is exact; invalid output has the expected code and no
    partial value.

    Interpretation: Failure identifies action-contract drift requiring independent
    review.

    Limitations: This is deterministic software verification, not scientific validation
    or UQ.
    """

    from pathlib import Path

    from ksdft2effmass.harness.pi import (
        ChainView,
        JsonRecordDeserializer,
        ProjectProfile,
        WireRecordKind,
    )

    root = Path(__file__).resolve().parents[6]

    def load(kind: WireRecordKind, name: str) -> object:
        result = JsonRecordDeserializer().execute(
            kind, (root / f"harness/pi/fixtures/valid/{name}.json").read_bytes()
        )
        assert result.record is not None
        return result.record

    chain = load(WireRecordKind.ChainView, "chain-view")
    profile = load(WireRecordKind.ProjectProfile, "project-profile")
    assert isinstance(chain, ChainView) and isinstance(profile, ProjectProfile)
    valid = SUT().execute(chain, (), (), (), profile)
    assert valid.validation.status == "PASS" and valid.active_task_ids == ("T1",)
    invalid = SUT().execute(chain, (), (), ("unknown",), profile)
    assert (
        invalid.active_task_ids
        == invalid.blocked_task_ids
        == invalid.ready_task_ids
        == ()
    )
    assert [issue.code for issue in invalid.validation.issues] == [
        "PIH.CHAIN.PREREQUISITE_MISSING"
    ]
