r"""Software verification of ``HarnessConfigurationResolutionResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies the immutable closed outcome of exact-source harness configuration
resolution.

Intrinsic and cross-object scope

``HarnessConfigurationResolutionResult`` is the sole system under test. Configuration
resolution, source parsing, and snapshot construction are owned separately.

VVUQ and scientific exclusions

This is software verification only. It establishes no filesystem availability,
authority, scientific validity, protected execution, or human acceptance.
"""

from typing import cast

import pytest

from ksdft2effmass.harness import (
    HarnessConfigurationResolutionFinding,
    HarnessConfigurationResolutionResult,
    HarnessConfigurationSourceBinding,
)

pytestmark = pytest.mark.software_verification
SUT = HarnessConfigurationResolutionResult


def test_constructor__source_bindings__rejects_wrong_member_type() -> None:
    """Evidence ID: software-verification.harness-configuration.result.source-binding-member-type

    Requirement: Source bindings contain only exact
    ``HarnessConfigurationSourceBinding`` values, and a wrong member type is a semantic
    type error.

    Method: Construct a failed result with one valid finding and an ``object`` cast only
    across the static type boundary as the sole source-binding member.

    Oracle: The public constructor contract requires exact binding value types before
    role-order validation can inspect binding fields.

    Acceptance: Construction raises ``TypeError`` with the stable wrong-member message
    rather than leaking ``AttributeError`` from role access.

    Interpretation: Failure indicates that malformed public input bypasses its owning
    type-validation boundary.

    Limitations: Valid binding order and complete resolved/failed partitions are covered
    by the configuration contract integration module.
    """  # noqa: E501
    finding = HarnessConfigurationResolutionFinding(
        "HARNESS_CONFIGURATION.SOURCE_INVALID",
        "harness/configuration.json",
        "Harness configuration source is invalid.",
    )
    wrong_binding = cast(HarnessConfigurationSourceBinding, object())

    with pytest.raises(TypeError, match="source_bindings contain a wrong value type"):
        SUT(1, "failed", (wrong_binding,), None, None, (finding,))
