"""Request-bound analysis of synthetic band-equivalence locality."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.finite_periodic.numpy.matrix_evaluation import (
    NumpyFiniteFourierMatrixEvaluationResult,
)
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.numerics.finite_periodic.numpy.tensor_product_evaluation import (
    NumpyTensorProductFourierMatrixEvaluationDefinition,
    NumpyTensorProductFourierMatrixSeriesEvaluator,
)
from projectkoios.numerics.finite_periodic.numpy.transform_diagnostics import (
    NumpyCenteredUniformMeshHermiticityAnalyzer,
    NumpyFinitePeriodicParsevalAnalyzer,
)
from projectkoios.numerics.finite_periodic.numpy.transforms import (
    NumpyCenteredUniformMeshMatrixFourierTransformDefinition,
    NumpyCenteredUniformMeshMatrixFourierTransformer,
    NumpyCenteredUniformMeshMatrixFourierTransformResult,
)
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer
from scipy.special import j0, jv  # type: ignore[import-untyped]

from .alignment import (
    FrameTransportDiagnostic,
    frame_transport_diagnostics,
    restricted_alignment,
)
from .constrained_bessel import (
    ConstrainedBesselGeometryEnum,
    ConstrainedBesselZeroModeDiagnostic,
    ConstrainedBesselZeroModeRequest,
)
from .definitions import (
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityFamilyEnum,
    BandEquivalenceLocalityRequest,
    BandEquivalenceLocalitySyntheticModelDefinition,
    GaugeNormalizationEnum,
    ParentEnum,
)
from .fourier import (
    error_channels,
    iter_complete_shell_fields,
    maximum_matrix_defect,
)
from .geometry import (
    basis_distance_range,
    metric_covariance_defect,
    minimum_mesh_separation,
)
from .geometry import (
    metric_indices as physical_metric_indices,
)
from .results import (
    BandEquivalenceLocalityAmplitudeMidpointAnalysis,
    BandEquivalenceLocalityCaseAnalysis,
    BandEquivalenceLocalityErrorChannels,
    BandEquivalenceLocalityFirstPassingDecision,
    BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis,
    BandEquivalenceLocalityPointAnalysis,
    BandEquivalenceLocalityShellAnalysis,
)
from .shell_power import BandEquivalenceLocalityFourierShellPowerAnalyzer

ComplexArray = NDArray[np.complex128]
FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


@dataclass(frozen=True, slots=True, eq=False)
class BandEquivalenceLocalityAnalysis:
    """Represent the complete correlated analysis of one locality request."""

    request: BandEquivalenceLocalityRequest
    status: str
    cases: tuple[BandEquivalenceLocalityCaseAnalysis, ...]

    def __post_init__(self) -> None:
        if type(self.request) is not BandEquivalenceLocalityRequest:
            raise TypeError("request must be BandEquivalenceLocalityRequest")
        if type(self.status) is not str or not self.status:
            raise TypeError("status must be a nonempty built-in string")
        if (
            type(self.cases) is not tuple
            or not self.cases
            or any(
                type(case) is not BandEquivalenceLocalityCaseAnalysis
                for case in self.cases
            )
        ):
            raise TypeError(
                "cases must contain BandEquivalenceLocalityCaseAnalysis values"
            )
        if tuple(case.name for case in self.cases) != tuple(
            case.name for case in self.request.cases
        ):
            raise ValueError("analysis cases must match the request")

    @property
    def family(self) -> BandEquivalenceLocalityFamilyEnum:
        """Return the analyzed lattice-family identity."""
        return self.request.family

    @property
    def construction_size(self) -> int:
        """Return the analyzed construction-mesh size per axis."""
        return self.request.construction_size

    @property
    def evaluation_size(self) -> int:
        """Return the analyzed evaluation-mesh size per axis."""
        return self.request.evaluation_size


class BandEquivalenceLocalityAnalyzer:
    """Perform the complete locality analysis of one bound request."""

    __slots__ = ("_request",)

    def __init__(self, *, request: BandEquivalenceLocalityRequest) -> None:
        if type(request) is not BandEquivalenceLocalityRequest:
            raise TypeError("request must be BandEquivalenceLocalityRequest")
        self._request = request

    @property
    def request(self) -> BandEquivalenceLocalityRequest:
        """Return the exact immutable request bound to this analyzer."""
        return self._request

    def transform(
        self,
        definition: NumpyCenteredUniformMeshMatrixFourierTransformDefinition,
    ) -> NumpyCenteredUniformMeshMatrixFourierTransformResult:
        """Execute one constructor-bound canonical matrix Fourier transform."""
        return NumpyCenteredUniformMeshMatrixFourierTransformer(
            definition=definition
        ).result()

    def evaluate(
        self,
        definition: NumpyTensorProductFourierMatrixEvaluationDefinition,
    ) -> NumpyFiniteFourierMatrixEvaluationResult:
        """Execute one constructor-bound canonical tensor-grid evaluation."""
        return NumpyTensorProductFourierMatrixSeriesEvaluator(
            definition=definition
        ).result()

    def matrix_defect(self, left: ComplexArray, right: ComplexArray) -> float:
        """Return the maximum pointwise matrix Frobenius defect."""
        return maximum_matrix_defect(left, right)

    def error_channels(
        self,
        approximation: ComplexArray,
        direct: ComplexArray,
    ) -> BandEquivalenceLocalityErrorChannels:
        """Return rank-normalized matrix and ordered-band error channels."""
        return error_channels(approximation, direct)

    def complete_shell_fields(
        self,
        source_mesh: CenteredUniformMesh,
        series: NumpyFiniteFourierMatrixSeries,
        coordinate_axes: tuple[FloatArray, ...],
        metric_indices: IntArray,
        shells: tuple[int, ...],
    ) -> tuple[ComplexArray, ...]:
        """Return cumulative KSD-selected complete physical-metric supports."""
        return tuple(
            iter_complete_shell_fields(
                source_mesh,
                series,
                coordinate_axes,
                metric_indices,
                shells,
            )
        )

    def coordinate_axis(self, size: int, mesh_offset: float) -> FloatArray:
        """Return one uniform reduced-coordinate axis with its declared offset."""
        return np.asarray(
            -0.5 + (np.arange(size, dtype=np.float64) + mesh_offset) / float(size),
            dtype=np.float64,
        )

    def coordinates(self, size: int, dimension: int, mesh_offset: float) -> FloatArray:
        """Return a tensor grid in reduced reciprocal coordinates.

        ``mesh_offset=0.5`` is the conventional Monkhorst--Pack origin for an even
        construction size. Other offsets define withheld uniform meshes and are not
        silently identified with the construction mesh.
        """
        axis = self.coordinate_axis(size, mesh_offset)
        return np.stack(np.meshgrid(*(axis,) * dimension, indexing="ij"), axis=-1)

    def rotation_field(self, angles: FloatArray) -> ComplexArray:
        rotations = np.empty((*angles.shape, 2, 2), dtype=np.complex128)
        cosine = np.cos(angles)
        sine = np.sin(angles)
        rotations[..., 0, 0] = cosine
        rotations[..., 0, 1] = -sine
        rotations[..., 1, 0] = sine
        rotations[..., 1, 1] = cosine
        return rotations

    def parent_field(
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
            hermitian_bond = directed + directed.conjugate().T
            result += parent_scale * structure[..., None, None] * hermitian_bond
            return result

        exponentials = np.exp(-2.0j * np.pi * coordinates)
        gamma = (1.0 + np.sum(exponentials, axis=-1)) / float(case.dimension + 1)
        sublattice = np.empty((*shape, 2, 2), dtype=np.complex128)
        sublattice[..., 0, 0] = 0.0
        sublattice[..., 0, 1] = gamma
        sublattice[..., 1, 0] = gamma.conjugate()
        sublattice[..., 1, 1] = 0.0
        parent_dimension = int(model.onsite.magnitude.shape[0])
        retained_rank = model.retained_rank
        result = np.zeros(
            (*shape, parent_dimension, parent_dimension),
            dtype=np.complex128,
        )
        identity = np.eye(retained_rank, dtype=np.complex128)
        result[..., :retained_rank, :retained_rank] = (
            model.bipartite_lower_onsite.magnitude * identity
            + parent_scale * model.bipartite_lower_bond_scale.magnitude * sublattice
        )
        result[..., retained_rank:, retained_rank:] = (
            model.bipartite_upper_onsite.magnitude * identity
            + parent_scale * model.bipartite_upper_bond_scale.magnitude * sublattice
        )
        coupling = model.bipartite_intersector_coupling.magnitude
        result[..., :retained_rank, retained_rank:] = coupling * identity
        result[..., retained_rank:, :retained_rank] = coupling * identity
        return result

    def _continuous_gap_lower_bound(
        self,
        model: BandEquivalenceLocalitySyntheticModelDefinition,
        case: BandEquivalenceLocalityCase,
        parent_scale: float,
    ) -> float:
        if case.parent_kind is ParentEnum.BIPARTITE_INSPIRED:
            onsite_separation = (
                model.bipartite_upper_onsite.magnitude
                - model.bipartite_lower_onsite.magnitude
            )
            bond_width = (
                model.bipartite_lower_bond_scale.magnitude
                + model.bipartite_upper_bond_scale.magnitude
            )
            coupling_width = 2.0 * model.bipartite_intersector_coupling.magnitude
            return onsite_separation - parent_scale * bond_width - coupling_width
        onsite = model.onsite.magnitude
        directed = model.directed_hopping.magnitude
        hermitian_bond = directed + directed.conjugate().T
        onsite_gap = float(
            np.linalg.eigvalsh(onsite)[2] - np.linalg.eigvalsh(onsite)[1]
        )
        if case.parent_kind is ParentEnum.DIRECTED_AXIS:
            return onsite_gap - 4.0 * parent_scale * float(np.linalg.norm(directed, 2))
        return onsite_gap - 2.0 * parent_scale * float(
            np.linalg.norm(hermitian_bond, 2)
        )

    def retained_frame(
        self,
        model: BandEquivalenceLocalitySyntheticModelDefinition,
        parent: ComplexArray,
    ) -> tuple[ComplexArray, FloatArray, FloatArray]:
        eigenvalues, eigenvectors = np.linalg.eigh(parent)
        low = eigenvectors[..., :, :2]
        projector = low @ np.swapaxes(low.conjugate(), -1, -2)
        projected_seed = projector @ model.retained_seed.magnitude
        seed_gram = np.swapaxes(projected_seed.conjugate(), -1, -2) @ projected_seed
        gram_values, gram_vectors = np.linalg.eigh(seed_gram)
        inverse_root = (
            gram_vectors * (1.0 / np.sqrt(gram_values))[..., None, :]
        ) @ np.swapaxes(gram_vectors.conjugate(), -1, -2)
        frame = projected_seed @ inverse_root
        return frame, eigenvalues, gram_values

    def retained_field(self, frame: ComplexArray, parent: ComplexArray) -> ComplexArray:
        return np.swapaxes(frame.conjugate(), -1, -2) @ parent @ frame

    def gauge_angles(
        self,
        case: BandEquivalenceLocalityCase,
        coordinates: FloatArray,
        amplitude: float,
    ) -> FloatArray:
        bonds = np.asarray(case.positive_bonds, dtype=np.float64)
        arguments = np.einsum("...d,bd->...b", coordinates, bonds)
        sine_sum = np.sum(np.sin(2.0 * np.pi * arguments), axis=-1)
        if case.gauge_normalization is GaugeNormalizationEnum.AXIS_MAXIMUM:
            return amplitude * sine_sum / float(case.dimension)
        return amplitude * math.sqrt(2.0 / float(len(case.positive_bonds))) * sine_sum

    def _analytic_flat_correlation(
        self, case: BandEquivalenceLocalityCase, amplitude: float
    ) -> tuple[float, float]:
        bond_count = len(case.positive_bonds)
        if case.gauge_normalization is GaugeNormalizationEnum.AXIS_MAXIMUM:
            argument = 2.0 * amplitude / float(case.dimension)
        else:
            argument = 2.0 * amplitude * math.sqrt(2.0 / float(bond_count))
        bonds = np.asarray(case.positive_bonds, dtype=np.float64)
        if (
            bond_count == case.dimension
            and np.linalg.matrix_rank(bonds) == case.dimension
        ):
            return float(j0(argument)) ** bond_count, 0.0
        if case.dimension == 2 and bond_count == 3:
            diagnostic = ConstrainedBesselZeroModeDiagnostic(
                request=ConstrainedBesselZeroModeRequest(
                    ConstrainedBesselGeometryEnum.TRIANGULAR,
                    argument,
                    20,
                )
            ).result()
            return diagnostic.value, diagnostic.remainder_bound
        if case.dimension == 3 and bond_count == 6:
            diagnostic = ConstrainedBesselZeroModeDiagnostic(
                request=ConstrainedBesselZeroModeRequest(
                    ConstrainedBesselGeometryEnum.FCC,
                    argument,
                    9,
                )
            ).result()
            return diagnostic.value, diagnostic.remainder_bound
        raise ValueError("no analytic flat correlation owns this bond inventory")

    def _analytic_flat_correlation_values(
        self, case: BandEquivalenceLocalityCase, amplitudes: FloatArray
    ) -> FloatArray:
        """Evaluate one flat correlation law vectorially for resolution diagnostics."""
        bond_count = len(case.positive_bonds)
        scale = (
            2.0 / float(case.dimension)
            if case.gauge_normalization is GaugeNormalizationEnum.AXIS_MAXIMUM
            else 2.0 * math.sqrt(2.0 / float(bond_count))
        )
        arguments = scale * amplitudes
        bonds = np.asarray(case.positive_bonds, dtype=np.float64)
        if (
            bond_count == case.dimension
            and np.linalg.matrix_rank(bonds) == case.dimension
        ):
            return np.asarray(j0(arguments) ** bond_count, dtype=np.float64)
        if case.dimension == 2 and bond_count == 3:
            indices = np.arange(-20, 21, dtype=np.int64)
            positive = jv(indices[None, :], arguments[:, None])
            negative = jv(-indices[None, :], arguments[:, None])
            return np.asarray(
                np.sum(negative * positive * positive, axis=1), dtype=np.float64
            )
        if case.dimension == 3 and bond_count == 6:
            free = np.arange(-9, 10, dtype=np.int64)
            one, two, three = np.meshgrid(free, free, free, indexing="ij")
            orders = np.arange(-18, 19, dtype=np.int64)
            offset = 18
            flattened_indices = tuple(
                value.ravel() + offset
                for value in (
                    one + two,
                    -one + three,
                    -two - three,
                    one,
                    two,
                    three,
                )
            )
            values = np.empty(arguments.size, dtype=np.float64)
            batch_size = 64
            for start in range(0, arguments.size, batch_size):
                stop = min(start + batch_size, arguments.size)
                bessel = jv(orders[None, :], arguments[start:stop, None])
                product = np.ones((stop - start, one.size), dtype=np.float64)
                for indices in flattened_indices:
                    product *= bessel[:, indices]
                values[start:stop] = np.sum(product, axis=1)
            return values
        raise ValueError("no analytic flat correlation owns this bond inventory")

    def _flat_amplitude_resolution(
        self,
        definition: BandEquivalenceLocalityRequest,
        case: BandEquivalenceLocalityCase,
    ) -> tuple[BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis, ...]:
        maximum_amplitude = definition.amplitudes[-1]
        finest_intervals = definition.amplitude_resolution_intervals[-1]
        fine_positions = np.arange(2 * finest_intervals + 1, dtype=np.float64)
        fine_amplitudes = (
            maximum_amplitude * fine_positions / float(2 * finest_intervals)
        )
        correlations = np.clip(
            self._analytic_flat_correlation_values(case, fine_amplitudes), -1.0, 1.0
        )
        operator = np.sqrt(np.maximum(0.0, 1.0 - correlations**2))
        joint = np.sqrt(np.maximum(0.0, 2.0 * (1.0 - correlations)))
        results: list[BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis] = []
        for intervals in definition.amplitude_resolution_intervals:
            stride = finest_intervals // intervals
            node_indices = np.arange(0, 2 * finest_intervals + 1, 2 * stride)
            midpoint_indices = node_indices[:-1] + stride
            operator_interpolated = 0.5 * (
                operator[node_indices[:-1]] + operator[node_indices[1:]]
            )
            joint_interpolated = 0.5 * (
                joint[node_indices[:-1]] + joint[node_indices[1:]]
            )
            results.append(
                BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis(
                    amplitude_intervals=intervals,
                    amplitude_nodes=intervals + 1,
                    maximum_operator_threshold_midpoint_interpolation_defect=float(
                        np.max(
                            np.abs(operator_interpolated - operator[midpoint_indices])
                        )
                    ),
                    maximum_joint_threshold_midpoint_interpolation_defect=float(
                        np.max(np.abs(joint_interpolated - joint[midpoint_indices]))
                    ),
                    passes_unit_scale_draft_tolerance=None,
                    tolerance_inapplicable_reason=(
                        "Paper 2 did not prospectively freeze a family-owned amplitude "
                        "resolution tolerance; Paper 1's tolerance is not transferred"
                    ),
                )
            )
        return tuple(results)

    def _amplitude_midpoint_diagnostic(
        self,
        definition: BandEquivalenceLocalityRequest,
        points: tuple[BandEquivalenceLocalityPointAnalysis, ...],
    ) -> BandEquivalenceLocalityAmplitudeMidpointAnalysis:
        amplitudes = definition.amplitudes
        if len(amplitudes) != 3 or not math.isclose(
            amplitudes[1],
            0.5 * (amplitudes[0] + amplitudes[2]),
            rel_tol=0.0,
            abs_tol=1.0e-15,
        ):
            return BandEquivalenceLocalityAmplitudeMidpointAnalysis(
                amplitude_nodes=len(amplitudes),
                applicable=False,
                inapplicable_reason=(
                    "the declared amplitudes do not form one "
                    "endpoint-midpoint-endpoint triple"
                ),
                endpoint_minimum_threshold_over_sqrt_splitting=None,
                maximum_correlation_midpoint_defect=None,
                maximum_operator_threshold_midpoint_defect=None,
                maximum_joint_threshold_midpoint_defect=None,
                maximum_nonzero_hopping_weight_midpoint_defect=None,
                maximum_hopping_block_power_midpoint_defect=None,
            )

        endpoint_thresholds: list[float] = []
        correlations: list[float] = []
        operator_thresholds: list[float] = []
        joint_thresholds: list[float] = []
        hopping_weights: list[float] = []
        hopping_block_powers: list[float] = []
        for parent_scale in definition.parent_scales:
            triple = tuple(
                point for point in points if point.parent_scale == parent_scale
            )
            if len(triple) != 3:
                raise RuntimeError(
                    "amplitude point inventory does not match definition"
                )
            left, midpoint, right = triple
            if right.minimum_operator_threshold_over_sqrt_splitting is not None:
                endpoint_thresholds.append(
                    right.minimum_operator_threshold_over_sqrt_splitting
                )
            if (
                left.finite_mesh_maximum_correlation is not None
                and midpoint.finite_mesh_maximum_correlation is not None
                and right.finite_mesh_maximum_correlation is not None
            ):
                correlations.append(
                    abs(
                        midpoint.finite_mesh_maximum_correlation
                        - 0.5
                        * (
                            left.finite_mesh_maximum_correlation
                            + right.finite_mesh_maximum_correlation
                        )
                    )
                )
            operator_thresholds.append(
                abs(
                    midpoint.minimum_operator_threshold
                    - 0.5
                    * (
                        left.minimum_operator_threshold
                        + right.minimum_operator_threshold
                    )
                )
            )
            joint_thresholds.append(
                abs(
                    midpoint.exact_spectrum_joint_operator_threshold
                    - 0.5
                    * (
                        left.exact_spectrum_joint_operator_threshold
                        + right.exact_spectrum_joint_operator_threshold
                    )
                )
            )
            hopping_weights.append(
                abs(
                    midpoint.comparison_nononsite_power
                    - 0.5
                    * (
                        left.comparison_nononsite_power
                        + right.comparison_nononsite_power
                    )
                )
            )
            for left_shell, midpoint_shell, right_shell in zip(
                left.shell_diagnostics,
                midpoint.shell_diagnostics,
                right.shell_diagnostics,
                strict=True,
            ):
                if not (
                    left_shell.shell_index
                    == midpoint_shell.shell_index
                    == right_shell.shell_index
                ):
                    raise RuntimeError("amplitude shell inventories differ")
                hopping_block_powers.append(
                    abs(
                        midpoint_shell.comparison_shell_power
                        - 0.5
                        * (
                            left_shell.comparison_shell_power
                            + right_shell.comparison_shell_power
                        )
                    )
                )
        return BandEquivalenceLocalityAmplitudeMidpointAnalysis(
            amplitude_nodes=len(amplitudes),
            applicable=True,
            inapplicable_reason=None,
            endpoint_minimum_threshold_over_sqrt_splitting=(
                min(endpoint_thresholds) if endpoint_thresholds else None
            ),
            maximum_correlation_midpoint_defect=(
                max(correlations) if correlations else None
            ),
            maximum_operator_threshold_midpoint_defect=max(operator_thresholds),
            maximum_joint_threshold_midpoint_defect=max(joint_thresholds),
            maximum_nonzero_hopping_weight_midpoint_defect=max(hopping_weights),
            maximum_hopping_block_power_midpoint_defect=max(hopping_block_powers),
        )

    def _first_passing(
        self, shells: tuple[BandEquivalenceLocalityShellAnalysis, ...], tolerance: float
    ) -> BandEquivalenceLocalityFirstPassingDecision:
        def select(
            channel: str, quantity: str
        ) -> tuple[int | None, float | None, float | None]:
            previous: float | None = None
            for shell in shells:
                errors = (
                    shell.reference_total
                    if channel == "reference"
                    else shell.comparison_total
                )
                value = (
                    errors.maximum_band
                    if quantity == "band"
                    else errors.maximum_hamiltonian
                )
                if value <= tolerance:
                    return shell.shell_index, value, previous
                previous = value
            return None, None, None

        reference_band = select("reference", "band")
        comparison_band = select("comparison", "band")
        reference_hamiltonian = select("reference", "hamiltonian")
        comparison_hamiltonian = select("comparison", "hamiltonian")
        return BandEquivalenceLocalityFirstPassingDecision(
            tolerance=tolerance,
            reference_band_shell=reference_band[0],
            comparison_band_shell=comparison_band[0],
            reference_hamiltonian_shell=reference_hamiltonian[0],
            comparison_hamiltonian_shell=comparison_hamiltonian[0],
            reference_band_passing_error=reference_band[1],
            reference_band_preceding_error=reference_band[2],
            comparison_band_passing_error=comparison_band[1],
            comparison_band_preceding_error=comparison_band[2],
            reference_hamiltonian_passing_error=reference_hamiltonian[1],
            reference_hamiltonian_preceding_error=reference_hamiltonian[2],
            comparison_hamiltonian_passing_error=comparison_hamiltonian[1],
            comparison_hamiltonian_preceding_error=comparison_hamiltonian[2],
        )

    def execute(self) -> BandEquivalenceLocalityAnalysis:
        """Analyze the exact immutable request bound at construction."""
        definition = self._request
        construction = self.coordinates(
            definition.construction_size, definition.dimension, 0.5
        )
        evaluation = self.coordinates(
            definition.evaluation_size,
            definition.dimension,
            0.5 + definition.evaluation_shift,
        )
        separation = minimum_mesh_separation(construction, evaluation)
        case_results = tuple(
            self._case(definition, case, construction, evaluation, separation)
            for case in definition.cases
        )
        return BandEquivalenceLocalityAnalysis(
            request=definition,
            status="development-smoke-not-retained-evidence",
            cases=case_results,
        )

    def _case(
        self,
        definition: BandEquivalenceLocalityRequest,
        case: BandEquivalenceLocalityCase,
        construction: FloatArray,
        evaluation: FloatArray,
        separation: float,
    ) -> BandEquivalenceLocalityCaseAnalysis:
        points: list[BandEquivalenceLocalityPointAnalysis] = []
        source_mesh = CenteredUniformMesh(
            case.dimension,
            definition.construction_size,
            (0.5,) * case.dimension,
        )
        construction_axis = self.coordinate_axis(definition.construction_size, 0.5)
        construction_axes = (construction_axis,) * case.dimension
        evaluation_axis = self.coordinate_axis(
            definition.evaluation_size,
            0.5 + definition.evaluation_shift,
        )
        evaluation_axes = (evaluation_axis,) * case.dimension
        for parent_scale in definition.parent_scales:
            parent = self.parent_field(
                definition.synthetic_model,
                case,
                construction,
                parent_scale,
            )
            frame, eigenvalues, seed_gram_values = self.retained_frame(
                definition.synthetic_model,
                parent,
            )
            transport = frame_transport_diagnostics(
                frame,
                case.dimension,
                definition.transport_rank_absolute,
                definition.transport_rank_relative,
            )
            projector = frame @ np.swapaxes(frame.conjugate(), -1, -2)
            retained = self.retained_field(frame, parent)
            eigensystem = np.linalg.eigh(parent)
            reconstructed_parent = (
                eigensystem.eigenvectors * eigensystem.eigenvalues[..., None, :]
            ) @ np.swapaxes(eigensystem.eigenvectors.conjugate(), -1, -2)
            identity = np.eye(
                definition.synthetic_model.retained_rank,
                dtype=np.complex128,
            )
            parent_reconstruction = projector @ parent @ projector
            lifted = frame @ retained @ np.swapaxes(frame.conjugate(), -1, -2)
            parent_transform = self.transform(
                NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                    source_mesh,
                    parent,
                )
            )
            parent_fourier_values = self.evaluate(
                NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                    source_mesh,
                    parent_transform.series,
                    construction_axes,
                )
            ).matrix_values
            parent_fourier_reconstruction = self.matrix_defect(
                parent_fourier_values,
                parent,
            )
            periodic_frame_closure = 0.0
            for axis in range(case.dimension):
                shifted = construction.copy()
                shifted[..., axis] += 1.0
                shifted_frame, _, _ = self.retained_frame(
                    definition.synthetic_model,
                    self.parent_field(
                        definition.synthetic_model,
                        case,
                        shifted,
                        parent_scale,
                    ),
                )
                periodic_frame_closure = max(
                    periodic_frame_closure,
                    self.matrix_defect(shifted_frame, frame),
                )
            minimum_sampled_external_gap = float(
                np.min(eigenvalues[..., 2] - eigenvalues[..., 1])
            )
            continuous_external_gap_lower_bound = self._continuous_gap_lower_bound(
                definition.synthetic_model,
                case,
                parent_scale,
            )
            minimum_seed_overlap = float(np.min(seed_gram_values))
            maximum_parent_hermiticity_defect = self.matrix_defect(
                parent, np.swapaxes(parent.conjugate(), -1, -2)
            )
            maximum_eigensystem_reconstruction_defect = self.matrix_defect(
                parent, reconstructed_parent
            )
            maximum_frame_orthonormality_defect = self.matrix_defect(
                np.swapaxes(frame.conjugate(), -1, -2) @ frame,
                np.broadcast_to(identity, (*construction.shape[:-1], 2, 2)),
            )
            maximum_projector_reconstruction_defect = self.matrix_defect(
                projector,
                eigensystem.eigenvectors[..., :, :2]
                @ np.swapaxes(eigensystem.eigenvectors[..., :, :2].conjugate(), -1, -2),
            )
            maximum_parent_retained_reconstruction_defect = self.matrix_defect(
                parent_reconstruction, lifted
            )
            direct_parent_eval = self.parent_field(
                definition.synthetic_model,
                case,
                evaluation,
                parent_scale,
            )
            direct_frame_eval, _, _ = self.retained_frame(
                definition.synthetic_model,
                direct_parent_eval,
            )
            direct_reference_eval = self.retained_field(
                direct_frame_eval, direct_parent_eval
            )
            for amplitude in definition.amplitudes:
                points.append(
                    self._point(
                        definition,
                        case,
                        construction,
                        evaluation,
                        source_mesh,
                        construction_axes,
                        evaluation_axes,
                        parent_scale,
                        amplitude,
                        retained,
                        direct_reference_eval,
                        transport,
                        minimum_sampled_external_gap=minimum_sampled_external_gap,
                        continuous_external_gap_lower_bound=(
                            continuous_external_gap_lower_bound
                        ),
                        minimum_seed_overlap=minimum_seed_overlap,
                        maximum_parent_hermiticity_defect=(
                            maximum_parent_hermiticity_defect
                        ),
                        maximum_eigensystem_reconstruction_defect=(
                            maximum_eigensystem_reconstruction_defect
                        ),
                        maximum_frame_orthonormality_defect=(
                            maximum_frame_orthonormality_defect
                        ),
                        maximum_projector_reconstruction_defect=(
                            maximum_projector_reconstruction_defect
                        ),
                        maximum_parent_retained_reconstruction_defect=(
                            maximum_parent_retained_reconstruction_defect
                        ),
                        maximum_parent_fourier_reconstruction_defect=(
                            parent_fourier_reconstruction
                        ),
                        maximum_periodic_frame_closure_defect=periodic_frame_closure,
                    )
                )
        point_tuple = tuple(points)
        return BandEquivalenceLocalityCaseAnalysis(
            name=case.name,
            metric_covariance_defect=metric_covariance_defect(case),
            construction_evaluation_minimum_separation=separation,
            amplitude_midpoint=self._amplitude_midpoint_diagnostic(
                definition, point_tuple
            ),
            flat_amplitude_resolution=self._flat_amplitude_resolution(definition, case),
            points=point_tuple,
        )

    def _point(
        self,
        definition: BandEquivalenceLocalityRequest,
        case: BandEquivalenceLocalityCase,
        construction: FloatArray,
        evaluation: FloatArray,
        source_mesh: CenteredUniformMesh,
        construction_axes: tuple[FloatArray, ...],
        evaluation_axes: tuple[FloatArray, ...],
        parent_scale: float,
        amplitude: float,
        reference: ComplexArray,
        direct_reference_eval: ComplexArray,
        transport: FrameTransportDiagnostic,
        *,
        minimum_sampled_external_gap: float,
        continuous_external_gap_lower_bound: float,
        minimum_seed_overlap: float,
        maximum_parent_hermiticity_defect: float,
        maximum_eigensystem_reconstruction_defect: float,
        maximum_frame_orthonormality_defect: float,
        maximum_projector_reconstruction_defect: float,
        maximum_parent_retained_reconstruction_defect: float,
        maximum_parent_fourier_reconstruction_defect: float,
        maximum_periodic_frame_closure_defect: float,
    ) -> BandEquivalenceLocalityPointAnalysis:
        rotation = self.rotation_field(self.gauge_angles(case, construction, amplitude))
        comparison = np.swapaxes(rotation.conjugate(), -1, -2) @ reference @ rotation
        rotation_eval = self.rotation_field(
            self.gauge_angles(case, evaluation, amplitude)
        )
        direct_comparison_eval = (
            np.swapaxes(rotation_eval.conjugate(), -1, -2)
            @ direct_reference_eval
            @ rotation_eval
        )
        direct_band_defect = float(
            np.max(
                np.abs(np.linalg.eigvalsh(reference) - np.linalg.eigvalsh(comparison))
            )
        )
        covariant_defect = self.matrix_defect(
            comparison,
            np.swapaxes(rotation.conjugate(), -1, -2) @ reference @ rotation,
        )
        (
            angle,
            angle_degenerate,
            splitting_scale,
            correlation,
            minimum_threshold,
            exact_spectrum_threshold,
        ) = restricted_alignment(reference, comparison)
        reference_transform_definition = (
            NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                source_mesh,
                reference,
            )
        )
        comparison_transform_definition = (
            NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                source_mesh,
                comparison,
            )
        )
        reference_transform = self.transform(reference_transform_definition)
        comparison_transform = self.transform(comparison_transform_definition)
        reference_series = reference_transform.series
        comparison_series = comparison_transform.series
        displacements = reference_series.integer_modes
        reference_blocks = reference_series.matrix_coefficients
        comparison_displacements = comparison_series.integer_modes
        comparison_blocks = comparison_series.matrix_coefficients
        if not np.array_equal(displacements, comparison_displacements):
            raise RuntimeError("reference and comparison Fourier inventories differ")
        analytic_correlation: float | None = None
        analytic_remainder: float | None = None
        correlation_defect: float | None = None
        if parent_scale == 0.0 and correlation is not None:
            analytic_correlation, analytic_remainder = self._analytic_flat_correlation(
                case, amplitude
            )
            correlation_defect = abs(correlation - analytic_correlation)
        complete_metric_indices = physical_metric_indices(case, displacements)
        reference_power = BandEquivalenceLocalityFourierShellPowerAnalyzer(
            identifier="band-equivalence-reference-complete",
            energy_reference=definition.synthetic_model.energy_reference,
            basis_identifier=definition.synthetic_model.retained_basis_identifier,
            series=reference_series,
            shell_indices=tuple(int(value) for value in complete_metric_indices),
            retained_rank=definition.synthetic_model.retained_rank,
            power_analyzer=BlockHoppingPowerAnalyzer(),
        ).execute()
        comparison_power = BandEquivalenceLocalityFourierShellPowerAnalyzer(
            identifier="band-equivalence-comparison-complete",
            energy_reference=definition.synthetic_model.energy_reference,
            basis_identifier=definition.synthetic_model.retained_basis_identifier,
            series=comparison_series,
            shell_indices=tuple(int(value) for value in complete_metric_indices),
            retained_rank=definition.synthetic_model.retained_rank,
            power_analyzer=BlockHoppingPowerAnalyzer(),
        ).execute()
        reference_total_power = reference_power.normalized_total_power
        comparison_total_power = comparison_power.normalized_total_power
        onsite_displacements = tuple(
            power.displacement
            for power in reference_power.powers
            if power.displacement.is_zero
        )
        reference_onsite_power = reference_power.normalized_power_for(
            onsite_displacements
        )
        comparison_onsite_power = comparison_power.normalized_power_for(
            onsite_displacements
        )
        reference_nononsite_power = reference_total_power - reference_onsite_power
        comparison_nononsite_power = comparison_total_power - comparison_onsite_power
        excess_nonzero_power = comparison_nononsite_power - reference_nononsite_power
        root_splitting = math.sqrt(splitting_scale)
        if root_splitting > 1.0e-15:
            normalized_operator_threshold = minimum_threshold / root_splitting
            normalized_joint_threshold = exact_spectrum_threshold / root_splitting
            normalized_squared_residual = normalized_operator_threshold**2
            normalized_excess_power = excess_nonzero_power / splitting_scale
            flat_identity_departure = (
                normalized_excess_power - normalized_squared_residual
            )
        else:
            normalized_operator_threshold = None
            normalized_joint_threshold = None
            normalized_squared_residual = None
            normalized_excess_power = None
            flat_identity_departure = None
        flat_identity_defect = (
            abs(minimum_threshold**2 - comparison_nononsite_power)
            if parent_scale == 0.0 and correlation is not None
            else None
        )
        reconstructed_reference = self.evaluate(
            NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                source_mesh,
                reference_series,
                construction_axes,
            )
        ).matrix_values
        reconstructed_comparison = self.evaluate(
            NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                source_mesh,
                comparison_series,
                construction_axes,
            )
        ).matrix_values
        reference_parseval = (
            NumpyFinitePeriodicParsevalAnalyzer(
                definition=reference_transform_definition,
                transform_result=reference_transform,
            )
            .result()
            .absolute_defect
        )
        comparison_parseval = (
            NumpyFinitePeriodicParsevalAnalyzer(
                definition=comparison_transform_definition,
                transform_result=comparison_transform,
            )
            .result()
            .absolute_defect
        )
        reference_hermiticity_diagnostics = NumpyCenteredUniformMeshHermiticityAnalyzer(
            transform_result=reference_transform
        ).result()
        comparison_hermiticity_diagnostics = (
            NumpyCenteredUniformMeshHermiticityAnalyzer(
                transform_result=comparison_transform
            ).result()
        )
        reference_twisted = (
            reference_hermiticity_diagnostics.twisted_cyclic_maximum_frobenius_defect
        )
        reference_hermiticity = (
            reference_hermiticity_diagnostics.ordinary_maximum_frobenius_defect
        )
        comparison_twisted = (
            comparison_hermiticity_diagnostics.twisted_cyclic_maximum_frobenius_defect
        )
        comparison_hermiticity = (
            comparison_hermiticity_diagnostics.ordinary_maximum_frobenius_defect
        )
        nyquist = np.any(displacements == -definition.construction_size // 2, axis=1)
        nyquist_components = {
            tuple(int(component) for component in displacement)
            for displacement in displacements[nyquist]
        }
        nyquist_displacements = tuple(
            power.displacement
            for power in reference_power.powers
            if power.displacement.components in nyquist_components
        )
        reference_nyquist_power = reference_power.normalized_power_for(
            nyquist_displacements
        )
        comparison_nyquist_power = comparison_power.normalized_power_for(
            nyquist_displacements
        )
        ordinary = ~nyquist
        ordinary_displacements = displacements[ordinary]
        ordinary_reference = reference_blocks[ordinary]
        ordinary_comparison = comparison_blocks[ordinary]
        ordinary_reference_series = NumpyFiniteFourierMatrixSeries.from_arrays(
            case.dimension,
            ordinary_displacements,
            ordinary_reference,
        )
        ordinary_comparison_series = NumpyFiniteFourierMatrixSeries.from_arrays(
            case.dimension,
            ordinary_displacements,
            ordinary_comparison,
        )
        full_reference_eval = self.evaluate(
            NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                source_mesh,
                ordinary_reference_series,
                evaluation_axes,
            )
        ).matrix_values
        full_comparison_eval = self.evaluate(
            NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                source_mesh,
                ordinary_comparison_series,
                evaluation_axes,
            )
        ).matrix_values
        full_reference_source = self.evaluate(
            NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                source_mesh,
                ordinary_reference_series,
                construction_axes,
            )
        ).matrix_values
        full_comparison_source = self.evaluate(
            NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                source_mesh,
                ordinary_comparison_series,
                construction_axes,
            )
        ).matrix_values
        reference_interpolation = self.error_channels(
            full_reference_eval, direct_reference_eval
        )
        comparison_interpolation = self.error_channels(
            full_comparison_eval, direct_comparison_eval
        )
        metric_indices = physical_metric_indices(case, ordinary_displacements)
        ordinary_reference_power = BandEquivalenceLocalityFourierShellPowerAnalyzer(
            identifier="band-equivalence-reference-ordinary",
            energy_reference=definition.synthetic_model.energy_reference,
            basis_identifier=definition.synthetic_model.retained_basis_identifier,
            series=ordinary_reference_series,
            shell_indices=tuple(int(value) for value in metric_indices),
            retained_rank=definition.synthetic_model.retained_rank,
            power_analyzer=BlockHoppingPowerAnalyzer(),
        ).execute()
        ordinary_comparison_power = BandEquivalenceLocalityFourierShellPowerAnalyzer(
            identifier="band-equivalence-comparison-ordinary",
            energy_reference=definition.synthetic_model.energy_reference,
            basis_identifier=definition.synthetic_model.retained_basis_identifier,
            series=ordinary_comparison_series,
            shell_indices=tuple(int(value) for value in metric_indices),
            retained_rank=definition.synthetic_model.retained_rank,
            power_analyzer=BlockHoppingPowerAnalyzer(),
        ).execute()
        shells = tuple(
            int(value)
            for value in sorted(set(metric_indices.tolist()))
            if value <= definition.shell_cap
        )
        reference_evaluations = self.complete_shell_fields(
            source_mesh,
            ordinary_reference_series,
            evaluation_axes,
            metric_indices,
            shells,
        )
        comparison_evaluations = self.complete_shell_fields(
            source_mesh,
            ordinary_comparison_series,
            evaluation_axes,
            metric_indices,
            shells,
        )
        reference_sources = self.complete_shell_fields(
            source_mesh,
            ordinary_reference_series,
            construction_axes,
            metric_indices,
            shells,
        )
        comparison_sources = self.complete_shell_fields(
            source_mesh,
            ordinary_comparison_series,
            construction_axes,
            metric_indices,
            shells,
        )
        shell_results: list[BandEquivalenceLocalityShellAnalysis] = []
        for (
            shell,
            reference_eval,
            comparison_eval,
            reference_source,
            comparison_source,
        ) in zip(
            shells,
            reference_evaluations,
            comparison_evaluations,
            reference_sources,
            comparison_sources,
            strict=True,
        ):
            retained_mask = metric_indices <= shell
            reference_shell_power = ordinary_reference_power.normalized_power_at_shell(
                shell
            )
            comparison_shell_power = (
                ordinary_comparison_power.normalized_power_at_shell(shell)
            )
            reference_omitted = ordinary_reference_power.normalized_power_beyond_shell(
                shell
            )
            comparison_omitted = (
                ordinary_comparison_power.normalized_power_beyond_shell(shell)
            )
            reference_source_truncation = self.error_channels(
                reference_source, full_reference_source
            )
            comparison_source_truncation = self.error_channels(
                comparison_source, full_comparison_source
            )
            shell_results.append(
                BandEquivalenceLocalityShellAnalysis(
                    shell_index=shell,
                    retained_blocks=int(np.count_nonzero(retained_mask)),
                    reference_truncation=self.error_channels(
                        reference_eval, full_reference_eval
                    ),
                    comparison_truncation=self.error_channels(
                        comparison_eval, full_comparison_eval
                    ),
                    reference_total=self.error_channels(
                        reference_eval, direct_reference_eval
                    ),
                    comparison_total=self.error_channels(
                        comparison_eval, direct_comparison_eval
                    ),
                    reference_shell_power=reference_shell_power,
                    comparison_shell_power=comparison_shell_power,
                    reference_omitted_power=reference_omitted,
                    comparison_omitted_power=comparison_omitted,
                    reference_total_omitted_power=(
                        reference_omitted + reference_nyquist_power
                    ),
                    comparison_total_omitted_power=(
                        comparison_omitted + comparison_nyquist_power
                    ),
                    reference_truncation_parseval_defect=abs(
                        reference_source_truncation.rms_hamiltonian**2
                        - reference_omitted
                    ),
                    comparison_truncation_parseval_defect=abs(
                        comparison_source_truncation.rms_hamiltonian**2
                        - comparison_omitted
                    ),
                )
            )
        decisions = tuple(
            self._first_passing(tuple(shell_results), tolerance)
            for tolerance in definition.band_tolerances
        )
        largest_mask = metric_indices <= shells[-1]
        basis_minimum, basis_maximum = basis_distance_range(
            case, ordinary_displacements[largest_mask]
        )
        return BandEquivalenceLocalityPointAnalysis(
            parent_scale=parent_scale,
            amplitude=amplitude,
            minimum_sampled_external_gap=minimum_sampled_external_gap,
            continuous_external_gap_lower_bound=continuous_external_gap_lower_bound,
            minimum_seed_overlap=minimum_seed_overlap,
            maximum_parent_hermiticity_defect=maximum_parent_hermiticity_defect,
            maximum_eigensystem_reconstruction_defect=(
                maximum_eigensystem_reconstruction_defect
            ),
            maximum_frame_orthonormality_defect=(maximum_frame_orthonormality_defect),
            maximum_projector_reconstruction_defect=(
                maximum_projector_reconstruction_defect
            ),
            maximum_parent_retained_reconstruction_defect=(
                maximum_parent_retained_reconstruction_defect
            ),
            maximum_parent_fourier_reconstruction_defect=(
                maximum_parent_fourier_reconstruction_defect
            ),
            maximum_periodic_frame_closure_defect=(
                maximum_periodic_frame_closure_defect
            ),
            minimum_sampled_transport_singular_value=(transport.minimum_singular_value),
            maximum_transport_procrustes_residual=(
                transport.maximum_procrustes_residual
            ),
            maximum_transport_squared_residual_roundoff_cutoff=(
                transport.maximum_squared_residual_roundoff_cutoff
            ),
            maximum_transport_unitarity_defect=transport.maximum_unitarity_defect,
            maximum_transport_rank_cutoff=transport.maximum_rank_cutoff,
            transport_rank_deficient_link_count=(transport.rank_deficient_link_count),
            transport_closure_and_plaquette_applicable=(
                transport.closure_and_plaquette_applicable
            ),
            transport_closure_and_plaquette_inapplicable_reason=(
                transport.closure_and_plaquette_inapplicable_reason
            ),
            maximum_absolute_closure_holonomy_phases=(
                transport.maximum_absolute_closure_phases
            ),
            maximum_closure_holonomy_unitarity_defect=(
                transport.maximum_closure_unitarity_defect
            ),
            maximum_plaquette_holonomy_phase=transport.maximum_plaquette_phase,
            maximum_direct_band_defect=direct_band_defect,
            maximum_covariant_defect=covariant_defect,
            alignment_applicable=correlation is not None,
            alignment_inapplicable_reason=(
                None
                if correlation is not None
                else "zero splitting scale: normalized correlation is undefined"
            ),
            restricted_global_rotation_angle=angle,
            restricted_global_rotation_degenerate=angle_degenerate,
            splitting_scale=splitting_scale,
            finite_mesh_maximum_correlation=correlation,
            analytic_flat_correlation=analytic_correlation,
            analytic_correlation_remainder_bound=analytic_remainder,
            correlation_quadrature_defect=correlation_defect,
            minimum_operator_threshold=minimum_threshold,
            exact_spectrum_joint_operator_threshold=exact_spectrum_threshold,
            minimum_operator_threshold_over_sqrt_splitting=(
                normalized_operator_threshold
            ),
            exact_spectrum_joint_threshold_over_sqrt_splitting=(
                normalized_joint_threshold
            ),
            normalized_squared_operator_residual=normalized_squared_residual,
            restricted_global_rotation_residual=minimum_threshold,
            reference_fourier_reconstruction_defect=self.matrix_defect(
                reconstructed_reference, reference
            ),
            comparison_fourier_reconstruction_defect=self.matrix_defect(
                reconstructed_comparison, comparison
            ),
            reference_parseval_defect=reference_parseval,
            comparison_parseval_defect=comparison_parseval,
            reference_twisted_nyquist_defect=reference_twisted,
            comparison_twisted_nyquist_defect=comparison_twisted,
            reference_ordinary_hermiticity_defect=reference_hermiticity,
            comparison_ordinary_hermiticity_defect=comparison_hermiticity,
            reference_interpolation=reference_interpolation,
            comparison_interpolation=comparison_interpolation,
            reference_total_power=reference_total_power,
            comparison_total_power=comparison_total_power,
            reference_onsite_power=reference_onsite_power,
            comparison_onsite_power=comparison_onsite_power,
            reference_nononsite_power=reference_nononsite_power,
            comparison_nononsite_power=comparison_nononsite_power,
            excess_nonzero_hopping_weight=excess_nonzero_power,
            normalized_excess_nonzero_hopping_weight=normalized_excess_power,
            flat_identity_departure=flat_identity_departure,
            reference_nyquist_power=reference_nyquist_power,
            comparison_nyquist_power=comparison_nyquist_power,
            flat_residual_tail_identity_defect=flat_identity_defect,
            basis_distance_minimum=basis_minimum,
            basis_distance_maximum=basis_maximum,
            shell_diagnostics=tuple(shell_results),
            first_passing=decisions,
        )


__all__ = ["BandEquivalenceLocalityAnalysis", "BandEquivalenceLocalityAnalyzer"]
