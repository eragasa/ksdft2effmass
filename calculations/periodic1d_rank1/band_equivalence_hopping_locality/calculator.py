"""Calculation-owned composition of maintained periodic-1D rank-one capabilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from ksdft2effmass.periodic1d.fourier_locality.result import (
    Periodic1DFourierLocalityCalculationResult,
    Periodic1DFourierLocalityMeshResult,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.rank1.alignment.analysis import (
    Periodic1DRank1AlignmentApplicabilityAnalyzer,
)
from ksdft2effmass.periodic1d.rank1.alignment.result import (
    Periodic1DRank1AlignmentApplicabilityResult,
)
from ksdft2effmass.periodic1d.rank1.hopping_locality.analysis import (
    Periodic1DRank1HoppingLocalityAnalysis,
    Periodic1DRank1HoppingLocalityAnalysisRequest,
    Periodic1DRank1HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rank1.support_truncation.analysis import (
    Periodic1DRank1SupportTruncationAnalysis,
    Periodic1DRank1SupportTruncationAnalysisRequest,
    Periodic1DRank1SupportTruncationAnalyzer,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1dRank1CalculationResult:
    """Correlate one Fourier-locality result with its rank-one capability views.

    Parameters
    ----------
    source_calculation : Periodic1DFourierLocalityCalculationResult
        Exact typed Fourier-locality calculation being projected. The source object
        remains the rank-one band-equivalence analysis and retains all native result
        values.
    lattice_geometry : Periodic1DLatticeGeometry
        Explicit direct-lattice period and physical length unit selected by the caller.
        This value is new correlation metadata and does not reinterpret historical
        dimensionless result bytes.
    production_mesh : Periodic1DFourierLocalityMeshResult
        Exact source mesh whose construction size equals the configuration's declared
        production construction size.
    alignment : Periodic1DRank1AlignmentApplicabilityResult
        Operator-trivial ``U(1)`` alignment disposition for the source configuration.
    hopping_locality : Periodic1DRank1HoppingLocalityAnalysis
        Descriptive complete-coefficient and omitted-tail projection for every stored
        range on the production mesh.
    support_truncation : Periodic1DRank1SupportTruncationAnalysis
        Deliberate support-removal consequences for every stored production-mesh range.

    Notes
    -----
    This aggregate is an in-memory calculation composition. It introduces no wire,
    writes no artifact, and does not alter the retained predecessor execution. The
    source calculation, alignment, locality, and truncation values remain owned by
    their maintained installed packages.
    """

    source_calculation: Periodic1DFourierLocalityCalculationResult
    lattice_geometry: Periodic1DLatticeGeometry
    production_mesh: Periodic1DFourierLocalityMeshResult
    alignment: Periodic1DRank1AlignmentApplicabilityResult
    hopping_locality: Periodic1DRank1HoppingLocalityAnalysis
    support_truncation: Periodic1DRank1SupportTruncationAnalysis

    def __post_init__(self) -> None:
        """Validate exact owner types and shared source-object correlation.

        Raises
        ------
        TypeError
            If any field is not owned by its exact maintained rank-one type.
        ValueError
            If the production mesh is not the exact declared source mesh, or if any
            capability projection is correlated with another source calculation,
            source mesh, configuration, or lattice geometry.
        """
        if type(self.source_calculation) is not (
            Periodic1DFourierLocalityCalculationResult
        ):
            raise TypeError(
                "source_calculation must be Periodic1DFourierLocalityCalculationResult"
            )
        if type(self.lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")
        if type(self.production_mesh) is not Periodic1DFourierLocalityMeshResult:
            raise TypeError(
                "production_mesh must be Periodic1DFourierLocalityMeshResult"
            )
        if type(self.alignment) is not Periodic1DRank1AlignmentApplicabilityResult:
            raise TypeError(
                "alignment must be Periodic1DRank1AlignmentApplicabilityResult"
            )
        if type(self.hopping_locality) is not Periodic1DRank1HoppingLocalityAnalysis:
            raise TypeError(
                "hopping_locality must be Periodic1DRank1HoppingLocalityAnalysis"
            )
        if type(self.support_truncation) is not (
            Periodic1DRank1SupportTruncationAnalysis
        ):
            raise TypeError(
                "support_truncation must be Periodic1DRank1SupportTruncationAnalysis"
            )

        # The selected production mesh must be one exact member of the source result,
        # not a structurally equal reconstruction from another calculation.
        if not any(
            mesh is self.production_mesh for mesh in self.source_calculation.meshes
        ):
            raise ValueError("production_mesh must belong to source_calculation")
        if self.production_mesh.construction_size != (
            self.source_calculation.configuration.production_construction_size
        ):
            raise ValueError(
                "production_mesh must match the configured production size"
            )

        # Alignment is configuration-level because scalar U(1) conjugation is exactly
        # operator-trivial and therefore requires no duplicate per-mesh calculation.
        if self.alignment.configuration is not self.source_calculation.configuration:
            raise ValueError("alignment must retain the exact source configuration")
        if self.alignment.lattice_geometry != self.lattice_geometry:
            raise ValueError("alignment must retain the selected lattice geometry")

        # Locality and truncation are distinct projections over the same production
        # mesh. Their source objects must agree by identity before interpretation.
        for analysis, name in (
            (self.hopping_locality, "hopping_locality"),
            (self.support_truncation, "support_truncation"),
        ):
            if analysis.source_calculation is not self.source_calculation:
                raise ValueError(f"{name} must retain the exact source calculation")
            if analysis.source_mesh is not self.production_mesh:
                raise ValueError(f"{name} must retain the exact production mesh")
            if analysis.lattice_geometry != self.lattice_geometry:
                raise ValueError(f"{name} must retain the selected lattice geometry")

    @property
    def band_subspace_rank(self) -> int:
        """Return the exact scalar retained-space rank."""
        return 1

    @property
    def band_equivalence(self) -> Periodic1DFourierLocalityCalculationResult:
        """Return the unchanged rank-one band-equivalence source calculation."""
        return self.source_calculation


@final
@dataclass(frozen=True, slots=True)
class Periodic1dRank1Calculator:
    """Compose maintained rank-one capability views for one typed calculation.

    Parameters
    ----------
    source_calculation : Periodic1DFourierLocalityCalculationResult
        Exact admitted or freshly produced Fourier-locality result to project.
    lattice_geometry : Periodic1DLatticeGeometry
        Explicit physical direct-lattice geometry selected for current interpretation.

    Notes
    -----
    The operation is read-only with respect to ``source_calculation``. It does not
    deserialize files, choose a physical lattice implicitly, construct a replacement
    Bloch-hopping model, or write a new execution artifact. Callers own byte admission
    and any later persistence boundary.
    """

    source_calculation: Periodic1DFourierLocalityCalculationResult
    lattice_geometry: Periodic1DLatticeGeometry

    def __post_init__(self) -> None:
        """Validate the exact source-result and geometry boundary.

        Raises
        ------
        TypeError
            If either constructor argument is not owned by its exact maintained type.
        """
        if type(self.source_calculation) is not (
            Periodic1DFourierLocalityCalculationResult
        ):
            raise TypeError(
                "source_calculation must be Periodic1DFourierLocalityCalculationResult"
            )
        if type(self.lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")

    def result(self) -> Periodic1dRank1CalculationResult:
        """Return the correlated rank-one capability composition.

        Returns
        -------
        Periodic1dRank1CalculationResult
            The source band-equivalence result, exact production mesh, scalar alignment
            disposition, descriptive hopping-locality projection, and support-removal
            projection correlated through one explicit lattice geometry.

        Raises
        ------
        ValueError
            If the source result does not contain exactly one mesh matching its declared
            production construction size.
        """
        source = self.source_calculation
        configuration = source.configuration

        # Select by the authored production identity rather than assuming that the last
        # mesh remains the production mesh after a future inventory reordering.
        production_meshes = tuple(
            mesh
            for mesh in source.meshes
            if mesh.construction_size == configuration.production_construction_size
        )
        if len(production_meshes) != 1:
            raise ValueError(
                "source_calculation must contain exactly one declared production mesh"
            )
        production_mesh = production_meshes[0]

        # Rank-one alignment is an exact applicability statement over the scalar family,
        # so it binds the configuration and geometry but performs no numerical fit.
        alignment = Periodic1DRank1AlignmentApplicabilityAnalyzer(
            request=configuration,
            lattice_geometry=self.lattice_geometry,
        ).execute()

        # Locality projects complete coefficient tails without deleting support.
        hopping_locality = Periodic1DRank1HoppingLocalityAnalyzer(
            request=Periodic1DRank1HoppingLocalityAnalysisRequest(
                lattice_geometry=self.lattice_geometry,
                source_calculation=source,
                source_mesh=production_mesh,
            )
        ).execute()

        # Truncation remains a separate capability projection over the same exact source
        # ranges, preserving interpolation, truncation-only, and total error channels.
        support_truncation = Periodic1DRank1SupportTruncationAnalyzer(
            request=Periodic1DRank1SupportTruncationAnalysisRequest(
                lattice_geometry=self.lattice_geometry,
                source_calculation=source,
                source_mesh=production_mesh,
            )
        ).execute()

        return Periodic1dRank1CalculationResult(
            source_calculation=source,
            lattice_geometry=self.lattice_geometry,
            production_mesh=production_mesh,
            alignment=alignment,
            hopping_locality=hopping_locality,
            support_truncation=support_truncation,
        )


__all__ = ["Periodic1dRank1CalculationResult", "Periodic1dRank1Calculator"]
