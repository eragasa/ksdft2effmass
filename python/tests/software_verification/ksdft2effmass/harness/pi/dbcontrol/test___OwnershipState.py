r"""Software verification of ``_OwnershipState``.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_OwnershipState``.

Intrinsic and cross-object scope

Only the object's bounded contract is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness.pi.dbcontrol.documents import _OwnershipState

SUT = _OwnershipState

pytestmark = pytest.mark.software_verification


def test_field__immutable_state__rejects_reassignment() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.ownership-state.field.immutable

    Requirement: Parsed ownership state is operationally immutable.

    Method: Construct literal state and attempt field reassignment.

    Oracle: Frozen dataclass semantics reject assignment.

    Acceptance: Reassignment raises exactly ``FrozenInstanceError``.

    Interpretation: Failure indicates mutable inspection evidence.

    Limitations: Ownership parsing is excluded.
    """  # noqa: E501
    value = _OwnershipState("check.py", ("python", "check.py"), (), ())
    with pytest.raises(FrozenInstanceError):
        value.completion_path = "other.py"  # type: ignore[misc]
