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
    UnitSystem,
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
    """Bind an ordinary-lattice rank-one PhysKit hopping representation.

    Parameters
    ----------
    geometry : Periodic1DLatticeGeometry
        Physical primitive-period convention for the one-dimensional lattice.
    unit_system : UnitSystem
        Physical coherent unit system used to dimensionalize normalized coefficients.
    physkit_model : DenseBlockHoppingModel
        Canonical ordinary-lattice model with the unit system's energy unit and exact
        ``1 x 1`` dense coefficient blocks.

    Raises
    ------
    TypeError
        If either field lacks its exact nominal owner or the model energy unit is not
        physical.
    ValueError
        If the model is not one-dimensional, does not have retained dimension one, or
        lacks exact conjugate displacement support.

    Notes
    -----
    ``band_subspace_rank`` is the retained-space dimension, not the algebraic rank of
    a coefficient matrix. Every displacement must have its exact conjugate partner,
    including an exactly Hermitian onsite block.

    Complete finite-DFT cyclic coefficients are not admitted by this contract. They
    must remain in a cyclic representation until an explicit conversion establishes
    an ordinary-lattice hopping model.
    """

    MODEL_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic1d-rank1-bloch-hopping-model.v1"
    )

    geometry: Periodic1DLatticeGeometry
    unit_system: UnitSystem
    physkit_model: DenseBlockHoppingModel

    @classmethod
    def from_lattice_kinetic_parameters(
        cls,
        *,
        identifier: str,
        geometry: Periodic1DLatticeGeometry,
        unit_system: UnitSystem,
        energy_reference: str,
        basis_identifier: str,
        normalized_onsite: float,
        normalized_positive_hoppings: tuple[tuple[int, float | complex], ...],
    ) -> Self:
        r"""Construct a physical model from coefficients normalized by ``E_a``.

        Parameters
        ----------
        identifier : str
            Nonempty identity for the resulting PhysKit hopping model.
        geometry : Periodic1DLatticeGeometry
            Physical primitive period used in ``E_a = hbar^2 / (m_e a^2)``.
        unit_system : UnitSystem
            Physical coherent unit system for length, mass, action, and energy.
        energy_reference : str
            Nonempty identity for the common coefficient energy zero.
        basis_identifier : str
            Nonempty identity for the retained rank-one basis.
        normalized_onsite : float
            Finite onsite coefficient expressed as a ratio to ``E_a``.
        normalized_positive_hoppings : tuple[tuple[int, float | complex], ...]
            Strictly increasing positive displacements and finite ratios to ``E_a``.

        Returns
        -------
        Self
            Immutable rank-one model with canonical conjugate displacement support.

        Raises
        ------
        TypeError
            If geometry, units, containers, displacements, or ratios lack their exact
            admitted nominal scalar types.
        ValueError
            If ratios are nonfinite, displacements are not positive and strictly
            increasing, or dimensionalization overflows binary64.

        Notes
        -----
        ``normalized_onsite`` and every hopping ratio are multiplied by ``E_a`` in
        ``unit_system.energy_unit``. The constructor generates each negative
        displacement coefficient as the exact complex conjugate of its positive
        partner. Boolean values, integer ratios, numeric strings, and implicit unit
        conversions are not admitted.
        """
        if type(geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("geometry must be Periodic1DLatticeGeometry")
        if type(unit_system) is not UnitSystem:
            raise TypeError("unit_system must be UnitSystem")
        if unit_system is UnitSystem.NONDIMENSIONAL:
            raise ValueError("unit_system must be physical")
        energy_unit = unit_system.energy_unit
        if type(energy_unit) is not PhysicalUnit:
            raise TypeError("physical unit systems must own a PhysicalUnit energy")
        if type(normalized_onsite) is not float:
            raise TypeError("normalized_onsite must be a built-in float")
        if not math.isfinite(normalized_onsite):
            raise ValueError("normalized_onsite must be finite")
        if type(normalized_positive_hoppings) is not tuple:
            raise TypeError("normalized_positive_hoppings must be an exact tuple")

        # Validate the complete normalized inventory before dimensionalization so a
        # partially admitted model can never escape after a later invalid entry.
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

        # One coherent UnitSystem supplies hbar, electron-mass, length, and energy
        # units; KSD adds only the declared lattice period and no-half scale convention.
        energy_scale = Periodic1DLatticeKineticEnergyScale(
            lattice_geometry=geometry,
            unit_system=unit_system,
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
            # Negative support is generated rather than independently rounded, which
            # preserves exact rank-one Hermiticity in the stored binary64 inventory.
            dimensionalized.extend(
                (
                    (-displacement, coefficient.conjugate()),
                    (displacement, coefficient),
                )
            )
        dimensionalized.sort(key=lambda item: item[0])

        # Rank-one blocks remain nominally dense 1 x 1 matrices; scalar shortcuts would
        # bypass the uniform PhysKit block-hopping contract used by higher ranks.
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
            unit_system=unit_system,
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
        if type(self.unit_system) is not UnitSystem:
            raise TypeError("unit_system must be UnitSystem")
        if self.unit_system is UnitSystem.NONDIMENSIONAL:
            raise ValueError("unit_system must be physical")
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
        if energy_unit != self.unit_system.energy_unit:
            raise ValueError(
                "physkit_model energy_unit must match unit_system.energy_unit"
            )
        Periodic1DLatticeKineticEnergyScale(
            lattice_geometry=self.geometry,
            unit_system=self.unit_system,
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
        """Return the composed ordinary-lattice hopping model.

        Returns
        -------
        DenseBlockHoppingModel
            Exact immutable PhysKit model retained by this owner.
        """
        return self.physkit_model

    @property
    def lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the physical one-dimensional lattice geometry.

        Returns
        -------
        Periodic1DLatticeGeometry
            Exact primitive-period convention retained by this model.
        """
        return self.geometry

    @property
    def energy_unit(self) -> PhysicalUnit:
        """Return the common physical coefficient unit.

        Returns
        -------
        PhysicalUnit
            Exact energy unit shared by all hopping blocks.
        """
        energy_unit = self.physkit_model.energy_unit
        if type(energy_unit) is not PhysicalUnit:
            raise TypeError("admitted model energy unit must be PhysicalUnit")
        return energy_unit

    @property
    def lattice_kinetic_energy_scale(self) -> ScalarQuantity:
        r"""Return ``hbar^2 / (m_e a^2)``.

        Returns
        -------
        ScalarQuantity
            Lattice kinetic-energy scale in the model coefficient unit.
        """
        return Periodic1DLatticeKineticEnergyScale(
            lattice_geometry=self.geometry,
            unit_system=self.unit_system,
        ).energy_scale

    @property
    def model_id(self) -> str:
        """Return the complete model identity.

        Returns
        -------
        str
            Stable identity binding representation, geometry, role, units, energy
            reference, and retained basis.
        """
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:{self.physkit_model.identifier}:"
            f"period-{self.geometry.lattice_period.hex()}:"
            f"length-unit-{self.geometry.lattice_unit.expression}:"
            f"role-{PeriodicModelRole.REDUCED_MODEL.value}:"
            f"energy-scale-{Periodic1DLatticeKineticEnergyScale.SCALE_IDENTITY}:"
            f"unit-system-{self.unit_system.value}:"
            f"energy-unit-{self.energy_unit.expression}:"
            f"energy-reference-{self.physkit_model.energy_reference}:"
            f"basis-{self.physkit_model.basis_identifier}"
        )

    @property
    def model_role(self) -> PeriodicModelRole:
        """Return the scientific model role.

        Returns
        -------
        PeriodicModelRole
            ``REDUCED_MODEL`` without implying fitting or scientific validation.
        """
        return PeriodicModelRole.REDUCED_MODEL

    @property
    def band_subspace_rank(self) -> Literal[1]:
        """Return the retained-space dimension.

        Returns
        -------
        Literal[1]
            Exact retained basis size one.
        """
        return 1


__all__ = ["Periodic1DRank1BlochHoppingModel"]
