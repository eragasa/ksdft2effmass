"""Typed scientific values for finite-rank band-equivalence/locality losses."""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.numerics.validation import exact_nonnegative_float

from ksdft2effmass.analysis.matrix_field import positive_norm_energy_scale
from ksdft2effmass.representation_equivalence import RepresentationEquivalence


@dataclass(frozen=True, slots=True)
class BandEquivalenceHoppingLocalitySampleMeasure:
    """Identify one normalized C-order measure on a periodic sample inventory."""

    spatial_dimension: int
    sample_shape: tuple[int, ...]
    sample_weights: tuple[float, ...]
    sample_inventory_identifier: str

    def __post_init__(self) -> None:
        dimension = _spatial_dimension(self.spatial_dimension)
        shape = _sample_shape(self.sample_shape, dimension)
        _sample_weights(self.sample_weights, shape)
        _identifier("sample_inventory_identifier", self.sample_inventory_identifier)


@dataclass(frozen=True, slots=True)
class BandEquivalenceHoppingLocalityComparisonIdentity:
    """Declare the state-space and physical identities required for comparison."""

    retained_basis_identifier: str
    retained_space_identifier: str
    gauge_identifier: str
    geometry_identifier: str
    energy_unit_identifier: str
    energy_reference_identifier: str

    def __post_init__(self) -> None:
        _identifier("retained_basis_identifier", self.retained_basis_identifier)
        _identifier("retained_space_identifier", self.retained_space_identifier)
        _identifier("gauge_identifier", self.gauge_identifier)
        _identifier("geometry_identifier", self.geometry_identifier)
        _identifier("energy_unit_identifier", self.energy_unit_identifier)
        _identifier("energy_reference_identifier", self.energy_reference_identifier)


@dataclass(frozen=True, slots=True)
class BandEquivalenceHoppingLocalityLossDefinition:
    """Own the complete finite-rank loss definition independently of its result."""

    retained_rank: int
    sample_measure: BandEquivalenceHoppingLocalitySampleMeasure
    comparison_identity: BandEquivalenceHoppingLocalityComparisonIdentity
    norm_energy_scale: float

    def __post_init__(self) -> None:
        rank = _retained_rank(self.retained_rank)
        if type(self.sample_measure) is not BandEquivalenceHoppingLocalitySampleMeasure:
            raise TypeError(
                "sample_measure must be BandEquivalenceHoppingLocalitySampleMeasure"
            )
        if (
            type(self.comparison_identity)
            is not BandEquivalenceHoppingLocalityComparisonIdentity
        ):
            raise TypeError(
                "comparison_identity must be BandEquivalenceHoppingLocalityComparisonIdentity"  # noqa: E501
            )
        norm_energy_scale = positive_norm_energy_scale(self.norm_energy_scale)
        _loss_normalization(rank, norm_energy_scale)


