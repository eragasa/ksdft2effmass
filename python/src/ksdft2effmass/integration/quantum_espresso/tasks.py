"""Operation-specific Quantum ESPRESSO scientific Task adapters.

The four public Task classes bind one exact immutable QE execution input to one
explicitly injected backend-neutral plane-wave calculator port.  SCF has no
predecessor.  NSCF, band-path, and bands-extraction Tasks require one mechanically
completed predecessor result whose exact native-state artifact is identified by the
new execution input.

These adapters validate operation, predecessor, and Workflow correlation boundaries
and return existing QE mechanical ResultObjects.  They implement no workspace,
process, parsing, artifact-discovery, retry, authorization, numerical-acceptance, or
scientific-acceptance behavior.  External effects remain behind the injected
``PlaneWaveCalculator`` implementation and require separately established authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from ksdft2effmass.calculators.dft.pw import PlaneWaveCalculator
from ksdft2effmass.workflows import (
    ResultObject,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
)

from .contracts import (
    QuantumEspressoBandsResult,
    QuantumEspressoCompletedOutcome,
    QuantumEspressoExecutionInput,
    QuantumEspressoProgram,
    QuantumEspressoPwResult,
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoScfTask:
    """Execute one exact QE self-consistent-field operation.

    Parameters
    ----------
    simulation_input
        Exact ``pw`` execution input.  It must identify this Task definition and
        contain no predecessor native state.
    calculator
        Explicit backend-neutral calculator port bound to QE input and ``pw`` result
        types.  The adapter invokes it only after validating its empty predecessor
        binding and exact Workflow correlation context.

    Notes
    -----
    The fixed Task-definition identity is ``quantum-espresso.scf.v1``.  Returning a
    mechanically completed result does not establish numerical convergence or
    scientific acceptance.
    """

    simulation_input: QuantumEspressoExecutionInput
    calculator: PlaneWaveCalculator[
        QuantumEspressoExecutionInput, QuantumEspressoPwResult
    ]

    _IDENTITY: ClassVar[TaskDefinitionIdentity] = TaskDefinitionIdentity(
        "quantum-espresso.scf.v1"
    )

    def __post_init__(self) -> None:
        """Validate the operation-specific input and injected calculator boundary."""
        if type(self.simulation_input) is not QuantumEspressoExecutionInput:
            raise TypeError("simulation_input must be QuantumEspressoExecutionInput")
        if not isinstance(self.calculator, PlaneWaveCalculator):
            raise TypeError("calculator must implement PlaneWaveCalculator")
        if self.simulation_input.program is not QuantumEspressoProgram.PW:
            raise ValueError("SCF input must use the pw program role")
        if self.simulation_input.task_definition_identity != self.identity:
            raise ValueError("SCF input must identify the SCF Task definition")
        if self.simulation_input.predecessor_native_state:
            raise ValueError("SCF input must not contain predecessor native state")

    @property
    def identity(self) -> TaskDefinitionIdentity:
        """Return the fixed reusable SCF Task-definition identity."""
        return self._IDENTITY

    def execute(
        self,
        inputs: tuple[TaskInputBinding, ...],
        context: TaskExecutionContext,
    ) -> tuple[ResultObject, ...]:
        """Validate and delegate one SCF operation to the injected calculator.

        Parameters
        ----------
        inputs
            Exactly the empty tuple because SCF has no predecessor result.
        context
            Exact Workflow context matching the Task-instance, activation,
            operation, and attempt identities in ``simulation_input``.

        Returns
        -------
        tuple[ResultObject, ...]
            One newly returned :class:`QuantumEspressoPwResult`.

        Raises
        ------
        TypeError
            If an argument, calculator result, or structural boundary has the wrong
            semantic type.
        ValueError
            If predecessor, context, or returned-input correlations disagree.
        """
        if type(inputs) is not tuple or any(
            type(item) is not TaskInputBinding for item in inputs
        ):
            raise TypeError("inputs must be a tuple of TaskInputBinding")
        if inputs:
            raise ValueError("SCF Task requires no predecessor input bindings")
        self._validate_context(context)
        result = self.calculator.execute(self.simulation_input, context)
        if type(result) is not QuantumEspressoPwResult:
            raise TypeError("SCF calculator must return QuantumEspressoPwResult")
        if result.evidence.execution_input != self.simulation_input:
            raise ValueError("SCF result must identify the exact execution input")
        return (result,)

    def _validate_context(self, context: TaskExecutionContext) -> None:
        """Require exact run-scoped correlations before calculator delegation."""
        if type(context) is not TaskExecutionContext:
            raise TypeError("context must be TaskExecutionContext")
        expected = (
            (
                context.task_instance_identity,
                self.simulation_input.task_instance_identity,
            ),
            (
                context.task_activation_identity,
                self.simulation_input.activation_identity,
            ),
            (context.operation_identity, self.simulation_input.operation_identity),
            (context.attempt_identity, self.simulation_input.attempt_identity),
        )
        if any(actual != required for actual, required in expected):
            raise ValueError("SCF context must match the execution input correlations")


@dataclass(frozen=True, slots=True)
class QuantumEspressoNscfTask:
    """Execute one exact QE non-self-consistent-field operation.

    Parameters
    ----------
    simulation_input
        Exact ``pw`` execution input identifying this Task definition and exactly one
        staged predecessor native state.
    calculator
        Explicit backend-neutral calculator port bound to QE input and ``pw`` result
        types.

    Notes
    -----
    The fixed Task-definition identity is ``quantum-espresso.nscf.v1``.  The required
    input binding is named ``scf_result`` and must contain a mechanically completed
    :class:`QuantumEspressoPwResult` matching the staged native state.
    """

    simulation_input: QuantumEspressoExecutionInput
    calculator: PlaneWaveCalculator[
        QuantumEspressoExecutionInput, QuantumEspressoPwResult
    ]

    _IDENTITY: ClassVar[TaskDefinitionIdentity] = TaskDefinitionIdentity(
        "quantum-espresso.nscf.v1"
    )

    def __post_init__(self) -> None:
        """Validate the NSCF input shape and injected calculator boundary."""
        if type(self.simulation_input) is not QuantumEspressoExecutionInput:
            raise TypeError("simulation_input must be QuantumEspressoExecutionInput")
        if not isinstance(self.calculator, PlaneWaveCalculator):
            raise TypeError("calculator must implement PlaneWaveCalculator")
        if self.simulation_input.program is not QuantumEspressoProgram.PW:
            raise ValueError("NSCF input must use the pw program role")
        if self.simulation_input.task_definition_identity != self.identity:
            raise ValueError("NSCF input must identify the NSCF Task definition")
        if len(self.simulation_input.predecessor_native_state) != 1:
            raise ValueError("NSCF input requires exactly one predecessor native state")

    @property
    def identity(self) -> TaskDefinitionIdentity:
        """Return the fixed reusable NSCF Task-definition identity."""
        return self._IDENTITY

    def execute(
        self,
        inputs: tuple[TaskInputBinding, ...],
        context: TaskExecutionContext,
    ) -> tuple[ResultObject, ...]:
        """Validate the admitted SCF predecessor and delegate one NSCF operation.

        Parameters
        ----------
        inputs
            Exactly one ``scf_result`` binding containing a mechanically completed
            :class:`QuantumEspressoPwResult`.
        context
            Exact Workflow context matching ``simulation_input``.

        Returns
        -------
        tuple[ResultObject, ...]
            One newly returned :class:`QuantumEspressoPwResult`.

        Raises
        ------
        TypeError
            If an argument, predecessor, calculator result, or structural boundary
            has the wrong semantic type.
        ValueError
            If predecessor, native-state, context, or returned-input correlations
            disagree.
        """
        self._validate_predecessor(inputs)
        self._validate_context(context)
        result = self.calculator.execute(self.simulation_input, context)
        if type(result) is not QuantumEspressoPwResult:
            raise TypeError("NSCF calculator must return QuantumEspressoPwResult")
        if result.evidence.execution_input != self.simulation_input:
            raise ValueError("NSCF result must identify the exact execution input")
        return (result,)

    def _validate_predecessor(
        self, inputs: tuple[TaskInputBinding, ...]
    ) -> QuantumEspressoPwResult:
        """Require one completed SCF result matching the staged native state."""
        if type(inputs) is not tuple or any(
            type(item) is not TaskInputBinding for item in inputs
        ):
            raise TypeError("inputs must be a tuple of TaskInputBinding")
        if len(inputs) != 1 or inputs[0].name != "scf_result":
            raise ValueError("NSCF Task requires exactly one scf_result binding")
        predecessor = inputs[0].result
        if type(predecessor) is not QuantumEspressoPwResult:
            raise TypeError("scf_result must be QuantumEspressoPwResult")
        self._validate_predecessor_state(predecessor)
        return predecessor

    def _validate_predecessor_state(self, predecessor: QuantumEspressoPwResult) -> None:
        """Require completed evidence and exact native-state provenance closure."""
        if type(predecessor.evidence.calculator_outcome) is not (
            QuantumEspressoCompletedOutcome
        ):
            raise ValueError("NSCF predecessor must be mechanically completed")
        state = self.simulation_input.predecessor_native_state[0]
        if state.predecessor_result_identity != predecessor.identity:
            raise ValueError("NSCF native state must identify the SCF result")
        if (
            state.content.manifest_identity
            != predecessor.evidence.native_output_manifest_identity
            or state.predecessor_manifest_entry_identity
            not in predecessor.evidence.native_output_entry_identities
            or state.predecessor_manifest_entry_identity
            not in state.content.manifest_entry_identities
        ):
            raise ValueError("NSCF native state must belong to the SCF result manifest")

    def _validate_context(self, context: TaskExecutionContext) -> None:
        """Require exact run-scoped correlations before calculator delegation."""
        if type(context) is not TaskExecutionContext:
            raise TypeError("context must be TaskExecutionContext")
        expected = (
            (
                context.task_instance_identity,
                self.simulation_input.task_instance_identity,
            ),
            (
                context.task_activation_identity,
                self.simulation_input.activation_identity,
            ),
            (context.operation_identity, self.simulation_input.operation_identity),
            (context.attempt_identity, self.simulation_input.attempt_identity),
        )
        if any(actual != required for actual, required in expected):
            raise ValueError("NSCF context must match the execution input correlations")


@dataclass(frozen=True, slots=True)
class QuantumEspressoBandPathTask:
    """Execute one exact QE band-path ``pw`` operation.

    Parameters
    ----------
    simulation_input
        Exact ``pw`` execution input identifying this Task definition and exactly one
        staged predecessor native state.
    calculator
        Explicit backend-neutral calculator port bound to QE input and ``pw`` result
        types.

    Notes
    -----
    The fixed Task-definition identity is ``quantum-espresso.band-path.v1``.  The
    required ``predecessor_result`` binding may represent the explicitly composed SCF
    or NSCF parent, but it must be mechanically completed and exactly match the staged
    native state.
    """

    simulation_input: QuantumEspressoExecutionInput
    calculator: PlaneWaveCalculator[
        QuantumEspressoExecutionInput, QuantumEspressoPwResult
    ]

    _IDENTITY: ClassVar[TaskDefinitionIdentity] = TaskDefinitionIdentity(
        "quantum-espresso.band-path.v1"
    )

    def __post_init__(self) -> None:
        """Validate the band-path input shape and injected calculator boundary."""
        if type(self.simulation_input) is not QuantumEspressoExecutionInput:
            raise TypeError("simulation_input must be QuantumEspressoExecutionInput")
        if not isinstance(self.calculator, PlaneWaveCalculator):
            raise TypeError("calculator must implement PlaneWaveCalculator")
        if self.simulation_input.program is not QuantumEspressoProgram.PW:
            raise ValueError("band-path input must use the pw program role")
        if self.simulation_input.task_definition_identity != self.identity:
            raise ValueError(
                "band-path input must identify the band-path Task definition"
            )
        if len(self.simulation_input.predecessor_native_state) != 1:
            raise ValueError(
                "band-path input requires exactly one predecessor native state"
            )

    @property
    def identity(self) -> TaskDefinitionIdentity:
        """Return the fixed reusable band-path Task-definition identity."""
        return self._IDENTITY

    def execute(
        self,
        inputs: tuple[TaskInputBinding, ...],
        context: TaskExecutionContext,
    ) -> tuple[ResultObject, ...]:
        """Validate the admitted predecessor and delegate one band-path operation.

        Parameters
        ----------
        inputs
            Exactly one ``predecessor_result`` binding containing a mechanically
            completed :class:`QuantumEspressoPwResult`.
        context
            Exact Workflow context matching ``simulation_input``.

        Returns
        -------
        tuple[ResultObject, ...]
            One newly returned :class:`QuantumEspressoPwResult`.

        Raises
        ------
        TypeError
            If an argument, predecessor, calculator result, or structural boundary
            has the wrong semantic type.
        ValueError
            If predecessor, native-state, context, or returned-input correlations
            disagree.
        """
        self._validate_predecessor(inputs)
        self._validate_context(context)
        result = self.calculator.execute(self.simulation_input, context)
        if type(result) is not QuantumEspressoPwResult:
            raise TypeError("band-path calculator must return QuantumEspressoPwResult")
        if result.evidence.execution_input != self.simulation_input:
            raise ValueError("band-path result must identify the exact execution input")
        return (result,)

    def _validate_predecessor(
        self, inputs: tuple[TaskInputBinding, ...]
    ) -> QuantumEspressoPwResult:
        """Require one completed parent result matching the staged native state."""
        if type(inputs) is not tuple or any(
            type(item) is not TaskInputBinding for item in inputs
        ):
            raise TypeError("inputs must be a tuple of TaskInputBinding")
        if len(inputs) != 1 or inputs[0].name != "predecessor_result":
            raise ValueError(
                "band-path Task requires exactly one predecessor_result binding"
            )
        predecessor = inputs[0].result
        if type(predecessor) is not QuantumEspressoPwResult:
            raise TypeError("predecessor_result must be QuantumEspressoPwResult")
        self._validate_predecessor_state(predecessor)
        return predecessor

    def _validate_predecessor_state(self, predecessor: QuantumEspressoPwResult) -> None:
        """Require completed evidence and exact native-state provenance closure."""
        if type(predecessor.evidence.calculator_outcome) is not (
            QuantumEspressoCompletedOutcome
        ):
            raise ValueError("band-path predecessor must be mechanically completed")
        state = self.simulation_input.predecessor_native_state[0]
        if state.predecessor_result_identity != predecessor.identity:
            raise ValueError("band-path native state must identify its predecessor")
        if (
            state.content.manifest_identity
            != predecessor.evidence.native_output_manifest_identity
            or state.predecessor_manifest_entry_identity
            not in predecessor.evidence.native_output_entry_identities
            or state.predecessor_manifest_entry_identity
            not in state.content.manifest_entry_identities
        ):
            raise ValueError(
                "band-path native state must belong to its predecessor manifest"
            )

    def _validate_context(self, context: TaskExecutionContext) -> None:
        """Require exact run-scoped correlations before calculator delegation."""
        if type(context) is not TaskExecutionContext:
            raise TypeError("context must be TaskExecutionContext")
        expected = (
            (
                context.task_instance_identity,
                self.simulation_input.task_instance_identity,
            ),
            (
                context.task_activation_identity,
                self.simulation_input.activation_identity,
            ),
            (context.operation_identity, self.simulation_input.operation_identity),
            (context.attempt_identity, self.simulation_input.attempt_identity),
        )
        if any(actual != required for actual, required in expected):
            raise ValueError(
                "band-path context must match the execution input correlations"
            )


@dataclass(frozen=True, slots=True)
class QuantumEspressoBandsExtractionTask:
    """Execute one exact QE ``bands`` extraction operation.

    Parameters
    ----------
    simulation_input
        Exact ``bands`` execution input identifying this Task definition and exactly
        one staged band-path native state.
    calculator
        Explicit backend-neutral calculator port bound to QE input and ``bands``
        result types.

    Notes
    -----
    The fixed Task-definition identity is
    ``quantum-espresso.bands-extraction.v1``.  The required input binding is named
    ``band_path_result`` and must contain a mechanically completed
    :class:`QuantumEspressoPwResult` matching the staged native state.
    """

    simulation_input: QuantumEspressoExecutionInput
    calculator: PlaneWaveCalculator[
        QuantumEspressoExecutionInput, QuantumEspressoBandsResult
    ]

    _IDENTITY: ClassVar[TaskDefinitionIdentity] = TaskDefinitionIdentity(
        "quantum-espresso.bands-extraction.v1"
    )

    def __post_init__(self) -> None:
        """Validate the extraction input shape and injected calculator boundary."""
        if type(self.simulation_input) is not QuantumEspressoExecutionInput:
            raise TypeError("simulation_input must be QuantumEspressoExecutionInput")
        if not isinstance(self.calculator, PlaneWaveCalculator):
            raise TypeError("calculator must implement PlaneWaveCalculator")
        if self.simulation_input.program is not QuantumEspressoProgram.BANDS:
            raise ValueError("bands-extraction input must use the bands program role")
        if self.simulation_input.task_definition_identity != self.identity:
            raise ValueError(
                "bands-extraction input must identify the extraction Task definition"
            )
        if len(self.simulation_input.predecessor_native_state) != 1:
            raise ValueError(
                "bands-extraction input requires exactly one predecessor native state"
            )

    @property
    def identity(self) -> TaskDefinitionIdentity:
        """Return the fixed reusable bands-extraction Task-definition identity."""
        return self._IDENTITY

    def execute(
        self,
        inputs: tuple[TaskInputBinding, ...],
        context: TaskExecutionContext,
    ) -> tuple[ResultObject, ...]:
        """Validate the band-path predecessor and delegate one extraction operation.

        Parameters
        ----------
        inputs
            Exactly one ``band_path_result`` binding containing a mechanically
            completed :class:`QuantumEspressoPwResult`.
        context
            Exact Workflow context matching ``simulation_input``.

        Returns
        -------
        tuple[ResultObject, ...]
            One newly returned :class:`QuantumEspressoBandsResult`.

        Raises
        ------
        TypeError
            If an argument, predecessor, calculator result, or structural boundary
            has the wrong semantic type.
        ValueError
            If predecessor, native-state, context, or returned-input correlations
            disagree.
        """
        self._validate_predecessor(inputs)
        self._validate_context(context)
        result = self.calculator.execute(self.simulation_input, context)
        if type(result) is not QuantumEspressoBandsResult:
            raise TypeError(
                "bands-extraction calculator must return QuantumEspressoBandsResult"
            )
        if result.evidence.execution_input != self.simulation_input:
            raise ValueError(
                "bands-extraction result must identify the exact execution input"
            )
        return (result,)

    def _validate_predecessor(
        self, inputs: tuple[TaskInputBinding, ...]
    ) -> QuantumEspressoPwResult:
        """Require one completed band-path result matching staged native state."""
        if type(inputs) is not tuple or any(
            type(item) is not TaskInputBinding for item in inputs
        ):
            raise TypeError("inputs must be a tuple of TaskInputBinding")
        if len(inputs) != 1 or inputs[0].name != "band_path_result":
            raise ValueError(
                "bands-extraction Task requires exactly one band_path_result binding"
            )
        predecessor = inputs[0].result
        if type(predecessor) is not QuantumEspressoPwResult:
            raise TypeError("band_path_result must be QuantumEspressoPwResult")
        self._validate_predecessor_state(predecessor)
        return predecessor

    def _validate_predecessor_state(self, predecessor: QuantumEspressoPwResult) -> None:
        """Require completed evidence and exact native-state provenance closure."""
        if type(predecessor.evidence.calculator_outcome) is not (
            QuantumEspressoCompletedOutcome
        ):
            raise ValueError(
                "bands-extraction predecessor must be mechanically completed"
            )
        state = self.simulation_input.predecessor_native_state[0]
        if state.predecessor_result_identity != predecessor.identity:
            raise ValueError(
                "bands-extraction native state must identify the band-path result"
            )
        if (
            state.content.manifest_identity
            != predecessor.evidence.native_output_manifest_identity
            or state.predecessor_manifest_entry_identity
            not in predecessor.evidence.native_output_entry_identities
            or state.predecessor_manifest_entry_identity
            not in state.content.manifest_entry_identities
        ):
            raise ValueError(
                "bands-extraction native state must belong to the band-path manifest"
            )

    def _validate_context(self, context: TaskExecutionContext) -> None:
        """Require exact run-scoped correlations before calculator delegation."""
        if type(context) is not TaskExecutionContext:
            raise TypeError("context must be TaskExecutionContext")
        expected = (
            (
                context.task_instance_identity,
                self.simulation_input.task_instance_identity,
            ),
            (
                context.task_activation_identity,
                self.simulation_input.activation_identity,
            ),
            (context.operation_identity, self.simulation_input.operation_identity),
            (context.attempt_identity, self.simulation_input.attempt_identity),
        )
        if any(actual != required for actual, required in expected):
            raise ValueError(
                "bands-extraction context must match the execution input correlations"
            )
