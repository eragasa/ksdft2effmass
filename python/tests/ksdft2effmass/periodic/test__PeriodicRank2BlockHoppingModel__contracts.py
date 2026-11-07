"""Contracts for periodic rank-two block-hopping scientific models."""

from __future__ import annotations

from dataclasses import replace
from importlib import import_module

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice1D,
    DirectLattice2D,
    DirectLattice3D,
)
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
    Unitless,
)

from ksdft2effmass.periodic.catalog import PeriodicControlModelCatalog
from ksdft2effmass.periodic.models import (
    PeriodicModelRole,
    PeriodicRank2BlockHoppingModel,
)
from ksdft2effmass.periodic.periodic1d.rank2.models import (
    Periodic1DRank2BlockHoppingModel,
)
from ksdft2effmass.periodic.periodic2d.rank2.models import (
    Periodic2DRank2BlockHoppingModel,
)
from ksdft2effmass.periodic.periodic3d.rank2.models import (
    Periodic3DRank2BlockHoppingModel,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic2d.geometry import Periodic2DLatticeGeometry
from ksdft2effmass.periodic3d.geometry import Periodic3DLatticeGeometry
from ksdft2effmass.solidstate.hopping_transforms import BlockHoppingModel1D

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodicRank2BlockHoppingModel:
    """Establish inheritance, dimensional, rank, and Hermiticity contracts."""

    @staticmethod
    def _representation(dimension: LatticeDimension) -> DenseBlockHoppingModel:
        """Construct a minimal exactly Hermitian rank-two hopping kernel.

        Parameters
        ----------
        dimension
            Ordinary-lattice dimension used by every displacement index.

        Returns
        -------
        DenseBlockHoppingModel
            Three-term kernel containing one onsite block and one conjugate pair.

        Notes
        -----
        The displacement tuples are dimensionless integer coefficients. Their physical
        translations are determined only after the representation is composed with a
        dimensional lattice geometry.

        """
        displacement: tuple[int] | tuple[int, int] | tuple[int, int, int]
        negative_displacement: tuple[int] | tuple[int, int] | tuple[int, int, int]
        zero_displacement: tuple[int] | tuple[int, int] | tuple[int, int, int]
        if dimension is LatticeDimension.ONE:
            displacement = (1,)
            negative_displacement = (-1,)
            zero_displacement = (0,)
        elif dimension is LatticeDimension.TWO:
            displacement = (1, 0)
            negative_displacement = (-1, 0)
            zero_displacement = (0, 0)
        elif dimension is LatticeDimension.THREE:
            displacement = (1, 0, 0)
            negative_displacement = (-1, 0, 0)
            zero_displacement = (0, 0, 0)
        else:
            raise ValueError("test representation dimension must be one, two, or three")
        # Use a genuinely complex, non-Hermitian positive-displacement block so the
        # negative-displacement term must be its conjugate transpose rather than a
        # coincidentally equal copy.
        positive = np.array(
            ((0.2 + 0.0j, 0.1 - 0.03j), (0.0 + 0.04j, -0.1 + 0.0j)),
            dtype=np.complex128,
        )
        # The zero-displacement coefficient is the primitive-cell onsite operator and
        # must be Hermitian by itself because zero is its own additive inverse.
        onsite = np.array(
            ((-0.8 + 0.0j, 0.05 - 0.02j), (0.05 + 0.02j, 0.6 + 0.0j)),
            dtype=np.complex128,
        )
        terms = (
            DenseBlockHoppingTerm(
                displacement=LatticeDisplacement(
                    dimension,
                    negative_displacement,
                ),
                coefficient=ComplexMatrixQuantity(positive.conjugate().T, Unitless()),
            ),
            DenseBlockHoppingTerm(
                displacement=LatticeDisplacement(
                    dimension,
                    zero_displacement,
                ),
                coefficient=ComplexMatrixQuantity(onsite, Unitless()),
            ),
            DenseBlockHoppingTerm(
                displacement=LatticeDisplacement(dimension, displacement),
                coefficient=ComplexMatrixQuantity(positive, Unitless()),
            ),
        )
        return DenseBlockHoppingModel(
            identifier=f"rank2-{int(dimension)}d-representation",
            dimension=dimension,
            terms=terms,
            energy_unit=Unitless(),
            energy_reference="dimensionless-zero-v1",
            basis_identifier="retained-rank2-basis-v1",
        )

    @staticmethod
    def _model_1d() -> Periodic1DRank2BlockHoppingModel:
        """Construct the one-dimensional member of the comparison family.

        Returns
        -------
        Periodic1DRank2BlockHoppingModel
            Unit-bearing rank-two control model with a one-bohr primitive period.

        """
        return Periodic1DRank2BlockHoppingModel(
            identifier="periodic1d-rank2-block-model-v1",
            role=PeriodicModelRole.CONTROL_MODEL,
            geometry=Periodic1DLatticeGeometry(
                lattice_period=1.0,
                lattice_unit=PhysicalUnit("bohr"),
            ),
            representation=TestPeriodicRank2BlockHoppingModel._representation(
                LatticeDimension.ONE
            ),
        )

    @staticmethod
    def _model_2d() -> Periodic2DRank2BlockHoppingModel:
        """Construct the two-dimensional member of the comparison family.

        Returns
        -------
        Periodic2DRank2BlockHoppingModel
            Unit-bearing model on an ordered nonorthogonal direct basis in bohr.

        """
        return Periodic2DRank2BlockHoppingModel(
            identifier="periodic2d-rank2-block-model-v1",
            role=PeriodicModelRole.CONTROL_MODEL,
            geometry=Periodic2DLatticeGeometry.from_direct_lattice(
                DirectLattice2D(
                    a1=np.array((2.0, 0.0), dtype=np.float64),
                    a2=np.array((0.5, 3.0), dtype=np.float64),
                ),
                PhysicalUnit("bohr"),
            ),
            representation=TestPeriodicRank2BlockHoppingModel._representation(
                LatticeDimension.TWO
            ),
        )

    @staticmethod
    def _model_3d() -> Periodic3DRank2BlockHoppingModel:
        """Construct the three-dimensional member of the comparison family.

        Returns
        -------
        Periodic3DRank2BlockHoppingModel
            Unit-bearing model on an ordered nonorthogonal direct basis in bohr.

        """
        return Periodic3DRank2BlockHoppingModel(
            identifier="periodic3d-rank2-block-model-v1",
            role=PeriodicModelRole.CONTROL_MODEL,
            geometry=Periodic3DLatticeGeometry.from_direct_lattice(
                DirectLattice3D(
                    a1=np.array((2.0, 0.0, 0.0), dtype=np.float64),
                    a2=np.array((0.5, 3.0, 0.0), dtype=np.float64),
                    a3=np.array((0.25, -0.5, 4.0), dtype=np.float64),
                ),
                PhysicalUnit("bohr"),
            ),
            representation=TestPeriodicRank2BlockHoppingModel._representation(
                LatticeDimension.THREE
            ),
        )

    def test__dimensional_models__inherit_the_shared_rank_two_parent(self) -> None:
        """Keep rank identity shared while geometry remains dimension specific.

        Notes
        -----
        This test distinguishes retained state-space rank from spatial dimension. All
        three models have ``2 x 2`` coefficient blocks, but their integer displacement
        tuples and primitive-basis matrices have one, two, and three components.

        """
        model_1d = self._model_1d()
        model_2d = self._model_2d()
        model_3d = self._model_3d()

        # Rank two is enforced by one inherited scientific-model contract rather than
        # repeated as three unrelated dimensional conventions.
        assert Periodic1DRank2BlockHoppingModel.__bases__ == (
            PeriodicRank2BlockHoppingModel,
        )
        assert Periodic2DRank2BlockHoppingModel.__bases__ == (
            PeriodicRank2BlockHoppingModel,
        )
        assert Periodic3DRank2BlockHoppingModel.__bases__ == (
            PeriodicRank2BlockHoppingModel,
        )
        assert isinstance(model_1d, PeriodicRank2BlockHoppingModel)
        assert isinstance(model_2d, PeriodicRank2BlockHoppingModel)
        assert isinstance(model_3d, PeriodicRank2BlockHoppingModel)
        # Each model reconstructs the exact provider lattice from immutable geometry;
        # the physical length unit remains owned by the KSD geometry value.
        assert type(model_1d.direct_lattice) is DirectLattice1D
        assert type(model_2d.direct_lattice) is DirectLattice2D
        assert type(model_3d.direct_lattice) is DirectLattice3D
        assert model_1d.lattice_geometry.lattice_unit == PhysicalUnit("bohr")
        assert model_2d.lattice_geometry.lattice_unit == PhysicalUnit("bohr")
        assert model_3d.lattice_geometry.lattice_unit == PhysicalUnit("bohr")
        assert model_1d.band_subspace_rank == 2
        assert model_2d.band_subspace_rank == 2
        assert model_3d.band_subspace_rank == 2
        assert model_1d.spatial_dimension == 1
        assert model_2d.spatial_dimension == 2
        assert model_3d.spatial_dimension == 3

    def test__dimensional_models__preserve_coordinate_maps_and_units(self) -> None:
        """Map integer coefficients through ordered basis columns as ``R_n = A n``.

        Notes
        -----
        The nonorthogonal fixtures make an accidental row-vector convention observable.
        A transposed primitive-basis matrix would produce different physical
        displacements even though it contains the same scalar entries.

        """
        model_1d = self._model_1d()
        model_2d = self._model_2d()
        model_3d = self._model_3d()

        displacement_1d = model_1d.lattice_geometry.direct_translation(
            LatticeDisplacement(LatticeDimension.ONE, (2,))
        )
        displacement_2d = model_2d.lattice_geometry.direct_translation(
            LatticeDisplacement(LatticeDimension.TWO, (1, -2))
        )
        displacement_3d = model_3d.lattice_geometry.direct_translation(
            LatticeDisplacement(LatticeDimension.THREE, (1, -2, 3))
        )

        assert displacement_1d.magnitude == 2.0
        np.testing.assert_array_equal(
            displacement_2d.magnitude,
            np.array((1.0, -6.0), dtype=np.float64),
        )
        np.testing.assert_array_equal(
            displacement_3d.magnitude,
            np.array((1.75, -7.5, 12.0), dtype=np.float64),
        )
        assert displacement_1d.unit == PhysicalUnit("bohr")
        assert displacement_2d.unit == PhysicalUnit("bohr")
        assert displacement_3d.unit == PhysicalUnit("bohr")

    def test__legacy_ordinary_representation__composes_with_the_current_1d_model(
        self,
    ) -> None:
        """Correlate the maintained representation with the approved model hierarchy.

        Notes
        -----
        Representation conversion preserves the legacy coefficient inventory. The
        existing scientific-model constructor separately supplies geometry and role and
        enforces exact rank-two Hermiticity. No adapter class or alternate model is
        introduced.

        """
        unit = Unitless()
        positive = np.array(
            ((0.25 + 0.0j, 0.1 - 0.05j), (0.02 + 0.03j, -0.2 + 0.0j)),
            dtype=np.complex128,
        )
        onsite = np.array(
            ((-0.5 + 0.0j, 0.04 - 0.01j), (0.04 + 0.01j, 0.7 + 0.0j)),
            dtype=np.complex128,
        )
        source = BlockHoppingModel1D(
            reciprocal_period=ScalarQuantity(1.0, unit),
            representatives=(-1, 0, 1),
            hopping_blocks=(
                ComplexMatrixQuantity(positive.conjugate().T, unit),
                ComplexMatrixQuantity(onsite, unit),
                ComplexMatrixQuantity(positive, unit),
            ),
        )

        representation = source.to_physkit_ordinary_representation(
            identifier="legacy-ordinary-rank2-v1",
            energy_reference="dimensionless-zero-v1",
            basis_identifier="ordered-rank2-basis-v1",
        )
        model = Periodic1DRank2BlockHoppingModel(
            identifier="periodic1d-rank2-from-legacy-v1",
            role=PeriodicModelRole.CONTROL_MODEL,
            geometry=Periodic1DLatticeGeometry(
                lattice_period=2.0,
                lattice_unit=PhysicalUnit("bohr"),
            ),
            representation=representation,
        )

        assert model.block_hopping_model is representation
        assert model.lattice_geometry.lattice_period == 2.0
        assert model.band_subspace_rank == 2
        assert tuple(term.displacement.components for term in representation.terms) == (
            (-1,),
            (0,),
            (1,),
        )
        assert source.reciprocal_period.magnitude == 1.0

    def test__dimensional_models__are_admitted_by_the_control_catalog(self) -> None:
        """Admit the dimensional family without implying scientific validation."""
        model_1d = self._model_1d()
        model_2d = self._model_2d()
        model_3d = self._model_3d()

        catalog = PeriodicControlModelCatalog(models=(model_1d, model_2d, model_3d))

        assert catalog.model_ids == (
            model_1d.model_id,
            model_2d.model_id,
            model_3d.model_id,
        )
        assert catalog.spatial_dimensions == (1, 2, 3)

    def test__retired_model_namespaces__have_no_aliases(self) -> None:
        """Prevent duplicate import paths from creating competing model identities."""
        retired_namespaces = (
            "ksdft2effmass.models.periodic",
            "ksdft2effmass.periodic1d.models",
            "ksdft2effmass.periodic1d.rank2.models",
            "ksdft2effmass.periodic1d.rankN.models",
            "ksdft2effmass.periodic2d.models",
            "ksdft2effmass.periodic2d.rank2.models",
            "ksdft2effmass.periodic2d.rankN.models",
            "ksdft2effmass.periodic3d.models",
            "ksdft2effmass.periodic3d.rank2.models",
            "ksdft2effmass.periodic3d.rankN.models",
        )

        for namespace in retired_namespaces:
            with pytest.raises(ModuleNotFoundError):
                import_module(namespace)

    def test__periodic1d_model__requires_exact_physical_geometry(self) -> None:
        """Reject a bare provider lattice that omits the physical length unit."""
        model = self._model_1d()

        with pytest.raises(TypeError, match="Periodic1DLatticeGeometry"):
            replace(
                model,
                geometry=DirectLattice1D(1.0),  # type: ignore[arg-type]
            )

    def test__periodic2d_and_3d_models__require_exact_physical_geometry(self) -> None:
        """Reject metrics that discard ordered basis and unit ownership.

        Notes
        -----
        A Gram metric records intrinsic lengths and angles, but it is not the complete
        coordinate map ``r = A s`` and does not carry the declared length unit.

        """
        model_2d = self._model_2d()
        model_3d = self._model_3d()

        with pytest.raises(TypeError, match="Periodic2DLatticeGeometry"):
            replace(
                model_2d,
                geometry=model_2d.direct_metric,  # type: ignore[arg-type]
            )
        with pytest.raises(TypeError, match="Periodic3DLatticeGeometry"):
            replace(
                model_3d,
                geometry=model_3d.direct_metric,  # type: ignore[arg-type]
            )

    def test__dimensional_model__rejects_a_provider_dimension_mismatch(self) -> None:
        """Reject a kernel whose integer-index dimension differs from its geometry."""
        model = self._model_1d()

        with pytest.raises(ValueError, match="dimension must match"):
            replace(
                model,
                representation=self._representation(LatticeDimension.TWO),
            )

    def test__dimensional_model__rejects_nonhermitian_support(self) -> None:
        """Reject a coefficient pair that violates exact lattice Hermiticity.

        Notes
        -----
        Scientific-model admission requires ``T(-n) = T(n)^dagger`` exactly. A
        tolerance-bearing Fourier reconstruction remains a representation until a
        separate model-construction policy resolves its numerical residual.

        """
        representation = self._representation(LatticeDimension.THREE)
        model = replace(self._model_3d(), representation=representation)
        positive_term = representation.terms[-1]
        # Perturb only the positive-displacement block. Its retained negative partner
        # is then no longer the required conjugate transpose.
        invalid_positive = DenseBlockHoppingTerm(
            displacement=positive_term.displacement,
            coefficient=ComplexMatrixQuantity(
                positive_term.coefficient.magnitude
                + np.array(((0.0, 0.1j), (0.0, 0.0)), dtype=np.complex128),
                Unitless(),
            ),
        )
        invalid_representation = replace(
            representation,
            terms=(*representation.terms[:-1], invalid_positive),
        )

        with pytest.raises(ValueError, match="conjugate transposes"):
            replace(model, representation=invalid_representation)
