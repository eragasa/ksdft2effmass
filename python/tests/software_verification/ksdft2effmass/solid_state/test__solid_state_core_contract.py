r"""Software verification of solid-state core contract.

Evidence profile: routine

Bounded artifact scope: public one-, two-, and three-dimensional direct, reciprocal,
Bravais, finite-lattice, boundary-twist, scalar-hopping, localized-perturbation, and
integral-operation contracts.

Facet and represented meaning

The artifact under test is the cohesive initial ``ksdft2effmass.solid_state`` public
surface and its exact cross-object dimensional behavior.

Intrinsic and cross-object scope

Closed dimension validation, all Bravais system--centering combinations,
direct--reciprocal duality, last-axis-fastest indexing, periodic wrapping, twist
reduction and enumeration, deterministic model inventories, and lattice-operation
compatibility are included.

VVUQ and scientific exclusions

This is software verification of represented contracts. It does not verify a finite
Hamiltonian constructor, reproduce an accepted calculation, establish numerical or
scientific validation, quantify uncertainty, or provide human acceptance.
"""

import pytest

import ksdft2effmass.solid_state as solid_state
from ksdft2effmass.operators import PhysicalUnit, Unitless
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    BoundaryTwistMesh,
    BoundaryTwistMeshEnumerator,
    BoundaryTwistReducer,
    BoundaryTwistTransformer,
    BravaisCentering,
    BravaisLattice1D,
    BravaisLattice2D,
    BravaisLattice3D,
    DirectLattice1D,
    DirectLattice2D,
    DirectLattice3D,
    FiniteLatticeCoordinateResolver,
    FiniteLatticeIndexer,
    FiniteLatticeShape,
    IntegralLatticeOperation,
    Lattice1D,
    Lattice2D,
    Lattice3D,
    LatticeCoordinate,
    LatticeCoordinateTransformer,
    LatticeDimension,
    LatticeDisplacement,
    LatticeDualityAnalyzer,
    LatticeOperationCompatibilityAuditor,
    LatticeSystem1D,
    LatticeSystem2D,
    LatticeSystem3D,
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    PeriodicImageResolver,
    ReciprocalLattice1D,
    ReciprocalLattice2D,
    ReciprocalLattice3D,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)

pytestmark = pytest.mark.software_verification


