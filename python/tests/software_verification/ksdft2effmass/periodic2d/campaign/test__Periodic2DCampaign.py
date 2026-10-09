"""Software evidence for removal of the dimension-only campaign base.

Facet and represented meaning
-----------------------------
The module verifies that concrete periodic-2D campaign composition roots are
independent and that the retired nominal base has no public or defining route.

Intrinsic and cross-object scope
--------------------------------
The oracle is source ownership: each concrete campaign owns its exact documents and
operations without inheriting a shared campaign identity.

VVUQ and scientific exclusions
------------------------------
These are exact software-contract checks. They establish neither compatibility among
campaigns nor numerical or scientific validation, uncertainty quantification, or
acceptance.
"""

import importlib

import pytest

import ksdft2effmass.periodic2d as periodic2d
import ksdft2effmass.periodic2d.campaign as campaign
from ksdft2effmass.periodic2d import (
    Periodic2DCompositeCampaign,
    Periodic2DIsolatedBandCampaign,
    Periodic2DOptimizerBasinCampaign,
    Periodic2DOptimizerReanalysisCampaign,
    Periodic2DOptimizerRegressionCampaign,
    Periodic2DOptimizerStandaloneCampaign,
    Periodic2DTopologicalCampaign,
    Periodic2DTopologicalPhaseSweepCampaign,
    Periodic2DWannier90BalancedCampaign,
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


class TestPeriodic2DCampaignRemoval:
    """Own removal evidence for the unjustified dimension-only base."""

    def test_public_api__retired_base__is_absent(self) -> None:
        """Neither reviewed periodic-2D facade exposes the retired base."""
        if hasattr(periodic2d, "Periodic2DCampaign"):
            raise AssertionError("periodic2d root still exposes retired campaign base")
        if hasattr(campaign, "Periodic2DCampaign"):
            raise AssertionError("campaign facade still exposes retired campaign base")

    def test_defining_module__retired_base__is_absent(self) -> None:
        """The removed defining module cannot be imported."""
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module("ksdft2effmass.periodic2d.campaign.base")

    @pytest.mark.parametrize("campaign_type", CAMPAIGN_TYPES)
    def test_class__concrete_campaign__has_no_shared_campaign_base(
        self, campaign_type: type[object]
    ) -> None:
        """Each concrete campaign derives directly from ``object``."""
        if campaign_type.__bases__ != (object,):
            raise AssertionError(
                f"{campaign_type.__name__} retains an unexpected nominal base"
            )
