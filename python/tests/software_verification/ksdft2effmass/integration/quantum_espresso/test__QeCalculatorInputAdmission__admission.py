r"""Software verification of direct provider calculator-input admission.

The tests use synthetic immutable records only. They perform no filesystem access,
calculator execution, scientific validation, convergence assessment, or authorization.
"""

import hashlib
from dataclasses import FrozenInstanceError, replace

import pytest
from projectkoios.simulations.calculator import CalculatorIntegrationEnum
from projectkoios.simulations.calculator_input import (
    CalculatorExternalInputRequirement,
    CalculatorInputArtifact,
    CalculatorInputRecord,
)

import ksdft2effmass.integration.quantum_espresso as qe
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactManifestEntryIdentity,
)

from .resources.calculator_input_scenarios import (
    CalculatorInputAdmissionScenario,
    calculator_input_admission_scenario,
)

pytestmark = pytest.mark.software_verification

type AdmissionResult = (
    qe.QeCalculatorInputBinding | qe.QeCalculatorInputAdmissionFailure
)


@pytest.fixture
def admission_scenario() -> CalculatorInputAdmissionScenario:
    """Return one explicit synthetic provider/KSD admission scenario."""
    return calculator_input_admission_scenario(
        native_bytes=b"&CONTROL\n calculation = 'scf'\n/\n",
        pseudopotential_bytes=b"synthetic pseudopotential",
        policy_identity_value="ksd.qe.calculator-input-admission:1",
    )


