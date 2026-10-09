"""Typed one-case inference and post hoc evaluation composition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .construction import BlindAlignmentObservationConstructionResult
from .evaluation import (
    BlindAlignmentEvaluationRequest,
    BlindAlignmentInferenceEvaluator,
)
from .inference import BlindAlignmentInference
from .records import (
    BlindAlignmentInferencePolicy,
    BlindAlignmentInferenceRequest,
    BlindAlignmentInferenceResult,
)
from .result_records import (
    BlindAlignmentStoppedCaseResult,
    BlindAlignmentSuccessfulCaseResult,
    DiagnosticOutcome,
    SuccessfulStatus,
)

type BlindAlignmentInferenceRoute = Literal["ordinary", "reconciled_partial"]


@dataclass(frozen=True, slots=True)
class BlindAlignmentCaseExecutionRequest:
    """Request inference and conditionally separate post hoc evaluation.

    Parameters
    ----------
    construction
        Observation and separately held hidden truth.
    policy
        Explicit numerical inference policy.
    cell_count
        Positive cell count used only by post hoc model-class evaluation.
    eigenvalue_degeneracy_tolerance
        Positive finite absolute spectral degeneracy tolerance in ``E_G``.
    inference_route
        Ordinary square-space inference or explicitly reconciled rectangular partial
        inference.
    """

    construction: BlindAlignmentObservationConstructionResult
    policy: BlindAlignmentInferencePolicy
    cell_count: int
    eigenvalue_degeneracy_tolerance: float = 1.0e-9
    inference_route: BlindAlignmentInferenceRoute = "ordinary"

    def __post_init__(self) -> None:
        """Validate exact records, positive controls, and the closed route name."""
        if not isinstance(
            self.construction, BlindAlignmentObservationConstructionResult
        ):
            raise TypeError(
                "construction must be BlindAlignmentObservationConstructionResult"
            )
        if not isinstance(self.policy, BlindAlignmentInferencePolicy):
            raise TypeError("policy must be BlindAlignmentInferencePolicy")
        if type(self.cell_count) is not int or self.cell_count < 1:
            raise ValueError("cell_count must be a positive integer")
        if isinstance(self.eigenvalue_degeneracy_tolerance, bool) or not isinstance(
            self.eigenvalue_degeneracy_tolerance, int | float
        ):
            raise TypeError("eigenvalue_degeneracy_tolerance must be real")
        if self.eigenvalue_degeneracy_tolerance <= 0.0:
            raise ValueError("eigenvalue_degeneracy_tolerance must be positive")
        if self.inference_route not in ("ordinary", "reconciled_partial"):
            raise ValueError("unsupported blind-alignment inference route")


@dataclass(frozen=True, slots=True)
class BlindAlignmentCaseExecutionResult:
    """Return represented inference separately from flattened campaign outcome.

    Parameters
    ----------
    inference
        Full represented inference result, including successful matrices when present.
    outcome
        Flattened successful diagnostics or structured stop.
    """

    inference: BlindAlignmentInferenceResult
    outcome: DiagnosticOutcome

    def __post_init__(self) -> None:
        """Require exact inference and outcome records with coherent dispositions."""
        if not isinstance(self.inference, BlindAlignmentInferenceResult):
            raise TypeError("inference must be BlindAlignmentInferenceResult")
        if not isinstance(
            self.outcome,
            BlindAlignmentSuccessfulCaseResult | BlindAlignmentStoppedCaseResult,
        ):
            raise TypeError("outcome must be a successful or stopped case")
        if (self.inference.status == "stopped") != isinstance(
            self.outcome, BlindAlignmentStoppedCaseResult
        ):
            raise ValueError("inference and flattened outcome dispositions must agree")


class BlindAlignmentCaseExecutor:
    """Infer from observation-only data, then evaluate successful output post hoc."""

    __slots__ = ()

    def execute(
        self, request: BlindAlignmentCaseExecutionRequest
    ) -> BlindAlignmentCaseExecutionResult:
        """Execute one case while preventing hidden truth from entering inference.

        Parameters
        ----------
        request
            Separate construction, policy, evaluation controls, and explicit route.

        Returns
        -------
        BlindAlignmentCaseExecutionResult
            Represented inference plus flattened successful diagnostics or structured
            stop.

        Raises
        ------
        TypeError
            If ``request`` has the wrong public type.
        ValueError
            If route requirements or successful diagnostics are incomplete.
        """
        if not isinstance(request, BlindAlignmentCaseExecutionRequest):
            raise TypeError("request must be BlindAlignmentCaseExecutionRequest")
        construction = request.construction
        inference_request = BlindAlignmentInferenceRequest(
            construction.observation, request.policy
        )
        actionizer = BlindAlignmentInference()
        if request.inference_route == "ordinary":
            inference = actionizer.execute(inference_request)
        else:
            inference = actionizer.execute_reconciled_partial(inference_request)
        if inference.status == "stopped":
            stopped = BlindAlignmentStoppedCaseResult(
                identifier=construction.observation.identifier,
                issue_codes=inference.issue_codes,
                anchor_rank=inference.anchor_rank,
                anchor_condition_number=inference.anchor_condition_number,
                minimum_anchor_singular_value=(inference.minimum_anchor_singular_value),
                maximum_principal_angle_radians=(
                    inference.maximum_principal_angle_radians
                ),
                energy_anchor_rank=(
                    None
                    if inference.energy_anchor_rank is None
                    else float(inference.energy_anchor_rank)
                ),
            )
            return BlindAlignmentCaseExecutionResult(inference, stopped)
        if (
            inference.anchor_condition_number is None
            or inference.minimum_anchor_singular_value is None
            or inference.maximum_principal_angle_radians is None
            or inference.energy_anchor_rank is None
            or inference.inferred_energy_shift is None
        ):
            raise ValueError("successful inference diagnostics are incomplete")
        evaluation = BlindAlignmentInferenceEvaluator().execute(
            BlindAlignmentEvaluationRequest(
                identifier=construction.observation.identifier,
                inference=inference,
                hidden_truth=construction.hidden_truth,
                cell_count=request.cell_count,
                eigenvalue_degeneracy_tolerance=(
                    request.eigenvalue_degeneracy_tolerance
                ),
            )
        )
        status: SuccessfulStatus
        if inference.status == "aligned_full":
            status = "aligned_full"
        elif inference.status == "aligned_partial":
            status = "aligned_partial"
        else:
            raise ValueError("successful inference has unsupported status")
        successful = BlindAlignmentSuccessfulCaseResult(
            identifier=construction.observation.identifier,
            status=status,
            dimension=construction.observation.reference_operator.basis.dimension,
            anchor_rank=inference.anchor_rank,
            anchor_condition_number=inference.anchor_condition_number,
            minimum_anchor_singular_value=inference.minimum_anchor_singular_value,
            maximum_principal_angle_radians=(inference.maximum_principal_angle_radians),
            energy_anchor_rank=float(inference.energy_anchor_rank),
            inferred_energy_shift=inference.inferred_energy_shift,
            evaluation=evaluation,
        )
        return BlindAlignmentCaseExecutionResult(inference, successful)