@dataclass(frozen=True, slots=True)
class BandEquivalenceHoppingLocalityLoss(RepresentationEquivalence):
    r"""Retain finite-rank operator and ordered-spectrum loss values.

    For normalized sample weights :math:`w_q`, explicitly same-space rank-:math:`r`
    Hamiltonians :math:`H_q` and :math:`\widetilde H_q`, ordered eigenvalues
    :math:`\epsilon_{qn}` and :math:`\widetilde\epsilon_{qn}`, and declared
    :math:`E_{\mathrm{norm}}>0`, the losses are

    .. math::

       L_H = \frac{1}{rE_{\mathrm{norm}}^2}
             \sum_q w_q\lVert H_q-\widetilde H_q\rVert_F^2,

       L_\epsilon = \frac{1}{rE_{\mathrm{norm}}^2}
             \sum_q w_q\sum_{n=1}^r
             (\epsilon_{qn}-\widetilde\epsilon_{qn})^2.

    For :math:`r=2`, these are the Ragasa2026a losses. The explicit :math:`1/r`
    normalization is the cross-rank quadratic normalization selected by Ragasa2026c.
    ``norm_energy_scale`` remains only a positive normalization magnitude. The separate
    energy-reference identity declares the common energy-zero/alignment convention.
    """

    definition: BandEquivalenceHoppingLocalityLossDefinition
    operator_loss: float
    spectral_loss: float

    def __post_init__(self) -> None:
        if type(self.definition) is not BandEquivalenceHoppingLocalityLossDefinition:
            raise TypeError(
                "definition must be BandEquivalenceHoppingLocalityLossDefinition"
            )
        exact_nonnegative_float(self.operator_loss, "operator_loss")
        exact_nonnegative_float(self.spectral_loss, "spectral_loss")

    @property
    def spatial_dimension(self) -> int:
        """Return the dimension of the sample inventory."""
        return self.definition.sample_measure.spatial_dimension

    @property
    def retained_rank(self) -> int:
        """Return the retained Hamiltonian rank."""
        return self.definition.retained_rank

    @property
    def sample_shape(self) -> tuple[int, ...]:
        """Return the leading matrix-field sample shape."""
        return self.definition.sample_measure.sample_shape

    @property
    def sample_weights(self) -> tuple[float, ...]:
        """Return normalized weights in NumPy C order."""
        return self.definition.sample_measure.sample_weights

    @property
    def sample_inventory_identifier(self) -> str:
        """Return the reciprocal-sample inventory identity."""
        return self.definition.sample_measure.sample_inventory_identifier

    @property
    def retained_basis_identifier(self) -> str:
        """Return the common retained-basis identity."""
        return self.definition.comparison_identity.retained_basis_identifier

    @property
    def retained_space_identifier(self) -> str:
        """Return the common retained-space identity."""
        return self.definition.comparison_identity.retained_space_identifier

    @property
    def gauge_identifier(self) -> str:
        """Return the common gauge identity."""
        return self.definition.comparison_identity.gauge_identifier

    @property
    def geometry_identifier(self) -> str:
        """Return the physical geometry identity."""
        return self.definition.comparison_identity.geometry_identifier

    @property
    def energy_unit_identifier(self) -> str:
        """Return the matrix-field energy unit identity."""
        return self.definition.comparison_identity.energy_unit_identifier

    @property
    def energy_reference_identifier(self) -> str:
        """Return the common energy-zero/alignment identity."""
        return self.definition.comparison_identity.energy_reference_identifier

    @property
    def norm_energy_scale(self) -> float:
        """Return the positive energy normalization magnitude."""
        return self.definition.norm_energy_scale


def _spatial_dimension(value: int) -> int:
    if type(value) is not int:
        raise TypeError("spatial_dimension must be a built-in integer")
    if value not in (2, 3):
        raise ValueError("spatial_dimension must be two or three")
    return value


def _retained_rank(value: int) -> int:
    if type(value) is not int:
        raise TypeError("retained_rank must be a built-in integer")
    if value < 2:
        raise ValueError("retained_rank must be at least two")
    return value


def _sample_shape(value: tuple[int, ...], dimension: int) -> tuple[int, ...]:
    if type(value) is not tuple or not all(type(size) is int for size in value):
        raise TypeError("sample_shape must contain built-in integers")
    if len(value) != dimension:
        raise ValueError("sample_shape length must match spatial_dimension")
    if not all(size >= 1 for size in value):
        raise ValueError("sample_shape entries must be positive")
    return value


def _sample_weights(
    value: tuple[float, ...],
    sample_shape: tuple[int, ...],
) -> tuple[float, ...]:
    if type(value) is not tuple or not all(type(weight) is float for weight in value):
        raise TypeError("sample_weights must contain built-in floats")
    if len(value) != math.prod(sample_shape):
        raise ValueError("sample_weights length must match sample_shape")
    if not all(math.isfinite(weight) and weight >= 0.0 for weight in value):
        raise ValueError("sample_weights must be finite and nonnegative")
    try:
        total_weight = math.fsum(value)
    except OverflowError as error:
        raise ValueError(
            "sample_weights must sum exactly to one in binary64"
        ) from error
    if total_weight != 1.0:
        raise ValueError("sample_weights must sum exactly to one in binary64")
    return value


def _identifier(name: str, value: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in string")
    if not value:
        raise ValueError(f"{name} must be nonempty")
    return value


def _loss_normalization(retained_rank: int, norm_energy_scale: float) -> float:
    try:
        scale_squared = norm_energy_scale * norm_energy_scale
        normalization = retained_rank * scale_squared
    except OverflowError as error:
        raise FloatingPointError("loss normalization overflowed") from error
    if not math.isfinite(scale_squared) or not math.isfinite(normalization):
        raise FloatingPointError("loss normalization overflowed")
    if scale_squared == 0.0 or normalization == 0.0:
        raise FloatingPointError("loss normalization underflowed")
    return normalization


__all__ = [
    "BandEquivalenceHoppingLocalityComparisonIdentity",
    "BandEquivalenceHoppingLocalityLoss",
    "BandEquivalenceHoppingLocalityLossDefinition",
    "BandEquivalenceHoppingLocalitySampleMeasure",
]
