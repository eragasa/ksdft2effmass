r"""Software verification of private QE NSCF and DOS calculator contracts.

Evidence profile: routine

Bounded artifact scope: immutable private QE NSCF and DOS input/result records and
their membership in the private closed DFT operation unions.

Facet and represented meaning

The artifact preserves exact predecessor-result, native-state, native-input,
pseudopotential, process-observation, and produced-artifact identities without
asserting scientific meaning.

Intrinsic and cross-object scope

Tests cover exact construction, operational immutability, nominal predecessor types,
closed-union membership, and absence from the supported calculator package surface.
Cross-object compatibility remains an ActionObject or Workflow-control concern.

VVUQ and scientific exclusions

This is software verification of private records using synthetic lexical identities.
No calculator runs, native-state contents, convergence, numerical verification,
scientific validation, uncertainty quantification, or human acceptance are claimed.
"""

from dataclasses import FrozenInstanceError
from typing import get_args

import pytest

import ksdft2effmass.calculators as calculators
from ksdft2effmass.calculators._dft import (
    CalculatorArtifactIdentity,
    ProcessObservationIdentity,
    QuantumEspressoDosInput,
    QuantumEspressoDosOutput,
    QuantumEspressoNscfInput,
    QuantumEspressoNscfOutput,
    SimulationInputIdentity,
    SimulationTypeInput,
    SimulationTypeOutput,
)
from ksdft2effmass.workflows import ResultObject, ResultObjectIdentity

pytestmark = pytest.mark.software_verification


def test_artifact__nscf_input__binds_exact_scf_result_and_state() -> None:
    """Evidence ID: SV-DFT-NSCF-DOS-001

    Requirement: A QE NSCF input retains its own exact native input and
    pseudopotentials plus the admitted SCF result and immutable native-state identity.

    Method: Construct one input from fixed nominal identities, inspect every field,
    and attempt mutation.

    Oracle: The private operation contract declares the exact five fields and frozen
    record behavior.

    Acceptance: Fields equal the supplied values and assignment raises
    ``FrozenInstanceError``.

    Interpretation: Failure identifies NSCF input identity or immutability drift.

    Limitations: Identity binding does not inspect or validate native-state contents.
    """
    input_identity = SimulationInputIdentity("qe.nscf.input")
    native_input = CalculatorArtifactIdentity("sha256:nscf-input")
    pseudopotential = CalculatorArtifactIdentity("sha256:si-pseudo")
    scf_output = ResultObjectIdentity("qe.scf.output")
    state = CalculatorArtifactIdentity("sha256:scf-state")
    value = QuantumEspressoNscfInput(
        input_identity,
        native_input,
        (pseudopotential,),
        scf_output,
        state,
    )

    assert value.identity is input_identity
    assert value.native_input_identity is native_input
    assert value.pseudopotential_identities == (pseudopotential,)
    assert value.scf_output_identity is scf_output
    assert value.native_state_identity is state
    with pytest.raises(FrozenInstanceError):
        value.native_state_identity = CalculatorArtifactIdentity("replacement")  # type: ignore[misc]


def test_artifact__dos_input__binds_exact_nscf_result_and_state() -> None:
    """Evidence ID: SV-DFT-NSCF-DOS-002

    Requirement: A QE DOS input retains its exact native input together with the
    admitted NSCF result and immutable post-NSCF native-state identity, without a
    pseudopotential field that ``dos.x`` does not consume.

    Method: Construct one DOS input and inspect its declared fields.

    Oracle: The private operation contract fixes four nominal identity fields and no
    pseudopotential collection.

    Acceptance: Every field equals the supplied value and the record has no
    ``pseudopotential_identities`` attribute.

    Interpretation: Failure identifies DOS predecessor or native-input contract drift.

    Limitations: This does not establish that the native state is readable by QE.
    """
    value = QuantumEspressoDosInput(
        SimulationInputIdentity("qe.dos.input"),
        CalculatorArtifactIdentity("sha256:dos-input"),
        ResultObjectIdentity("qe.nscf.output"),
        CalculatorArtifactIdentity("sha256:nscf-state"),
    )

    assert value.identity.value == "qe.dos.input"
    assert value.native_input_identity.value == "sha256:dos-input"
    assert value.nscf_output_identity.value == "qe.nscf.output"
    assert value.native_state_identity.value == "sha256:nscf-state"
    assert not hasattr(value, "pseudopotential_identities")


