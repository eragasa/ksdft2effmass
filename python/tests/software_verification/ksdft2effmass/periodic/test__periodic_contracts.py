r"""Software verification of backend-neutral periodic package contract.

Evidence profile: claim_bearing

Bounded artifact scope: public periodic imports, immutable represented geometry,
intrinsic unit and ordering invariants, and package dependency direction.

Facet and represented meaning

The artifact represents finite direct and reciprocal lattices, periodic structures,
and sampled reciprocal-space points with explicit units and conventions.

Intrinsic and cross-object scope

Construction, exact represented state, immutability, direct--reciprocal consistency,
source ordering, and forbidden package dependencies are covered.

VVUQ and scientific exclusions

These tests establish software-contract behavior only. They do not establish DFT
convergence, physical adequacy, scientific validation, or uncertainty quantification.
"""

from __future__ import annotations

import ast
import math
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

import ksdft2effmass.periodic as periodic
from ksdft2effmass.periodic import (
    AtomicSpecies,
    CoordinateConvention,
    DirectLattice,
    InverseLengthUnit,
    KPointSampling,
    KPointWeightNormalization,
    LengthUnit,
    PeriodicSite,
    PeriodicStructure,
    PhysicalDimension,
    ReciprocalLattice,
    ReciprocalLatticeCompatibilityValidator,
    ReciprocalScaleConvention,
    UnitSystem,
)

pytestmark = pytest.mark.software_verification


def make_direct_lattice() -> DirectLattice:
    """Return a cubic two-bohr lattice for caller-owned assertions.

    Evidence ID: Helper owns no identifier.

    Requirement: Support lattice evidence without an independent claim.

    Method: Construct one explicit public record.

    Oracle: Consuming tests own expected values.

    Acceptance: Return the declared immutable record.

    Interpretation: Failure blocks the consuming evidence owners.

    Limitations: This helper establishes no independent evidence.
    """
    return DirectLattice(
        vectors=((2.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 2.0)),
        unit_system=UnitSystem.HARTREE_ATOMIC,
        dimension=PhysicalDimension.LENGTH,
        unit=LengthUnit.BOHR,
        coordinate_convention=CoordinateConvention.CARTESIAN,
        vector_order="source order",
    )


def make_reciprocal_lattice() -> ReciprocalLattice:
    """Return the analytically dual lattice for caller-owned assertions.

    Evidence ID: Helper owns no identifier.

    Requirement: Support reciprocal-lattice evidence without an independent claim.

    Method: Construct one explicit public record dual to ``2 I``.

    Oracle: Consuming tests own the analytic ``pi I`` expectation.

    Acceptance: Return the declared immutable record.

    Interpretation: Failure blocks the consuming evidence owners.

    Limitations: This helper establishes no independent evidence.
    """
    physical = math.pi
    return ReciprocalLattice(
        raw_coefficients=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        raw_dimension=PhysicalDimension.DIMENSIONLESS,
        raw_coordinate_convention=CoordinateConvention.CARTESIAN,
        scale_convention=ReciprocalScaleConvention.TWO_PI_OVER_ALAT,
        scale_alat=2.0,
        scale_alat_unit=LengthUnit.BOHR,
        incorporates_two_pi=True,
        physical_vectors=(
            (physical, 0.0, 0.0),
            (0.0, physical, 0.0),
            (0.0, 0.0, physical),
        ),
        physical_dimension=PhysicalDimension.INVERSE_LENGTH,
        physical_unit=InverseLengthUnit.PER_BOHR,
        physical_coordinate_convention=CoordinateConvention.CARTESIAN,
    )


def test_public_api__package__exports_exact_backend_neutral_surface() -> None:
    """Evidence ID: SV-PERIODIC-024

    Requirement: The periodic package exports only its documented backend-neutral
    enums, immutable geometry records, and lattice-compatibility ActionObject.

    Method: Compare the public export declaration with an independently enumerated
    architecture-owned inventory and inspect each bound name.

    Oracle: The v2 periodic architecture and maintained package documentation.

    Acceptance: ``__all__`` equals the exact inventory and every name is bound.

    Interpretation: Failure exposes an unsupported removal or ownership leak.

    Limitations: Import shape does not establish constructor or scientific behavior.
    """
    expected = {
        "AtomicSpecies",
        "CoordinateConvention",
        "DirectLattice",
        "InverseLengthUnit",
        "KPointSampling",
        "KPointWeightNormalization",
        "LengthUnit",
        "PeriodicSite",
        "PeriodicStructure",
        "PhysicalDimension",
        "ReciprocalLattice",
        "ReciprocalLatticeCompatibilityValidator",
        "ReciprocalScaleConvention",
        "UnitSystem",
    }
    assert set(periodic.__all__) == expected
    assert all(getattr(periodic, name) is not None for name in expected)


