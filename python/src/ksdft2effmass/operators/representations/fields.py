"""Semantic-role interfaces and immutable NumPy-backed matrix fields.

The concrete leaves validate finite ``complex128`` storage, domain correlation,
and shape only. Their names declare an intended role; they do not establish
Hermiticity, projector identities, unitarity, isometry, periodicity, or sewing.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.numerics.numpy.validation import immutable_complex128_array

from .domains import (
    FiniteDomainABC,
    FiniteMomentumMeshDomain,
    FiniteTranslationDomain,
)


class MatrixFieldABC(ABC):
    """Narrow interface for a finite-domain-correlated matrix field."""

    __slots__ = ()

    @property
    @abstractmethod
    def domain(self) -> FiniteDomainABC:
        """Return the exact finite domain correlated with the first array axis."""

    @property
    @abstractmethod
    def values(self) -> Complex128Array:
        """Return immutable finite matrices in retained domain order."""

    @property
    @abstractmethod
    def source_dimension(self) -> int:
        """Return the positive matrix source dimension."""

    @property
    @abstractmethod
    def target_dimension(self) -> int:
        """Return the positive matrix target dimension."""

    def __eq__(self, other: object) -> bool:
        """Return exact value equality for one identical concrete field type."""
        if type(self) is not type(other):
            return NotImplemented
        if not isinstance(other, MatrixFieldABC):
            return NotImplemented
        return self.domain == other.domain and bool(
            np.array_equal(self.values, other.values)
        )


class SquareMatrixFieldABC(MatrixFieldABC, ABC):
    """Matrix field whose source and target dimensions are equal."""

    __slots__ = ()

    @property
    def dimension(self) -> int:
        """Return the common square-matrix dimension."""
        return self.source_dimension


class OperatorFieldABC(SquareMatrixFieldABC, ABC):
    """Intended operator-field role without mathematical-property inference."""

    __slots__ = ()


class ProjectorFieldABC(SquareMatrixFieldABC, ABC):
    """Intended projector-field role without projector evidence inference."""

    __slots__ = ()


class GaugeFieldABC(SquareMatrixFieldABC, ABC):
    """Intended internal-gauge role without unitarity evidence inference."""

    __slots__ = ()


class RectangularMatrixFieldABC(MatrixFieldABC, ABC):
    """Matrix field that may have unequal source and target dimensions."""

    __slots__ = ()


class FrameFieldABC(RectangularMatrixFieldABC, ABC):
    """Intended frame role without isometry evidence inference."""

    __slots__ = ()


class FourierBlockFieldABC(SquareMatrixFieldABC, ABC):
    """Translation-domain square matrix-coefficient field."""

    __slots__ = ()


def _require_momentum_domain(
    domain: FiniteMomentumMeshDomain,
    /,
) -> FiniteMomentumMeshDomain:
    """Validate one exact momentum-domain leaf."""
    if type(domain) is not FiniteMomentumMeshDomain:
        raise TypeError("domain must be an exact FiniteMomentumMeshDomain")
    return domain


def _require_translation_domain(
    domain: FiniteTranslationDomain,
    /,
) -> FiniteTranslationDomain:
    """Validate one exact translation-domain leaf."""
    if type(domain) is not FiniteTranslationDomain:
        raise TypeError("domain must be an exact FiniteTranslationDomain")
    return domain


def _immutable_field_values(
    values: Complex128Array,
    domain: FiniteDomainABC,
    name: str,
    /,
    *,
    require_square: bool,
) -> Complex128Array:
    """Own and validate one finite field array and its domain correlation."""
    immutable = immutable_complex128_array(values, name)
    if immutable.ndim != 3:
        raise ValueError(f"{name} must have shape (domain, target, source)")
    if immutable.shape[0] != domain.cardinality:
        raise ValueError(f"{name} first axis must match domain cardinality")
    if immutable.shape[1] <= 0 or immutable.shape[2] <= 0:
        raise ValueError(f"{name} matrix dimensions must be positive")
    if require_square and immutable.shape[1] != immutable.shape[2]:
        raise ValueError(f"{name} matrices must be square")
    return immutable


@final
@dataclass(frozen=True, slots=True, eq=False, init=False)
class NumpyOperatorField(OperatorFieldABC):
    """Immutable momentum-domain field with intended operator role."""

    _domain: FiniteMomentumMeshDomain
    _values: Complex128Array

    def __init__(
        self,
        domain: FiniteMomentumMeshDomain,
        values: Complex128Array,
    ) -> None:
        """Own validated finite complex square matrices in domain order."""
        validated_domain = _require_momentum_domain(domain)
        immutable = _immutable_field_values(
            values,
            validated_domain,
            "operator field values",
            require_square=True,
        )
        object.__setattr__(self, "_domain", validated_domain)
        object.__setattr__(self, "_values", immutable)

    @property
    def domain(self) -> FiniteMomentumMeshDomain:
        """Return the exact momentum domain."""
        return self._domain

    @property
    def values(self) -> Complex128Array:
        """Return immutable complex128 matrices."""
        return self._values

    @property
    def source_dimension(self) -> int:
        """Return the common square source dimension."""
        return int(self._values.shape[2])

    @property
    def target_dimension(self) -> int:
        """Return the common square target dimension."""
        return int(self._values.shape[1])


@final
@dataclass(frozen=True, slots=True, eq=False, init=False)
class NumpyProjectorField(ProjectorFieldABC):
    """Immutable momentum-domain field with intended projector role."""

    _domain: FiniteMomentumMeshDomain
    _values: Complex128Array

    def __init__(
        self,
        domain: FiniteMomentumMeshDomain,
        values: Complex128Array,
    ) -> None:
        """Own validated finite complex square matrices in domain order."""
        validated_domain = _require_momentum_domain(domain)
        immutable = _immutable_field_values(
            values,
            validated_domain,
            "projector field values",
            require_square=True,
        )
        object.__setattr__(self, "_domain", validated_domain)
        object.__setattr__(self, "_values", immutable)

    @property
    def domain(self) -> FiniteMomentumMeshDomain:
        """Return the exact momentum domain."""
        return self._domain

    @property
    def values(self) -> Complex128Array:
        """Return immutable complex128 matrices."""
        return self._values

    @property
    def source_dimension(self) -> int:
        """Return the common square source dimension."""
        return int(self._values.shape[2])

    @property
    def target_dimension(self) -> int:
        """Return the common square target dimension."""
        return int(self._values.shape[1])


@final
@dataclass(frozen=True, slots=True, eq=False, init=False)
class NumpyGaugeField(GaugeFieldABC):
    """Immutable momentum-domain field with intended gauge role."""

    _domain: FiniteMomentumMeshDomain
    _values: Complex128Array

    def __init__(
        self,
        domain: FiniteMomentumMeshDomain,
        values: Complex128Array,
    ) -> None:
        """Own validated finite complex square matrices in domain order."""
        validated_domain = _require_momentum_domain(domain)
        immutable = _immutable_field_values(
            values,
            validated_domain,
            "gauge field values",
            require_square=True,
        )
        object.__setattr__(self, "_domain", validated_domain)
        object.__setattr__(self, "_values", immutable)

    @property
    def domain(self) -> FiniteMomentumMeshDomain:
        """Return the exact momentum domain."""
        return self._domain

    @property
    def values(self) -> Complex128Array:
        """Return immutable complex128 matrices."""
        return self._values

    @property
    def source_dimension(self) -> int:
        """Return the common square source dimension."""
        return int(self._values.shape[2])

    @property
    def target_dimension(self) -> int:
        """Return the common square target dimension."""
        return int(self._values.shape[1])


@final
@dataclass(frozen=True, slots=True, eq=False, init=False)
class NumpyFrameField(FrameFieldABC):
    """Immutable momentum-domain rectangular field with intended frame role.

    Matrix columns are source coordinates in the retained space and rows are
    target coordinates in the ambient space. No isometry is inferred.
    """

    _domain: FiniteMomentumMeshDomain
    _values: Complex128Array

    def __init__(
        self,
        domain: FiniteMomentumMeshDomain,
        values: Complex128Array,
    ) -> None:
        """Own validated finite complex rectangular matrices in domain order."""
        validated_domain = _require_momentum_domain(domain)
        immutable = _immutable_field_values(
            values,
            validated_domain,
            "frame field values",
            require_square=False,
        )
        object.__setattr__(self, "_domain", validated_domain)
        object.__setattr__(self, "_values", immutable)

    @property
    def domain(self) -> FiniteMomentumMeshDomain:
        """Return the exact momentum domain."""
        return self._domain

    @property
    def values(self) -> Complex128Array:
        """Return immutable complex128 matrices."""
        return self._values

    @property
    def source_dimension(self) -> int:
        """Return the represented frame-column dimension."""
        return int(self._values.shape[2])

    @property
    def target_dimension(self) -> int:
        """Return the represented frame-row dimension."""
        return int(self._values.shape[1])


@final
@dataclass(frozen=True, slots=True, eq=False, init=False)
class NumpyFourierBlockField(FourierBlockFieldABC):
    """Immutable translation-domain square Fourier-block field."""

    _domain: FiniteTranslationDomain
    _values: Complex128Array

    def __init__(
        self,
        domain: FiniteTranslationDomain,
        values: Complex128Array,
    ) -> None:
        """Own validated finite complex square blocks in domain order."""
        validated_domain = _require_translation_domain(domain)
        immutable = _immutable_field_values(
            values,
            validated_domain,
            "Fourier block field values",
            require_square=True,
        )
        object.__setattr__(self, "_domain", validated_domain)
        object.__setattr__(self, "_values", immutable)

    @property
    def domain(self) -> FiniteTranslationDomain:
        """Return the exact translation domain."""
        return self._domain

    @property
    def values(self) -> Complex128Array:
        """Return immutable complex128 blocks."""
        return self._values

    @property
    def source_dimension(self) -> int:
        """Return the common square source dimension."""
        return int(self._values.shape[2])

    @property
    def target_dimension(self) -> int:
        """Return the common square target dimension."""
        return int(self._values.shape[1])


__all__ = [
    "FourierBlockFieldABC",
    "FrameFieldABC",
    "GaugeFieldABC",
    "MatrixFieldABC",
    "NumpyFourierBlockField",
    "NumpyFrameField",
    "NumpyGaugeField",
    "NumpyOperatorField",
    "NumpyProjectorField",
    "OperatorFieldABC",
    "ProjectorFieldABC",
    "RectangularMatrixFieldABC",
    "SquareMatrixFieldABC",
]
