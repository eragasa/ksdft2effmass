"""Thin typed factory for the three periodic-1D alignment study families."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast, final, overload

from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementAnalyzer
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityConfiguration,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.rank1.alignment import (
    Periodic1DRank1AlignmentApplicabilityAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.analysis import (
    Periodic1DCompositeBandAlignmentAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.composite.result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation_result import (
    Periodic1DRankNAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.composite.calculation import (
    Periodic1DRankNAlignmentAnalyzer,
)

from .base import Periodic1DGaugeAlignment


@dataclass(frozen=True, slots=True)
class Periodic1DRank1AlignmentStudySpecification:
    """Bind the exact scalar family whose alignment is operator-trivial."""

    lattice_geometry: Periodic1DLatticeGeometry
    configuration: Periodic1DFourierLocalityConfiguration

    def __post_init__(self) -> None:
        if type(self.lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")
        if type(self.configuration) is not Periodic1DFourierLocalityConfiguration:
            raise TypeError(
                "configuration must be Periodic1DFourierLocalityConfiguration"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2AlignmentStudySpecification:
    """Bind one bounded U(2) study and its explicit Procrustes owner."""

    lattice_geometry: Periodic1DLatticeGeometry
    configuration: Periodic1DCompositeBandAlignmentConfiguration
    procrustes_solver: NumpyBatchedComplexUnitaryProcrustesSolver

    def __post_init__(self) -> None:
        if type(self.lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")
        if type(self.configuration) is not (
            Periodic1DCompositeBandAlignmentConfiguration
        ):
            raise TypeError(
                "configuration must be Periodic1DCompositeBandAlignmentConfiguration"
            )
        if type(self.procrustes_solver) is not (
            NumpyBatchedComplexUnitaryProcrustesSolver
        ):
            raise TypeError(
                "procrustes_solver must be the canonical NumPy batched solver"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DRankNAlignmentStudySpecification:
    """Bind one D1-v1 higher-rank case and every numerical collaborator."""

    lattice_geometry: Periodic1DLatticeGeometry
    request: Periodic1DRankNAlignmentCalculationRequest
    procrustes_solver: NumpyBatchedComplexUnitaryProcrustesSolver
    transporter: ClosedLoopPolarFrameTransporter
    scalar_refinement_analyzer: ScalarRefinementAnalyzer

    def __post_init__(self) -> None:
        if type(self.lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")
        if type(self.request) is not Periodic1DRankNAlignmentCalculationRequest:
            raise TypeError(
                "request must be Periodic1DRankNAlignmentCalculationRequest"
            )
        if type(self.procrustes_solver) is not (
            NumpyBatchedComplexUnitaryProcrustesSolver
        ):
            raise TypeError(
                "procrustes_solver must be the canonical NumPy batched solver"
            )
        if type(self.transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        if type(self.scalar_refinement_analyzer) is not ScalarRefinementAnalyzer:
            raise TypeError(
                "scalar_refinement_analyzer must be ScalarRefinementAnalyzer"
            )


Periodic1DAlignmentStudySpecification = (
    Periodic1DRank1AlignmentStudySpecification
    | Periodic1DRank2AlignmentStudySpecification
    | Periodic1DRankNAlignmentStudySpecification
)


@final
class Periodic1DRank2AlignmentStudyAnalyzer(Periodic1DGaugeAlignment):
    """Bind explicit lattice geometry to the maintained rank-two action."""

    __slots__ = ("_delegate", "_specification")

    def __init__(
        self,
        specification: Periodic1DRank2AlignmentStudySpecification,
    ) -> None:
        if type(specification) is not Periodic1DRank2AlignmentStudySpecification:
            raise TypeError(
                "specification must be Periodic1DRank2AlignmentStudySpecification"
            )
        self._specification = specification
        self._delegate = Periodic1DCompositeBandAlignmentAnalyzer(
            specification.configuration,
            specification.procrustes_solver,
        )

    @property
    def specification(self) -> Periodic1DRank2AlignmentStudySpecification:
        """Return the complete exact rank-two study specification."""
        return self._specification

    @property
    def lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the explicit caller-selected lattice geometry."""
        return self.specification.lattice_geometry

    @property
    def direct_lattice(self) -> DirectLattice1D:
        """Return the caller-selected PhysKit direct lattice."""
        return self.specification.lattice_geometry.direct_lattice

    @property
    def delegate(self) -> Periodic1DCompositeBandAlignmentAnalyzer:
        """Return the maintained rank-two numerical action."""
        return self._delegate

    def execute(self) -> Periodic1DCompositeBandAlignmentCalculationResult:
        """Execute the maintained rank-two action without changing its result wire."""
        return self._delegate.execute()


