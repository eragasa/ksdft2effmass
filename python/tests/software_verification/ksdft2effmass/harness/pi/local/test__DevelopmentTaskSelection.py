r"""Software verification of ``DevelopmentTaskSelection``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies minimal immutable development Task selection facts.

Intrinsic and cross-object scope

The sole primary SUT is ``DevelopmentTaskSelection``. Intrinsic field, identifier,
ordering, uniqueness, and disabled-successor invariants are covered. Selected-Task
existence and receipt interpretation remain outside the DataObject.

VVUQ and scientific exclusions

Passing establishes software-contract behavior only. It grants no development or
protected authority and represents no scientific CPN or Workflow state.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness import DevelopmentTaskSelection

pytestmark = pytest.mark.software_verification
SUT = DevelopmentTaskSelection


def test_constructor__fields__retains_exact_immutable_inactive_state() -> None:
    """Evidence ID: SV-HT-104

    Requirement: Version 1 represents no active Task, no activation receipts, and
    disabled automatic successor activation as exact immutable state.

    Method: Construct the canonical inactive value and attempt field reassignment.

    Oracle: The accepted minimal selection-state contract fixes all four fields.

    Acceptance: Fields equal the exact inactive tuple and reassignment raises
    ``FrozenInstanceError``.

    Interpretation: Failure identifies field or immutability drift.

    Limitations: Inactive state does not establish completion or authorization.
    """
    selection = SUT(1, None, (), False)
    assert selection.schema_version == 1
    assert selection.active_task_id is None
    assert selection.explicit_activation_receipt_ids == ()
    assert selection.automatic_successor_activation is False
    with pytest.raises(FrozenInstanceError):
        selection.active_task_id = "task"  # type: ignore[misc]


def test_constructor__fields__retains_active_and_receipt_references() -> None:
    """Evidence ID: SV-HT-105

    Requirement: Selection may reference one Task and sorted unique activation receipt
    identities without embedding or interpreting either record.

    Method: Construct an active-reference value with two explicit receipt identities.

    Oracle: The DataObject field contract defines exact reference preservation.

    Acceptance: Active and receipt identities equal the supplied built-in strings.

    Interpretation: Failure identifies unwanted normalization or embedded authority.

    Limitations: Referenced records are synthetic and their existence is not checked.
    """
    selection = SUT(1, "task.active", ("receipt.a", "receipt.b"), False)
    assert selection.active_task_id == "task.active"
    assert selection.explicit_activation_receipt_ids == ("receipt.a", "receipt.b")


def test_constructor__invariants__rejects_invalid_types_order_and_policy() -> None:
    """Evidence ID: SV-HT-106

    Requirement: Wrong semantic types, invalid identifiers, unordered or duplicate
    receipts, and enabled automatic succession are rejected.

    Method: Construct independently invalid values at each intrinsic boundary.

    Oracle: The public constructor contract fixes exception taxonomy and disabled
    policy.

    Acceptance: Wrong types raise ``TypeError`` and value invariants raise
    ``ValueError``.

    Interpretation: Failure identifies coercion or an activation-policy escape.

    Limitations: Cross-record selection consistency belongs to a later validator.
    """
    with pytest.raises(TypeError):
        SUT(1, 1, (), False)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT(1, "bad/id", (), False)
    with pytest.raises(TypeError, match="tuple"):
        SUT(1, None, [], False)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="unique and strictly sorted"):
        SUT(1, None, ("receipt.b", "receipt.a"), False)
    with pytest.raises(ValueError, match="unique and strictly sorted"):
        SUT(1, None, ("receipt.a", "receipt.a"), False)
    with pytest.raises(TypeError, match="bool"):
        SUT(1, None, (), 0)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must be false"):
        SUT(1, None, (), True)
