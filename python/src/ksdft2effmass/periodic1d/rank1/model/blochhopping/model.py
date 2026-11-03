"""Periodic-1D retained-dimension-one Bloch-hopping model contract."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import ClassVar, Literal, Self, final

import numpy as np
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    DenseBlockHoppingModel,
    DenseBlockHoppingTerm,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
)

from ksdft2effmass.periodic import PeriodicModelRole
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.model.blochhopping import (
    Periodic1DBlochHoppingModel,
    Periodic1DLatticeKineticEnergyScale,
)


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank1BlochHoppingModel(Periodic1DBlochHoppingModel):
    """Bind one ordinary-lattice rank-one PhysKit hopping representation.

    ``band_subspace_rank`` is the retained-space dimension, not the algebraic rank of
    a coefficient matrix. The wrapped PhysKit model must contain exact ``1 x 1`` blocks
    on ordinary integer displacements in one spatial dimension. Every displacement must
    have its exact conjugate partner, including an exactly Hermitian onsite block.

    Complete finite-DFT cyclic coefficients are not admitted by this contract. They must
    remain in a cyclic representation until an explicit conversion establishes an
    ordinary-lattice hopping model.
    """

    MODEL_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic1d-rank1-bloch-hopping-model.v1"
    )

    geometry: Periodic1DLatticeGeometry
    physkit_model: DenseBlockHoppingModel

    @classmethod
    def from_lattice_kinetic_parameters(
        cls,
        *,
        identifier: str,
        geometry: Periodic1DLatticeGeometry,
        energy_unit: PhysicalUnit,
        energy_reference: str,
        basis_identifier: str,
        normalized_onsite: float,
        normalized_positive_hoppings: tuple[tuple[int, float | complex], ...],
    ) -> Self:
        r"""Construct a physical model from coefficients normalized by ``E_a``.

        ``normalized_onsite`` and every hopping ratio are multiplied by
        ``E_a = hbar^2 / (m_e a^2)`` in ``energy_unit``. Positive displacements must be
        strictly increasing. The constructor generates every negative-displacement
        coefficient as the exact complex conjugate of its positive partner.

        Boolean values, integers used as ratios, numeric strings, nonfinite ratios, and
        nonpositive or repeated hopping displacements are rejected. A ``ValueError`` is
        raised if dimensionalization produces a nonfinite binary64 coefficient.
        """
        if type(geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("geometry must be Periodic1DLatticeGeometry")
        if type(energy_unit) is not PhysicalUnit:
            raise TypeError("energy_unit must be PhysicalUnit")
        if type(normalized_onsite) is not float:
            raise TypeError("normalized_onsite must be a built-in float")
        if not math.isfinite(normalized_onsite):
            raise ValueError("normalized_onsite must be finite")
        if type(normalized_positive_hoppings) is not tuple:
            raise TypeError("normalized_positive_hoppings must be an exact tuple")

        admitted_hoppings: list[tuple[int, complex]] = []
        previous_displacement = 0
        for hopping in normalized_positive_hoppings:
            if type(hopping) is not tuple or len(hopping) != 2:
                raise TypeError(
                    "each normalized positive hopping must be a displacement-ratio pair"
                )
            displacement, ratio = hopping
            if type(displacement) is not int:
                raise TypeError("hopping displacements must be built-in integers")
            if displacement <= previous_displacement:
                raise ValueError(
                    "hopping displacements must be positive and strictly increasing"
                )
            if type(ratio) not in (float, complex):
                raise TypeError(
                    "normalized hopping ratios must be built-in float or complex values"
                )
            complex_ratio = complex(ratio)
            if not math.isfinite(complex_ratio.real) or not math.isfinite(
                complex_ratio.imag
            ):
                raise ValueError("normalized hopping ratios must be finite")
            admitted_hoppings.append((displacement, complex_ratio))
            previous_displacement = displacement

        energy_scale = Periodic1DLatticeKineticEnergyScale(
            lattice_geometry=geometry,
            energy_unit=energy_unit,
        ).energy_scale.magnitude

        onsite_coefficient = complex(energy_scale * normalized_onsite)
        if not math.isfinite(onsite_coefficient.real):
            raise ValueError("dimensionalized onsite coefficient must be finite")
        dimensionalized: list[tuple[int, complex]] = [(0, onsite_coefficient)]
        for displacement, ratio in admitted_hoppings:
            coefficient = energy_scale * ratio
            if not math.isfinite(coefficient.real) or not math.isfinite(
                coefficient.imag
            ):
                raise ValueError("dimensionalized hopping coefficients must be finite")
            dimensionalized.extend(
                (
                    (-displacement, coefficient.conjugate()),
                    (displacement, coefficient),
                )
            )
        dimensionalized.sort(key=lambda item: item[0])

        terms = tuple(
            DenseBlockHoppingTerm(
                displacement=LatticeDisplacement(
                    LatticeDimension.ONE,
                    (displacement,),
                ),
                coefficient=ComplexMatrixQuantity(
                    np.asarray([[coefficient]], dtype=np.complex128),
                    energy_unit,
                ),
            )
            for displacement, coefficient in dimensionalized
        )
        return cls(
            geometry=geometry,
            physkit_model=DenseBlockHoppingModel(
                identifier=identifier,
                dimension=LatticeDimension.ONE,
                terms=terms,
                energy_unit=energy_unit,
                energy_reference=energy_reference,
                basis_identifier=basis_identifier,
            ),
        )

    def __post_init__(self) -> None:
        """Validate rank, dimension, geometry, and exact Hermiticity."""
        if type(self.geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("geometry must be Periodic1DLatticeGeometry")
        if type(self.physkit_model) is not DenseBlockHoppingModel:
            raise TypeError(
                "physkit_model must be the exact PhysKit DenseBlockHoppingModel"
            )
        if self.physkit_model.dimension is not LatticeDimension.ONE:
            raise ValueError("physkit_model must have periodic dimension one")
        if self.physkit_model.basis_size != 1:
            raise ValueError("physkit_model must have retained-space dimension one")
        energy_unit = self.physkit_model.energy_unit
        if type(energy_unit) is not PhysicalUnit:
            raise TypeError(
                "physkit_model energy_unit must be a physical energy unit"
            )
        Periodic1DLatticeKineticEnergyScale(
            lattice_geometry=self.geometry,
            energy_unit=energy_unit,
        )

        terms_by_displacement = {
            term.displacement.components: term for term in self.physkit_model.terms
        }
        for displacement, term in terms_by_displacement.items():
            opposite_displacement = (-displacement[0],)
            opposite = terms_by_displacement.get(opposite_displacement)
            if opposite is None:
                raise ValueError(
                    "every hopping displacement must have its conjugate partner"
                )
            expected = np.conjugate(term.coefficient.magnitude.T)
            if not np.array_equal(opposite.coefficient.magnitude, expected):
                raise ValueError(
                    "opposite hopping coefficients must be exact conjugate transposes"
                )

    @property
    def block_hopping_model(self) -> DenseBlockHoppingModel:
        """Return the exact composed PhysKit ordinary-lattice model."""
        return self.physkit_model

    @property
    def lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the explicit physical one-dimensional lattice geometry."""
        return self.geometry

    @property
    def energy_unit(self) -> PhysicalUnit:
        """Return the exact common physical coefficient unit."""
        energy_unit = self.physkit_model.energy_unit
        if type(energy_unit) is not PhysicalUnit:
            raise TypeError("admitted model energy unit must be PhysicalUnit")
        return energy_unit

    @property
    def lattice_kinetic_energy_scale(self) -> ScalarQuantity:
        r"""Return ``hbar^2 / (m_e a^2)`` in the model coefficient unit."""
        return Periodic1DLatticeKineticEnergyScale(
            lattice_geometry=self.geometry,
            energy_unit=self.energy_unit,
        ).energy_scale

    @property
    def model_id(self) -> str:
        """Return an identity binding representation and physical lattice convention."""
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:{self.physkit_model.identifier}:"
            f"period-{self.geometry.lattice_period.hex()}:"
            f"length-unit-{self.geometry.lattice_unit.expression}:"
            f"role-{PeriodicModelRole.REDUCED_MODEL.value}:"
            f"energy-scale-{Periodic1DLatticeKineticEnergyScale.SCALE_IDENTITY}:"
            f"energy-unit-{self.energy_unit.expression}:"
            f"energy-reference-{self.physkit_model.energy_reference}:"
            f"basis-{self.physkit_model.basis_identifier}"
        )

    @property
    def model_role(self) -> PeriodicModelRole:
        """Classify every instance as a parameterized reduced model."""
        return PeriodicModelRole.REDUCED_MODEL

    @property
    def band_subspace_rank(self) -> Literal[1]:
        """Return the exact retained-space dimension one."""
        return 1


__all__ = ["Periodic1DRank1BlochHoppingModel"]
