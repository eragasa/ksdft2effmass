r"""Software verification of ``ValidationRouteSelector``.

Facet and represented meaning

The module verifies deterministic route-selection truth-table behavior.

Intrinsic and cross-object scope

``ValidationRouteSelector`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes software routing behavior only, not scientific validation or UQ.
"""

import pytest

from ksdft2effmass.harness.pi.local import (
    RouteConfiguration,
    ValidationRoute,
    ValidationRouteSelector,
)

pytestmark = pytest.mark.software_verification
SUT = ValidationRouteSelector


def test_method__execute__implements_exact_route_truth_table() -> None:
    """Evidence ID: SV-HL-009

    Requirement: Legacy, shadow, and local configurations map to the accepted run and
    authority facts.

    Method: Execute the selector for every closed ``ValidationRoute`` member.

    Oracle: The accepted table is legacy=(1,0,legacy), shadow=(1,1,legacy),
    local=(0,1,local).

    Acceptance: Every returned tuple equals its exact table row.

    Interpretation: Failure indicates unsafe authority selection or table drift.

    Limitations: No command is executed; deployment, scientific validity, and UQ are
    excluded.
    """
    selector = ValidationRouteSelector()
    actual = {
        route: selector.execute(RouteConfiguration(route)) for route in ValidationRoute
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
