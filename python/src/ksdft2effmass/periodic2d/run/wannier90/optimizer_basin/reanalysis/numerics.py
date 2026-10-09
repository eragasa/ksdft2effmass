"""Bounded numerical Actions for optimizer-basin reanalysis verification."""

import itertools
import math
from dataclasses import dataclass

from .records import (
    OptimizerBasinSourceEndpoint,
    OptimizerReanalysisEndpoint,
    PeriodicCenterSet2D,
)

_TRACE_DELTA_TOLERANCE = 1.0e-8
_TRACE_GRADIENT_TOLERANCE = 1.0e-3
_DESCENT_SLOPE_TOLERANCE = -1.0e-8
_DETRENDED_SPREAD_RMS_TOLERANCE = 1.0e-5
_SPREAD_COMPONENT_TOLERANCE = 2.0e-8
_SQUARE_LATTICE_OPERATION_COUNT = 8


class OptimizerReanalysisTerminalTraceClassifier:
    """Apply the retained post-hoc descriptive endpoint classifier."""

    __slots__ = ()

    def execute(self, endpoint: OptimizerReanalysisEndpoint) -> str:
        """Return one endpoint's retained descriptive terminal class.

        Parameters
        ----------
        endpoint
            Typed endpoint containing native convergence and terminal trace metrics.

        Returns
        -------
        str
            One fixed descriptive class. It is not a native convergence decision or
            acceptance criterion.

        Raises
        ------
        TypeError
            If ``endpoint`` is not the exact decoded endpoint type.
        """
        if type(endpoint) is not OptimizerReanalysisEndpoint:
            raise TypeError("endpoint must be OptimizerReanalysisEndpoint")
        metrics = endpoint.spread_components
        if endpoint.convergence_criterion_satisfied:
            return "native_converged"
        if (
            metrics.terminal_median_absolute_delta_spread <= _TRACE_DELTA_TOLERANCE
            and metrics.terminal_median_rms_gradient <= _TRACE_GRADIENT_TOLERANCE
        ):
            return "near_stationary_without_window_convergence"
        if metrics.terminal_spread_slope_per_iteration < _DESCENT_SLOPE_TOLERANCE:
            return "continuing_descent_at_iteration_limit"
        if metrics.terminal_detrended_spread_rms > _DETRENDED_SPREAD_RMS_TOLERANCE:
            return "oscillatory_or_stalled"
        return "stalled_or_nondescent"


class OptimizerReanalysisEndpointSpreadVerifier:
    """Verify retained spread algebra and source total-spread correlation."""

    __slots__ = ("trace_classifier",)

    def __init__(self) -> None:
        """Create one verifier with the fixed descriptive trace classifier."""
        self.trace_classifier = OptimizerReanalysisTerminalTraceClassifier()

    def execute(
        self,
        endpoint: OptimizerReanalysisEndpoint,
        source_endpoint: OptimizerBasinSourceEndpoint,
    ) -> str:
        """Verify one endpoint and return its reconstructed descriptive class.

        Parameters
        ----------
        endpoint
            Typed offline-reanalysis endpoint.
        source_endpoint
            Corresponding typed source-result endpoint.

        Returns
        -------
        str
            Reconstructed descriptive terminal class.

        Raises
        ------
        TypeError
            If either endpoint has an incompatible exact decoded type.
        AssertionError
            If retained spread algebra, source total spread, or classification differs.
        """
        if type(endpoint) is not OptimizerReanalysisEndpoint:
            raise TypeError("endpoint must be OptimizerReanalysisEndpoint")
        if type(source_endpoint) is not OptimizerBasinSourceEndpoint:
            raise TypeError("source_endpoint must be OptimizerBasinSourceEndpoint")
        components = endpoint.spread_components
        # The retained decomposition defines Omega_tilde as the sum of the diagonal and
        # off-diagonal gauge-dependent components; no missing term is inferred.
        omega_tilde = components.omega_d_cell_squared + components.omega_od_cell_squared
        if (
            abs(components.omega_tilde_cell_squared - omega_tilde)
            > _SPREAD_COMPONENT_TOLERANCE
        ):
            raise AssertionError(
                f"{endpoint.configuration_id}/{endpoint.gauge_id}: Omega_tilde changed"
            )
        omega_total = components.omega_i_cell_squared + omega_tilde
        if (
            abs(components.omega_total_cell_squared - omega_total)
            > _SPREAD_COMPONENT_TOLERANCE
        ):
            raise AssertionError(
                f"{endpoint.configuration_id}/{endpoint.gauge_id}: Omega_total changed"
            )
        if (
            abs(
                source_endpoint.native_total_spread_cell_squared
                - components.omega_total_cell_squared
            )
            > _SPREAD_COMPONENT_TOLERANCE
        ):
            raise AssertionError(
                f"{endpoint.configuration_id}/{endpoint.gauge_id}: "
                "source total spread changed"
            )
        classification = self.trace_classifier.execute(endpoint)
        if classification != components.diagnostic_classification:
            raise AssertionError(
                f"{endpoint.configuration_id}/{endpoint.gauge_id}: "
                "diagnostic class changed"
            )
        return classification


