"""Retained projection for plain mesh-refinement assessments."""

from __future__ import annotations

from .records.refinement import (
    BandEquivalenceHoppingLocalityRefinementAssessmentRecord,
)
from .refinement_records import BandEquivalenceHoppingLocalityRefinementAssessment


class BandEquivalenceHoppingLocalityRefinementAssessmentRecorder:
    """Project one bound refinement assessment without rerunning its analyzer."""

    __slots__ = ("_assessment",)

    def __init__(
        self,
        assessment: BandEquivalenceHoppingLocalityRefinementAssessment,
    ) -> None:
        if type(assessment) is not BandEquivalenceHoppingLocalityRefinementAssessment:
            raise TypeError(
                "assessment must be BandEquivalenceHoppingLocalityRefinementAssessment"
            )
        self._assessment = assessment

    @property
    def assessment(self) -> BandEquivalenceHoppingLocalityRefinementAssessment:
        """Return the immutable scientific assessment bound to this recorder."""
        return self._assessment

    def result(self) -> BandEquivalenceHoppingLocalityRefinementAssessmentRecord:
        """Return the retained projection without scientific recomputation."""
        return BandEquivalenceHoppingLocalityRefinementAssessmentRecord.from_analysis(
            self._assessment
        )


__all__ = ["BandEquivalenceHoppingLocalityRefinementAssessmentRecorder"]
