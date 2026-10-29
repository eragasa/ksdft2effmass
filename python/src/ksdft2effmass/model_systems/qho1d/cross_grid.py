"""Typed adjacent-grid diagnostics for direct QHO1D calculation results."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Self, cast

import numpy as np
from projectkoios.physkit.linalg.matrix.norm import FrobeniusMatrixNorm
from projectkoios.physkit.units import MatrixQuantity, ScalarQuantity, Unitless

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue
from ksdft2effmass.verification import (
    CompositeVerification,
    MaximumAbsoluteErrorComparison,
)

from .configuration import Qho1dConfiguration
from .result import Qho1dCalculationResult, Qho1dCaseResult


class _Qho1dCaseInventory:
    """Index one calculation's unique cases by their authored sweep keys."""

    __slots__ = ("_cases",)

    def __init__(self, result: Qho1dCalculationResult) -> None:
        cases = {case.key: case for case in result.cases}
        if len(cases) != len(result.cases):
            raise ValueError("result cases must have unique authored sweep keys")
        self._cases = MappingProxyType(cases)

    def required(self, key: tuple[float, float, int]) -> Qho1dCaseResult:
        """Return one required configured case or fail closed."""
        try:
            return self._cases[key]
        except KeyError as error:
            raise ValueError(f"configured QHO1D case is absent: {key}") from error


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dCrossGridComparisonResult(BaseTypedRecord):
    """Retain one adjacent-grid difference in common retained coordinates.

    Parameters
    ----------
    box_half_width
        Shared finite-domain half-width.
    retained_dimension
        Shared retained number-state dimension.
    coarse_requested_grid_spacing, fine_requested_grid_spacing
        Adjacent authored grid controls in strictly decreasing order.
    coarse_grid_spacing, fine_grid_spacing
        Corresponding realized finite-grid spacings.
    coarse_interior_points, fine_interior_points
        Corresponding represented spatial dimensions.
    coarse_minus_fine_frobenius
        Frobenius norm of the coarse pulled-back Hamiltonian minus the fine
        pulled-back Hamiltonian in the shared retained number-state coordinates.

    Raises
    ------
    TypeError
        A quantity or integer has the wrong semantic type.
    ValueError
        Units, positivity, grid ordering, or represented dimensions are invalid.

    Notes
    -----
    This result compares finite matrix representations only after both have been
    pulled into the same ordered retained number-state coordinates. It is not a
    continuum-convergence estimate or physical uncertainty.
    """

    box_half_width: ScalarQuantity
    retained_dimension: int
    coarse_requested_grid_spacing: ScalarQuantity
    fine_requested_grid_spacing: ScalarQuantity
    coarse_grid_spacing: ScalarQuantity
    fine_grid_spacing: ScalarQuantity
    coarse_interior_points: int
    fine_interior_points: int
    coarse_minus_fine_frobenius: ScalarQuantity

    def __post_init__(self) -> None:
        quantity_names = (
            "box_half_width",
            "coarse_requested_grid_spacing",
            "fine_requested_grid_spacing",
            "coarse_grid_spacing",
            "fine_grid_spacing",
            "coarse_minus_fine_frobenius",
        )
        for name in quantity_names:
            value = getattr(self, name)
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            if not isinstance(value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if not np.isfinite(value.magnitude):
                raise ValueError(f"{name} must be finite")
        for name in (
            "box_half_width",
            "coarse_requested_grid_spacing",
            "fine_requested_grid_spacing",
            "coarse_grid_spacing",
            "fine_grid_spacing",
        ):
            if getattr(self, name).magnitude <= 0.0:
                raise ValueError(f"{name} must be positive")
        if self.coarse_minus_fine_frobenius.magnitude < 0.0:
            raise ValueError("coarse_minus_fine_frobenius must be nonnegative")
        for name in (
            "retained_dimension",
            "coarse_interior_points",
            "fine_interior_points",
        ):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if (
            self.coarse_requested_grid_spacing.magnitude
            <= self.fine_requested_grid_spacing.magnitude
        ):
            raise ValueError("requested grid spacings must define coarse then fine")
        if self.coarse_grid_spacing.magnitude <= self.fine_grid_spacing.magnitude:
            raise ValueError("realized grid spacings must define coarse then fine")
        if self.coarse_interior_points >= self.fine_interior_points:
            raise ValueError("interior-point counts must define coarse then fine")
        if self.retained_dimension > self.coarse_interior_points:
            raise ValueError("retained dimension exceeds the coarse spatial dimension")

    @property
    def key(self) -> tuple[float, int, float, float]:
        """Return the authored adjacent-grid comparison key.

        Returns
        -------
        tuple[float, int, float, float]
            Box half-width, retained dimension, coarse requested spacing, and fine
            requested spacing.
        """
        return (
            self.box_half_width.magnitude,
            self.retained_dimension,
            self.coarse_requested_grid_spacing.magnitude,
            self.fine_requested_grid_spacing.magnitude,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != set(cls.__dataclass_fields__):
            raise ValueError("QHO1D cross-grid comparison fields do not match")
        quantity_names = (
            "box_half_width",
            "coarse_requested_grid_spacing",
            "fine_requested_grid_spacing",
            "coarse_grid_spacing",
            "fine_grid_spacing",
            "coarse_minus_fine_frobenius",
        )
        if any(not isinstance(values[name], ScalarQuantity) for name in quantity_names):
            raise TypeError("cross-grid quantities must decode to ScalarQuantity")
        retained_dimension = values["retained_dimension"]
        coarse_points = values["coarse_interior_points"]
        fine_points = values["fine_interior_points"]
        dimensions = (retained_dimension, coarse_points, fine_points)
        if any(type(value) is not int for value in dimensions):
            raise TypeError("cross-grid dimensions must decode to built-in ints")
        return cls(
            box_half_width=cast(ScalarQuantity, values["box_half_width"]),
            retained_dimension=cast(int, retained_dimension),
            coarse_requested_grid_spacing=cast(
                ScalarQuantity, values["coarse_requested_grid_spacing"]
            ),
            fine_requested_grid_spacing=cast(
                ScalarQuantity, values["fine_requested_grid_spacing"]
            ),
            coarse_grid_spacing=cast(ScalarQuantity, values["coarse_grid_spacing"]),
            fine_grid_spacing=cast(ScalarQuantity, values["fine_grid_spacing"]),
            coarse_interior_points=cast(int, coarse_points),
            fine_interior_points=cast(int, fine_points),
            coarse_minus_fine_frobenius=cast(
                ScalarQuantity, values["coarse_minus_fine_frobenius"]
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dCrossGridAnalysisResult(BaseTypedRecord):
    """Compose the complete adjacent-grid diagnostic inventory.

    Parameters
    ----------
    configuration
        Exact direct QHO1D sweep configuration.
    comparisons
        Ordered adjacent-grid comparisons with box varying slowest, retained
        dimension next, and adjacent requested-spacing pair fastest.

    Raises
    ------
    TypeError
        The configuration or comparison collection has the wrong type.
    ValueError
        The comparisons do not cover the configured adjacent-grid inventory.
    """

    configuration: Qho1dConfiguration
    comparisons: tuple[Qho1dCrossGridComparisonResult, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, Qho1dConfiguration):
            raise TypeError("configuration must be Qho1dConfiguration")
        if not isinstance(self.comparisons, tuple) or any(
            not isinstance(value, Qho1dCrossGridComparisonResult)
            for value in self.comparisons
        ):
            raise TypeError(
                "comparisons must be a tuple of Qho1dCrossGridComparisonResult"
            )
        if len(self.configuration.grid_spacings) < 2:
            raise ValueError("cross-grid analysis requires at least two grid spacings")
        expected = tuple(
            (box, retained, coarse, fine)
            for box in self.configuration.box_half_widths
            for retained in self.configuration.retained_dimensions
            for coarse, fine in zip(
                self.configuration.grid_spacings,
                self.configuration.grid_spacings[1:],
                strict=False,
            )
        )
        if tuple(value.key for value in self.comparisons) != expected:
            raise ValueError(
                "comparisons must equal the configured adjacent-grid inventory"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "configuration": self.configuration,
            "comparisons": self.comparisons,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"configuration", "comparisons"}:
            raise ValueError("QHO1D cross-grid analysis fields do not match")
        configuration_value = values["configuration"]
        comparisons_value = values["comparisons"]
        if not isinstance(configuration_value, Mapping):
            raise TypeError("configuration must decode to a mapping")
        if not isinstance(comparisons_value, tuple) or any(
            not isinstance(value, Mapping) for value in comparisons_value
        ):
            raise TypeError("comparisons must decode to a tuple of mappings")
        return cls(
            configuration=Qho1dConfiguration.from_dict(configuration_value),
            comparisons=tuple(
                Qho1dCrossGridComparisonResult.from_dict(value)
                for value in comparisons_value
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dCrossGridAnalysisRequest:
    """Bind one complete direct result for adjacent-grid analysis."""

    result: Qho1dCalculationResult

    def __post_init__(self) -> None:
        """Admit the exact typed calculation subject."""
        if type(self.result) is not Qho1dCalculationResult:
            raise TypeError("result must be Qho1dCalculationResult")


class Qho1dCrossGridAnalyzer:
    """Calculate adjacent-grid changes from one bound QHO1D result."""

    __slots__ = ("_request",)

    def __init__(self, request: Qho1dCrossGridAnalysisRequest) -> None:
        if type(request) is not Qho1dCrossGridAnalysisRequest:
            raise TypeError("request must be Qho1dCrossGridAnalysisRequest")
        self._request = request

    @property
    def request(self) -> Qho1dCrossGridAnalysisRequest:
        """Return the complete immutable adjacent-grid analysis request."""
        return self._request

    def execute(self) -> Qho1dCrossGridAnalysisResult:
        """Calculate the complete adjacent-grid comparison inventory.

        Returns
        -------
        Qho1dCrossGridAnalysisResult
            Typed ordered coarse/fine Frobenius diagnostics.

        Raises
        ------
        ValueError
            A configured case is absent, duplicated, or does not define a strict
            coarse/fine pair after grid realization.
        """
        result = self.request.result
        cases = _Qho1dCaseInventory(result)
        comparisons: list[Qho1dCrossGridComparisonResult] = []
        configuration = result.configuration
        for box in configuration.box_half_widths:
            for retained in configuration.retained_dimensions:
                for coarse_requested, fine_requested in zip(
                    configuration.grid_spacings,
                    configuration.grid_spacings[1:],
                    strict=False,
                ):
                    coarse = cases.required((box, coarse_requested, retained))
                    fine = cases.required((box, fine_requested, retained))
                    difference = MatrixQuantity(
                        coarse.pulled_back_hamiltonian.magnitude
                        - fine.pulled_back_hamiltonian.magnitude,
                        coarse.pulled_back_hamiltonian.unit,
                    )
                    comparisons.append(
                        Qho1dCrossGridComparisonResult(
                            box_half_width=coarse.box_half_width,
                            retained_dimension=retained,
                            coarse_requested_grid_spacing=(
                                coarse.requested_grid_spacing
                            ),
                            fine_requested_grid_spacing=fine.requested_grid_spacing,
                            coarse_grid_spacing=coarse.grid_spacing,
                            fine_grid_spacing=fine.grid_spacing,
                            coarse_interior_points=coarse.interior_points,
                            fine_interior_points=fine.interior_points,
                            coarse_minus_fine_frobenius=FrobeniusMatrixNorm(
                                difference
                            ).result(),
                        )
                    )
        return Qho1dCrossGridAnalysisResult(
            configuration=configuration,
            comparisons=tuple(comparisons),
        )


class Qho1dCrossGridVerification(CompositeVerification):
    """Compose checks of derived adjacent-grid Frobenius diagnostics."""


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dCrossGridVerificationRequest:
    """Bind one calculation and its correlated derived cross-grid analysis."""

    result: Qho1dCalculationResult
    analysis: Qho1dCrossGridAnalysisResult

    def __post_init__(self) -> None:
        """Admit both typed subjects and their exact configuration correlation."""
        if type(self.result) is not Qho1dCalculationResult:
            raise TypeError("result must be Qho1dCalculationResult")
        if type(self.analysis) is not Qho1dCrossGridAnalysisResult:
            raise TypeError("analysis must be Qho1dCrossGridAnalysisResult")
        if self.analysis.configuration.to_json() != self.result.configuration.to_json():
            raise ValueError("analysis configuration differs from calculation result")


class Qho1dCrossGridVerifier:
    """Verify one bound adjacent-grid analysis from authoritative case matrices."""

    __slots__ = ("_request",)

    def __init__(self, request: Qho1dCrossGridVerificationRequest) -> None:
        if type(request) is not Qho1dCrossGridVerificationRequest:
            raise TypeError("request must be Qho1dCrossGridVerificationRequest")
        self._request = request

    @property
    def request(self) -> Qho1dCrossGridVerificationRequest:
        """Return the complete immutable cross-grid verification request."""
        return self._request

    def execute(self) -> Qho1dCrossGridVerification:
        """Verify every stored diagnostic against direct matrix subtraction.

        Returns
        -------
        Qho1dCrossGridVerification
            Exact, operation-named verification observations.

        Raises
        ------
        ValueError
            A declared case is absent or duplicated.

        Notes
        -----
        This verifier does not invoke ``Qho1dAnalyzer``, ``Qho1dComparator``, or
        ``Qho1dCrossGridAnalyzer``. It verifies derivation from the supplied
        authoritative matrices; independent reconstruction of those matrices remains
        the responsibility of ``Qho1dVerifier``.
        """
        result = self.request.result
        analysis = self.request.analysis
        cases = _Qho1dCaseInventory(result)
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}
        for index, diagnostic in enumerate(analysis.comparisons):
            box, retained, coarse_requested, fine_requested = diagnostic.key
            coarse = cases.required((box, coarse_requested, retained))
            fine = cases.required((box, fine_requested, retained))
            difference = MatrixQuantity(
                coarse.pulled_back_hamiltonian.magnitude
                - fine.pulled_back_hamiltonian.magnitude,
                coarse.pulled_back_hamiltonian.unit,
            )
            reference = FrobeniusMatrixNorm(difference).result()
            prefix = f"pair_{index:02d}"
            expected = {
                "coarse_grid_spacing": coarse.grid_spacing,
                "fine_grid_spacing": fine.grid_spacing,
                "coarse_interior_points": ScalarQuantity(
                    float(coarse.interior_points), Unitless()
                ),
                "fine_interior_points": ScalarQuantity(
                    float(fine.interior_points), Unitless()
                ),
                "coarse_minus_fine_frobenius": reference,
            }
            observed = {
                "coarse_grid_spacing": diagnostic.coarse_grid_spacing,
                "fine_grid_spacing": diagnostic.fine_grid_spacing,
                "coarse_interior_points": ScalarQuantity(
                    float(diagnostic.coarse_interior_points), Unitless()
                ),
                "fine_interior_points": ScalarQuantity(
                    float(diagnostic.fine_interior_points), Unitless()
                ),
                "coarse_minus_fine_frobenius": (diagnostic.coarse_minus_fine_frobenius),
            }
            for name, expected_value in expected.items():
                comparisons[f"{prefix}.{name}"] = MaximumAbsoluteErrorComparison(
                    observed=observed[name],
                    reference=expected_value,
                    tolerance=ScalarQuantity(0.0, expected_value.unit),
                )
        return Qho1dCrossGridVerification.evaluate(comparisons)
