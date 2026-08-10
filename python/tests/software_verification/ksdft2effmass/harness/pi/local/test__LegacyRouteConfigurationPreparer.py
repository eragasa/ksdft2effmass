r"""Software verification of ``LegacyRouteConfigurationPreparer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies preparation of the retained legacy route configuration.

Intrinsic and cross-object scope

``LegacyRouteConfigurationPreparer`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes software routing behavior only, not scientific validation or UQ.
"""

import pytest

from ksdft2effmass.harness.pi.local import (
    LegacyRouteConfigurationPreparer,
    RouteConfiguration,
    ValidationRoute,
)

pytestmark = pytest.mark.software_verification
SUT = LegacyRouteConfigurationPreparer


def test_method__execute__returns_retained_legacy_route() -> None:
    """Evidence ID: SV-HL-019

    Requirement: Every nonlegacy input produces the retained legacy configuration.

    Method: Execute the preparer with local and shadow route configurations.

    Oracle: The accepted rollback contract fixes ``RouteConfiguration(LEGACY)``.

    Acceptance: Both results equal that exact immutable configuration.

    Interpretation: Failure indicates route preparation or retained-authority drift.

    Limitations: No command is executed; deployment, scientific validity, and UQ are
    excluded.
    """
    preparer = LegacyRouteConfigurationPreparer()
    expected = RouteConfiguration(ValidationRoute.LEGACY)
    assert preparer.execute(RouteConfiguration(ValidationRoute.LOCAL)) == expected
    assert preparer.execute(RouteConfiguration(ValidationRoute.SHADOW)) == expected