class TestQeCalculatorInputAdmission:
    """Own direct-instance admission evidence for provider calculator inputs."""

    def test__QeCalculatorInputAdmission__retains_provider_instance_directly(
        self, admission_scenario: CalculatorInputAdmissionScenario
    ) -> None:
        """Admitted input retains exact instances and explicit policy identity."""
        result: AdmissionResult = admission_scenario.admission.execute(
            admission_scenario.provider_input,
            admission_scenario.execution_input,
        )

        assert type(result) is qe.QeCalculatorInputBinding
        assert (
            result.admission_policy_identity
            is admission_scenario.admission.policy_identity
        )
        assert result.calculator_input is admission_scenario.provider_input
        assert result.execution_input is admission_scenario.execution_input
        assert result.primary_input_artifact is result.calculator_input.artifacts[0]
        assert len(result.external_input_resources) == 1
        external_resource: qe.QeExternalInputResourceBinding = (
            result.external_input_resources[0]
        )
        assert (
            external_resource.external_requirement
            is (result.calculator_input.external_requirements[0])
        )
        assert external_resource.artifact_identity == (
            result.execution_input.pseudopotentials[0].identity
        )
        assert external_resource.destination == (
            result.execution_input.pseudopotentials[0].destination
        )
        assert external_resource.external_requirement.sha256 == (
            result.calculator_input.external_requirements[0].sha256
        )
        assert result.provider_record_byte_size == result.calculator_input.byte_size
        assert result.provider_record_sha256 == result.calculator_input.sha256
        with pytest.raises(FrozenInstanceError):
            result.execution_input = admission_scenario.execution_input  # type: ignore[misc]

    def test__QeCalculatorInputAdmission__rejects_copied_external_requirement(
        self, admission_scenario: CalculatorInputAdmissionScenario
    ) -> None:
        """A binding must retain the exact provider requirement instance."""
        result: AdmissionResult = admission_scenario.admission.execute(
            admission_scenario.provider_input,
            admission_scenario.execution_input,
        )
        assert type(result) is qe.QeCalculatorInputBinding
        resource: qe.QeExternalInputResourceBinding = result.external_input_resources[0]
        copied_resource: qe.QeExternalInputResourceBinding = replace(
            resource,
            external_requirement=replace(resource.external_requirement),
        )

        with pytest.raises(ValueError, match="exact provider requirement"):
            replace(result, external_input_resources=(copied_resource,))

    @pytest.mark.parametrize(
        "integration_id",
        (CalculatorIntegrationEnum.VASP, CalculatorIntegrationEnum.ABINIT),
    )
    def test__QeCalculatorInputAdmission__rejects_wrong_integration(
        self,
        admission_scenario: CalculatorInputAdmissionScenario,
        integration_id: CalculatorIntegrationEnum,
    ) -> None:
        """A provider record for another calculator integration fails closed."""
        provider_input: CalculatorInputRecord = replace(
            admission_scenario.provider_input,
            integration_id=integration_id,
        )

        result: AdmissionResult = admission_scenario.admission.execute(
            provider_input, admission_scenario.execution_input
        )

        assert type(result) is qe.QeCalculatorInputAdmissionFailure
        assert result.code is (
            qe.QeCalculatorInputAdmissionFailureCode.UNSUPPORTED_PROVIDER_CONTRACT
        )
        assert result.admission_policy_identity is (
            admission_scenario.admission.policy_identity
        )

    def test__QeCalculatorInputAdmission__rejects_wrong_representation(
        self, admission_scenario: CalculatorInputAdmissionScenario
    ) -> None:
        """An unsupported provider representation fails closed."""
        provider_input: CalculatorInputRecord = replace(
            admission_scenario.provider_input,
            representation="other-representation",
        )

        result: AdmissionResult = admission_scenario.admission.execute(
            provider_input, admission_scenario.execution_input
        )

        assert type(result) is qe.QeCalculatorInputAdmissionFailure
        assert result.code is (
            qe.QeCalculatorInputAdmissionFailureCode.UNSUPPORTED_PROVIDER_CONTRACT
        )

    def test__QeCalculatorInputAdmission__rejects_wrong_operation(
        self, admission_scenario: CalculatorInputAdmissionScenario
    ) -> None:
        """A non-pw preparation operation fails closed."""
        provider_input: CalculatorInputRecord = replace(
            admission_scenario.provider_input,
            preparation_operation="projectkoios.qe.bands.prepare",
        )

        result: AdmissionResult = admission_scenario.admission.execute(
            provider_input, admission_scenario.execution_input
        )

        assert type(result) is qe.QeCalculatorInputAdmissionFailure
        assert (
            result.code is qe.QeCalculatorInputAdmissionFailureCode.OPERATION_MISMATCH
        )

    def test__QeCalculatorInputAdmission__rejects_primary_content_mismatch(
        self, admission_scenario: CalculatorInputAdmissionScenario
    ) -> None:
        """Provider native bytes must match KSD's exact native-input identity."""
        different: bytes = b"different"
        mismatched: qe.QeExecutionInput = replace(
            admission_scenario.execution_input,
            native_input=replace(
                admission_scenario.execution_input.native_input,
                content=qe.QeFileArtifactContent(
                    ArtifactContentIdentity(
                        "sha256",
                        hashlib.sha256(different).hexdigest(),
                        len(different),
                    )
                ),
            ),
        )

        result: AdmissionResult = admission_scenario.admission.execute(
            admission_scenario.provider_input, mismatched
        )

        assert type(result) is qe.QeCalculatorInputAdmissionFailure
        assert result.code is (
            qe.QeCalculatorInputAdmissionFailureCode.CONTENT_IDENTITY_MISMATCH
        )

    def test__QeCalculatorInputAdmission__rejects_external_content_mismatch(
        self, admission_scenario: CalculatorInputAdmissionScenario
    ) -> None:
        """Provider external requirements must match the admitted KSD correlation."""
        requirement: CalculatorExternalInputRequirement = (
            admission_scenario.provider_input.external_requirements[0]
        )
        provider_input: CalculatorInputRecord = replace(
            admission_scenario.provider_input,
            external_requirements=(replace(requirement, sha256="0" * 64),),
        )

        result: AdmissionResult = admission_scenario.admission.execute(
            provider_input, admission_scenario.execution_input
        )

        assert type(result) is qe.QeCalculatorInputAdmissionFailure
        assert result.code is (
            qe.QeCalculatorInputAdmissionFailureCode.CONTENT_IDENTITY_MISMATCH
        )

    def test__QeCalculatorInputAdmission__rejects_artifact_role_mismatch(
        self, admission_scenario: CalculatorInputAdmissionScenario
    ) -> None:
        """Unknown provider artifact roles are not inferred as QE inputs."""
        primary: CalculatorInputArtifact = admission_scenario.provider_input.artifacts[
            0
        ]
        provider_input: CalculatorInputRecord = replace(
            admission_scenario.provider_input,
            artifacts=(replace(primary, role="control-file"),),
        )

        result: AdmissionResult = admission_scenario.admission.execute(
            provider_input, admission_scenario.execution_input
        )

        assert type(result) is qe.QeCalculatorInputAdmissionFailure
        assert result.code is (
            qe.QeCalculatorInputAdmissionFailureCode.ARTIFACT_ROLE_MISMATCH
        )

    def test__QeCalculatorInputAdmission__rejects_unadmitted_predecessor_entry(
        self, admission_scenario: CalculatorInputAdmissionScenario
    ) -> None:
        """A predecessor entry absent from its exact tree cannot be correlated."""
        predecessor: qe.QePredecessorNativeStateArtifact = (
            admission_scenario.execution_input.predecessor_native_state[0]
        )
        mismatched: qe.QeExecutionInput = replace(
            admission_scenario.execution_input,
            predecessor_native_state=(
                replace(
                    predecessor,
                    predecessor_manifest_entry_identity=(
                        ArtifactManifestEntryIdentity("manifest.scf.other")
                    ),
                ),
            ),
        )

        result: AdmissionResult = admission_scenario.admission.execute(
            admission_scenario.provider_input, mismatched
        )

        assert type(result) is qe.QeCalculatorInputAdmissionFailure
        assert result.code is (
            qe.QeCalculatorInputAdmissionFailureCode.PREDECESSOR_ADMISSION_MISMATCH
        )

    def test__QeCalculatorInputAdmission__rejects_wrong_nominal_inputs(
        self, admission_scenario: CalculatorInputAdmissionScenario
    ) -> None:
        """Admission accepts only exact provider, KSD input, and policy types."""
        with pytest.raises(TypeError):
            admission_scenario.admission.execute(
                "input",  # type: ignore[arg-type]
                admission_scenario.execution_input,
            )
        with pytest.raises(TypeError):
            admission_scenario.admission.execute(
                admission_scenario.provider_input,
                "input",  # type: ignore[arg-type]
            )
        with pytest.raises(TypeError):
            qe.QeCalculatorInputAdmission("policy")  # type: ignore[arg-type]

    def test__QeCalculatorInputAdmission__is_public_without_legacy_aliases(
        self,
    ) -> None:
        """The public package exports only concise QE admission names."""
        assert "QeCalculatorInputAdmission" in qe.__all__
        assert "QeCalculatorInputAdmissionPolicyIdentity" in qe.__all__
        assert "QeCalculatorInputBinding" in qe.__all__
        assert "QeExternalInputResourceBinding" in qe.__all__
        assert not hasattr(qe, "QuantumEspressoCalculatorInputAdapter")