@final
class Periodic1DRankNAlignmentStudyAnalyzer(Periodic1DGaugeAlignment):
    """Bind explicit lattice geometry to one maintained D1-v1 action."""

    __slots__ = ("_delegate", "_specification")

    def __init__(
        self,
        specification: Periodic1DRankNAlignmentStudySpecification,
    ) -> None:
        if type(specification) is not Periodic1DRankNAlignmentStudySpecification:
            raise TypeError(
                "specification must be Periodic1DRankNAlignmentStudySpecification"
            )
        self._specification = specification
        self._delegate = Periodic1DRankNAlignmentAnalyzer(
            request=specification.request,
            procrustes_solver=specification.procrustes_solver,
            transporter=specification.transporter,
            scalar_refinement_analyzer=specification.scalar_refinement_analyzer,
        )

    @property
    def specification(self) -> Periodic1DRankNAlignmentStudySpecification:
        """Return the complete exact higher-rank study specification."""
        return self._specification

    @property
    def lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the explicit caller-selected lattice geometry."""
        return self.specification.lattice_geometry

    @property
    def direct_lattice(self) -> DirectLattice1D:
        """Return the caller-selected PhysKit direct lattice."""
        return self.specification.lattice_geometry.direct_lattice

    @property
    def delegate(self) -> Periodic1DRankNAlignmentAnalyzer:
        """Return the maintained higher-rank numerical action."""
        return self._delegate

    def execute(self) -> Periodic1DRankNAlignmentCalculationResult:
        """Execute the maintained rank-N action without changing its result wire."""
        return self._delegate.execute()


Periodic1DAlignmentAnalyzer = (
    Periodic1DRank1AlignmentApplicabilityAnalyzer
    | Periodic1DRank2AlignmentStudyAnalyzer
    | Periodic1DRankNAlignmentStudyAnalyzer
)


class Periodic1DAlignmentStudyFactory[
    SpecificationT: Periodic1DAlignmentStudySpecification,
]:
    """Construct one exact family-specific action from a bound specification."""

    __slots__ = ("_specification",)

    def __init__(self, specification: SpecificationT) -> None:
        if type(specification) not in (
            Periodic1DRank1AlignmentStudySpecification,
            Periodic1DRank2AlignmentStudySpecification,
            Periodic1DRankNAlignmentStudySpecification,
        ):
            raise TypeError(
                "specification must be an exact periodic-1D alignment study "
                "specification"
            )
        self._specification = specification

    @property
    def specification(self) -> SpecificationT:
        """Return the exact immutable study specification."""
        return self._specification

    @overload
    def create(
        self: Periodic1DAlignmentStudyFactory[
            Periodic1DRank1AlignmentStudySpecification
        ],
    ) -> Periodic1DRank1AlignmentApplicabilityAnalyzer: ...

    @overload
    def create(
        self: Periodic1DAlignmentStudyFactory[
            Periodic1DRank2AlignmentStudySpecification
        ],
    ) -> Periodic1DRank2AlignmentStudyAnalyzer: ...

    @overload
    def create(
        self: Periodic1DAlignmentStudyFactory[
            Periodic1DRankNAlignmentStudySpecification
        ],
    ) -> Periodic1DRankNAlignmentStudyAnalyzer: ...

    def create(self) -> Periodic1DAlignmentAnalyzer:
        """Dispatch on the bound typed specification, never on a bare rank."""
        specification = self.specification
        if type(specification) is Periodic1DRank1AlignmentStudySpecification:
            rank1 = cast(Periodic1DRank1AlignmentStudySpecification, specification)
            return Periodic1DRank1AlignmentApplicabilityAnalyzer(
                request=rank1.configuration,
                lattice_geometry=rank1.lattice_geometry,
            )
        if type(specification) is Periodic1DRank2AlignmentStudySpecification:
            rank2 = cast(Periodic1DRank2AlignmentStudySpecification, specification)
            return Periodic1DRank2AlignmentStudyAnalyzer(rank2)
        if type(specification) is Periodic1DRankNAlignmentStudySpecification:
            rankn = cast(Periodic1DRankNAlignmentStudySpecification, specification)
            return Periodic1DRankNAlignmentStudyAnalyzer(rankn)
        raise AssertionError("validated study specification became unsupported")


__all__ = [
    "Periodic1DAlignmentAnalyzer",
    "Periodic1DAlignmentStudyFactory",
    "Periodic1DAlignmentStudySpecification",
    "Periodic1DRank1AlignmentStudySpecification",
    "Periodic1DRank2AlignmentStudyAnalyzer",
    "Periodic1DRank2AlignmentStudySpecification",
    "Periodic1DRankNAlignmentStudyAnalyzer",
    "Periodic1DRankNAlignmentStudySpecification",
]
