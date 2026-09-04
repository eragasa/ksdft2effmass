r"""Software verification of retained QE silicon DOS Workflow observation.

Evidence profile: routine

Bounded artifact scope: the compact calculated QE 7.5 silicon SCF-to-NSCF-to-DOS
Workflow observation retained under ``examples/tutorials/silicon-dos``.

Facet and represented meaning

The artifact records exact input, executable, Task-control, immutable state-handoff,
process, CPN firing, and DOS artifact identities from one authorized tutorial run.

Intrinsic and cross-object scope

Tests cover record correlation and bounded mechanical observations. The checked-in
JSON is the oracle; full native states and calculator output remain external.

VVUQ and scientific exclusions

This is software verification of retained provenance. It does not rerun Quantum
ESPRESSO or establish production convergence, numerical verification, scientific
validation, uncertainty quantification, accepted geometry, or a reference DOS.
"""

import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


def retained_observation() -> dict[str, object]:
    """Evidence ID: Helper owns no identifier.

    Requirement: Load the exact checked-in compact Workflow observation.

    Method: Resolve the repository-relative JSON path and parse it with ``json``.

    Oracle: The project tutorial layout fixes the single retained file location.

    Acceptance: Return the parsed top-level JSON object.

    Interpretation: Failure identifies missing or malformed retained evidence.

    Limitations: Loading does not inspect external native artifacts.
    """
    repository_root = Path(__file__).resolve().parents[5]
    path = repository_root / (
        "examples/tutorials/silicon-dos/qe/expected/qe75-calculated-observation.json"
    )
    value = json.loads(path.read_text(encoding="utf-8"))
    assert type(value) is dict
    return value


def test_artifact__provenance__retains_exact_inputs_and_executables() -> None:
    """Evidence ID: SV-RETAINED-SILICON-DOS-001

    Requirement: The retained Workflow binds the selected geometry and exact SCF,
    NSCF, DOS, pseudopotential, and QE 7.5 executable identities.

    Method: Inspect the fixed provenance fields in the compact observation.

    Oracle: The authorized preflight fixes every expected identity and geometry value.

    Acceptance: Every recorded hash and the lattice constant equals the preflight
    value exactly.

    Interpretation: Failure identifies retained execution-provenance drift.

    Limitations: Hash agreement does not establish scientific suitability.
    """
    value = retained_observation()
    source = value["source"]
    assert type(source) is dict
    geometry = source["selected_geometry"]
    inputs = source["inputs"]
    executables = source["executables"]
    assert type(geometry) is dict
    assert type(inputs) is dict
    assert type(executables) is dict

    assert geometry["conventional_cubic_lattice_constant_bohr"] == 10.207479550732002
    assert inputs["scf"]["sha256"] == (
        "23714f9a78a1e6436b4a0b68ce58932e14141e1efa69a82eb0e2c4e950582657"
    )
    assert inputs["nscf"]["sha256"] == (
        "5b0ee9fbc27f735a652845a96a122fc59d9e7d59e5d37f5e8ccda18edf5afd34"
    )
    assert inputs["dos"]["sha256"] == (
        "9d1eedb8d792fddcdbf0bb6d266799cf98f36655c033a24015f48eb45230fe65"
    )
    assert source["pseudopotential"]["sha256"] == (
        "e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217"
    )
    assert executables["pw.x"]["sha256"] == (
        "87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910"
    )
    assert executables["dos.x"]["sha256"] == (
        "0b5dfbbf63e0dba23771d9ddeb25991b14148f2fc9f819be61745b2d288b33f8"
    )


def test_artifact__control__retains_three_independent_task_firings() -> None:
    """Evidence ID: SV-RETAINED-SILICON-DOS-002

    Requirement: SCF, NSCF, and DOS retain distinct run-scoped control identities and
    fire in the admitted predecessor-result order without retry or automatic successor
    activation.

    Method: Inspect the retained independent-control and CPN summaries.

    Oracle: The authorized architecture fixes three distinct identities per control
    role and the exact ``dft.scf``, ``dft.nscf``, ``dft.dos`` order.

    Acceptance: The distinctness flag is true, every identity collection has length
    three, all attempts are ordinal one, grants are consumed, and firing order matches.

    Interpretation: Failure identifies Task independence or CPN correlation drift.

    Limitations: The compact record does not implement a general execution service.
    """
    value = retained_observation()
    controls = value["independent_task_controls"]
    cpn = value["cpn"]
    assert type(controls) is dict
    assert type(cpn) is dict

    assert controls["all_identity_sets_have_three_distinct_members"] is True
    assert len(controls["task_instance_identities"]) == 3
    assert len(controls["activation_identities"]) == 3
    assert len(controls["attempt_identities"]) == 3
    assert len(controls["grant_identities"]) == 3
    assert len(controls["process_observation_identities"]) == 3
    assert len(controls["result_object_identities"]) == 3
    assert controls["attempt_ordinals"] == [1, 1, 1]
    assert controls["grant_terminal_statuses"] == ["consumed", "consumed", "consumed"]
    assert controls["automatic_retry"] is False
    assert controls["automatic_successor_activation"] is False
    assert cpn["firing_order"] == ["dft.scf", "dft.nscf", "dft.dos"]


