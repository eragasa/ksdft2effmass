"""Effect-free compiler for generic plane-wave parameter-study composition.

Compilation validates analysis-to-calculator mappings, ordered multi-Task candidate
branches, exact per-Task reuse, Workflow dependencies, and a pure colored-Petri-net
fan-in. It performs no Task invocation, calculator execution, normalization,
scientific acceptance, authority decision, persistence, or native rendering.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from itertools import pairwise

from ksdft2effmass.analysis._parameter_study import (
    ParameterStudyCandidate,
    ParameterStudyCandidateIdentity,
    ParameterStudyObservationCollectionIdentity,
    ParameterStudyObservationCollectionRequest,
    ParameterStudyObservationReuse,
    ParameterStudyObservationRoleIdentity,
    ParameterStudyRevision,
    ParameterStudySubjectIdentity,
    QuantityOfInterestDefinition,
)
from ksdft2effmass.analysis.qoi import (
    NormalizedObservationRequirementIdentity,
    QuantityOfInterestIdentity,
)
from ksdft2effmass.calculators.dft.pw import (
    PlaneWaveBackendBinding,
    PlaneWaveNativeConfigurationIdentity,
    PlaneWaveObservationRequirementIdentity,
    PlaneWavePhysicalModelIdentity,
)
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetArcDefinition,
    ColoredPetriNetArcIdentity,
    ColoredPetriNetBindingVariableIdentity,
    ColoredPetriNetColorDefinition,
    ColoredPetriNetColorIdentity,
    ColoredPetriNetDefinition,
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetGuardExpression,
    ColoredPetriNetGuardOperator,
    ColoredPetriNetInputInscription,
    ColoredPetriNetInputMode,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
    ColoredPetriNetOutputInscription,
    ColoredPetriNetPlaceDefinition,
    ColoredPetriNetPlaceIdentity,
    ColoredPetriNetPlaceMarking,
    ColoredPetriNetToken,
    ColoredPetriNetTokenIdentity,
    ColoredPetriNetTokenPattern,
    ColoredPetriNetTokenTemplate,
    ColoredPetriNetTransitionDefinition,
    ColoredPetriNetTransitionIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueExpression,
    ColoredPetriNetValueExpressionKind,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.units import UnitIdentity
from ksdft2effmass.workflows import (
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGate,
    TaskStartGateIdentity,
    TaskStartGateSet,
    TaskStartGateSetIdentity,
    TaskStartGateSetMode,
    WorkflowComposition,
    WorkflowIdentity,
)


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCompilerIdentity:
    """Identify one exact generic study compiler implementation."""

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("compiler identity value must be a built-in str")
        if not self.value:
            raise ValueError("compiler identity value must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCompilationIdentity:
    """Identify one immutable effect-free study compilation operation."""

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("compilation identity value must be a built-in str")
        if not self.value:
            raise ValueError("compilation identity value must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyTaskRoleIdentity:
    """Identify one ordered Task role within every candidate branch."""

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("Task-role identity value must be a built-in str")
        if not self.value:
            raise ValueError("Task-role identity value must not be empty")

    @property
    def observation_role_identity(self) -> ParameterStudyObservationRoleIdentity:
        """Return the analysis-owned observation role with the same exact value."""
        return ParameterStudyObservationRoleIdentity(self.value)


class PlaneWaveStudyCompilationOutcome(StrEnum):
    """Closed outcome kinds of effect-free study compilation."""

    COMPILED = "compiled"
    UNSUPPORTED = "unsupported"
    INCOMPATIBLE = "incompatible"
    INVALID = "invalid"
    ERROR = "error"


class PlaneWaveStudyCompilationFailureCode(StrEnum):
    """Stable fail-closed study-compilation codes."""

    COMPILER_IDENTITY_MISMATCH = "compiler_identity_mismatch"
    CANDIDATE_BINDING_COUNT_MISMATCH = "candidate_binding_count_mismatch"
    CANDIDATE_BINDING_ORDER_MISMATCH = "candidate_bindings_must_follow_revision_order"
    CANDIDATE_SUBJECT_MISMATCH = "candidate_subject_binding_mismatch"
    CANDIDATE_TASK_ROLE_MISMATCH = "candidate_task_role_mismatch"
    FACTOR_TASK_ROLE_MISSING = "factor_task_role_missing"
    PHYSICAL_MODEL_MISMATCH = "physical_model_binding_mismatch"
    CANDIDATE_FACTOR_MISMATCH = "candidate_factor_binding_mismatch"
    QOI_BINDING_COVERAGE_MISMATCH = "qoi_binding_coverage_mismatch"
    QOI_OBSERVATION_MAPPING_MISMATCH = "qoi_observation_mapping_mismatch"
    REQUIRED_OBSERVATION_MISSING = "required_observation_missing"
    BACKEND_BINDING_IDENTITY_CONFLICT = "backend_binding_identity_content_conflict"
    TASK_INSTANCE_IDENTITY_CONFLICT = "task_instance_identity_content_conflict"
    DISTINCT_TASK_CONTENT_SHARES_INSTANCE = "distinct_task_content_shares_instance"
    IDENTICAL_TASK_CONTENT_NOT_REUSED = "identical_task_content_requires_reuse"
    REQUEST_TASK_ALREADY_GATED = "request_task_instance_must_be_ungated"


@dataclass(frozen=True, slots=True)
class PlaneWaveStudySubjectBinding:
    """Bind an analysis subject to one calculator physical-model identity."""

    study_subject_identity: ParameterStudySubjectIdentity
    physical_model_identity: PlaneWavePhysicalModelIdentity

    def __post_init__(self) -> None:
        if type(self.study_subject_identity) is not ParameterStudySubjectIdentity:
            raise TypeError(
                "study_subject_identity must be ParameterStudySubjectIdentity"
            )
        if type(self.physical_model_identity) is not PlaneWavePhysicalModelIdentity:
            raise TypeError(
                "physical_model_identity must be PlaneWavePhysicalModelIdentity"
            )


@dataclass(frozen=True, slots=True)
class PlaneWaveObservationRequirementBinding:
    """Bind one analysis requirement to one Task role and calculator requirement."""

    task_role_identity: PlaneWaveStudyTaskRoleIdentity
    analysis_requirement_identity: NormalizedObservationRequirementIdentity
    calculator_requirement_identity: PlaneWaveObservationRequirementIdentity

    def __post_init__(self) -> None:
        if type(self.task_role_identity) is not PlaneWaveStudyTaskRoleIdentity:
            raise TypeError("task_role_identity must be PlaneWaveStudyTaskRoleIdentity")
        if (
            type(self.analysis_requirement_identity)
            is not NormalizedObservationRequirementIdentity
        ):
            raise TypeError(
                "analysis_requirement_identity must be "
                "NormalizedObservationRequirementIdentity"
            )
        if (
            type(self.calculator_requirement_identity)
            is not PlaneWaveObservationRequirementIdentity
        ):
            raise TypeError(
                "calculator_requirement_identity must be "
                "PlaneWaveObservationRequirementIdentity"
            )


@dataclass(frozen=True, slots=True)
class PlaneWaveQuantityOfInterestBinding:
    """Bind one QoI definition to role-specific calculator observations."""

    definition: QuantityOfInterestDefinition
    observation_bindings: tuple[PlaneWaveObservationRequirementBinding, ...]

    def __post_init__(self) -> None:
        if type(self.definition) is not QuantityOfInterestDefinition:
            raise TypeError("definition must be QuantityOfInterestDefinition")
        if type(self.observation_bindings) is not tuple or any(
            type(item) is not PlaneWaveObservationRequirementBinding
            for item in self.observation_bindings
        ):
            raise TypeError(
                "observation_bindings must be a tuple of "
                "PlaneWaveObservationRequirementBinding"
            )
        if not self.observation_bindings:
            raise ValueError("observation_bindings must not be empty")
        analysis_ids = tuple(
            value.analysis_requirement_identity for value in self.observation_bindings
        )
        if len(set(analysis_ids)) != len(analysis_ids):
            raise ValueError("analysis observation bindings must be unique")
        calculator_keys = tuple(
            (value.task_role_identity, value.calculator_requirement_identity)
            for value in self.observation_bindings
        )
        if len(set(calculator_keys)) != len(calculator_keys):
            raise ValueError("role-calculator observation bindings must be unique")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyTaskBinding:
    """Bind one candidate Task role to exact portable/native input identity.

    ``backend_binding`` may be ``None`` when no demonstrated portable simulation
    specification represents an integration-native Task, such as an explicit-point
    diagnostic NSCF. The exact native configuration and declared calculator
    observations remain mandatory; no portable fields are fabricated.
    """

    role_identity: PlaneWaveStudyTaskRoleIdentity
    task_instance: TaskInstance
    native_configuration_identity: PlaneWaveNativeConfigurationIdentity
    observation_requirement_identities: tuple[
        PlaneWaveObservationRequirementIdentity, ...
    ]
    backend_binding: PlaneWaveBackendBinding | None

    def __post_init__(self) -> None:
        if type(self.role_identity) is not PlaneWaveStudyTaskRoleIdentity:
            raise TypeError("role_identity must be PlaneWaveStudyTaskRoleIdentity")
        if type(self.task_instance) is not TaskInstance:
            raise TypeError("task_instance must be TaskInstance")
        if (
            type(self.native_configuration_identity)
            is not PlaneWaveNativeConfigurationIdentity
        ):
            raise TypeError(
                "native_configuration_identity must be "
                "PlaneWaveNativeConfigurationIdentity"
            )
        if type(self.observation_requirement_identities) is not tuple or any(
            type(value) is not PlaneWaveObservationRequirementIdentity
            for value in self.observation_requirement_identities
        ):
            raise TypeError(
                "observation_requirement_identities must be a tuple of "
                "PlaneWaveObservationRequirementIdentity"
            )
        if not self.observation_requirement_identities:
            raise ValueError("observation_requirement_identities must not be empty")
        if len(set(self.observation_requirement_identities)) != len(
            self.observation_requirement_identities
        ):
            raise ValueError("observation requirement identities must be unique")
        if self.backend_binding is not None:
            if type(self.backend_binding) is not PlaneWaveBackendBinding:
                raise TypeError(
                    "backend_binding must be PlaneWaveBackendBinding or None"
                )
            if (
                self.backend_binding.supplement.native_configuration_identity
                != self.native_configuration_identity
            ):
                raise ValueError(
                    "backend binding and Task binding native configuration must agree"
                )
            portable_requirements = set(
                self.backend_binding.specification.observation_requirement_identities
            )
            if not set(self.observation_requirement_identities).issubset(
                portable_requirements
            ):
                raise ValueError(
                    "portable backend binding must declare every Task observation"
                )


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCandidateBinding:
    """Bind one logical candidate to an ordered reusable multi-Task branch."""

    candidate: ParameterStudyCandidate
    task_bindings: tuple[PlaneWaveStudyTaskBinding, ...]
    factor_task_role_identity: PlaneWaveStudyTaskRoleIdentity

    def __post_init__(self) -> None:
        if type(self.candidate) is not ParameterStudyCandidate:
            raise TypeError("candidate must be ParameterStudyCandidate")
        if type(self.task_bindings) is not tuple or any(
            type(value) is not PlaneWaveStudyTaskBinding for value in self.task_bindings
        ):
            raise TypeError(
                "task_bindings must be a tuple of PlaneWaveStudyTaskBinding"
            )
        if not self.task_bindings:
            raise ValueError("task_bindings must not be empty")
        roles = tuple(value.role_identity for value in self.task_bindings)
        if len(set(roles)) != len(roles):
            raise ValueError("candidate Task roles must be unique")
        if type(self.factor_task_role_identity) is not PlaneWaveStudyTaskRoleIdentity:
            raise TypeError(
                "factor_task_role_identity must be PlaneWaveStudyTaskRoleIdentity"
            )

    def task_for_role(
        self, role_identity: PlaneWaveStudyTaskRoleIdentity
    ) -> PlaneWaveStudyTaskBinding | None:
        """Return this candidate's Task binding for an exact role, if present."""
        if type(role_identity) is not PlaneWaveStudyTaskRoleIdentity:
            raise TypeError("role_identity must be PlaneWaveStudyTaskRoleIdentity")
        for binding in self.task_bindings:
            if binding.role_identity == role_identity:
                return binding
        return None


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyTaskDependency:
    """Record one directed dependency between compiled Task instances."""

    upstream_identity: TaskInstanceIdentity
    downstream_identity: TaskInstanceIdentity

    def __post_init__(self) -> None:
        if type(self.upstream_identity) is not TaskInstanceIdentity:
            raise TypeError("upstream_identity must be TaskInstanceIdentity")
        if type(self.downstream_identity) is not TaskInstanceIdentity:
            raise TypeError("downstream_identity must be TaskInstanceIdentity")
        if self.upstream_identity == self.downstream_identity:
            raise ValueError("dependency must connect distinct Task instances")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyTaskReuse:
    """Record one logical candidate's exact reuse of a prior candidate Task."""

    candidate_identity: ParameterStudyCandidateIdentity
    canonical_candidate_identity: ParameterStudyCandidateIdentity
    task_role_identity: PlaneWaveStudyTaskRoleIdentity
    task_instance_identity: TaskInstanceIdentity

    def __post_init__(self) -> None:
        if type(self.candidate_identity) is not ParameterStudyCandidateIdentity:
            raise TypeError(
                "candidate_identity must be ParameterStudyCandidateIdentity"
            )
        if (
            type(self.canonical_candidate_identity)
            is not ParameterStudyCandidateIdentity
        ):
            raise TypeError(
                "canonical_candidate_identity must be ParameterStudyCandidateIdentity"
            )
        if self.candidate_identity == self.canonical_candidate_identity:
            raise ValueError("reuse must identify two distinct candidates")
        if type(self.task_role_identity) is not PlaneWaveStudyTaskRoleIdentity:
            raise TypeError("task_role_identity must be PlaneWaveStudyTaskRoleIdentity")
        if type(self.task_instance_identity) is not TaskInstanceIdentity:
            raise TypeError("task_instance_identity must be TaskInstanceIdentity")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCompilationRequest:
    """Exact inputs to generic effect-free multi-revision study compilation."""

    identity: PlaneWaveStudyCompilationIdentity
    compiler_identity: PlaneWaveStudyCompilerIdentity
    workflow_identity: WorkflowIdentity
    definition_identity: ColoredPetriNetDefinitionIdentity
    initial_marking_identity: ColoredPetriNetMarkingIdentity
    revisions: tuple[ParameterStudyRevision, ...]
    subject_binding: PlaneWaveStudySubjectBinding
    quantity_bindings: tuple[PlaneWaveQuantityOfInterestBinding, ...]
    candidate_bindings: tuple[PlaneWaveStudyCandidateBinding, ...]
    collection_task_instance: TaskInstance
    analysis_task_instance: TaskInstance
    observation_collection_identity: ParameterStudyObservationCollectionIdentity

    def __post_init__(self) -> None:
        if type(self.identity) is not PlaneWaveStudyCompilationIdentity:
            raise TypeError("identity must be PlaneWaveStudyCompilationIdentity")
        if type(self.compiler_identity) is not PlaneWaveStudyCompilerIdentity:
            raise TypeError("compiler_identity must be PlaneWaveStudyCompilerIdentity")
        if type(self.workflow_identity) is not WorkflowIdentity:
            raise TypeError("workflow_identity must be WorkflowIdentity")
        if type(self.definition_identity) is not ColoredPetriNetDefinitionIdentity:
            raise TypeError(
                "definition_identity must be ColoredPetriNetDefinitionIdentity"
            )
        if type(self.initial_marking_identity) is not ColoredPetriNetMarkingIdentity:
            raise TypeError(
                "initial_marking_identity must be ColoredPetriNetMarkingIdentity"
            )
        if type(self.revisions) is not tuple or any(
            type(value) is not ParameterStudyRevision for value in self.revisions
        ):
            raise TypeError("revisions must be a tuple of ParameterStudyRevision")
        if not self.revisions:
            raise ValueError("revisions must not be empty")
        if len({value.identity for value in self.revisions}) != len(self.revisions):
            raise ValueError("revision identities must be unique")
        if type(self.subject_binding) is not PlaneWaveStudySubjectBinding:
            raise TypeError("subject_binding must be PlaneWaveStudySubjectBinding")
        if type(self.quantity_bindings) is not tuple or any(
            type(value) is not PlaneWaveQuantityOfInterestBinding
            for value in self.quantity_bindings
        ):
            raise TypeError(
                "quantity_bindings must be a tuple of "
                "PlaneWaveQuantityOfInterestBinding"
            )
        if type(self.candidate_bindings) is not tuple or any(
            type(value) is not PlaneWaveStudyCandidateBinding
            for value in self.candidate_bindings
        ):
            raise TypeError(
                "candidate_bindings must be a tuple of PlaneWaveStudyCandidateBinding"
            )
        for field_name, value in (
            ("collection_task_instance", self.collection_task_instance),
            ("analysis_task_instance", self.analysis_task_instance),
        ):
            if type(value) is not TaskInstance:
                raise TypeError(f"{field_name} must be TaskInstance")
        if (
            type(self.observation_collection_identity)
            is not ParameterStudyObservationCollectionIdentity
        ):
            raise TypeError(
                "observation_collection_identity must be "
                "ParameterStudyObservationCollectionIdentity"
            )


