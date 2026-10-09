"""Public compositions for reproducible research-monograph calculations.

This package binds exact monograph study definitions, retained wire formats, and
provenance conventions to reusable analysis contracts. Periodic controlled-model
campaigns now have canonical owners in :mod:`ksdft2effmass.campaigns.periodic_1d`,
:mod:`ksdft2effmass.periodic2d`, :mod:`ksdft2effmass.campaigns.piab1d`, and
:mod:`ksdft2effmass.campaigns.qho1d`. This package does not grant execution authority
or establish scientific acceptance.
"""

from ksdft2effmass.periodic2d import (
    Periodic2DDefect,
    Periodic2DDefectExtractionRequest,
    Periodic2DDefectExtractionResult,
    Periodic2DDefectLocalityAnalyzer,
    Periodic2DDefectLocalityRequest,
    Periodic2DDefectLocalityResult,
    Periodic2DDefectPerturbationExtractor,
    Periodic2DDefectRepresentationRequest,
    Periodic2DDefectRepresentationResult,
    Periodic2DDefectRepresenter,
)

from ..periodic_1d import (
    Periodic1DHoppingReductionRequest,
    Periodic1DHoppingReductionResult,
    Periodic1DHoppingReductionWorkflow,
)
from ..qho1d import (
    HarmonicOscillatorResultVerifier,
    HarmonicOscillatorStudyDefinition,
    HarmonicOscillatorStudyEvaluator,
    HarmonicOscillatorStudyInputDeserializer,
    HarmonicOscillatorStudyResult,
    HarmonicOscillatorStudyResultSerializer,
)
from .citation_snapshot import (
    CitationContentAlgorithm,
    CitationContentIdentity,
    CitationSnapshotError,
    CitationSnapshotErrorCode,
    ManuscriptBibliographyEntrySnapshot,
    ManuscriptCitationCall,
    ManuscriptCitationCommandKind,
    ManuscriptCitationGroup,
    ManuscriptCitationOccurrence,
    ManuscriptCitationOrigin,
    ManuscriptCitationPriority,
    ManuscriptCitationSnapshot,
    ManuscriptCitationSourceGap,
    ManuscriptCitationSourceGapReason,
    ManuscriptCitationTodo,
    ManuscriptIncludeInstance,
    ManuscriptSourceFileSnapshot,
    ManuscriptSourceLocator,
    ResearchMonographCitationSnapshotCompiler,
    ResearchMonographCitationSnapshotIntegrityValidator,
    ResearchMonographCitationSnapshotRequest,
    ResearchMonographCitationSnapshotResult,
)
from .impurity_defect_2d import (
    AdoptedCriteriaPlot,
    AdoptedCriterionPlotRecord,
    AdverseControlBarPlot,
    AdverseControlPlotRecord,
    StageCParentSvgPlotter,
)

__all__ = [
    "AdoptedCriteriaPlot",
    "AdoptedCriterionPlotRecord",
    "AdverseControlBarPlot",
    "AdverseControlPlotRecord",
    "CitationContentAlgorithm",
    "CitationContentIdentity",
    "CitationSnapshotError",
    "CitationSnapshotErrorCode",
    "HarmonicOscillatorResultVerifier",
    "HarmonicOscillatorStudyDefinition",
    "HarmonicOscillatorStudyEvaluator",
    "HarmonicOscillatorStudyInputDeserializer",
    "HarmonicOscillatorStudyResult",
    "HarmonicOscillatorStudyResultSerializer",
    "ManuscriptBibliographyEntrySnapshot",
    "ManuscriptCitationCall",
    "ManuscriptCitationCommandKind",
    "ManuscriptCitationGroup",
    "ManuscriptCitationOccurrence",
    "ManuscriptCitationOrigin",
    "ManuscriptCitationPriority",
    "ManuscriptCitationSnapshot",
    "ManuscriptCitationSourceGap",
    "ManuscriptCitationSourceGapReason",
    "ManuscriptCitationTodo",
    "ManuscriptIncludeInstance",
    "ManuscriptSourceFileSnapshot",
    "ManuscriptSourceLocator",
    "Periodic1DHoppingReductionRequest",
    "Periodic1DHoppingReductionResult",
    "Periodic1DHoppingReductionWorkflow",
    "Periodic2DDefect",
    "Periodic2DDefectExtractionRequest",
    "Periodic2DDefectExtractionResult",
    "Periodic2DDefectLocalityAnalyzer",
    "Periodic2DDefectLocalityRequest",
    "Periodic2DDefectLocalityResult",
    "Periodic2DDefectPerturbationExtractor",
    "Periodic2DDefectRepresentationRequest",
    "Periodic2DDefectRepresentationResult",
    "Periodic2DDefectRepresenter",
    "ResearchMonographCitationSnapshotCompiler",
    "ResearchMonographCitationSnapshotIntegrityValidator",
    "ResearchMonographCitationSnapshotRequest",
    "ResearchMonographCitationSnapshotResult",
    "StageCParentSvgPlotter",
]
