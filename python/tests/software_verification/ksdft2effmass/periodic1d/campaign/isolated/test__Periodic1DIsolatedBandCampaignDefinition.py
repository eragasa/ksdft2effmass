r"""Software verification of ``Periodic1DIsolatedBandCampaignDefinition``.

Evidence profile: routine

Facet and represented meaning

The immutable definition rejects controls that its isolated-band calculation cannot
consume and preserves exact type-versus-value exception boundaries.

VVUQ and scientific exclusions

These tests establish intrinsic control validation only. They do not execute the
campaign or establish convergence, physical adequacy, scientific validation,
uncertainty quantification, or acceptance.
"""

from dataclasses import replace
from pathlib import Path
from typing import cast

import numpy as np
import pytest

from ksdft2effmass.operators import Unitless, VectorQuantity
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DIsolatedBandCampaignDefinition,
    Periodic1DIsolatedBandCampaignJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DIsolatedBandCampaignDefinition


class TestPeriodic1DIsolatedBandCampaignDefinition:
    """Own intrinsic validation evidence for isolated-band controls."""

    @staticmethod
    def _definition() -> Periodic1DIsolatedBandCampaignDefinition:
        root = Path(__file__).resolve().parents[7]
        payload = root.joinpath(
            "calculations/research-monograph/periodic-1d/input.json"
        ).read_bytes()
        return Periodic1DIsolatedBandCampaignJsonSerializer().deserialize(payload)

    def test_construction__distinguishes_identity_type_and_value_errors(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-049.

        Wrong identity representation raises ``TypeError``; an empty exact string
        raises ``ValueError``.
        """
        definition = self._definition()

        with pytest.raises(TypeError, match="built-in str"):
            replace(definition, experiment_id=cast(str, 7))
        with pytest.raises(ValueError, match="nonempty"):
            replace(definition, experiment_id="")

    def test_construction__rejects_unusable_parent_dimensions(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-050.

        Every finite-difference grid, shared low-mode dimension, and compared band
        inventory must fit the declared finite parent representations.
        """
        definition = self._definition()

        with pytest.raises(ValueError, match="at least three"):
            replace(definition, finite_difference_points=(2,))
        with pytest.raises(ValueError, match="low-mode dimension"):
            replace(
                definition,
                finite_difference_points=(3,),
                common_low_mode_cutoff=2,
            )
        with pytest.raises(ValueError, match="compared bands"):
            replace(
                definition,
                finite_difference_points=(3,),
                common_low_mode_cutoff=1,
                compared_band_count=4,
            )

    def test_construction__rejects_nonpositive_weak_strengths(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-051.

        Every weak-potential control must satisfy the calculation's positive-strength
        precondition.
        """
        definition = self._definition()
        invalid = VectorQuantity(np.asarray([0.0, 0.1]), Unitless())

        with pytest.raises(ValueError, match="must be positive"):
            replace(definition, weak_potential_strengths=invalid)
