r"""Software verification of ``_HarnessProjectionSyncResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_HarnessProjectionSyncResult``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness.pi.local.dbcontrol.records import (
    _HarnessProjectionSyncResult,
)

SUT = _HarnessProjectionSyncResult

pytestmark = pytest.mark.software_verification


def test_field__nested_state__is_immutable() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-result.nested-state-is-immutable

    Requirement: Migration results expose immutable tuples for counts, issues, and paths.

    Method: Construct the private result and attempt field reassignment.

    Oracle: A frozen dataclass rejects private field reassignment.

    Acceptance: Exact tuple state is retained and reassignment raises ``FrozenInstanceError``.

    Interpretation: Failure indicates mutable migration evidence or an incorrect record boundary.

    Limitations: The test does not establish that represented counts came from a migration.
    """  # noqa: E501
    result = _HarnessProjectionSyncResult(1, "a" * 64, (("tasks", 1),), (), ("x",))
    assert result.counts == (("tasks", 1),)
    with pytest.raises(FrozenInstanceError):
        result.schema_version = 2  # type: ignore[misc]
