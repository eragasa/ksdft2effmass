"""Aggregate correlation for the standalone optimizer-study records."""

from .numerics import OptimizerStandaloneEndpointEvaluator
from .records import (
    OptimizerStandaloneDecodedDocuments,
    OptimizerStandaloneEndpoint,
    OptimizerStandaloneGroup,
    OptimizerStandaloneProposal,
    OptimizerStandaloneReconstruction,
)

_EXPECTED_START_COUNT = 16
_EXPECTED_ENDPOINT_COUNT = 256
_EXPECTED_GROUP_COUNT = 16
_EXPECTED_CONTROL_STATUS = (
    "planned pre-execution control lacks a retained record; post-hoc exact-equivalence "
    "and threshold-sensitivity controls are reported without retroactive compliance"
)
_EXPECTED_DISPOSITION = (
    "does not support the frozen standalone finite-sequence criteria"
)


class OptimizerStandaloneSensitivityCorrelator:
    """Reconstruct direct rejected-pair sensitivity for one retained group."""

    __slots__ = ()

    def execute(
        self,
        proposal: OptimizerStandaloneProposal,
        group: OptimizerStandaloneGroup,
    ) -> None:
        """Require retained sensitivity counts and best-endpoint identities.

        Parameters
        ----------
        proposal
            Frozen basin thresholds.
        group
            One retained group with rejected comparisons and sensitivity records.

        Raises
        ------
        TypeError
            If either argument is not its exact immutable record type.
        AssertionError
            If a frozen-threshold rejection or sensitivity reconstruction disagrees.
        """
        if type(proposal) is not OptimizerStandaloneProposal:
            raise TypeError("proposal must be OptimizerStandaloneProposal")
        if type(group) is not OptimizerStandaloneGroup:
            raise TypeError("group must be OptimizerStandaloneGroup")
        candidates: list[tuple[str | None, float, float]] = []
        for basin in group.basins:
            for rejected in basin.rejected_equivalence_candidates:
                if (
                    rejected.center_set_periodic_distance <= proposal.center_tolerance
                    and rejected.maximum_density_l2_mismatch
                    <= proposal.density_tolerance
                ):
                    raise AssertionError("a threshold-passing pair was rejected")
                candidates.append(
                    (
                        basin.representative_start_id
                        if rejected.representative_start_id
                        == group.best_observed_start_id
                        else None,
                        rejected.center_set_periodic_distance,
                        rejected.maximum_density_l2_mismatch,
                    )
                )
        for record in group.sensitivity:
            matches = tuple(
                candidate
                for candidate in candidates
                if candidate[1] <= proposal.center_tolerance
                and candidate[2] <= record.density_l2_tolerance
            )
            if record.direct_matching_pair_count != len(matches):
                raise AssertionError("sensitivity direct-pair count disagrees")
            expected_ids = tuple(
                candidate[0] for candidate in matches if candidate[0] is not None
            )
            if record.best_endpoint_direct_match_start_ids != expected_ids:
                raise AssertionError("best-endpoint sensitivity identities disagree")
            if record.best_endpoint_direct_occupancy != 1 + len(expected_ids):
                raise AssertionError("best-endpoint sensitivity occupancy disagrees")


