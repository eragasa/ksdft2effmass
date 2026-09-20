r"""Software verification of ``Periodic1DCompositeBandCalculationWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: execution-local Appendix G parent fibers, composite gauge and
Wilson channels, complete block hoppings, separate approximation diagnostics, and
compatibility with authenticated historical scalar values.

Facet and represented meaning

The Workflow composes the reusable finite model, solid-state, and analysis owners into
one typed calculation result without reading retained result bytes.

Intrinsic and cross-object scope

This evidence checks parent/result structure, exact channel inventories, intrinsic
matrix properties, historical scalar compatibility, and pre-transform identities.
Independent numerical reconstruction is owned by the numerical facet.

VVUQ and scientific exclusions

A pass is software verification of behavior-preserving extraction. It does not
establish basis convergence, material validation, polarization, topology, uncertainty
quantification, or human acceptance.
"""

from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeBandCalculationGroupResult,
    Periodic1DCompositeBandCalculationRequest,
    Periodic1DCompositeBandCalculationResult,
    Periodic1DCompositeBandCalculationWorkflow,
    Periodic1DCompositeBandGroupResult,
    Periodic1DCompositeCampaignDefinition,
    Periodic1DCompositeCampaignJsonSerializer,
    Periodic1DCompositeCampaignResult,
    Periodic1DCompositeResultJsonSerializer,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCompositeBandCalculationWorkflow


