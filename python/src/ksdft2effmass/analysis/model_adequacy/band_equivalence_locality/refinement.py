"""Three-level refinement diagnostics for dimensional development replications."""

from __future__ import annotations

import math

from .analysis import BandEquivalenceLocalityAnalysis
from .refinement_records import (
    BandEquivalenceLocalityRefinementAssessment,
    BandEquivalenceLocalityRefinementPair,
)
from .results import BandEquivalenceLocalityPointAnalysis


def _maximum_change(coarse: tuple[float, ...], fine: tuple[float, ...]) -> float:
    if len(coarse) != len(fine):
        raise ValueError("refinement diagnostic inventories differ")
    return max(
        (abs(left - right) for left, right in zip(coarse, fine, strict=True)),
        default=0.0,
    )


def _periodic_angle_change(left: float, right: float) -> float:
    return abs((left - right + 0.5 * math.pi) % math.pi - 0.5 * math.pi)


def _parent_diagnostics(
    point: BandEquivalenceLocalityPointAnalysis,
) -> tuple[float, ...]:
    return (
        point.minimum_sampled_external_gap,
        point.continuous_external_gap_lower_bound,
        point.minimum_seed_overlap,
        point.maximum_parent_hermiticity_defect,
        point.maximum_eigensystem_reconstruction_defect,
        point.maximum_frame_orthonormality_defect,
        point.maximum_projector_reconstruction_defect,
        point.maximum_parent_retained_reconstruction_defect,
        point.maximum_parent_fourier_reconstruction_defect,
        point.maximum_periodic_frame_closure_defect,
        point.minimum_sampled_transport_singular_value,
        point.maximum_transport_procrustes_residual,
        point.maximum_transport_squared_residual_roundoff_cutoff,
        point.maximum_transport_unitarity_defect,
        point.maximum_transport_rank_cutoff,
        float(point.transport_rank_deficient_link_count),
    )


def _invariant_diagnostics(
    point: BandEquivalenceLocalityPointAnalysis,
) -> tuple[float, ...]:
    return (
        point.minimum_sampled_external_gap,
        point.continuous_external_gap_lower_bound,
        point.minimum_seed_overlap,
    )


def _reconstruction_diagnostics(
    point: BandEquivalenceLocalityPointAnalysis,
) -> tuple[float, ...]:
    return (
        point.maximum_eigensystem_reconstruction_defect,
        point.maximum_projector_reconstruction_defect,
        point.maximum_parent_retained_reconstruction_defect,
        point.maximum_parent_fourier_reconstruction_defect,
        point.reference_fourier_reconstruction_defect,
        point.comparison_fourier_reconstruction_defect,
    )


def _topology_diagnostic_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> tuple[bool, float]:
    stable = (
        coarse.transport_closure_and_plaquette_applicable
        == fine.transport_closure_and_plaquette_applicable
    )
    if not stable:
        return False, 0.0
    if not coarse.transport_closure_and_plaquette_applicable:
        return (
            coarse.transport_closure_and_plaquette_inapplicable_reason
            == fine.transport_closure_and_plaquette_inapplicable_reason,
            0.0,
        )
    coarse_phases = coarse.maximum_absolute_closure_holonomy_phases
    fine_phases = fine.maximum_absolute_closure_holonomy_phases
    coarse_closure = coarse.maximum_closure_holonomy_unitarity_defect
    fine_closure = fine.maximum_closure_holonomy_unitarity_defect
    coarse_plaquette = coarse.maximum_plaquette_holonomy_phase
    fine_plaquette = fine.maximum_plaquette_holonomy_phase
    if (
        coarse_phases is None
        or fine_phases is None
        or coarse_closure is None
        or fine_closure is None
        or coarse_plaquette is None
        or fine_plaquette is None
    ):
        raise ValueError("applicable transport is missing topology diagnostics")
    return True, max(
        _maximum_change(coarse_phases, fine_phases),
        abs(coarse_closure - fine_closure),
        abs(coarse_plaquette - fine_plaquette),
    )