class Periodic2DOptimizerStandaloneCorrelator:
    """Correlate start design, endpoint transitions, groups, and claim boundaries."""

    __slots__ = ("endpoint_evaluator", "sensitivity_correlator")

    def __init__(self) -> None:
        """Create one correlator with independent endpoint and sensitivity owners."""
        self.endpoint_evaluator = OptimizerStandaloneEndpointEvaluator()
        self.sensitivity_correlator = OptimizerStandaloneSensitivityCorrelator()

    def execute(
        self, documents: OptimizerStandaloneDecodedDocuments
    ) -> OptimizerStandaloneReconstruction:
        """Reconstruct the bounded retained software and numerical relationships.

        Parameters
        ----------
        documents
            Closed immutable proposal, gauge-design, and result records.

        Returns
        -------
        OptimizerStandaloneReconstruction
            Independently accumulated endpoint and continuation counts.

        Raises
        ------
        TypeError
            If ``documents`` is not the exact decoded-record aggregate.
        AssertionError
            If any frozen count, identity, transition, aggregate, basin, threshold
            sensitivity, control, or claim-boundary relationship disagrees.
        """
        if type(documents) is not OptimizerStandaloneDecodedDocuments:
            raise TypeError("documents must be OptimizerStandaloneDecodedDocuments")
        starts = documents.gauge_design.start_ids
        if documents.gauge_design.declared_start_count != len(starts):
            raise AssertionError("declared start count disagrees")
        if len(starts) != _EXPECTED_START_COUNT or len(set(starts)) != len(starts):
            raise AssertionError("expected 16 unique deterministic starts")
        endpoints = documents.result.endpoints
        endpoint_keys = {
            (endpoint.configuration_id, endpoint.arm, endpoint.start_id)
            for endpoint in endpoints
        }
        if len(endpoints) != _EXPECTED_ENDPOINT_COUNT or len(endpoint_keys) != len(
            endpoints
        ):
            raise AssertionError("expected 256 uniquely identified endpoints")
        continuation_count = 0
        effective_converged_count = 0
        diagnostic_counts: dict[str, int] = {}
        for endpoint in endpoints:
            if endpoint.start_id not in starts:
                raise AssertionError("endpoint uses an undeclared start identity")
            if endpoint.start_index != starts.index(endpoint.start_id):
                raise AssertionError("endpoint start index disagrees")
            classification = self.endpoint_evaluator.execute(endpoint)
            continuation_count += int(endpoint.continuation_applied)
            effective_converged_count += int(endpoint.effective_native_converged)
            if not endpoint.effective_native_converged:
                diagnostic_counts[classification] = (
                    diagnostic_counts.get(classification, 0) + 1
                )
        self._check_summary(
            documents,
            continuation_count,
            effective_converged_count,
            diagnostic_counts,
        )
        self._check_groups(documents)
        self._check_claim_boundary(documents)
        return OptimizerStandaloneReconstruction(
            endpoint_count=len(endpoints),
            continuation_count=continuation_count,
            effective_converged_count=effective_converged_count,
            final_nonconverged_count=len(endpoints) - effective_converged_count,
        )

    def _check_summary(
        self,
        documents: OptimizerStandaloneDecodedDocuments,
        continuation_count: int,
        effective_converged_count: int,
        diagnostic_counts: dict[str, int],
    ) -> None:
        """Require independently accumulated endpoint counts to match the summary."""
        endpoints = documents.result.endpoints
        summary = documents.result.summary
        expected = (
            (summary.initial_localization_count, len(endpoints)),
            (
                summary.initial_process_completion_count,
                sum(endpoint.initial_process_completed for endpoint in endpoints),
            ),
            (
                summary.initial_native_converged_count,
                sum(endpoint.initial_native_converged for endpoint in endpoints),
            ),
            (summary.continuation_count, continuation_count),
            (
                summary.continuation_native_converged_count,
                sum(
                    endpoint.continuation_native_converged is True
                    for endpoint in endpoints
                ),
            ),
            (summary.effective_native_converged_count, effective_converged_count),
            (
                summary.effective_native_nonconverged_count,
                len(endpoints) - effective_converged_count,
            ),
        )
        if any(actual != reconstructed for actual, reconstructed in expected):
            raise AssertionError("execution summary counts disagree")
        represented = dict(summary.diagnostic_counts)
        if len(represented) != len(summary.diagnostic_counts):
            raise AssertionError("diagnostic labels must be unique")
        if represented != diagnostic_counts:
            raise AssertionError("nonconvergence diagnostic counts disagree")

    def _check_groups(self, documents: OptimizerStandaloneDecodedDocuments) -> None:
        """Require each group to reconstruct its endpoints, basins, and controls."""
        groups = documents.result.groups
        group_keys = {(group.configuration_id, group.arm) for group in groups}
        if len(groups) != _EXPECTED_GROUP_COUNT or len(group_keys) != len(groups):
            raise AssertionError("expected 16 uniquely identified groups")
        for group in groups:
            self._check_group(documents, group)

    def _check_group(
        self,
        documents: OptimizerStandaloneDecodedDocuments,
        group: OptimizerStandaloneGroup,
    ) -> None:
        """Reconstruct one group's count, best endpoint, and basin relationships."""
        starts = documents.gauge_design.start_ids
        selected = tuple(
            endpoint
            for endpoint in documents.result.endpoints
            if endpoint.configuration_id == group.configuration_id
            and endpoint.arm == group.arm
        )
        if len(selected) != len(starts):
            raise AssertionError("group endpoint count disagrees")
        selected_start_ids = tuple(endpoint.start_id for endpoint in selected)
        if len(set(selected_start_ids)) != len(selected_start_ids) or set(
            selected_start_ids
        ) != set(starts):
            raise AssertionError("group start identities disagree")
        converged = tuple(
            endpoint for endpoint in selected if endpoint.effective_native_converged
        )
        if not converged:
            raise AssertionError("group has no converged endpoint for retained best")
        if group.initial_native_converged_count != sum(
            endpoint.initial_native_converged for endpoint in selected
        ):
            raise AssertionError("group initial convergence count disagrees")
        if group.effective_native_converged_count != len(converged):
            raise AssertionError("group effective convergence count disagrees")
        if group.effective_native_converged_fraction != len(converged) / len(selected):
            raise AssertionError("group effective convergence fraction disagrees")
        expected_nonconverged = {
            endpoint.start_id
            for endpoint in selected
            if not endpoint.effective_native_converged
        }
        represented_nonconverged = set(group.effective_nonconverged_start_ids)
        if (
            len(represented_nonconverged) != len(group.effective_nonconverged_start_ids)
            or represented_nonconverged != expected_nonconverged
        ):
            raise AssertionError("group nonconverged identities disagree")
        best = min(
            converged,
            key=lambda endpoint: (
                endpoint.effective_native_endpoint.omega_tilde_cell_squared,
                endpoint.start_id,
            ),
        )
        if group.best_observed_start_id != best.start_id:
            raise AssertionError("group best endpoint disagrees")
        if group.declared_basin_count != len(group.basins) or not group.basins:
            raise AssertionError("group basin count disagrees")
        members = tuple(
            start_id for basin in group.basins for start_id in basin.start_ids
        )
        if len(set(members)) != len(members) or sorted(members) != sorted(
            endpoint.start_id for endpoint in converged
        ):
            raise AssertionError("basins do not partition converged endpoints")
        self._check_basin_membership(documents, group, converged)
        best_basins = tuple(
            basin for basin in group.basins if best.start_id in basin.start_ids
        )
        if len(best_basins) != 1:
            raise AssertionError("best endpoint must belong to exactly one basin")
        best_basin = best_basins[0]
        expected_pass = (
            best_basin.occupancy >= documents.proposal.best_basin_minimum_occupancy
            and best_basin.appears_in_both_start_blocks
        )
        if group.best_basin_criterion_pass != expected_pass:
            raise AssertionError("best-basin criterion disagrees")
        self.sensitivity_correlator.execute(documents.proposal, group)
        self._check_controls(documents, group)

    def _check_basin_membership(
        self,
        documents: OptimizerStandaloneDecodedDocuments,
        group: OptimizerStandaloneGroup,
        converged: tuple[OptimizerStandaloneEndpoint, ...],
    ) -> None:
        """Reconstruct basin order, member diagnostics, and start-block presence."""
        endpoint_by_start = {endpoint.start_id: endpoint for endpoint in converged}
        basin_by_start = {
            start_id: basin for basin in group.basins for start_id in basin.start_ids
        }
        ordered_endpoints = sorted(
            converged,
            key=lambda endpoint: (
                endpoint.effective_native_endpoint.omega_tilde_cell_squared,
                endpoint.start_id,
            ),
        )
        ordered_basins = []
        for endpoint in ordered_endpoints:
            basin = basin_by_start[endpoint.start_id]
            if basin not in ordered_basins:
                if endpoint.start_id != basin.representative_start_id:
                    raise AssertionError(
                        "basin representative is not its first endpoint"
                    )
                ordered_basins.append(basin)
        if tuple(ordered_basins) != group.basins:
            raise AssertionError("basin order disagrees with converged endpoints")
        starts = documents.gauge_design.start_ids
        for index, basin in enumerate(group.basins, start=1):
            if basin.basin_id != f"density_d4_basin_{index:02d}":
                raise AssertionError("basin identity sequence disagrees")
            if (
                not basin.start_ids
                or basin.start_ids[0] != basin.representative_start_id
                or basin.occupancy != len(basin.start_ids)
            ):
                raise AssertionError("basin occupancy or representative disagrees")
            representative = endpoint_by_start[basin.representative_start_id]
            if (
                basin.representative_omega_tilde_cell_squared
                != representative.effective_native_endpoint.omega_tilde_cell_squared
            ):
                raise AssertionError("basin representative spread disagrees")
            member_ids = tuple(
                diagnostic.start_id
                for diagnostic in basin.member_equivalence_diagnostics
            )
            if member_ids != basin.start_ids[1:]:
                raise AssertionError("basin member diagnostics disagree")
            for diagnostic in basin.member_equivalence_diagnostics:
                if (
                    diagnostic.center_set_periodic_distance < 0.0
                    or diagnostic.maximum_density_l2_mismatch < 0.0
                    or diagnostic.center_set_periodic_distance
                    > documents.proposal.center_tolerance
                    or diagnostic.maximum_density_l2_mismatch
                    > documents.proposal.density_tolerance
                ):
                    raise AssertionError("basin member fails frozen thresholds")
            expected_blocks = tuple(
                sorted(
                    {
                        0 if starts.index(start_id) <= 7 else 1
                        for start_id in basin.start_ids
                    }
                )
            )
            if basin.start_blocks_present != expected_blocks:
                raise AssertionError("basin start-block presence disagrees")
            if basin.appears_in_both_start_blocks != (expected_blocks == (0, 1)):
                raise AssertionError("basin both-block flag disagrees")
            expected_rejected_ids = tuple(
                previous.representative_start_id
                for previous in group.basins[: index - 1]
                if abs(
                    basin.representative_omega_tilde_cell_squared
                    - previous.representative_omega_tilde_cell_squared
                )
                <= documents.proposal.spread_tolerance
            )
            represented_rejected_ids = tuple(
                rejected.representative_start_id
                for rejected in basin.rejected_equivalence_candidates
            )
            if represented_rejected_ids != expected_rejected_ids:
                raise AssertionError("basin rejected-comparison sequence disagrees")

    def _check_controls(
        self,
        documents: OptimizerStandaloneDecodedDocuments,
        group: OptimizerStandaloneGroup,
    ) -> None:
        """Reconstruct post-hoc control maxima and frozen-threshold flags."""
        controls = group.controls
        if controls.declared_count != len(controls.observations):
            raise AssertionError("post-hoc control count disagrees")
        if not controls.observations:
            raise AssertionError("post-hoc controls must be nonempty")
        maximum_center = max(
            observation.center_set_periodic_distance
            for observation in controls.observations
        )
        maximum_density = max(
            observation.maximum_density_l2_mismatch
            for observation in controls.observations
        )
        if controls.maximum_center_distance != maximum_center:
            raise AssertionError("post-hoc center maximum disagrees")
        if controls.maximum_density_mismatch != maximum_density:
            raise AssertionError("post-hoc density maximum disagrees")
        if controls.passes_center_tolerance != (
            maximum_center <= documents.proposal.center_tolerance
        ):
            raise AssertionError("post-hoc center threshold flag disagrees")
        if controls.passes_density_tolerance != (
            maximum_density <= documents.proposal.density_tolerance
        ):
            raise AssertionError("post-hoc density threshold flag disagrees")

    def _check_claim_boundary(
        self, documents: OptimizerStandaloneDecodedDocuments
    ) -> None:
        """Require the exact retained negative and non-global claim boundary."""
        result = documents.result
        if result.basin_tolerance_control_status != _EXPECTED_CONTROL_STATUS:
            raise AssertionError("basin-control protocol deviation changed")
        if result.supports_declared_convergence:
            raise AssertionError("negative convergence disposition changed")
        if (
            not result.not_global_optimizer_convergence
            or not result.not_general_wannier_convergence
        ):
            raise AssertionError("optimizer claim boundary changed")
        if result.convergence_disposition != _EXPECTED_DISPOSITION:
            raise AssertionError("convergence disposition text changed")