@dataclass(frozen=True, slots=True)
class PeriodicCenterSetComparisonRequest:
    """Request periodic center matching with explicit symmetry policy.

    Parameters
    ----------
    first, second
        Nonempty immutable finite center sets in periodic cell coordinates.
    include_square_lattice_symmetry
        Whether matching minimizes over the eight retained square-lattice operations.
    """

    first: PeriodicCenterSet2D
    second: PeriodicCenterSet2D
    include_square_lattice_symmetry: bool

    def __post_init__(self) -> None:
        """Validate immutable center sets and the exact symmetry-policy flag."""
        self._check_args_centers()
        if type(self.include_square_lattice_symmetry) is not bool:
            raise TypeError("include_square_lattice_symmetry must be a built-in bool")

    def _check_args_centers(self) -> None:
        """Require nonempty exact tuples of finite two-coordinate float tuples."""
        for name, centers in (("first", self.first), ("second", self.second)):
            if type(centers) is not tuple:
                raise TypeError(f"{name} must be an exact tuple")
            if not centers:
                raise ValueError(f"{name} must be nonempty")
            for center in centers:
                if type(center) is not tuple or len(center) != 2:
                    raise TypeError(f"{name} centers must be exact coordinate pairs")
                if any(type(value) is not float for value in center):
                    raise TypeError(f"{name} coordinates must be binary64 floats")
                if any(not math.isfinite(value) for value in center):
                    raise ValueError(f"{name} coordinates must be finite")


class SquareLatticeCenterSetTransformer:
    """Apply one of the eight retained square-lattice coordinate operations."""

    __slots__ = ()

    def execute(
        self, centers: PeriodicCenterSet2D, operation: int
    ) -> PeriodicCenterSet2D:
        """Return periodically wrapped centers after one indexed operation.

        Parameters
        ----------
        centers
            Immutable finite centers in periodic cell coordinates.
        operation
            Integer index of one retained square-lattice operation.

        Returns
        -------
        PeriodicCenterSet2D
            Transformed centers wrapped componentwise into one cell.

        Raises
        ------
        TypeError
            If centers or ``operation`` have incompatible exact representations.
        ValueError
            If centers are empty/nonfinite or ``operation`` lies outside the retained
            eight-operation family.
        """
        validated = PeriodicCenterSetComparisonRequest(
            first=centers,
            second=centers,
            include_square_lattice_symmetry=False,
        )
        if type(operation) is not int:
            raise TypeError("operation must be an integer")
        if not 0 <= operation < _SQUARE_LATTICE_OPERATION_COUNT:
            raise ValueError("operation must index the eight square-lattice operations")
        transformed: list[tuple[float, float]] = []
        for x, y in validated.first:
            a, b = (
                (x, y),
                (-y, x),
                (-x, -y),
                (y, -x),
                (x, -y),
                (-x, y),
                (y, x),
                (-y, -x),
            )[operation]
            transformed.append((a % 1.0, b % 1.0))
        return tuple(transformed)


class PeriodicCenterSetDistanceEvaluator:
    """Evaluate permutation-minimized periodic center-set distance."""

    __slots__ = ()

    def execute(self, first: PeriodicCenterSet2D, second: PeriodicCenterSet2D) -> float:
        """Return the minimum maximum distance over all orbital permutations.

        Parameters
        ----------
        first, second
            Equal-cardinality nonempty center sets in periodic cell coordinates.

        Returns
        -------
        float
            Minimum over permutations of the maximum periodic Euclidean distance.

        Raises
        ------
        TypeError
            If either center set has an incompatible exact representation.
        ValueError
            If either center set is empty or contains nonfinite coordinates.
        AssertionError
            If center-set cardinalities differ.

        Notes
        -----
        This dense operation enumerates :math:`n!` permutations at retained rank
        ``n``. It imposes no arbitrary size cap and can require substantial time or
        memory for large caller-supplied center sets.
        """
        validated = PeriodicCenterSetComparisonRequest(
            first=first,
            second=second,
            include_square_lattice_symmetry=False,
        )
        if len(validated.first) != len(validated.second):
            raise AssertionError("center sets must have equal cardinality")
        return min(
            max(
                math.sqrt(
                    sum(
                        min(abs(a - b), 1.0 - abs(a - b)) ** 2
                        for a, b in zip(
                            validated.first[index],
                            validated.second[target],
                            strict=True,
                        )
                    )
                )
                for index, target in enumerate(permutation)
            )
            for permutation in itertools.permutations(range(len(validated.second)))
        )