def _validate_point_pair(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> None:
    if (coarse.parent_scale, coarse.amplitude) != (fine.parent_scale, fine.amplitude):
        raise ValueError("refinement point identities differ")


def _parent_diagnostic_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> float:
    _, topology_change = _topology_diagnostic_change(coarse, fine)
    return max(
        _maximum_change(_parent_diagnostics(coarse), _parent_diagnostics(fine)),
        topology_change,
    )


def _correlation_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> float:
    if (
        coarse.finite_mesh_maximum_correlation is None
        or fine.finite_mesh_maximum_correlation is None
    ):
        return 0.0
    return abs(
        coarse.finite_mesh_maximum_correlation - fine.finite_mesh_maximum_correlation
    )


def _threshold_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> float:
    return max(
        abs(coarse.minimum_operator_threshold - fine.minimum_operator_threshold),
        abs(
            coarse.exact_spectrum_joint_operator_threshold
            - fine.exact_spectrum_joint_operator_threshold
        ),
    )


def _hopping_weight_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> float:
    return max(
        abs(coarse.reference_nononsite_power - fine.reference_nononsite_power),
        abs(coarse.comparison_nononsite_power - fine.comparison_nononsite_power),
    )


def _hopping_block_power_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> float:
    fine_shells = {shell.shell_index: shell for shell in fine.shell_diagnostics}
    changes: list[float] = []
    for coarse_shell in coarse.shell_diagnostics:
        fine_shell = fine_shells.get(coarse_shell.shell_index)
        if fine_shell is not None:
            changes.extend(
                (
                    abs(
                        coarse_shell.reference_shell_power
                        - fine_shell.reference_shell_power
                    ),
                    abs(
                        coarse_shell.comparison_shell_power
                        - fine_shell.comparison_shell_power
                    ),
                )
            )
    return max(changes, default=0.0)


def _angle_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> float:
    if (
        coarse.restricted_global_rotation_angle is None
        or fine.restricted_global_rotation_angle is None
    ):
        return 0.0
    return _periodic_angle_change(
        coarse.restricted_global_rotation_angle,
        fine.restricted_global_rotation_angle,
    )


def _band_defect_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> float:
    return abs(coarse.maximum_direct_band_defect - fine.maximum_direct_band_defect)


def _reconstruction_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> float:
    return _maximum_change(
        _reconstruction_diagnostics(coarse), _reconstruction_diagnostics(fine)
    )


def _parseval_change(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> float:
    return max(
        abs(coarse.reference_parseval_defect - fine.reference_parseval_defect),
        abs(coarse.comparison_parseval_defect - fine.comparison_parseval_defect),
    )


def _decision_changes(
    coarse: BandEquivalenceLocalityPointAnalysis,
    fine: BandEquivalenceLocalityPointAnalysis,
) -> tuple[bool, int | None]:
    if len(coarse.first_passing) != len(fine.first_passing):
        raise ValueError("refinement decision inventories differ")
    stable = True
    changes: list[int] = []
    for left, right in zip(coarse.first_passing, fine.first_passing, strict=True):
        if left.tolerance != right.tolerance:
            raise ValueError("refinement tolerances differ")
        for coarse_shell, fine_shell in (
            (left.reference_band_shell, right.reference_band_shell),
            (left.comparison_band_shell, right.comparison_band_shell),
            (left.reference_hamiltonian_shell, right.reference_hamiltonian_shell),
            (left.comparison_hamiltonian_shell, right.comparison_hamiltonian_shell),
        ):
            stable = stable and coarse_shell == fine_shell
            if coarse_shell is not None and fine_shell is not None:
                changes.append(abs(coarse_shell - fine_shell))
    return stable, max(changes) if changes else None


class BandEquivalenceLocalityRefinementAnalyzer:
    """Compare bound mesh levels without inventing convergence tolerances."""

    __slots__ = ("_results",)

    def __init__(
        self,
        *,
        results: tuple[BandEquivalenceLocalityAnalysis, ...],
    ) -> None:
        if type(results) is not tuple or len(results) < 3:
            raise ValueError("results must contain at least three mesh levels")
        if any(
            type(result) is not BandEquivalenceLocalityAnalysis for result in results
        ):
            raise TypeError(
                "results must contain BandEquivalenceLocalityAnalysis values"
            )
        self._results = results

    @property
    def results(self) -> tuple[BandEquivalenceLocalityAnalysis, ...]:
        """Return the exact ordered diagnostics bound to this analyzer."""
        return self._results

    def execute(self) -> BandEquivalenceLocalityRefinementAssessment:
        results = self._results
        family = results[0].family
        if any(result.family is not family for result in results):
            raise ValueError("all refinement results must belong to one family")
        sizes = tuple(result.construction_size for result in results)
        if any(
            fine != 2 * coarse
            for coarse, fine in zip(sizes[:-1], sizes[1:], strict=True)
        ):
            raise ValueError("construction sizes must form a doubling ladder")
        pairs: list[BandEquivalenceLocalityRefinementPair] = []
        for coarse_result, fine_result in zip(results[:-1], results[1:], strict=True):
            point_pairs: list[
                tuple[
                    BandEquivalenceLocalityPointAnalysis,
                    BandEquivalenceLocalityPointAnalysis,
                ]
            ] = []
            decision_stability: list[bool] = []
            transport_applicability_stability: list[bool] = []
            decision_changes: list[int] = []
            for coarse_case, fine_case in zip(
                coarse_result.cases, fine_result.cases, strict=True
            ):
                if coarse_case.name != fine_case.name:
                    raise ValueError("refinement case identities differ")
                for coarse_point, fine_point in zip(
                    coarse_case.points, fine_case.points, strict=True
                ):
                    _validate_point_pair(coarse_point, fine_point)
                    point_pairs.append((coarse_point, fine_point))
                    topology_stable, _ = _topology_diagnostic_change(
                        coarse_point, fine_point
                    )
                    transport_applicability_stability.append(topology_stable)
                    stable, maximum_change = _decision_changes(coarse_point, fine_point)
                    decision_stability.append(stable)
                    if maximum_change is not None:
                        decision_changes.append(maximum_change)
            maximum_parent_change = max(
                (
                    _parent_diagnostic_change(coarse, fine)
                    for coarse, fine in point_pairs
                ),
                default=0.0,
            )
            maximum_invariant_change = max(
                (
                    _maximum_change(
                        _invariant_diagnostics(coarse),
                        _invariant_diagnostics(fine),
                    )
                    for coarse, fine in point_pairs
                ),
                default=0.0,
            )
            maximum_correlation_change = max(
                (_correlation_change(coarse, fine) for coarse, fine in point_pairs),
                default=0.0,
            )
            maximum_threshold_change = max(
                (_threshold_change(coarse, fine) for coarse, fine in point_pairs),
                default=0.0,
            )
            maximum_hopping_change = max(
                (_hopping_weight_change(coarse, fine) for coarse, fine in point_pairs),
                default=0.0,
            )
            maximum_block_change = max(
                (
                    _hopping_block_power_change(coarse, fine)
                    for coarse, fine in point_pairs
                ),
                default=0.0,
            )
            maximum_angle_change = max(
                (_angle_change(coarse, fine) for coarse, fine in point_pairs),
                default=0.0,
            )
            maximum_band_change = max(
                (_band_defect_change(coarse, fine) for coarse, fine in point_pairs),
                default=0.0,
            )
            maximum_reconstruction_change = max(
                (_reconstruction_change(coarse, fine) for coarse, fine in point_pairs),
                default=0.0,
            )
            maximum_parseval_change = max(
                (_parseval_change(coarse, fine) for coarse, fine in point_pairs),
                default=0.0,
            )
            pairs.append(
                BandEquivalenceLocalityRefinementPair(
                    coarse_construction_size=coarse_result.construction_size,
                    fine_construction_size=fine_result.construction_size,
                    maximum_parent_diagnostic_change=maximum_parent_change,
                    maximum_final_parent_invariant_change=maximum_invariant_change,
                    maximum_correlation_change=maximum_correlation_change,
                    maximum_threshold_change=maximum_threshold_change,
                    maximum_hopping_weight_change=maximum_hopping_change,
                    maximum_hopping_block_power_change=maximum_block_change,
                    maximum_angle_change=maximum_angle_change,
                    maximum_band_defect=maximum_band_change,
                    maximum_reconstruction_defect=maximum_reconstruction_change,
                    maximum_parseval_defect=maximum_parseval_change,
                    maximum_final_outcome_change=(
                        max(decision_changes) if decision_changes else None
                    ),
                    first_passing_dispositions_stable=all(decision_stability),
                    transport_closure_and_plaquette_applicability_stable=all(
                        transport_applicability_stability
                    ),
                    shared_mesh_quantities_applicable=False,
                    shared_mesh_inapplicable_reason=(
                        "half-step Monkhorst--Pack doubling meshes have no "
                        "shared nodes; "
                        "shared-node eigenvalue and projector defects are inapplicable"
                    ),
                    maximum_shared_parent_eigenvalue_defect=None,
                    maximum_shared_projector_defect=None,
                    within_draft_tolerances=None,
                    tolerance_disposition_reason=(
                        "channel-specific refinement tolerances were not prospectively "
                        "frozen for these replaceable development actions"
                    ),
                )
            )
        return BandEquivalenceLocalityRefinementAssessment(
            family=family,
            refinements=tuple(pairs),
            required_stable_refinements=2,
            momentum_disposition="unresolved",
            momentum_disposition_reason=(
                "three levels are available, but catalog-wide channel tolerances were "
                "not prospectively frozen"
            ),
            passes_draft_tolerance=None,
            passes_unit_scale_draft_tolerance=None,
            tolerance_inapplicable_reason=(
                "Paper 2 family-owned alignment and refinement tolerances were not "
                "prospectively frozen; Paper 1 tolerances are not transferred"
            ),
            paper1_literal_range_endpoints_applicable=False,
            paper1_literal_range_endpoints_inapplicable_reason=(
                "Paper 1 ranges 0, 8, and 16 are one-dimensional absolute-displacement "
                "cutoffs; Paper 2 uses geometry-owned complete physical-metric shells"
            ),
        )


__all__ = ["BandEquivalenceLocalityRefinementAnalyzer"]
