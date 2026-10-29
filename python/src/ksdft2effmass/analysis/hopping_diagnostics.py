"""Hermiticity diagnostics for one-dimensional matrix-valued hoppings."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import (
    ModelSystemUnitConverter,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.solidstate import (
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    BlockHoppingTruncationResult1D,
    ReciprocalOperatorFourierTransformResult1D,
)


@dataclass(frozen=True, slots=True, eq=False)
class BlockHoppingHermiticityResult1D:
    """Retain ``T[-R] = T[R]^dagger`` coverage and maximum block defect."""

    model: BlockHoppingModel1D
    representative_modulus: int | None
    paired_representatives: tuple[int, ...]
    missing_opposite_representatives: tuple[int, ...]
    maximum_frobenius_defect: ScalarQuantity
    absolute_tolerance: ScalarQuantity
    passes: bool

    def __post_init__(self) -> None:
        """Validate pairing inventories, tolerance units, and pass disposition."""
        if type(self.model) is not BlockHoppingModel1D:
            raise TypeError("model must be BlockHoppingModel1D")
        if self.representative_modulus is not None:
            if type(self.representative_modulus) is not int:
                raise TypeError("representative_modulus must be a built-in int or None")
            if self.representative_modulus <= 0:
                raise ValueError("representative_modulus must be positive")
        for name, values in (
            ("paired_representatives", self.paired_representatives),
            (
                "missing_opposite_representatives",
                self.missing_opposite_representatives,
            ),
        ):
            if not isinstance(values, tuple) or any(
                type(value) is not int for value in values
            ):
                raise TypeError(f"{name} must be a tuple of built-in integers")
            if tuple(sorted(set(values))) != values:
                raise ValueError(f"{name} must be unique and strictly increasing")
        represented = set(self.model.representatives)
        if (
            set(self.paired_representatives)
            | set(self.missing_opposite_representatives)
            != represented
        ):
            raise ValueError("pairing inventories must partition model representatives")
        if set(self.paired_representatives) & set(
            self.missing_opposite_representatives
        ):
            raise ValueError("paired and missing inventories must be disjoint")
        for name, value in (
            ("maximum_frobenius_defect", self.maximum_frobenius_defect),
            ("absolute_tolerance", self.absolute_tolerance),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.unit != self.model.hopping_blocks[0].unit:
                raise ValueError(f"{name} must use the hopping-block unit")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = (
            not self.missing_opposite_representatives
            and self.maximum_frobenius_defect.magnitude
            <= self.absolute_tolerance.magnitude
        )
        if self.passes is not expected:
            raise ValueError("passes must match coverage, defect, and tolerance")


@dataclass(frozen=True, slots=True, eq=False)
class HoppingParsevalResult1D:
    """Retain the complete-mesh Parseval identity for one hopping truncation."""

    transform: ReciprocalOperatorFourierTransformResult1D
    truncation: BlockHoppingTruncationResult1D
    training_squared_frobenius_residual: ScalarQuantity
    expected_squared_frobenius_residual: ScalarQuantity
    parseval_absolute_residual: ScalarQuantity
    absolute_tolerance: ScalarQuantity
    passes: bool

    def __post_init__(self) -> None:
        """Validate squared-energy units, represented values, and disposition."""
        if type(self.transform) is not ReciprocalOperatorFourierTransformResult1D:
            raise TypeError(
                "transform must be ReciprocalOperatorFourierTransformResult1D"
            )
        if type(self.truncation) is not BlockHoppingTruncationResult1D:
            raise TypeError("truncation must be BlockHoppingTruncationResult1D")
        block_unit = self.transform.hopping_model.hopping_blocks[0].unit
        squared_unit = (
            Unitless()
            if isinstance(block_unit, Unitless)
            else PhysicalUnit(f"({block_unit.expression}) ** 2")
        )
        for name, value in (
            (
                "training_squared_frobenius_residual",
                self.training_squared_frobenius_residual,
            ),
            (
                "expected_squared_frobenius_residual",
                self.expected_squared_frobenius_residual,
            ),
            ("parseval_absolute_residual", self.parseval_absolute_residual),
            ("absolute_tolerance", self.absolute_tolerance),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.unit != squared_unit:
                raise ValueError(f"{name} must use the squared hopping-block unit")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected_passes = (
            self.parseval_absolute_residual.magnitude
            <= self.absolute_tolerance.magnitude
        )
        if self.passes is not expected_passes:
            raise ValueError("passes must match residual and tolerance")
        expected_residual = abs(
            self.training_squared_frobenius_residual.magnitude
            - self.expected_squared_frobenius_residual.magnitude
        )
        if self.parseval_absolute_residual.magnitude != expected_residual:
            raise ValueError("parseval_absolute_residual must match retained norms")


@dataclass(frozen=True, slots=True, eq=False)
class HoppingParsevalRequest1D:
    """Bind one complete transform, truncation, and squared-norm tolerance."""

    transform: ReciprocalOperatorFourierTransformResult1D
    truncation: BlockHoppingTruncationResult1D
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Admit exact transform, truncation, source, and tolerance correlations."""
        if type(self.transform) is not ReciprocalOperatorFourierTransformResult1D:
            raise TypeError(
                "transform must be ReciprocalOperatorFourierTransformResult1D"
            )
        if type(self.truncation) is not BlockHoppingTruncationResult1D:
            raise TypeError("truncation must be BlockHoppingTruncationResult1D")
        if (
            self.transform.hopping_model.representatives
            != self.truncation.source.representatives
        ):
            raise ValueError("truncation source must match transformed hopping model")
        for transformed, truncated_source in zip(
            self.transform.hopping_model.hopping_blocks,
            self.truncation.source.hopping_blocks,
            strict=True,
        ):
            if transformed.unit != truncated_source.unit or not np.array_equal(
                transformed.magnitude, truncated_source.magnitude
            ):
                raise ValueError(
                    "truncation source must match transformed hopping model"
                )
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")
        block_unit = self.transform.hopping_model.hopping_blocks[0].unit
        squared_unit = (
            Unitless()
            if isinstance(block_unit, Unitless)
            else PhysicalUnit(f"({block_unit.expression}) ** 2")
        )
        if not ModelSystemUnitConverter.compatible(
            self.absolute_tolerance.unit, squared_unit
        ):
            raise ValueError("tolerance must have squared hopping-block dimensions")


