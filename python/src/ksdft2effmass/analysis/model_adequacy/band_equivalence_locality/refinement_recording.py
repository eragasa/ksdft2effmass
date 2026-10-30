"""Retained projection for plain mesh-refinement assessments."""

from __future__ import annotations

from .records.refinement import (
    BandEquivalenceLocalityRefinementAssessmentRecord,
)
from .refinement_records import BandEquivalenceLocalityRefinementAssessment


class BandEquivalenceLocalityRefinementAssessmentRecorder:
    """Project one bound refinement assessment without rerunning its analyzer."""

    __slots__ = ("_assessment",)

    def __init__(
        self,
        assessment: BandEquivalenceLocalityRefinementAssessment,
    ) -> None:
        if type(assessment) is not BandEquivalenceLocalityRefinementAssessment:
            raise TypeError(
                "assessment must be BandEquivalenceLocalityRefinementAssessment"
            )
        self._assessment = assessment

    @property
    def assessment(self) -> BandEquivalenceLocalityRefinementAssessment:
        """Return the immutable scientific assessment bound to this recorder."""
        return self._assessment

    def result(self) -> BandEquivalenceLocalityRefinementAssessmentRecord:
        """Return the retained projection without scientific recomputation."""
        return BandEquivalenceLocalityRefinementAssessmentRecord.from_analysis(
            self._assessment
        )


__all__ = ["BandEquivalenceLocalityRefinementAssessmentRecorder"]
