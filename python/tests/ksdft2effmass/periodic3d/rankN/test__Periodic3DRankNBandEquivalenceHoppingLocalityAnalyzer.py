"""Periodic-3D rank-N aggregate analyzer and result contracts."""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.periodic.lattice import DirectLattice3D, DirectLatticeMetric

from ksdft2effmass.gauge_alignment import GaugeAlignmentActionConvention
from ksdft2effmass.periodic3d.gauge_alignment.base import (
    Periodic3DGaugeAlignmentAnalysis,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.case_expansion import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.fourier_reference import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer,
    Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.model import (
    Periodic3DRankNGaugeNormalizationEnum,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.reference import (
    Periodic3DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer,
    Periodic3DRankNBandEquivalenceHoppingLocalityReferenceRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.request import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum,
    Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.result import (
    Periodic3DRankNAlignmentInapplicabilityEnum,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum,
    Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.verification import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerification,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerifier,
    Periodic3DRankNBandEquivalenceHoppingLocalityVerification,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.definition import (
    Periodic3DRankNGaugeAlignment,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNBandEquivalenceHoppingLocalityAnalyzer:
    """Exercise one case while retaining the complete aggregate wire contract."""

    @staticmethod
    def _request() -> Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
        geometry = Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition(
            identifier="simple-cubic-axis-control",
            positive_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            gauge_normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
            direct_metric=DirectLatticeMetric(
                DirectLattice3D(
                    a1=np.array((1.0, 0.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0, 0.0), dtype=np.float64),
                    a3=np.array((0.0, 0.0, 1.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=1.0,
        )
        return Periodic3DRankNBandEquivalenceHoppingLocalityRequest(
            family=Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL,
            cases=(geometry,),
            retained_ranks=(3, 4, 8),
            circuit_depths=(1, 2, 4),
            construction_size=8,
            evaluation_size=17,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0, 1.0),
            attack_coefficients=(0.0, math.pi / 8.0, math.pi / 4.0),
            band_tolerances=(1.0e-3, 1.0e-5),
            gauge_alignments=(
                Periodic3DRankNGaugeAlignment.IDENTITY,
                Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
                Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
            ),
            shell_cap=9,
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

    def test_case_analysis_uses_dimension_and_gauge_analysis_bases(self) -> None:
        request = self._request()
        model = Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander(
            request=request
        ).execute()[1]
        result = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
        ).execute()

        assert result.model_identity == model.model_identity
        assert result.minimum_sampled_external_gap >= 1.9
        assert tuple(item.alignment for item in result.alignments) == (
            Periodic3DRankNGaugeAlignment.IDENTITY,
            Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        )
        assert all(
            isinstance(item, Periodic3DGaugeAlignmentAnalysis)
            for item in result.alignments
        )
        qualified = tuple(
            item
            for item in result.alignments
            if type(item)
            is Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
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
        assert all(len(item.shells) == 9 for item in qualified)
        assert all(len(item.tolerance_decisions) == 2 for item in qualified)

    def test_parent_alignment_and_transport_reference_is_independent(self) -> None:
        request = self._request()
        model = Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander(
            request=request
        ).execute()[1]
        case = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
        ).execute()

        reference = Periodic3DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer(
            request=Periodic3DRankNBandEquivalenceHoppingLocalityReferenceRequest(
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
        model = Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander(
            request=request
        ).execute()[1]
        case = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
        ).execute()

        reference = Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer(  # noqa: E501
            request=Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest(
                study_request=request,
                case_analysis=case,
            )
        ).execute()

        assert reference.passed
        assert len(reference.comparisons) > 700
        assert (
            "alignment[identity].shell[0].reference_shell_power"
            in reference.comparisons
        )
        assert any("tolerance[" in key for key in reference.comparisons)

    def test_case_verification_composes_both_independent_routes(self) -> None:
        request = self._request()
        model = Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander(
            request=request
        ).execute()[1]
        case = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
        ).execute()

        verification = Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerifier(
            request=Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest(
                study_request=request,
                case_analysis=case,
            )
        ).execute()

        decoded_case = Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerification.from_json(  # noqa: E501
            verification.to_json()
        )
        aggregate = Periodic3DRankNBandEquivalenceHoppingLocalityVerification(
            request_sha256="0" * 64,
            analysis_sha256="1" * 64,
            cases=(verification,),
        )
        decoded_aggregate = (
            Periodic3DRankNBandEquivalenceHoppingLocalityVerification.from_json(
                aggregate.to_json()
            )
        )

        assert verification.passed
        assert decoded_case.to_json() == verification.to_json()
        assert aggregate.passed
        assert decoded_aggregate.to_json() == aggregate.to_json()

    def test_aggregate_analysis_round_trips_canonical_json(self) -> None:
        request = self._request()
        model = Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander(
            request=request
        ).execute()[0]
        case = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=request.cases[0],
        ).execute()
        failure_type = (
            Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis
        )
        transport_failure = failure_type(
            identity=case.alignments[0].analysis_identity,
            alignment=Periodic3DRankNGaugeAlignment.IDENTITY,
            reason=(
                Periodic3DRankNAlignmentInapplicabilityEnum.TRANSPORT_LINK_RANK_DEFICIENT
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
        analysis = Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis(
            request=request,
            status=(
                Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum.SOFTWARE_QUALIFICATION_NOT_SCIENTIFIC_EVIDENCE
            ),
            cases=cases,
        )

        decoded = Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis.from_json(
            analysis.to_json()
        )

        assert decoded.to_json() == analysis.to_json()
        assert decoded.request.to_json() == request.to_json()
        decoded_failure = decoded.cases[0].alignments[0]
        assert isinstance(
            decoded_failure,
            Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
        )
        assert decoded_failure.retained_rank == 3
        assert (
            decoded_failure.reason
            is Periodic3DRankNAlignmentInapplicabilityEnum.TRANSPORT_LINK_RANK_DEFICIENT
        )
