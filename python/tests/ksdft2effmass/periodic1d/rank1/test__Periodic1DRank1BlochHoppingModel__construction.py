"""Contracts for the periodic-1D retained-dimension-one hopping model."""

from dataclasses import FrozenInstanceError
from typing import TypedDict

import numpy as np
import pytest
from numpy.typing import NDArray
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
    ModelSystemQuantity,
    ModelSystemUnitConverter,
    PhysicalUnit,
    Unitless,
    UnitSystem,
)

from ksdft2effmass.model.blochhopping import BlochHoppingModel
from ksdft2effmass.periodic import Periodic1DModel, PeriodicModelRole
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.model.blochhopping import Periodic1DBlochHoppingModel
from ksdft2effmass.periodic1d.rank1.model.blochhopping import (
    Periodic1DRank1BlochHoppingModel,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]

type TestDisplacement = tuple[int] | tuple[int, int] | tuple[int, int, int]


class _LatticeKineticParameterArguments(TypedDict):
    identifier: str
    geometry: Periodic1DLatticeGeometry
    unit_system: UnitSystem
    energy_reference: str
    basis_identifier: str


class TestPeriodic1DRank1BlochHoppingModel:
    """Establish rank, geometry, ordinary-support, and Hermiticity boundaries."""

    @staticmethod
    def _term(
        displacement: TestDisplacement,
        value: NDArray[np.complex128],
        dimension: LatticeDimension,
        energy_unit: PhysicalUnit | Unitless,
    ) -> DenseBlockHoppingTerm:
        """Construct one exact dense hopping term for a controlled model."""
        return DenseBlockHoppingTerm(
            displacement=LatticeDisplacement(dimension, displacement),
            coefficient=ComplexMatrixQuantity(value, energy_unit),
        )

    @classmethod
    def _physkit_model(
        cls,
        *,
        dimension: LatticeDimension = LatticeDimension.ONE,
        blocks: tuple[tuple[TestDisplacement, complex], ...] = (
            ((-1,), 0.25 - 0.5j),
            ((0,), 1.0 + 0.0j),
            ((1,), 0.25 + 0.5j),
        ),
        basis_size: int = 1,
        energy_unit: PhysicalUnit | Unitless | None = None,
    ) -> DenseBlockHoppingModel:
        """Construct a controlled PhysKit model with caller-selected boundaries."""
        selected_energy_unit = (
            PhysicalUnit("electron_volt") if energy_unit is None else energy_unit
        )
        terms = tuple(
            cls._term(
                displacement,
                np.eye(basis_size, dtype=np.complex128) * value,
                dimension,
                selected_energy_unit,
            )
            for displacement, value in blocks
        )
        return DenseBlockHoppingModel(
            identifier="controlled-rank1-ordinary-hopping-v1",
            dimension=dimension,
            terms=terms,
            energy_unit=selected_energy_unit,
            energy_reference="controlled-zero-v1",
            basis_identifier="controlled-scalar-cell-basis-v1",
        )

    @classmethod
    def _model(cls) -> Periodic1DRank1BlochHoppingModel:
        """Return the valid rank-one model reused by ownership tests."""
        return Periodic1DRank1BlochHoppingModel(
            geometry=Periodic1DLatticeGeometry(
                2.0,
                PhysicalUnit("angstrom"),
            ),
            unit_system=UnitSystem.METAL,
            physkit_model=cls._physkit_model(),
        )

    @staticmethod
    def _kinetic_arguments() -> _LatticeKineticParameterArguments:
        """Return common arguments for normalized kinetic-scale construction."""
        return {
            "identifier": "reduced-rank1-from-ea-v1",
            "geometry": Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            "unit_system": UnitSystem.ATOMIC,
            "energy_reference": "controlled-zero-v1",
            "basis_identifier": "controlled-scalar-cell-basis-v1",
        }

    @staticmethod
    def _kinetic_model() -> Periodic1DRank1BlochHoppingModel:
        """Return a finite-support model constructed from normalized coefficients."""
        return Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
            identifier="reduced-rank1-from-ea-v1",
            geometry=Periodic1DLatticeGeometry(2.0, PhysicalUnit("angstrom")),
            unit_system=UnitSystem.METAL,
            energy_reference="controlled-zero-v1",
            basis_identifier="controlled-scalar-cell-basis-v1",
            normalized_onsite=1.5,
            normalized_positive_hoppings=(
                (1, -0.25 + 0.5j),
                (2, 0.125),
            ),
        )

    def test__Periodic1DRank1BlochHoppingModel__owns_rank_one_hierarchy(self) -> None:
        """Occupy each declared domain layer while remaining concretely rank one."""
        model = self._model()

        assert (
            isinstance(model, BlochHoppingModel),
            isinstance(model, Periodic1DBlochHoppingModel),
            isinstance(model, Periodic1DModel),
            model.spatial_dimension,
            model.band_subspace_rank,
            model.model_role,
        ) == (True, True, True, 1, 1, PeriodicModelRole.REDUCED_MODEL)

    def test__Periodic1DRank1BlochHoppingModel__retains_physkit_metadata(self) -> None:
        """Retain exact PhysKit identity, rank, unit, reference, and basis metadata."""
        model = self._model()

        # These fields jointly identify the represented operator and retained basis.
        assert (
            model.block_hopping_model is model.physkit_model,
            model.block_hopping_model.dimension,
            model.block_hopping_model.basis_size,
            model.unit_system,
            model.energy_unit,
            model.block_hopping_model.energy_unit is model.energy_unit,
            model.block_hopping_model.energy_reference,
            model.block_hopping_model.basis_identifier,
        ) == (
            True,
            LatticeDimension.ONE,
            1,
            UnitSystem.METAL,
            PhysicalUnit("electron_volt"),
            True,
            "controlled-zero-v1",
            "controlled-scalar-cell-basis-v1",
        )

    def test__Periodic1DRank1BlochHoppingModel__binds_identity_conventions(
        self,
    ) -> None:
        """Bind role, geometry, scale, unit, and reference into model identity."""
        model = self._model()
        required_tokens = (
            "role-reduced_model",
            "period-0x1.0000000000000p+1",
            "length-unit-angstrom",
            "lattice-kinetic-energy-scale.hbar2-over-me-a2.v1",
            "unit-system-metal",
            "energy-unit-electron_volt",
            "energy-reference-controlled-zero-v1",
        )

        assert model.model_id.startswith(
            "ksdft2effmass.periodic1d-rank1-bloch-hopping-model.v1:"
        )
        assert all(token in model.model_id for token in required_tokens)

    def test__Periodic1DRank1BlochHoppingModel__retains_positive_energy_scale(
        self,
    ) -> None:
        """Retain a positive lattice kinetic-energy scale in the model energy unit."""
        model = self._model()

        assert (
            model.lattice_geometry.lattice_period,
            model.lattice_kinetic_energy_scale.unit,
            model.lattice_kinetic_energy_scale.magnitude > 0.0,
        ) == (2.0, PhysicalUnit("electron_volt"), True)

    def test__Periodic1DRank1BlochHoppingModel__keeps_coefficients_immutable(
        self,
    ) -> None:
        """Expose coefficient arrays as operationally immutable values."""
        coefficient = self._model().block_hopping_model.terms[0].coefficient

        assert not coefficient.magnitude.flags.writeable

    def test__Periodic1DRank1BlochHoppingModel__keeps_record_frozen(self) -> None:
        """Reject mutation of the retained lattice geometry."""
        model = self._model()

        with pytest.raises(FrozenInstanceError):
            model.geometry = Periodic1DLatticeGeometry(  # type: ignore[misc]
                1.0,
                PhysicalUnit("bohr"),
            )

    def test__Periodic1DRank1BlochHoppingModel__kinetic_factory_orders_support(
        self,
    ) -> None:
        """Expand positive normalized hoppings into sorted conjugate support."""
        terms = {
            term.displacement.components[0]: term
            for term in self._kinetic_model().block_hopping_model.terms
        }

        assert tuple(terms) == (-2, -1, 0, 1, 2)

    def test__Periodic1DRank1BlochHoppingModel__kinetic_factory_owns_quantities(
        self,
    ) -> None:
        """Represent every dimensionalized coefficient with the PhysKit quantity."""
        terms = self._kinetic_model().block_hopping_model.terms

        assert all(
            type(term.coefficient) is ComplexMatrixQuantity
            and isinstance(term.coefficient, ModelSystemQuantity)
            for term in terms
        )

    def test__Periodic1DRank1BlochHoppingModel__kinetic_factory_scales_values(
        self,
    ) -> None:
        """Scale normalized onsite and hopping coefficients by the declared E_a."""
        model = self._kinetic_model()
        scale = model.lattice_kinetic_energy_scale.magnitude
        terms = {
            term.displacement.components[0]: term
            for term in model.block_hopping_model.terms
        }

        # One ordered vector comparison covers onsite, conjugate pairing, and range.
        actual = np.asarray(
            [terms[index].coefficient.magnitude[0, 0] for index in terms],
            dtype=np.complex128,
        )
        expected = scale * np.asarray(
            [
                0.125,
                -0.25 - 0.5j,
                1.5,
                -0.25 + 0.5j,
                0.125,
            ],
            dtype=np.complex128,
        )
        np.testing.assert_allclose(actual, expected, rtol=1.0e-15, atol=0.0)

    def test__Periodic1DRank1BlochHoppingModel__kinetic_factory_retains_unit(
        self,
    ) -> None:
        """Assign one exact physical energy unit to every generated coefficient."""
        terms = self._kinetic_model().block_hopping_model.terms

        assert tuple(term.coefficient.unit for term in terms) == (
            PhysicalUnit("electron_volt"),
        ) * len(terms)

    def test__Periodic1DRank1BlochHoppingModel__kinetic_factory_freezes_values(
        self,
    ) -> None:
        """Freeze arrays created from normalized kinetic-scale coefficients."""
        coefficient = self._kinetic_model().block_hopping_model.terms[1].coefficient

        assert not coefficient.magnitude.flags.writeable

    def test__Periodic1DRank1BlochHoppingModel__factory_rejects_foreign_unit_system(
        self,
    ) -> None:
        """Reject strings rather than coercing them to unit-system members."""
        arguments = self._kinetic_arguments()
        arguments["unit_system"] = "atomic"  # type: ignore[typeddict-item]

        with pytest.raises(TypeError, match="UnitSystem"):
            Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
                **arguments,
                normalized_onsite=0.0,
                normalized_positive_hoppings=(),
            )

    def test__Periodic1DRank1BlochHoppingModel__factory_rejects_unitless_system(
        self,
    ) -> None:
        """Reject the nondimensional control system at the physical model boundary."""
        arguments = self._kinetic_arguments()
        arguments["unit_system"] = UnitSystem.NONDIMENSIONAL

        with pytest.raises(ValueError, match="must be physical"):
            Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
                **arguments,
                normalized_onsite=0.0,
                normalized_positive_hoppings=(),
            )

    def test__Periodic1DRank1BlochHoppingModel__onsite_rejects_boolean(self) -> None:
        """Reject booleans as normalized onsite scalars."""
        with pytest.raises(TypeError, match="normalized_onsite"):
            Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
                **self._kinetic_arguments(),
                normalized_onsite=True,
                normalized_positive_hoppings=(),
            )

    def test__Periodic1DRank1BlochHoppingModel__onsite_rejects_nonfinite(self) -> None:
        """Reject nonfinite normalized onsite values."""
        with pytest.raises(ValueError, match="normalized_onsite"):
            Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
                **self._kinetic_arguments(),
                normalized_onsite=float("nan"),
                normalized_positive_hoppings=(),
            )

    def test__Periodic1DRank1BlochHoppingModel__hoppings_require_tuple(self) -> None:
        """Reject mutable normalized hopping inventories."""
        with pytest.raises(TypeError, match="exact tuple"):
            Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
                **self._kinetic_arguments(),
                normalized_onsite=0.0,
                normalized_positive_hoppings=[  # type: ignore[arg-type]
                    (1, 0.5)
                ],
            )

    def test__Periodic1DRank1BlochHoppingModel__hoppings_require_order(self) -> None:
        """Reject duplicate or nonincreasing positive displacements."""
        with pytest.raises(ValueError, match="positive and strictly increasing"):
            Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
                **self._kinetic_arguments(),
                normalized_onsite=0.0,
                normalized_positive_hoppings=((1, 0.5), (1, 0.25)),
            )

    def test__Periodic1DRank1BlochHoppingModel__hoppings_reject_integer_ratio(
        self,
    ) -> None:
        """Reject integer coefficient ratios rather than coercing them silently."""
        with pytest.raises(TypeError, match="float or complex"):
            Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
                **self._kinetic_arguments(),
                normalized_onsite=0.0,
                normalized_positive_hoppings=((1, 1),),
            )

    def test__Periodic1DRank1BlochHoppingModel__hoppings_reject_nonfinite(
        self,
    ) -> None:
        """Reject nonfinite complex hopping ratios."""
        with pytest.raises(ValueError, match="ratios must be finite"):
            Periodic1DRank1BlochHoppingModel.from_lattice_kinetic_parameters(
                **self._kinetic_arguments(),
                normalized_onsite=0.0,
                normalized_positive_hoppings=((1, complex(float("inf"), 0.0)),),
            )

    def test__Periodic1DRank1BlochHoppingModel__dimension_rejects_non_one(
        self,
    ) -> None:
        """Reject PhysKit hopping models outside periodic dimension one."""
        physkit_model = self._physkit_model(
            dimension=LatticeDimension.TWO,
            blocks=(
                ((-1, 0), 0.25 + 0.0j),
                ((0, 0), 1.0 + 0.0j),
                ((1, 0), 0.25 + 0.0j),
            ),
        )

        with pytest.raises(ValueError, match="periodic dimension one"):
            Periodic1DRank1BlochHoppingModel(
                geometry=Periodic1DLatticeGeometry(
                    1.0,
                    PhysicalUnit("bohr"),
                ),
                unit_system=UnitSystem.METAL,
                physkit_model=physkit_model,
            )

    def test__Periodic1DRank1BlochHoppingModel__rank_rejects_larger_block(
        self,
    ) -> None:
        """Reject retained coefficient blocks larger than one by one."""
        with pytest.raises(ValueError, match="retained-space dimension one"):
            Periodic1DRank1BlochHoppingModel(
                geometry=Periodic1DLatticeGeometry(
                    1.0,
                    PhysicalUnit("bohr"),
                ),
                unit_system=UnitSystem.METAL,
                physkit_model=self._physkit_model(basis_size=2),
            )

    @pytest.mark.parametrize(
        "blocks, message",
        (
            (
                (
                    ((0,), 1.0 + 0.0j),
                    ((1,), 0.25 + 0.5j),
                ),
                "conjugate partner",
            ),
            (
                (
                    ((-1,), 0.25 + 0.5j),
                    ((0,), 1.0 + 0.0j),
                    ((1,), 0.25 + 0.5j),
                ),
                "conjugate transposes",
            ),
            (
                (((0,), 1.0 + 0.25j),),
                "conjugate transposes",
            ),
        ),
    )
    def test__Periodic1DRank1BlochHoppingModel__hermiticity_rejects_invalid_support(
        self,
        blocks: tuple[tuple[TestDisplacement, complex], ...],
        message: str,
    ) -> None:
        """Reject missing, mismatched, or non-Hermitian conjugate support."""
        with pytest.raises(ValueError, match=message):
            Periodic1DRank1BlochHoppingModel(
                geometry=Periodic1DLatticeGeometry(
                    1.0,
                    PhysicalUnit("bohr"),
                ),
                unit_system=UnitSystem.METAL,
                physkit_model=self._physkit_model(blocks=blocks),
            )

    def test__Periodic1DRank1BlochHoppingModel__energy_unit_accepts_physical(
        self,
    ) -> None:
        """Accept a PhysKit model expressed in a physical energy unit."""
        model = Periodic1DRank1BlochHoppingModel(
            geometry=Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            unit_system=UnitSystem.METAL,
            physkit_model=self._physkit_model(),
        )

        assert model.energy_unit == PhysicalUnit("electron_volt")

    def test__Periodic1DRank1BlochHoppingModel__energy_unit_rejects_unitless(
        self,
    ) -> None:
        """Reject dimensionless Hamiltonian coefficients."""
        with pytest.raises(TypeError, match="physical energy unit"):
            Periodic1DRank1BlochHoppingModel(
                geometry=Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
                unit_system=UnitSystem.METAL,
                physkit_model=self._physkit_model(energy_unit=Unitless()),
            )

    def test__Periodic1DRank1BlochHoppingModel__rejects_unit_system_mismatch(
        self,
    ) -> None:
        """Reject a model unit that differs from the selected coherent system."""
        with pytest.raises(ValueError, match="match unit_system"):
            Periodic1DRank1BlochHoppingModel(
                geometry=Periodic1DLatticeGeometry(
                    1.0,
                    PhysicalUnit("angstrom"),
                ),
                unit_system=UnitSystem.METAL,
                physkit_model=self._physkit_model(energy_unit=PhysicalUnit("meter")),
            )

    def test__Periodic1DRank1BlochHoppingModel__conversion_retains_geometry(
        self,
    ) -> None:
        """Change energy representation explicitly while retaining geometry identity."""
        source = self._physkit_model()
        target_unit = PhysicalUnit("joule")
        converted_terms = tuple(
            DenseBlockHoppingTerm(
                displacement=term.displacement,
                coefficient=ModelSystemUnitConverter.convert_complex_matrix(
                    term.coefficient,
                    target_unit,
                ),
            )
            for term in source.terms
        )
        converted = DenseBlockHoppingModel(
            identifier=f"{source.identifier}-joule",
            dimension=source.dimension,
            terms=converted_terms,
            energy_unit=target_unit,
            energy_reference=source.energy_reference,
            basis_identifier=source.basis_identifier,
        )
        geometry = Periodic1DLatticeGeometry(2.0, PhysicalUnit("angstrom"))
        source_model = Periodic1DRank1BlochHoppingModel(
            geometry=geometry,
            unit_system=UnitSystem.METAL,
            physkit_model=source,
        )
        converted_model = Periodic1DRank1BlochHoppingModel(
            geometry=geometry,
            unit_system=UnitSystem.SI,
            physkit_model=converted,
        )

        assert (
            converted_model.energy_unit,
            converted_model.lattice_geometry is source_model.lattice_geometry,
            converted_model.model_id != source_model.model_id,
        ) == (target_unit, True, True)

    def test__Periodic1DRank1BlochHoppingModel__conversion_scales_coefficient(
        self,
    ) -> None:
        """Apply the explicit electron-volt to joule conversion to coefficients."""
        source = self._physkit_model()
        converted = ModelSystemUnitConverter.convert_complex_matrix(
            source.terms[-1].coefficient,
            PhysicalUnit("joule"),
        )

        assert converted.magnitude[0, 0].real == pytest.approx(
            source.terms[-1].coefficient.magnitude[0, 0].real * 1.602176634e-19,
            rel=1.0e-15,
            abs=0.0,
        )

    def test__Periodic1DRank1BlochHoppingModel__units_reject_mixed_model(
        self,
    ) -> None:
        """Reject a PhysKit model whose coefficient and model units differ."""
        term = self._term(
            (0,),
            np.asarray([[1.0 + 0.0j]], dtype=np.complex128),
            LatticeDimension.ONE,
            PhysicalUnit("electron_volt"),
        )

        with pytest.raises(ValueError, match="units must match"):
            DenseBlockHoppingModel(
                identifier="mixed-unit-model",
                dimension=LatticeDimension.ONE,
                terms=(term,),
                energy_unit=PhysicalUnit("joule"),
                energy_reference="controlled-zero-v1",
                basis_identifier="controlled-scalar-cell-basis-v1",
            )

    def test__Periodic1DRank1BlochHoppingModel__types_require_domain_geometry(
        self,
    ) -> None:
        """Reject a direct lattice in place of the periodic-1D geometry owner."""
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(TypeError, match="geometry"):
            Periodic1DRank1BlochHoppingModel(
                geometry=geometry.direct_lattice,  # type: ignore[arg-type]
                unit_system=UnitSystem.METAL,
                physkit_model=self._physkit_model(),
            )
