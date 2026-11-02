"""Periodic-3D rank-N aggregate band-equivalence/locality analysis."""

from __future__ import annotations

from typing import ClassVar, final

import numpy as np
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array, Int64Array
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer

from ksdft2effmass.band_equivalence_hopping_locality.fourier import (
    error_channels,
    iter_complete_shell_fields,
    maximum_matrix_defect,
)
from ksdft2effmass.band_equivalence_hopping_locality.geometry import (
    metric_shell_classification,
)
from ksdft2effmass.band_equivalence_hopping_locality.rankN.analysis import (
    _PeriodicRankNBandEquivalenceHoppingLocalityProductionArithmetic,
    _ReferenceFourierData,
)
from ksdft2effmass.band_equivalence_hopping_locality.results import (
    BandEquivalenceHoppingLocalityErrorChannels,
)
from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (
    MetricShellHoppingPowerResult,
)
from ksdft2effmass.gauge_alignment import GaugeAlignmentAnalysisIdentity
from ksdft2effmass.periodic3d.rankN.band_alignment.frame_transport.analysis import (
    Periodic3DRankNTransportAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_alignment.frame_transport.request import (
    Periodic3DRankNTransportAnalysisRequest,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.base import (
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzerRole,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.analysis import (
    Periodic3DRankNGlobalGaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.definition import (
    Periodic3DRankNGaugeAlignment,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.procrustes.analysis import (
    Periodic3DRankNProcrustesAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.procrustes.request import (
    Periodic3DRankNProcrustesAnalysisRequest,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.procrustes.result import (
    Periodic3DRankNProcrustesAnalysis,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.request import (
    Periodic3DRankNGlobalGaugeAlignmentAnalysisRequest,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.result import (
    Periodic3DRankNGlobalGaugeAlignmentAnalysis,
    Periodic3DRankNGlobalGaugeAlignmentRankDeficient,
    Periodic3DRankNGlobalGaugeAlignmentSelected,
)
from ksdft2effmass.periodic3d.rankN.hopping_locality.analysis import (
    Periodic3DRankNHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.hopping_locality.request import (
    Periodic3DRankNHoppingLocalityAnalysisRequest,
    Periodic3DRankNHoppingLocalityChannelEnum,
)
from ksdft2effmass.periodic3d.rankN.support_truncation.analysis import (
    Periodic3DRankNSupportTruncationAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.support_truncation.request import (
    Periodic3DRankNSupportTruncationAnalysisRequest,
    Periodic3DRankNSupportTruncationChannelEnum,
)
from ksdft2effmass.real_space_support_truncation import (
    MinimumToleranceSatisfyingSupport,
    SupportToleranceSelectionOutcome,
    SupportToleranceUnresolved,
)

from .case_expansion import Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander
from .model import Periodic3DRankNAnalyticCase
from .request import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
)
from .result import (
    Periodic3DRankNAlignmentInapplicabilityEnum,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels,
    Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary,
    Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision,
    Periodic3DRankNFittedAlignmentEvidence,
    Periodic3DRankNPrescribedAlignmentEvidence,
    Periodic3DRankNSupportSelected,
    Periodic3DRankNSupportSelection,
    Periodic3DRankNSupportUnresolved,
)


@final
class Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
    _PeriodicRankNBandEquivalenceHoppingLocalityProductionArithmetic,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction,
):
    """Compose installed capability owners for one exact analytic case.

    The retained locality summary currently derives non-onsite power by subtracting
    the separately rounded onsite power from total power and clipping at zero.  For
    the selected bounded analytic baseline this can suppress only roundoff-scale
    power and does not affect shell selection, which uses direct shell sums.  It is
    deferred numerical robustness debt recorded as ``TD-BEL-003``; a reported zero
    must not be interpreted as proof of an exactly onsite-only model.
    """

    __slots__ = ("_geometry", "_model", "_request")

    _SPATIAL_DIMENSION: ClassVar[int] = 3

    @property
    def band_subspace_rank(self) -> int:
        """Return the exact case's represented band-subspace rank."""
        return self._model.retained_rank

    def __init__(
        self,
        *,
        request: Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
        model: Periodic3DRankNAnalyticCase,
        geometry: Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    ) -> None:
        if type(request) is not Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
            raise TypeError("request must be the exact periodic-3D rank-N request")
        if type(model) is not Periodic3DRankNAnalyticCase:
            raise TypeError("model must be the exact periodic-3D analytic case")
        if (
            type(geometry)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition
        ):
            raise TypeError("geometry must be the exact periodic-3D case definition")
        selected_geometry = next(
            (
                case
                for case in request.cases
                if case.identifier == model.case_identifier
            ),
            None,
        )
        if selected_geometry is not geometry:
            raise ValueError("geometry must be the request-owned model geometry")
        if (
            model.positive_bonds != geometry.positive_bonds
            or model.gauge_normalization is not geometry.gauge_normalization
            or model.retained_rank not in request.retained_ranks
            or model.circuit_depth not in request.circuit_depths
            or model.parent_scale not in request.parent_scales
            or model.attack_coefficient not in request.attack_coefficients
        ):
            raise ValueError("model must be one exact expansion of the request")
        self._request = request
        self._model = model
        self._geometry = geometry

    @property
    def request(self) -> Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
        """Return the immutable aggregate request bound to this action."""
        return self._request

    def _alignment_identity(
        self,
        retained_rank: int,
    ) -> GaugeAlignmentAnalysisIdentity:
        return super()._common_alignment_identity(
            retained_rank,
            self._request.construction_size,
        )

    @staticmethod
    def _error_record(
        value: BandEquivalenceHoppingLocalityErrorChannels,
    ) -> Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels:
        return Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels(
            maximum_matrix_frobenius=value.maximum_hamiltonian,
            root_mean_square_matrix_frobenius=value.rms_hamiltonian,
            maximum_ordered_spectrum=value.maximum_band,
            root_mean_square_ordered_spectrum=value.rms_band,
        )

    @staticmethod
    def _locality_summary(
        value: MetricShellHoppingPowerResult,
    ) -> Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary:
        """Project powers through the deferred subtraction policy of TD-BEL-003."""
        onsite = tuple(
            power.displacement for power in value.powers if power.displacement.is_zero
        )
        onsite_power = value.normalized_power_for(onsite)
        total = value.normalized_total_power
        return Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary(
            total_power=total,
            onsite_power=onsite_power,
            nononsite_power=max(0.0, total - onsite_power),
        )

    def _hopping_locality(
        self,
        *,
        model: Periodic3DRankNAnalyticCase,
        channel: Periodic3DRankNHoppingLocalityChannelEnum,
        series: NumpyFiniteFourierMatrixSeries,
        metric_indices: Int64Array,
    ) -> MetricShellHoppingPowerResult:
        return Periodic3DRankNHoppingLocalityAnalyzer(
            request=Periodic3DRankNHoppingLocalityAnalysisRequest(
                retained_rank=model.retained_rank,
                channel=channel,
                energy_reference="dimensionless-zero-v1",
                basis_identifier=(
                    f"{model.MODEL_FAMILY_IDENTITY}:retained-coordinate-basis"
                ),
                series=series,
                shell_indices=tuple(int(value) for value in metric_indices),
            ),
            power_analyzer=BlockHoppingPowerAnalyzer(),
        ).execute()

    def _reference_fourier(
        self,
        *,
        model: Periodic3DRankNAnalyticCase,
        geometry: Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
        construction_values: Complex128Array,
    ) -> _ReferenceFourierData:
        size = self._request.construction_size
        source_mesh = self._centered_mesh(size, 0.5)
        construction_axis = self._coordinate_axis(size, 0.5)
        evaluation_axis = self._coordinate_axis(
            self._request.evaluation_size,
            0.5 + self._request.evaluation_shift,
        )
        construction_axes = self._tensor_axes(construction_axis)
        evaluation_axes = self._tensor_axes(evaluation_axis)
        series = self._ordinary_series(
            size,
            self._transform(source_mesh, construction_values),
        )
        full_construction = self._evaluate(source_mesh, series, construction_axes)
        full_evaluation = self._evaluate(source_mesh, series, evaluation_axes)
        classification = metric_shell_classification(geometry, series.integer_modes)
        metric_indices = np.asarray(
            classification.metric_shell_values,
            dtype=np.int64,
        )
        metric_shell_values = tuple(
            value
            for value in sorted(set(classification.metric_shell_values))
            if value <= self._request.shell_cap
        )
        if not metric_shell_values or metric_shell_values[0] != 0:
            raise RuntimeError("selected shell cap must retain the onsite shell")
        locality = self._hopping_locality(
            model=model,
            channel=Periodic3DRankNHoppingLocalityChannelEnum.REFERENCE,
            series=series,
            metric_indices=metric_indices,
        )
        return _ReferenceFourierData(
            source_mesh=source_mesh,
            construction_axes=construction_axes,
            evaluation_axes=evaluation_axes,
            ordinary_series=series,
            full_construction=full_construction,
            full_evaluation=full_evaluation,
            shell_classification=classification,
            metric_indices=metric_indices,
            metric_shell_values=metric_shell_values,
            locality=locality,
            shell_evaluation_fields=tuple(
                iter_complete_shell_fields(
                    source_mesh,
                    series,
                    evaluation_axes,
                    metric_indices,
                    metric_shell_values,
                )
            ),
        )

    @staticmethod
    def _fitted_evidence(
        *analyses: Periodic3DRankNGlobalGaugeAlignmentAnalysis
        | Periodic3DRankNProcrustesAnalysis,
    ) -> Periodic3DRankNFittedAlignmentEvidence:
        owner_results = tuple(analysis.owner_result for analysis in analyses)
        return Periodic3DRankNFittedAlignmentEvidence(
            sample_count=sum(result.batch_size for result in owner_results),
            minimum_numerical_rank=min(
                int(np.min(result.numerical_ranks)) for result in owner_results
            ),
            minimum_cross_singular_value=min(
                float(np.min(result.cross_singular_values)) for result in owner_results
            ),
            maximum_optimal_residual_frobenius_norm=max(
                float(np.max(result.optimal_residual_frobenius_norms))
                for result in owner_results
            ),
            maximum_applied_rank_cutoff=max(
                float(np.max(result.applied_rank_cutoffs)) for result in owner_results
            ),
        )

    def _support_selection(
        self,
        outcome: SupportToleranceSelectionOutcome,
        metric_shell_values: tuple[int, ...],
    ) -> Periodic3DRankNSupportSelection:
        if type(outcome) is MinimumToleranceSatisfyingSupport:
            index = outcome.comparison_index
            return Periodic3DRankNSupportSelected(
                ordinal_shell_index=index,
                metric_shell_value=metric_shell_values[index],
                satisfying_error=outcome.satisfying_error,
                preceding_error=outcome.preceding_error,
            )
        if type(outcome) is SupportToleranceUnresolved:
            return Periodic3DRankNSupportUnresolved(
                comparison_count=outcome.comparison_count,
                minimum_observed_error=outcome.minimum_observed_error,
                largest_support_error=outcome.largest_support_error,
            )
        raise TypeError("support outcome must be an exact selected or unresolved value")

    def _decisions(
        self,
        *,
        model: Periodic3DRankNAnalyticCase,
        reference_errors: tuple[BandEquivalenceHoppingLocalityErrorChannels, ...],
        comparison_errors: tuple[BandEquivalenceHoppingLocalityErrorChannels, ...],
        reference: _ReferenceFourierData,
    ) -> tuple[Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision, ...]:
        decisions: list[
            Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision
        ] = []
        for tolerance in self._request.band_tolerances:
            reference_selection = Periodic3DRankNSupportTruncationAnalyzer(
                request=Periodic3DRankNSupportTruncationAnalysisRequest(
                    retained_rank=model.retained_rank,
                    channel=Periodic3DRankNSupportTruncationChannelEnum.REFERENCE,
                    support_inventory=reference.shell_classification.support_inventory,
                    total_errors=reference_errors,
                    tolerance=tolerance,
                )
            ).execute()
            comparison_selection = Periodic3DRankNSupportTruncationAnalyzer(
                request=Periodic3DRankNSupportTruncationAnalysisRequest(
                    retained_rank=model.retained_rank,
                    channel=Periodic3DRankNSupportTruncationChannelEnum.COMPARISON,
                    support_inventory=reference.shell_classification.support_inventory,
                    total_errors=comparison_errors,
                    tolerance=tolerance,
                )
            ).execute()
            decisions.append(
                Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision(
                    tolerance=tolerance,
                    reference_matrix=self._support_selection(
                        reference_selection.matrix_frobenius_maximum_error,
                        reference.metric_shell_values,
                    ),
                    reference_ordered_spectrum=self._support_selection(
                        reference_selection.ordered_eigenvalue_maximum_absolute_error,
                        reference.metric_shell_values,
                    ),
                    comparison_matrix=self._support_selection(
                        comparison_selection.matrix_frobenius_maximum_error,
                        reference.metric_shell_values,
                    ),
                    comparison_ordered_spectrum=self._support_selection(
                        comparison_selection.ordered_eigenvalue_maximum_absolute_error,
                        reference.metric_shell_values,
                    ),
                )
            )
        return tuple(decisions)

    def _qualified_alignment(
        self,
        *,
        model: Periodic3DRankNAnalyticCase,
        geometry: Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
        alignment: Periodic3DRankNGaugeAlignment,
        evidence: Periodic3DRankNFittedAlignmentEvidence
        | Periodic3DRankNPrescribedAlignmentEvidence,
        aligned_frame: Complex128Array,
        comparison_construction: Complex128Array,
        comparison_evaluation: Complex128Array,
        reference_construction: Complex128Array,
        reference_evaluation: Complex128Array,
        reference_frame: Complex128Array,
        reference: _ReferenceFourierData,
    ) -> (
        Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
        | Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis
    ):
        transport = Periodic3DRankNTransportAnalyzer(
            request=Periodic3DRankNTransportAnalysisRequest(
                retained_rank=model.retained_rank,
                frame=aligned_frame,
                rank_absolute=self._request.transport_rank_absolute,
                rank_relative=self._request.transport_rank_relative,
            )
        ).execute()
        if transport.rank_deficient_link_count > 0:
            return Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(  # noqa: E501
                identity=self._alignment_identity(model.retained_rank),
                alignment=alignment,
                reason=(
                    Periodic3DRankNAlignmentInapplicabilityEnum.TRANSPORT_LINK_RANK_DEFICIENT
                ),
                deficient_sample_count=transport.rank_deficient_link_count,
                minimum_numerical_rank=None,
            )
        if transport.maximum_absolute_closure_phases is None:
            raise RuntimeError("applicable transport must retain closure phases")
        if transport.maximum_plaquette_phase is None:
            raise RuntimeError("periodic-3D transport must retain a plaquette phase")
        comparison_series = self._ordinary_series(
            self._request.construction_size,
            self._transform(reference.source_mesh, comparison_construction),
        )
        if not np.array_equal(
            reference.ordinary_series.integer_modes,
            comparison_series.integer_modes,
        ):
            raise RuntimeError("reference and comparison Fourier inventories differ")
        comparison_full_construction = self._evaluate(
            reference.source_mesh,
            comparison_series,
            reference.construction_axes,
        )
        comparison_full_evaluation = self._evaluate(
            reference.source_mesh,
            comparison_series,
            reference.evaluation_axes,
        )
        comparison_locality = self._hopping_locality(
            model=model,
            channel=Periodic3DRankNHoppingLocalityChannelEnum.COMPARISON,
            series=comparison_series,
            metric_indices=reference.metric_indices,
        )
        comparison_shell_evaluation = tuple(
            iter_complete_shell_fields(
                reference.source_mesh,
                comparison_series,
                reference.evaluation_axes,
                reference.metric_indices,
                reference.metric_shell_values,
            )
        )
        shell_results: list[
            Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis
        ] = []
        reference_total_errors: list[BandEquivalenceHoppingLocalityErrorChannels] = []
        comparison_total_errors: list[BandEquivalenceHoppingLocalityErrorChannels] = []
        for ordinal, (metric_value, reference_eval, comparison_eval) in enumerate(
            zip(
                reference.metric_shell_values,
                reference.shell_evaluation_fields,
                comparison_shell_evaluation,
                strict=True,
            )
        ):
            retained = reference.metric_indices <= metric_value
            reference_truncation = error_channels(
                reference_eval,
                reference.full_evaluation,
            )
            comparison_truncation = error_channels(
                comparison_eval,
                comparison_full_evaluation,
            )
            reference_total = error_channels(reference_eval, reference_evaluation)
            comparison_total = error_channels(comparison_eval, comparison_evaluation)
            reference_total_errors.append(reference_total)
            comparison_total_errors.append(comparison_total)
            shell_results.append(
                Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis(
                    ordinal_shell_index=ordinal,
                    metric_shell_value=metric_value,
                    retained_block_count=int(np.count_nonzero(retained)),
                    reference_shell_power=reference.locality.normalized_power_at_shell(
                        metric_value
                    ),
                    comparison_shell_power=comparison_locality.normalized_power_at_shell(
                        metric_value
                    ),
                    reference_omitted_power=reference.locality.normalized_power_beyond_shell(
                        metric_value
                    ),
                    comparison_omitted_power=comparison_locality.normalized_power_beyond_shell(
                        metric_value
                    ),
                    reference_total_errors=self._error_record(reference_total),
                    comparison_total_errors=self._error_record(comparison_total),
                    reference_truncation_errors=self._error_record(
                        reference_truncation
                    ),
                    comparison_truncation_errors=self._error_record(
                        comparison_truncation
                    ),
                )
            )
        direct_spectrum_difference = float(
            np.max(
                np.abs(
                    np.linalg.eigvalsh(reference_evaluation)
                    - np.linalg.eigvalsh(comparison_evaluation)
                )
            )
        )
        return Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis(
            identity=self._alignment_identity(model.retained_rank),
            alignment=alignment,
            alignment_evidence=evidence,
            maximum_aligned_frame_defect=maximum_matrix_defect(
                aligned_frame,
                reference_frame,
            ),
            minimum_transport_singular_value=transport.minimum_singular_value,
            maximum_transport_procrustes_residual=(
                transport.maximum_procrustes_residual
            ),
            maximum_transport_unitarity_defect=transport.maximum_unitarity_defect,
            maximum_transport_rank_cutoff=transport.maximum_rank_cutoff,
            maximum_absolute_closure_phases=(transport.maximum_absolute_closure_phases),
            maximum_plaquette_phase=transport.maximum_plaquette_phase,
            maximum_direct_matrix_difference=maximum_matrix_defect(
                comparison_evaluation,
                reference_evaluation,
            ),
            maximum_direct_ordered_spectrum_difference=direct_spectrum_difference,
            reference_reconstruction_errors=self._error_record(
                error_channels(reference.full_construction, reference_construction)
            ),
            comparison_reconstruction_errors=self._error_record(
                error_channels(
                    comparison_full_construction,
                    comparison_construction,
                )
            ),
            reference_interpolation_errors=self._error_record(
                error_channels(reference.full_evaluation, reference_evaluation)
            ),
            comparison_interpolation_errors=self._error_record(
                error_channels(comparison_full_evaluation, comparison_evaluation)
            ),
            reference_locality=self._locality_summary(reference.locality),
            comparison_locality=self._locality_summary(comparison_locality),
            shells=tuple(shell_results),
            tolerance_decisions=self._decisions(
                model=model,
                reference_errors=tuple(reference_total_errors),
                comparison_errors=tuple(comparison_total_errors),
                reference=reference,
            ),
        )

    def _case(
        self,
        model: Periodic3DRankNAnalyticCase,
        geometry: Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
        construction: Float64Array,
        evaluation: Float64Array,
    ) -> Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis:
        reference_construction = model.exact_reduced_hamiltonians(construction)
        reference_evaluation = model.exact_reduced_hamiltonians(evaluation)
        reference_frame = model.reference_frames(construction)
        attacked_frame = model.attacked_frames(construction)
        attacked_construction = model.attacked_reduced_hamiltonians(construction)
        attacked_evaluation = model.attacked_reduced_hamiltonians(evaluation)
        reference = self._reference_fourier(
            model=model,
            geometry=geometry,
            construction_values=reference_construction,
        )
        alignments: list[
            Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
            | Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis
        ] = []
        for alignment in self._request.gauge_alignments:
            if alignment is Periodic3DRankNGaugeAlignment.IDENTITY:
                alignments.append(
                    self._qualified_alignment(
                        model=model,
                        geometry=geometry,
                        alignment=alignment,
                        evidence=Periodic3DRankNPrescribedAlignmentEvidence("identity"),
                        aligned_frame=attacked_frame,
                        comparison_construction=attacked_construction,
                        comparison_evaluation=attacked_evaluation,
                        reference_construction=reference_construction,
                        reference_evaluation=reference_evaluation,
                        reference_frame=reference_frame,
                        reference=reference,
                    )
                )
                continue
            if alignment is Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE:
                construction_action = model.known_inverse_right_actions(construction)
                evaluation_action = model.known_inverse_right_actions(evaluation)
                alignments.append(
                    self._qualified_alignment(
                        model=model,
                        geometry=geometry,
                        alignment=alignment,
                        evidence=Periodic3DRankNPrescribedAlignmentEvidence(
                            "known-inverse-oracle"
                        ),
                        aligned_frame=attacked_frame @ construction_action,
                        comparison_construction=self._apply_right_action(
                            attacked_construction,
                            construction_action,
                        ),
                        comparison_evaluation=self._apply_right_action(
                            attacked_evaluation,
                            evaluation_action,
                        ),
                        reference_construction=reference_construction,
                        reference_evaluation=reference_evaluation,
                        reference_frame=reference_frame,
                        reference=reference,
                    )
                )
                continue
            if alignment is Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY:
                global_analysis = Periodic3DRankNGlobalGaugeAlignmentAnalyzer(
                    request=Periodic3DRankNGlobalGaugeAlignmentAnalysisRequest(
                        retained_rank=model.retained_rank,
                        source=attacked_frame,
                        target=reference_frame,
                        tolerance=self._request.procrustes_tolerance,
                    )
                ).execute()
                outcome = global_analysis.selection_outcome
                if type(outcome) is Periodic3DRankNGlobalGaugeAlignmentRankDeficient:
                    alignments.append(
                        Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
                            identity=self._alignment_identity(model.retained_rank),
                            alignment=alignment,
                            reason=(
                                Periodic3DRankNAlignmentInapplicabilityEnum.AGGREGATE_RANK_DEFICIENT
                            ),
                            deficient_sample_count=1,
                            minimum_numerical_rank=outcome.numerical_rank,
                        )
                    )
                    continue
                if type(outcome) is not Periodic3DRankNGlobalGaugeAlignmentSelected:
                    raise RuntimeError("global alignment returned an unknown outcome")
                action = outcome.right_unitary
                alignments.append(
                    self._qualified_alignment(
                        model=model,
                        geometry=geometry,
                        alignment=alignment,
                        evidence=self._fitted_evidence(global_analysis),
                        aligned_frame=attacked_frame @ action,
                        comparison_construction=self._apply_right_action(
                            attacked_construction,
                            action,
                        ),
                        comparison_evaluation=self._apply_right_action(
                            attacked_evaluation,
                            action,
                        ),
                        reference_construction=reference_construction,
                        reference_evaluation=reference_evaluation,
                        reference_frame=reference_frame,
                        reference=reference,
                    )
                )
                continue
            construction_analysis = Periodic3DRankNProcrustesAnalyzer(
                request=Periodic3DRankNProcrustesAnalysisRequest(
                    retained_rank=model.retained_rank,
                    source=attacked_frame,
                    target=reference_frame,
                    tolerance=self._request.procrustes_tolerance,
                )
            ).execute()
            if construction_analysis.owner_result.rank_deficient_count > 0:
                alignments.append(
                    Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
                        identity=self._alignment_identity(model.retained_rank),
                        alignment=alignment,
                        reason=(
                            Periodic3DRankNAlignmentInapplicabilityEnum.POINTWISE_CONSTRUCTION_RANK_DEFICIENT
                        ),
                        deficient_sample_count=(
                            construction_analysis.owner_result.rank_deficient_count
                        ),
                        minimum_numerical_rank=int(
                            np.min(construction_analysis.owner_result.numerical_ranks)
                        ),
                    )
                )
                continue
            attacked_eval_frame = model.attacked_frames(evaluation)
            reference_eval_frame = model.reference_frames(evaluation)
            evaluation_analysis = Periodic3DRankNProcrustesAnalyzer(
                request=Periodic3DRankNProcrustesAnalysisRequest(
                    retained_rank=model.retained_rank,
                    source=attacked_eval_frame,
                    target=reference_eval_frame,
                    tolerance=self._request.procrustes_tolerance,
                )
            ).execute()
            if evaluation_analysis.owner_result.rank_deficient_count > 0:
                alignments.append(
                    Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
                        identity=self._alignment_identity(model.retained_rank),
                        alignment=alignment,
                        reason=(
                            Periodic3DRankNAlignmentInapplicabilityEnum.POINTWISE_EVALUATION_RANK_DEFICIENT
                        ),
                        deficient_sample_count=(
                            evaluation_analysis.owner_result.rank_deficient_count
                        ),
                        minimum_numerical_rank=int(
                            np.min(evaluation_analysis.owner_result.numerical_ranks)
                        ),
                    )
                )
                continue
            construction_action = (
                construction_analysis.owner_result.right_unitary_completions
            )
            evaluation_action = (
                evaluation_analysis.owner_result.right_unitary_completions
            )
            alignments.append(
                self._qualified_alignment(
                    model=model,
                    geometry=geometry,
                    alignment=alignment,
                    evidence=self._fitted_evidence(
                        construction_analysis,
                        evaluation_analysis,
                    ),
                    aligned_frame=attacked_frame @ construction_action,
                    comparison_construction=self._apply_right_action(
                        attacked_construction,
                        construction_action,
                    ),
                    comparison_evaluation=self._apply_right_action(
                        attacked_evaluation,
                        evaluation_action,
                    ),
                    reference_construction=reference_construction,
                    reference_evaluation=reference_evaluation,
                    reference_frame=reference_frame,
                    reference=reference,
                )
            )
        retained = model.retained_energies(construction)
        exterior = model.exterior_energies(construction)
        minimum_gap = float(
            np.min(exterior[..., 0] - retained[..., model.retained_rank - 1])
        )
        return Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis(
            model_identity=model.model_identity,
            case_identifier=model.case_identifier,
            retained_rank=model.retained_rank,
            circuit_depth=model.circuit_depth,
            parent_scale=model.parent_scale,
            attack_coefficient=model.attack_coefficient,
            minimum_sampled_external_gap=minimum_gap,
            alignments=tuple(alignments),
        )

    def execute(self) -> Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis:
        """Execute one analytic case without creating retained evidence."""
        construction = self._coordinates(self._request.construction_size, 0.5)
        evaluation = self._coordinates(
            self._request.evaluation_size,
            0.5 + self._request.evaluation_shift,
        )
        return self._case(
            self._model,
            self._geometry,
            construction,
            evaluation,
        )


@final
class Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer(
    Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzerRole[
        Periodic3DRankNBandEquivalenceHoppingLocalityRequest
    ]
):
    """Thinly expand and sequence one exact aggregate software request."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic3DRankNBandEquivalenceHoppingLocalityRequest,
    ) -> None:
        if type(request) is not Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
            raise TypeError("request must be the exact periodic-3D rank-N request")
        self._request = request

    @property
    def request(self) -> Periodic3DRankNBandEquivalenceHoppingLocalityRequest:
        """Return the immutable aggregate request bound to this action."""
        return self._request

    def execute(self) -> Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis:
        """Execute all analytic cases without creating retained evidence."""
        geometry_by_identifier = {case.identifier: case for case in self._request.cases}
        models = Periodic3DRankNBandEquivalenceHoppingLocalityCaseExpander(
            request=self._request
        ).execute()
        cases = tuple(
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer(
                request=self._request,
                model=model,
                geometry=geometry_by_identifier[model.case_identifier],
            ).execute()
            for model in models
        )
        return Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis(
            request=self._request,
            status=(
                Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum.SOFTWARE_QUALIFICATION_NOT_SCIENTIFIC_EVIDENCE
            ),
            cases=cases,
        )


__all__ = [
    "Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer",
    "Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer",
]
