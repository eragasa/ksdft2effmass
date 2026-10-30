"""Independent diagnostic reconstruction for locality calculations."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

from ..definitions import (
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityRequest,
    BandEquivalenceLocalitySyntheticModelDefinition,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ..records import (
    BandEquivalenceLocalityDiagnostics,
    BandEquivalenceLocalityVerificationDiagnostics,
)

ComplexArray = NDArray[np.complex128]
FloatArray = NDArray[np.float64]


class BandEquivalenceLocalityVerifier:
    """Independently reconstruct selected point and stored-identity diagnostics."""

    __slots__ = ("_request", "_result")

    def __init__(
        self,
        *,
        request: BandEquivalenceLocalityRequest,
        result: BandEquivalenceLocalityDiagnostics,
    ) -> None:
        if type(request) is not BandEquivalenceLocalityRequest:
            raise TypeError("request must be BandEquivalenceLocalityRequest")
        if type(result) is not BandEquivalenceLocalityDiagnostics:
            raise TypeError("result must be BandEquivalenceLocalityDiagnostics")
        self._request = request
        self._result = result

    @property
    def request(self) -> BandEquivalenceLocalityRequest:
        """Return the immutable request bound to this verification action."""
        return self._request

    def _parent_field(
        self,
        model: BandEquivalenceLocalitySyntheticModelDefinition,
        case: BandEquivalenceLocalityCase,
        coordinates: FloatArray,
        parent_scale: float,
    ) -> ComplexArray:
        shape = coordinates.shape[:-1]
        onsite = model.onsite.magnitude
        directed = model.directed_hopping.magnitude
        result = np.broadcast_to(onsite, (*shape, 4, 4)).copy()
        if case.parent_kind is ParentEnum.DIRECTED_AXIS:
            phase_average = np.mean(np.exp(2.0j * np.pi * coordinates), axis=-1)
            scaled = parent_scale * phase_average
            result += scaled[..., None, None] * directed
            result += scaled.conjugate()[..., None, None] * directed.conjugate().T
            return result
        if case.parent_kind is ParentEnum.HERMITIAN_BRAVAIS:
            bonds = np.asarray(case.positive_bonds, dtype=np.float64)
            arguments = np.einsum("...d,bd->...b", coordinates, bonds)
            structure = np.mean(np.cos(2.0 * np.pi * arguments), axis=-1)
            result += (
                parent_scale
                * structure[..., None, None]
                * (directed + directed.conjugate().T)
            )
            return result
        exponentials = np.exp(-2.0j * np.pi * coordinates)
        gamma = (1.0 + np.sum(exponentials, axis=-1)) / float(case.dimension + 1)
        sublattice = np.empty((*shape, 2, 2), dtype=np.complex128)
        sublattice[..., 0, 0] = 0.0
        sublattice[..., 0, 1] = gamma
        sublattice[..., 1, 0] = gamma.conjugate()
        sublattice[..., 1, 1] = 0.0
        result = np.zeros((*shape, 4, 4), dtype=np.complex128)
        identity = np.eye(2, dtype=np.complex128)
        result[..., :2, :2] = (
            model.bipartite_lower_onsite.magnitude * identity
            + parent_scale * model.bipartite_lower_bond_scale.magnitude * sublattice
        )
        result[..., 2:, 2:] = (
            model.bipartite_upper_onsite.magnitude * identity
            + parent_scale * model.bipartite_upper_bond_scale.magnitude * sublattice
        )
        coupling = model.bipartite_intersector_coupling.magnitude
        result[..., :2, 2:] = coupling * identity
        result[..., 2:, :2] = coupling * identity
        return result

    def _retained_frame(
        self,
        model: BandEquivalenceLocalitySyntheticModelDefinition,
        parent: ComplexArray,
    ) -> ComplexArray:
        _, eigenvectors = np.linalg.eigh(parent)
        low = eigenvectors[..., :, :2]
        projector = low @ np.swapaxes(low.conjugate(), -1, -2)
        projected_seed = projector @ model.retained_seed.magnitude
        seed_gram = np.swapaxes(projected_seed.conjugate(), -1, -2) @ projected_seed
        gram_values, gram_vectors = np.linalg.eigh(seed_gram)
        inverse_root = (
            gram_vectors * (1.0 / np.sqrt(gram_values))[..., None, :]
        ) @ np.swapaxes(gram_vectors.conjugate(), -1, -2)
        return projected_seed @ inverse_root

    def _retained_field(
        self,
        frame: ComplexArray,
        parent: ComplexArray,
    ) -> ComplexArray:
        return np.swapaxes(frame.conjugate(), -1, -2) @ parent @ frame

    def _independent_parent(
        self,
        model: BandEquivalenceLocalitySyntheticModelDefinition,
        case: BandEquivalenceLocalityCase,
        coordinate: tuple[float, ...],
        parent_scale: float,
    ) -> ComplexArray:
        onsite = model.onsite.magnitude
        directed = model.directed_hopping.magnitude
        if case.parent_kind is ParentEnum.DIRECTED_AXIS:
            phase = sum(
                complex(math.cos(math.tau * value), math.sin(math.tau * value))
                for value in coordinate
            ) / float(case.dimension)
            return onsite + parent_scale * (
                phase * directed + phase.conjugate() * directed.conjugate().T
            )
        if case.parent_kind is ParentEnum.HERMITIAN_BRAVAIS:
            structure = math.fsum(
                math.cos(
                    math.tau
                    * math.fsum(
                        value * component
                        for value, component in zip(coordinate, bond, strict=True)
                    )
                )
                for bond in case.positive_bonds
            ) / float(len(case.positive_bonds))
            return onsite + parent_scale * structure * (
                directed + directed.conjugate().T
            )
        gamma = (
            1.0
            + sum(
                complex(math.cos(-math.tau * value), math.sin(-math.tau * value))
                for value in coordinate
            )
        ) / float(case.dimension + 1)
        sublattice = np.array(
            [[0.0, gamma], [gamma.conjugate(), 0.0]], dtype=np.complex128
        )
        result = np.zeros((4, 4), dtype=np.complex128)
        identity = np.eye(2)
        result[:2, :2] = (
            model.bipartite_lower_onsite.magnitude * identity
            + parent_scale * model.bipartite_lower_bond_scale.magnitude * sublattice
        )
        result[2:, 2:] = (
            model.bipartite_upper_onsite.magnitude * identity
            + parent_scale * model.bipartite_upper_bond_scale.magnitude * sublattice
        )
        coupling = model.bipartite_intersector_coupling.magnitude
        result[:2, 2:] = coupling * identity
        result[2:, :2] = coupling * identity
        return result

    def _independent_angle(
        self,
        case: BandEquivalenceLocalityCase,
        coordinate: tuple[float, ...],
        amplitude: float,
    ) -> float:
        total = math.fsum(
            math.sin(
                math.tau
                * math.fsum(
                    value * component
                    for value, component in zip(coordinate, bond, strict=True)
                )
            )
            for bond in case.positive_bonds
        )
        if case.gauge_normalization is GaugeNormalizationEnum.AXIS_MAXIMUM:
            return amplitude * total / float(case.dimension)
        return amplitude * math.sqrt(2.0 / len(case.positive_bonds)) * total

    @property
    def retained_result(self) -> BandEquivalenceLocalityDiagnostics:
        """Return the immutable retained result bound to this verification action."""
        return self._result

    def execute(self) -> BandEquivalenceLocalityVerificationDiagnostics:
        """Independently verify the constructor-bound retained result."""
        result = self._result
        definition = self._request
        if result.family is not definition.family:
            raise ValueError("result family does not match request")
        if (
            result.construction_size != definition.construction_size
            or result.evaluation_size != definition.evaluation_size
        ):
            raise ValueError("result mesh sizes do not match definition")
        stored_defects: list[float] = []
        for case in result.cases:
            stored_defects.append(case.metric_covariance_defect)
            for point in case.points:
                stored_defects.extend(
                    (
                        max(0.0, -point.continuous_external_gap_lower_bound),
                        point.maximum_parent_hermiticity_defect,
                        point.maximum_eigensystem_reconstruction_defect,
                        point.maximum_frame_orthonormality_defect,
                        point.maximum_projector_reconstruction_defect,
                        point.maximum_parent_retained_reconstruction_defect,
                        point.maximum_parent_fourier_reconstruction_defect,
                        point.maximum_periodic_frame_closure_defect,
                        point.maximum_transport_unitarity_defect,
                        point.maximum_direct_band_defect,
                        point.maximum_covariant_defect,
                        point.flat_residual_tail_identity_defect or 0.0,
                        (
                            0.0
                            if point.normalized_squared_operator_residual is None
                            else abs(
                                point.normalized_squared_operator_residual
                                - point.minimum_operator_threshold**2
                                / point.splitting_scale
                            )
                        ),
                        (
                            0.0
                            if point.flat_identity_departure is None
                            else abs(
                                point.flat_identity_departure
                                - (
                                    point.normalized_excess_nonzero_hopping_weight
                                    or 0.0
                                )
                                + (point.normalized_squared_operator_residual or 0.0)
                            )
                        ),
                        abs(
                            point.restricted_global_rotation_residual
                            - point.minimum_operator_threshold
                        ),
                        point.reference_fourier_reconstruction_defect,
                        point.comparison_fourier_reconstruction_defect,
                        point.reference_parseval_defect,
                        point.comparison_parseval_defect,
                        point.reference_twisted_nyquist_defect,
                        point.comparison_twisted_nyquist_defect,
                        point.reference_ordinary_hermiticity_defect,
                        point.comparison_ordinary_hermiticity_defect,
                    )
                )
                if point.transport_closure_and_plaquette_applicable:
                    closure_defect = point.maximum_closure_holonomy_unitarity_defect
                    if closure_defect is None:
                        raise ValueError(
                            "applicable transport is missing closure unitarity"
                        )
                    stored_defects.append(closure_defect)
                for shell in point.shell_diagnostics:
                    stored_defects.append(
                        max(
                            0.0,
                            shell.reference_total.maximum_band
                            - math.sqrt(2.0)
                            * shell.reference_total.maximum_hamiltonian,
                            shell.comparison_total.maximum_band
                            - math.sqrt(2.0)
                            * shell.comparison_total.maximum_hamiltonian,
                            shell.reference_truncation.maximum_band
                            - math.sqrt(2.0)
                            * shell.reference_truncation.maximum_hamiltonian,
                            shell.comparison_truncation.maximum_band
                            - math.sqrt(2.0)
                            * shell.comparison_truncation.maximum_hamiltonian,
                            shell.reference_truncation_parseval_defect,
                            shell.comparison_truncation_parseval_defect,
                            abs(
                                shell.reference_total_omitted_power
                                - shell.reference_omitted_power
                                - point.reference_nyquist_power
                            ),
                            abs(
                                shell.comparison_total_omitted_power
                                - shell.comparison_omitted_power
                                - point.comparison_nyquist_power
                            ),
                        )
                    )
                shell_positions = {
                    shell.shell_index: index
                    for index, shell in enumerate(point.shell_diagnostics)
                }
                for decision in point.first_passing:
                    channels = (
                        (
                            "reference_band",
                            decision.reference_band_shell,
                            decision.reference_band_passing_error,
                            decision.reference_band_preceding_error,
                        ),
                        (
                            "comparison_band",
                            decision.comparison_band_shell,
                            decision.comparison_band_passing_error,
                            decision.comparison_band_preceding_error,
                        ),
                        (
                            "reference_hamiltonian",
                            decision.reference_hamiltonian_shell,
                            decision.reference_hamiltonian_passing_error,
                            decision.reference_hamiltonian_preceding_error,
                        ),
                        (
                            "comparison_hamiltonian",
                            decision.comparison_hamiltonian_shell,
                            decision.comparison_hamiltonian_passing_error,
                            decision.comparison_hamiltonian_preceding_error,
                        ),
                    )
                    for name, shell_index, passing, preceding in channels:
                        if shell_index is None:
                            stored_defects.append(
                                0.0 if passing is None and preceding is None else 1.0
                            )
                            continue
                        position = shell_positions[shell_index]
                        shell = point.shell_diagnostics[position]
                        errors = (
                            shell.reference_total
                            if name.startswith("reference")
                            else shell.comparison_total
                        )
                        expected_passing = (
                            errors.maximum_band
                            if name.endswith("band")
                            else errors.maximum_hamiltonian
                        )
                        assert passing is not None
                        stored_defects.extend(
                            (
                                abs(passing - expected_passing),
                                max(0.0, passing - decision.tolerance),
                            )
                        )
                        if position == 0:
                            stored_defects.append(0.0 if preceding is None else 1.0)
                        else:
                            previous = point.shell_diagnostics[position - 1]
                            previous_errors = (
                                previous.reference_total
                                if name.startswith("reference")
                                else previous.comparison_total
                            )
                            expected_preceding = (
                                previous_errors.maximum_band
                                if name.endswith("band")
                                else previous_errors.maximum_hamiltonian
                            )
                            assert preceding is not None
                            stored_defects.extend(
                                (
                                    abs(preceding - expected_preceding),
                                    max(0.0, decision.tolerance - preceding),
                                )
                            )
        independent_parent = 0.0
        independent_band = 0.0
        probes = tuple(
            0.137 * (index + 1) - 0.25 for index in range(definition.dimension)
        )
        coordinate = np.asarray(probes, dtype=np.float64).reshape(
            *((1,) * definition.dimension), definition.dimension
        )
        for case_definition, case_result in zip(
            definition.cases, result.cases, strict=True
        ):
            if case_definition.name != case_result.name:
                raise ValueError("case order or identity does not match definition")
            expected_point_identities = tuple(
                (parent_scale, amplitude)
                for parent_scale in definition.parent_scales
                for amplitude in definition.amplitudes
            )
            stored_point_identities = tuple(
                (point.parent_scale, point.amplitude) for point in case_result.points
            )
            if stored_point_identities != expected_point_identities:
                raise ValueError("point identities do not match the analysis request")
            for parent_scale in definition.parent_scales:
                parent = self._independent_parent(
                    definition.synthetic_model,
                    case_definition,
                    probes,
                    parent_scale,
                )
                vectorized = self._parent_field(
                    definition.synthetic_model,
                    case_definition,
                    coordinate,
                    parent_scale,
                ).reshape(4, 4)
                independent_parent = max(
                    independent_parent,
                    float(np.linalg.norm(parent - vectorized)),
                )
                parent_probe = vectorized.reshape(1, 4, 4)
                frame = self._retained_frame(
                    definition.synthetic_model,
                    parent_probe,
                )
                retained = self._retained_field(frame, parent_probe)[0]
                for amplitude in definition.amplitudes:
                    theta = self._independent_angle(case_definition, probes, amplitude)
                    cosine = math.cos(theta)
                    sine = math.sin(theta)
                    rotation = np.array(
                        [[cosine, -sine], [sine, cosine]], dtype=np.complex128
                    )
                    comparison = rotation.T @ retained @ rotation
                    independent_band = max(
                        independent_band,
                        float(
                            np.max(
                                np.abs(
                                    np.linalg.eigvalsh(retained)
                                    - np.linalg.eigvalsh(comparison)
                                )
                            )
                        ),
                    )
        maximum_stored = max(stored_defects, default=0.0)

        passes = all(
            math.isfinite(value)
            for value in (maximum_stored, independent_parent, independent_band)
        )
        return BandEquivalenceLocalityVerificationDiagnostics(
            family=result.family,
            passes=passes,
            maximum_stored_identity_defect=maximum_stored,
            maximum_independent_parent_defect=independent_parent,
            maximum_independent_band_defect=independent_band,
        )


__all__ = ["BandEquivalenceLocalityVerifier"]
