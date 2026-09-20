"""Band-spectrum, isolation, and reduced-operator errors on reciprocal paths."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    MatrixQuantity,
    ScalarQuantity,
    VectorQuantity,
)
from ksdft2effmass.solid_state import ReciprocalOperatorSamples1D


@dataclass(frozen=True, slots=True, eq=False)
class BandSpectrumSamples1D:
    """Retain ordered real band eigenvalues at reciprocal coordinates."""

    coordinates: VectorQuantity
    reciprocal_period: ScalarQuantity
    eigenvalues: MatrixQuantity

    def __post_init__(self) -> None:
        """Validate coordinate and eigenvalue sample dimensions."""
        if type(self.coordinates) is not VectorQuantity:
            raise TypeError("coordinates must be VectorQuantity")
        if type(self.reciprocal_period) is not ScalarQuantity:
            raise TypeError("reciprocal_period must be ScalarQuantity")
        if self.reciprocal_period.magnitude <= 0.0:
            raise ValueError("reciprocal_period must be positive")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.coordinates.unit, self.reciprocal_period.unit
        ):
            raise ValueError("coordinates and reciprocal_period must be compatible")
        object.__setattr__(
            self,
            "coordinates",
            MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
                self.coordinates, self.reciprocal_period.unit
            ),
        )
        if type(self.eigenvalues) is not MatrixQuantity:
            raise TypeError("eigenvalues must be MatrixQuantity")
        sample_count, band_count = self.eigenvalues.magnitude.shape
        if sample_count != self.coordinates.magnitude.size:
            raise ValueError("eigenvalue rows must equal coordinate count")
        if band_count == 0:
            raise ValueError("at least one band must be retained")
        if np.any(np.diff(self.eigenvalues.magnitude, axis=1) < 0.0):
            raise ValueError("eigenvalues must be nondecreasing within each sample")

    @property
    def sample_count(self) -> int:
        """Return the reciprocal sample count."""
        return int(self.eigenvalues.magnitude.shape[0])

    @property
    def band_count(self) -> int:
        """Return the retained band count."""
        return int(self.eigenvalues.magnitude.shape[1])


@dataclass(frozen=True, slots=True)
class ContiguousBandSelection:
    """Identify one inclusive contiguous zero-based band interval."""

    lower_index: int
    upper_index: int

    def __post_init__(self) -> None:
        """Validate nonnegative ordered built-in integer indices."""
        if type(self.lower_index) is not int or type(self.upper_index) is not int:
            raise TypeError("band indices must be built-in integers")
        if self.lower_index < 0 or self.upper_index < self.lower_index:
            raise ValueError("band indices must be nonnegative and ordered")

    @property
    def band_count(self) -> int:
        """Return the selected subspace rank."""
        return self.upper_index - self.lower_index + 1


@dataclass(frozen=True, slots=True, eq=False)
class BandGapResult1D:
    """Retain internal and external gaps for one contiguous band selection."""

    spectrum: BandSpectrumSamples1D
    selection: ContiguousBandSelection
    internal_minimum_gap: ScalarQuantity | None
    external_minimum_gap: ScalarQuantity | None

    def __post_init__(self) -> None:
        """Validate selection bounds and gap units and availability."""
        if type(self.spectrum) is not BandSpectrumSamples1D:
            raise TypeError("spectrum must be BandSpectrumSamples1D")
        if type(self.selection) is not ContiguousBandSelection:
            raise TypeError("selection must be ContiguousBandSelection")
        if self.selection.upper_index >= self.spectrum.band_count:
            raise ValueError("selection must lie within retained bands")
        if self.selection.band_count == 1:
            if self.internal_minimum_gap is not None:
                raise ValueError("single-band selection has no internal gap")
        elif type(self.internal_minimum_gap) is not ScalarQuantity:
            raise TypeError("composite selection requires an internal gap")
        has_external_neighbor = (
            self.selection.lower_index > 0
            or self.selection.upper_index + 1 < self.spectrum.band_count
        )
        if (
            has_external_neighbor
            and type(self.external_minimum_gap) is not ScalarQuantity
        ):
            raise TypeError(
                "selection with an external neighbor requires an external gap"
            )
        if not has_external_neighbor and self.external_minimum_gap is not None:
            raise ValueError("selection without external neighbors has no external gap")
        for gap in (self.internal_minimum_gap, self.external_minimum_gap):
            if gap is not None and gap.unit != self.spectrum.eigenvalues.unit:
                raise ValueError("gap must use the spectrum energy unit")


class BandGapAnalyzer1D:
    """Measure internal and external direct gaps on one sampled path."""

    __slots__ = ()

    def execute(
        self,
        spectrum: BandSpectrumSamples1D,
        selection: ContiguousBandSelection,
    ) -> BandGapResult1D:
        """Return minimum adjacent gaps without applying an isolation threshold."""
        if type(spectrum) is not BandSpectrumSamples1D:
            raise TypeError("spectrum must be BandSpectrumSamples1D")
        if type(selection) is not ContiguousBandSelection:
            raise TypeError("selection must be ContiguousBandSelection")
        if selection.upper_index >= spectrum.band_count:
            raise ValueError("selection must lie within retained bands")
        values = spectrum.eigenvalues.magnitude
        internal: ScalarQuantity | None = None
        if selection.band_count > 1:
            internal_value = float(
                np.min(
                    values[
                        :,
                        selection.lower_index + 1 : selection.upper_index + 1,
                    ]
                    - values[
                        :,
                        selection.lower_index : selection.upper_index,
                    ]
                )
            )
            internal = ScalarQuantity(internal_value, spectrum.eigenvalues.unit)
        external_candidates: list[float] = []
        if selection.lower_index > 0:
            external_candidates.append(
                float(
                    np.min(
                        values[:, selection.lower_index]
                        - values[:, selection.lower_index - 1]
                    )
                )
            )
        if selection.upper_index + 1 < spectrum.band_count:
            external_candidates.append(
                float(
                    np.min(
                        values[:, selection.upper_index + 1]
                        - values[:, selection.upper_index]
                    )
                )
            )
        external = (
            ScalarQuantity(min(external_candidates), spectrum.eigenvalues.unit)
            if external_candidates
            else None
        )
        return BandGapResult1D(spectrum, selection, internal, external)


@dataclass(frozen=True, slots=True, eq=False)
class BandApproximationErrorResult1D:
    """Retain a maximum band-eigenvalue error on one reciprocal sample set."""

    target: BandSpectrumSamples1D
    candidate: ReciprocalOperatorSamples1D
    maximum_absolute_error: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate sample, matrix, and energy-unit correlations."""
        if type(self.target) is not BandSpectrumSamples1D:
            raise TypeError("target must be BandSpectrumSamples1D")
        if type(self.candidate) is not ReciprocalOperatorSamples1D:
            raise TypeError("candidate must be ReciprocalOperatorSamples1D")
        if self.candidate.matrix_dimension != self.target.band_count:
            raise ValueError("candidate dimension must equal target band count")
        if len(self.candidate.matrices) != self.target.sample_count:
            raise ValueError("candidate and target sample counts must agree")
        if type(self.maximum_absolute_error) is not ScalarQuantity:
            raise TypeError("maximum_absolute_error must be ScalarQuantity")
        if self.maximum_absolute_error.magnitude < 0.0:
            raise ValueError("maximum_absolute_error must be nonnegative")
        if self.maximum_absolute_error.unit != self.target.eigenvalues.unit:
            raise ValueError("maximum_absolute_error must use the target energy unit")


