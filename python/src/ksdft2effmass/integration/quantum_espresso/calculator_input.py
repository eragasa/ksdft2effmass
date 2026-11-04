"""Direct provider-input admission and KSD Workflow correlation.

The admission action retains the immutable Project Koios Simulations
``CalculatorInputRecord`` instance directly. It does not serialize, copy, render,
resolve paths, read files, stage artifacts, invoke a process, or grant execution
authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from projectkoios.simulations.calculator import CalculatorIntegrationId
from projectkoios.simulations.calculator.input import (
    CalculatorExternalInputRequirement,
    CalculatorInputArtifact,
    CalculatorInputRecord,
)

from ksdft2effmass.serialization import StrWireEnum
from ksdft2effmass.workflows import ArtifactContentIdentity, ArtifactIdentity

from .contracts import (
    QeArtifactDestination,
    QeExecutionInput,
    QeProgram,
    QePseudopotentialArtifact,
)

_QE_INTEGRATION_ID_VALUE: str = "quantum-espresso"
_QE_PW_INPUT_REPRESENTATION: str = "quantum-espresso-pw-input"
_QE_PROVIDER_SCHEMA_VERSION: int = 1


@dataclass(frozen=True, slots=True)
class QeCalculatorInputAdmissionPolicyIdentity:
    """Identify one exact KSD provider-input admission policy.

    Attributes
    ----------
    value
        Nonempty exact policy identity.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("admission policy identity must be a built-in str")
        if not self.value:
            raise ValueError("admission policy identity must not be empty")


class QeCalculatorInputAdmissionFailureCode(StrWireEnum):
    """Closed causes for rejecting one provider input correlation."""

    UNSUPPORTED_PROVIDER_CONTRACT = "unsupported_provider_contract"
    OPERATION_MISMATCH = "operation_mismatch"
    ARTIFACT_ROLE_MISMATCH = "artifact_role_mismatch"
    CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
    PREDECESSOR_ADMISSION_MISMATCH = "predecessor_admission_mismatch"


