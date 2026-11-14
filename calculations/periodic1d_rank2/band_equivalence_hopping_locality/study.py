"""Compose the periodic-1D rank-two comparison-study operand."""

from typing import Final

from ksdft2effmass.periodic.periodic1d.rank2.models import (
    Periodic1DRank2BlockHoppingModel,
)
from ksdft2effmass.study.periodic import PeriodicStudyModelRole
from ksdft2effmass.study.periodic1d.rank2 import (
    Periodic1DRank2Study,
    Periodic1DRank2StudyOrchestrator,
)

STUDY_ID: Final = "periodic1d-rank2-band-equivalence-hopping-locality"


def compose_study(
    *,
    model: Periodic1DRank2BlockHoppingModel,
    model_role: PeriodicStudyModelRole,
) -> Periodic1DRank2Study:
    """Correlate one exact periodic-1D rank-two model and comparison role.

    Parameters
    ----------
    model
        Exact periodic-1D rank-two scientific model.
    model_role
        Explicit reference or candidate role in the named study comparison.

    Returns
    -------
    Periodic1DRank2Study
        Immutable identity, model, and role correlation. The frozen historical
        locality request is not invoked by this composition.

    """
    return Periodic1DRank2StudyOrchestrator(
        study_id=STUDY_ID,
        model=model,
        model_role=model_role,
    ).execute()


__all__ = ["STUDY_ID", "compose_study"]