class TestSolidStateCoreContract:
    """Own software evidence for the initial public solid-state artifact."""

    def test_public_api__package__exports_initial_contract(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-001

        Requirement: The package exposes the accepted initial solid-state records and
        actions through one supported public import surface.

        Acceptance: Every required public name is present and no underscore-prefixed
        name is declared in ``__all__``.
        """
        required = {
            "BoundaryTwistLift",
            "BoundaryTwistMesh",
            "BoundaryTwistReducer",
            "BravaisCentering",
            "BravaisLattice3D",
            "DirectLattice3D",
            "FiniteLatticeIndexer",
            "FiniteLatticeShape",
            "IntegralLatticeOperation",
            "Lattice3D",
            "LatticeCoordinate",
            "LatticeDimension",
            "LatticeDisplacement",
            "LocalizedPerturbation",
            "ReciprocalLattice3D",
            "ScalarHoppingModel",
        }

        assert required <= set(solid_state.__all__)
        assert not any(name.startswith("_") for name in solid_state.__all__)

    def test_artifact__geometry__indexes_all_supported_dimensions(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-002

        Requirement: Finite lattice indexing is closed over one, two, and three
        dimensions with the last axis varying fastest.

        Acceptance: Hand-derived terminal indices are 3, 5, and 23, and inverse
        resolution recovers the exact coordinates.
        """
        indexer = FiniteLatticeIndexer()
        resolver = FiniteLatticeCoordinateResolver()
        one = FiniteLatticeShape(LatticeDimension.ONE, (4,))
        two = FiniteLatticeShape(LatticeDimension.TWO, (2, 3))
        three = FiniteLatticeShape(LatticeDimension.THREE, (2, 3, 4))

        assert indexer.execute(one, LatticeCoordinate(LatticeDimension.ONE, (3,))) == 3
        assert (
            indexer.execute(two, LatticeCoordinate(LatticeDimension.TWO, (1, 2))) == 5
        )
        assert (
            indexer.execute(three, LatticeCoordinate(LatticeDimension.THREE, (1, 2, 3)))
            == 23
        )
        assert resolver.execute(three, 23).components == (1, 2, 3)

    def test_artifact__periodic_image__retains_negative_crossing_quotients(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-003

        Requirement: Periodic wrapping uses Euclidean division and retains one
        boundary-crossing quotient per axis.

        Acceptance: The 3D coordinate ``(-1, 7, -9)`` in shape ``(4, 5, 6)`` wraps to
        ``(3, 2, 3)`` with quotient ``(-1, 1, -2)``.
        """
        result = PeriodicImageResolver().execute(
            FiniteLatticeShape(LatticeDimension.THREE, (4, 5, 6)),
            LatticeCoordinate(LatticeDimension.THREE, (-1, 7, -9)),
        )

        assert result.coordinate.components == (3, 2, 3)
        assert result.quotient.components == (-1, 1, -2)

    def test_artifact__boundary_twist__separates_lift_reduction_and_mesh_order(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-004

        Requirement: Twist lifts retain unreduced values, reduction records integer
        quotients, and tensor-product enumeration varies the last axis fastest.

        Acceptance: ``(0.25, -0.25)`` reduces to ``(0.25, 0.75)`` with quotient
        ``(0, -1)``, while a ``2 by 3`` mesh begins ``(0,0)``, ``(0,1/3)``,
        ``(0,2/3)``, ``(1/2,0)``.
        """
        reduced = BoundaryTwistReducer().execute(
            BoundaryTwistLift(LatticeDimension.TWO, (0.25, -0.25))
        )
        points = BoundaryTwistMeshEnumerator().execute(
            BoundaryTwistMesh(LatticeDimension.TWO, (2, 3))
        )

        assert reduced.representative.turns == (0.25, 0.75)
        assert reduced.quotient.components == (0, -1)
        assert tuple(point.turns for point in points[:4]) == (
            (0.0, 0.0),
            (0.0, 1.0 / 3.0),
            (0.0, 2.0 / 3.0),
            (0.5, 0.0),
        )

    def test_artifact__lattice_models__retain_deterministic_scalar_terms(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-005

        Requirement: Scalar parent and localized perturbation records retain explicit
        dimension, units, energy reference, basis identity, and canonical term order.

        Acceptance: A 2D Hermitian hopping inventory and onsite-then-bond perturbation
        construct with exact values; a duplicate hopping displacement is rejected.
        """
        negative = ScalarHoppingTerm(
            LatticeDisplacement(LatticeDimension.TWO, (-1, 0)), -1.0, 0.0
        )
        positive = ScalarHoppingTerm(
            LatticeDisplacement(LatticeDimension.TWO, (1, 0)), -1.0, 0.0
        )
        parent = ScalarHoppingModel(
            "parent",
            LatticeDimension.TWO,
            (negative, positive),
            Unitless(),
            "parent_zero",
            "scalar_cell_basis",
        )
        onsite = LocalizedOnsiteTerm(
            LatticeCoordinate(LatticeDimension.TWO, (0, 0)), 0.2, 0.0
        )
        bond = LocalizedBondTerm(
            LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
            LatticeDisplacement(LatticeDimension.TWO, (1, 1)),
            0.05,
            0.0,
        )
        perturbation = LocalizedPerturbation(
            "defect",
            LatticeDimension.TWO,
            (onsite, bond),
            Unitless(),
            "parent_zero",
            "scalar_cell_basis",
        )

        assert tuple(term.value for term in parent.terms) == (-1.0 + 0.0j,) * 2
        assert tuple(term.value for term in perturbation.terms) == (
            0.2 + 0.0j,
            0.05 + 0.0j,
        )
        with pytest.raises(ValueError, match="sorted and unique"):
            ScalarHoppingModel(
                "duplicate",
                LatticeDimension.TWO,
                (negative, negative),
                Unitless(),
                "parent_zero",
                "scalar_cell_basis",
            )

    def test_artifact__lattice_operation__transforms_3d_values_and_audits_shapes(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-006

        Requirement: Integral operations transform coordinates and twists in the
        declared dimension, while finite-shape compatibility is explicit.

        Acceptance: A 3D axis cycle maps ``(1,2,3)`` and ``(0.1,0.2,0.3)`` to
        ``(2,3,1)`` and ``(0.2,0.3,0.1)``, maps shape ``(2,3,4)`` to ``(3,4,2)``,
        and rejects an unchanged target shape by extent mismatch.
        """
        operation = IntegralLatticeOperation(
            "axis_cycle",
            LatticeDimension.THREE,
            ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
        )
        coordinate = LatticeCoordinateTransformer().execute(
            operation, LatticeCoordinate(LatticeDimension.THREE, (1, 2, 3))
        )
        twist = BoundaryTwistTransformer().execute(
            operation, BoundaryTwistLift(LatticeDimension.THREE, (0.1, 0.2, 0.3))
        )
        auditor = LatticeOperationCompatibilityAuditor()
        source = FiniteLatticeShape(LatticeDimension.THREE, (2, 3, 4))

        assert coordinate.components == (2, 3, 1)
        assert twist.turns == (0.2, 0.3, 0.1)
        assert auditor.execute(
            source,
            FiniteLatticeShape(LatticeDimension.THREE, (3, 4, 2)),
            operation,
        ).compatible
        mismatch = auditor.execute(source, source, operation)
        assert mismatch.issue_codes == (
            "SOLID_STATE.LATTICE_OPERATION.EXTENT_MISMATCH",
        )

    def test_artifact__closed_dimensions__rejects_boolean_and_length_laundering(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-007

        Requirement: Public dimensioned records reject Boolean integers and coordinate
        tuples whose lengths do not match the declared one-, two-, or three-axis domain.

        Acceptance: Boolean extent and one-component coordinate for a 2D declaration
        each raise the documented semantic error class.
        """
        with pytest.raises(TypeError, match="built-in integers"):
            FiniteLatticeShape(LatticeDimension.ONE, (True,))
        with pytest.raises(ValueError, match="count must match dimension"):
            LatticeCoordinate(LatticeDimension.TWO, (1,))

    def test_artifact__bravais_classification__covers_all_dimension_combinations(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-008

        Requirement: Factored lattice-system and P/C/I/F/R centering records represent
        the unique 1D, five 2D, and fourteen 3D Bravais classifications while rejecting
        prohibited combinations.

        Acceptance: The standard 1 + 5 + 14 combinations construct exactly and square
        C, tetragonal F, and rhombohedral P are rejected.
        """
        one = (BravaisLattice1D(LatticeSystem1D.LINE, BravaisCentering.P),)
        two = tuple(
            BravaisLattice2D(system, centering)
            for system, centering in (
                (LatticeSystem2D.OBLIQUE, BravaisCentering.P),
                (LatticeSystem2D.RECTANGULAR, BravaisCentering.P),
                (LatticeSystem2D.RECTANGULAR, BravaisCentering.C),
                (LatticeSystem2D.SQUARE, BravaisCentering.P),
                (LatticeSystem2D.HEXAGONAL, BravaisCentering.P),
            )
        )
        three = tuple(
            BravaisLattice3D(system, centering)
            for system, centering in (
                (LatticeSystem3D.TRICLINIC, BravaisCentering.P),
                (LatticeSystem3D.MONOCLINIC, BravaisCentering.P),
                (LatticeSystem3D.MONOCLINIC, BravaisCentering.C),
                (LatticeSystem3D.ORTHORHOMBIC, BravaisCentering.P),
                (LatticeSystem3D.ORTHORHOMBIC, BravaisCentering.C),
                (LatticeSystem3D.ORTHORHOMBIC, BravaisCentering.I),
                (LatticeSystem3D.ORTHORHOMBIC, BravaisCentering.F),
                (LatticeSystem3D.TETRAGONAL, BravaisCentering.P),
                (LatticeSystem3D.TETRAGONAL, BravaisCentering.I),
                (LatticeSystem3D.RHOMBOHEDRAL, BravaisCentering.R),
                (LatticeSystem3D.HEXAGONAL, BravaisCentering.P),
                (LatticeSystem3D.CUBIC, BravaisCentering.P),
                (LatticeSystem3D.CUBIC, BravaisCentering.I),
                (LatticeSystem3D.CUBIC, BravaisCentering.F),
            )
        )

        assert len(one) == 1
        assert len(two) == 5
        assert len(three) == 14
        with pytest.raises(ValueError, match="two-dimensional"):
            BravaisLattice2D(LatticeSystem2D.SQUARE, BravaisCentering.C)
        with pytest.raises(ValueError, match="three-dimensional"):
            BravaisLattice3D(LatticeSystem3D.TETRAGONAL, BravaisCentering.F)
        with pytest.raises(ValueError, match="three-dimensional"):
            BravaisLattice3D(LatticeSystem3D.RHOMBOHEDRAL, BravaisCentering.P)

    def test_artifact__direct_reciprocal_lattices__analyzes_two_pi_duality(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-009

        Requirement: Dimension-specific direct and reciprocal records retain physical
        units and a caller-toleranced analyzer checks ``A B^T = 2*pi*I``.

        Acceptance: Hand-derived orthogonal 1D, 2D, and 3D unit bases with reciprocal
        magnitude ``2*pi`` pass at ``1e-14``; a mismatched 1D reciprocal value fails.
        """
        length = PhysicalUnit("bohr")
        inverse_length = PhysicalUnit("1 / bohr")
        two_pi = 6.283185307179586
        analyzer = LatticeDualityAnalyzer()
        one = analyzer.execute(
            DirectLattice1D((1.0,), length),
            ReciprocalLattice1D((two_pi,), inverse_length),
            absolute_tolerance=1.0e-14,
        )
        two = analyzer.execute(
            DirectLattice2D(((1.0, 0.0), (0.0, 1.0)), length),
            ReciprocalLattice2D(((two_pi, 0.0), (0.0, two_pi)), inverse_length),
            absolute_tolerance=1.0e-14,
        )
        three = analyzer.execute(
            DirectLattice3D(
                ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
                length,
            ),
            ReciprocalLattice3D(
                (
                    (two_pi, 0.0, 0.0),
                    (0.0, two_pi, 0.0),
                    (0.0, 0.0, two_pi),
                ),
                inverse_length,
            ),
            absolute_tolerance=1.0e-14,
        )
        mismatch = analyzer.execute(
            DirectLattice1D((1.0,), length),
            ReciprocalLattice1D((1.0,), inverse_length),
            absolute_tolerance=1.0e-14,
        )

        assert one.compatible and one.maximum_absolute_residual == 0.0
        assert two.compatible and two.maximum_absolute_residual == 0.0
        assert three.compatible and three.maximum_absolute_residual == 0.0
        assert mismatch.issue_codes == (
            "SOLID_STATE.LATTICE_DUALITY.RESIDUAL_EXCEEDED",
        )

    def test_artifact__lattice_composition__retains_dimension_specific_records(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-010

        Requirement: Lattice1D, Lattice2D, and Lattice3D compose only matching direct,
        reciprocal, and dimension-specific Bravais records without claiming that
        construction itself proves duality.

        Acceptance: Exact 1D, square-P 2D, and cubic-P 3D compositions retain their
        component identities.
        """
        length = PhysicalUnit("bohr")
        inverse_length = PhysicalUnit("1 / bohr")
        two_pi = 6.283185307179586
        one = Lattice1D(
            DirectLattice1D((1.0,), length),
            ReciprocalLattice1D((two_pi,), inverse_length),
            BravaisLattice1D(LatticeSystem1D.LINE, BravaisCentering.P),
        )
        two = Lattice2D(
            DirectLattice2D(((1.0, 0.0), (0.0, 1.0)), length),
            ReciprocalLattice2D(((two_pi, 0.0), (0.0, two_pi)), inverse_length),
            BravaisLattice2D(LatticeSystem2D.SQUARE, BravaisCentering.P),
        )
        three = Lattice3D(
            DirectLattice3D(
                ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
                length,
            ),
            ReciprocalLattice3D(
                (
                    (two_pi, 0.0, 0.0),
                    (0.0, two_pi, 0.0),
                    (0.0, 0.0, two_pi),
                ),
                inverse_length,
            ),
            BravaisLattice3D(LatticeSystem3D.CUBIC, BravaisCentering.P),
        )

        assert one.bravais.centering is BravaisCentering.P
        assert two.bravais.system is LatticeSystem2D.SQUARE
        assert three.bravais.system is LatticeSystem3D.CUBIC