@dataclass(frozen=True, slots=True)
class CompiledPlaneWaveStudyTask:
    """Correlate one compiled Task role, transition, and result place."""

    role_identity: PlaneWaveStudyTaskRoleIdentity
    task_instance: TaskInstance
    transition_identity: ColoredPetriNetTransitionIdentity
    result_place_identity: ColoredPetriNetPlaceIdentity

    def __post_init__(self) -> None:
        if type(self.role_identity) is not PlaneWaveStudyTaskRoleIdentity:
            raise TypeError("role_identity must be PlaneWaveStudyTaskRoleIdentity")
        if type(self.task_instance) is not TaskInstance:
            raise TypeError("task_instance must be TaskInstance")
        if type(self.transition_identity) is not ColoredPetriNetTransitionIdentity:
            raise TypeError(
                "transition_identity must be ColoredPetriNetTransitionIdentity"
            )
        if type(self.result_place_identity) is not ColoredPetriNetPlaceIdentity:
            raise TypeError(
                "result_place_identity must be ColoredPetriNetPlaceIdentity"
            )


@dataclass(frozen=True, slots=True)
class CompiledPlaneWaveStudyCandidate:
    """Retain one logical candidate and its ordered compiled Task branch."""

    candidate_identity: ParameterStudyCandidateIdentity
    tasks: tuple[CompiledPlaneWaveStudyTask, ...]

    def __post_init__(self) -> None:
        if type(self.candidate_identity) is not ParameterStudyCandidateIdentity:
            raise TypeError(
                "candidate_identity must be ParameterStudyCandidateIdentity"
            )
        if type(self.tasks) is not tuple or any(
            type(value) is not CompiledPlaneWaveStudyTask for value in self.tasks
        ):
            raise TypeError("tasks must be a tuple of CompiledPlaneWaveStudyTask")
        if not self.tasks:
            raise ValueError("tasks must not be empty")


