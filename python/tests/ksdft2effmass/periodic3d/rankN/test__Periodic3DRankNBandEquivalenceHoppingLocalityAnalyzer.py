"""Periodic-3D rank-N aggregate analyzer and result contracts."""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.periodic.lattice import DirectLattice3D, DirectLatticeMetric

from ksdft2effmass.gauge_alignment import GaugeAlignmentActionConvention
from ksdft2effmass.periodic3d.gauge_alignment.base import (
    Periodic3DGaugeAlignmentAnalysis,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
    Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.field_geometry import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.fourier_reference import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer,
    Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.policy import (
    Periodic3DRankNBandEquivalenceHoppingLocalityPolicy,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.reference import (
    Periodic3DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer,
    Periodic3DRankNBandEquivalenceHoppingLocalityReferenceRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.represented_fields import (  # noqa: E501
    Periodic3DRankNParentGaugeCaseFieldSampler,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.request import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    Periodic3DRankNBandEquivalenceHoppingLocalityFamilyEnum,
    Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
    Periodic3DRankNLatticeControlEnum,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.result import (
    Periodic3DRankNAlignmentInapplicabilityEnum,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum,
    Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalysis,
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
from ksdft2effmass.periodic3d.rankN.gauge_alignment.transformation import (
    Periodic3DRankNGaugeNormalizationEnum,
)
from ksdft2effmass.sewing import (
    IdentityReciprocalSewing,
    ReciprocalEndpointSewingInventory,
)
from periodic3d_rankn_analytic_case_support import (
    SyntheticPeriodic3DRankNCaseExpander,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNBandEquivalenceHoppingLocalityAnalyzer:
    """Exercise one case while retaining the complete aggregate wire contract."""

    @staticmethod
    def _request() -> Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
        geometry = Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition(
            lattice_control=(
                Periodic3DRankNLatticeControlEnum.SIMPLE_CUBIC_AXIS_CONTROL
            ),
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
            transformation_coefficients=(0.0, math.pi / 8.0, math.pi / 4.0),
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

    @staticmethod
    def _simple_cubic_case(
        request: Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
    ) -> Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition:
        return request.case(Periodic3DRankNLatticeControlEnum.SIMPLE_CUBIC_AXIS_CONTROL)

    @staticmethod
    def _field_geometry(
        source: Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    ) -> Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry:
        return Periodic3DRankNBandEquivalenceHoppingLocalityFieldGeometry(
            identifier=source.lattice_control.to_wire(),
            direct_metric=source.direct_metric,
            shell_metric_scale=source.shell_metric_scale,
            basis_offsets=source.basis_offsets,
        )

    @staticmethod
    def _policy(
        request: Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
        ambient_dimension: int,
    ) -> Periodic3DRankNBandEquivalenceHoppingLocalityPolicy:
        identity_sewing = IdentityReciprocalSewing(ambient_dimension=ambient_dimension)
        return Periodic3DRankNBandEquivalenceHoppingLocalityPolicy(
            construction_size=request.construction_size,
            construction_offsets=(0.5, 0.5, 0.5),
            norm_energy_scale=request.norm_energy_scale,
            band_tolerances=request.band_tolerances,
            gauge_alignments=request.gauge_alignments,
            shell_cap=request.shell_cap,
            procrustes_tolerance=request.procrustes_tolerance,
            transport_rank_absolute=request.transport_rank_absolute,
            transport_rank_relative=request.transport_rank_relative,
            endpoint_sewing=ReciprocalEndpointSewingInventory(
                positive_axis_maps=(identity_sewing.endpoint_map,) * 3
            ),
        )

    @staticmethod
    def _coordinates(size: int, offset: float) -> Float64Array:
        axis = -0.5 + (np.arange(size, dtype=np.float64) + offset) / float(size)
        return np.asarray(
            np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1),
            dtype=np.float64,
        )

    def test_aggregate_analyzer_requires_explicit_complete_model_inventory(
        self,
    ) -> None:
        request = self._request()
        models = SyntheticPeriodic3DRankNCaseExpander(request=request).execute()

        analyzer = Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer(
            request=request,
            models=models,
        )

        assert analyzer.request is request
        with pytest.raises(ValueError, match="every exact request expansion"):
            Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer(
                request=request,
                models=models[:-1],
            )

    def test_case_analysis_uses_dimension_and_gauge_analysis_bases(self) -> None:
        request = self._request()
        expander = SyntheticPeriodic3DRankNCaseExpander(request=request)
        model = expander.execute()[1]
        analyzer = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=self._simple_cubic_case(request),
        )
        result = analyzer.execute()

        assert expander.band_subspace_ranks == (3, 4, 8)
        assert analyzer.band_subspace_rank == 3
        assert result.band_subspace_rank == 3
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

    def test_field_analyzer_reproduces_the_synthetic_adapter_analysis(self) -> None:
        request = self._request()
        model = SyntheticPeriodic3DRankNCaseExpander(request=request).execute()[1]
        fields = Periodic3DRankNParentGaugeCaseFieldSampler(model).execute(
            self._coordinates(request.construction_size, 0.5),
            self._coordinates(
                request.evaluation_size,
                0.5 + request.evaluation_shift,
            ),
        )

        policy = self._policy(request, model.ambient_dimension)
        field_analysis = Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer(
            policy=policy,
            geometry=self._field_geometry(self._simple_cubic_case(request)),
            fields=fields,
        ).execute()
        case_analysis = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=self._simple_cubic_case(request),
        ).execute()

        assert (
            type(field_analysis)
            is Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalysis
        )
        assert field_analysis.policy is policy
        assert field_analysis.geometry_identifier == (
            self._simple_cubic_case(request).lattice_control.to_wire()
        )
        assert field_analysis.retained_rank == fields.retained_rank
        assert field_analysis.operator_identifier == fields.operator_identifier
        assert field_analysis.energy_reference == fields.energy_reference
        assert field_analysis.energy_unit == fields.energy_unit
        assert field_analysis.basis_identifier == fields.basis_identifier
        assert field_analysis.alignments == case_analysis.alignments
        assert not hasattr(field_analysis, "parent_scale")
        assert not hasattr(field_analysis, "transformation_coefficient")
        assert not hasattr(field_analysis, "minimum_sampled_external_gap")

    def test_field_analyzer_allows_analysis_without_an_inverse_oracle(self) -> None:
        request = self._request()
        model = SyntheticPeriodic3DRankNCaseExpander(request=request).execute()[1]
        fields = Periodic3DRankNParentGaugeCaseFieldSampler(model).execute(
            self._coordinates(request.construction_size, 0.5),
            self._coordinates(
                request.evaluation_size,
                0.5 + request.evaluation_shift,
            ),
        )
        fields_without_inverse = replace(
            fields,
            comparison_inverse_construction_right_actions=None,
            comparison_inverse_evaluation_right_actions=None,
        )
        full_policy = self._policy(request, model.ambient_dimension)
        policy_without_oracle = replace(
            full_policy,
            gauge_alignments=full_policy.gauge_alignments[:-1],
        )

        analysis = Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer(
            policy=policy_without_oracle,
            geometry=self._field_geometry(self._simple_cubic_case(request)),
            fields=fields_without_inverse,
        ).execute()

        assert tuple(item.alignment for item in analysis.alignments) == (
            Periodic3DRankNGaugeAlignment.IDENTITY,
            Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
        )
        with pytest.raises(ValueError, match="requires prescribed actions"):
            Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer(
                policy=full_policy,
                geometry=self._field_geometry(self._simple_cubic_case(request)),
                fields=fields_without_inverse,
            )

    def test_parent_alignment_and_transport_reference_is_independent(self) -> None:
        request = self._request()
        model = SyntheticPeriodic3DRankNCaseExpander(request=request).execute()[1]
        case = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=self._simple_cubic_case(request),
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
        model = SyntheticPeriodic3DRankNCaseExpander(request=request).execute()[1]
        case = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=self._simple_cubic_case(request),
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
        model = SyntheticPeriodic3DRankNCaseExpander(request=request).execute()[1]
        case = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=self._simple_cubic_case(request),
        ).execute()

        verification = Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerifier(
            request=Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest(
                study_request=request,
                case_analysis=case,
            )
        ).execute()

        decoded_case = (
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseVerification.from_json(  # noqa: E501
                verification.to_json()
            )
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
        model = SyntheticPeriodic3DRankNCaseExpander(request=request).execute()[0]
        case = Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
            request=request,
            model=model,
            geometry=self._simple_cubic_case(request),
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
