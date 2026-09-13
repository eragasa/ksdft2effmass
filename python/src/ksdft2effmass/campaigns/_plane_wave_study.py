"""Private effect-free compiler for one plane-wave parameter-study probe.

Compilation validates explicit QoI-to-observation mappings, complete candidate and
backend bindings, Task-instance composition, dependencies, and reuse. It performs no
Task invocation, calculator execution, normalization, or scientific acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.analysis._parameter_study import (
    NormalizedObservationRequirementIdentity,
    ParameterStudyCandidate,
    ParameterStudyCandidateIdentity,
    ParameterStudyRevision,
    ParameterStudySubjectIdentity,
    QuantityOfInterestDefinition,
)
from ksdft2effmass.calculators.dft.pw import (
    PlaneWaveBackendBinding,
    PlaneWaveEnergyUnit,
    PlaneWaveObservationRequirementIdentity,
    PlaneWavePhysicalModelIdentity,
)
from ksdft2effmass.workflows import (
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowComposition,
    WorkflowIdentity,
)


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCompilerIdentity:
    """Nominal identity and version of one study compiler implementation."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("compiler identity value must be a string")
        if not self.value:
            raise ValueError("compiler identity value must not be empty")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCompilationIdentity:
    """Nominal identity of one study compilation operation."""

    value: str

    def __post_init__(self) -> None:
        """Validate the owner-local identity."""
        if type(self.value) is not str:
            raise TypeError("compilation identity value must be a string")
        if not self.value:
            raise ValueError("compilation identity value must not be empty")


class PlaneWaveStudyCompilationOutcome(StrEnum):
    """Closed result kind of effect-free study compilation."""

    COMPILED = "compiled"
    UNSUPPORTED = "unsupported"
    INCOMPATIBLE = "incompatible"
    INVALID = "invalid"
    ERROR = "error"


class PlaneWaveStudyCompilationFailureCode(StrEnum):
    """Stable fail-closed study compilation codes."""

    COMPILER_IDENTITY_MISMATCH = "compiler_identity_mismatch"
    CANDIDATE_BINDING_COUNT_MISMATCH = "candidate_binding_count_mismatch"
    CANDIDATE_BINDING_ORDER_MISMATCH = "candidate_bindings_must_follow_revision_order"
    CANDIDATE_SUBJECT_MISMATCH = "candidate_subject_binding_mismatch"
    PHYSICAL_MODEL_MISMATCH = "physical_model_binding_mismatch"
    CANDIDATE_CUTOFF_MISMATCH = "candidate_cutoff_binding_mismatch"
    QOI_BINDING_COVERAGE_MISMATCH = "qoi_binding_coverage_mismatch"
    QOI_OBSERVATION_MAPPING_MISMATCH = "qoi_observation_mapping_mismatch"
    REQUIRED_OBSERVATION_MISSING = "required_observation_missing"
    BACKEND_BINDING_IDENTITY_CONFLICT = "backend_binding_identity_content_conflict"
    DISTINCT_BINDINGS_SHARE_TASK = "distinct_backend_bindings_share_task_instance"
    IDENTICAL_BINDING_NOT_REUSED = "identical_backend_binding_requires_task_reuse"
    DEPENDENCY_TASK_MISSING = "dependency_task_instance_missing"
    DEPENDENCY_SELF_REFERENCE = "dependency_self_reference"
    DEPENDENCY_DUPLICATE = "dependency_duplicate"
    TASK_INSTANCE_IDENTITY_CONFLICT = "task_instance_identity_content_conflict"