class PeriodicCenterSetComparator:
    """Compare periodic center sets with an explicit square-lattice symmetry policy."""

    __slots__ = ("distance_evaluator", "transformer")

    def __init__(self) -> None:
        """Create one comparator with explicit transformation and distance Actions."""
        self.distance_evaluator = PeriodicCenterSetDistanceEvaluator()
        self.transformer = SquareLatticeCenterSetTransformer()

    def execute(self, request: PeriodicCenterSetComparisonRequest) -> float:
        """Return the minimum requested periodic center-set distance.

        Parameters
        ----------
        request
            Validated center sets and explicit square-lattice symmetry policy.

        Returns
        -------
        float
            Minimum periodic distance under the requested operation family.

        Raises
        ------
        TypeError
            If ``request`` has an incompatible exact type.
        AssertionError
            If center-set cardinalities differ.
        MemoryError
            If dense permutation comparison cannot allocate required state.
        """
        if type(request) is not PeriodicCenterSetComparisonRequest:
            raise TypeError("request must be PeriodicCenterSetComparisonRequest")
        if len(request.first) != len(request.second):
            raise AssertionError("center sets must have equal cardinality")
        if not request.first:
            raise ValueError("center sets must be nonempty")
        operation_count = (
            _SQUARE_LATTICE_OPERATION_COUNT
            if request.include_square_lattice_symmetry
            else 1
        )
        return min(
            self.distance_evaluator.execute(
                self.transformer.execute(request.first, operation), request.second
            )
            for operation in range(operation_count)
        )


@dataclass(frozen=True, slots=True)
class OptimizerReanalysisBasinPartitionRequest:
    """Request the retained representative basin partition.

    Parameters
    ----------
    endpoints
        Nonempty immutable sequence of native-converged endpoints.
    spread_tolerance
        Finite nonnegative absolute gauge-dependent-spread tolerance.
    center_tolerance
        Finite nonnegative periodic center-set tolerance.
    """

    endpoints: tuple[OptimizerReanalysisEndpoint, ...]
    spread_tolerance: float
    center_tolerance: float

    def __post_init__(self) -> None:
        """Validate immutable endpoints and finite nonnegative tolerances."""
        self._check_args_endpoints()
        self._check_args_tolerances()

    def _check_args_endpoints(self) -> None:
        """Require a nonempty exact tuple of decoded endpoint records."""
        if type(self.endpoints) is not tuple:
            raise TypeError("endpoints must be an exact tuple")
        if not self.endpoints:
            raise ValueError("endpoints must be nonempty")
        if any(
            type(value) is not OptimizerReanalysisEndpoint for value in self.endpoints
        ):
            raise TypeError("endpoints must contain exact reanalysis endpoint records")

    def _check_args_tolerances(self) -> None:
        """Require finite nonnegative binary64 basin tolerances."""
        for name, value in (
            ("spread_tolerance", self.spread_tolerance),
            ("center_tolerance", self.center_tolerance),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a binary64 float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


class OptimizerReanalysisBasinPartitioner:
    """Construct the retained order-dependent square-lattice basin partition."""

    __slots__ = ("center_comparator",)

    def __init__(self) -> None:
        """Create one partitioner with a periodic center-set comparator."""
        self.center_comparator = PeriodicCenterSetComparator()

    def execute(
        self, request: OptimizerReanalysisBasinPartitionRequest
    ) -> tuple[tuple[str, ...], ...]:
        """Return sorted gauge memberships for bounded observed basins.

        Parameters
        ----------
        request
            Native-converged endpoints and explicit spread/center tolerances.

        Returns
        -------
        tuple[tuple[str, ...], ...]
            Representative-order basin partition with sorted member identities.

        Raises
        ------
        TypeError
            If ``request`` has an incompatible exact type.
        AssertionError
            If compared center sets have inconsistent cardinality.
        MemoryError
            If dense permutation comparison cannot allocate required state.
        """
        if type(request) is not OptimizerReanalysisBasinPartitionRequest:
            raise TypeError("request must be OptimizerReanalysisBasinPartitionRequest")
        clusters: list[list[OptimizerReanalysisEndpoint]] = []
        # Representative selection is intentionally order-dependent: the lowest
        # Omega_tilde endpoint, tie-broken by gauge identity, seeds each observed basin.
        ordered = sorted(
            request.endpoints,
            key=lambda endpoint: (
                endpoint.spread_components.omega_tilde_cell_squared,
                endpoint.gauge_id,
            ),
        )
        for endpoint in ordered:
            match: list[OptimizerReanalysisEndpoint] | None = None
            for cluster in clusters:
                representative = cluster[0]
                spread_distance = abs(
                    endpoint.spread_components.omega_tilde_cell_squared
                    - representative.spread_components.omega_tilde_cell_squared
                )
                center_distance = self.center_comparator.execute(
                    PeriodicCenterSetComparisonRequest(
                        first=endpoint.native_centers_modulo_cell,
                        second=representative.native_centers_modulo_cell,
                        include_square_lattice_symmetry=True,
                    )
                )
                if (
                    spread_distance <= request.spread_tolerance
                    and center_distance <= request.center_tolerance
                ):
                    match = cluster
                    break
            if match is None:
                clusters.append([endpoint])
            else:
                match.append(endpoint)
        return tuple(
            tuple(sorted(endpoint.gauge_id for endpoint in cluster))
            for cluster in clusters
        )
