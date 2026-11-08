"""Typed synthetic scenarios for QE calculator-input admission tests."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from projectkoios.simulations.calculator import CalculatorIntegrationId
from projectkoios.simulations.calculator.input import (
    CalculatorExternalInputRequirement,
    CalculatorInputArtifact,
    CalculatorInputRecord,
    CalculatorInputSourceReference,
)

from ksdft2effmass.integration.quantum_espresso import (
    QeArtifactDestination,
    QeCalculatorInputAdmission,
    QeCalculatorInputAdmissionPolicyIdentity,
    QeExecutionInput,
    QeExecutionInputIdentity,
    QeFileArtifactContent,
    QeNativeInputArtifact,
    QePredecessorNativeStateArtifact,
    QeProgram,
    QePseudopotentialArtifact,
    QeTreeArtifactContent,
)
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    AttemptIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class CalculatorInputAdmissionScenario:
    """Contain one exact synthetic provider/KSD admission scenario."""

    admission: QeCalculatorInputAdmission
    provider_input: CalculatorInputRecord
    execution_input: QeExecutionInput

    def __post_init__(self) -> None:
        if type(self.admission) is not QeCalculatorInputAdmission:
            raise TypeError("admission must be QeCalculatorInputAdmission")
        if type(self.provider_input) is not CalculatorInputRecord:
            raise TypeError("provider_input must be CalculatorInputRecord")
        if type(self.execution_input) is not QeExecutionInput:
            raise TypeError("execution_input must be QeExecutionInput")


def calculator_input_admission_scenario(
    *,
    native_bytes: bytes,
    pseudopotential_bytes: bytes,
    policy_identity_value: str,
) -> CalculatorInputAdmissionScenario:
    """Construct one fully typed synthetic admission scenario."""
    native_identity: ArtifactContentIdentity = ArtifactContentIdentity(
        "sha256", hashlib.sha256(native_bytes).hexdigest(), len(native_bytes)
    )
    pseudopotential_identity: ArtifactContentIdentity = ArtifactContentIdentity(
        "sha256",
        hashlib.sha256(pseudopotential_bytes).hexdigest(),
        len(pseudopotential_bytes),
    )
    predecessor_entry: ArtifactManifestEntryIdentity = ArtifactManifestEntryIdentity(
        "manifest.scf.entry"
    )
    predecessor: QePredecessorNativeStateArtifact = QePredecessorNativeStateArtifact(
        identity=ArtifactIdentity("state.scf"),
        content=QeTreeArtifactContent(
            manifest_identity=ArtifactManifestIdentity("manifest.scf"),
            manifest_entry_identities=(predecessor_entry,),
        ),
        destination=QeArtifactDestination("work/si.save"),
        predecessor_result_identity=ResultObjectIdentity("result.scf"),
        predecessor_manifest_entry_identity=predecessor_entry,
    )
    execution_input: QeExecutionInput = QeExecutionInput(
        identity=QeExecutionInputIdentity("ksd.input.scf"),
        program=QeProgram.PW,
        native_input=QeNativeInputArtifact(
            identity=ArtifactIdentity("input.pw"),
            content=QeFileArtifactContent(native_identity),
            destination=QeArtifactDestination("input/pw.in"),
        ),
        pseudopotentials=(
            QePseudopotentialArtifact(
                identity=ArtifactIdentity("pseudo.si"),
                content=QeFileArtifactContent(pseudopotential_identity),
                destination=QeArtifactDestination("pseudo/Si.upf"),
            ),
        ),
        predecessor_native_state=(predecessor,),
        task_definition_identity=TaskDefinitionIdentity("task.qe.scf"),
        task_instance_identity=TaskInstanceIdentity("task-instance.qe.scf"),
        activation_identity=TaskActivationIdentity("activation.qe.scf"),
        operation_identity=OperationIdentity("operation.qe.scf"),
        attempt_identity=AttemptIdentity("attempt.qe.scf.1"),
        contract_version="qe-execution-input:1",
    )
    provider_input: CalculatorInputRecord = CalculatorInputRecord(
        input_id="Si.QE.PreparedInput",
        schema_version=1,
        source=CalculatorInputSourceReference(
            simulation_id="Si.QE.SCF",
            representation="projectkoios.pw-dft-scf+json",
            schema_version=1,
            byte_size=100,
            sha256="1" * 64,
        ),
        integration_id=CalculatorIntegrationId("quantum-espresso"),
        calculator_name="Quantum ESPRESSO pw.x",
        calculator_version_constraint=">=7.5,<8",
        representation="quantum-espresso-pw-input",
        artifacts=(
            CalculatorInputArtifact(
                role="primary-input",
                filename="pw.in",
                media_type="text/plain; charset=us-ascii",
                content=native_bytes,
                byte_size=len(native_bytes),
                sha256=native_identity.digest,
            ),
        ),
        external_requirements=(
            CalculatorExternalInputRequirement(
                role="pseudopotential",
                stable_id="Si.synthetic",
                filename="Si.upf",
                format="upf;version=2.0.1",
                byte_size=len(pseudopotential_bytes),
                sha256=pseudopotential_identity.digest,
                provenance="synthetic software-verification fixture",
                element_symbol="Si",
            ),
        ),
        mappings=(),
        preparation_operation="projectkoios.qe.pw.scf.prepare",
        preparation_version="1",
    )
    policy_identity: QeCalculatorInputAdmissionPolicyIdentity = (
        QeCalculatorInputAdmissionPolicyIdentity(policy_identity_value)
    )
    admission: QeCalculatorInputAdmission = QeCalculatorInputAdmission(policy_identity)
    return CalculatorInputAdmissionScenario(
        admission=admission,
        provider_input=provider_input,
        execution_input=execution_input,
    )