@dataclass(frozen=True, slots=True)
class PlaneWaveStudySubjectBinding:
    """Explicitly bind analysis subject and calculator physical-model identities."""

    study_subject_identity: ParameterStudySubjectIdentity
    physical_model_identity: PlaneWavePhysicalModelIdentity

    def __post_init__(self) -> None:
        """Validate both nominal identities without equating their strings."""
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
    """Explicitly bind one analysis requirement to calculator vocabulary."""

    analysis_requirement_identity: NormalizedObservationRequirementIdentity
    calculator_requirement_identity: PlaneWaveObservationRequirementIdentity

    def __post_init__(self) -> None:
        """Validate distinct nominal requirement identities."""
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
    """Bind one QoI definition to its calculator observation requirements."""

    definition: QuantityOfInterestDefinition
    observation_bindings: tuple[PlaneWaveObservationRequirementBinding, ...]

    def __post_init__(self) -> None:
        """Validate intrinsic mapping field types and uniqueness."""
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
        if len(
            {item.analysis_requirement_identity for item in self.observation_bindings}
        ) != len(self.observation_bindings):
            raise ValueError("analysis observation bindings must be unique")
        if len(
            {item.calculator_requirement_identity for item in self.observation_bindings}
        ) != len(self.observation_bindings):
            raise ValueError("calculator observation bindings must be unique")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCandidateBinding:
    """Bind one study candidate to one exact backend binding and Task instance."""

    candidate: ParameterStudyCandidate
    backend_binding: PlaneWaveBackendBinding
    task_instance: TaskInstance

    def __post_init__(self) -> None:
        """Validate exact candidate-binding fields."""
        if type(self.candidate) is not ParameterStudyCandidate:
            raise TypeError("candidate must be ParameterStudyCandidate")
        if type(self.backend_binding) is not PlaneWaveBackendBinding:
            raise TypeError("backend_binding must be PlaneWaveBackendBinding")
        if type(self.task_instance) is not TaskInstance:
            raise TypeError("task_instance must be TaskInstance")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyTaskDependency:
    """Explicit directed dependency between two compiled Task instances."""

    upstream_identity: TaskInstanceIdentity
    downstream_identity: TaskInstanceIdentity

    def __post_init__(self) -> None:
        """Validate exact dependency identities and reject self-dependency."""
        if type(self.upstream_identity) is not TaskInstanceIdentity:
            raise TypeError("upstream_identity must be TaskInstanceIdentity")
        if type(self.downstream_identity) is not TaskInstanceIdentity:
            raise TypeError("downstream_identity must be TaskInstanceIdentity")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyTaskReuse:
    """Record one candidate's explicit reuse of a prior candidate Task instance."""

    candidate_identity: ParameterStudyCandidateIdentity
    canonical_candidate_identity: ParameterStudyCandidateIdentity
    task_instance_identity: TaskInstanceIdentity

    def __post_init__(self) -> None:
        """Validate reuse identities without inferring scientific equivalence."""
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
        if type(self.task_instance_identity) is not TaskInstanceIdentity:
            raise TypeError("task_instance_identity must be TaskInstanceIdentity")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCompilationRequest:
    """Exact inputs to one effect-free parameter-study compilation."""

    identity: PlaneWaveStudyCompilationIdentity
    compiler_identity: PlaneWaveStudyCompilerIdentity
    workflow_identity: WorkflowIdentity
    revision: ParameterStudyRevision
    subject_binding: PlaneWaveStudySubjectBinding
    quantity_bindings: tuple[PlaneWaveQuantityOfInterestBinding, ...]
    candidate_bindings: tuple[PlaneWaveStudyCandidateBinding, ...]
    task_dependencies: tuple[PlaneWaveStudyTaskDependency, ...]

    def __post_init__(self) -> None:
        """Validate request types; compatibility remains compiler-owned."""
        if type(self.identity) is not PlaneWaveStudyCompilationIdentity:
            raise TypeError("identity must be PlaneWaveStudyCompilationIdentity")
        if type(self.compiler_identity) is not PlaneWaveStudyCompilerIdentity:
            raise TypeError("compiler_identity must be PlaneWaveStudyCompilerIdentity")
        if type(self.workflow_identity) is not WorkflowIdentity:
            raise TypeError("workflow_identity must be WorkflowIdentity")
        if type(self.revision) is not ParameterStudyRevision:
            raise TypeError("revision must be ParameterStudyRevision")
        if type(self.subject_binding) is not PlaneWaveStudySubjectBinding:
            raise TypeError("subject_binding must be PlaneWaveStudySubjectBinding")
        if type(self.quantity_bindings) is not tuple or any(
            type(item) is not PlaneWaveQuantityOfInterestBinding
            for item in self.quantity_bindings
        ):
            raise TypeError(
                "quantity_bindings must be a tuple of "
                "PlaneWaveQuantityOfInterestBinding"
            )
        if type(self.candidate_bindings) is not tuple or any(
            type(item) is not PlaneWaveStudyCandidateBinding
            for item in self.candidate_bindings
        ):
            raise TypeError(
                "candidate_bindings must be a tuple of PlaneWaveStudyCandidateBinding"
            )
        if type(self.task_dependencies) is not tuple or any(
            type(item) is not PlaneWaveStudyTaskDependency
            for item in self.task_dependencies
        ):
            raise TypeError(
                "task_dependencies must be a tuple of PlaneWaveStudyTaskDependency"
            )


