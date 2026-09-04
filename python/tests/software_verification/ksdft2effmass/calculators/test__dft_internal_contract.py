r"""Software verification of the private calculator DFT probe contract.

Evidence profile: routine

Bounded artifact scope: private calculator identities, concrete SCF and bands
records, closed operation unions, and the injected calculator protocol.

Facet and represented meaning

The artifact represents exact calculator-specific inputs and mechanical results for
the retained QE and ABINIT SCF-to-fixed-density-bands architecture probe.

Intrinsic and cross-object scope

Tests cover exact nominal fields, immutable concrete variants, intrinsic rejection,
structural protocol conformance, and absence from the supported package surface.

VVUQ and scientific exclusions

This is software verification of a private revisable contract. It invokes no
scientific executable and establishes no convergence, numerical verification,
scientific validation, backend equivalence, uncertainty quantification, or
acceptance.
"""

from dataclasses import FrozenInstanceError

import pytest

import ksdft2effmass.calculators as calculators
from ksdft2effmass.calculators._dft import (
    AbinitFixedDensityBandsInput,
    AbinitFixedDensityBandsOutput,
    AbinitScfInput,
    AbinitScfOutput,
    CalculatorArtifactIdentity,
    DftCalculator,
    ProcessObservationIdentity,
    QuantumEspressoFixedDensityBandsInput,
    QuantumEspressoFixedDensityBandsOutput,
    QuantumEspressoScfInput,
    QuantumEspressoScfOutput,
    SimulationInputIdentity,
)
from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskExecutionContext,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)

pytestmark = pytest.mark.software_verification


def make_context() -> TaskExecutionContext:
    """Return exact synthetic correlation state for protocol evidence.

    Evidence ID: Helper owns no identifier.

    Requirement: Support protocol evidence with explicit nominal identities.

    Acceptance: Return one valid immutable execution context.
    """
    return TaskExecutionContext(
        WorkflowIdentity("workflow.probe"),
        WorkflowRunIdentity("run.probe"),
        TaskInstanceIdentity("task.probe"),
        TaskActivationIdentity("activation.probe"),
        OperationIdentity("operation.probe"),
        AttemptIdentity("attempt.probe"),
    )


def make_qe_scf_input() -> QuantumEspressoScfInput:
    """Return one valid private QE SCF input for consuming tests.

    Evidence ID: Helper owns no identifier.

    Requirement: Support record evidence with exact calculator input identities.

    Acceptance: Return one valid immutable QE SCF input.
    """
    return QuantumEspressoScfInput(
        SimulationInputIdentity("qe.scf.input"),
        CalculatorArtifactIdentity("qe.scf.native-input"),
        (CalculatorArtifactIdentity("qe.si.pseudopotential"),),
    )


def make_qe_scf_output() -> QuantumEspressoScfOutput:
    """Return one valid private QE SCF output for consuming tests.

    Evidence ID: Helper owns no identifier.

    Requirement: Support result evidence with exact mechanical identities.

    Acceptance: Return one valid immutable QE SCF output.
    """
    return QuantumEspressoScfOutput(
        ResultObjectIdentity("qe.scf.output"),
        SimulationInputIdentity("qe.scf.input"),
        ProcessObservationIdentity("qe.scf.process"),
        CalculatorArtifactIdentity("qe.scf.native-state"),
    )


def test_artifact__variants__retain_exact_calculator_specific_state() -> None:
    """Evidence ID: SV-CALCULATOR-PRIVATE-001

    Requirement: QE and ABINIT SCF and fixed-density-bands records retain exact
    nominal input, artifact, process, continuation, and result identities without
    collapsing calculator variants.

    Acceptance: Every constructed field equals the independently supplied identity,
    and corresponding QE and ABINIT values have distinct concrete types.
    """
    qe_scf_input = make_qe_scf_input()
    qe_scf_output = make_qe_scf_output()
    abinit_scf_input = AbinitScfInput(
        SimulationInputIdentity("abinit.scf.input"),
        CalculatorArtifactIdentity("abinit.scf.native-input"),
        (CalculatorArtifactIdentity("abinit.si.pseudopotential"),),
    )
    abinit_scf_output = AbinitScfOutput(
        ResultObjectIdentity("abinit.scf.output"),
        abinit_scf_input.identity,
        ProcessObservationIdentity("abinit.process"),
        CalculatorArtifactIdentity("abinit.density"),
    )
    qe_bands_input = QuantumEspressoFixedDensityBandsInput(
        SimulationInputIdentity("qe.bands.input"),
        CalculatorArtifactIdentity("qe.bands.native-input"),
        qe_scf_input.pseudopotential_identities,
        qe_scf_output.identity,
        qe_scf_output.native_state_identity,
    )
    qe_bands_output = QuantumEspressoFixedDensityBandsOutput(
        ResultObjectIdentity("qe.bands.output"),
        qe_bands_input.identity,
        ProcessObservationIdentity("qe.bands.process"),
        CalculatorArtifactIdentity("qe.bands.result"),
    )
    abinit_bands_input = AbinitFixedDensityBandsInput(
        SimulationInputIdentity("abinit.bands.input"),
        CalculatorArtifactIdentity("abinit.bands.native-input"),
        abinit_scf_input.pseudopotential_identities,
        abinit_scf_output.identity,
        abinit_scf_output.native_state_identity,
    )
    abinit_bands_output = AbinitFixedDensityBandsOutput(
        ResultObjectIdentity("abinit.bands.output"),
        abinit_bands_input.identity,
        abinit_scf_output.process_observation_identity,
        CalculatorArtifactIdentity("abinit.bands.result"),
    )

    assert type(qe_scf_input) is not type(abinit_scf_input)
    assert type(qe_scf_output) is not type(abinit_scf_output)
    assert type(qe_bands_input) is not type(abinit_bands_input)
    assert type(qe_bands_output) is not type(abinit_bands_output)
    assert qe_bands_input.scf_output_identity is qe_scf_output.identity
    assert qe_bands_input.native_state_identity is qe_scf_output.native_state_identity
    assert abinit_bands_input.scf_output_identity is abinit_scf_output.identity
    assert abinit_bands_output.process_observation_identity is (
        abinit_scf_output.process_observation_identity
    )