class BandApproximationErrorAnalyzer1D:
    """Compare represented Hermitian eigenvalues with sampled target bands."""

    __slots__ = ()

    def execute(
        self,
        target: BandSpectrumSamples1D,
        candidate: ReciprocalOperatorSamples1D,
        coordinate_absolute_tolerance: float,
    ) -> BandApproximationErrorResult1D:
        """Return the maximum ordered eigenvalue error without pooling sample sets."""
        if type(target) is not BandSpectrumSamples1D:
            raise TypeError("target must be BandSpectrumSamples1D")
        if type(candidate) is not ReciprocalOperatorSamples1D:
            raise TypeError("candidate must be ReciprocalOperatorSamples1D")
        if type(coordinate_absolute_tolerance) is not float:
            raise TypeError("coordinate_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(coordinate_absolute_tolerance)
            or coordinate_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "coordinate_absolute_tolerance must be finite and nonnegative"
            )
        if candidate.matrix_dimension != target.band_count:
            raise ValueError("candidate dimension must equal target band count")
        coordinates = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            candidate.coordinates, target.reciprocal_period.unit
        )
        if coordinates.magnitude.shape != target.coordinates.magnitude.shape:
            raise ValueError("candidate and target sample counts must agree")
        if (
            float(np.max(np.abs(coordinates.magnitude - target.coordinates.magnitude)))
            > coordinate_absolute_tolerance
        ):
            raise ValueError("candidate and target coordinates do not agree")
        candidate_unit = candidate.matrices[0].unit
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            candidate_unit, target.eigenvalues.unit
        ):
            raise ValueError("candidate and target energy units must be compatible")
        factor = MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
            candidate_unit, target.eigenvalues.unit
        )
        values = np.asarray(
            [
                np.linalg.eigvalsh(matrix.magnitude) * factor
                for matrix in candidate.matrices
            ],
            dtype=np.float64,
        )
        error = float(np.max(np.abs(values - target.eigenvalues.magnitude)))
        return BandApproximationErrorResult1D(
            target,
            candidate,
            ScalarQuantity(error, target.eigenvalues.unit),
        )
