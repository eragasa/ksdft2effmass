r"""Site-diagonal bridges between supported boundary-twist gauges."""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from enum import StrEnum

import numpy as np
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import ComplexSparseMatrixQuantity, Unitless

from .boundary_phases import TwistFiber, TwistGaugeRepresentation
from .geometry import FiniteLatticeCoordinateResolver, FiniteLatticeShape
from .represented_operators import ScalarFiniteLatticeOperator


class TwistGaugeBridgeConvention(StrEnum):
    """Supported direction convention for site-diagonal gauge bridges."""

    TARGET_EQUALS_U_SOURCE_U_DAGGER = "target_equals_u_source_u_dagger"


@dataclass(frozen=True, slots=True)
class TwistGaugeBridgeResult:
    """Record a site-diagonal transformation between two twist gauges.

    Parameters
    ----------
    shape
        Finite shape defining the site basis and last-axis-fastest ordering.
    source_fiber
        Centered-uniform-link fiber, including its unreduced lift.
    target_fiber
        Quotient-seam fiber with the same retained twist reduction.
    transformation
        Unitless canonical complex CSR matrix ``U``.
    convention
        Exact relation ``H_target = U H_source U^dagger``.

    Notes
    -----
    Construction does not compare source and target operators. Gauge-equivalence
    residual analysis remains a separate ActionObject.
    """

    shape: FiniteLatticeShape
    source_fiber: TwistFiber
    target_fiber: TwistFiber
    transformation: ComplexSparseMatrixQuantity
    convention: TwistGaugeBridgeConvention

    def __post_init__(self) -> None:
        """Validate correlated dimensions, fibers, storage, and convention."""
        if type(self.shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(self.source_fiber) is not TwistFiber:
            raise TypeError("source_fiber must be TwistFiber")
        if type(self.target_fiber) is not TwistFiber:
            raise TypeError("target_fiber must be TwistFiber")
        if type(self.transformation) is not ComplexSparseMatrixQuantity:
            raise TypeError("transformation must be ComplexSparseMatrixQuantity")
        if type(self.convention) is not TwistGaugeBridgeConvention:
            raise TypeError("convention must be TwistGaugeBridgeConvention")
        if self.source_fiber.dimension is not self.shape.dimension:
            raise ValueError("source fiber and shape dimensions must agree")
        if self.target_fiber.dimension is not self.shape.dimension:
            raise ValueError("target fiber and shape dimensions must agree")
        if self.source_fiber.reduction != self.target_fiber.reduction:
            raise ValueError("source and target fibers must share one twist reduction")
        if (
            self.source_fiber.gauge
            is not TwistGaugeRepresentation.CENTERED_UNIFORM_LINK
        ):
            raise ValueError("source fiber must use centered uniform-link gauge")
        if self.target_fiber.gauge is not TwistGaugeRepresentation.QUOTIENT_SEAM:
            raise ValueError("target fiber must use quotient-seam gauge")
        expected_shape = (self.shape.cell_count, self.shape.cell_count)
        if self.transformation.shape != expected_shape:
            raise ValueError(
                "transformation shape must equal finite-lattice cell count"
            )
        if type(self.transformation.unit) is not Unitless:
            raise ValueError("gauge transformation must be unitless")
        cell_count = self.shape.cell_count
        if (
            self.transformation.nonzero_count != cell_count
            or not np.array_equal(
                self.transformation.row_offsets,
                np.arange(cell_count + 1, dtype=np.int64),
            )
            or not np.array_equal(
                self.transformation.column_indices,
                np.arange(cell_count, dtype=np.int64),
            )
        ):
            raise ValueError(
                "gauge transformation must have one diagonal entry per site"
            )
        magnitude_tolerance = 8.0 * np.finfo(np.float64).eps
        if not np.allclose(
            np.abs(self.transformation.data),
            1.0,
            rtol=0.0,
            atol=magnitude_tolerance,
        ):
            raise ValueError("gauge transformation diagonal must have unit magnitude")


class TwistGaugeEquivalenceIssueCode(StrEnum):
    """Structured prerequisites that can block represented gauge comparison."""

    SHAPE = "shape"
    SOURCE_FIBER = "source_fiber"
    TARGET_FIBER = "target_fiber"
    BASIS = "basis"
    UNIT = "unit"
    ENERGY_REFERENCE = "energy_reference"


@dataclass(frozen=True, slots=True)
class TwistGaugeEquivalenceResult:
    """Record compatibility and a caller-toleranced gauge-equivalence residual."""

    source: ScalarFiniteLatticeOperator
    target: ScalarFiniteLatticeOperator
    bridge: TwistGaugeBridgeResult
    absolute_tolerance: float
    maximum_absolute_residual: float | None
    issue_codes: tuple[TwistGaugeEquivalenceIssueCode, ...]

    def __post_init__(self) -> None:
        """Validate exact retained inputs, scalar results, and issue ordering."""
        if type(self.source) is not ScalarFiniteLatticeOperator:
            raise TypeError("source must be ScalarFiniteLatticeOperator")
        if type(self.target) is not ScalarFiniteLatticeOperator:
            raise TypeError("target must be ScalarFiniteLatticeOperator")
        if type(self.bridge) is not TwistGaugeBridgeResult:
            raise TypeError("bridge must be TwistGaugeBridgeResult")
        if type(self.absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(self.absolute_tolerance) or self.absolute_tolerance < 0.0:
            raise ValueError("absolute_tolerance must be finite and nonnegative")
        if self.maximum_absolute_residual is not None:
            if type(self.maximum_absolute_residual) is not float:
                raise TypeError("maximum_absolute_residual must be float or None")
            if not math.isfinite(self.maximum_absolute_residual):
                raise ValueError("maximum_absolute_residual must be finite")
            if self.maximum_absolute_residual < 0.0:
                raise ValueError("maximum_absolute_residual must be nonnegative")
        if type(self.issue_codes) is not tuple or any(
            type(code) is not TwistGaugeEquivalenceIssueCode
            for code in self.issue_codes
        ):
            raise TypeError("issue_codes must contain TwistGaugeEquivalenceIssueCode")
        ordered = tuple(sorted(set(self.issue_codes), key=lambda code: code.value))
        if self.issue_codes != ordered:
            raise ValueError("issue_codes must be sorted and unique")
        if bool(self.issue_codes) == (self.maximum_absolute_residual is not None):
            raise ValueError("residual presence must agree with compatibility issues")

    @property
    def compatible(self) -> bool:
        """Return whether all represented comparison prerequisites agree."""
        return not self.issue_codes

    @property
    def is_equivalent(self) -> bool:
        """Return compatibility and inclusive residual acceptance."""
        return (
            self.maximum_absolute_residual is not None
            and self.maximum_absolute_residual <= self.absolute_tolerance
        )


class TwistGaugeBridgeConstructor:
    r"""Construct the site-diagonal bridge from uniform-link to quotient-seam gauge.

    For site coordinate ``r``, the diagonal phase is

    .. math::

       U_{rr}=\exp\!\left(2\pi i\sum_a r_a\phi_a/N_a\right),

    using the unreduced lift ``phi``. The returned convention is
    ``H_seam = U H_uniform U^dagger``.
    """

    __slots__ = ()

    def execute(
        self, shape: FiniteLatticeShape, source_fiber: TwistFiber
    ) -> TwistGaugeBridgeResult:
        """Return one canonical sparse diagonal bridge and target fiber."""
        if type(shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(source_fiber) is not TwistFiber:
            raise TypeError("source_fiber must be TwistFiber")
        if source_fiber.dimension is not shape.dimension:
            raise ValueError("source fiber and shape dimensions must agree")
        if source_fiber.gauge is not TwistGaugeRepresentation.CENTERED_UNIFORM_LINK:
            raise ValueError("source fiber must use centered uniform-link gauge")
        resolver = FiniteLatticeCoordinateResolver()
        phases: list[complex] = []
        for index in range(shape.cell_count):
            coordinate = resolver.execute(shape, index)
            phase_turns = math.fsum(
                float(coordinate.components[axis])
                * source_fiber.lift.turns[axis]
                / float(shape.extents[axis])
                for axis in range(shape.dimension.value)
            )
            phases.append(cmath.exp(2.0j * math.pi * phase_turns))
        transformation = ComplexSparseMatrixQuantity.from_csr(
            sparse.diags(
                np.asarray(phases, dtype=np.complex128), offsets=0, format="csr"
            ),
            Unitless(),
        )
        target_fiber = TwistFiber(
            source_fiber.reduction, TwistGaugeRepresentation.QUOTIENT_SEAM
        )
        return TwistGaugeBridgeResult(
            shape,
            source_fiber,
            target_fiber,
            transformation,
            TwistGaugeBridgeConvention.TARGET_EQUALS_U_SOURCE_U_DAGGER,
        )


class TwistGaugeEquivalenceAnalyzer:
    """Compare two compatible scalar operators through an explicit gauge bridge."""

    __slots__ = ()

    def execute(
        self,
        source: ScalarFiniteLatticeOperator,
        target: ScalarFiniteLatticeOperator,
        bridge: TwistGaugeBridgeResult,
        *,
        absolute_tolerance: float,
    ) -> TwistGaugeEquivalenceResult:
        """Return represented compatibility and a nondensifying maximum residual."""
        if type(source) is not ScalarFiniteLatticeOperator:
            raise TypeError("source must be ScalarFiniteLatticeOperator")
        if type(target) is not ScalarFiniteLatticeOperator:
            raise TypeError("target must be ScalarFiniteLatticeOperator")
        if type(bridge) is not TwistGaugeBridgeResult:
            raise TypeError("bridge must be TwistGaugeBridgeResult")
        if type(absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(absolute_tolerance) or absolute_tolerance < 0.0:
            raise ValueError("absolute_tolerance must be finite and nonnegative")
        issues: set[TwistGaugeEquivalenceIssueCode] = set()
        if source.shape != target.shape or source.shape != bridge.shape:
            issues.add(TwistGaugeEquivalenceIssueCode.SHAPE)
        if source.twist_fiber != bridge.source_fiber:
            issues.add(TwistGaugeEquivalenceIssueCode.SOURCE_FIBER)
        if target.twist_fiber != bridge.target_fiber:
            issues.add(TwistGaugeEquivalenceIssueCode.TARGET_FIBER)
        if source.basis_identifier != target.basis_identifier:
            issues.add(TwistGaugeEquivalenceIssueCode.BASIS)
        if source.matrix.unit != target.matrix.unit:
            issues.add(TwistGaugeEquivalenceIssueCode.UNIT)
        if source.energy_reference != target.energy_reference:
            issues.add(TwistGaugeEquivalenceIssueCode.ENERGY_REFERENCE)
        ordered = tuple(sorted(issues, key=lambda code: code.value))
        if ordered:
            return TwistGaugeEquivalenceResult(
                source, target, bridge, absolute_tolerance, None, ordered
            )
        unitary = bridge.transformation.to_csr()
        transformed = unitary @ source.matrix.to_csr() @ unitary.conjugate().transpose()
        residual = target.matrix.to_csr() - transformed
        residual.sum_duplicates()
        residual.eliminate_zeros()
        if residual.data.size == 0:
            maximum = 0.0
        else:
            magnitudes = np.abs(residual.data)
            if not np.all(np.isfinite(magnitudes)):
                raise ValueError("gauge-equivalence residual must remain finite")
            maximum = float(np.max(magnitudes))
        if not math.isfinite(maximum):
            raise ValueError("gauge-equivalence residual must remain finite")
        return TwistGaugeEquivalenceResult(
            source, target, bridge, absolute_tolerance, maximum, ()
        )
