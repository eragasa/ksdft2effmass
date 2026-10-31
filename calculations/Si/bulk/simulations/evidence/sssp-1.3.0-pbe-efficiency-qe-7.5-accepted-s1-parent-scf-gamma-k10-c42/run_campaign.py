from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, replace
from datetime import UTC, datetime
from pathlib import Path

import prepare_campaign as pre
from projectkoios.integrations.quantumespresso.pw.scf.handler import (
    QePwDftScfActionHandler,
    QePwDftScfTask,
)
from projectkoios.integrations.quantumespresso.pw.scf.integration import (
    QePwDftScfIntegration,
)
from projectkoios.physkit.periodic.unit_cell import UnitCellJsonCodec
from projectkoios.physkit.units import MODEL_SYSTEM_UNIT_CONVERTER, PhysicalUnit
from projectkoios.simulations.dft.pseudopotential.library import PseudopotentialLibrary
from projectkoios.simulations.dft.pw.scf.base import (
    PwDftScfWorkflowFailed,
    PwDftScfWorkflowSucceeded,
)
from projectkoios.simulations.structure import (
    ObservedStructureProvenance,
    ObservedStructureScope,
    StructureProvenanceReference,
    StructureRecord,
    StructureRecordReference,
    StructureRepresentation,
    StructureResolution,
)
from projectkoios.simulations.workflows.pw_dft_scf.convergence.base import (
    PwDftScfConvergenceCoordinate,
)
from projectkoios.simulations.workflows.pw_dft_scf.cpn.workflow import (
    LocalPwDftScfWorkflow,
)
from projectkoios.simulations.workflows.pw_dft_scf.recipe import (
    PwDftScfKpointConvergenceRecipe,
    PwDftScfSingleCalculationRecipe,
)
from tools.pw_dft_scf.environment import WorkflowRunnerEnvironment

AUTHORIZATION_MESSAGE = (
    "Authorize exactly one accepted-S1 parent SCF invocation described in "
    "campaign-preflight.json, with zero retries and stop on failure."
)


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tree_size(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def inventory(root: Path) -> dict[str, object]:
    files = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "byte_size": path.stat().st_size,
                "sha256": pre.sha256(path),
            }
        )
    return {
        "schema_version": 1,
        "root": str(root),
        "file_count": len(files),
        "total_bytes": sum(int(item["byte_size"]) for item in files),
        "files": files,
    }