class TestPeriodic1DCompositeBandCalculationWorkflow:
    """Own execution-local composite-band calculation evidence."""

    @staticmethod
    def repo_root() -> Path:
        """This helper owns no identifier; it locates maintained campaign files."""

        return Path(__file__).resolve().parents[7]

    @classmethod
    def definition(cls) -> Periodic1DCompositeCampaignDefinition:
        """This helper owns no identifier; it decodes the maintained input."""

        path = (
            cls.repo_root()
            / "calculations"
            / "research-monograph"
            / "periodic-1d"
            / "composite-input.json"
        )
        return Periodic1DCompositeCampaignJsonSerializer().deserialize(
            path.read_bytes()
        )

    @classmethod
    def retained_result(cls) -> Periodic1DCompositeCampaignResult:
        """This helper owns no identifier; it decodes historical comparison data."""

        path = (
            cls.repo_root()
            / "calculations"
            / "research-monograph"
            / "periodic-1d"
            / "composite-result.json"
        )
        return Periodic1DCompositeResultJsonSerializer().deserialize(path.read_bytes())

    @classmethod
    def request(cls) -> Periodic1DCompositeBandCalculationRequest:
        """This helper owns no identifier; it supplies explicit finite tolerances."""

        return Periodic1DCompositeBandCalculationRequest(
            definition=cls.definition(),
            duality_absolute_tolerance=ScalarQuantity(1.0e-12, Unitless()),
            frame_orthonormality_absolute_tolerance=ScalarQuantity(1.0e-10, Unitless()),
            overlap_singular_value_threshold=ScalarQuantity(0.0, Unitless()),
            coordinate_absolute_tolerance=ScalarQuantity(1.0e-12, Unitless()),
            transform_reconstruction_absolute_tolerance=ScalarQuantity(
                1.0e-10, Unitless()
            ),
            hopping_hermiticity_absolute_tolerance=ScalarQuantity(1.0e-10, Unitless()),
            wilson_phase_absolute_tolerance=1.0e-10,
        )

    @staticmethod
    def assert_group_compatibility(
        calculated_group: Periodic1DCompositeBandCalculationGroupResult,
        retained_group: Periodic1DCompositeBandGroupResult,
        definition: Periodic1DCompositeCampaignDefinition,
    ) -> None:
        """This helper owns no identifier; it checks one cohesive group contract."""

        outcome = calculated_group.outcome
        assert outcome.group_id == retained_group.group_id
        assert outcome.band_indices == retained_group.band_indices
        assert outcome.isolation.external_status.value == "pass"
        gauge = outcome.gauge_comparison
        hopping = outcome.hopping_representation
        assert gauge.controlled_gauge_projector_maximum_frobenius_defect < 1.0e-13
        assert gauge.pointwise_alignment_operator_maximum_frobenius_defect < 1.0e-12
        assert gauge.controlled_gauge_eigenvalue_maximum_defect < 1.0e-12
        assert outcome.wilson.controlled_gauge_phase_set_defect < 1.0e-12
        assert hopping.smooth_full_reconstruction_maximum_frobenius_error < 1.0e-12
        assert hopping.rough_full_reconstruction_maximum_frobenius_error < 1.0e-12
        assert hopping.smooth_hopping_hermiticity_maximum_frobenius_residual < 1.0e-12
        assert (
            tuple(record.hopping_range_cells for record in outcome.range_study)
            == definition.hopping_ranges_cells
        )
        np.testing.assert_allclose(
            outcome.wilson.spectrum.eigenphases,
            retained_group.wilson.spectrum.eigenphases,
            atol=5.0e-12,
            rtol=0.0,
        )
        retained_gauge = retained_group.gauge_comparison
        retained_hopping = retained_group.hopping_representation
        np.testing.assert_allclose(
            (
                outcome.isolation.internal_minimum_gap,
                outcome.isolation.external_minimum_gap,
                gauge.neighbor_overlap_minimum_singular_value,
                gauge.controlled_gauge_projector_maximum_frobenius_defect,
                gauge.pointwise_alignment_frame_maximum_frobenius_defect,
                gauge.pointwise_alignment_operator_maximum_frobenius_defect,
                gauge.controlled_gauge_eigenvalue_maximum_defect,
                gauge.rough_vs_smooth_unaligned_hopping_l2_defect,
                hopping.smooth_full_reconstruction_maximum_frobenius_error,
                hopping.rough_full_reconstruction_maximum_frobenius_error,
                hopping.smooth_hopping_hermiticity_maximum_frobenius_residual,
                outcome.direct_route.coefficient_frobenius_defect,
                outcome.direct_route.training_operator_maximum_frobenius_defect,
            ),
            (
                retained_group.isolation.internal_minimum_gap,
                retained_group.isolation.external_minimum_gap,
                retained_gauge.neighbor_overlap_minimum_singular_value,
                retained_gauge.controlled_gauge_projector_maximum_frobenius_defect,
                retained_gauge.pointwise_alignment_frame_maximum_frobenius_defect,
                retained_gauge.pointwise_alignment_operator_maximum_frobenius_defect,
                retained_gauge.controlled_gauge_eigenvalue_maximum_defect,
                retained_gauge.rough_vs_smooth_unaligned_hopping_l2_defect,
                retained_hopping.smooth_full_reconstruction_maximum_frobenius_error,
                retained_hopping.rough_full_reconstruction_maximum_frobenius_error,
                retained_hopping.smooth_hopping_hermiticity_maximum_frobenius_residual,
                retained_group.direct_route.coefficient_frobenius_defect,
                retained_group.direct_route.training_operator_maximum_frobenius_defect,
            ),
            atol=5.0e-12,
            rtol=0.0,
        )
        calculated_ranges = np.asarray(
            [
                (
                    record.smooth_omitted_block_l2_norm,
                    record.rough_omitted_block_l2_norm,
                    record.smooth_training_eigenvalue_maximum_error,
                    record.rough_training_eigenvalue_maximum_error,
                    record.smooth_withheld_eigenvalue_maximum_error,
                    record.rough_withheld_eigenvalue_maximum_error,
                )
                for record in outcome.range_study
            ],
            dtype=np.float64,
        )
        retained_ranges = np.asarray(
            [
                (
                    record.smooth_omitted_block_l2_norm,
                    record.rough_omitted_block_l2_norm,
                    record.smooth_training_eigenvalue_maximum_error,
                    record.rough_training_eigenvalue_maximum_error,
                    record.smooth_withheld_eigenvalue_maximum_error,
                    record.rough_withheld_eigenvalue_maximum_error,
                )
                for record in retained_group.range_study
            ],
            dtype=np.float64,
        )
        np.testing.assert_allclose(
            calculated_ranges,
            retained_ranges,
            atol=5.0e-12,
            rtol=0.0,
        )
        calculated_smooth_hoppings = np.asarray(
            [block.magnitude for block in hopping.smooth_hopping_model.hopping_blocks]
        )
        retained_smooth_hoppings = np.asarray(
            [
                block.magnitude
                for block in retained_hopping.smooth_hopping_model.hopping_blocks
            ]
        )
        calculated_rough_hoppings = np.asarray(
            [block.magnitude for block in hopping.rough_hopping_model.hopping_blocks]
        )
        retained_rough_hoppings = np.asarray(
            [
                block.magnitude
                for block in retained_hopping.rough_hopping_model.hopping_blocks
            ]
        )
        np.testing.assert_allclose(
            calculated_smooth_hoppings,
            retained_smooth_hoppings,
            atol=5.0e-12,
            rtol=0.0,
        )
        np.testing.assert_allclose(
            calculated_rough_hoppings,
            retained_rough_hoppings,
            atol=5.0e-12,
            rtol=0.0,
        )
        assert (
            outcome.identities.smooth_frame_sha256
            == retained_group.identities.smooth_frame_sha256
        )
        assert (
            outcome.identities.smooth_projector_sha256
            == retained_group.identities.smooth_projector_sha256
        )
        assert (
            outcome.identities.smooth_reciprocal_hamiltonian_sha256
            == retained_group.identities.smooth_reciprocal_hamiltonian_sha256
        )
        assert calculated_group.wilson_comparison.passes

    def test_method__execute__calculates_composite_channels(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-025

        Requirement: The public execution-local Workflow calculates parent spectra,
        frame/gauge/Wilson channels, complete hopping models, separate truncation,
        training, withheld, Hermiticity, and direct-route diagnostics without reading
        retained result bytes.

        Method: Deserialize the frozen Appendix G input, execute the public Workflow,
        and deserialize the historical result only after execution for compatibility
        comparison.

        Oracle: Intrinsic matrix identities, explicit channel structure, and the
        authenticated historical scalar result values and pre-transform identities.

        Acceptance: The calculated result exposes every demonstrated channel, satisfies
        its exact structural identities, and agrees with historical scalar values to
        ``5e-12``. Public FFT hopping identities may differ from historical direct-sum
        byte identities while their represented numerical values agree.

        Interpretation: A pass establishes behavior-preserving software extraction for
        the documented finite composite calculation.

        Limitations: This does not establish basis convergence, physical adequacy,
        material validation, uncertainty quantification, polarization, topology, or
        human acceptance. Independent mathematical reconstruction belongs to
        ``NV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-002``.
        """

        calculated = SUT().execute(self.request())
        assert type(calculated) is Periodic1DCompositeBandCalculationResult
        definition = calculated.request.definition
        parent = calculated.parent
        assert parent.mesh.point_count == definition.reciprocal_mesh_size
        assert len(parent.parent_operators.matrices) == definition.reciprocal_mesh_size
        assert parent.training_spectrum.sample_count == definition.reciprocal_mesh_size
        assert parent.withheld_spectrum.sample_count == definition.withheld_mesh_size
        assert parent.parent_eigenframes.rank == 5
        matrices = np.asarray(
            [matrix.magnitude for matrix in parent.parent_operators.matrices]
        )
        np.testing.assert_allclose(
            matrices,
            np.swapaxes(matrices.conj(), 1, 2),
            atol=1.0e-14,
            rtol=0.0,
        )
        eigenvalues = np.asarray(
            [np.linalg.eigvalsh(matrix)[:5] for matrix in matrices]
        )
        np.testing.assert_allclose(
            eigenvalues,
            parent.training_spectrum.eigenvalues.magnitude,
            atol=5.0e-13,
            rtol=0.0,
        )

        retained = self.retained_result()
        low_calculated, high_calculated = calculated.groups
        low_retained, high_retained = retained.groups
        assert (low_calculated.group.identifier, high_calculated.group.identifier) == (
            "low_pair",
            "higher_pair",
        )
        self.assert_group_compatibility(low_calculated, low_retained, definition)
        self.assert_group_compatibility(high_calculated, high_retained, definition)