def test_constructor__lattices__preserves_units_scale_and_duality() -> None:
    """Evidence ID: SV-PERIODIC-025

    Requirement: Direct and reciprocal records preserve explicit bohr conventions,
    exact ``2*pi/alat`` scaling, and the represented duality relation.

    Method: Construct a hand-derived cubic lattice and inspect public fields.

    Oracle: For ``A = 2 I`` bohr and ``alat = 2`` bohr, ``B = pi I`` bohr^-1
    gives ``A B^T = 2*pi I`` exactly to the declared residual tolerance.

    Acceptance: Construction succeeds and all public unit and vector fields equal
    the independently specified values.

    Interpretation: Failure indicates represented-unit, scaling, or duality drift.

    Limitations: One analytic cubic case does not verify arbitrary physical models.
    """
    direct = make_direct_lattice()
    reciprocal = make_reciprocal_lattice()
    ReciprocalLatticeCompatibilityValidator().execute(
        direct, reciprocal, absolute_tolerance=1.0e-14
    )
    assert direct.vectors == (
        (2.0, 0.0, 0.0),
        (0.0, 2.0, 0.0),
        (0.0, 0.0, 2.0),
    )
    assert direct.unit_system is UnitSystem.HARTREE_ATOMIC
    assert direct.dimension is PhysicalDimension.LENGTH
    assert direct.unit is LengthUnit.BOHR
    assert direct.coordinate_convention is CoordinateConvention.CARTESIAN
    assert reciprocal.raw_coefficients[0] == (1.0, 0.0, 0.0)
    assert reciprocal.physical_vectors[1] == (0.0, math.pi, 0.0)
    assert reciprocal.physical_dimension is PhysicalDimension.INVERSE_LENGTH
    assert reciprocal.physical_unit is InverseLengthUnit.PER_BOHR
    assert reciprocal.scale_convention is ReciprocalScaleConvention.TWO_PI_OVER_ALAT


def test_method__execute__rejects_incompatible_lattice_pair() -> None:
    """Evidence ID: SV-PERIODIC-032

    Requirement: Direct--reciprocal compatibility and its tolerance belong to the
    public validator rather than either immutable lattice record.

    Method: Validate a reciprocal lattice against an independently represented
    direct lattice with one incompatible axis length.

    Oracle: A first-axis product of ``3*pi`` differs from the required ``2*pi`` by
    ``pi``, exceeding the explicit ``1e-14`` componentwise tolerance.

    Acceptance: Each lattice constructs independently and validator execution raises
    ``ValueError`` for their incompatible relation.

    Interpretation: Failure indicates missing ActionObject-owned compatibility policy.

    Limitations: Rejection does not establish physical adequacy of either lattice.
    """
    incompatible_direct = DirectLattice(
        vectors=((3.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 2.0)),
        unit_system=UnitSystem.HARTREE_ATOMIC,
        dimension=PhysicalDimension.LENGTH,
        unit=LengthUnit.BOHR,
        coordinate_convention=CoordinateConvention.CARTESIAN,
        vector_order="source order",
    )
    reciprocal = make_reciprocal_lattice()
    validator = ReciprocalLatticeCompatibilityValidator()
    with pytest.raises(ValueError, match="inconsistent"):
        validator.execute(
            incompatible_direct,
            reciprocal,
            absolute_tolerance=1.0e-14,
        )
    with pytest.raises(TypeError):
        validator.execute(
            incompatible_direct,
            reciprocal,
            absolute_tolerance=True,
        )


