r"""Software verification of the reduction-challenge definition invariants.

Evidence profile: claim_bearing

Bounded artifact scope
----------------------
Exact nominal typing, reciprocal-mesh executability, band-index bounds, and potential-
shape identity for the retained version-one definition.

Scientific exclusions
---------------------
These construction tests establish fail-closed control validation only. They do not
execute the campaign, establish convergence, validate a model, quantify uncertainty,
or record acceptance.
"""

from dataclasses import replace
from pathlib import Path
from typing import cast

import numpy as np
import pytest

from ksdft2effmass.operators import VectorQuantity
from ksdft2effmass.periodic1d.campaign.reduction_challenge import (
    Periodic1DReductionChallengeCampaignDefinition,
    Periodic1DReductionChallengeCampaignJsonSerializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = Periodic1DReductionChallengeCampaignDefinition


class TestPeriodic1DReductionChallengeCampaignDefinition:
    """Own fail-closed invariant evidence for the canonical definition."""

    @staticmethod
    def _definition() -> Periodic1DReductionChallengeCampaignDefinition:
        """Decode the exact retained controls through the reviewed strict adapter."""
        root = Path(__file__).resolve().parents[7]
        payload = root.joinpath(
            "calculations/research-monograph/periodic-1d/stress-input.json"
        ).read_bytes()
        return Periodic1DReductionChallengeCampaignJsonSerializer().deserialize(payload)

    def test_construction__rejects_boolean_integer_control(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-005.

        Requirement: Public numeric controls reject booleans rather than accepting
        Python's integer subtype relation.

        Method: Replace the reference cutoff with an intentionally invalid typed
        boolean fixture.

        Oracle: Exact nominal-type contract.

        Acceptance: Construction raises ``TypeError``.

        Interpretation: A pass establishes fail-closed integer representation.

        Limitations: This does not test numerical execution.
        """
        definition = self._definition()

        with pytest.raises(TypeError, match="built-in int"):
            replace(
                definition,
                plane_wave_reference_cutoff=cast(int, True),
            )

    def test_construction__rejects_odd_reciprocal_mesh(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-006.

        Requirement: Centered complete-mesh reconstruction uses nontrivial even mesh
        sizes.

        Method: Replace the retained mesh inventory with one odd size.

        Oracle: The centered representative and Nyquist convention.

        Acceptance: Construction raises ``ValueError``.

        Interpretation: A pass establishes an executable reciprocal-mesh contract.

        Limitations: It does not establish mesh convergence.
        """
        with pytest.raises(ValueError, match="even values of at least two"):
            replace(self._definition(), reciprocal_mesh_sizes=(3,))

    def test_construction__rejects_band_index_outside_compared_inventory(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-007.

        Requirement: Every challenged band index fits the explicitly compared finite
        eigenspectrum.

        Method: Set one index equal to the compared-band count.

        Oracle: Zero-based finite-eigenspectrum indexing.

        Acceptance: Construction raises ``ValueError``.

        Interpretation: A pass excludes a non-executable band request.

        Limitations: It does not establish physical band isolation.
        """
        definition = self._definition()

        with pytest.raises(ValueError, match="outside compared bands"):
            replace(
                definition,
                challenged_band_indices=(definition.compared_band_count,),
            )

    def test_construction__requires_two_bands_for_boundary_gap(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-021.

        Requirement: The amplitude verifier's zone-boundary gap uses two bands.

        Method: Reduce the compared inventory and challenged subset to one band.

        Oracle: The explicit two-eigenvalue boundary-gap definition.

        Acceptance: Construction raises ``ValueError`` before numerical execution.

        Interpretation: A pass excludes incidental indexing failure in verification.

        Limitations: It does not establish physical isolation.
        """
        with pytest.raises(ValueError, match="at least two"):
            replace(
                self._definition(),
                compared_band_count=1,
                challenged_band_indices=(0,),
            )

    def test_construction__requires_every_plane_wave_sweep_to_fit_compared_bands(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-022.

        Requirement: Every finite plane-wave sweep matrix contains every compared band.

        Method: Supply a rank-three sweep matrix with four requested bands.

        Oracle: Symmetric cutoff dimension ``2 * cutoff + 1``.

        Acceptance: Construction raises ``ValueError``.

        Interpretation: A pass establishes executable low-band slicing controls.

        Limitations: It does not establish cutoff convergence.
        """
        with pytest.raises(ValueError, match="plane-wave sweep dimension"):
            replace(
                self._definition(),
                plane_wave_cutoffs=(1,),
                compared_band_count=4,
                challenged_band_indices=(0,),
            )

    def test_construction__requires_challenged_band_upper_neighbor(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-023.

        Requirement: Every challenged band has an upper neighbor in the finest
        plane-wave isolation representation.

        Method: Challenge the highest band of a rank-three sweep matrix.

        Oracle: Adjacent-gap indexing requires ``band_index + 1``.

        Acceptance: Construction raises ``ValueError``.

        Interpretation: A pass excludes truncated adjacent-gap lookup.

        Limitations: It does not establish a nonzero gap.
        """
        with pytest.raises(ValueError, match="upper neighbor"):
            replace(
                self._definition(),
                plane_wave_cutoffs=(1,),
                compared_band_count=3,
                challenged_band_indices=(2,),
            )

    def test_construction__requires_every_grid_to_fit_compared_bands(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-024.

        Requirement: Every finite-difference matrix contains every compared band.

        Method: Request eight bands from a seven-point periodic grid.

        Oracle: Dense matrix rank bounds the eigensolver subset.

        Acceptance: Construction raises ``ValueError``.

        Interpretation: A pass excludes incidental eigensolver-argument failure.

        Limitations: It does not establish grid convergence.
        """
        with pytest.raises(ValueError, match="finite-difference grid"):
            replace(self._definition(), finite_difference_points=(7,))

    def test_construction__requires_shape_harmonics_to_fit_reference_matrix(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-025.

        Requirement: Every represented Fourier harmonic has a nonempty diagonal in the
        finite reference plane-wave matrix.

        Method: Place five harmonics in a rank-five reference representation.

        Oracle: A rank ``2 * cutoff + 1`` matrix supports offsets through rank minus
        one.

        Acceptance: Construction raises ``ValueError``.

        Interpretation: A pass excludes negative-size or absent harmonic diagonals.

        Limitations: It does not establish adequacy of the retained harmonic count.
        """
        definition = self._definition()
        shape = definition.potential_shapes[0]
        unit = shape.potential.cosine_coefficients.unit
        potential = replace(
            shape.potential,
            cosine_coefficients=VectorQuantity(np.zeros(5), unit),
            sine_coefficients=VectorQuantity(np.zeros(5), unit),
        )

        with pytest.raises(ValueError, match="harmonics must fit"):
            replace(
                definition,
                plane_wave_cutoffs=(1,),
                plane_wave_reference_cutoff=2,
                compared_band_count=2,
                challenged_band_indices=(0,),
                potential_shapes=(replace(shape, potential=potential),),
            )

    def test_construction__rejects_duplicate_potential_shape_identity(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-008.

        Requirement: Potential-shape cases have explicit unique wire identities.

        Method: Repeat the first retained shape object.

        Oracle: Closed unique shape inventory.

        Acceptance: Construction raises ``ValueError``.

        Interpretation: A pass prevents ambiguous result correlation.

        Limitations: A unique identifier does not establish a physical potential model.
        """
        definition = self._definition()
        shape = definition.potential_shapes[0]

        with pytest.raises(ValueError, match="identifiers must be unique"):
            replace(definition, potential_shapes=(shape, shape))
