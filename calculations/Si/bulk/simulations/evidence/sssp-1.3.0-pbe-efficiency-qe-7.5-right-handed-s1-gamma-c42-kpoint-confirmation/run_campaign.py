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
from projectkoios.simulations.workflows.pw_dft_scf.convergence.assessment import (
    EnergyAxisConvergenceAssessmentRequest,
    EnergyAxisConvergenceAssessor,
)
from projectkoios.simulations.workflows.pw_dft_scf.convergence.base import (
    PwDftScfConvergenceAxis,
    PwDftScfEnergyObservation,
)
from projectkoios.simulations.workflows.pw_dft_scf.cpn.workflow import (
    LocalPwDftScfWorkflow,
)
from projectkoios.simulations.workflows.pw_dft_scf.recipe import (
    PwDftScfKpointConvergenceRecipe,
)
from tools.pw_dft_scf.environment import WorkflowRunnerEnvironment

AUTHORIZATION_MESSAGE = (
    "Authorize exactly the four S1 K6, K8, K10, and K12 SCF invocations "
    "described in campaign-preflight.json, with zero retries and stop on first "
    "failure."
)


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tree_size(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def build_campaign() -> tuple[
    object,
    PwDftScfKpointConvergenceRecipe,
    QePwDftScfIntegration,
    PseudopotentialLibrary,
    tuple[object, ...],
    tuple[object, ...],
]:
    structure_content = pre.STRUCTURE_PATH.read_bytes()
    if len(structure_content) != pre.STRUCTURE_BYTES:
        raise RuntimeError("S1 byte-size mismatch")
    if hashlib.sha256(structure_content).hexdigest() != pre.STRUCTURE_SHA256:
        raise RuntimeError("S1 SHA-256 mismatch")
    unit_cell = UnitCellJsonCodec().loads(
        structure_content.decode("utf-8"),
        expected_structure_id=pre.STRUCTURE_ID,
    )
    relaxation_calculation = pre.RELAXATION_ROOT / "calculation.toml"
    relaxation_evidence = pre.RELAXATION_ROOT / "result/relaxation-result.json"
    s0_reference = StructureRecordReference(
        structure_id="Si.PrimitiveUnitCell.RightHanded",
        representation=StructureRepresentation.primitive,
        schema_version=1,
        byte_size=692,
        sha256="7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a",
    )
    structure_record = StructureRecord(
        structure_id=pre.STRUCTURE_ID,
        representation=StructureRepresentation.primitive,
        schema_version=1,
        sha256=pre.STRUCTURE_SHA256,
        byte_size=pre.STRUCTURE_BYTES,
        provenance=ObservedStructureProvenance(
            starting_structure=s0_reference,
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
        record=structure_record,
        path=pre.STRUCTURE_PATH,
        unit_cell=unit_cell,
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
            "GammaKpointConfirmation.SSSP130.PBE.C42Ry"
        ),
        simulation=replace(source_specification.simulation, structure=structure_record),
        wavefunction_cutoff_ev=cutoff_ev,
        kpoint_sampling=replace(
            source_specification.kpoint_sampling,
            mesh=(10, 10, 10),
            shift=(0, 0, 0),
        ),
    )
    base_request = replace(
        source_recipe.base_request,
        evaluation_id="ksdft-si-s1-gamma-kpoint-c42-preflight-base",
        specification=specification,
    )
    recipe = PwDftScfKpointConvergenceRecipe(
        campaign_id="ksdft-si-s1-kpoint-confirmation",
        base_request=base_request,
        mesh_densities=pre.MESHES,
        policy=source_recipe.policy,
    )
    projection_configuration = environment.loader.qe_projection_configuration(
        loaded.projection_profile_id
    )
    integration = QePwDftScfIntegration(
        artifact_root=pre.ROOT,
        projection_configuration=projection_configuration,
    )
    library = PseudopotentialLibrary(root=pre.PSEUDOPOTENTIAL_ROOT)
    requests = tuple(
        recipe.request_for(coordinate, scope="preflight")
        for coordinate in recipe.coordinates()
    )
    prepared_inputs = tuple(
        integration.project(request, structure) for request in requests
    )
    return loaded, recipe, integration, library, requests, prepared_inputs


def main() -> None:
    manifest = json.loads((pre.ROOT / "campaign-preflight.json").read_text())
    expected_authorization = {
        "coordinates_in_order": ["K6", "K8", "K10", "K12"],
        "maximum_invocations": 4,
        "retries": 0,
        "stop_on_first_failure": True,
    }
    if manifest["authorization_request"] != expected_authorization:
        raise RuntimeError("preflight authorization bounds changed")
    if manifest["execution_performed"] is not False:
        raise RuntimeError("preflight does not declare an unexecuted campaign")
    if pre.sha256(pre.EXECUTABLE) != pre.EXECUTABLE_SHA256:
        raise RuntimeError("QE executable SHA-256 mismatch")
    run_root = pre.ROOT / "run"
    if run_root.exists():
        raise RuntimeError("run directory already exists; retries are prohibited")

    loaded, recipe, integration, library, requests, prepared_inputs = build_campaign()
    for mesh, prepared, occurrence in zip(
        pre.MESHES,
        prepared_inputs,
        manifest["occurrences"],
        strict=True,
    ):
        artifact = prepared.artifacts[0]
        retained_input = pre.ROOT / f"preflight/K{mesh}/pw.in"
        if artifact.content != retained_input.read_bytes():
            raise RuntimeError(f"K{mesh} rendered input differs from preflight")
        if prepared.sha256 != occurrence["prepared_input_sha256"]:
            raise RuntimeError(f"K{mesh} prepared-input identity mismatch")
        if artifact.sha256 != occurrence["pw_input"]["sha256"]:
            raise RuntimeError(f"K{mesh} pw.in identity mismatch")

    run_root.mkdir(mode=0o700)
    authorization = {
        "schema_version": 1,
        "authorized": True,
        "operator_message": AUTHORIZATION_MESSAGE,
        "authorized_bounds": expected_authorization,
        "authorized_at_utc": datetime.now(UTC).isoformat(),
        "campaign_preflight_sha256": pre.sha256(pre.ROOT / "campaign-preflight.json"),
        "run_script_sha256": pre.sha256(pre.ROOT / "run_campaign.py"),
    }
    write_json(pre.ROOT / "authorization.json", authorization)

    tasks: list[QePwDftScfTask] = []
    for mesh, request, prepared in zip(
        pre.MESHES, requests, prepared_inputs, strict=True
    ):
        working_directory = run_root / f"K{mesh}"
        working_directory.mkdir(mode=0o700)
        tasks.append(
            QePwDftScfTask(
                evaluation_id=request.evaluation_id,
                task_id=f"ksdft-si-s1-gamma-kpoint-k{mesh}-attempt-1",
                output_artifact_id=f"run/K{mesh}/pw.out",
                prepared_input=prepared,
                pseudopotentials=request.specification.simulation.pseudopotentials,
                pseudopotential_library=library,
                executable=pre.EXECUTABLE,
                working_directory=working_directory,
                timeout_seconds=pre.TIMEOUT_SECONDS,
                execution_authorized=True,
            )
        )

    handler = QePwDftScfActionHandler(integration=integration, tasks=tuple(tasks))
    observations: list[PwDftScfEnergyObservation] = []
    occurrence_results: list[dict[str, object]] = []
    write_json(
        pre.ROOT / "campaign-progress.json",
        {"status": "authorized-not-started", "completed_occurrences": []},
    )
    for mesh, coordinate, request, task in zip(
        pre.MESHES,
        recipe.coordinates(),
        requests,
        tasks,
        strict=True,
    ):
        write_json(
            pre.ROOT / "campaign-progress.json",
            {
                "status": "running",
                "active_coordinate": f"K{mesh}",
                "completed_occurrences": occurrence_results,
            },
        )
        workflow = LocalPwDftScfWorkflow(
            evaluation_id=request.evaluation_id,
            runtime=loaded.campaign.runtime,
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
            failure = {
                "status": "failed",
                "failed_coordinate": f"K{mesh}",
                "failure": asdict(outcome),
                "completed_occurrences": occurrence_results,
                "retries_performed": 0,
            }
            write_json(pre.ROOT / "campaign-result.json", failure)
            write_json(
                pre.ROOT / "campaign-progress.json",
                {
                    "status": "stopped-on-first-failure",
                    "failed_coordinate": f"K{mesh}",
                    "completed_occurrences": occurrence_results,
                },
            )
            raise RuntimeError(  # noqa: TRY004
                f"K{mesh} workflow failed: {outcome.code}"
            )
        if not isinstance(outcome, PwDftScfWorkflowSucceeded):
            raise TypeError("SCF workflow returned an unknown outcome")
        observation = outcome.result.observation
        retained_bytes = tree_size(task.working_directory)
        if retained_bytes > pre.MAXIMUM_BYTES_PER_OCCURRENCE:
            raise RuntimeError(f"K{mesh} exceeded retained-byte bound")
        observations.append(
            PwDftScfEnergyObservation(
                coordinate=coordinate,
                total_energy_ev_per_atom=observation.total_energy_ev_per_atom,
            )
        )
        occurrence_results.append(
            {
                "mesh_density": mesh,
                "status": "succeeded",
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
                "observed_wavefunction_cutoff_ev": (observation.wavefunction_cutoff_ev),
                "diagnostics": [
                    {
                        "code": item.code,
                        "severity": item.severity.value,
                        "message": item.message,
                    }
                    for item in observation.diagnostics
                ],
                "retained_bytes": retained_bytes,
                "fired_transitions": fired,
                "pw_input_sha256": pre.sha256(task.working_directory / "pw.in"),
                "pw_output_sha256": pre.sha256(task.working_directory / "pw.out"),
                "execution_record_sha256": pre.sha256(
                    task.working_directory / "execution.json"
                ),
            }
        )

    reference = observations[-1].total_energy_ev_per_atom
    deltas = {
        str(item.coordinate.mesh_density): abs(
            item.total_energy_ev_per_atom - reference
        )
        * 1000.0
        for item in observations
    }
    selected = next(
        item.coordinate.mesh_density
        for item in observations
        if deltas[str(item.coordinate.mesh_density)] <= 1.0
    )
    assessment = EnergyAxisConvergenceAssessor().assess(
        EnergyAxisConvergenceAssessmentRequest(
            axis=PwDftScfConvergenceAxis.kpoint,
            observations=tuple(observations),
            policy=recipe.policy,
        )
    )
    result = {
        "status": "succeeded",
        "invocation_count": 4,
        "retries_performed": 0,
        "occurrences": occurrence_results,
        "projectkoios_policy_assessment": asdict(assessment),
        "calculation_owned_selection": {
            "reference_mesh_density": 12,
            "absolute_energy_differences_mev_per_atom": deltas,
            "tolerance_mev_per_atom": 1.0,
            "selected_mesh_density": selected,
        },
        "scientific_disposition": (
            "sampled S1 k-point confirmation evidence only; cutoff confirmation "
            "and stable-pair disposition remain separate"
        ),
    }
    write_json(pre.ROOT / "campaign-result.json", result)
    write_json(
        pre.ROOT / "campaign-progress.json",
        {"status": "completed", "completed_occurrences": occurrence_results},
    )


if __name__ == "__main__":
    main()
