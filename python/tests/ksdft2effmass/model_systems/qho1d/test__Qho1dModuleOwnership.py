"""Software verification of cohesive QHO1D source-module ownership."""

from __future__ import annotations

import importlib.util

from ksdft2effmass.model_systems import qho1d
from ksdft2effmass.model_systems.qho1d.analytical import Qho1dAnalytical
from ksdft2effmass.model_systems.qho1d.comparison_records import (
    Qho1dComparisonRequest,
    Qho1dComparisonResult,
)
from ksdft2effmass.model_systems.qho1d.finite_difference import Qho1dFiniteDifference
from ksdft2effmass.model_systems.qho1d.ladder_operators import Qho1dLadderOperators
from ksdft2effmass.model_systems.qho1d.parameters import (
    Qho1dNondimensionalizer,
    Qho1dParameters,
)


class TestQho1dModuleOwnership:
    """Verify direct owners and the deliberate package-level public surface."""

    def test_public_api__classes__are_the_direct_owner_classes(self) -> None:
        """The public root re-exports each class directly from its domain owner."""
        expected = {
            "Qho1dAnalytical": Qho1dAnalytical,
            "Qho1dComparisonRequest": Qho1dComparisonRequest,
            "Qho1dComparisonResult": Qho1dComparisonResult,
            "Qho1dFiniteDifference": Qho1dFiniteDifference,
            "Qho1dLadderOperators": Qho1dLadderOperators,
            "Qho1dNondimensionalizer": Qho1dNondimensionalizer,
            "Qho1dParameters": Qho1dParameters,
        }

        assert all(getattr(qho1d, name) is owner for name, owner in expected.items())

    def test_import__former_model_module__is_absent(self) -> None:
        """The former aggregate module is removed rather than retained as a facade."""
        assert (
            importlib.util.find_spec("ksdft2effmass.model_systems.qho1d.model") is None
        )
