r"""Software verification of private reusable DFT SCF-NSCF-DOS CPN Task composition.

Evidence profile: routine

Bounded artifact scope: private reusable SCF, NSCF, and DOS Task-instance
composition and its effect-free CPN result-availability topology.

Facet and represented meaning

The artifact represents three independent run-scoped Task instances built from
reusable operation definitions and ordered by explicit result dependencies.

Intrinsic and cross-object scope

Tests cover distinct Task instances, reusable definition identities, exact
Task-to-transition correlation, predecessor-state arcs, and fail-closed construction.

VVUQ and scientific exclusions

This is software verification of a private revisable composition. Synthetic
identities are used only to inspect topology. No scientific executable is invoked and
no convergence, numerical verification, scientific validation, uncertainty
quantification, physical result, or human acceptance is established.
"""

import pytest

import ksdft2effmass.workflows as workflows
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetDefinitionValidator,
    ColoredPetriNetInputMode,
)
from ksdft2effmass.workflows import TaskInstanceIdentity
from ksdft2effmass.workflows._dft_scf_nscf_dos import (
    DftScfNscfDosCpnComposer,
    DftScfNscfDosCpnCompositionInput,
)

pytestmark = pytest.mark.software_verification


def make_composition_input(prefix: str) -> DftScfNscfDosCpnCompositionInput:
    """Return three explicit synthetic Task-instance identities.

    Evidence ID: Helper owns no identifier.

    Requirement: Support composition evidence with distinct run-scoped identities.

    Method: Construct the three nominal identities from one explicit lexical prefix.

    Oracle: The explicit prefix and operation suffixes fix the three expected values.

    Acceptance: Return one valid immutable composition input.

    Interpretation: Failure identifies synthetic setup construction drift.

    Limitations: The helper owns no independent composition or scientific claim.
    """
    return DftScfNscfDosCpnCompositionInput(
        TaskInstanceIdentity(f"{prefix}.scf"),
        TaskInstanceIdentity(f"{prefix}.nscf"),
        TaskInstanceIdentity(f"{prefix}.dos"),
    )


def test_artifact__composition__creates_independent_reusable_task_instances() -> None:
    """Evidence ID: SV-DFT-SCF-NSCF-DOS-CPN-001

    Requirement: SCF, NSCF, and DOS are distinct run-scoped Task instances of
    reusable operation definitions, each correlated with its own CPN transition.

    Method: Compose two runs with disjoint instance identities and inspect their
    Task, Workflow, CPN, and correlation identities.

    Oracle: The accepted private architecture fixes three reusable definitions and
    one Task-to-transition correlation per run-scoped operation instance.

    Acceptance: Two compositions retain different supplied instance identities but
    the exact same Workflow, Task-definition, CPN-definition, and transition
    identities; every composition contains three one-to-one Task-transition bindings.

    Interpretation: Failure identifies Task independence, reuse, or correlation drift.

    Limitations: This checks identity composition without dispatching a Task.
    """
    first = DftScfNscfDosCpnComposer().execute(make_composition_input("run.one"))
    second = DftScfNscfDosCpnComposer().execute(make_composition_input("run.two"))

    first_tasks = first.workflow_composition.task_instances
    second_tasks = second.workflow_composition.task_instances
    assert tuple(item.identity.value for item in first_tasks) == (
        "run.one.scf",
        "run.one.nscf",
        "run.one.dos",
    )
    assert tuple(item.identity.value for item in second_tasks) == (
        "run.two.scf",
        "run.two.nscf",
        "run.two.dos",
    )
    assert tuple(item.definition_identity.value for item in first_tasks) == (
        "dft.scf",
        "dft.nscf",
        "dft.dos",
    )
    assert tuple(item.definition_identity for item in first_tasks) == tuple(
        item.definition_identity for item in second_tasks
    )
    assert first.workflow_composition.workflow_identity.value == ("dft.scf-nscf-dos.v1")
    assert first.definition == second.definition
    assert tuple(
        (
            item.task_instance_identity.value,
            item.transition_identity.value,
        )
        for item in first.task_transition_bindings
    ) == (
        ("run.one.scf", "dft.scf"),
        ("run.one.nscf", "dft.nscf"),
        ("run.one.dos", "dft.dos"),
    )


