"""Source, endpoint, and basin correlation for optimizer reanalysis."""

from dataclasses import dataclass

from ksdft2effmass.serialization.json import ImmutableJsonCodec

from .numerics import (
    OptimizerReanalysisBasinPartitioner,
    OptimizerReanalysisBasinPartitionRequest,
    OptimizerReanalysisEndpointSpreadVerifier,
)
from .records import (
    OptimizerReanalysisDecodedDocuments,
    OptimizerReanalysisEndpoint,
)


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisCorrelationResult:
    """Retain correlated endpoints for downstream refinement verification.

    Parameters
    ----------
    endpoints
        Nonempty immutable sequence of source-correlated reanalysis endpoints.
    """

    endpoints: tuple[OptimizerReanalysisEndpoint, ...]

    def __post_init__(self) -> None:
        """Require a nonempty immutable tuple of exact decoded endpoints."""
        if type(self.endpoints) is not tuple:
            raise TypeError("endpoints must be an exact tuple")
        if not self.endpoints:
            raise ValueError("endpoints must be nonempty")
        if any(
            type(value) is not OptimizerReanalysisEndpoint for value in self.endpoints
        ):
            raise TypeError("endpoints must contain exact reanalysis endpoint records")


class Periodic2DOptimizerReanalysisCorrelator:
    """Correlate source observations and reconstruct bounded basin diagnostics."""

    __slots__ = ("basin_partitioner", "immutable_json", "spread_verifier")

    def __init__(self) -> None:
        """Create one correlator with explicit numerical collaborators."""
        self.basin_partitioner = OptimizerReanalysisBasinPartitioner()
        self.immutable_json = ImmutableJsonCodec()
        self.spread_verifier = OptimizerReanalysisEndpointSpreadVerifier()

    def execute(
        self, documents: OptimizerReanalysisDecodedDocuments
    ) -> OptimizerReanalysisCorrelationResult:
        """Verify source correlation, spread diagnostics, basins, and best copies.

        Parameters
        ----------
        documents
            Strictly decoded immutable source and reanalysis records.

        Returns
        -------
        OptimizerReanalysisCorrelationResult
            Correlated endpoint records for refinement verification.

        Raises
        ------
        TypeError
            If ``documents`` has an incompatible exact type.
        AssertionError
            If identities, source values, spread arithmetic, classifications, basin
            membership, aggregate counts, or complete best-endpoint copies disagree.
        MemoryError
            If canonical comparison or dense permutation matching cannot allocate state.
        """
        if type(documents) is not OptimizerReanalysisDecodedDocuments:
            raise TypeError("documents must be OptimizerReanalysisDecodedDocuments")
        source = documents.source_result
        result = documents.reanalysis_result
        source_ids = tuple(item.configuration_id for item in source.configurations)
        result_ids = tuple(item.configuration_id for item in result.configurations)
        if len(source_ids) != len(set(source_ids)):
            raise AssertionError("source configurations must have unique identities")
        if len(result_ids) != len(set(result_ids)):
            raise AssertionError("result configurations must have unique identities")
        if set(source_ids) != set(result_ids):
            raise AssertionError("configuration identities disagree")
        source_by_id = {item.configuration_id: item for item in source.configurations}

        observed_counts: dict[str, int] = {}
        correlated_endpoints: list[OptimizerReanalysisEndpoint] = []
        for configuration in result.configurations:
            identifier = configuration.configuration_id
            source_configuration = source_by_id[identifier]
            if (
                configuration.plane_wave_cutoff
                != source_configuration.plane_wave_cutoff
            ):
                raise AssertionError(f"{identifier}:plane_wave_cutoff changed")
            if (
                configuration.reciprocal_mesh_size
                != source_configuration.reciprocal_mesh_size
            ):
                raise AssertionError(f"{identifier}:reciprocal_mesh_size changed")
            if (
                configuration.transverse_lattice_length
                != source_configuration.transverse_lattice_length
            ):
                raise AssertionError(f"{identifier}:embedding changed")

            source_gauges = tuple(
                start.gauge_id for start in source_configuration.starts
            )
            result_gauges = tuple(start.gauge_id for start in configuration.starts)
            if len(source_gauges) != len(set(source_gauges)):
                raise AssertionError(
                    f"{identifier}:source starts must have unique identities"
                )
            if len(result_gauges) != len(set(result_gauges)):
                raise AssertionError(
                    f"{identifier}:reanalysis starts must have unique identities"
                )
            if set(source_gauges) != set(result_gauges):
                raise AssertionError(f"{identifier}: endpoint identities disagree")
            source_starts = {
                start.gauge_id: start for start in source_configuration.starts
            }

            for endpoint in configuration.starts:
                if endpoint.configuration_id != identifier:
                    raise AssertionError(
                        f"{identifier}/{endpoint.gauge_id}: configuration changed"
                    )
                source_endpoint = source_starts[endpoint.gauge_id]
                if (
                    endpoint.convergence_criterion_satisfied
                    != source_endpoint.convergence_criterion_satisfied
                ):
                    raise AssertionError(
                        f"{identifier}/{endpoint.gauge_id}: convergence changed"
                    )
                classification = self.spread_verifier.execute(endpoint, source_endpoint)
                observed_counts[classification] = (
                    observed_counts.get(classification, 0) + 1
                )
                correlated_endpoints.append(endpoint)

            converged = tuple(
                endpoint
                for endpoint in configuration.starts
                if endpoint.convergence_criterion_satisfied
            )
            if not converged:
                raise AssertionError(f"{identifier}: no converged endpoint")
            expected_partition = self.basin_partitioner.execute(
                OptimizerReanalysisBasinPartitionRequest(
                    endpoints=converged,
                    spread_tolerance=result.method.basin_spread_absolute_tolerance,
                    center_tolerance=(
                        result.method.basin_center_set_periodic_tolerance
                    ),
                )
            )
            retained_partition = tuple(
                tuple(sorted(basin.gauge_ids))
                for basin in configuration.symmetry_aware_observed_basins
            )
            if sorted(expected_partition) != sorted(retained_partition):
                raise AssertionError(f"{identifier}: D4 basin membership changed")
            if configuration.symmetry_aware_observed_basin_count != len(
                configuration.symmetry_aware_observed_basins
            ):
                raise AssertionError(f"{identifier}:symmetry-aware basin count changed")

            best = min(
                converged,
                key=lambda endpoint: (
                    endpoint.spread_components.omega_tilde_cell_squared,
                    endpoint.gauge_id,
                ),
            )
            best_wire = self.immutable_json.serialize(best.complete_document)
            retained_best_wire = self.immutable_json.serialize(
                configuration.best_observed_converged_by_omega_tilde.complete_document
            )
            if best_wire != retained_best_wire:
                raise AssertionError(f"{identifier}: best Omega_tilde endpoint changed")

        if dict(result.diagnostic_classification_counts) != observed_counts:
            raise AssertionError("diagnostic counts disagree")
        return OptimizerReanalysisCorrelationResult(tuple(correlated_endpoints))