def build_campaign() -> tuple[
    object,
    QePwDftScfIntegration,
    PseudopotentialLibrary,
    object,
    object,
]:
    structure_content = pre.STRUCTURE_PATH.read_bytes()
    if len(structure_content) != pre.STRUCTURE_BYTES:
        raise RuntimeError("S1 byte-size mismatch")
    if hashlib.sha256(structure_content).hexdigest() != pre.STRUCTURE_SHA256:
        raise RuntimeError("S1 SHA-256 mismatch")
    unit_cell = UnitCellJsonCodec().loads(
        structure_content.decode("utf-8"), expected_structure_id=pre.STRUCTURE_ID
    )
    relaxation_calculation = pre.RELAXATION_ROOT / "calculation.toml"
    relaxation_evidence = pre.RELAXATION_ROOT / "result/relaxation-result.json"
    structure_record = StructureRecord(
        structure_id=pre.STRUCTURE_ID,
        representation=StructureRepresentation.primitive,
        schema_version=1,
        sha256=pre.STRUCTURE_SHA256,
        byte_size=pre.STRUCTURE_BYTES,
        provenance=ObservedStructureProvenance(
            starting_structure=StructureRecordReference(
                structure_id="Si.PrimitiveUnitCell.RightHanded",
                representation=StructureRepresentation.primitive,
                schema_version=1,
                byte_size=692,
                sha256="7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a",
            ),
            relaxation_calculation=StructureProvenanceReference(
                stable_id="si-bulk-vc-relax-ibrav2-gamma-k10-c42",
                representation="projectkoios-calculation-toml",
                schema_version=1,
                byte_size=relaxation_calculation.stat().st_size,
                sha256=pre.sha256(relaxation_calculation),
            ),
            relaxation_evidence=StructureProvenanceReference(
                stable_id="si-bulk-vc-relax-ibrav2-gamma-k10-c42-result",
                representation="ksdft2effmass-relaxation-result-json",
                schema_version=1,
                byte_size=relaxation_evidence.stat().st_size,
                sha256=pre.sha256(relaxation_evidence),
            ),
            scope=ObservedStructureScope.atomic_positions_and_cell,
            publication_operation="ksdft2effmass.qe-vc-relax.publish-source-basis",
            publication_version="1",
            result_sha256=pre.STRUCTURE_SHA256,
        ),
    )
    structure = StructureResolution(
        record=structure_record, path=pre.STRUCTURE_PATH, unit_cell=unit_cell
    )
    environment = WorkflowRunnerEnvironment.load(pre.RUNNER_CONFIG)
    loaded = environment.loader.load(pre.SOURCE_CAMPAIGN)
    source_recipe = loaded.campaign.recipe
    if not isinstance(source_recipe, PwDftScfKpointConvergenceRecipe):
        raise TypeError("source campaign is not k-point convergence")
    cutoff_ev = pre.WAVEFUNCTION_CUTOFF_RY * (
        MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
            PhysicalUnit("rydberg"), PhysicalUnit("eV")
        )
    )
    source_specification = source_recipe.base_request.specification
    specification = replace(
        source_specification,
        simulation_id=(
            "Si.PrimitiveUnitCell.RightHanded.RelaxedS1.QE.SCF."
            "AcceptedParent.SSSP130.PBE.GammaK10.C42Ry"
        ),
        simulation=replace(source_specification.simulation, structure=structure_record),
        wavefunction_cutoff_ev=cutoff_ev,
        kpoint_sampling=replace(
            source_specification.kpoint_sampling,
            mesh=(pre.MESH_DENSITY, pre.MESH_DENSITY, pre.MESH_DENSITY),
            shift=(0, 0, 0),
        ),
    )
    base_request = replace(
        source_recipe.base_request,
        evaluation_id="ksdft-si-accepted-s1-parent-scf-preflight-base",
        specification=specification,
    )
    recipe = PwDftScfSingleCalculationRecipe(
        campaign_id="ksdft-si-accepted-s1-parent-scf",
        base_request=base_request,
    )
    coordinate = PwDftScfConvergenceCoordinate(
        mesh_density=pre.MESH_DENSITY, wavefunction_cutoff_ev=cutoff_ev
    )
    request = recipe.request_for(coordinate, scope="preflight")
    projection_configuration = environment.loader.qe_projection_configuration(
        loaded.projection_profile_id
    )
    integration = QePwDftScfIntegration(
        artifact_root=pre.ROOT, projection_configuration=projection_configuration
    )
    prepared = integration.project(request, structure)
    library = PseudopotentialLibrary(root=pre.PSEUDOPOTENTIAL_ROOT)
    return loaded, integration, library, request, prepared