class HoppingParsevalAnalyzer1D:
    """Check Parseval scaling for one constructor-bound hopping truncation."""

    __slots__ = ("_request",)

    def __init__(self, request: HoppingParsevalRequest1D) -> None:
        if type(request) is not HoppingParsevalRequest1D:
            raise TypeError("request must be HoppingParsevalRequest1D")
        self._request = request

    @property
    def request(self) -> HoppingParsevalRequest1D:
        """Return the complete immutable Parseval-analysis request."""
        return self._request

    def execute(self) -> HoppingParsevalResult1D:
        """Compare training residual squared with scaled omitted-block norm."""
        transform = self.request.transform
        truncation = self.request.truncation
        block_unit = transform.hopping_model.hopping_blocks[0].unit
        squared_unit = (
            Unitless()
            if isinstance(block_unit, Unitless)
            else PhysicalUnit(f"({block_unit.expression}) ** 2")
        )
        tolerance = ModelSystemUnitConverter.convert_scalar(
            self.request.absolute_tolerance, squared_unit
        )
        reconstructed = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(
                truncation.truncated, transform.source.coordinates
            )
        ).execute()
        training_squared = float(
            sum(
                np.linalg.norm(candidate.magnitude - reference.magnitude) ** 2
                for candidate, reference in zip(
                    reconstructed.matrices,
                    transform.source.matrices,
                    strict=True,
                )
            )
        )
        expected_squared = float(
            transform.mesh.point_count * truncation.omitted_block_l2_norm**2
        )
        residual = abs(training_squared - expected_squared)
        return HoppingParsevalResult1D(
            transform,
            truncation,
            ScalarQuantity(training_squared, squared_unit),
            ScalarQuantity(expected_squared, squared_unit),
            ScalarQuantity(residual, squared_unit),
            tolerance,
            residual <= tolerance.magnitude,
        )


