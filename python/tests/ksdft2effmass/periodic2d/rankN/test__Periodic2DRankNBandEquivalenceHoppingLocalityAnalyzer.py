"""Periodic-2D rank-N aggregate analyzer and result contracts."""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.gauge_alignment import GaugeAlignmentActionConvention
from ksdft2effmass.periodic.operators import (
    LabeledComponentBasisCoordinate,
    PeriodicBasisInventory,
    PeriodicBasisInventoryEntry,
)
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity
from ksdft2effmass.periodic2d.gauge_alignment.base import (
    Periodic2DGaugeAlignmentAnalysis,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.fourier_reference import (  # noqa: E501
    Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer,
    Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.reference import (
    Periodic2DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer,
    Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.request import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum,
    Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.result import (
    Periodic2DRankNAlignmentInapplicabilityEnum,
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum,
    Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.verification import (  # noqa: E501
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerifier,
    Periodic2DRankNBandEquivalenceHoppingLocalityVerification,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.definition import (
    Periodic2DRankNGaugeAlignment,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.transformation import (
    Periodic2DRankNGaugeNormalizationEnum,
)
from ksdft2effmass.sewing import (
    IdentityReciprocalSewing,
    ReciprocalEndpointSewingInventory,
    ReciprocalEndpointSewingMap,
)
from periodic2d_rankn_analytic_case_support import (
    SyntheticPeriodic2DRankNCaseExpander,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]

PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY = PeriodicBasisInventory(
    entries=tuple(
        PeriodicBasisInventoryEntry(
            retained_rank=rank,
            basis_identity=Periodic2DBasisIdentity(
                display_identifier=f"periodic2d-rankN-test-basis-r{rank}",
                coordinates=tuple(
                    LabeledComponentBasisCoordinate(
                        label=f"test-retained-orbital-{index:02d}"
                    )
                    for index in range(rank)
                ),
            ),
        )
        for rank in (3, 4, 8)
    )
)


class TestPeriodic2DRankNBandEquivalenceHoppingLocalityAnalyzer:
    """Exercise one case while retaining the complete aggregate wire contract."""

    @staticmethod
    def _endpoint_sewing(
        ambient_dimension: int,
    ) -> ReciprocalEndpointSewingInventory:
        identity_sewing = IdentityReciprocalSewing(ambient_dimension=ambient_dimension)
        return ReciprocalEndpointSewingInventory(
            positive_axis_maps=(identity_sewing.endpoint_map,) * 2
        )

    @staticmethod
    def _request() -> Periodic2DRankNBandEquivalenceHoppingLocalityRequest:
        geometry = Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition(
            identifier="square-axis-control",
            positive_bonds=((1, 0), (0, 1)),
            gauge_normalization=Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(
                    a1=np.array((1.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=1.0,
        )
        return Periodic2DRankNBandEquivalenceHoppingLocalityRequest(
            family=Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL,
            cases=(geometry,),
            retained_ranks=(3, 4, 8),
            circuit_depths=(1, 2, 4),
            construction_size=16,
            evaluation_size=33,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0, 1.0),
            transformation_coefficients=(0.0, math.pi / 8.0, math.pi / 4.0),
            band_tolerances=(1.0e-3, 1.0e-5),
            gauge_alignments=(
                Periodic2DRankNGaugeAlignment.IDENTITY,
                Periodic2DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic2DRankNGaugeAlignment.POINTWISE_UNITARY,
                Periodic2DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
            ),
            shell_cap=25,
            procrustes_rank_cutoff_rule=(
                ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM
            ),
            procrustes_rank_absolute=1.0e-12,
            procrustes_rank_relative=1.0e-10,
            procrustes_validation_absolute=1.0e-12,
            procrustes_validation_relative=1.0e-10,
            transport_rank_absolute=1.0e-10,
            transport_rank_relative=1.0e-12,
            norm_energy_scale=1.0,
        )

    def test_aggregate_analyzer_requires_explicit_complete_model_inventory(
        self,
    ) -> None:
        request = self._request()
        models = SyntheticPeriodic2DRankNCaseExpander(
            request=request,
            basis_inventory=PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY,
        ).execute()

        analyzer = Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer(
            request=request,
            models=models,
        )

        assert analyzer.request is request
        with pytest.raises(ValueError, match="every exact request expansion"):
            Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer(
                request=request,
                models=models[:-1],
            )

    def test_case_analysis_uses_dimension_and_gauge_analysis_bases(self) -> None:
        request = self._request()
        expander = SyntheticPeriodic2DRankNCaseExpander(
            request=request,
            basis_inventory=PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY,
        )
        model = expander.execute()[1]
        analyzer = Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
            endpoint_sewing=self._endpoint_sewing(model.ambient_dimension),
        )
        result = analyzer.execute()

        assert expander.band_subspace_ranks == (3, 4, 8)
        assert analyzer.band_subspace_rank == 3
        assert result.band_subspace_rank == 3
        assert result.model_identity == model.model_identity
        assert result.minimum_sampled_external_gap >= 1.9
        assert tuple(item.alignment for item in result.alignments) == (
            Periodic2DRankNGaugeAlignment.IDENTITY,
            Periodic2DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic2DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic2DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        )
        assert all(
            isinstance(item, Periodic2DGaugeAlignmentAnalysis)
            for item in result.alignments
        )
        qualified = tuple(
            item
            for item in result.alignments
            if type(item)
            is Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
        )
        assert len(qualified) == 4
        assert all(item.retained_rank == 3 for item in qualified)
        assert all(item.gauge_group == "U(3)" for item in qualified)
        assert all(
            item.action_convention is GaugeAlignmentActionConvention.RIGHT
            for item in qualified
        )
        assert all(
            item.maximum_direct_ordered_spectrum_difference < 1.0e-12
            for item in qualified
        )
        assert all(
            item.reference_reconstruction_errors.maximum_matrix_frobenius < 1.0e-11
            for item in qualified
        )
        assert all(
            item.comparison_reconstruction_errors.maximum_matrix_frobenius < 1.0e-11
            for item in qualified[2:]
        )
        assert all(
            item.comparison_reconstruction_errors.maximum_matrix_frobenius > 1.0e-12
            for item in qualified[:2]
        )
        assert all(len(item.shells) == 14 for item in qualified)
        assert all(len(item.tolerance_decisions) == 2 for item in qualified)

    def test_v1_case_analysis_rejects_nonidentity_endpoint_sewing(self) -> None:
        request = self._request()
        model = SyntheticPeriodic2DRankNCaseExpander(
            request=request,
            basis_inventory=PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY,
        ).execute()[1]
        phase_matrix = np.eye(model.ambient_dimension, dtype=np.complex128)
        phase_matrix[0, 0] = np.exp(0.25j)
        identity_sewing = IdentityReciprocalSewing(
            ambient_dimension=model.ambient_dimension
        )

        with pytest.raises(ValueError, match="only named identity sewing"):
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
                request=request,
                model=model,
                geometry=request.cases[0],
                endpoint_sewing=ReciprocalEndpointSewingInventory(
                    positive_axis_maps=(
                        ReciprocalEndpointSewingMap(
                            identifier="rankN-nonidentity.test",
                            coefficient_map=ComplexMatrixQuantity(
                                phase_matrix,
                                Unitless(),
                            ),
                        ),
                        identity_sewing.endpoint_map,
                    )
                ),
            )

    def test_parent_alignment_and_transport_reference_is_independent(self) -> None:
        request = self._request()
        model = SyntheticPeriodic2DRankNCaseExpander(
            request=request,
            basis_inventory=PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY,
        ).execute()[1]
        case = Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
            endpoint_sewing=self._endpoint_sewing(model.ambient_dimension),
        ).execute()

        reference = Periodic2DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer(
            request=Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest(
                study_request=request,
                case_analysis=case,
            )
        ).execute()

        assert reference.passed
        assert len(reference.comparisons) == 55
        assert "parent.minimum_sampled_external_gap" in reference.comparisons
        assert (
            "alignment[global-unitary].minimum_cross_singular_value"
            in reference.comparisons
        )

    def test_fourier_shell_and_support_reference_uses_direct_sums(self) -> None:
        request = self._request()
        model = SyntheticPeriodic2DRankNCaseExpander(
            request=request,
            basis_inventory=PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY,
        ).execute()[1]
        case = Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
            endpoint_sewing=self._endpoint_sewing(model.ambient_dimension),
        ).execute()

        reference = Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer(  # noqa: E501
            request=Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest(
                study_request=request,
                case_analysis=case,
            )
        ).execute()

        assert reference.passed
        assert len(reference.comparisons) > 1_000
        assert (
            "alignment[identity].shell[0].reference_shell_power"
            in reference.comparisons
        )
        assert any("tolerance[" in key for key in reference.comparisons)

    def test_case_verification_composes_both_independent_routes(self) -> None:
        request = self._request()
        model = SyntheticPeriodic2DRankNCaseExpander(
            request=request,
            basis_inventory=PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY,
        ).execute()[1]
        case = Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
            endpoint_sewing=self._endpoint_sewing(model.ambient_dimension),
        ).execute()

        verification = Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerifier(
            request=Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest(
                study_request=request,
                case_analysis=case,
            )
        ).execute()

        decoded_case = (
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification.from_json(  # noqa: E501
                verification.to_json()
            )
        )
        aggregate = Periodic2DRankNBandEquivalenceHoppingLocalityVerification(
            request_sha256="0" * 64,
            analysis_sha256="1" * 64,
            cases=(verification,),
        )
        decoded_aggregate = (
            Periodic2DRankNBandEquivalenceHoppingLocalityVerification.from_json(
                aggregate.to_json()
            )
        )

        assert verification.passed
        assert decoded_case.to_json() == verification.to_json()
        assert aggregate.passed
        assert decoded_aggregate.to_json() == aggregate.to_json()

    def test_aggregate_analysis_round_trips_canonical_json(self) -> None:
        request = self._request()
        model = SyntheticPeriodic2DRankNCaseExpander(
            request=request,
            basis_inventory=PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY,
        ).execute()[0]
        case = Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
            endpoint_sewing=self._endpoint_sewing(model.ambient_dimension),
        ).execute()
        failure_type = (
            Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis
        )
        transport_failure = failure_type(
            identity=case.alignments[0].analysis_identity,
            alignment=Periodic2DRankNGaugeAlignment.IDENTITY,
            reason=(
                Periodic2DRankNAlignmentInapplicabilityEnum.TRANSPORT_LINK_RANK_DEFICIENT
            ),
            deficient_sample_count=1,
            minimum_numerical_rank=None,
        )
        case = replace(
            case,
            alignments=(transport_failure, *case.alignments[1:]),
        )
        cases = tuple(
            replace(case, model_identity=f"{case.model_identity}:wire-{index}")
            for index in range(request.case_count)
        )
        analysis = Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis(
            request=request,
            status=(
                Periodic2DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum.SOFTWARE_QUALIFICATION_NOT_SCIENTIFIC_EVIDENCE
            ),
            cases=cases,
        )

        decoded = Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis.from_json(
            analysis.to_json()
        )

        assert decoded.to_json() == analysis.to_json()
        assert decoded.request.to_json() == request.to_json()
        decoded_failure = decoded.cases[0].alignments[0]
        assert isinstance(
            decoded_failure,
            Periodic2DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
        )
        assert decoded_failure.retained_rank == 3
        assert (
            decoded_failure.reason
            is Periodic2DRankNAlignmentInapplicabilityEnum.TRANSPORT_LINK_RANK_DEFICIENT
        )