def test_artifact__construction__rejects_invalid_intrinsic_state() -> None:
    """Evidence ID: SV-CALCULATOR-PRIVATE-002

    Requirement: Private records reject wrong nominal identity types, empty identity
    strings, empty pseudopotential sets, and duplicate pseudopotential identities.

    Acceptance: Wrong semantic types raise ``TypeError`` and invalid correctly typed
    values raise ``ValueError``.
    """
    with pytest.raises(TypeError):
        SimulationInputIdentity(1)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SimulationInputIdentity("")
    with pytest.raises(TypeError):
        QuantumEspressoScfInput(
            CalculatorArtifactIdentity("wrong"),  # type: ignore[arg-type]
            CalculatorArtifactIdentity("native"),
            (CalculatorArtifactIdentity("pseudo"),),
        )
    with pytest.raises(ValueError):
        QuantumEspressoScfInput(
            SimulationInputIdentity("input"),
            CalculatorArtifactIdentity("native"),
            (),
        )
    duplicate = CalculatorArtifactIdentity("pseudo")
    with pytest.raises(ValueError):
        QuantumEspressoScfInput(
            SimulationInputIdentity("input"),
            CalculatorArtifactIdentity("native"),
            (duplicate, duplicate),
        )


def test_artifact__immutability__prevents_record_mutation() -> None:
    """Evidence ID: SV-CALCULATOR-PRIVATE-003

    Requirement: Calculator probe records are operationally immutable values.

    Acceptance: Assigning a field raises ``FrozenInstanceError`` and tuple-owned
    pseudopotential state exposes no mutating list interface.
    """
    value = make_qe_scf_input()
    with pytest.raises(FrozenInstanceError):
        value.identity = SimulationInputIdentity("replacement")  # type: ignore[misc]
    assert type(value.pseudopotential_identities) is tuple


def test_artifact__protocol__admits_explicit_injected_implementation() -> None:
    """Evidence ID: SV-CALCULATOR-PRIVATE-004

    Requirement: ``DftCalculator`` is a structural consumer port for explicit
    implementations and does not require a registry or nominal base class.

    Acceptance: A local object with the exact execute signature satisfies the
    runtime-checkable protocol and returns the supplied immutable result.
    """

    class RetainedQeCalculator:
        def __init__(self, output: QuantumEspressoScfOutput) -> None:
            self.output = output

        def execute(
            self,
            simulation_input: QuantumEspressoScfInput,
            context: TaskExecutionContext,
        ) -> QuantumEspressoScfOutput:
            assert simulation_input == make_qe_scf_input()
            assert context == make_context()
            return self.output

    output = make_qe_scf_output()
    calculator = RetainedQeCalculator(output)
    assert isinstance(calculator, DftCalculator)
    assert calculator.execute(make_qe_scf_input(), make_context()) is output


def test_artifact__package_surface__keeps_probe_contract_private() -> None:
    """Evidence ID: SV-CALCULATOR-PRIVATE-005

    Requirement: The revisable DFT probe contract is not exported from the supported
    ``ksdft2effmass.calculators`` package surface.

    Acceptance: Representative probe types are absent from package attributes and
    the package declares no public export inventory.
    """
    assert not hasattr(calculators, "SimulationInputIdentity")
    assert not hasattr(calculators, "QuantumEspressoScfInput")
    assert not hasattr(calculators, "DftCalculator")
    assert not hasattr(calculators, "__all__")