@dataclass(frozen=True, slots=True, eq=False)
class ScalarHoppingBandShapeResult1D:
    """Retain scalar hopping bandwidth and reduced-coordinate center curvature."""

    model: BlockHoppingModel1D
    comparison_coordinates: VectorQuantity
    bandwidth: ScalarQuantity
    zone_center_curvature: ScalarQuantity
    maximum_imaginary_residual: ScalarQuantity
    imaginary_absolute_tolerance: ScalarQuantity
    passes: bool

    def __post_init__(self) -> None:
        """Validate scalar-model units, nonnegative diagnostics, and disposition."""
        if type(self.model) is not BlockHoppingModel1D:
            raise TypeError("model must be BlockHoppingModel1D")
        if self.model.matrix_dimension != 1:
            raise ValueError("band-shape diagnostics require scalar hopping blocks")
        if type(self.comparison_coordinates) is not VectorQuantity:
            raise TypeError("comparison_coordinates must be VectorQuantity")
        if self.comparison_coordinates.magnitude.size == 0:
            raise ValueError("comparison_coordinates must be nonempty")
        unit = self.model.hopping_blocks[0].unit
        for name, value in (
            ("bandwidth", self.bandwidth),
            ("zone_center_curvature", self.zone_center_curvature),
            ("maximum_imaginary_residual", self.maximum_imaginary_residual),
            ("imaginary_absolute_tolerance", self.imaginary_absolute_tolerance),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.unit != unit:
                raise ValueError(f"{name} must use the hopping-block unit")
        if self.bandwidth.magnitude < 0.0:
            raise ValueError("bandwidth must be nonnegative")
        if self.maximum_imaginary_residual.magnitude < 0.0:
            raise ValueError("maximum_imaginary_residual must be nonnegative")
        if self.imaginary_absolute_tolerance.magnitude < 0.0:
            raise ValueError("imaginary_absolute_tolerance must be nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = (
            self.maximum_imaginary_residual.magnitude
            <= self.imaginary_absolute_tolerance.magnitude
        )
        if self.passes is not expected:
            raise ValueError("passes must match imaginary residual and tolerance")


@dataclass(frozen=True, slots=True, eq=False)
class ScalarHoppingBandShapeRequest1D:
    """Bind one scalar hopping model, comparison inventory, and tolerance."""

    model: BlockHoppingModel1D
    comparison_coordinates: VectorQuantity
    imaginary_absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Admit scalar rank, reciprocal coordinates, and energy tolerance."""
        if type(self.model) is not BlockHoppingModel1D:
            raise TypeError("model must be BlockHoppingModel1D")
        if self.model.matrix_dimension != 1:
            raise ValueError("band-shape diagnostics require scalar hopping blocks")
        if type(self.comparison_coordinates) is not VectorQuantity:
            raise TypeError("comparison_coordinates must be VectorQuantity")
        if self.comparison_coordinates.magnitude.size == 0:
            raise ValueError("comparison_coordinates must be nonempty")
        if type(self.imaginary_absolute_tolerance) is not ScalarQuantity:
            raise TypeError("imaginary_absolute_tolerance must be ScalarQuantity")
        if self.imaginary_absolute_tolerance.magnitude < 0.0:
            raise ValueError("imaginary_absolute_tolerance must be nonnegative")
        if not ModelSystemUnitConverter.compatible(
            self.imaginary_absolute_tolerance.unit,
            self.model.hopping_blocks[0].unit,
        ):
            raise ValueError("imaginary tolerance and hopping units must be compatible")


class ScalarHoppingBandShapeAnalyzer1D:
    """Evaluate one constructor-bound scalar hopping band shape."""

    __slots__ = ("_request",)

    def __init__(self, request: ScalarHoppingBandShapeRequest1D) -> None:
        if type(request) is not ScalarHoppingBandShapeRequest1D:
            raise TypeError("request must be ScalarHoppingBandShapeRequest1D")
        self._request = request

    @property
    def request(self) -> ScalarHoppingBandShapeRequest1D:
        """Return the complete immutable band-shape request."""
        return self._request

    def execute(self) -> ScalarHoppingBandShapeResult1D:
        """Evaluate bandwidth and analytical second derivative at zone center."""
        model = self.request.model
        comparison_coordinates = self.request.comparison_coordinates
        unit = model.hopping_blocks[0].unit
        tolerance = ModelSystemUnitConverter.convert_scalar(
            self.request.imaginary_absolute_tolerance, unit
        )
        samples = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(model, comparison_coordinates)
        ).execute()
        values = np.asarray(
            [matrix.magnitude[0, 0] for matrix in samples.matrices],
            dtype=np.complex128,
        )
        curvature = 0.0 + 0.0j
        for representative, block in zip(
            model.representatives, model.hopping_blocks, strict=True
        ):
            curvature += (
                -((2.0 * np.pi * float(representative)) ** 2) * block.magnitude[0, 0]
            )
        maximum_imaginary = max(
            float(np.max(np.abs(values.imag))), abs(float(curvature.imag))
        )
        return ScalarHoppingBandShapeResult1D(
            model,
            comparison_coordinates,
            ScalarQuantity(float(np.ptp(values.real)), unit),
            ScalarQuantity(float(curvature.real), unit),
            ScalarQuantity(maximum_imaginary, unit),
            tolerance,
            maximum_imaginary <= tolerance.magnitude,
        )


@dataclass(frozen=True, slots=True, eq=False)
class BlockHoppingHermiticityRequest1D:
    """Bind one hopping model, energy tolerance, and representative modulus."""

    model: BlockHoppingModel1D
    absolute_tolerance: ScalarQuantity
    representative_modulus: int | None

    def __post_init__(self) -> None:
        """Admit model, tolerance, and optional modular representative inventory."""
        if type(self.model) is not BlockHoppingModel1D:
            raise TypeError("model must be BlockHoppingModel1D")
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")
        if not ModelSystemUnitConverter.compatible(
            self.absolute_tolerance.unit, self.model.hopping_blocks[0].unit
        ):
            raise ValueError("tolerance and hopping-block units must be compatible")
        if self.representative_modulus is not None:
            if type(self.representative_modulus) is not int:
                raise TypeError("representative_modulus must be a built-in int or None")
            if self.representative_modulus <= 0:
                raise ValueError("representative_modulus must be positive")
            residues = tuple(
                representative % self.representative_modulus
                for representative in self.model.representatives
            )
            if len(set(residues)) != len(residues):
                raise ValueError(
                    "model representatives must be unique modulo the declared modulus"
                )


class BlockHoppingHermiticityAnalyzer1D:
    """Analyze conjugacy for one constructor-bound block-hopping model."""

    __slots__ = ("_request",)

    def __init__(self, request: BlockHoppingHermiticityRequest1D) -> None:
        if type(request) is not BlockHoppingHermiticityRequest1D:
            raise TypeError("request must be BlockHoppingHermiticityRequest1D")
        self._request = request

    @property
    def request(self) -> BlockHoppingHermiticityRequest1D:
        """Return the complete immutable Hermiticity-analysis request."""
        return self._request

    def execute(self) -> BlockHoppingHermiticityResult1D:
        """Compare every represented block with its exact or modular opposite."""
        model = self.request.model
        representative_modulus = self.request.representative_modulus
        tolerance = ModelSystemUnitConverter.convert_scalar(
            self.request.absolute_tolerance, model.hopping_blocks[0].unit
        )
        lookup = {
            representative: index
            for index, representative in enumerate(model.representatives)
        }
        paired: list[int] = []
        missing: list[int] = []
        defects: list[float] = []
        for representative, block in zip(
            model.representatives, model.hopping_blocks, strict=True
        ):
            opposite: int | None = None
            if -representative in lookup:
                opposite = -representative
            elif representative_modulus is not None:
                candidates = tuple(
                    value
                    for value in model.representatives
                    if (value + representative) % representative_modulus == 0
                )
                if len(candidates) == 1:
                    opposite = candidates[0]
            if opposite is None:
                missing.append(representative)
                continue
            paired.append(representative)
            opposite_block = model.hopping_blocks[lookup[opposite]]
            defects.append(
                float(
                    np.linalg.norm(block.magnitude - opposite_block.magnitude.conj().T)
                )
            )
        maximum = max(defects, default=0.0)
        return BlockHoppingHermiticityResult1D(
            model,
            representative_modulus,
            tuple(sorted(paired)),
            tuple(sorted(missing)),
            ScalarQuantity(maximum, model.hopping_blocks[0].unit),
            tolerance,
            not missing and maximum <= tolerance.magnitude,
        )