def test_constructor__structure__preserves_species_and_site_source_order() -> None:
    """Evidence ID: SV-PERIODIC-026

    Requirement: A structure retains unique species and contiguous one-based sites
    with resolvable species references in source order.

    Method: Construct a two-site single-species structure and inspect exact fields.

    Oracle: The explicitly listed species inventory and one-based source sequence.

    Acceptance: Construction succeeds and ordered species, indices, coordinates,
    and references equal the declared inputs.

    Interpretation: Failure indicates structure ordering or reference-contract drift.

    Limitations: This is structural software verification, not geometry validation.
    """
    species = AtomicSpecies(
        "Si", 28.085, PhysicalDimension.MASS, "unified_atomic_mass_unit", "Si.upf"
    )
    sites = (
        PeriodicSite(
            1,
            "Si",
            (0.0, 0.0, 0.0),
            CoordinateConvention.CARTESIAN,
            PhysicalDimension.LENGTH,
            LengthUnit.BOHR,
        ),
        PeriodicSite(
            2,
            "Si",
            (1.0, 1.0, 1.0),
            CoordinateConvention.CARTESIAN,
            PhysicalDimension.LENGTH,
            LengthUnit.BOHR,
        ),
    )
    structure = PeriodicStructure(make_direct_lattice(), (species,), sites)
    assert structure.species == (species,)
    assert tuple(site.index for site in structure.sites) == (1, 2)
    assert structure.sites[1].species_name == "Si"
    assert structure.sites[1].coordinates == (1.0, 1.0, 1.0)
    assert structure.direct_lattice == make_direct_lattice()


def test_constructor__k_points__preserves_scale_weights_and_normalization() -> None:
    """Evidence ID: SV-PERIODIC-027

    Requirement: K-point records retain ordered raw and physical coordinates,
    explicit reciprocal scale, finite weights, and declared normalization.

    Method: Construct two analytically scaled points whose weights sum to two.

    Oracle: Direct multiplication by ``2*pi/alat`` for ``alat = 2`` bohr and the
    exact declared weight sum.

    Acceptance: Construction succeeds and public coordinates and weights equal the
    independently listed values.

    Interpretation: Failure indicates k-point scale or normalization drift.

    Limitations: Sampling adequacy and Brillouin-zone convergence are excluded.
    """
    sampling = KPointSampling(
        raw_coordinates=((0.0, 0.0, 0.0), (0.5, 0.0, 0.0)),
        raw_dimension=PhysicalDimension.DIMENSIONLESS,
        coordinate_convention=CoordinateConvention.CARTESIAN,
        scale_convention=ReciprocalScaleConvention.TWO_PI_OVER_ALAT,
        scale_alat=2.0,
        scale_alat_unit=LengthUnit.BOHR,
        incorporates_two_pi=True,
        physical_coordinates=((0.0, 0.0, 0.0), (0.5 * math.pi, 0.0, 0.0)),
        physical_dimension=PhysicalDimension.INVERSE_LENGTH,
        physical_unit=InverseLengthUnit.PER_BOHR,
        weights=(1.0, 1.0),
        weight_normalization=KPointWeightNormalization.SUM_TO_TWO,
    )
    assert sampling.raw_coordinates == ((0.0, 0.0, 0.0), (0.5, 0.0, 0.0))
    assert sampling.physical_coordinates[1] == (0.5 * math.pi, 0.0, 0.0)
    assert sampling.scale_alat == 2.0
    assert sampling.scale_alat_unit is LengthUnit.BOHR
    assert sampling.physical_unit is InverseLengthUnit.PER_BOHR
    assert sampling.weights == (1.0, 1.0)
    assert sampling.weight_normalization is KPointWeightNormalization.SUM_TO_TWO


def test_constructor__numeric_inputs__rejects_invalid_scalar_values() -> None:
    """Evidence ID: SV-PERIODIC-028

    Requirement: Public periodic numeric fields accept only their documented
    built-in scalar types and reject booleans, numeric strings, and nonfinite values.

    Method: Replace one valid field at a time with a wrong semantic type or value.

    Oracle: Python's exact built-in scalar types and ``math.isfinite`` semantics.

    Acceptance: Wrong semantic types raise ``TypeError`` and nonfinite built-in
    floats raise ``ValueError``.

    Interpretation: Failure indicates numeric-boundary or exception-taxonomy drift.

    Limitations: Overflow during external parsing belongs to the integration owner.
    """
    with pytest.raises(TypeError):
        DirectLattice(
            ((True, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 2.0)),
            UnitSystem.HARTREE_ATOMIC,
            PhysicalDimension.LENGTH,
            LengthUnit.BOHR,
            CoordinateConvention.CARTESIAN,
            "source order",
        )
    with pytest.raises(TypeError):
        PeriodicSite(
            True,
            "Si",
            (0.0, 0.0, 0.0),
            CoordinateConvention.CARTESIAN,
            PhysicalDimension.LENGTH,
            LengthUnit.BOHR,
        )
    with pytest.raises(TypeError):
        AtomicSpecies(
            "Si",
            "28.085",  # type: ignore[arg-type]
            PhysicalDimension.MASS,
            "unified_atomic_mass_unit",
            "Si.upf",
        )
    with pytest.raises(ValueError):
        DirectLattice(
            ((math.inf, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 2.0)),
            UnitSystem.HARTREE_ATOMIC,
            PhysicalDimension.LENGTH,
            LengthUnit.BOHR,
            CoordinateConvention.CARTESIAN,
            "source order",
        )
    with pytest.raises(TypeError):
        replace(make_direct_lattice(), vector_order=1)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        replace(make_reciprocal_lattice(), scale_alat="2.0")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        replace(make_reciprocal_lattice(), scale_alat=math.nan)


