"""Exact-byte independent verification for constrained admissible sets."""

from __future__ import annotations

from typing import ClassVar

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.model_systems.analysis import BaseModelAnalysisVerifier
from ksdft2effmass.model_systems.verification import VisualizationProjectionVerification
from ksdft2effmass.verification import (
    CompositeVerification,
    MaximumAbsoluteErrorComparison,
)

from ..rank2.band_alignment.composite import Periodic1DCompositeBandAlignmentVerifier
from .reference import (
    Periodic1DConstrainedAdmissibleSetIndependentReferenceAnalyzer,
    Periodic1DConstrainedAdmissibleSetIndependentReferenceRequest,
)
from .results import Periodic1DConstrainedAdmissibleSetCalculationResult
from .verification import (
    ConstrainedAdmissibleSetUpstreamVerification,
    ConstrainedAdmissibleSetVerification,
    Periodic1DConstrainedAdmissibleSetVerification,
)
from .visualizations import (
    Periodic1DAdmissibleSetProofPointVisualizationData,
    Periodic1DConstrainedAdmissibleSetVisualizationData,
)


class Periodic1DConstrainedAdmissibleSetVerifier(
    BaseModelAnalysisVerifier[
        Periodic1DConstrainedAdmissibleSetCalculationResult,
        Periodic1DConstrainedAdmissibleSetVerification,
        Periodic1DConstrainedAdmissibleSetVisualizationData,
    ]
):
    """Own exact M3 bytes and compose a closed independent verification inventory."""

    __slots__ = ()

    verification_inventory: ClassVar[
        tuple[tuple[type[CompositeVerification], frozenset[str]], ...]
    ] = (
        (
            ConstrainedAdmissibleSetUpstreamVerification,
            frozenset(
                {
                    "upstream_subject_sha256",
                    "upstream_verification_passed",
                }
            ),
        ),
        (
            ConstrainedAdmissibleSetVerification,
            frozenset(
                {
                    "result_spectral_channel_id_error",
                    "result_spectral_alignment_identity_error",
                    "result_spectral_center_maximum_absolute_error",
                    "result_spectral_matrix_maximum_absolute_error",
                    "result_spectral_minimum_squared_loss_absolute_error",
                    "result_operator_count_error",
                    "result_operator_channel_id_error",
                    "result_operator_alignment_angle_maximum_absolute_error",
                    "result_operator_center_maximum_absolute_error",
                    "result_operator_matrix_maximum_absolute_error",
                    "result_operator_minimum_squared_loss_maximum_absolute_error",
                    "result_compatible_threshold_case_id_error",
                    "result_compatible_threshold_values_maximum_absolute_error",
                    "result_compatible_disposition_error",
                    "result_compatible_feasible_angle_count_error",
                    "result_compatible_feasible_angles_maximum_absolute_error",
                    "result_compatible_common_witness_presence_error",
                    "result_compatible_separation_values_maximum_absolute_error",
                    "result_compatible_evaluation_roles_error",
                    "result_compatible_evaluation_parameters_maximum_absolute_error",
                    "result_compatible_evaluation_angles_maximum_absolute_error",
                    "result_compatible_evaluation_losses_maximum_absolute_error",
                    "result_compatible_locality_ranges_maximum_absolute_error",
                    "result_compatible_cyclic_conversion_powers_maximum_absolute_error",
                    "result_compatible_ordinary_omitted_block_l2_norms_maximum_absolute_error",
                    "result_separated_threshold_case_id_error",
                    "result_separated_threshold_values_maximum_absolute_error",
                    "result_separated_disposition_error",
                    "result_separated_feasible_angle_count_error",
                    "result_separated_feasible_angles_maximum_absolute_error",
                    "result_separated_common_witness_presence_error",
                    "result_separated_separation_values_maximum_absolute_error",
                    "result_separated_evaluation_roles_error",
                    "result_separated_evaluation_parameters_maximum_absolute_error",
                    "result_separated_evaluation_angles_maximum_absolute_error",
                    "result_separated_evaluation_losses_maximum_absolute_error",
                    "result_separated_locality_ranges_maximum_absolute_error",
                    "result_separated_cyclic_conversion_powers_maximum_absolute_error",
                    "result_separated_ordinary_omitted_block_l2_norms_maximum_absolute_error",
                }
            ),
        ),
        (
            VisualizationProjectionVerification,
            frozenset(
                {
                    "visualization_parameter_names_error",
                    "visualization_parameter_bounds_maximum_absolute_error",
                    "visualization_loss_channel_names_error",
                    "visualization_locality_channel_names_error",
                    "visualization_proof_point_count_error",
                    "visualization_threshold_case_ids_error",
                    "visualization_threshold_values_maximum_absolute_error",
                    "visualization_dispositions_error",
                    "visualization_separation_bounds_maximum_absolute_error",
                    "visualization_evaluation_roles_error",
                    "visualization_evaluation_parameters_maximum_absolute_error",
                    "visualization_evaluation_angles_maximum_absolute_error",
                    "visualization_evaluation_losses_maximum_absolute_error",
                    "visualization_locality_ranges_maximum_absolute_error",
                    "visualization_cyclic_conversion_powers_maximum_absolute_error",
                    "visualization_ordinary_omitted_block_l2_norms_maximum_absolute_error",
                }
            ),
        ),
    )

    @classmethod
    def _result_type(cls) -> type[Periodic1DConstrainedAdmissibleSetCalculationResult]:
        """Return the typed M3 root reconstructed by the shared boundary."""
        return Periodic1DConstrainedAdmissibleSetCalculationResult

    def _visualization_data(
        self,
    ) -> Periodic1DConstrainedAdmissibleSetVisualizationData:
        """Compose the projection from existing typed result sections."""
        result = self._result
        unit = Unitless()
        compatible, separated = result.cases
        proof_points: list[Periodic1DAdmissibleSetProofPointVisualizationData] = []
        for case, evaluation in (
            (compatible, compatible.spectral_certificate_point),
            (separated, separated.spectral_certificate_point),
            (separated, separated.operator_certificate_point),
        ):
            proof_points.append(
                Periodic1DAdmissibleSetProofPointVisualizationData(
                    thresholds=case.thresholds,
                    disposition=case.disposition,
                    separation_bounds=VectorQuantity(
                        np.asarray(
                            (
                                case.separation_lower_bound,
                                case.separation_upper_bound,
                            )
                        ),
                        unit,
                    ),
                    evaluation=evaluation,
                )
            )
        return Periodic1DConstrainedAdmissibleSetVisualizationData(
            parameter_names=("energy_shift_ratio", "splitting_scale"),
            parameter_bounds=MatrixQuantity(
                np.asarray(
                    (
                        result.configuration.energy_shift_ratio_bounds,
                        result.configuration.splitting_scale_bounds,
                    )
                ),
                unit,
            ),
            loss_channel_names=("spectral", "operator"),
            locality_channel_names=("reference", "attacked", "candidate"),
            proof_points=(proof_points[0], proof_points[1], proof_points[2]),
        )

    def _verification_types(self) -> tuple[type[CompositeVerification], ...]:
        """Return the closed reusable verification class inventory."""
        return tuple(
            component_type for component_type, _ in self.verification_inventory
        )

    def _verification_components(
        self, visualization_data: Periodic1DConstrainedAdmissibleSetVisualizationData
    ) -> tuple[CompositeVerification, ...]:
        """Compose only explicitly admitted upstream, result, and projection checks."""
        unit = Unitless()
        zero = ScalarQuantity(0.0, unit)
        upstream = Periodic1DCompositeBandAlignmentVerifier(
            result_wire=self._result.composite_baseline.to_json()
        ).result()
        expected_digest = self._result.configuration.upstream_result_sha256
        independent = Periodic1DConstrainedAdmissibleSetIndependentReferenceAnalyzer(
            Periodic1DConstrainedAdmissibleSetIndependentReferenceRequest(
                self._result, visualization_data
            )
        ).execute()
        comparisons = dict(independent.comparisons)
        comparisons.update(
            {
                "upstream_subject_sha256": MaximumAbsoluteErrorComparison(
                    ScalarQuantity(
                        0.0
                        if upstream.verification.subject_sha256 == expected_digest
                        else 1.0,
                        unit,
                    ),
                    zero,
                    zero,
                ),
                "upstream_verification_passed": MaximumAbsoluteErrorComparison(
                    ScalarQuantity(
                        0.0 if upstream.verification.passed else 1.0,
                        unit,
                    ),
                    zero,
                    zero,
                ),
            }
        )
        admitted_names = frozenset(
            name
            for _, component_names in self.verification_inventory
            for name in component_names
        )
        if frozenset(comparisons) != admitted_names:
            raise ValueError(
                "independent comparisons must match the closed verification inventory"
            )
        return tuple(
            component_type.evaluate(
                {name: comparisons[name] for name in sorted(component_names)}
            )
            for component_type, component_names in self.verification_inventory
        )

    def _verification(
        self,
        *,
        visualization_data_sha256: str,
        components: tuple[CompositeVerification, ...],
    ) -> Periodic1DConstrainedAdmissibleSetVerification:
        """Compose the M3 aggregate from the closed component inventory."""
        return Periodic1DConstrainedAdmissibleSetVerification(
            self._subject_sha256, visualization_data_sha256, components
        )


__all__ = ["Periodic1DConstrainedAdmissibleSetVerifier"]
