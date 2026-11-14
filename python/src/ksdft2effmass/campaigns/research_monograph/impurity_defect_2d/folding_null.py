"""Typed contracts for folding and null-alignment controls.

This bounded synthetic numerical campaign evaluates scalar Hermitian hopping models on
declared two-dimensional finite periodic shapes, checks finite Bloch folding, and
recovers a planted null perturbation after an explicit translation, site-phase, and
energy-reference attack. It reads no accepted parent and authorizes no external
calculation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from projectkoios.physkit.units import Unitless

from ksdft2effmass.solidstate import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeDimension,
    QuotientSeamOperatorConstructor,
    ScalarHoppingModel,
)

type ComplexMatrix = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]
type IntegerComponents = tuple[int] | tuple[int, int] | tuple[int, int, int]
type FloatComponents = tuple[float] | tuple[float, float] | tuple[float, float, float]


def _integer_pair(value: IntegerComponents) -> tuple[int, int]:
    """Close one already validated two-dimensional integer tuple."""
    if len(value) != 2:
        raise AssertionError("two-dimensional integer components were lost")
    return value[0], value[1]


def _float_pair(value: FloatComponents) -> tuple[float, float]:
    """Close one already validated two-dimensional floating tuple."""
    if len(value) != 2:
        raise AssertionError("two-dimensional floating components were lost")
    return value[0], value[1]


@dataclass(frozen=True, slots=True)
class FoldingNullCase:
    """Retain one finite shape and unreduced boundary-twist lift."""

    identifier: str
    shape: FiniteLatticeShape
    twist: BoundaryTwistLift

    def __post_init__(self) -> None:
        """Validate exact two-dimensional case identity and representation."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(self.twist) is not BoundaryTwistLift:
            raise TypeError("twist must be BoundaryTwistLift")
        if self.shape.dimension is not LatticeDimension.TWO:
            raise ValueError("folding/null-control shapes must be two-dimensional")
        if self.twist.dimension is not LatticeDimension.TWO:
            raise ValueError("folding/null-control twists must be two-dimensional")


@dataclass(frozen=True, slots=True)
class FoldingNullAlignmentAttack:
    """Retain the known translation, site-phase, and energy-reference attack."""

    translation_cells: tuple[int, int]
    site_phase_steps_radians: tuple[float, float]
    energy_reference_shift: float

    def __post_init__(self) -> None:
        """Validate closed two-dimensional finite attack controls."""
        if (
            type(self.translation_cells) is not tuple
            or len(self.translation_cells) != 2
        ):
            raise TypeError("translation_cells must be a two-integer tuple")
        if any(type(value) is not int for value in self.translation_cells):
            raise TypeError("translation_cells must contain built-in integers")
        if (
            type(self.site_phase_steps_radians) is not tuple
            or len(self.site_phase_steps_radians) != 2
        ):
            raise TypeError("site_phase_steps_radians must be a two-float tuple")
        if any(type(value) is not float for value in self.site_phase_steps_radians):
            raise TypeError("site phase steps must contain built-in floats")
        if any(not math.isfinite(value) for value in self.site_phase_steps_radians):
            raise ValueError("site phase steps must be finite")
        if type(self.energy_reference_shift) is not float:
            raise TypeError("energy_reference_shift must be a built-in float")
        if not math.isfinite(self.energy_reference_shift):
            raise ValueError("energy_reference_shift must be finite")