@dataclass(frozen=True, slots=True)
class CompiledPlaneWaveStudy:
    """Complete generic Workflow, CPN, reuse, and observation-collection plan."""

    request: PlaneWaveStudyCompilationRequest
    workflow_composition: WorkflowComposition
    definition: ColoredPetriNetDefinition
    initial_marking: ColoredPetriNetMarking
    candidates: tuple[CompiledPlaneWaveStudyCandidate, ...]
    collection_task_instance: TaskInstance
    collection_transition_identity: ColoredPetriNetTransitionIdentity
    analysis_task_instance: TaskInstance
    analysis_transition_identity: ColoredPetriNetTransitionIdentity
    task_dependencies: tuple[PlaneWaveStudyTaskDependency, ...]
    reuse: tuple[PlaneWaveStudyTaskReuse, ...]
    observation_collection_request: ParameterStudyObservationCollectionRequest

    def __post_init__(self) -> None:
        if type(self.request) is not PlaneWaveStudyCompilationRequest:
            raise TypeError("request must be PlaneWaveStudyCompilationRequest")
        if type(self.workflow_composition) is not WorkflowComposition:
            raise TypeError("workflow_composition must be WorkflowComposition")
        if type(self.definition) is not ColoredPetriNetDefinition:
            raise TypeError("definition must be ColoredPetriNetDefinition")
        if type(self.initial_marking) is not ColoredPetriNetMarking:
            raise TypeError("initial_marking must be ColoredPetriNetMarking")
        if type(self.candidates) is not tuple or any(
            type(value) is not CompiledPlaneWaveStudyCandidate
            for value in self.candidates
        ):
            raise TypeError(
                "candidates must be a tuple of CompiledPlaneWaveStudyCandidate"
            )
        for field_name, task_value in (
            ("collection_task_instance", self.collection_task_instance),
            ("analysis_task_instance", self.analysis_task_instance),
        ):
            if type(task_value) is not TaskInstance:
                raise TypeError(f"{field_name} must be TaskInstance")
        for field_name, transition_value in (
            ("collection_transition_identity", self.collection_transition_identity),
            ("analysis_transition_identity", self.analysis_transition_identity),
        ):
            if type(transition_value) is not ColoredPetriNetTransitionIdentity:
                raise TypeError(
                    f"{field_name} must be ColoredPetriNetTransitionIdentity"
                )
        if type(self.task_dependencies) is not tuple or any(
            type(value) is not PlaneWaveStudyTaskDependency
            for value in self.task_dependencies
        ):
            raise TypeError(
                "task_dependencies must be a tuple of PlaneWaveStudyTaskDependency"
            )
        if type(self.reuse) is not tuple or any(
            type(value) is not PlaneWaveStudyTaskReuse for value in self.reuse
        ):
            raise TypeError("reuse must be a tuple of PlaneWaveStudyTaskReuse")
        if (
            type(self.observation_collection_request)
            is not ParameterStudyObservationCollectionRequest
        ):
            raise TypeError(
                "observation_collection_request must be "
                "ParameterStudyObservationCollectionRequest"
            )


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCompilationCompiled:
    """Represent successful complete parameter-study compilation."""

    outcome: PlaneWaveStudyCompilationOutcome
    study: CompiledPlaneWaveStudy

    def __post_init__(self) -> None:
        if self.outcome is not PlaneWaveStudyCompilationOutcome.COMPILED:
            raise ValueError("outcome must be COMPILED")
        if type(self.study) is not CompiledPlaneWaveStudy:
            raise TypeError("study must be CompiledPlaneWaveStudy")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCompilationFailure:
    """Represent one fail-closed result correlated to its exact invocation."""

    request: PlaneWaveStudyCompilationRequest
    executed_compiler_identity: PlaneWaveStudyCompilerIdentity
    outcome: PlaneWaveStudyCompilationOutcome
    code: PlaneWaveStudyCompilationFailureCode

    def __post_init__(self) -> None:
        if type(self.request) is not PlaneWaveStudyCompilationRequest:
            raise TypeError("request must be PlaneWaveStudyCompilationRequest")
        if type(self.executed_compiler_identity) is not PlaneWaveStudyCompilerIdentity:
            raise TypeError(
                "executed_compiler_identity must be PlaneWaveStudyCompilerIdentity"
            )
        if self.outcome not in {
            PlaneWaveStudyCompilationOutcome.UNSUPPORTED,
            PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
            PlaneWaveStudyCompilationOutcome.INVALID,
            PlaneWaveStudyCompilationOutcome.ERROR,
        }:
            raise ValueError("outcome must be a study compilation failure")
        if type(self.code) is not PlaneWaveStudyCompilationFailureCode:
            raise TypeError("code must be PlaneWaveStudyCompilationFailureCode")