def main() -> None:
    manifest = json.loads((pre.ROOT / "campaign-preflight.json").read_text())
    expected_authorization = {
        "maximum_invocations": 1,
        "retries": 0,
        "stop_on_failure": True,
    }
    if manifest["authorization_request"] != expected_authorization:
        raise RuntimeError("preflight authorization bounds changed")
    if manifest["execution_performed"] is not False:
        raise RuntimeError("preflight does not declare an unexecuted campaign")
    if pre.sha256(pre.ACCEPTED_PAIR_PATH) != pre.ACCEPTED_PAIR_SHA256:
        raise RuntimeError("accepted stable-pair identity mismatch")
    if pre.sha256(pre.EXECUTABLE) != pre.EXECUTABLE_SHA256:
        raise RuntimeError("QE executable identity mismatch")
    run_root = pre.ROOT / "run"
    if run_root.exists():
        raise RuntimeError("run directory already exists; retries are prohibited")

    loaded, integration, library, request, prepared = build_campaign()
    artifact = prepared.artifacts[0]
    retained_input = pre.ROOT / "preflight/pw.in"
    if artifact.content != retained_input.read_bytes():
        raise RuntimeError("rendered input differs from preflight")
    occurrence = manifest["occurrence"]
    if prepared.sha256 != occurrence["prepared_input_sha256"]:
        raise RuntimeError("prepared-input identity mismatch")
    if artifact.sha256 != occurrence["pw_input"]["sha256"]:
        raise RuntimeError("pw.in identity mismatch")

    run_root.mkdir(mode=0o700)
    write_json(
        pre.ROOT / "authorization.json",
        {
            "schema_version": 1,
            "authorized": True,
            "operator_message": AUTHORIZATION_MESSAGE,
            "authorized_bounds": expected_authorization,
            "authorized_at_utc": datetime.now(UTC).isoformat(),
            "campaign_preflight_sha256": pre.sha256(
                pre.ROOT / "campaign-preflight.json"
            ),
            "run_script_sha256": pre.sha256(pre.ROOT / "run_campaign.py"),
        },
    )
    task = QePwDftScfTask(
        evaluation_id=request.evaluation_id,
        task_id="ksdft-si-accepted-s1-parent-scf-attempt-1",
        output_artifact_id="run/pw.out",
        prepared_input=prepared,
        pseudopotentials=request.specification.simulation.pseudopotentials,
        pseudopotential_library=library,
        executable=pre.EXECUTABLE,
        working_directory=run_root,
        timeout_seconds=pre.TIMEOUT_SECONDS,
        execution_authorized=True,
    )
    handler = QePwDftScfActionHandler(integration=integration, tasks=(task,))
    write_json(pre.ROOT / "campaign-progress.json", {"status": "running"})
    workflow = LocalPwDftScfWorkflow(
        evaluation_id=request.evaluation_id, runtime=loaded.campaign.runtime
    )
    fired: list[str] = []
    while workflow.outcome() is None:
        actions = workflow.pending_actions()
        if len(actions) != 1:
            raise RuntimeError("SCF workflow requires one pending action")
        for event in handler.handle(actions[0]):
            fired.extend(workflow.accept(event))
    outcome = workflow.outcome()
    if isinstance(outcome, PwDftScfWorkflowFailed):
        write_json(
            pre.ROOT / "campaign-result.json",
            {
                "status": "failed",
                "failure": asdict(outcome),
                "invocation_count": 1,
                "retries_performed": 0,
            },
        )
        raise RuntimeError(  # noqa: TRY004
            f"parent SCF failed: {outcome.code}"
        )
    if not isinstance(outcome, PwDftScfWorkflowSucceeded):
        raise TypeError("SCF workflow returned an unknown outcome")
    retained_bytes = tree_size(run_root)
    if retained_bytes > pre.MAXIMUM_BYTES:
        raise RuntimeError("parent SCF exceeded retained-byte bound")
    saved_state = run_root / "tmp/system.save"
    if not saved_state.is_dir() or saved_state.is_symlink():
        raise RuntimeError("parent SCF saved state is unavailable")
    saved_manifest = inventory(saved_state)
    write_json(pre.ROOT / "saved-state-manifest.json", saved_manifest)
    run_manifest = inventory(run_root)
    write_json(pre.ROOT / "run-artifact-manifest.json", run_manifest)
    observation = outcome.result.observation
    result = {
        "status": "succeeded",
        "invocation_count": 1,
        "retries_performed": 0,
        "accepted_pair": manifest["accepted_pair"],
        "observation": {
            "evaluation_id": outcome.result.evaluation_id,
            "task_id": outcome.result.task_id,
            "total_energy_ev": observation.total_energy_ev,
            "total_energy_ev_per_atom": observation.total_energy_ev_per_atom,
            "atom_count": observation.atom_count,
            "electronic_iteration_count": observation.electronic_iteration_count,
            "completed": observation.completed,
            "converged": observation.converged,
            "program_version": observation.program_version,
            "irreducible_kpoint_count": observation.irreducible_kpoint_count,
            "observed_wavefunction_cutoff_ev": observation.wavefunction_cutoff_ev,
            "diagnostics": [
                {
                    "code": item.code,
                    "severity": item.severity.value,
                    "message": item.message,
                }
                for item in observation.diagnostics
            ],
            "fired_transitions": fired,
        },
        "artifacts": {
            "pw_input": pre.observed(run_root / "pw.in"),
            "pw_output": pre.observed(run_root / "pw.out"),
            "pw_stderr": pre.observed(run_root / "pw.err"),
            "execution_record": pre.observed(run_root / "execution.json"),
            "qexsd": pre.observed(saved_state / "data-file-schema.xml"),
            "saved_state_manifest": pre.observed(
                pre.ROOT / "saved-state-manifest.json"
            ),
            "run_artifact_manifest": pre.observed(
                pre.ROOT / "run-artifact-manifest.json"
            ),
        },
        "retained_bytes": retained_bytes,
        "scientific_disposition": (
            "accepted-pair parent SCF process and saved-state evidence; downstream "
            "NSCF and Wannier stages remain separately authorized"
        ),
    }
    write_json(pre.ROOT / "campaign-result.json", result)
    write_json(pre.ROOT / "campaign-progress.json", {"status": "completed"})


if __name__ == "__main__":
    main()