@dataclass(frozen=True, slots=True, kw_only=True)
class QeCalculatorInputAdmissionFailure:
    """Represent one effect-free provider-input admission failure.

    Parameters
    ----------
    code
        Closed mechanical failure cause.
    admission_policy_identity
        Exact KSD admission policy that produced the failure.
    provider_input_id
        Exact provider record identity supplied to the action.
    provider_record_sha256
        Canonical provider-record SHA-256 supplied to the action.
    execution_input_identity
        Exact KSD execution-input identity that was not bound.
    diagnostic
        Sanitized mechanical diagnostic with no scientific interpretation.
    """

    code: QeCalculatorInputAdmissionFailureCode
    admission_policy_identity: QeCalculatorInputAdmissionPolicyIdentity
    provider_input_id: str
    provider_record_sha256: str
    execution_input_identity: str
    diagnostic: str

    def __post_init__(self) -> None:
        if type(self.code) is not QeCalculatorInputAdmissionFailureCode:
            raise TypeError("code must be QeCalculatorInputAdmissionFailureCode")
        if (
            type(self.admission_policy_identity)
            is not QeCalculatorInputAdmissionPolicyIdentity
        ):
            raise TypeError(
                "admission_policy_identity must be "
                "QeCalculatorInputAdmissionPolicyIdentity"
            )
        for value, name in (
            (self.provider_input_id, "provider_input_id"),
            (self.provider_record_sha256, "provider_record_sha256"),
            (self.execution_input_identity, "execution_input_identity"),
            (self.diagnostic, "diagnostic"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QeExternalInputResourceBinding:
    """Bind one exact provider external requirement to KSD deployment correlation.

    Parameters
    ----------
    external_requirement
        Exact provider-owned requirement instance retaining stable identity, filename,
        format, byte count, SHA-256, provenance, role, and optional element symbol.
    artifact_identity
        Exact KSD Workflow-facing artifact identity for staging correlation.
    destination
        Exact root-confined workspace destination selected by KSD policy. Its basename
        must equal the provider requirement filename.

    Notes
    -----
    This immutable value contains no local source path, copied provider metadata,
    filesystem capability, staging authority, or execution authority.
    """

    external_requirement: CalculatorExternalInputRequirement
    artifact_identity: ArtifactIdentity
    destination: QeArtifactDestination

    def __post_init__(self) -> None:
        if type(self.external_requirement) is not CalculatorExternalInputRequirement:
            raise TypeError(
                "external_requirement must be CalculatorExternalInputRequirement"
            )
        if self.external_requirement.role != "pseudopotential":
            raise ValueError("external_requirement must have the pseudopotential role")
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if type(self.destination) is not QeArtifactDestination:
            raise TypeError("destination must be QeArtifactDestination")
        if PurePosixPath(self.destination.value).name != (
            self.external_requirement.filename
        ):
            raise ValueError(
                "destination basename must equal the provider requirement filename"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class QeCalculatorInputBinding:
    """Retain one provider input instance with exact KSD Workflow correlations.

    Parameters
    ----------
    admission_policy_identity
        Exact KSD admission policy applied to the bound instances.
    calculator_input
        The exact immutable provider record instance. Its native bytes, canonical
        record identity, source reference, mappings, and external requirements are
        retained without translation or copying.
    primary_input_artifact
        Exact nominal provider artifact admitted as the single primary input.
    external_input_resources
        Canonical bindings from exact provider external-requirement instances to KSD
        artifact identities and deployment destinations.
    execution_input
        Existing KSD-owned Workflow, artifact, predecessor, operation, and attempt
        correlations admitted against the provider record.
    Notes
    -----
    This binding is not a wire envelope and grants no authority to execute or stage
    the represented input. If persistence is later required, the common Workflow
    serializer owns that representation; this integration defines no JSON codec.
    """

    admission_policy_identity: QeCalculatorInputAdmissionPolicyIdentity
    calculator_input: CalculatorInputRecord
    primary_input_artifact: CalculatorInputArtifact
    external_input_resources: tuple[QeExternalInputResourceBinding, ...]
    execution_input: QeExecutionInput

    def __post_init__(self) -> None:
        if (
            type(self.admission_policy_identity)
            is not QeCalculatorInputAdmissionPolicyIdentity
        ):
            raise TypeError(
                "admission_policy_identity must be "
                "QeCalculatorInputAdmissionPolicyIdentity"
            )
        if type(self.calculator_input) is not CalculatorInputRecord:
            raise TypeError("calculator_input must be CalculatorInputRecord")
        if type(self.primary_input_artifact) is not CalculatorInputArtifact:
            raise TypeError("primary_input_artifact must be CalculatorInputArtifact")
        if not any(
            artifact is self.primary_input_artifact
            for artifact in self.calculator_input.artifacts
        ):
            raise ValueError(
                "primary_input_artifact must be retained by calculator_input"
            )
        if self.primary_input_artifact.role != "primary-input":
            raise ValueError("primary_input_artifact must have the primary-input role")
        resources: tuple[QeExternalInputResourceBinding, ...] = (
            self.external_input_resources
        )
        if type(resources) is not tuple or any(
            type(value) is not QeExternalInputResourceBinding for value in resources
        ):
            raise TypeError(
                "external_input_resources must contain "
                "QeExternalInputResourceBinding values"
            )
        if resources != tuple(
            sorted(resources, key=lambda value: value.artifact_identity.value)
        ) or len({value.artifact_identity for value in resources}) != len(resources):
            raise ValueError(
                "external_input_resources must be unique and lexically sorted"
            )
        if any(
            not any(
                requirement is resource.external_requirement
                for requirement in self.calculator_input.external_requirements
            )
            for resource in resources
        ):
            raise ValueError(
                "every external resource must retain an exact provider requirement"
            )
        if type(self.execution_input) is not QeExecutionInput:
            raise TypeError("execution_input must be QeExecutionInput")
        native_identity: ArtifactContentIdentity = (
            self.execution_input.native_input.content.content_identity
        )
        if (
            self.primary_input_artifact.filename
            != PurePosixPath(self.execution_input.native_input.destination.value).name
            or self.primary_input_artifact.byte_size != native_identity.byte_count
            or self.primary_input_artifact.sha256 != native_identity.digest
        ):
            raise ValueError(
                "primary_input_artifact does not match its admitted KSD correlation"
            )
        pseudopotentials_by_filename: dict[str, QePseudopotentialArtifact] = {
            PurePosixPath(value.destination.value).name: value
            for value in self.execution_input.pseudopotentials
        }
        if len(resources) != len(pseudopotentials_by_filename) or len(resources) != len(
            self.calculator_input.external_requirements
        ):
            raise ValueError(
                "external resources must correspond one-to-one to pseudopotentials"
            )
        for resource in resources:
            requirement: CalculatorExternalInputRequirement = (
                resource.external_requirement
            )
            pseudopotential: QePseudopotentialArtifact | None = (
                pseudopotentials_by_filename.get(requirement.filename)
            )
            if pseudopotential is None:
                raise ValueError(
                    "external resource has no matching KSD pseudopotential correlation"
                )
            content_identity: ArtifactContentIdentity = (
                pseudopotential.content.content_identity
            )
            if (
                resource.artifact_identity != pseudopotential.identity
                or resource.destination != pseudopotential.destination
                or requirement.byte_size != content_identity.byte_count
                or requirement.sha256 != content_identity.digest
            ):
                raise ValueError(
                    "external resource does not match its admitted KSD correlation"
                )

    @property
    def provider_record_byte_size(self) -> int:
        """Return the provider record's canonical byte size without copying it."""
        return self.calculator_input.byte_size

    @property
    def provider_record_sha256(self) -> str:
        """Return the provider record's canonical SHA-256 without copying it."""
        return self.calculator_input.sha256


@dataclass(frozen=True, slots=True)
class QeCalculatorInputAdmission:
    """Admit one provider input instance against exact KSD correlations.

    Parameters
    ----------
    policy_identity
        Exact KSD admission-policy identity applied by this action.

    The action is deterministic and effect-free. It supports the provider's schema-1
    Quantum ESPRESSO ``pw.x`` input representation. Unsupported provider contracts or
    correlation mismatches return a typed failure rather than an inferred binding.
    """

    policy_identity: QeCalculatorInputAdmissionPolicyIdentity

    def __post_init__(self) -> None:
        if type(self.policy_identity) is not QeCalculatorInputAdmissionPolicyIdentity:
            raise TypeError(
                "policy_identity must be QeCalculatorInputAdmissionPolicyIdentity"
            )

    def execute(
        self,
        calculator_input: CalculatorInputRecord,
        execution_input: QeExecutionInput,
    ) -> QeCalculatorInputBinding | QeCalculatorInputAdmissionFailure:
        """Return one direct binding or one closed mechanical failure.

        Parameters
        ----------
        calculator_input
            Exact immutable provider record instance.
        execution_input
            Exact KSD Workflow and artifact correlation value.

        Returns
        -------
        QeCalculatorInputBinding or QeCalculatorInputAdmissionFailure
            Direct instance binding on exact agreement; otherwise one typed failure.

        Raises
        ------
        TypeError
            Either argument is not its exact supported nominal type.
        """
        if type(calculator_input) is not CalculatorInputRecord:
            raise TypeError("calculator_input must be CalculatorInputRecord")
        if type(execution_input) is not QeExecutionInput:
            raise TypeError("execution_input must be QeExecutionInput")

        provider_failure: QeCalculatorInputAdmissionFailure | None = (
            self._provider_contract_failure(calculator_input, execution_input)
        )
        if provider_failure is not None:
            return provider_failure
        operation_failure: QeCalculatorInputAdmissionFailure | None = (
            self._operation_failure(calculator_input, execution_input)
        )
        if operation_failure is not None:
            return operation_failure
        artifact_failure: QeCalculatorInputAdmissionFailure | None = (
            self._artifact_failure(calculator_input, execution_input)
        )
        if artifact_failure is not None:
            return artifact_failure
        predecessor_failure: QeCalculatorInputAdmissionFailure | None = (
            self._predecessor_failure(calculator_input, execution_input)
        )
        if predecessor_failure is not None:
            return predecessor_failure
        primary_input_artifact: CalculatorInputArtifact = calculator_input.artifacts[0]
        external_input_resources: tuple[QeExternalInputResourceBinding, ...] = (
            self._external_input_resources(calculator_input, execution_input)
        )
        return QeCalculatorInputBinding(
            admission_policy_identity=self.policy_identity,
            calculator_input=calculator_input,
            primary_input_artifact=primary_input_artifact,
            external_input_resources=external_input_resources,
            execution_input=execution_input,
        )

    def _provider_contract_failure(
        self,
        calculator_input: CalculatorInputRecord,
        execution_input: QeExecutionInput,
    ) -> QeCalculatorInputAdmissionFailure | None:
        if (
            calculator_input.schema_version != _QE_PROVIDER_SCHEMA_VERSION
            or calculator_input.integration_id
            != CalculatorIntegrationId(_QE_INTEGRATION_ID_VALUE)
            or calculator_input.representation != _QE_PW_INPUT_REPRESENTATION
        ):
            return self._failure(
                QeCalculatorInputAdmissionFailureCode.UNSUPPORTED_PROVIDER_CONTRACT,
                calculator_input,
                execution_input,
                "provider schema, integration, or representation is unsupported",
            )
        return None

    def _operation_failure(
        self,
        calculator_input: CalculatorInputRecord,
        execution_input: QeExecutionInput,
    ) -> QeCalculatorInputAdmissionFailure | None:
        if execution_input.program is not QeProgram.PW or not (
            calculator_input.preparation_operation.startswith("projectkoios.qe.pw.")
        ):
            return self._failure(
                QeCalculatorInputAdmissionFailureCode.OPERATION_MISMATCH,
                calculator_input,
                execution_input,
                "provider preparation operation does not match the KSD QE program",
            )
        return None

    def _artifact_failure(
        self,
        calculator_input: CalculatorInputRecord,
        execution_input: QeExecutionInput,
    ) -> QeCalculatorInputAdmissionFailure | None:
        primary_inputs: tuple[CalculatorInputArtifact, ...] = tuple(
            artifact
            for artifact in calculator_input.artifacts
            if artifact.role == "primary-input"
        )
        if len(primary_inputs) != 1 or len(calculator_input.artifacts) != 1:
            return self._failure(
                QeCalculatorInputAdmissionFailureCode.ARTIFACT_ROLE_MISMATCH,
                calculator_input,
                execution_input,
                "provider artifacts must contain exactly one primary-input role",
            )
        if any(
            requirement.role != "pseudopotential"
            for requirement in calculator_input.external_requirements
        ):
            return self._failure(
                QeCalculatorInputAdmissionFailureCode.ARTIFACT_ROLE_MISMATCH,
                calculator_input,
                execution_input,
                "provider external requirements must be pseudopotentials",
            )

        primary: CalculatorInputArtifact = primary_inputs[0]
        native_identity: ArtifactContentIdentity = (
            execution_input.native_input.content.content_identity
        )
        if (
            primary.filename
            != PurePosixPath(execution_input.native_input.destination.value).name
            or primary.byte_size != native_identity.byte_count
            or primary.sha256 != native_identity.digest
        ):
            return self._failure(
                QeCalculatorInputAdmissionFailureCode.CONTENT_IDENTITY_MISMATCH,
                calculator_input,
                execution_input,
                "provider primary input does not match the KSD native-input identity",
            )

        requirements: dict[str, CalculatorExternalInputRequirement] = {
            requirement.filename: requirement
            for requirement in calculator_input.external_requirements
        }
        pseudopotentials: dict[str, QePseudopotentialArtifact] = {
            PurePosixPath(artifact.destination.value).name: artifact
            for artifact in execution_input.pseudopotentials
        }
        if (
            len(pseudopotentials) != len(execution_input.pseudopotentials)
            or requirements.keys() != pseudopotentials.keys()
        ):
            return self._failure(
                QeCalculatorInputAdmissionFailureCode.ARTIFACT_ROLE_MISMATCH,
                calculator_input,
                execution_input,
                "provider and KSD pseudopotential filenames do not agree",
            )
        for filename, requirement in requirements.items():
            identity: ArtifactContentIdentity = pseudopotentials[
                filename
            ].content.content_identity
            if (
                requirement.byte_size != identity.byte_count
                or requirement.sha256 != identity.digest
            ):
                return self._failure(
                    QeCalculatorInputAdmissionFailureCode.CONTENT_IDENTITY_MISMATCH,
                    calculator_input,
                    execution_input,
                    "provider pseudopotential does not match the KSD content identity",
                )
        return None

    def _external_input_resources(
        self,
        calculator_input: CalculatorInputRecord,
        execution_input: QeExecutionInput,
    ) -> tuple[QeExternalInputResourceBinding, ...]:
        requirements_by_filename: dict[str, CalculatorExternalInputRequirement] = {
            requirement.filename: requirement
            for requirement in calculator_input.external_requirements
        }
        resources: list[QeExternalInputResourceBinding] = []
        for pseudopotential in execution_input.pseudopotentials:
            filename: str = PurePosixPath(pseudopotential.destination.value).name
            requirement: CalculatorExternalInputRequirement = requirements_by_filename[
                filename
            ]
            resources.append(
                QeExternalInputResourceBinding(
                    external_requirement=requirement,
                    artifact_identity=pseudopotential.identity,
                    destination=pseudopotential.destination,
                )
            )
        return tuple(sorted(resources, key=lambda value: value.artifact_identity.value))

    def _predecessor_failure(
        self,
        calculator_input: CalculatorInputRecord,
        execution_input: QeExecutionInput,
    ) -> QeCalculatorInputAdmissionFailure | None:
        for predecessor in execution_input.predecessor_native_state:
            if (
                predecessor.predecessor_manifest_entry_identity
                not in predecessor.content.manifest_entry_identities
            ):
                return self._failure(
                    QeCalculatorInputAdmissionFailureCode.PREDECESSOR_ADMISSION_MISMATCH,
                    calculator_input,
                    execution_input,
                    "predecessor manifest entry is absent from the admitted tree",
                )
        return None

    def _failure(
        self,
        code: QeCalculatorInputAdmissionFailureCode,
        calculator_input: CalculatorInputRecord,
        execution_input: QeExecutionInput,
        diagnostic: str,
    ) -> QeCalculatorInputAdmissionFailure:
        return QeCalculatorInputAdmissionFailure(
            code=code,
            admission_policy_identity=self.policy_identity,
            provider_input_id=calculator_input.input_id,
            provider_record_sha256=calculator_input.sha256,
            execution_input_identity=execution_input.identity.value,
            diagnostic=diagnostic,
        )
