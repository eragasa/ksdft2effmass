"""Typed physical-metric shell aggregation for block-hopping powers.

PhysKit owns raw unit-aware squared Frobenius powers for individual hopping blocks.
This module owns only the KSD model-adequacy policy that assigns those blocks to
physical-metric shells and normalizes their powers by the retained rank.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    BlockHoppingModel,
    BlockHoppingTerm,
)
from projectkoios.physkit.solidstate.tb.diagnostics import (
    BlockHoppingPowerAnalyzer,
    BlockHoppingPowerResult,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless


@dataclass(frozen=True, slots=True)
class MetricShellHoppingPower:
    """Retain one unitless normalized block power and its metric shell.

    The power is a finite nonnegative built-in float. Construction rejects booleans,
    numeric strings, NumPy scalar types, negative values, and nonfinite values.
    """

    displacement: LatticeDisplacement
    shell_index: int
    normalized_frobenius_power: float

    def __post_init__(self) -> None:
        """Validate one exact displacement, shell label, and finite power."""
        if type(self.displacement) is not LatticeDisplacement:
            raise TypeError("displacement must be LatticeDisplacement")
        if type(self.shell_index) is not int:
            raise TypeError("shell_index must be a built-in integer")
        if self.shell_index < 0:
            raise ValueError("shell_index must be nonnegative")
        if type(self.normalized_frobenius_power) is not float:
            raise TypeError("normalized_frobenius_power must be a built-in float")
        if (
            not math.isfinite(self.normalized_frobenius_power)
            or self.normalized_frobenius_power < 0.0
        ):
            raise ValueError(
                "normalized_frobenius_power must be finite and nonnegative"
            )

    @property
    def metric_shell_value(self) -> int:
        """Return the historical shell label as a scaled metric value."""
        return self.shell_index


@dataclass(frozen=True, slots=True)
class MetricShellHoppingPowerResult:
    """Retain unitless binary64 powers in canonical displacement order.

    Aggregate methods return built-in floats and raise :class:`FloatingPointError` if
    their finite inputs overflow during summation.
    """

    retained_rank: int
    powers: tuple[MetricShellHoppingPower, ...]

    def __post_init__(self) -> None:
        """Validate rank, ownership, canonical order, and shell inventory."""
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank <= 0:
            raise ValueError("retained_rank must be positive")
        if type(self.powers) is not tuple or any(
            type(power) is not MetricShellHoppingPower for power in self.powers
        ):
            raise TypeError("powers must contain MetricShellHoppingPower values")
        if not self.powers:
            raise ValueError("powers must be nonempty")
        components = tuple(power.displacement.components for power in self.powers)
        if components != tuple(sorted(set(components))):
            raise ValueError("powers must follow unique canonical displacement order")

    def _require_shell_index(self, shell_index: int) -> None:
        """Require one nonnegative built-in shell index."""
        if type(shell_index) is not int:
            raise TypeError("shell_index must be a built-in integer")
        if shell_index < 0:
            raise ValueError("shell_index must be nonnegative")

    def _finite_power_sum(self, values: Iterable[float]) -> float:
        """Return one finite built-in-float sum or reject overflow."""
        try:
            total = math.fsum(values)
        except OverflowError as error:
            raise FloatingPointError(
                "normalized hopping-power sum overflowed"
            ) from error
        if not math.isfinite(total):
            raise FloatingPointError("normalized hopping-power sum became nonfinite")
        return total

    @property
    def normalized_total_power(self) -> float:
        """Return normalized power across the complete block inventory."""
        return self._finite_power_sum(
            power.normalized_frobenius_power for power in self.powers
        )

    def normalized_power_at_shell(self, shell_index: int) -> float:
        """Return normalized power assigned exactly to ``shell_index``."""
        self._require_shell_index(shell_index)
        return self._finite_power_sum(
            power.normalized_frobenius_power
            for power in self.powers
            if power.shell_index == shell_index
        )

    def normalized_power_beyond_shell(self, shell_index: int) -> float:
        """Return normalized power assigned beyond ``shell_index``."""
        self._require_shell_index(shell_index)
        return self._finite_power_sum(
            power.normalized_frobenius_power
            for power in self.powers
            if power.shell_index > shell_index
        )

    def normalized_power_for(
        self,
        displacements: tuple[LatticeDisplacement, ...],
    ) -> float:
        """Return normalized power for one explicit displacement inventory."""
        if type(displacements) is not tuple or any(
            type(displacement) is not LatticeDisplacement
            for displacement in displacements
        ):
            raise TypeError("displacements must contain LatticeDisplacement values")
        components = tuple(displacement.components for displacement in displacements)
        if components != tuple(sorted(set(components))):
            raise ValueError("displacements must be sorted and unique")
        available = {power.displacement.components for power in self.powers}
        if not set(components).issubset(available):
            raise ValueError("displacements must belong to the power inventory")
        requested = set(components)
        return self._finite_power_sum(
            power.normalized_frobenius_power
            for power in self.powers
            if power.displacement.components in requested
        )


class BandEquivalenceLocalityFourierShellPowerAnalyzer:
    """Adapt one immutable Fourier series to the typed shell-power owners."""

    __slots__ = (
        "_basis_identifier",
        "_energy_reference",
        "_identifier",
        "_power_analyzer",
        "_retained_rank",
        "_series",
        "_shell_indices",
    )

    def __init__(
        self,
        *,
        identifier: str,
        energy_reference: str,
        basis_identifier: str,
        series: NumpyFiniteFourierMatrixSeries,
        shell_indices: tuple[int, ...],
        retained_rank: int,
        power_analyzer: BlockHoppingPowerAnalyzer,
    ) -> None:
        """Bind one immutable Fourier inventory and explicit power collaborator."""
        if type(identifier) is not str:
            raise TypeError("identifier must be a built-in string")
        if not identifier:
            raise ValueError("identifier must be nonempty")
        for value, name in (
            (energy_reference, "energy_reference"),
            (basis_identifier, "basis_identifier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(series) is not NumpyFiniteFourierMatrixSeries:
            raise TypeError("series must be NumpyFiniteFourierMatrixSeries")
        if series.dimension not in (2, 3):
            raise ValueError("series dimension must be two or three")
        if type(shell_indices) is not tuple or any(
            type(shell_index) is not int for shell_index in shell_indices
        ):
            raise TypeError("shell_indices must contain built-in integers")
        if len(shell_indices) != len(series.integer_modes):
            raise ValueError("shell_indices must match the Fourier term count")
        if any(shell_index < 0 for shell_index in shell_indices):
            raise ValueError("shell_indices must be nonnegative")
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if retained_rank <= 0:
            raise ValueError("retained_rank must be positive")
        if series.matrix_coefficients.shape[1:] != (
            retained_rank,
            retained_rank,
        ):
            raise ValueError("retained_rank must match the Fourier block size")
        if type(power_analyzer) is not BlockHoppingPowerAnalyzer:
            raise TypeError("power_analyzer must be BlockHoppingPowerAnalyzer")
        self._identifier = identifier
        self._energy_reference = energy_reference
        self._basis_identifier = basis_identifier
        self._series = series
        self._shell_indices = shell_indices
        self._retained_rank = retained_rank
        self._power_analyzer = power_analyzer

    def _displacement(self, components: NDArray[np.int64]) -> LatticeDisplacement:
        """Return one typed displacement from a bound-series mode row."""
        if self._series.dimension == 2:
            return LatticeDisplacement(
                LatticeDimension.TWO,
                (int(components[0]), int(components[1])),
            )
        return LatticeDisplacement(
            LatticeDimension.THREE,
            (int(components[0]), int(components[1]), int(components[2])),
        )

    def execute(self) -> MetricShellHoppingPowerResult:
        """Return typed shell powers through the PhysKit raw-power owner."""
        entries = sorted(
            (
                (
                    self._displacement(mode),
                    np.array(coefficient, dtype=np.complex128, copy=True),
                    shell_index,
                )
                for mode, coefficient, shell_index in zip(
                    self._series.integer_modes,
                    self._series.matrix_coefficients,
                    self._shell_indices,
                    strict=True,
                )
            ),
            key=lambda entry: entry[0].components,
        )
        dimension = (
            LatticeDimension.TWO
            if self._series.dimension == 2
            else LatticeDimension.THREE
        )
        model = BlockHoppingModel(
            identifier=self._identifier,
            dimension=dimension,
            terms=tuple(
                BlockHoppingTerm(
                    displacement=displacement,
                    coefficient=ComplexMatrixQuantity(coefficient, Unitless()),
                )
                for displacement, coefficient, _ in entries
            ),
            energy_unit=Unitless(),
            energy_reference=self._energy_reference,
            basis_identifier=self._basis_identifier,
        )
        return MetricShellHoppingPowerAnalyzer(
            model=model,
            shell_indices=tuple(shell_index for _, _, shell_index in entries),
            retained_rank=self._retained_rank,
            power_analyzer=self._power_analyzer,
        ).execute()


class MetricShellHoppingPowerAnalyzer:
    """Aggregate PhysKit-owned raw block powers by KSD metric-shell labels.

    This action accepts only a unitless block model because its public result uses
    built-in floats. It applies finite binary64 division by the positive built-in
    integer retained rank; aggregate overflow is reported by the result methods.
    """

    __slots__ = ("_model", "_power_analyzer", "_retained_rank", "_shell_indices")

    def __init__(
        self,
        *,
        model: BlockHoppingModel,
        shell_indices: tuple[int, ...],
        retained_rank: int,
        power_analyzer: BlockHoppingPowerAnalyzer,
    ) -> None:
        """Bind one immutable model, shell inventory, rank, and collaborator."""
        if type(model) is not BlockHoppingModel:
            raise TypeError("model must be BlockHoppingModel")
        if type(model.energy_unit) is not Unitless:
            raise ValueError("metric-shell scalar powers require a unitless model")
        if type(shell_indices) is not tuple or any(
            type(shell_index) is not int for shell_index in shell_indices
        ):
            raise TypeError("shell_indices must contain built-in integers")
        if len(shell_indices) != len(model.terms):
            raise ValueError("shell_indices must match the model term count")
        if any(shell_index < 0 for shell_index in shell_indices):
            raise ValueError("shell_indices must be nonnegative")
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if retained_rank <= 0:
            raise ValueError("retained_rank must be positive")
        if retained_rank != model.basis_size:
            raise ValueError("retained_rank must match the model basis size")
        if type(power_analyzer) is not BlockHoppingPowerAnalyzer:
            raise TypeError("power_analyzer must be BlockHoppingPowerAnalyzer")
        self._model = model
        self._shell_indices = shell_indices
        self._retained_rank = retained_rank
        self._power_analyzer = power_analyzer

    def execute(self) -> MetricShellHoppingPowerResult:
        """Return normalized block powers in canonical displacement order."""
        raw: BlockHoppingPowerResult = self._power_analyzer.execute(self._model)
        normalization = float(self._retained_rank)
        return MetricShellHoppingPowerResult(
            retained_rank=self._retained_rank,
            powers=tuple(
                MetricShellHoppingPower(
                    displacement=power.displacement,
                    shell_index=shell_index,
                    normalized_frobenius_power=(
                        power.frobenius_power.magnitude / normalization
                    ),
                )
                for power, shell_index in zip(
                    raw.powers,
                    self._shell_indices,
                    strict=True,
                )
            ),
        )


__all__ = [
    "BandEquivalenceLocalityFourierShellPowerAnalyzer",
    "MetricShellHoppingPower",
    "MetricShellHoppingPowerAnalyzer",
    "MetricShellHoppingPowerResult",
]