@dataclass(frozen=True, slots=True)
class CompiledPlaneWaveStudy:
    """Complete correlated Task plan for one immutable parameter-study revision."""

    request: PlaneWaveStudyCompilationRequest
    workflow_composition: WorkflowComposition
    reuse: tuple[PlaneWaveStudyTaskReuse, ...]

    def __post_init__(self) -> None:
        """Validate the complete private compiled plan."""
        if type(self.request) is not PlaneWaveStudyCompilationRequest:
            raise TypeError("request must be PlaneWaveStudyCompilationRequest")
        if type(self.workflow_composition) is not WorkflowComposition:
            raise TypeError("workflow_composition must be WorkflowComposition")
        if type(self.reuse) is not tuple or any(
            type(item) is not PlaneWaveStudyTaskReuse for item in self.reuse
        ):
            raise TypeError("reuse must be a tuple of PlaneWaveStudyTaskReuse")


@dataclass(frozen=True, slots=True)
class PlaneWaveStudyCompilationCompiled:
    """Represent successful complete parameter-study compilation."""

    outcome: PlaneWaveStudyCompilationOutcome
    study: CompiledPlaneWaveStudy

    def __post_init__(self) -> None:
        """Validate the closed success result."""
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
        """Validate the exact correlation and closed failure result."""
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
"""Closed private result of compiling one immutable parameter-study revision."""


