"""Calculate the BCT periodic-3D rank-two study locality component."""

from typing import Final

from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer

from ksdft2effmass.periodic.periodic3d.rank2.models import (
    Periodic3DRank2BlockHoppingModel,
)
from ksdft2effmass.periodic3d.rank2.hopping_locality.analysis import (
    Periodic3DRank2HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic3d.rank2.hopping_locality.request import (
    Periodic3DRank2HoppingLocalityAnalysisRequest,
)
from ksdft2effmass.periodic3d.rank2.hopping_locality.result import (
    Periodic3DRank2HoppingLocalityAnalysis,
)
from ksdft2effmass.study.periodic import PeriodicStudyModelRole
from ksdft2effmass.study.periodic3d.rank2 import (
    Periodic3DRank2Study,
    Periodic3DRank2StudyOrchestrator,
)

STUDY_ID: Final = "periodic3d-rank2-bct-band-equivalence-hopping-locality"


def calculate_study(
    *,
    model: Periodic3DRank2BlockHoppingModel,
    model_role: PeriodicStudyModelRole,
    shell_indices: tuple[int, ...],
) -> tuple[Periodic3DRank2Study, Periodic3DRank2HoppingLocalityAnalysis]:
    """Correlate the BCT model and calculate unchanged hopping locality.

    Parameters
    ----------
    model
        Exact BCT scientific model supplied by this calculation.
    model_role
        Explicit reference or candidate role in the named comparison study.
    shell_indices
        Metric-shell labels aligned with immutable provider term order.

    Returns
    -------
    tuple[Periodic3DRank2Study, Periodic3DRank2HoppingLocalityAnalysis]
        Study correlation and descriptive normalized hopping powers. No support is
        removed and no locality threshold is applied.

    """
    study = Periodic3DRank2StudyOrchestrator(
        study_id=STUDY_ID,
        model=model,
        model_role=model_role,
    ).execute()
    locality = Periodic3DRank2HoppingLocalityAnalyzer(
        request=Periodic3DRank2HoppingLocalityAnalysisRequest(
            model=model,
            shell_indices=shell_indices,
        ),
        power_analyzer=BlockHoppingPowerAnalyzer(),
    ).execute()
    return study, locality


__all__ = ["STUDY_ID", "calculate_study"]