def test_artifact__operation_outputs__separate_state_and_dos_artifacts() -> None:
    """Evidence ID: SV-DFT-NSCF-DOS-003

    Requirement: NSCF produces a new native-state identity whereas DOS produces a DOS
    result-artifact identity, and each output retains its own process observation.

    Method: Construct one result of each concrete variant and inspect structural
    ResultObject conformance and variant-specific artifact fields.

    Oracle: The private operation contracts distinguish continuation state from final
    DOS data and require one mechanical process-observation identity per output.

    Acceptance: Both values conform to ``ResultObject`` and preserve the exact,
    differently named output artifact and process identities.

    Interpretation: Failure identifies result variant collapse or correlation drift.

    Limitations: Mechanical output records make no completion or scientific claim.
    """
    nscf = QuantumEspressoNscfOutput(
        ResultObjectIdentity("qe.nscf.output"),
        SimulationInputIdentity("qe.nscf.input"),
        ProcessObservationIdentity("qe.nscf.process"),
        CalculatorArtifactIdentity("sha256:nscf-state"),
    )
    dos = QuantumEspressoDosOutput(
        ResultObjectIdentity("qe.dos.output"),
        SimulationInputIdentity("qe.dos.input"),
        ProcessObservationIdentity("qe.dos.process"),
        CalculatorArtifactIdentity("sha256:dos-data"),
    )

    assert isinstance(nscf, ResultObject)
    assert isinstance(dos, ResultObject)
    assert nscf.native_state_identity.value == "sha256:nscf-state"
    assert nscf.process_observation_identity.value == "qe.nscf.process"
    assert dos.native_dos_result_identity.value == "sha256:dos-data"
    assert dos.process_observation_identity.value == "qe.dos.process"


def test_artifact__predecessor_fields__reject_wrong_nominal_identities() -> None:
    """Evidence ID: SV-DFT-NSCF-DOS-004

    Requirement: Predecessor ResultObject identities and native-state artifact
    identities are not interchangeable even though both contain strings.

    Method: Construct NSCF and DOS inputs with the two nominal identity types swapped.

    Oracle: Exact nominal validation assigns result correlation and artifact identity
    different semantic roles.

    Acceptance: Each malformed construction raises ``TypeError``.

    Interpretation: Failure identifies accidental structural interchangeability.

    Limitations: Nominal typing does not prove cross-object compatibility.
    """
    with pytest.raises(TypeError):
        QuantumEspressoNscfInput(
            SimulationInputIdentity("qe.nscf.input"),
            CalculatorArtifactIdentity("sha256:nscf-input"),
            (CalculatorArtifactIdentity("sha256:si-pseudo"),),
            CalculatorArtifactIdentity("sha256:not-a-result"),  # type: ignore[arg-type]
            CalculatorArtifactIdentity("sha256:scf-state"),
        )
    with pytest.raises(TypeError):
        QuantumEspressoDosInput(
            SimulationInputIdentity("qe.dos.input"),
            CalculatorArtifactIdentity("sha256:dos-input"),
            ResultObjectIdentity("qe.nscf.output"),
            ResultObjectIdentity("not-an-artifact"),  # type: ignore[arg-type]
        )


def test_artifact__closed_unions__include_nscf_and_dos_variants() -> None:
    """Evidence ID: SV-DFT-NSCF-DOS-005

    Requirement: The private injected DFT calculator port accepts the new concrete QE
    NSCF and DOS input and output variants without erasing their concrete types.

    Method: Inspect the runtime arguments of both closed private type aliases.

    Oracle: The bounded probe contract explicitly adds one input and one output
    variant for each operation.

    Acceptance: The four concrete NSCF and DOS types are members of the corresponding
    union arguments.

    Interpretation: Failure identifies private calculator-port coverage drift.

    Limitations: Union membership does not invoke or authorize a calculator.
    """
    input_variants = get_args(SimulationTypeInput.__value__)
    output_variants = get_args(SimulationTypeOutput.__value__)

    assert QuantumEspressoNscfInput in input_variants
    assert QuantumEspressoDosInput in input_variants
    assert QuantumEspressoNscfOutput in output_variants
    assert QuantumEspressoDosOutput in output_variants


def test_artifact__package_surface__keeps_operation_variants_private() -> None:
    """Evidence ID: SV-DFT-NSCF-DOS-006

    Requirement: The new QE operation variants remain private and revisable during
    actual-data workflow probing.

    Method: Inspect representative names on the supported calculator package.

    Oracle: The architecture decision explicitly adds no calculator package export.

    Acceptance: The NSCF and DOS input/result names are absent.

    Interpretation: Failure identifies premature public API stabilization.

    Limitations: Attribute absence does not establish package release behavior.
    """
    assert not hasattr(calculators, "QuantumEspressoNscfInput")
    assert not hasattr(calculators, "QuantumEspressoNscfOutput")
    assert not hasattr(calculators, "QuantumEspressoDosInput")
    assert not hasattr(calculators, "QuantumEspressoDosOutput")