def test_artifact__handoffs__retain_exact_immutable_state_copies() -> None:
    """Evidence ID: SV-RETAINED-SILICON-DOS-003

    Requirement: NSCF consumes the admitted SCF state and DOS consumes the admitted
    NSCF state through separately verified immutable copies.

    Method: Compare each retained source, predecessor-copy, and pre-invocation work-copy
    tree identity.

    Oracle: An identity-preserving handoff requires exact equality within each edge and
    different post-SCF and post-NSCF identities.

    Acceptance: Both edge checks are true, identities match within each edge, and the
    two edge source identities differ.

    Interpretation: Failure identifies immutable continuation-state correlation drift.

    Limitations: The full tree manifests remain in the external run.
    """
    value = retained_observation()
    handoffs = value["immutable_handoffs"]
    assert type(handoffs) is dict
    scf_to_nscf = handoffs["scf_to_nscf"]
    nscf_to_dos = handoffs["nscf_to_dos"]
    assert type(scf_to_nscf) is dict
    assert type(nscf_to_dos) is dict

    assert scf_to_nscf["copies_verified"] is True
    assert nscf_to_dos["copies_verified"] is True
    assert (
        scf_to_nscf["source_native_state_identity"]
        == (scf_to_nscf["predecessor_state_copy_identity"])
    )
    assert (
        scf_to_nscf["source_native_state_identity"]
        == (scf_to_nscf["work_state_copy_identity_before_invocation"])
    )
    assert (
        nscf_to_dos["source_native_state_identity"]
        == (nscf_to_dos["predecessor_state_copy_identity"])
    )
    assert (
        nscf_to_dos["source_native_state_identity"]
        == (nscf_to_dos["work_state_copy_identity_before_invocation"])
    )
    assert (
        scf_to_nscf["source_native_state_identity"]
        != (nscf_to_dos["source_native_state_identity"])
    )


def test_artifact__dos_result__retains_bounded_finite_parse() -> None:
    """Evidence ID: SV-RETAINED-SILICON-DOS-004

    Requirement: The admitted DOS result retains process completion, tetrahedron use,
    exact artifact identity, and bounded finite grid-shape observations.

    Method: Inspect the DOS Task and artifact summaries in the compact observation.

    Oracle: The identified output file mechanically contains one header and 2,501
    finite three-column rows on the exact −9 to 16 eV, 0.01 eV grid.

    Acceptance: Exit and timeout fields indicate completion, calculator markers are
    present, and all exact artifact and grid fields match.

    Interpretation: Failure identifies compact DOS process or parse-record drift.

    Limitations: These structural observations do not validate the DOS values.
    """
    value = retained_observation()
    tasks = value["tasks"]
    assert type(tasks) is dict
    dos = tasks["dos"]
    assert type(dos) is dict
    execution = dos["execution"]
    observations = dos["calculator_observations"]
    artifact = dos["dos_artifact"]
    assert type(execution) is dict
    assert type(observations) is dict
    assert type(artifact) is dict

    assert execution["exit_status"] == 0
    assert execution["timed_out"] is False
    assert observations["job_done_marker_present"] is True
    assert observations["tetrahedra_used_reported"] is True
    assert artifact["sha256"] == (
        "b967ed73c7d2572123dbf0b928630e38868ad2f9afbb1b3e77f140ecd53bf6df"
    )
    assert artifact["byte_count"] == 82588
    assert artifact["data_row_count"] == 2501
    assert artifact["column_count"] == 3
    assert artifact["all_values_finite"] is True
    assert artifact["energy_min_ev"] == -9.0
    assert artifact["energy_max_ev"] == 16.0
    assert artifact["uniform_energy_step_ev"] == 0.01
