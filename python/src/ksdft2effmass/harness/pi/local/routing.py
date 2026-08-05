"""Explicit controlled route selection and rollback."""

from __future__ import annotations

from dataclasses import dataclass

from .models import RouteConfiguration, ValidationRoute

_ROUTE_TRUTH_TABLE = {
    ValidationRoute.LEGACY: (True, False, ValidationRoute.LEGACY),
    ValidationRoute.SHADOW: (True, True, ValidationRoute.LEGACY),
    ValidationRoute.LOCAL: (False, True, ValidationRoute.LOCAL),
}


@dataclass(frozen=True, slots=True)
class RouteSelection:
    """Pure route decision for caller-owned legacy and local implementations.

    The three fields must be exactly one row of the public legacy/shadow/local
    truth table. A caller cannot construct a contradictory authority decision.
    """

    run_legacy: bool
    run_local: bool
    authoritative_route: ValidationRoute

    def __post_init__(self) -> None:
        if type(self.run_legacy) is not bool or type(self.run_local) is not bool:
            raise TypeError("run flags must be bool")
        if type(self.authoritative_route) is not ValidationRoute:
            raise TypeError("authoritative_route must be ValidationRoute")
        candidate = (self.run_legacy, self.run_local, self.authoritative_route)
        if candidate not in _ROUTE_TRUTH_TABLE.values():
            raise ValueError("route selection is absent from the exact truth table")


class SelectValidationRoute:
    """Convert explicit route configuration into deterministic run facts."""

    __slots__ = ()

    def execute(self, configuration: RouteConfiguration) -> RouteSelection:
        """Select legacy, shadow, or local behavior without ambient defaults."""
        if type(configuration) is not RouteConfiguration:
            raise TypeError("configuration must be RouteConfiguration")
        return RouteSelection(*_ROUTE_TRUTH_TABLE[configuration.route])


class RollBackValidationRoute:
    """Construct the retained legacy rollback route without transforming data."""

    __slots__ = ()

    def execute(self, configuration: RouteConfiguration) -> RouteConfiguration:
        """Create a legacy configuration without deleting local evidence."""
        if type(configuration) is not RouteConfiguration:
            raise TypeError("configuration must be RouteConfiguration")
        return RouteConfiguration(ValidationRoute.LEGACY)