def test_constructor__aggregate_members__rejects_wrong_semantic_types() -> None:
    """Evidence ID: SV-PERIODIC-029

    Requirement: Structure aggregates reject wrong member types at their public
    boundary rather than leaking attribute-access failures.

    Method: Supply a string in each nominal aggregate member position.

    Oracle: The documented ``DirectLattice``, ``AtomicSpecies``, and ``PeriodicSite``
    field types and project exception taxonomy.

    Acceptance: Each wrong semantic type raises ``TypeError``.

    Interpretation: Failure indicates an incomplete aggregate type boundary.

    Limitations: Valid cross-object scientific compatibility is not established.
    """
    species = AtomicSpecies(
        "Si", 28.085, PhysicalDimension.MASS, "unified_atomic_mass_unit", "Si.upf"
    )
    site = PeriodicSite(
        1,
        "Si",
        (0.0, 0.0, 0.0),
        CoordinateConvention.CARTESIAN,
        PhysicalDimension.LENGTH,
        LengthUnit.BOHR,
    )
    with pytest.raises(TypeError):
        PeriodicStructure(make_direct_lattice(), ("Si",), (site,))  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        PeriodicStructure(make_direct_lattice(), (species,), ("site",))  # type: ignore[arg-type]


def test_method__setattr__records_are_immutable() -> None:
    """Evidence ID: SV-PERIODIC-030

    Requirement: Public periodic records are operationally immutable through their
    ordinary field API.

    Method: Attempt to replace a field on a constructed frozen slotted record.

    Oracle: Python frozen-dataclass assignment semantics.

    Acceptance: Assignment raises ``FrozenInstanceError`` and state is unchanged.

    Interpretation: Failure indicates mutation exposure at the represented-state API.

    Limitations: This does not assess hostile reflection or interpreter internals.
    """
    lattice = make_direct_lattice()
    with pytest.raises(FrozenInstanceError):
        lattice.vector_order = "changed"  # type: ignore[misc]
    assert lattice.vector_order == "source order"


def test_artifact__dependency__periodic_imports_no_consumer_package() -> None:
    """Evidence ID: SV-PERIODIC-031

    Requirement: The periodic owner must not depend on calculator, integration,
    Kohn--Sham, workflow, or analysis consumers.

    Method: Parse every periodic source module and inspect absolute import targets.

    Oracle: The forbidden dependency edge in the normative v2 periodic architecture.

    Acceptance: No import begins with a forbidden project package prefix.

    Interpretation: Failure indicates inversion of the backend-neutral owner boundary.

    Limitations: Dynamic imports outside ordinary syntax are not represented here.
    """
    package_root = Path(periodic.__file__).resolve().parent
    forbidden = (
        "ksdft2effmass.analysis",
        "ksdft2effmass.calculators",
        "ksdft2effmass.integration",
        "ksdft2effmass.io",
        "ksdft2effmass.ksdft",
        "ksdft2effmass.workflows",
    )
    source_paths = package_root.rglob("*.py")
    trees = tuple(
        ast.parse(path.read_text(encoding="utf-8")) for path in source_paths
    )
    nodes = tuple(node for tree in trees for node in ast.walk(tree))
    direct_imports = {
        alias.name
        for node in nodes
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    from_imports = {
        node.module
        for node in nodes
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert not any(name.startswith(forbidden) for name in direct_imports | from_imports)
