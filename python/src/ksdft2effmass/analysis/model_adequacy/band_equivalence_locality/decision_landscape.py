"""Sampled shell--scale decision landscapes for rank-two locality studies."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.numerics.finite_periodic.numpy.transforms import (
    NumpyCenteredUniformMeshMatrixFourierTransformDefinition,
    NumpyCenteredUniformMeshMatrixFourierTransformer,
)

from .alignment import restricted_alignment
from .calculation import (
    _coordinate_axis,
    _coordinates,
    _gauge_angles,
    _parent_field,
    _retained_field,
    _retained_frame,
    _rotation_field,
)
from .definitions import (
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityFamily,
    BandEquivalenceLocalityRequest,
)
from .fourier import error_channels, iter_complete_shell_fields
from .geometry import metric_indices


@dataclass(frozen=True, slots=True)
class ShellScaleDecisionLandscapeRequest:
    """Select one bounded shell--scale calculation."""

    locality_request: BandEquivalenceLocalityRequest
    scale_sample_count: int = 17

    def __post_init__(self) -> None:
        if type(self.locality_request) is not BandEquivalenceLocalityRequest:
            raise TypeError("locality_request must be BandEquivalenceLocalityRequest")
        if (
            type(self.scale_sample_count) is not int
            or not 2 <= self.scale_sample_count <= 1001
        ):
            raise ValueError(
                "scale_sample_count must be a built-in integer in [2, 1001]"
            )


@dataclass(frozen=True, slots=True)
class ShellScaleDecisionPoint:
    """Retain one calculated objective vector and its decision coordinates."""

    shell_index: int
    retained_blocks: int
    scale_path_coordinate: float
    comparison_scale: float
    maximum_hamiltonian_error: float
    maximum_sorted_band_error: float
    pareto_efficient: bool

    def __post_init__(self) -> None:
        if type(self.shell_index) is not int or self.shell_index < 0:
            raise ValueError("shell_index must be a nonnegative built-in integer")
        if type(self.retained_blocks) is not int or self.retained_blocks < 1:
            raise ValueError("retained_blocks must be a positive built-in integer")
        for name, value in (
            ("scale_path_coordinate", self.scale_path_coordinate),
            ("comparison_scale", self.comparison_scale),
            ("maximum_hamiltonian_error", self.maximum_hamiltonian_error),
            ("maximum_sorted_band_error", self.maximum_sorted_band_error),
        ):
            if type(value) is not float or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite built-in float")
        if not 0.0 <= self.scale_path_coordinate <= 1.0:
            raise ValueError("scale_path_coordinate must lie in [0, 1]")
        if (
            self.comparison_scale < 0.0
            or self.maximum_hamiltonian_error < 0.0
            or self.maximum_sorted_band_error < 0.0
        ):
            raise ValueError("scale and error values must be nonnegative")
        if type(self.pareto_efficient) is not bool:
            raise TypeError("pareto_efficient must be a built-in bool")


@dataclass(frozen=True, slots=True)
class ShellScaleCaseDecisionLandscape:
    """Retain one independently interpreted case landscape."""

    name: str
    parent_scale: float
    gauge_amplitude: float
    optimized_comparison_scale: float
    shell_indices: tuple[int, ...]
    retained_block_counts: tuple[int, ...]
    scale_path_coordinates: tuple[float, ...]
    comparison_scales: tuple[float, ...]
    points: tuple[ShellScaleDecisionPoint, ...]

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise ValueError("name must be a nonempty built-in str")
        for name, value in (
            ("parent_scale", self.parent_scale),
            ("gauge_amplitude", self.gauge_amplitude),
            ("optimized_comparison_scale", self.optimized_comparison_scale),
        ):
            if type(value) is not float or not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative built-in float")
        if type(self.shell_indices) is not tuple or not self.shell_indices:
            raise TypeError("shell_indices must be a nonempty tuple")
        if type(self.retained_block_counts) is not tuple:
            raise TypeError("retained_block_counts must be a tuple")
        if len(self.shell_indices) != len(self.retained_block_counts):
            raise ValueError(
                "shell and retained-block inventories must have equal length"
            )
        if any(type(value) is not int or value < 0 for value in self.shell_indices):
            raise ValueError("shell_indices must contain nonnegative built-in integers")
        if any(
            type(value) is not int or value < 1 for value in self.retained_block_counts
        ):
            raise ValueError(
                "retained_block_counts must contain positive built-in integers"
            )
        if tuple(sorted(set(self.shell_indices))) != self.shell_indices:
            raise ValueError("shell_indices must be strictly increasing")
        if tuple(sorted(self.retained_block_counts)) != self.retained_block_counts:
            raise ValueError("retained_block_counts must be nondecreasing")
        if (
            type(self.scale_path_coordinates) is not tuple
            or len(self.scale_path_coordinates) < 2
            or type(self.comparison_scales) is not tuple
            or len(self.comparison_scales) != len(self.scale_path_coordinates)
        ):
            raise ValueError(
                "scale coordinates and scales must be equal tuples of length >= 2"
            )
        if (
            self.scale_path_coordinates[0] != 0.0
            or self.scale_path_coordinates[-1] != 1.0
        ):
            raise ValueError("scale path must include the exact endpoints zero and one")
        if tuple(sorted(self.scale_path_coordinates)) != self.scale_path_coordinates:
            raise ValueError("scale_path_coordinates must be nondecreasing")
        if self.comparison_scales[0] != self.optimized_comparison_scale:
            raise ValueError(
                "the first comparison scale must equal the optimized scale"
            )
        if self.comparison_scales[-1] != 1.0:
            raise ValueError("the final comparison scale must equal one")
        expected_points = len(self.shell_indices) * len(self.scale_path_coordinates)
        if type(self.points) is not tuple or len(self.points) != expected_points:
            raise ValueError("points must cover the complete scale--shell product grid")
        for scale_index, (coordinate, scale) in enumerate(
            zip(self.scale_path_coordinates, self.comparison_scales, strict=True)
        ):
            for shell_index, (shell, block_count) in enumerate(
                zip(self.shell_indices, self.retained_block_counts, strict=True)
            ):
                point = self.points[scale_index * len(self.shell_indices) + shell_index]
                if (
                    point.scale_path_coordinate != coordinate
                    or point.comparison_scale != scale
                    or point.shell_index != shell
                    or point.retained_blocks != block_count
                ):
                    raise ValueError(
                        "points do not follow scale-major shell-minor order"
                    )

    @property
    def calculated_vertex_count(self) -> int:
        """Return the number of calculated decision vertices."""
        return len(self.points)

    @property
    def pareto_efficient_vertex_count(self) -> int:
        """Return the number of nondominated calculated vertices."""
        return sum(point.pareto_efficient for point in self.points)


@dataclass(frozen=True, slots=True)
class ShellScaleDecisionLandscapeResult:
    """Retain all case landscapes for one family request."""

    family: BandEquivalenceLocalityFamily
    construction_size: int
    evaluation_size: int
    scale_sample_count: int
    cases: tuple[ShellScaleCaseDecisionLandscape, ...]
    status: str = "sampled-development-landscape-not-continuum-or-acceptance-evidence"

    def __post_init__(self) -> None:
        if type(self.family) is not BandEquivalenceLocalityFamily:
            raise TypeError("family must be BandEquivalenceLocalityFamily")
        for name, value in (
            ("construction_size", self.construction_size),
            ("evaluation_size", self.evaluation_size),
            ("scale_sample_count", self.scale_sample_count),
        ):
            if type(value) is not int or value < 2:
                raise ValueError(f"{name} must be a built-in integer >= 2")
        if type(self.cases) is not tuple or not self.cases:
            raise TypeError("cases must be a nonempty tuple")
        if any(
            type(case) is not ShellScaleCaseDecisionLandscape for case in self.cases
        ):
            raise TypeError("cases must contain ShellScaleCaseDecisionLandscape values")
        if any(
            len(case.scale_path_coordinates) != self.scale_sample_count
            for case in self.cases
        ):
            raise ValueError("case scale grids must match scale_sample_count")
        if type(self.status) is not str or not self.status:
            raise ValueError("status must be a nonempty built-in str")


def _dominates(
    candidate: tuple[int, float, float],
    point: tuple[int, float, float],
) -> bool:
    return (
        candidate[0] <= point[0]
        and candidate[1] <= point[1]
        and candidate[2] <= point[2]
        and (
            candidate[0] < point[0]
            or candidate[1] < point[1]
            or candidate[2] < point[2]
        )
    )


def _pareto_efficient_mask(
    objectives: tuple[tuple[int, float, float], ...],
) -> tuple[bool, ...]:
    return tuple(
        not any(
            other_index != point_index and _dominates(other, point)
            for other_index, other in enumerate(objectives)
        )
        for point_index, point in enumerate(objectives)
    )


class ShellScaleDecisionLandscapeCalculator:
    """Calculate sampled rank-two shell--scale objective landscapes."""

    __slots__ = ()

    def execute(
        self, request: ShellScaleDecisionLandscapeRequest
    ) -> ShellScaleDecisionLandscapeResult:
        """Calculate every case at maximum parent scale and gauge amplitude."""
        if type(request) is not ShellScaleDecisionLandscapeRequest:
            raise TypeError("request must be ShellScaleDecisionLandscapeRequest")
        definition = request.locality_request
        return ShellScaleDecisionLandscapeResult(
            family=definition.family,
            construction_size=definition.construction_size,
            evaluation_size=definition.evaluation_size,
            scale_sample_count=request.scale_sample_count,
            cases=tuple(
                self._case(definition, case, request.scale_sample_count)
                for case in definition.cases
            ),
        )

    def _case(
        self,
        definition: BandEquivalenceLocalityRequest,
        case: BandEquivalenceLocalityCase,
        scale_sample_count: int,
    ) -> ShellScaleCaseDecisionLandscape:
        parent_scale = max(definition.parent_scales)
        amplitude = max(definition.amplitudes)
        construction = _coordinates(
            definition.construction_size,
            case.dimension,
            0.5,
        )
        evaluation = _coordinates(
            definition.evaluation_size,
            case.dimension,
            0.5 + definition.evaluation_shift,
        )
        parent = _parent_field(case, construction, parent_scale)
        frame, _, _ = _retained_frame(parent)
        reference = _retained_field(frame, parent)
        rotation = _rotation_field(_gauge_angles(case, construction, amplitude))
        comparison = np.swapaxes(rotation.conjugate(), -1, -2) @ reference @ rotation
        direct_parent = _parent_field(case, evaluation, parent_scale)
        direct_frame, _, _ = _retained_frame(direct_parent)
        direct_reference = _retained_field(direct_frame, direct_parent)
        angle, _, _, correlation, _, _ = restricted_alignment(reference, comparison)
        if angle is None or correlation is None:
            raise ValueError(
                f"case {case.name!r} has no applicable restricted alignment"
            )
        optimized_scale = max(0.0, correlation)
        scale_coordinates = tuple(
            float(index) / float(scale_sample_count - 1)
            for index in range(scale_sample_count)
        )
        comparison_scales = tuple(
            (1.0 - coordinate) * optimized_scale + coordinate
            for coordinate in scale_coordinates
        )

        source_mesh = CenteredUniformMesh(
            case.dimension,
            definition.construction_size,
            (0.5,) * case.dimension,
        )
        transform = NumpyCenteredUniformMeshMatrixFourierTransformer().transform(
            NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                source_mesh,
                comparison,
            )
        )
        displacements = transform.series.integer_modes
        blocks = transform.series.matrix_coefficients
        ordinary = ~np.any(
            displacements == -definition.construction_size // 2,
            axis=1,
        )
        ordinary_displacements = displacements[ordinary]
        ordinary_blocks = blocks[ordinary]
        ordinary_series = NumpyFiniteFourierMatrixSeries.from_arrays(
            case.dimension,
            ordinary_displacements,
            ordinary_blocks,
        )
        indices = metric_indices(case, ordinary_displacements)
        shells = tuple(
            int(value)
            for value in sorted(set(indices.tolist()))
            if value <= definition.shell_cap
        )
        if not shells:
            raise ValueError(f"case {case.name!r} has no shell within the declared cap")
        retained_blocks = tuple(
            int(np.count_nonzero(indices <= shell)) for shell in shells
        )
        evaluation_axis = _coordinate_axis(
            definition.evaluation_size,
            0.5 + definition.evaluation_shift,
        )
        shell_fields = tuple(
            iter_complete_shell_fields(
                source_mesh,
                ordinary_series,
                (evaluation_axis,) * case.dimension,
                indices,
                shells,
            )
        )

        cosine = np.cos(angle)
        sine = np.sin(angle)
        global_rotation = np.asarray(
            ((cosine, -sine), (sine, cosine)),
            dtype=np.complex128,
        )
        identity = np.eye(2, dtype=np.complex128)
        trace = np.trace(direct_reference, axis1=-2, axis2=-1).real / 2.0
        traceless = direct_reference - trace[..., None, None] * identity
        aligned_reference = global_rotation.T @ traceless @ global_rotation

        raw_points: list[tuple[int, int, float, float, float, float]] = []
        for coordinate, scale in zip(
            scale_coordinates,
            comparison_scales,
            strict=True,
        ):
            target = trace[..., None, None] * identity + scale * aligned_reference
            for shell, block_count, shell_field in zip(
                shells,
                retained_blocks,
                shell_fields,
                strict=True,
            ):
                channels = error_channels(shell_field, target)
                raw_points.append(
                    (
                        shell,
                        block_count,
                        coordinate,
                        scale,
                        channels.maximum_hamiltonian,
                        channels.maximum_band,
                    )
                )
        objectives = tuple((point[1], point[4], point[5]) for point in raw_points)
        efficient = _pareto_efficient_mask(objectives)
        points = tuple(
            ShellScaleDecisionPoint(
                shell_index=point[0],
                retained_blocks=point[1],
                scale_path_coordinate=point[2],
                comparison_scale=point[3],
                maximum_hamiltonian_error=point[4],
                maximum_sorted_band_error=point[5],
                pareto_efficient=is_efficient,
            )
            for point, is_efficient in zip(raw_points, efficient, strict=True)
        )
        return ShellScaleCaseDecisionLandscape(
            name=case.name,
            parent_scale=parent_scale,
            gauge_amplitude=amplitude,
            optimized_comparison_scale=optimized_scale,
            shell_indices=shells,
            retained_block_counts=retained_blocks,
            scale_path_coordinates=scale_coordinates,
            comparison_scales=comparison_scales,
            points=points,
        )


__all__ = [
    "ShellScaleCaseDecisionLandscape",
    "ShellScaleDecisionLandscapeCalculator",
    "ShellScaleDecisionLandscapeRequest",
    "ShellScaleDecisionLandscapeResult",
    "ShellScaleDecisionPoint",
]