def test_artifact__topology__requires_admitted_scf_then_nscf_then_dos() -> None:
    """Evidence ID: SV-DFT-SCF-NSCF-DOS-CPN-002

    Requirement: NSCF reads the admitted SCF result and DOS reads the admitted NSCF
    result while each operation consumes only its own prepared-input token.

    Method: Validate the composed generic definition and inspect exact transition
    priority, predecessor arcs, prepared-input arcs, places, and modes.

    Oracle: The architecture requires SCF before NSCF before DOS, immutable
    predecessor-result availability, and operation-local prepared-input consumption.

    Acceptance: The generic definition validates without findings; transition
    priority is SCF, NSCF, DOS; predecessor arcs are READ; and prepared-input arcs are
    CONSUME with the exact source and target identities.

    Interpretation: Failure identifies dependency or token-ownership topology drift.

    Limitations: This verifies a pure definition, not native-state content or effects.
    """
    result = DftScfNscfDosCpnComposer().execute(make_composition_input("run"))
    definition = result.definition
    arcs = {item.identity.value: item for item in definition.arcs}

    assert ColoredPetriNetDefinitionValidator().execute(definition).issues == ()
    assert tuple(item.value for item in definition.transition_priority) == (
        "dft.scf",
        "dft.nscf",
        "dft.dos",
    )
    assert arcs["nscf.scf-state"].place_identity.value == "scf.completed"
    assert arcs["nscf.scf-state"].transition_identity.value == "dft.nscf"
    assert arcs["nscf.scf-state"].input_inscription is not None
    assert (
        arcs["nscf.scf-state"].input_inscription.mode is ColoredPetriNetInputMode.READ
    )
    assert arcs["dos.nscf-state"].place_identity.value == "nscf.completed"
    assert arcs["dos.nscf-state"].transition_identity.value == "dft.dos"
    assert arcs["dos.nscf-state"].input_inscription is not None
    assert (
        arcs["dos.nscf-state"].input_inscription.mode is ColoredPetriNetInputMode.READ
    )
    scf_input_inscription = arcs["scf.input"].input_inscription
    nscf_input_inscription = arcs["nscf.input"].input_inscription
    dos_input_inscription = arcs["dos.input"].input_inscription
    assert scf_input_inscription is not None
    assert nscf_input_inscription is not None
    assert dos_input_inscription is not None
    assert scf_input_inscription.mode is ColoredPetriNetInputMode.CONSUME
    assert nscf_input_inscription.mode is ColoredPetriNetInputMode.CONSUME
    assert dos_input_inscription.mode is ColoredPetriNetInputMode.CONSUME


def test_artifact__construction__rejects_shared_task_instance_identity() -> None:
    """Evidence ID: SV-DFT-SCF-NSCF-DOS-CPN-003

    Requirement: The three operation roles cannot share one run-scoped Task-instance
    identity.

    Method: Construct an input with one identity assigned to both SCF and NSCF.

    Oracle: Independent run-scoped Tasks require pairwise-distinct instance identities.

    Acceptance: Reusing any identity raises ``ValueError`` before composition.

    Interpretation: Failure would allow operation roles to collapse into one instance.

    Limitations: Other runtime correlation checks belong to Workflow control.
    """
    shared = TaskInstanceIdentity("run.shared")
    with pytest.raises(ValueError):
        DftScfNscfDosCpnCompositionInput(
            shared,
            shared,
            TaskInstanceIdentity("run.dos"),
        )


def test_artifact__package_surface__keeps_composition_private() -> None:
    """Evidence ID: SV-DFT-SCF-NSCF-DOS-CPN-004

    Requirement: The probe composition remains private and revisable until later
    workflow evidence supports a stable public contract.

    Method: Inspect the supported Workflow package attributes directly.

    Oracle: The architecture decision keeps this probe private and adds no export.

    Acceptance: Representative composition types are absent from the supported
    ``ksdft2effmass.workflows`` package surface.

    Interpretation: Failure identifies premature public API stabilization.

    Limitations: Attribute absence does not establish packaging or release behavior.
    """
    assert not hasattr(workflows, "DftScfNscfDosCpnComposer")
    assert not hasattr(workflows, "DftScfNscfDosCpnCompositionInput")