@dataclass(frozen=True, slots=True)
class PlaneWaveParameterStudyCompiler:
    """Compile exact study-to-backend bindings without executing any Task."""

    identity: PlaneWaveStudyCompilerIdentity

    def __post_init__(self) -> None:
        """Validate the exact compiler implementation identity."""
        if type(self.identity) is not PlaneWaveStudyCompilerIdentity:
            raise TypeError("identity must be PlaneWaveStudyCompilerIdentity")

    def execute(
        self, request: PlaneWaveStudyCompilationRequest
    ) -> PlaneWaveStudyCompilationResult:
        """Return a complete correlated Task plan or one represented failure."""
        if type(request) is not PlaneWaveStudyCompilationRequest:
            raise TypeError("request must be PlaneWaveStudyCompilationRequest")
        if request.compiler_identity != self.identity:
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.COMPILER_IDENTITY_MISMATCH,
            )
        expected_candidates = request.revision.candidates
        bindings = request.candidate_bindings
        if len(bindings) != len(expected_candidates):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.CANDIDATE_BINDING_COUNT_MISMATCH,
            )
        if tuple(item.candidate for item in bindings) != expected_candidates:
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.CANDIDATE_BINDING_ORDER_MISMATCH,
            )
        if any(
            item.candidate.subject_identity
            != request.subject_binding.study_subject_identity
            for item in bindings
        ):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
                PlaneWaveStudyCompilationFailureCode.CANDIDATE_SUBJECT_MISMATCH,
            )
        if any(
            item.backend_binding.specification.physical_model_identity
            != request.subject_binding.physical_model_identity
            for item in bindings
        ):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
                PlaneWaveStudyCompilationFailureCode.PHYSICAL_MODEL_MISMATCH,
            )
        if any(not self._candidate_cutoff_agrees(item) for item in bindings):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
                PlaneWaveStudyCompilationFailureCode.CANDIDATE_CUTOFF_MISMATCH,
            )
        quantity_failure = self._quantity_failure(request)
        if quantity_failure is not None:
            return quantity_failure
        identity_failure = self._binding_identity_failure(request, bindings)
        if identity_failure is not None:
            return identity_failure
        task_identity_failure = self._task_identity_failure(request, bindings)
        if task_identity_failure is not None:
            return task_identity_failure
        task_failure = self._task_reuse_failure(request, bindings)
        if task_failure is not None:
            return task_failure
        task_instances = self._unique_task_instances(bindings)
        dependency_failure = self._dependency_failure(
            request, request.task_dependencies, task_instances
        )
        if dependency_failure is not None:
            return dependency_failure
        composition = WorkflowComposition(request.workflow_identity, task_instances)
        return PlaneWaveStudyCompilationCompiled(
            PlaneWaveStudyCompilationOutcome.COMPILED,
            CompiledPlaneWaveStudy(
                request,
                composition,
                self._reuse_records(bindings),
            ),
        )

    def _quantity_failure(
        self, request: PlaneWaveStudyCompilationRequest
    ) -> PlaneWaveStudyCompilationFailure | None:
        """Return a QoI coverage or observation mapping failure when present."""
        criterion_ids = tuple(
            criterion.quantity_identity for criterion in request.revision.criteria
        )
        definition_ids = tuple(
            binding.definition.identity for binding in request.quantity_bindings
        )
        if definition_ids != criterion_ids:
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.QOI_BINDING_COVERAGE_MISMATCH,
            )
        required_calculator_observations: set[
            PlaneWaveObservationRequirementIdentity
        ] = set()
        for binding in request.quantity_bindings:
            analysis_ids = tuple(
                item.analysis_requirement_identity
                for item in binding.observation_bindings
            )
            if analysis_ids != binding.definition.observation_requirement_identities:
                return self._failure(
                    request,
                    PlaneWaveStudyCompilationOutcome.INCOMPATIBLE,
                    PlaneWaveStudyCompilationFailureCode.QOI_OBSERVATION_MAPPING_MISMATCH,
                )
            required_calculator_observations.update(
                item.calculator_requirement_identity
                for item in binding.observation_bindings
            )
        if any(
            not required_calculator_observations.issubset(
                item.backend_binding.specification.observation_requirement_identities
            )
            for item in request.candidate_bindings
        ):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.UNSUPPORTED,
                PlaneWaveStudyCompilationFailureCode.REQUIRED_OBSERVATION_MISSING,
            )
        return None

    def _binding_identity_failure(
        self,
        request: PlaneWaveStudyCompilationRequest,
        bindings: tuple[PlaneWaveStudyCandidateBinding, ...],
    ) -> PlaneWaveStudyCompilationFailure | None:
        """Reject one nominal binding identity assigned to unequal content."""
        for left_index, left in enumerate(bindings):
            if any(
                right.backend_binding.identity == left.backend_binding.identity
                and right.backend_binding != left.backend_binding
                for right in bindings[left_index + 1 :]
            ):
                return self._failure(
                    request,
                    PlaneWaveStudyCompilationOutcome.INVALID,
                    PlaneWaveStudyCompilationFailureCode.BACKEND_BINDING_IDENTITY_CONFLICT,
                )
        return None

    def _task_identity_failure(
        self,
        request: PlaneWaveStudyCompilationRequest,
        bindings: tuple[PlaneWaveStudyCandidateBinding, ...],
    ) -> PlaneWaveStudyCompilationFailure | None:
        """Reject one Task-instance identity assigned to unequal instance content."""
        for left_index, left in enumerate(bindings):
            if any(
                right.task_instance.identity == left.task_instance.identity
                and right.task_instance != left.task_instance
                for right in bindings[left_index + 1 :]
            ):
                return self._failure(
                    request,
                    PlaneWaveStudyCompilationOutcome.INVALID,
                    PlaneWaveStudyCompilationFailureCode.TASK_INSTANCE_IDENTITY_CONFLICT,
                )
        return None

    def _task_reuse_failure(
        self,
        request: PlaneWaveStudyCompilationRequest,
        bindings: tuple[PlaneWaveStudyCandidateBinding, ...],
    ) -> PlaneWaveStudyCompilationFailure | None:
        """Require Task reuse exactly when complete backend bindings are equal."""
        for left_index, left in enumerate(bindings):
            for right in bindings[left_index + 1 :]:
                same_binding = right.backend_binding == left.backend_binding
                same_task = right.task_instance == left.task_instance
                if not same_binding and same_task:
                    return self._failure(
                        request,
                        PlaneWaveStudyCompilationOutcome.INVALID,
                        PlaneWaveStudyCompilationFailureCode.DISTINCT_BINDINGS_SHARE_TASK,
                    )
                if same_binding and not same_task:
                    return self._failure(
                        request,
                        PlaneWaveStudyCompilationOutcome.INVALID,
                        PlaneWaveStudyCompilationFailureCode.IDENTICAL_BINDING_NOT_REUSED,
                    )
        return None

    def _dependency_failure(
        self,
        request: PlaneWaveStudyCompilationRequest,
        dependencies: tuple[PlaneWaveStudyTaskDependency, ...],
        task_instances: tuple[TaskInstance, ...],
    ) -> PlaneWaveStudyCompilationFailure | None:
        """Validate dependency membership, self-reference, and uniqueness."""
        task_ids = {item.identity for item in task_instances}
        if any(
            item.upstream_identity not in task_ids
            or item.downstream_identity not in task_ids
            for item in dependencies
        ):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.DEPENDENCY_TASK_MISSING,
            )
        if any(
            item.upstream_identity == item.downstream_identity for item in dependencies
        ):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.DEPENDENCY_SELF_REFERENCE,
            )
        if len(set(dependencies)) != len(dependencies):
            return self._failure(
                request,
                PlaneWaveStudyCompilationOutcome.INVALID,
                PlaneWaveStudyCompilationFailureCode.DEPENDENCY_DUPLICATE,
            )
        return None

    @staticmethod
    def _unique_task_instances(
        bindings: tuple[PlaneWaveStudyCandidateBinding, ...],
    ) -> tuple[TaskInstance, ...]:
        """Return Task instances in first-use order after exact reuse validation."""
        result: list[TaskInstance] = []
        for binding in bindings:
            if binding.task_instance not in result:
                result.append(binding.task_instance)
        return tuple(result)

    @staticmethod
    def _reuse_records(
        bindings: tuple[PlaneWaveStudyCandidateBinding, ...],
    ) -> tuple[PlaneWaveStudyTaskReuse, ...]:
        """Return explicit reuse edges for repeated complete backend bindings."""
        result: list[PlaneWaveStudyTaskReuse] = []
        for index, binding in enumerate(bindings):
            for canonical in bindings[:index]:
                if canonical.backend_binding == binding.backend_binding:
                    result.append(
                        PlaneWaveStudyTaskReuse(
                            binding.candidate.identity,
                            canonical.candidate.identity,
                            binding.task_instance.identity,
                        )
                    )
                    break
        return tuple(result)

    @staticmethod
    def _candidate_cutoff_agrees(binding: PlaneWaveStudyCandidateBinding) -> bool:
        """Return exact value/unit agreement for the initial cutoff-only probe."""
        cutoff = binding.backend_binding.specification.wavefunction_cutoff
        unit = {
            PlaneWaveEnergyUnit.HARTREE: "hartree",
            PlaneWaveEnergyUnit.RYDBERG: "rydberg",
            PlaneWaveEnergyUnit.ELECTRON_VOLT: "electron_volt",
        }[cutoff.unit]
        return (
            binding.candidate.value == cutoff.value and binding.candidate.unit == unit
        )

    def _failure(
        self,
        request: PlaneWaveStudyCompilationRequest,
        outcome: PlaneWaveStudyCompilationOutcome,
        code: PlaneWaveStudyCompilationFailureCode,
    ) -> PlaneWaveStudyCompilationFailure:
        """Return one failure correlated to the exact request and compiler."""
        return PlaneWaveStudyCompilationFailure(request, self.identity, outcome, code)
