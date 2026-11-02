"""Software verification for ``Periodic2DCampaign``.

Facet and represented meaning
-----------------------------
The module verifies the lightweight common type and exact dimensional identity of
canonical periodic2d campaign DataObjects.

Intrinsic and cross-object scope
--------------------------------
The intrinsic oracle is the documented two-dimensional package contract. Inheritance
checks cover only nominal campaign organization and do not compare campaign models.

VVUQ and scientific exclusions
------------------------------
These are exact software-contract checks. They provide no numerical verification,
scientific validation, uncertainty quantification, or campaign acceptance.
"""

import pytest

from ksdft2effmass.periodic2d.campaign.base import Periodic2DCampaign
from ksdft2effmass.periodic2d.campaign.nbands_1.data import (
    Periodic2DIsolatedBandCampaign,
)
from ksdft2effmass.periodic2d.run.composite.data import Periodic2DCompositeCampaign
from ksdft2effmass.periodic2d.run.topological.data import Periodic2DTopologicalCampaign
from ksdft2effmass.periodic2d.run.topological.phase_sweep.data import (
    Periodic2DTopologicalPhaseSweepCampaign,
)
from ksdft2effmass.periodic2d.run.wannier90.balanced.data import (
    Periodic2DWannier90BalancedCampaign,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression.data import (  # noqa: E501
    Periodic2DOptimizerRegressionCampaign,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.data import (
    Periodic2DOptimizerBasinCampaign,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis.data import (
    Periodic2DOptimizerReanalysisCampaign,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone.data import (
    Periodic2DOptimizerStandaloneCampaign,
)
from ksdft2effmass.periodic2d.run.wannier90.study.data import (
    Periodic2DWannier90StudyCampaign,
)

CAMPAIGN_TYPES = (
    pytest.param(Periodic2DIsolatedBandCampaign, id="isolated_band"),
    pytest.param(Periodic2DCompositeCampaign, id="composite_band"),
    pytest.param(Periodic2DTopologicalCampaign, id="topological_models"),
    pytest.param(Periodic2DTopologicalPhaseSweepCampaign, id="topological_sweep"),
    pytest.param(Periodic2DWannier90BalancedCampaign, id="wannier90_balanced"),
    pytest.param(Periodic2DWannier90StudyCampaign, id="wannier90_study"),
    pytest.param(Periodic2DOptimizerBasinCampaign, id="optimizer_basin"),
    pytest.param(Periodic2DOptimizerReanalysisCampaign, id="optimizer_reanalysis"),
    pytest.param(Periodic2DOptimizerStandaloneCampaign, id="optimizer_standalone"),
    pytest.param(Periodic2DOptimizerRegressionCampaign, id="optimizer_regression"),
)


class TestPeriodic2DCampaign:
    """Own software evidence for the lightweight periodic2d campaign base."""

    def test_public_api__authoritative_module_owns_the_base_class(self) -> None:
        """The direct base module owns the exact campaign class identity."""
        if Periodic2DCampaign.__module__ != "ksdft2effmass.periodic2d.campaign.base":
            raise AssertionError("campaign base class has an unexpected owner")

    def test_property__spatial_dimension__returns_exact_two(self) -> None:
        """The base campaign reports the exact built-in integer dimension two."""
        dimension = Periodic2DCampaign().spatial_dimension

        if type(dimension) is not int or dimension != 2:
            raise AssertionError(
                "periodic2d spatial dimension must be exact integer two"
            )

    @pytest.mark.parametrize("campaign_type", CAMPAIGN_TYPES)
    def test_class__inheritance__includes_every_canonical_campaign(
        self, campaign_type: type[Periodic2DCampaign]
    ) -> None:
        """Every canonical periodic2d campaign inherits the common base contract."""
        if not issubclass(campaign_type, Periodic2DCampaign):
            raise AssertionError(
                "canonical campaign does not inherit Periodic2DCampaign"
            )