type PlaneWaveStudyCompilationResult = (
    PlaneWaveStudyCompilationCompiled | PlaneWaveStudyCompilationFailure
)
"""Closed result of compiling immutable plane-wave study revisions."""


@dataclass(frozen=True, slots=True)
class PlaneWaveParameterStudyCompiler:
    """Compile generic ordered candidate branches without performing effects."""

    identity: PlaneWaveStudyCompilerIdentity

    def __post_init__(self) -> None:
        if type(self.identity) is not PlaneWaveStudyCompilerIdentity:
            raise TypeError("identity must be PlaneWaveStudyCompilerIdentity")

    def execute(
        self, request: PlaneWaveStudyCompilationRequest
    ) -> PlaneWaveStudyCompilationResult:
        """Return one complete generic plan or a deterministic closed failure."""
        if type(request) is not PlaneWaveStudyCompilationRequest:
            raise TypeError("request must be PlaneWaveStudyCompilationRequest")
        if request.compiler_identity != self.identity:
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.COMPILER_IDENTITY_MISMATCH,
            )
        expected_candidates = tuple(
            candidate
            for revision in request.revisions
            for candidate in revision.candidates
        )
        bindings = request.candidate_bindings
        if len(bindings) != len(expected_candidates):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.CANDIDATE_BINDING_COUNT_MISMATCH,
            )
        if tuple(value.candidate for value in bindings) != expected_candidates:
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.CANDIDATE_BINDING_ORDER_MISMATCH,
            )
        if any(
            value.candidate.subject_identity
            != request.subject_binding.study_subject_identity
            for value in bindings
        ):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
                PlaneWaveStudyCompilationFailureCode.CANDIDATE_SUBJECT_MISMATCH,
            )
        roles = tuple(value.role_identity for value in bindings[0].task_bindings)
        if any(
            tuple(task.role_identity for task in value.task_bindings) != roles
            for value in bindings
        ):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.CANDIDATE_TASK_ROLE_MISMATCH,
            )
        if any(value.factor_task_role_identity not in roles for value in bindings):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.FACTOR_TASK_ROLE_MISSING,
            )
        if (
            any(
                task.task_instance.start_gate_set is not None
                for value in bindings
                for task in value.task_bindings
            )
            or request.collection_task_instance.start_gate_set is not None
            or (request.analysis_task_instance.start_gate_set is not None)
        ):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.REQUEST_TASK_ALREADY_GATED,
            )
        if any(
            task.backend_binding is not None
            and task.backend_binding.specification.physical_model_identity
            != request.subject_binding.physical_model_identity
            for value in bindings
            for task in value.task_bindings
        ):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
                PlaneWaveStudyCompilationFailureCode.PHYSICAL_MODEL_MISMATCH,
            )
        if any(not self._candidate_factor_agrees(value) for value in bindings):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
                PlaneWaveStudyCompilationFailureCode.CANDIDATE_FACTOR_MISMATCH,
            )
        quantity_failure = self._quantity_failure(request, roles)
        if quantity_failure is not None:
            return quantity_failure
        identity_failure = self._identity_failure(request)
        if identity_failure is not None:
            return identity_failure
        reuse_failure = self._reuse_failure(request)
        if reuse_failure is not None:
            return reuse_failure
        return PlaneWaveStudyCompilationCompiled(
            PlaneWaveStudyCompilationOutcome.COMPILED,
            self._compile(request, roles),
        )

    def _quantity_failure(
        self,
        request: PlaneWaveStudyCompilationRequest,
        roles: tuple[PlaneWaveStudyTaskRoleIdentity, ...],
    ) -> PlaneWaveStudyCompilationFailure | None:
        """Return exact QoI coverage, mapping, or availability failure."""
        criterion_ids: list[QuantityOfInterestIdentity] = []
        for revision in request.revisions:
            for criterion in revision.criteria:
                if criterion.quantity_identity not in criterion_ids:
                    criterion_ids.append(criterion.quantity_identity)
        definition_ids = tuple(
            value.definition.identity for value in request.quantity_bindings
        )
        if definition_ids != tuple(criterion_ids):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.QOI_BINDING_COVERAGE_MISMATCH,
            )
        for binding in request.quantity_bindings:
            analysis_ids = tuple(
                value.analysis_requirement_identity
                for value in binding.observation_bindings
            )
            if analysis_ids != binding.definition.observation_requirement_identities:
                return self._failure(
                    request,
                    PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
                    PlaneWaveStudyCompilationFailureCode.QOI_OBSERVATION_MAPPING_MISMATCH,
                )
            if any(
                value.task_role_identity not in roles
                for value in binding.observation_bindings
            ):
                return self._failure(
                    request,
                    PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
                    PlaneWaveStudyCompilationFailureCode.QOI_OBSERVATION_MAPPING_MISMATCH,
                )
            for candidate in request.candidate_bindings:
                for observation in binding.observation_bindings:
                    task = candidate.task_for_role(observation.task_role_identity)
                    if task is None or (
                        observation.calculator_requirement_identity
                        not in task.observation_requirement_identities
                    ):
                        return self._failure(
                            request,
                            PlaneWaveStudyCompilationOutcome.UNSUPPORTED,
                            PlaneWaveStudyCompilationFailureCode.REQUIRED_OBSERVATION_MISSING,
                        )
        return None

    def _identity_failure(
        self, request: PlaneWaveStudyCompilationRequest
    ) -> PlaneWaveStudyCompilationFailure | None:
        """Reject nominal backend or Task identities assigned to unequal content."""
        tasks = tuple(
            task
            for candidate in request.candidate_bindings
            for task in candidate.task_bindings
        )
        for left_index, left in enumerate(tasks):
            if left.backend_binding is not None and any(
                right.backend_binding is not None
                and right.backend_binding.identity == left.backend_binding.identity
                and right.backend_binding != left.backend_binding
                for right in tasks[left_index + 1 :]
            ):
                return self._failure(
                    request,
                    PlaneWaveStudyCompilationOutcome.INVALID,
                    PlaneWaveStudyCompilationFailureCode.BACKEND_BINDING_IDENTITY_CONFLICT,
                )
            if any(
                right.task_instance.identity == left.task_instance.identity
                and right.task_instance != left.task_instance
                for right in tasks[left_index + 1 :]
            ):
                return self._failure(
                    request,
                    PlaneWaveStudyCompilationOutcome.INVALID,
                    PlaneWaveStudyCompilationFailureCode.TASK_INSTANCE_IDENTITY_CONFLICT,
                )
        return None

    def _reuse_failure(
        self, request: PlaneWaveStudyCompilationRequest
    ) -> PlaneWaveStudyCompilationFailure | None:
        """Require Task reuse exactly when complete role-specific content is equal."""
        bindings = request.candidate_bindings
        for left_index, left_candidate in enumerate(bindings):
            for right_candidate in bindings[left_index + 1 :]:
                for left, right in zip(
                    left_candidate.task_bindings,
                    right_candidate.task_bindings,
                    strict=True,
                ):
                    same_content = self._task_content_equal(left, right)
                    same_instance = left.task_instance == right.task_instance
                    if not same_content and same_instance:
                        return self._failure(
                            request,
                            PlaneWaveStudyCompilationOutcome.INVALID,
                            PlaneWaveStudyCompilationFailureCode.DISTINCT_TASK_CONTENT_SHARES_INSTANCE,
                        )
                    if same_content and not same_instance:
                        return self._failure(
                            request,
                            PlaneWaveStudyCompilationOutcome.INVALID,
                            PlaneWaveStudyCompilationFailureCode.IDENTICAL_TASK_CONTENT_NOT_REUSED,
                        )
        return None

    def _compile(
        self,
        request: PlaneWaveStudyCompilationRequest,
        roles: tuple[PlaneWaveStudyTaskRoleIdentity, ...],
    ) -> CompiledPlaneWaveStudy:
        """Construct Workflow, CPN, dependencies, reuse, and collection request."""
        unique_branches: list[PlaneWaveStudyCandidateBinding] = []
        canonical_for_candidate: list[PlaneWaveStudyCandidateBinding] = []
        for candidate in request.candidate_bindings:
            canonical = next(
                (
                    value
                    for value in unique_branches
                    if tuple(task.task_instance for task in value.task_bindings)
                    == tuple(task.task_instance for task in candidate.task_bindings)
                ),
                None,
            )
            if canonical is None:
                unique_branches.append(candidate)
                canonical = candidate
            canonical_for_candidate.append(canonical)
        compiled_by_task: dict[TaskInstanceIdentity, CompiledPlaneWaveStudyTask] = {}
        for branch in unique_branches:
            previous_transition: ColoredPetriNetTransitionIdentity | None = None
            for task in branch.task_bindings:
                transition = self._transition_identity(request, task.task_instance)
                gate_set = (
                    None
                    if previous_transition is None
                    else self._gate_set(
                        f"{task.task_instance.identity.value}.after-previous",
                        (previous_transition,),
                    )
                )
                compiled_instance = TaskInstance(
                    task.task_instance.identity,
                    task.task_instance.definition_identity,
                    gate_set,
                )
                compiled_by_task[task.task_instance.identity] = (
                    CompiledPlaneWaveStudyTask(
                        task.role_identity,
                        compiled_instance,
                        transition,
                        ColoredPetriNetPlaceIdentity(
                            f"{task.task_instance.identity.value}.completed"
                        ),
                    )
                )
                previous_transition = transition
        compiled_candidates = tuple(
            CompiledPlaneWaveStudyCandidate(
                candidate.candidate.identity,
                tuple(
                    compiled_by_task[task.task_instance.identity]
                    for task in canonical.task_bindings
                ),
            )
            for candidate, canonical in zip(
                request.candidate_bindings, canonical_for_candidate, strict=True
            )
        )
        unique_compiled_branches = tuple(
            next(
                value
                for value in compiled_candidates
                if value.candidate_identity == branch.candidate.identity
            )
            for branch in unique_branches
        )
        collection_transition = ColoredPetriNetTransitionIdentity(
            f"{request.workflow_identity.value}.collect"
        )
        analysis_transition = ColoredPetriNetTransitionIdentity(
            f"{request.workflow_identity.value}.analyze"
        )
        collection_task = TaskInstance(
            request.collection_task_instance.identity,
            request.collection_task_instance.definition_identity,
            self._gate_set(
                f"{request.collection_task_instance.identity.value}.after-branches",
                tuple(
                    value.tasks[-1].transition_identity
                    for value in unique_compiled_branches
                ),
            ),
        )
        analysis_task = TaskInstance(
            request.analysis_task_instance.identity,
            request.analysis_task_instance.definition_identity,
            self._gate_set(
                f"{request.analysis_task_instance.identity.value}.after-collection",
                (collection_transition,),
            ),
        )
        unique_tasks = tuple(
            task.task_instance
            for branch in unique_compiled_branches
            for task in branch.tasks
        )
        workflow = WorkflowComposition(
            request.workflow_identity, unique_tasks + (collection_task, analysis_task)
        )
        dependencies = (
            tuple(
                PlaneWaveStudyTaskDependency(
                    left.task_instance.identity, right.task_instance.identity
                )
                for branch in unique_compiled_branches
                for left, right in pairwise(branch.tasks)
            )
            + tuple(
                PlaneWaveStudyTaskDependency(
                    branch.tasks[-1].task_instance.identity, collection_task.identity
                )
                for branch in unique_compiled_branches
            )
            + (
                PlaneWaveStudyTaskDependency(
                    collection_task.identity, analysis_task.identity
                ),
            )
        )
        reuse = self._reuse_records(request.candidate_bindings)
        observation_request = ParameterStudyObservationCollectionRequest(
            request.observation_collection_identity,
            tuple(value.identity for value in request.revisions),
            tuple(value.candidate.identity for value in request.candidate_bindings),
            tuple(value.observation_role_identity for value in roles),
            tuple(
                ParameterStudyObservationReuse(
                    value.candidate_identity,
                    value.canonical_candidate_identity,
                    value.task_role_identity.observation_role_identity,
                    value.task_instance_identity,
                )
                for value in reuse
            ),
        )
        definition = self._definition(
            request,
            unique_branches,
            unique_compiled_branches,
            collection_transition,
            analysis_transition,
        )
        return CompiledPlaneWaveStudy(
            request,
            workflow,
            definition,
            self._initial_marking(
                request,
                definition,
                unique_branches,
                unique_compiled_branches,
            ),
            compiled_candidates,
            collection_task,
            collection_transition,
            analysis_task,
            analysis_transition,
            dependencies,
            reuse,
            observation_request,
        )

    def _definition(
        self,
        request: PlaneWaveStudyCompilationRequest,
        unique_bindings: list[PlaneWaveStudyCandidateBinding],
        unique_branches: tuple[CompiledPlaneWaveStudyCandidate, ...],
        collection_transition_identity: ColoredPetriNetTransitionIdentity,
        analysis_transition_identity: ColoredPetriNetTransitionIdentity,
    ) -> ColoredPetriNetDefinition:
        """Build generic ordered branches, all-branch collection, and analysis."""
        color = ColoredPetriNetColorDefinition(
            ColoredPetriNetColorIdentity("plane-wave-study-result-identity"),
            (ColoredPetriNetValueKind.STRING,),
        )
        places: list[ColoredPetriNetPlaceDefinition] = []
        transitions: list[ColoredPetriNetTransitionDefinition] = []
        arcs: list[ColoredPetriNetArcDefinition] = []
        output_places: list[ColoredPetriNetPlaceDefinition] = []
        for binding, branch in zip(unique_bindings, unique_branches, strict=True):
            previous_output: (
                tuple[
                    ColoredPetriNetPlaceDefinition,
                    ColoredPetriNetBindingVariableIdentity,
                ]
                | None
            ) = None
            for task_binding, compiled in zip(
                binding.task_bindings, branch.tasks, strict=True
            ):
                prepared = ColoredPetriNetPlaceDefinition(
                    ColoredPetriNetPlaceIdentity(
                        f"{task_binding.task_instance.identity.value}.prepared"
                    ),
                    (color.identity,),
                )
                completed = ColoredPetriNetPlaceDefinition(
                    compiled.result_place_identity,
                    (color.identity,),
                )
                places.extend((prepared, completed))
                prepared_variable = ColoredPetriNetBindingVariableIdentity(
                    f"{task_binding.task_instance.identity.value}.prepared-input"
                )
                output_variable = ColoredPetriNetBindingVariableIdentity(
                    f"{task_binding.task_instance.identity.value}.result"
                )
                input_variables: tuple[ColoredPetriNetBindingVariableIdentity, ...] = (
                    prepared_variable,
                )
                if previous_output is not None:
                    input_variables += (previous_output[1],)
                transition = self._transition(
                    compiled.transition_identity, input_variables, output_variable
                )
                transitions.append(transition)
                arcs.append(
                    self._input_arc(
                        f"{task_binding.task_instance.identity.value}.prepared-input",
                        prepared,
                        transition,
                        prepared_variable,
                        color,
                        ColoredPetriNetInputMode.CONSUME,
                    )
                )
                if previous_output is not None:
                    arcs.append(
                        self._input_arc(
                            f"{task_binding.task_instance.identity.value}.predecessor-result",
                            previous_output[0],
                            transition,
                            previous_output[1],
                            color,
                            ColoredPetriNetInputMode.READ,
                        )
                    )
                arcs.append(
                    self._output_arc(
                        f"{task_binding.task_instance.identity.value}.result",
                        completed,
                        transition,
                        output_variable,
                        color,
                    )
                )
                output_places.append(completed)
                previous_output = (completed, output_variable)
        collection_place = ColoredPetriNetPlaceDefinition(
            ColoredPetriNetPlaceIdentity(
                f"{request.observation_collection_identity.value}.completed"
            ),
            (color.identity,),
        )
        analysis_place = ColoredPetriNetPlaceDefinition(
            ColoredPetriNetPlaceIdentity(
                f"{request.analysis_task_instance.identity.value}.completed"
            ),
            (color.identity,),
        )
        places.extend((collection_place, analysis_place))
        collection_inputs = tuple(
            ColoredPetriNetBindingVariableIdentity(f"collection.source.{index}")
            for index in range(len(output_places))
        )
        collection_output = ColoredPetriNetBindingVariableIdentity(
            "collection.typed-result"
        )
        collection = self._transition(
            collection_transition_identity, collection_inputs, collection_output
        )
        for index, place in enumerate(output_places):
            arcs.append(
                self._input_arc(
                    f"collection.source.{index}",
                    place,
                    collection,
                    collection_inputs[index],
                    color,
                    ColoredPetriNetInputMode.CONSUME,
                )
            )
        arcs.append(
            self._output_arc(
                "collection.typed-result",
                collection_place,
                collection,
                collection_output,
                color,
            )
        )
        analysis_input = ColoredPetriNetBindingVariableIdentity(
            "analysis.typed-collection"
        )
        analysis_output = ColoredPetriNetBindingVariableIdentity("analysis.result")
        analysis = self._transition(
            analysis_transition_identity, (analysis_input,), analysis_output
        )
        arcs.extend(
            (
                self._input_arc(
                    "analysis.typed-collection",
                    collection_place,
                    analysis,
                    analysis_input,
                    color,
                    ColoredPetriNetInputMode.CONSUME,
                ),
                self._output_arc(
                    "analysis.result",
                    analysis_place,
                    analysis,
                    analysis_output,
                    color,
                ),
            )
        )
        transitions.extend((collection, analysis))
        priority = tuple(
            task.transition_identity
            for branch in unique_branches
            for task in branch.tasks
        ) + (collection_transition_identity, analysis_transition_identity)
        return ColoredPetriNetDefinition(
            request.definition_identity,
            (color,),
            tuple(places),
            tuple(transitions),
            tuple(arcs),
            priority,
        )

    @staticmethod
    def _initial_marking(
        request: PlaneWaveStudyCompilationRequest,
        definition: ColoredPetriNetDefinition,
        unique_bindings: list[PlaneWaveStudyCandidateBinding],
        unique_branches: tuple[CompiledPlaneWaveStudyCandidate, ...],
    ) -> ColoredPetriNetMarking:
        """Place exact native-configuration identities into prepared places."""
        color = definition.colors[0].identity
        tokens: dict[str, tuple[ColoredPetriNetToken, ...]] = {}
        for binding, branch in zip(unique_bindings, unique_branches, strict=True):
            for task_binding, _compiled in zip(
                binding.task_bindings, branch.tasks, strict=True
            ):
                place_value = f"{task_binding.task_instance.identity.value}.prepared"
                tokens[place_value] = (
                    ColoredPetriNetToken(
                        color,
                        ColoredPetriNetValue(
                            ColoredPetriNetValueKind.STRING,
                            task_binding.native_configuration_identity.value,
                        ),
                        ColoredPetriNetTokenIdentity(
                            f"{task_binding.task_instance.identity.value}.prepared-token"
                        ),
                    ),
                )
        return ColoredPetriNetMarking(
            request.initial_marking_identity,
            definition.identity,
            tuple(
                ColoredPetriNetPlaceMarking(
                    place.identity, tokens.get(place.identity.value, ())
                )
                for place in definition.places
            ),
        )

    @staticmethod
    def _task_content_equal(
        left: PlaneWaveStudyTaskBinding, right: PlaneWaveStudyTaskBinding
    ) -> bool:
        """Return equality of complete execution-defining Task content."""
        return (
            left.role_identity == right.role_identity
            and left.task_instance.definition_identity
            == right.task_instance.definition_identity
            and left.native_configuration_identity
            == right.native_configuration_identity
            and left.observation_requirement_identities
            == right.observation_requirement_identities
            and left.backend_binding == right.backend_binding
        )

    @staticmethod
    def _candidate_factor_agrees(binding: PlaneWaveStudyCandidateBinding) -> bool:
        """Check demonstrated cutoff or isotropic regular-mesh candidate binding."""
        factor_task = binding.task_for_role(binding.factor_task_role_identity)
        if factor_task is None or factor_task.backend_binding is None:
            return False
        specification = factor_task.backend_binding.specification
        candidate = binding.candidate
        if candidate.factor_name == "wavefunction_cutoff":
            cutoff = specification.wavefunction_cutoff
            return (
                candidate.unit == "electron_volt"
                and cutoff.unit is UnitIdentity.ELECTRON_VOLT
                and candidate.value == cutoff.value
            )
        if candidate.factor_name == "reciprocal_mesh_axis_count":
            counts = specification.reciprocal_mesh.axis_counts
            return (
                candidate.unit == "points_per_axis"
                and counts[0] == counts[1] == counts[2]
                and candidate.value == float(counts[0])
            )
        return False

    @staticmethod
    def _transition_identity(
        request: PlaneWaveStudyCompilationRequest, task: TaskInstance
    ) -> ColoredPetriNetTransitionIdentity:
        """Derive one deterministic transition identity from exact Task identity."""
        return ColoredPetriNetTransitionIdentity(
            f"{request.workflow_identity.value}.{task.identity.value}.transition"
        )

    @staticmethod
    def _gate_set(
        identity: str,
        transitions: tuple[ColoredPetriNetTransitionIdentity, ...],
    ) -> TaskStartGateSet:
        """Build one all-of gate set in exact transition order."""
        return TaskStartGateSet(
            TaskStartGateSetIdentity(identity),
            TaskStartGateSetMode.ALL_OF,
            tuple(
                TaskStartGate(
                    TaskStartGateIdentity(f"{identity}.{index}"), index, transition
                )
                for index, transition in enumerate(transitions)
            ),
        )

    @staticmethod
    def _transition(
        identity: ColoredPetriNetTransitionIdentity,
        inputs: tuple[ColoredPetriNetBindingVariableIdentity, ...],
        output: ColoredPetriNetBindingVariableIdentity,
    ) -> ColoredPetriNetTransitionDefinition:
        """Build one unconditional transition with one external output."""
        return ColoredPetriNetTransitionDefinition(
            identity,
            inputs,
            (output,),
            ColoredPetriNetGuardExpression(ColoredPetriNetGuardOperator.TRUE),
        )

    @staticmethod
    def _input_arc(
        identity: str,
        place: ColoredPetriNetPlaceDefinition,
        transition: ColoredPetriNetTransitionDefinition,
        variable: ColoredPetriNetBindingVariableIdentity,
        color: ColoredPetriNetColorDefinition,
        mode: ColoredPetriNetInputMode,
    ) -> ColoredPetriNetArcDefinition:
        """Build one exact input arc."""
        return ColoredPetriNetArcDefinition(
            ColoredPetriNetArcIdentity(identity),
            place.identity,
            transition.identity,
            ColoredPetriNetInputInscription(
                mode,
                (ColoredPetriNetTokenPattern(variable, (color.identity,)),),
            ),
        )

    @staticmethod
    def _output_arc(
        identity: str,
        place: ColoredPetriNetPlaceDefinition,
        transition: ColoredPetriNetTransitionDefinition,
        variable: ColoredPetriNetBindingVariableIdentity,
        color: ColoredPetriNetColorDefinition,
    ) -> ColoredPetriNetArcDefinition:
        """Build one exact externally supplied result-output arc."""
        expression = ColoredPetriNetValueExpression(
            ColoredPetriNetValueExpressionKind.VARIABLE,
            variable_identity=variable,
        )
        return ColoredPetriNetArcDefinition(
            ColoredPetriNetArcIdentity(identity),
            place.identity,
            transition.identity,
            output_inscription=ColoredPetriNetOutputInscription(
                (ColoredPetriNetTokenTemplate(color.identity, expression, expression),)
            ),
        )

    @classmethod
    def _reuse_records(
        cls,
        bindings: tuple[PlaneWaveStudyCandidateBinding, ...],
    ) -> tuple[PlaneWaveStudyTaskReuse, ...]:
        """Return exact per-role reuse records in candidate and Task order."""
        result: list[PlaneWaveStudyTaskReuse] = []
        for index, binding in enumerate(bindings):
            for task in binding.task_bindings:
                for canonical_candidate in bindings[:index]:
                    canonical_task = canonical_candidate.task_for_role(
                        task.role_identity
                    )
                    if canonical_task is not None and cls._task_content_equal(
                        canonical_task, task
                    ):
                        result.append(
                            PlaneWaveStudyTaskReuse(
                                binding.candidate.identity,
                                canonical_candidate.candidate.identity,
                                task.role_identity,
                                task.task_instance.identity,
                            )
                        )
                        break
        return tuple(result)

    def _failure(
        self,
        request: PlaneWaveStudyCompilationRequest,
        outcome: PlaneWaveStudyCompilationOutcome,
        code: PlaneWaveStudyCompilationFailureCode,
    ) -> PlaneWaveStudyCompilationFailure:
        """Return one failure correlated to exact request and compiler identity."""
        return PlaneWaveStudyCompilationFailure(request, self.identity, outcome, code)
