"""Independent finite-sum shell-power reference for result verification.

This module intentionally does not call the production analyzer, production Fourier
transformer, metric-shell classifier, or KSD metric-shell power analyzer. It shares
only the declared request geometry with production, then evaluates metric values,
finite Fourier sums, and normalized block powers through a separate numerical route.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import product

import numpy as np
from numpy.typing import NDArray

from .definitions import (
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityRequest,
    GaugeNormalizationEnum,
    ParentEnum,
)

type ComplexArray = NDArray[np.complex128]
type ReducedCoordinate = tuple[float, ...]
type IntegerDisplacement = tuple[int, ...]


def _independent_metric_indices(
    case: BandEquivalenceLocalityCase,
    displacements: NDArray[np.int64],
) -> NDArray[np.int64]:
    """Calculate shell values without calling the production classifier."""
    metric = case.direct_metric.metric_tensor
    values = case.shell_metric_scale * np.einsum(
        "ri,ij,rj->r",
        displacements,
        metric,
        displacements,
    )
    rounded = np.rint(values)
    if float(np.max(np.abs(values - rounded))) > 1.0e-12:
        raise ValueError("independent scaled metric values are not integral")
    return np.asarray(rounded, dtype=np.int64)


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityIndependentShellPower:
    """Retain independently reconstructed values for one metric shell."""

    shell_index: int
    reference_shell_power: float
    comparison_shell_power: float
    reference_omitted_power: float
    comparison_omitted_power: float
    reference_total_omitted_power: float
    comparison_total_omitted_power: float

    def __post_init__(self) -> None:
        """Validate one exact shell label and finite unitless binary64 values."""
        if type(self.shell_index) is not int:
            raise TypeError("shell_index must be a built-in integer")
        if self.shell_index < 0:
            raise ValueError("shell_index must be nonnegative")
        for value, name in (
            (self.reference_shell_power, "reference_shell_power"),
            (self.comparison_shell_power, "comparison_shell_power"),
            (self.reference_omitted_power, "reference_omitted_power"),
            (self.comparison_omitted_power, "comparison_omitted_power"),
            (self.reference_total_omitted_power, "reference_total_omitted_power"),
            (self.comparison_total_omitted_power, "comparison_total_omitted_power"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def metric_shell_value(self) -> int:
        """Return the independently calculated scaled metric shell value."""
        return self.shell_index


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityIndependentShellPowerPoint:
    """Retain one independently reconstructed sampled-point inventory."""

    case_name: str
    parent_scale: float
    amplitude: float
    reference_nyquist_power: float
    comparison_nyquist_power: float
    shells: tuple[BandEquivalenceLocalityIndependentShellPower, ...]

    def __post_init__(self) -> None:
        """Validate identity, finite scalars, and ordered shell ownership."""
        if type(self.case_name) is not str:
            raise TypeError("case_name must be a built-in string")
        if not self.case_name:
            raise ValueError("case_name must be nonempty")
        for value, name in (
            (self.parent_scale, "parent_scale"),
            (self.amplitude, "amplitude"),
            (self.reference_nyquist_power, "reference_nyquist_power"),
            (self.comparison_nyquist_power, "comparison_nyquist_power"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.shells) is not tuple or any(
            type(shell) is not BandEquivalenceLocalityIndependentShellPower
            for shell in self.shells
        ):
            raise TypeError(
                "shells must contain "
                "BandEquivalenceLocalityIndependentShellPower values"
            )
        shell_indices = tuple(shell.shell_index for shell in self.shells)
        if not shell_indices or shell_indices != tuple(sorted(set(shell_indices))):
            raise ValueError(
                "shells must be nonempty and ordered by unique shell index"
            )


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityIndependentShellPowerReference:
    """Retain the complete independent shell-power reference for one request."""

    request: BandEquivalenceLocalityRequest
    points: tuple[BandEquivalenceLocalityIndependentShellPowerPoint, ...]

    def __post_init__(self) -> None:
        """Validate request ownership and complete sampled-point ordering."""
        if type(self.request) is not BandEquivalenceLocalityRequest:
            raise TypeError("request must be BandEquivalenceLocalityRequest")
        if type(self.points) is not tuple or any(
            type(point) is not BandEquivalenceLocalityIndependentShellPowerPoint
            for point in self.points
        ):
            raise TypeError("points must contain independent shell-power point values")
        expected_identities = tuple(
            (case.name, parent_scale, amplitude)
            for case in self.request.cases
            for parent_scale in self.request.parent_scales
            for amplitude in self.request.amplitudes
        )
        observed_identities = tuple(
            (point.case_name, point.parent_scale, point.amplitude)
            for point in self.points
        )
        if observed_identities != expected_identities:
            raise ValueError("point identities must match the request inventory")


class BandEquivalenceLocalityIndependentShellPowerAnalyzer:
    """Reconstruct shell powers through an independent direct finite-sum route."""

    __slots__ = ("_request",)

    def __init__(self, *, request: BandEquivalenceLocalityRequest) -> None:
        """Bind one exact typed request before zero-argument execution."""
        if type(request) is not BandEquivalenceLocalityRequest:
            raise TypeError("request must be BandEquivalenceLocalityRequest")
        self._request = request

    @property
    def request(self) -> BandEquivalenceLocalityRequest:
        """Return the exact immutable request bound to this action."""
        return self._request

    def _coordinates(self) -> tuple[ReducedCoordinate, ...]:
        """Return the independently enumerated construction coordinates."""
        size = self._request.construction_size
        axis = tuple(-0.5 + (float(index) + 0.5) / float(size) for index in range(size))
        return tuple(
            tuple(values) for values in product(axis, repeat=self._request.dimension)
        )

    def _displacements(self) -> tuple[IntegerDisplacement, ...]:
        """Return the independently enumerated centered displacement inventory."""
        size = self._request.construction_size
        axis = range(-size // 2, size // 2)
        return tuple(
            tuple(values) for values in product(axis, repeat=self._request.dimension)
        )

    def _parent_at(
        self,
        case: BandEquivalenceLocalityCase,
        coordinate: ReducedCoordinate,
        parent_scale: float,
    ) -> ComplexArray:
        """Evaluate one synthetic parent through scalar finite formulas."""
        model = self._request.synthetic_model
        onsite = model.onsite.magnitude
        directed = model.directed_hopping.magnitude
        if case.parent_kind is ParentEnum.DIRECTED_AXIS:
            phase = math.fsum(
                math.cos(math.tau * value) for value in coordinate
            ) / float(case.dimension) + 1.0j * (
                math.fsum(math.sin(math.tau * value) for value in coordinate)
                / float(case.dimension)
            )
            return np.asarray(
                onsite
                + parent_scale
                * (phase * directed + phase.conjugate() * directed.conjugate().T),
                dtype=np.complex128,
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
            return np.asarray(
                onsite + parent_scale * structure * (directed + directed.conjugate().T),
                dtype=np.complex128,
            )
        gamma = (
            1.0
            + math.fsum(math.cos(-math.tau * value) for value in coordinate)
            + 1.0j * math.fsum(math.sin(-math.tau * value) for value in coordinate)
        ) / float(case.dimension + 1)
        sublattice = np.array(
            [[0.0, gamma], [gamma.conjugate(), 0.0]], dtype=np.complex128
        )
        result = np.zeros((4, 4), dtype=np.complex128)
        identity = np.eye(2, dtype=np.complex128)
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

    def _retained_at(self, parent: ComplexArray) -> ComplexArray:
        """Construct one retained matrix through an independent scalar route."""
        _, eigenvectors = np.linalg.eigh(parent)
        retained_rank = self._request.synthetic_model.retained_rank
        low = eigenvectors[:, :retained_rank]
        projector = low @ low.conjugate().T
        projected_seed = (
            projector @ self._request.synthetic_model.retained_seed.magnitude
        )
        seed_gram = projected_seed.conjugate().T @ projected_seed
        gram_values, gram_vectors = np.linalg.eigh(seed_gram)
        inverse_root = (
            gram_vectors * (1.0 / np.sqrt(gram_values))[None, :]
        ) @ gram_vectors.conjugate().T
        frame = projected_seed @ inverse_root
        return np.asarray(
            frame.conjugate().T @ parent @ frame,
            dtype=np.complex128,
        )

    def _gauge_angle(
        self,
        case: BandEquivalenceLocalityCase,
        coordinate: ReducedCoordinate,
        amplitude: float,
    ) -> float:
        """Evaluate one gauge angle through explicit scalar bond sums."""
        sine_sum = math.fsum(
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
            return amplitude * sine_sum / float(case.dimension)
        return amplitude * math.sqrt(2.0 / float(len(case.positive_bonds))) * sine_sum

    def _comparison_at(
        self,
        case: BandEquivalenceLocalityCase,
        coordinate: ReducedCoordinate,
        amplitude: float,
        reference: ComplexArray,
    ) -> ComplexArray:
        """Apply one independently evaluated real-orthogonal gauge rotation."""
        angle = self._gauge_angle(case, coordinate, amplitude)
        cosine = math.cos(angle)
        sine = math.sin(angle)
        rotation = np.array(
            [[cosine, -sine], [sine, cosine]],
            dtype=np.complex128,
        )
        return np.asarray(rotation.T @ reference @ rotation, dtype=np.complex128)

    def _direct_fourier_blocks(
        self,
        coordinates: tuple[ReducedCoordinate, ...],
        displacements: tuple[IntegerDisplacement, ...],
        fields: ComplexArray,
    ) -> ComplexArray:
        """Evaluate the explicit finite Fourier sum without the production FFT."""
        coordinate_array = np.asarray(coordinates, dtype=np.float64)
        displacement_array = np.asarray(displacements, dtype=np.float64)
        phases = np.exp(-1.0j * math.tau * (displacement_array @ coordinate_array.T))
        return np.asarray(
            np.einsum("rk,kij->rij", phases, fields, optimize=True)
            / float(len(coordinates)),
            dtype=np.complex128,
        )

    def _block_power(self, block: ComplexArray) -> float:
        """Return one direct retained-rank-normalized Frobenius power."""
        try:
            power = math.fsum(
                float(value.real) ** 2 + float(value.imag) ** 2 for value in block.flat
            ) / float(self._request.synthetic_model.retained_rank)
        except OverflowError as error:
            raise FloatingPointError("independent block power overflowed") from error
        if not math.isfinite(power) or power < 0.0:
            raise FloatingPointError("independent block power became invalid")
        return power

    def _finite_sum(self, values: tuple[float, ...]) -> float:
        """Return one finite direct sum or report binary64 overflow."""
        try:
            result = math.fsum(values)
        except OverflowError as error:
            raise FloatingPointError(
                "independent shell-power sum overflowed"
            ) from error
        if not math.isfinite(result) or result < 0.0:
            raise FloatingPointError("independent shell-power sum became invalid")
        return result

    def _point_reference(
        self,
        *,
        case: BandEquivalenceLocalityCase,
        parent_scale: float,
        amplitude: float,
        displacements: tuple[IntegerDisplacement, ...],
        reference_blocks: ComplexArray,
        comparison_blocks: ComplexArray,
    ) -> BandEquivalenceLocalityIndependentShellPowerPoint:
        """Aggregate one independent sampled-point shell inventory."""
        displacement_array = np.asarray(displacements, dtype=np.int64)
        labels = _independent_metric_indices(case, displacement_array)
        nyquist = np.any(
            displacement_array == -self._request.construction_size // 2,
            axis=1,
        )
        reference_powers = tuple(self._block_power(block) for block in reference_blocks)
        comparison_powers = tuple(
            self._block_power(block) for block in comparison_blocks
        )
        reference_nyquist = self._finite_sum(
            tuple(
                power
                for power, selected in zip(
                    reference_powers,
                    nyquist,
                    strict=True,
                )
                if selected
            )
        )
        comparison_nyquist = self._finite_sum(
            tuple(
                power
                for power, selected in zip(
                    comparison_powers,
                    nyquist,
                    strict=True,
                )
                if selected
            )
        )
        ordinary_labels = tuple(
            int(label)
            for label, selected in zip(labels, nyquist, strict=True)
            if not selected
        )
        ordinary_reference = tuple(
            power
            for power, selected in zip(reference_powers, nyquist, strict=True)
            if not selected
        )
        ordinary_comparison = tuple(
            power
            for power, selected in zip(comparison_powers, nyquist, strict=True)
            if not selected
        )
        shell_indices = tuple(
            shell
            for shell in sorted(set(ordinary_labels))
            if shell <= self._request.shell_cap
        )
        shells: list[BandEquivalenceLocalityIndependentShellPower] = []
        for shell_index in shell_indices:
            reference_omitted = self._finite_sum(
                tuple(
                    power
                    for label, power in zip(
                        ordinary_labels,
                        ordinary_reference,
                        strict=True,
                    )
                    if label > shell_index
                )
            )
            comparison_omitted = self._finite_sum(
                tuple(
                    power
                    for label, power in zip(
                        ordinary_labels,
                        ordinary_comparison,
                        strict=True,
                    )
                    if label > shell_index
                )
            )
            shells.append(
                BandEquivalenceLocalityIndependentShellPower(
                    shell_index=shell_index,
                    reference_shell_power=self._finite_sum(
                        tuple(
                            power
                            for label, power in zip(
                                ordinary_labels,
                                ordinary_reference,
                                strict=True,
                            )
                            if label == shell_index
                        )
                    ),
                    comparison_shell_power=self._finite_sum(
                        tuple(
                            power
                            for label, power in zip(
                                ordinary_labels,
                                ordinary_comparison,
                                strict=True,
                            )
                            if label == shell_index
                        )
                    ),
                    reference_omitted_power=reference_omitted,
                    comparison_omitted_power=comparison_omitted,
                    reference_total_omitted_power=self._finite_sum(
                        (reference_nyquist, reference_omitted)
                    ),
                    comparison_total_omitted_power=self._finite_sum(
                        (comparison_nyquist, comparison_omitted)
                    ),
                )
            )
        return BandEquivalenceLocalityIndependentShellPowerPoint(
            case_name=case.name,
            parent_scale=parent_scale,
            amplitude=amplitude,
            reference_nyquist_power=reference_nyquist,
            comparison_nyquist_power=comparison_nyquist,
            shells=tuple(shells),
        )

    def execute(self) -> BandEquivalenceLocalityIndependentShellPowerReference:
        """Return independently reconstructed shell powers for every sampled point."""
        points: list[BandEquivalenceLocalityIndependentShellPowerPoint] = []
        coordinates = self._coordinates()
        displacements = self._displacements()
        for case in self._request.cases:
            for parent_scale in self._request.parent_scales:
                reference_values = np.asarray(
                    tuple(
                        self._retained_at(
                            self._parent_at(case, coordinate, parent_scale)
                        )
                        for coordinate in coordinates
                    ),
                    dtype=np.complex128,
                )
                reference_blocks = self._direct_fourier_blocks(
                    coordinates,
                    displacements,
                    reference_values,
                )
                for amplitude in self._request.amplitudes:
                    comparison_values = np.asarray(
                        tuple(
                            self._comparison_at(
                                case,
                                coordinate,
                                amplitude,
                                reference,
                            )
                            for coordinate, reference in zip(
                                coordinates,
                                reference_values,
                                strict=True,
                            )
                        ),
                        dtype=np.complex128,
                    )
                    comparison_blocks = self._direct_fourier_blocks(
                        coordinates,
                        displacements,
                        comparison_values,
                    )
                    points.append(
                        self._point_reference(
                            case=case,
                            parent_scale=parent_scale,
                            amplitude=amplitude,
                            displacements=displacements,
                            reference_blocks=reference_blocks,
                            comparison_blocks=comparison_blocks,
                        )
                    )
        return BandEquivalenceLocalityIndependentShellPowerReference(
            request=self._request,
            points=tuple(points),
        )


__all__ = [
    "BandEquivalenceLocalityIndependentShellPower",
    "BandEquivalenceLocalityIndependentShellPowerAnalyzer",
    "BandEquivalenceLocalityIndependentShellPowerPoint",
    "BandEquivalenceLocalityIndependentShellPowerReference",
]
