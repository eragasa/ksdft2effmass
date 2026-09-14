"""Private QoI-driven parameter-study and adaptive-refinement probe.

The records and algorithms in this module are revisable architecture evidence. They
are not stable public exports, parameter recommendations, execution authority, or
scientific acceptance. Numerical convergence is represented only within one fixed
modeled-subject identity and over a declared finite candidate domain.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from itertools import pairwise

from .qoi import (
    NormalizedObservationRequirementIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestIdentity,
)


@dataclass(frozen=True, slots=True)
class ParameterStudyIdentity:
    """Nominal identity of one parameter study across immutable revisions."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("parameter-study identity value must be a string")
        if not self.value:
            raise ValueError("parameter-study identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ParameterStudyRevisionIdentity:
    """Nominal identity of one immutable parameter-study revision."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("study-revision identity value must be a string")
        if not self.value:
            raise ValueError("study-revision identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ParameterStudySubjectIdentity:
    """Nominal identity of the fixed or deliberately varied modeled subject."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("study-subject identity value must be a string")
        if not self.value:
            raise ValueError("study-subject identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ParameterStudyCandidateIdentity:
    """Nominal identity of one candidate in a parameter-study revision."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("study-candidate identity value must be a string")
        if not self.value:
            raise ValueError("study-candidate identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementIdentity:
    """Nominal identity and version of one refinement algorithm."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("refinement identity value must be a string")
        if not self.value:
            raise ValueError("refinement identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementConfigurationIdentity:
    """Nominal identity of one immutable refinement-algorithm configuration."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("refinement-configuration identity must be a string")
        if not self.value:
            raise ValueError("refinement-configuration identity must not be empty")


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementStateIdentity:
    """Nominal identity of one immutable refinement-state snapshot."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("refinement-state identity value must be a string")
        if not self.value:
            raise ValueError("refinement-state identity value must not be empty")


class ParameterStudyKind(StrEnum):
    """Closed interpretation assigned to a parameter study."""

    NUMERICAL_CONVERGENCE = "numerical_convergence"
    SOLVER_STABILITY = "solver_stability"
    MODEL_SENSITIVITY = "model_sensitivity"
    PHYSICAL_BRANCH_COMPARISON = "physical_branch_comparison"
    OPERATIONAL_BENCHMARK = "operational_benchmark"


class ParameterFactorKind(StrEnum):
    """Closed scientific or operational role of one varied factor."""

    NUMERICAL = "numerical"
    SOLVER = "solver"
    MODEL = "model"
    PHYSICAL_BRANCH = "physical_branch"
    OPERATIONAL = "operational"


class ParameterStudyRefinementOutcome(StrEnum):
    """Closed outcome of one refinement-algorithm invocation."""

    COMPLETE = "complete"
    PROPOSED = "proposed"
    INSUFFICIENT_INFORMATION = "insufficient_information"
    UNSUPPORTED = "unsupported"
    INVALID = "invalid"
    ERROR = "error"


class ParameterStudyRefinementFailureCode(StrEnum):
    """Stable failure codes of the first finite-sequence implementation."""

    REFINER_IDENTITY_MISMATCH = "refiner_identity_mismatch"
    REFINER_CONFIGURATION_MISMATCH = "refiner_configuration_mismatch"
    REQUIRES_NUMERICAL_CONVERGENCE = "finite_sequence_requires_numerical_convergence"
    REQUIRES_ONE_SCALAR_CRITERION = "finite_sequence_requires_one_scalar_criterion"
    REQUIRES_ONE_QOI_DEFINITION = "finite_sequence_requires_one_qoi_definition"
    QOI_DEFINITION_MISMATCH = "qoi_definition_mismatch"
    CANDIDATE_SEQUENCE_NOT_INCREASING = "candidate_sequence_must_be_strictly_increasing"
    EVALUATIONS_NOT_PREFIX = "evaluations_must_be_candidate_prefix"
    STATE_NOT_PREFIX = "state_must_be_evaluated_or_one_pending_prefix"
    PROPOSED_CANDIDATE_NOT_EVALUATED = "proposed_candidate_not_evaluated"
    EVALUATION_QOI_OR_UNIT_MISMATCH = "evaluation_quantity_or_unit_mismatch"
    CANDIDATE_SEQUENCE_EXHAUSTED = "candidate_sequence_exhausted"
    CANDIDATE_BUDGET_EXHAUSTED = "candidate_budget_exhausted"


class ParameterStudyProposalValidationOutcome(StrEnum):
    """Closed outcome of independent proposal validation."""

    VALID = "valid"
    INVALID = "invalid"


class ParameterStudyProposalValidationCode(StrEnum):
    """Stable independent proposal-validation failure codes."""

    CANDIDATE_BUDGET_EXHAUSTED = "candidate_budget_exhausted"
    QOI_DEFINITION_MISMATCH = "qoi_definition_mismatch"
    PROPOSAL_CORRELATION_MISMATCH = "proposal_correlation_mismatch"
    EVALUATIONS_NOT_PREFIX = "evaluations_must_be_candidate_prefix"
    EVALUATION_QOI_OR_UNIT_MISMATCH = "evaluation_quantity_or_unit_mismatch"
    PREDECESSOR_STATE_NOT_EVALUATED_PREFIX = (
        "predecessor_state_must_equal_evaluated_prefix"
    )
    CANDIDATE_OUTSIDE_DOMAIN = "candidate_outside_declared_domain"
    CANDIDATE_SEQUENCE_EXHAUSTED = "candidate_sequence_exhausted"
    CANDIDATE_NOT_NEXT = "proposal_must_select_next_declared_candidate"
    FIXED_SUBJECT_CHANGED = "proposal_changes_fixed_subject"
    SUCCESSOR_STATE_NOT_EXTENSION = "proposal_state_does_not_extend_predecessor"
    SUCCESSOR_STATE_PREDECESSOR_MISMATCH = "proposal_state_predecessor_mismatch"
    SUCCESSOR_STATE_IDENTITY_REUSED = "proposal_state_identity_must_be_new"


@dataclass(frozen=True, slots=True)
class QuantityOfInterestDefinition:
    """Calculator-independent QoI and its normalized observation requirements."""

    identity: QuantityOfInterestIdentity
    observation_requirement_identities: tuple[
        NormalizedObservationRequirementIdentity, ...
    ]
    completeness: QuantityOfInterestCompleteness

    def __post_init__(self) -> None:
        """Validate exact requirement closure and completeness."""
        if type(self.identity) is not QuantityOfInterestIdentity:
            raise TypeError("identity must be QuantityOfInterestIdentity")
        values = self.observation_requirement_identities
        if type(values) is not tuple or any(
            type(item) is not NormalizedObservationRequirementIdentity
            for item in values
        ):
            raise TypeError(
                "observation_requirement_identities must be a tuple of "
                "NormalizedObservationRequirementIdentity"
            )
        if not values:
            raise ValueError("observation_requirement_identities must not be empty")
        if len(set(values)) != len(values):
            raise ValueError("observation requirement identities must be unique")
        if type(self.completeness) is not QuantityOfInterestCompleteness:
            raise TypeError("completeness must be QuantityOfInterestCompleteness")


@dataclass(frozen=True, slots=True)
class ScalarQuantityOfInterestCriterion:
    """Absolute finite-setting criterion for one scalar QoI in one study."""

    quantity_identity: QuantityOfInterestIdentity
    unit: str
    absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate exact scalar criterion fields."""
        if type(self.quantity_identity) is not QuantityOfInterestIdentity:
            raise TypeError("quantity_identity must be QuantityOfInterestIdentity")
        if type(self.unit) is not str:
            raise TypeError("unit must be a string")
        if not self.unit:
            raise ValueError("unit must not be empty")
        if type(self.absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a float excluding bool")
        if not math.isfinite(self.absolute_tolerance):
            raise ValueError("absolute_tolerance must be finite")
        if self.absolute_tolerance <= 0.0:
            raise ValueError("absolute_tolerance must be positive")


@dataclass(frozen=True, slots=True)
class ParameterStudyCandidate:
    """One typed scalar factor candidate under an identified modeled subject."""

    identity: ParameterStudyCandidateIdentity
    subject_identity: ParameterStudySubjectIdentity
    factor_kind: ParameterFactorKind
    factor_name: str
    value: float
    unit: str

    def __post_init__(self) -> None:
        """Validate exact candidate fields without interpreting other candidates."""
        if type(self.identity) is not ParameterStudyCandidateIdentity:
            raise TypeError("identity must be ParameterStudyCandidateIdentity")
        if type(self.subject_identity) is not ParameterStudySubjectIdentity:
            raise TypeError("subject_identity must be ParameterStudySubjectIdentity")
        if type(self.factor_kind) is not ParameterFactorKind:
            raise TypeError("factor_kind must be ParameterFactorKind")
        if type(self.factor_name) is not str:
            raise TypeError("factor_name must be a string")
        if not self.factor_name:
            raise ValueError("factor_name must not be empty")
        if type(self.value) is not float:
            raise TypeError("value must be a float excluding bool and int")
        if not math.isfinite(self.value):
            raise ValueError("value must be finite")
        if type(self.unit) is not str:
            raise TypeError("unit must be a string")
        if not self.unit:
            raise ValueError("unit must not be empty")


@dataclass(frozen=True, slots=True)
class ParameterStudyRevision:
    """Immutable ordered candidates and criteria for one study revision."""

    identity: ParameterStudyRevisionIdentity
    study_identity: ParameterStudyIdentity
    kind: ParameterStudyKind
    candidates: tuple[ParameterStudyCandidate, ...]
    criteria: tuple[ScalarQuantityOfInterestCriterion, ...]
    predecessor_identity: ParameterStudyRevisionIdentity | None

    def __post_init__(self) -> None:
        """Validate aggregate closure and study-kind factor semantics."""
        if type(self.identity) is not ParameterStudyRevisionIdentity:
            raise TypeError("identity must be ParameterStudyRevisionIdentity")
        if type(self.study_identity) is not ParameterStudyIdentity:
            raise TypeError("study_identity must be ParameterStudyIdentity")
        if type(self.kind) is not ParameterStudyKind:
            raise TypeError("kind must be ParameterStudyKind")
        if type(self.candidates) is not tuple or any(
            type(item) is not ParameterStudyCandidate for item in self.candidates
        ):
            raise TypeError("candidates must be a tuple of ParameterStudyCandidate")
        if not self.candidates:
            raise ValueError("candidates must not be empty")
        if len({item.identity for item in self.candidates}) != len(self.candidates):
            raise ValueError("candidate identities must be unique")
        if type(self.criteria) is not tuple or any(
            type(item) is not ScalarQuantityOfInterestCriterion
            for item in self.criteria
        ):
            raise TypeError(
                "criteria must be a tuple of ScalarQuantityOfInterestCriterion"
            )
        if not self.criteria:
            raise ValueError("criteria must not be empty")
        if len({item.quantity_identity for item in self.criteria}) != len(
            self.criteria
        ):
            raise ValueError("criterion quantity identities must be unique")
        if (
            self.predecessor_identity is not None
            and type(self.predecessor_identity) is not ParameterStudyRevisionIdentity
        ):
            raise TypeError(
                "predecessor_identity must be ParameterStudyRevisionIdentity or None"
            )
        self._validate_kind_semantics()

    def _validate_kind_semantics(self) -> None:
        """Enforce factor role and fixed-subject rules for the declared study kind."""
        expected = {
            ParameterStudyKind.NUMERICAL_CONVERGENCE: ParameterFactorKind.NUMERICAL,
            ParameterStudyKind.SOLVER_STABILITY: ParameterFactorKind.SOLVER,
            ParameterStudyKind.MODEL_SENSITIVITY: ParameterFactorKind.MODEL,
            ParameterStudyKind.PHYSICAL_BRANCH_COMPARISON: (
                ParameterFactorKind.PHYSICAL_BRANCH
            ),
            ParameterStudyKind.OPERATIONAL_BENCHMARK: ParameterFactorKind.OPERATIONAL,
        }[self.kind]
        if any(item.factor_kind is not expected for item in self.candidates):
            raise ValueError("candidate factor kind does not match study kind")
        names = {item.factor_name for item in self.candidates}
        units = {item.unit for item in self.candidates}
        if len(names) != 1 or len(units) != 1:
            raise ValueError("one study revision must vary one factor and unit")
        if (
            self.kind
            in {
                ParameterStudyKind.NUMERICAL_CONVERGENCE,
                ParameterStudyKind.SOLVER_STABILITY,
                ParameterStudyKind.OPERATIONAL_BENCHMARK,
            }
            and len({item.subject_identity for item in self.candidates}) != 1
        ):
            raise ValueError("this study kind requires one fixed subject identity")


@dataclass(frozen=True, slots=True)
class ScalarQuantityOfInterestEvaluation:
    """One scalar QoI evaluated for one exact parameter candidate."""

    candidate_identity: ParameterStudyCandidateIdentity
    quantity_identity: QuantityOfInterestIdentity
    value: float
    unit: str

    def __post_init__(self) -> None:
        """Validate exact scalar evaluation fields."""
        if type(self.candidate_identity) is not ParameterStudyCandidateIdentity:
            raise TypeError(
                "candidate_identity must be ParameterStudyCandidateIdentity"
            )
        if type(self.quantity_identity) is not QuantityOfInterestIdentity:
            raise TypeError("quantity_identity must be QuantityOfInterestIdentity")
        if type(self.value) is not float:
            raise TypeError("value must be a float excluding bool and int")
        if not math.isfinite(self.value):
            raise ValueError("value must be finite")
        if type(self.unit) is not str:
            raise TypeError("unit must be a string")
        if not self.unit:
            raise ValueError("unit must not be empty")


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementState:
    """Immutable ordered candidate history and exact predecessor relation."""

    identity: ParameterStudyRefinementStateIdentity
    predecessor_identity: ParameterStudyRefinementStateIdentity | None
    considered_candidate_identities: tuple[ParameterStudyCandidateIdentity, ...]

    def __post_init__(self) -> None:
        """Validate exact ordered state closure."""
        if type(self.identity) is not ParameterStudyRefinementStateIdentity:
            raise TypeError("identity must be ParameterStudyRefinementStateIdentity")
        if (
            self.predecessor_identity is not None
            and type(self.predecessor_identity)
            is not ParameterStudyRefinementStateIdentity
        ):
            raise TypeError(
                "predecessor_identity must be "
                "ParameterStudyRefinementStateIdentity or None"
            )
        if self.predecessor_identity == self.identity:
            raise ValueError("refinement state cannot be its own predecessor")
        values = self.considered_candidate_identities
        if type(values) is not tuple or any(
            type(item) is not ParameterStudyCandidateIdentity for item in values
        ):
            raise TypeError(
                "considered_candidate_identities must be a tuple of "
                "ParameterStudyCandidateIdentity"
            )
        if len(set(values)) != len(values):
            raise ValueError("considered candidate identities must be unique")


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementRequest:
    """Exact immutable input to one adaptive-refinement operation."""

    revision: ParameterStudyRevision
    quantity_definitions: tuple[QuantityOfInterestDefinition, ...]
    evaluations: tuple[ScalarQuantityOfInterestEvaluation, ...]
    refinement_identity: ParameterStudyRefinementIdentity
    configuration_identity: ParameterStudyRefinementConfigurationIdentity
    state: ParameterStudyRefinementState
    remaining_candidate_budget: int

    def __post_init__(self) -> None:
        """Validate request field types and nonnegative budget."""
        if type(self.revision) is not ParameterStudyRevision:
            raise TypeError("revision must be ParameterStudyRevision")
        if type(self.quantity_definitions) is not tuple or any(
            type(item) is not QuantityOfInterestDefinition
            for item in self.quantity_definitions
        ):
            raise TypeError(
                "quantity_definitions must be a tuple of QuantityOfInterestDefinition"
            )
        if type(self.evaluations) is not tuple or any(
            type(item) is not ScalarQuantityOfInterestEvaluation
            for item in self.evaluations
        ):
            raise TypeError(
                "evaluations must be a tuple of ScalarQuantityOfInterestEvaluation"
            )
        if type(self.refinement_identity) is not ParameterStudyRefinementIdentity:
            raise TypeError(
                "refinement_identity must be ParameterStudyRefinementIdentity"
            )
        if (
            type(self.configuration_identity)
            is not ParameterStudyRefinementConfigurationIdentity
        ):
            raise TypeError(
                "configuration_identity must be "
                "ParameterStudyRefinementConfigurationIdentity"
            )
        if type(self.state) is not ParameterStudyRefinementState:
            raise TypeError("state must be ParameterStudyRefinementState")
        if type(self.remaining_candidate_budget) is not int:
            raise TypeError("remaining_candidate_budget must be an int excluding bool")
        if self.remaining_candidate_budget < 0:
            raise ValueError("remaining_candidate_budget must be nonnegative")


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementComplete:
    """Represent satisfaction of the finite-setting stopping criterion."""

    outcome: ParameterStudyRefinementOutcome
    refinement_identity: ParameterStudyRefinementIdentity
    configuration_identity: ParameterStudyRefinementConfigurationIdentity
    revision_identity: ParameterStudyRevisionIdentity
    selected_candidate_identity: ParameterStudyCandidateIdentity
    absolute_change: float

    def __post_init__(self) -> None:
        """Validate the closed completion result and correlations."""
        if self.outcome is not ParameterStudyRefinementOutcome.COMPLETE:
            raise ValueError("outcome must be COMPLETE")
        if type(self.refinement_identity) is not ParameterStudyRefinementIdentity:
            raise TypeError(
                "refinement_identity must be ParameterStudyRefinementIdentity"
            )
        if (
            type(self.configuration_identity)
            is not ParameterStudyRefinementConfigurationIdentity
        ):
            raise TypeError(
                "configuration_identity must be "
                "ParameterStudyRefinementConfigurationIdentity"
            )
        if type(self.revision_identity) is not ParameterStudyRevisionIdentity:
            raise TypeError("revision_identity must be ParameterStudyRevisionIdentity")
        if (
            type(self.selected_candidate_identity)
            is not ParameterStudyCandidateIdentity
        ):
            raise TypeError(
                "selected_candidate_identity must be ParameterStudyCandidateIdentity"
            )
        if type(self.absolute_change) is not float:
            raise TypeError("absolute_change must be a float")
        if not math.isfinite(self.absolute_change) or self.absolute_change < 0.0:
            raise ValueError("absolute_change must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementProposed:
    """Represent one proposed next candidate and immutable successor state."""

    outcome: ParameterStudyRefinementOutcome
    refinement_identity: ParameterStudyRefinementIdentity
    configuration_identity: ParameterStudyRefinementConfigurationIdentity
    revision_identity: ParameterStudyRevisionIdentity
    candidate: ParameterStudyCandidate
    state: ParameterStudyRefinementState

    def __post_init__(self) -> None:
        """Validate the closed proposal result and correlations."""
        if self.outcome is not ParameterStudyRefinementOutcome.PROPOSED:
            raise ValueError("outcome must be PROPOSED")
        if type(self.refinement_identity) is not ParameterStudyRefinementIdentity:
            raise TypeError(
                "refinement_identity must be ParameterStudyRefinementIdentity"
            )
        if (
            type(self.configuration_identity)
            is not ParameterStudyRefinementConfigurationIdentity
        ):
            raise TypeError(
                "configuration_identity must be "
                "ParameterStudyRefinementConfigurationIdentity"
            )
        if type(self.revision_identity) is not ParameterStudyRevisionIdentity:
            raise TypeError("revision_identity must be ParameterStudyRevisionIdentity")
        if type(self.candidate) is not ParameterStudyCandidate:
            raise TypeError("candidate must be ParameterStudyCandidate")
        if type(self.state) is not ParameterStudyRefinementState:
            raise TypeError("state must be ParameterStudyRefinementState")


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementFailure:
    """Represent a fail-closed non-proposal refinement outcome."""

    outcome: ParameterStudyRefinementOutcome
    code: ParameterStudyRefinementFailureCode
    requested_refinement_identity: ParameterStudyRefinementIdentity
    requested_configuration_identity: ParameterStudyRefinementConfigurationIdentity
    executed_refinement_identity: ParameterStudyRefinementIdentity
    executed_configuration_identity: ParameterStudyRefinementConfigurationIdentity
    revision_identity: ParameterStudyRevisionIdentity

    def __post_init__(self) -> None:
        """Validate the closed failure kind, code, and correlations."""
        if self.outcome not in {
            ParameterStudyRefinementOutcome.INSUFFICIENT_INFORMATION,
            ParameterStudyRefinementOutcome.UNSUPPORTED,
            ParameterStudyRefinementOutcome.INVALID,
            ParameterStudyRefinementOutcome.ERROR,
        }:
            raise ValueError("outcome must be a failure outcome")
        if type(self.code) is not ParameterStudyRefinementFailureCode:
            raise TypeError("code must be ParameterStudyRefinementFailureCode")
        if (
            type(self.requested_refinement_identity)
            is not ParameterStudyRefinementIdentity
        ):
            raise TypeError(
                "requested_refinement_identity must be ParameterStudyRefinementIdentity"
            )
        if (
            type(self.requested_configuration_identity)
            is not ParameterStudyRefinementConfigurationIdentity
        ):
            raise TypeError(
                "requested_configuration_identity must be "
                "ParameterStudyRefinementConfigurationIdentity"
            )
        if (
            type(self.executed_refinement_identity)
            is not ParameterStudyRefinementIdentity
        ):
            raise TypeError(
                "executed_refinement_identity must be ParameterStudyRefinementIdentity"
            )
        if (
            type(self.executed_configuration_identity)
            is not ParameterStudyRefinementConfigurationIdentity
        ):
            raise TypeError(
                "executed_configuration_identity must be "
                "ParameterStudyRefinementConfigurationIdentity"
            )
        if type(self.revision_identity) is not ParameterStudyRevisionIdentity:
            raise TypeError("revision_identity must be ParameterStudyRevisionIdentity")


type ParameterStudyRefinementResult = (
    ParameterStudyRefinementComplete
    | ParameterStudyRefinementProposed
    | ParameterStudyRefinementFailure
)
"""Closed private outcome of one parameter-study refinement invocation."""


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementRecord:
    """Exact request/result provenance for one refinement invocation."""

    request: ParameterStudyRefinementRequest
    result: ParameterStudyRefinementResult

    def __post_init__(self) -> None:
        """Validate request/result identity correlation."""
        if type(self.request) is not ParameterStudyRefinementRequest:
            raise TypeError("request must be ParameterStudyRefinementRequest")
        if type(self.result) not in {
            ParameterStudyRefinementComplete,
            ParameterStudyRefinementProposed,
            ParameterStudyRefinementFailure,
        }:
            raise TypeError("result must be ParameterStudyRefinementResult")
        if isinstance(self.result, ParameterStudyRefinementFailure):
            if (
                self.result.requested_refinement_identity
                != self.request.refinement_identity
            ):
                raise ValueError("failure requested refinement identity must match")
            if (
                self.result.requested_configuration_identity
                != self.request.configuration_identity
            ):
                raise ValueError("failure requested configuration identity must match")
        else:
            if self.result.refinement_identity != self.request.refinement_identity:
                raise ValueError("result refinement identity must match request")
            if (
                self.result.configuration_identity
                != self.request.configuration_identity
            ):
                raise ValueError("result configuration identity must match request")
        if self.result.revision_identity != self.request.revision.identity:
            raise ValueError("result revision identity must match request")


class ParameterStudyRefiner(ABC):
    """Nominal extension point for explicitly injected refinement algorithms."""

    @property
    @abstractmethod
    def refinement_identity(self) -> ParameterStudyRefinementIdentity:
        """Return the exact algorithm and version identity."""

    @property
    @abstractmethod
    def configuration_identity(
        self,
    ) -> ParameterStudyRefinementConfigurationIdentity:
        """Return the exact immutable algorithm-configuration identity."""

    @abstractmethod
    def execute(
        self, request: ParameterStudyRefinementRequest
    ) -> ParameterStudyRefinementResult:
        """Return completion, a successor proposal, or a represented failure."""


@dataclass(frozen=True, slots=True)
class FiniteSequenceParameterStudyRefiner(ParameterStudyRefiner):
    """Evaluate one scalar QoI over a declared finite candidate sequence."""

    _refinement_identity: ParameterStudyRefinementIdentity
    _configuration_identity: ParameterStudyRefinementConfigurationIdentity

    def __post_init__(self) -> None:
        """Validate immutable algorithm configuration identities."""
        if type(self._refinement_identity) is not ParameterStudyRefinementIdentity:
            raise TypeError(
                "_refinement_identity must be ParameterStudyRefinementIdentity"
            )
        if (
            type(self._configuration_identity)
            is not ParameterStudyRefinementConfigurationIdentity
        ):
            raise TypeError(
                "_configuration_identity must be "
                "ParameterStudyRefinementConfigurationIdentity"
            )

    @property
    def refinement_identity(self) -> ParameterStudyRefinementIdentity:
        """Return the exact finite-sequence algorithm identity."""
        return self._refinement_identity

    @property
    def configuration_identity(
        self,
    ) -> ParameterStudyRefinementConfigurationIdentity:
        """Return the exact finite-sequence configuration identity."""
        return self._configuration_identity

    def execute(
        self, request: ParameterStudyRefinementRequest
    ) -> ParameterStudyRefinementResult:
        """Evaluate a prefix and propose, stop, or fail without external effects."""
        if type(request) is not ParameterStudyRefinementRequest:
            raise TypeError("request must be ParameterStudyRefinementRequest")
        if request.refinement_identity != self.refinement_identity:
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INVALID,
                ParameterStudyRefinementFailureCode.REFINER_IDENTITY_MISMATCH,
            )
        if request.configuration_identity != self.configuration_identity:
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INVALID,
                ParameterStudyRefinementFailureCode.REFINER_CONFIGURATION_MISMATCH,
            )
        revision = request.revision
        if revision.kind is not ParameterStudyKind.NUMERICAL_CONVERGENCE:
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.UNSUPPORTED,
                ParameterStudyRefinementFailureCode.REQUIRES_NUMERICAL_CONVERGENCE,
            )
        if len(revision.criteria) != 1:
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.UNSUPPORTED,
                ParameterStudyRefinementFailureCode.REQUIRES_ONE_SCALAR_CRITERION,
            )
        if len(request.quantity_definitions) != 1:
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.UNSUPPORTED,
                ParameterStudyRefinementFailureCode.REQUIRES_ONE_QOI_DEFINITION,
            )
        criterion = revision.criteria[0]
        if request.quantity_definitions[0].identity != criterion.quantity_identity:
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INVALID,
                ParameterStudyRefinementFailureCode.QOI_DEFINITION_MISMATCH,
            )
        if any(
            right.value <= left.value for left, right in pairwise(revision.candidates)
        ):
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INVALID,
                ParameterStudyRefinementFailureCode.CANDIDATE_SEQUENCE_NOT_INCREASING,
            )
        candidate_ids = tuple(item.identity for item in revision.candidates)
        evaluation_ids = tuple(item.candidate_identity for item in request.evaluations)
        if evaluation_ids != candidate_ids[: len(evaluation_ids)]:
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INVALID,
                ParameterStudyRefinementFailureCode.EVALUATIONS_NOT_PREFIX,
            )
        considered = request.state.considered_candidate_identities
        if considered not in {
            candidate_ids[: len(evaluation_ids)],
            candidate_ids[: len(evaluation_ids) + 1],
        }:
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INVALID,
                ParameterStudyRefinementFailureCode.STATE_NOT_PREFIX,
            )
        if len(considered) > len(evaluation_ids):
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INSUFFICIENT_INFORMATION,
                (ParameterStudyRefinementFailureCode.PROPOSED_CANDIDATE_NOT_EVALUATED),
            )
        if any(
            item.quantity_identity != criterion.quantity_identity
            or item.unit != criterion.unit
            for item in request.evaluations
        ):
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INVALID,
                ParameterStudyRefinementFailureCode.EVALUATION_QOI_OR_UNIT_MISMATCH,
            )
        if len(request.evaluations) >= 2:
            absolute_change = abs(
                request.evaluations[-1].value - request.evaluations[-2].value
            )
            if absolute_change <= criterion.absolute_tolerance:
                return ParameterStudyRefinementComplete(
                    ParameterStudyRefinementOutcome.COMPLETE,
                    self.refinement_identity,
                    self.configuration_identity,
                    revision.identity,
                    request.evaluations[-1].candidate_identity,
                    absolute_change,
                )
        next_index = len(request.evaluations)
        if next_index >= len(revision.candidates):
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INSUFFICIENT_INFORMATION,
                ParameterStudyRefinementFailureCode.CANDIDATE_SEQUENCE_EXHAUSTED,
            )
        if request.remaining_candidate_budget == 0:
            return self._failure(
                request,
                ParameterStudyRefinementOutcome.INSUFFICIENT_INFORMATION,
                ParameterStudyRefinementFailureCode.CANDIDATE_BUDGET_EXHAUSTED,
            )
        candidate = revision.candidates[next_index]
        successor_state = ParameterStudyRefinementState(
            ParameterStudyRefinementStateIdentity(
                f"{request.state.identity.value}.{candidate.identity.value}"
            ),
            request.state.identity,
            considered + (candidate.identity,),
        )
        return ParameterStudyRefinementProposed(
            ParameterStudyRefinementOutcome.PROPOSED,
            self.refinement_identity,
            self.configuration_identity,
            revision.identity,
            candidate,
            successor_state,
        )

    def _failure(
        self,
        request: ParameterStudyRefinementRequest,
        outcome: ParameterStudyRefinementOutcome,
        code: ParameterStudyRefinementFailureCode,
    ) -> ParameterStudyRefinementFailure:
        """Return one identity-correlated failure for this algorithm invocation."""
        return ParameterStudyRefinementFailure(
            outcome,
            code,
            request.refinement_identity,
            request.configuration_identity,
            self.refinement_identity,
            self.configuration_identity,
            request.revision.identity,
        )


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementProposalValid:
    """Represent acceptance of one proposal against its exact request."""

    outcome: ParameterStudyProposalValidationOutcome

    def __post_init__(self) -> None:
        """Validate the closed successful result."""
        if self.outcome is not ParameterStudyProposalValidationOutcome.VALID:
            raise ValueError("outcome must be VALID")


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementProposalInvalid:
    """Represent rejection of one proposal without constructing a revision."""

    outcome: ParameterStudyProposalValidationOutcome
    code: ParameterStudyProposalValidationCode

    def __post_init__(self) -> None:
        """Validate the closed rejection result."""
        if self.outcome is not ParameterStudyProposalValidationOutcome.INVALID:
            raise ValueError("outcome must be INVALID")
        if type(self.code) is not ParameterStudyProposalValidationCode:
            raise TypeError("code must be ParameterStudyProposalValidationCode")


type ParameterStudyRefinementProposalValidationResult = (
    ParameterStudyRefinementProposalValid | ParameterStudyRefinementProposalInvalid
)
"""Closed private validation result for one adaptive proposal."""


@dataclass(frozen=True, slots=True)
class ParameterStudyRefinementProposalValidator:
    """Validate one algorithm proposal independently of its implementation."""

    def execute(
        self,
        request: ParameterStudyRefinementRequest,
        proposal: ParameterStudyRefinementProposed,
    ) -> ParameterStudyRefinementProposalValidationResult:
        """Check exact predecessor closure, domain, subject, state, and budget."""
        if type(request) is not ParameterStudyRefinementRequest:
            raise TypeError("request must be ParameterStudyRefinementRequest")
        if type(proposal) is not ParameterStudyRefinementProposed:
            raise TypeError("proposal must be ParameterStudyRefinementProposed")
        if request.remaining_candidate_budget == 0:
            return self._invalid(
                ParameterStudyProposalValidationCode.CANDIDATE_BUDGET_EXHAUSTED
            )
        if (
            proposal.refinement_identity != request.refinement_identity
            or (proposal.configuration_identity != request.configuration_identity)
            or proposal.revision_identity != request.revision.identity
        ):
            return self._invalid(
                ParameterStudyProposalValidationCode.PROPOSAL_CORRELATION_MISMATCH
            )
        criteria = request.revision.criteria
        definitions = request.quantity_definitions
        if (
            len(criteria) != 1
            or len(definitions) != 1
            or (definitions[0].identity != criteria[0].quantity_identity)
        ):
            return self._invalid(
                ParameterStudyProposalValidationCode.QOI_DEFINITION_MISMATCH
            )
        candidate_ids = tuple(item.identity for item in request.revision.candidates)
        evaluation_ids = tuple(item.candidate_identity for item in request.evaluations)
        if evaluation_ids != candidate_ids[: len(evaluation_ids)]:
            return self._invalid(
                ParameterStudyProposalValidationCode.EVALUATIONS_NOT_PREFIX
            )
        if any(
            item.quantity_identity != criteria[0].quantity_identity
            or item.unit != criteria[0].unit
            for item in request.evaluations
        ):
            return self._invalid(
                ParameterStudyProposalValidationCode.EVALUATION_QOI_OR_UNIT_MISMATCH
            )
        if request.state.considered_candidate_identities != evaluation_ids:
            return self._invalid(
                ParameterStudyProposalValidationCode.PREDECESSOR_STATE_NOT_EVALUATED_PREFIX
            )
        if proposal.candidate.identity not in candidate_ids:
            return self._invalid(
                ParameterStudyProposalValidationCode.CANDIDATE_OUTSIDE_DOMAIN
            )
        expected_index = len(request.evaluations)
        if expected_index >= len(request.revision.candidates):
            return self._invalid(
                ParameterStudyProposalValidationCode.CANDIDATE_SEQUENCE_EXHAUSTED
            )
        if proposal.candidate != request.revision.candidates[expected_index]:
            return self._invalid(
                ParameterStudyProposalValidationCode.CANDIDATE_NOT_NEXT
            )
        if (
            proposal.candidate.subject_identity
            != request.revision.candidates[0].subject_identity
        ):
            return self._invalid(
                ParameterStudyProposalValidationCode.FIXED_SUBJECT_CHANGED
            )
        expected_state = request.state.considered_candidate_identities + (
            proposal.candidate.identity,
        )
        if proposal.state.considered_candidate_identities != expected_state:
            return self._invalid(
                ParameterStudyProposalValidationCode.SUCCESSOR_STATE_NOT_EXTENSION
            )
        if proposal.state.identity == request.state.identity:
            return self._invalid(
                ParameterStudyProposalValidationCode.SUCCESSOR_STATE_IDENTITY_REUSED
            )
        if proposal.state.predecessor_identity != request.state.identity:
            return self._invalid(
                ParameterStudyProposalValidationCode.SUCCESSOR_STATE_PREDECESSOR_MISMATCH
            )
        return ParameterStudyRefinementProposalValid(
            ParameterStudyProposalValidationOutcome.VALID
        )

    @staticmethod
    def _invalid(
        code: ParameterStudyProposalValidationCode,
    ) -> ParameterStudyRefinementProposalInvalid:
        """Return one closed proposal rejection."""
        return ParameterStudyRefinementProposalInvalid(
            ParameterStudyProposalValidationOutcome.INVALID, code
        )