@dataclass(frozen=True, slots=True)
class FoldingNullTolerances:
    """Retain prospective algebraic and folding-unitarity tolerances."""

    algebraic_absolute: float
    folding_unitarity: float

    def __post_init__(self) -> None:
        """Require finite nonnegative built-in-float tolerances."""
        for value, name in (
            (self.algebraic_absolute, "algebraic_absolute"),
            (self.folding_unitarity, "folding_unitarity"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class FoldingNullStudyDefinition:
    """Retain one complete authored folding/null-control definition."""

    identifier: str
    parent: ScalarHoppingModel
    cases: tuple[FoldingNullCase, ...]
    null_attack: FoldingNullAlignmentAttack
    tolerances: FoldingNullTolerances

    def __post_init__(self) -> None:
        """Validate identity, scalar parent, case inventory, and Hermiticity."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.parent) is not ScalarHoppingModel:
            raise TypeError("parent must be ScalarHoppingModel")
        if self.parent.dimension is not LatticeDimension.TWO:
            raise ValueError("folding/null-control parent must be two-dimensional")
        if type(self.parent.energy_unit) is not Unitless:
            raise ValueError(
                "folding/null-control synthetic parent must be dimensionless"
            )
        if type(self.cases) is not tuple or not self.cases:
            raise TypeError("cases must be a nonempty tuple")
        if any(type(case) is not FoldingNullCase for case in self.cases):
            raise TypeError("cases must contain FoldingNullCase values")
        identifiers = tuple(case.identifier for case in self.cases)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("folding/null-control case identifiers must be unique")
        structural_keys = tuple(
            (case.shape.extents, case.twist.turns) for case in self.cases
        )
        if len(set(structural_keys)) != len(structural_keys):
            raise ValueError("folding/null shape-twist cases must be unique")
        if type(self.null_attack) is not FoldingNullAlignmentAttack:
            raise TypeError("null_attack must be FoldingNullAlignmentAttack")
        if type(self.tolerances) is not FoldingNullTolerances:
            raise TypeError("tolerances must be FoldingNullTolerances")
        terms = {term.displacement.components: term.value for term in self.parent.terms}
        for displacement, value in terms.items():
            displacement_x, displacement_y = _integer_pair(displacement)
            reverse = (-displacement_x, -displacement_y)
            if reverse not in terms or terms[reverse] != value.conjugate():
                raise ValueError(
                    "folding/null-control parent hopping inventory must be Hermitian"
                )


@dataclass(frozen=True, slots=True)
class FoldingMetrics:
    """Retain finite Fourier folding and spectrum residuals for one case."""

    unitarity_maximum_absolute_defect: float
    hermiticity_maximum_absolute_defect: float
    off_diagonal_maximum_absolute: float
    primitive_energy_maximum_absolute_defect: float
    eigenvalue_maximum_absolute_defect: float

    def __post_init__(self) -> None:
        """Validate finite nonnegative binary64 metrics."""
        for value in (
            self.unitarity_maximum_absolute_defect,
            self.hermiticity_maximum_absolute_defect,
            self.off_diagonal_maximum_absolute,
            self.primitive_energy_maximum_absolute_defect,
            self.eigenvalue_maximum_absolute_defect,
        ):
            if type(value) is not float:
                raise TypeError("folding metrics must be built-in floats")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError("folding metrics must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class NullAlignmentMetrics:
    """Retain known-map null-extraction residuals for one case."""

    transform_unitarity_maximum_absolute_defect: float
    recovered_maximum_absolute_defect: float
    recovered_frobenius_defect: float

    def __post_init__(self) -> None:
        """Validate finite nonnegative binary64 metrics."""
        for value in (
            self.transform_unitarity_maximum_absolute_defect,
            self.recovered_maximum_absolute_defect,
            self.recovered_frobenius_defect,
        ):
            if type(value) is not float:
                raise TypeError("null-extraction metrics must be built-in floats")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(
                    "null-extraction metrics must be finite and nonnegative"
                )


@dataclass(frozen=True, slots=True)
class FoldingNullCaseResult:
    """Retain one definition-correlated folding/null numerical result."""

    case: FoldingNullCase
    folding: FoldingMetrics
    null_extraction: NullAlignmentMetrics

    def __post_init__(self) -> None:
        """Validate exact retained component types."""
        if type(self.case) is not FoldingNullCase:
            raise TypeError("case must be FoldingNullCase")
        if type(self.folding) is not FoldingMetrics:
            raise TypeError("folding must be FoldingMetrics")
        if type(self.null_extraction) is not NullAlignmentMetrics:
            raise TypeError("null_extraction must be NullAlignmentMetrics")


@dataclass(frozen=True, slots=True)
class FoldingNullResult:
    """Retain one complete folding/null-control result and criterion disposition."""

    definition: FoldingNullStudyDefinition
    cases: tuple[FoldingNullCaseResult, ...]
    failed_criteria: tuple[str, ...]

    def __post_init__(self) -> None:
        """Require exact case correlation and recomputed criterion failures."""
        if type(self.definition) is not FoldingNullStudyDefinition:
            raise TypeError("definition must be FoldingNullStudyDefinition")
        if type(self.cases) is not tuple or any(
            type(case) is not FoldingNullCaseResult for case in self.cases
        ):
            raise TypeError("cases must contain FoldingNullCaseResult values")
        if tuple(case.case for case in self.cases) != self.definition.cases:
            raise ValueError("result cases must match the definition exactly")
        if type(self.failed_criteria) is not tuple or any(
            type(value) is not str or not value for value in self.failed_criteria
        ):
            raise TypeError("failed_criteria must contain nonempty strings")
        expected = FoldingNullCriterionEvaluator().execute(
            self.cases, self.definition.tolerances
        )
        if self.failed_criteria != expected:
            raise ValueError("failed_criteria must match the retained metrics")

    @property
    def passes(self) -> bool:
        """Return whether every retained prospective criterion passes."""
        return not self.failed_criteria


class FoldingNullCriterionEvaluator:
    """Evaluate criteria without discarding failed folding/null metrics."""

    __slots__ = ()

    def execute(
        self,
        cases: tuple[FoldingNullCaseResult, ...],
        tolerances: FoldingNullTolerances,
    ) -> tuple[str, ...]:
        """Return ordered names of every criterion exceeding its tolerance."""
        if type(cases) is not tuple or any(
            type(case) is not FoldingNullCaseResult for case in cases
        ):
            raise TypeError("cases must contain FoldingNullCaseResult values")
        if type(tolerances) is not FoldingNullTolerances:
            raise TypeError("tolerances must be FoldingNullTolerances")
        failures: list[str] = []
        for case in cases:
            folding = case.folding
            null = case.null_extraction
            criteria = (
                (
                    "folding.unitarity_maximum_absolute_defect",
                    folding.unitarity_maximum_absolute_defect,
                    tolerances.folding_unitarity,
                ),
                (
                    "folding.hermiticity_maximum_absolute_defect",
                    folding.hermiticity_maximum_absolute_defect,
                    tolerances.algebraic_absolute,
                ),
                (
                    "folding.off_diagonal_maximum_absolute",
                    folding.off_diagonal_maximum_absolute,
                    tolerances.algebraic_absolute,
                ),
                (
                    "folding.primitive_energy_maximum_absolute_defect",
                    folding.primitive_energy_maximum_absolute_defect,
                    tolerances.algebraic_absolute,
                ),
                (
                    "folding.eigenvalue_maximum_absolute_defect",
                    folding.eigenvalue_maximum_absolute_defect,
                    tolerances.algebraic_absolute,
                ),
                (
                    "null.transform_unitarity_maximum_absolute_defect",
                    null.transform_unitarity_maximum_absolute_defect,
                    tolerances.algebraic_absolute,
                ),
                (
                    "null.recovered_maximum_absolute_defect",
                    null.recovered_maximum_absolute_defect,
                    tolerances.algebraic_absolute,
                ),
                (
                    "null.recovered_frobenius_defect",
                    null.recovered_frobenius_defect,
                    tolerances.algebraic_absolute,
                ),
            )
            failures.extend(
                f"{case.case.identifier}.{name}"
                for name, value, tolerance in criteria
                if value > tolerance
            )
        return tuple(failures)


class FoldingNullCalculator:
    """Calculate folding/null controls through public seam construction."""

    __slots__ = ()

    def execute(self, definition: FoldingNullStudyDefinition) -> FoldingNullResult:
        """Return finite folding and known-map null-extraction diagnostics."""
        if type(definition) is not FoldingNullStudyDefinition:
            raise TypeError("definition must be FoldingNullStudyDefinition")
        results: list[FoldingNullCaseResult] = []
        constructor = QuotientSeamOperatorConstructor()
        for case in definition.cases:
            represented = constructor.execute_hopping(
                f"{case.identifier}.parent",
                definition.parent,
                case.shape,
                case.twist,
            )
            hamiltonian = np.asarray(
                represented.matrix.to_csr().toarray(), dtype=np.complex128
            )
            folding = self._folding(case)
            expected = self._primitive_energies(case, definition.parent)
            transformed = folding.conjugate().transpose() @ hamiltonian @ folding
            diagonal = np.diag(np.diag(transformed))
            expected_diagonal = np.diag(expected)
            null = self._null_metrics(case, hamiltonian, definition.null_attack)
            results.append(
                FoldingNullCaseResult(
                    case=case,
                    folding=FoldingMetrics(
                        unitarity_maximum_absolute_defect=self._maximum_absolute(
                            folding.conjugate().transpose() @ folding
                            - np.eye(case.shape.cell_count, dtype=np.complex128)
                        ),
                        hermiticity_maximum_absolute_defect=self._maximum_absolute(
                            hamiltonian - hamiltonian.conjugate().transpose()
                        ),
                        off_diagonal_maximum_absolute=self._maximum_absolute(
                            transformed - diagonal
                        ),
                        primitive_energy_maximum_absolute_defect=(
                            self._maximum_absolute(transformed - expected_diagonal)
                        ),
                        eigenvalue_maximum_absolute_defect=float(
                            np.max(
                                np.abs(
                                    np.sort(np.linalg.eigvalsh(hamiltonian))
                                    - np.sort(expected)
                                )
                            )
                        ),
                    ),
                    null_extraction=null,
                )
            )
        closed = tuple(results)
        failures = FoldingNullCriterionEvaluator().execute(
            closed, definition.tolerances
        )
        return FoldingNullResult(definition, closed, failures)

    @staticmethod
    def _folding(case: FoldingNullCase) -> ComplexMatrix:
        """Construct the dense finite Bloch folding matrix explicitly."""
        nx, ny = _integer_pair(case.shape.extents)
        phi_x, phi_y = _float_pair(case.twist.turns)
        dimension = case.shape.cell_count
        result = np.empty((dimension, dimension), dtype=np.complex128)
        scale = 1.0 / math.sqrt(float(dimension))
        for x in range(nx):
            for y in range(ny):
                row = x * ny + y
                for jx in range(nx):
                    kx = (float(jx) + phi_x) / float(nx)
                    for jy in range(ny):
                        ky = (float(jy) + phi_y) / float(ny)
                        column = jx * ny + jy
                        result[row, column] = scale * np.exp(
                            2.0j * np.pi * (kx * float(x) + ky * float(y))
                        )
        return result

    @staticmethod
    def _primitive_energies(
        case: FoldingNullCase, parent: ScalarHoppingModel
    ) -> RealVector:
        """Evaluate the scalar primitive Bloch energy at every folded momentum."""
        nx, ny = _integer_pair(case.shape.extents)
        phi_x, phi_y = _float_pair(case.twist.turns)
        energies = np.empty(case.shape.cell_count, dtype=np.float64)
        for jx in range(nx):
            kx = (float(jx) + phi_x) / float(nx)
            for jy in range(ny):
                ky = (float(jy) + phi_y) / float(ny)
                value = sum(
                    term.value
                    * np.exp(
                        2.0j
                        * np.pi
                        * (
                            kx * float(_integer_pair(term.displacement.components)[0])
                            + ky * float(_integer_pair(term.displacement.components)[1])
                        )
                    )
                    for term in parent.terms
                )
                if abs(value.imag) > 1.0e-11:
                    raise ValueError("primitive energy must remain real")
                energies[jx * ny + jy] = value.real
        return energies

    @classmethod
    def _null_metrics(
        cls,
        case: FoldingNullCase,
        pristine: ComplexMatrix,
        attack: FoldingNullAlignmentAttack,
    ) -> NullAlignmentMetrics:
        """Apply and exactly invert the known null-alignment attack."""
        nx, ny = _integer_pair(case.shape.extents)
        translation_x, translation_y = attack.translation_cells
        phase_step_x, phase_step_y = attack.site_phase_steps_radians
        dimension = case.shape.cell_count
        transform = np.zeros((dimension, dimension), dtype=np.complex128)
        for x in range(nx):
            for y in range(ny):
                source = x * ny + y
                target_x = (x + translation_x) % nx
                target_y = (y + translation_y) % ny
                target = target_x * ny + target_y
                transform[target, source] = np.exp(
                    1.0j * (phase_step_x * float(x) + phase_step_y * float(y))
                )
        identity = np.eye(dimension, dtype=np.complex128)
        attacked = (
            transform @ pristine @ transform.conjugate().transpose()
            + attack.energy_reference_shift * identity
        )
        recovered = (
            transform.conjugate().transpose()
            @ (attacked - attack.energy_reference_shift * identity)
            @ transform
            - pristine
        )
        return NullAlignmentMetrics(
            transform_unitarity_maximum_absolute_defect=cls._maximum_absolute(
                transform.conjugate().transpose() @ transform - identity
            ),
            recovered_maximum_absolute_defect=cls._maximum_absolute(recovered),
            recovered_frobenius_defect=float(np.linalg.norm(recovered, ord="fro")),
        )

    @staticmethod
    def _maximum_absolute(value: ComplexMatrix) -> float:
        """Return the finite maximum absolute matrix entry."""
        return float(np.max(np.abs(value), initial=0.0))
