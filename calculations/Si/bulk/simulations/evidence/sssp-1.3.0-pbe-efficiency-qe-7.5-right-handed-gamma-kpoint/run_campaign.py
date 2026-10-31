from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

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
from projectkoios.simulations.structure import (
    DerivedStructureProvenance,
    StructureRecord,
    StructureRecordReference,
    StructureResolution,
)
from projectkoios.simulations.workflows.pw_dft_scf.recipe import (
    PwDftScfKpointConvergenceRecipe,
)
from tools.pw_dft_scf.environment import WorkflowRunnerEnvironment

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-kpoint-gamma-sssp-qe75-right-handed-20261031T054832Z"
)
PROJECTKOIOS_ROOT = Path(
    "/Users/eugene/worktrees/projectkoios-simulations-pw-dft-wannierization-tranche-1"
)
RUNNER_CONFIG = PROJECTKOIOS_ROOT / "tools/pw_dft_scf/config/runner.toml"
SOURCE_CAMPAIGN = (
    PROJECTKOIOS_ROOT / "examples/workflows/pw_dft_scf/campaigns/qe-kpoint.toml"
)
EXECUTABLE = Path("/Users/eugene/projects/q-e-qe-7.5/build/bin/pw.x")
PSEUDOPOTENTIAL_ROOT = Path(
    "/Users/eugene/opt/pseudopotentials/quantum-espresso/sssp/1.3.0/sets/PBE/efficiency"
)
STRUCTURE_PATH = Path(
    "/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint/"
    "calculations/Si/bulk/simulations/structures/"
    "Si.PrimitiveUnitCell.RightHanded.json"
)
MESHES = (6, 8, 10, 12)
TIMEOUT_SECONDS = 600.0
MAXIMUM_BYTES_PER_OCCURRENCE = 2 * 1024**3


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_size(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if not EXECUTABLE.is_file() or EXECUTABLE.is_symlink():
        raise RuntimeError("QE executable is unavailable or symbolic")
    if sha256(EXECUTABLE) != (
        "87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910"
    ):
        raise RuntimeError("QE executable SHA-256 mismatch")

    environment = WorkflowRunnerEnvironment.load(RUNNER_CONFIG)
    loaded = environment.loader.load(SOURCE_CAMPAIGN)
    source_recipe = loaded.campaign.recipe
    if not isinstance(source_recipe, PwDftScfKpointConvergenceRecipe):
        raise RuntimeError("source campaign is not k-point convergence")

    structure_content = STRUCTURE_PATH.read_bytes()
    structure_sha256 = hashlib.sha256(structure_content).hexdigest()
    if len(structure_content) != 692 or structure_sha256 != (
        "7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a"
    ):
        raise RuntimeError("right-handed structure identity mismatch")
    unit_cell = UnitCellJsonCodec().loads(
        structure_content.decode("utf-8"),
        expected_structure_id="Si.PrimitiveUnitCell.RightHanded",
    )
    parent = loaded.structure.record
    parent_reference = StructureRecordReference(
        structure_id=parent.structure_id,
        representation=parent.representation,
        schema_version=parent.schema_version,
        byte_size=parent.byte_size,
        sha256=parent.sha256,
    )
    parameters_json = json.dumps(
        {
            "direct_basis_transform": [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
            "fractional_coordinate_transform": "transpose",
        },
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ) + "\n"
    structure_record = StructureRecord(
        structure_id="Si.PrimitiveUnitCell.RightHanded",
        representation=parent.representation,
        schema_version=1,
        sha256=structure_sha256,
        byte_size=len(structure_content),
        provenance=DerivedStructureProvenance(
            operation_id="ksdft2effmass.structure.swap-first-two-basis-vectors",
            operation_version="1",
            parents=(parent_reference,),
            parameters_json=parameters_json,
            parameters_sha256=hashlib.sha256(parameters_json.encode()).hexdigest(),
            result_sha256=structure_sha256,
        ),
    )
    structure = StructureResolution(
        record=structure_record,
        path=STRUCTURE_PATH,
        unit_cell=unit_cell,
    )

    cutoff_ev = 48.0 * MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
        PhysicalUnit("rydberg"),
        PhysicalUnit("eV"),
    )
    source_specification = source_recipe.base_request.specification
    specification = replace(
        source_specification,
        simulation_id=(
            "Si.PrimitiveUnitCell.RightHanded.QE.SCF."
            "GammaKpointConvergence.SSSP130.PBE.K48Ry"
        ),
        simulation=replace(
            source_specification.simulation,
            structure=structure_record,
        ),
        wavefunction_cutoff_ev=cutoff_ev,
        kpoint_sampling=replace(
            source_specification.kpoint_sampling,
            mesh=(8, 8, 8),
            shift=(0, 0, 0),
        ),
    )
    base_request = replace(
        source_recipe.base_request,
        evaluation_id="ksdft-si-gamma-kpoint-sssp-qe75-base",
        specification=specification,
    )
    recipe = PwDftScfKpointConvergenceRecipe(
        campaign_id="ksdft-si-kpoint-sssp-qe75",
        base_request=base_request,
        mesh_densities=MESHES,
        policy=source_recipe.policy,
    )
    projection_configuration = environment.loader.qe_projection_configuration(
        loaded.projection_profile_id
    )
    integration = QePwDftScfIntegration(
        artifact_root=ROOT,
        projection_configuration=projection_configuration,
    )
    library = PseudopotentialLibrary(root=PSEUDOPOTENTIAL_ROOT)

    requests = tuple(
        recipe.request_for(coordinate, scope="authorized")
        for coordinate in recipe.coordinates()
    )
    prepared_inputs = tuple(
        integration.project(request, structure) for request in requests
    )
    tasks: list[QePwDftScfTask] = []
    for mesh, request, prepared_input in zip(
        MESHES,
        requests,
        prepared_inputs,
        strict=True,
    ):
        working_directory = ROOT / f"K{mesh}"
        working_directory.mkdir(mode=0o700)
        tasks.append(
            QePwDftScfTask(
                evaluation_id=request.evaluation_id,
                task_id=f"ksdft-si-gamma-kpoint-k{mesh}-attempt-1",
                output_artifact_id=f"K{mesh}/pw.out",
                prepared_input=prepared_input,
                pseudopotentials=request.specification.simulation.pseudopotentials,
                pseudopotential_library=library,
                executable=EXECUTABLE,
                working_directory=working_directory,
                timeout_seconds=TIMEOUT_SECONDS,
                execution_authorized=True,
            )
        )

    manifest = {
        "schema_version": 1,
        "status": "authorized-not-started",
        "authorization": {
            "operator_message": "go",
            "maximum_invocations": 4,
            "retries": 0,
        },
        "purpose": "right-handed Gamma-centered fixed-cutoff k-point convergence workflow",
        "scientific_disposition": (
            "development calculation; completion is not scientific acceptance"
        ),
        "projectkoios_revision": "e146f3722e87ca2de2243421a94448cfa6e27037",
        "source_structure": {
            "structure_id": structure_record.structure_id,
            "role": "right-handed provisional S0",
            "path": str(STRUCTURE_PATH),
            "byte_size": structure_record.byte_size,
            "sha256": structure_record.sha256,
            "parent_structure_id": parent.structure_id,
            "parent_sha256": parent.sha256,
            "direct_basis_transform": [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
        },
        "executable": {
            "path": str(EXECUTABLE),
            "byte_size": EXECUTABLE.stat().st_size,
            "sha256": sha256(EXECUTABLE),
        },
        "pseudopotential": {
            "collection": "SSSP 1.3.0 PBE efficiency",
            "root": str(PSEUDOPOTENTIAL_ROOT),
            "filename": specification.simulation.pseudopotentials[0].filename,
            "byte_size": specification.simulation.pseudopotentials[0].byte_size,
            "sha256": specification.simulation.pseudopotentials[0].sha256,
        },
        "settings": {
            "mesh_densities": list(MESHES),
            "mesh_shift": [0, 0, 0],
            "wavefunction_cutoff_ry": 48.0,
            "wavefunction_cutoff_ev": cutoff_ev,
            "charge_density_cutoff_ratio": (
                projection_configuration.charge_density_cutoff_ratio
            ),
            "charge_density_cutoff_ry": 384.0,
            "electronic_tolerance_ry": (
                projection_configuration.electronic_tolerance_ry
            ),
            "maximum_electronic_iterations": (
                specification.electronic_convergence.maximum_electronic_iterations
            ),
            "occupation": specification.occupation.method.value,
            "spatial_symmetry": specification.kpoint_sampling.use_spatial_symmetry,
            "time_reversal": specification.kpoint_sampling.use_time_reversal,
        },
        "occurrences": [
            {
                "mesh_density": mesh,
                "evaluation_id": request.evaluation_id,
                "task_id": task.task_id,
                "working_directory": str(task.working_directory),
                "prepared_input_sha256": prepared.sha256,
                "pw_input_sha256": prepared.artifacts[0].sha256,
            }
            for mesh, request, task, prepared in zip(
                MESHES,
                requests,
                tasks,
                prepared_inputs,
                strict=True,
            )
        ],
        "resource_bounds": {
            "processes_per_occurrence": 1,
            "timeout_seconds_per_occurrence": TIMEOUT_SECONDS,
            "maximum_bytes_per_occurrence": MAXIMUM_BYTES_PER_OCCURRENCE,
        },
    }
    write_json(ROOT / "campaign-manifest.json", manifest)

    handler = QePwDftScfActionHandler(
        integration=integration,
        tasks=tuple(tasks),
    )
    observations: list[PwDftScfEnergyObservation] = []
    occurrence_results: list[dict[str, object]] = []
    for mesh, coordinate, request, task in zip(
        MESHES,
        recipe.coordinates(),
        requests,
        tasks,
        strict=True,
    ):
        workflow = LocalPwDftScfWorkflow(
            evaluation_id=request.evaluation_id,
            runtime=loaded.campaign.runtime,
        )
        fired: list[str] = []
        while workflow.outcome() is None:
            actions = workflow.pending_actions()
            if len(actions) != 1:
                raise RuntimeError("SCF workflow requires exactly one pending action")
            for event in handler.handle(actions[0]):
                fired.extend(workflow.accept(event))
        outcome = workflow.outcome()
        if isinstance(outcome, PwDftScfWorkflowFailed):
            write_json(
                ROOT / "campaign-result.json",
                {
                    "status": "failed",
                    "failed_mesh_density": mesh,
                    "failure": asdict(outcome),
                    "completed_occurrences": occurrence_results,
                },
            )
            raise RuntimeError(f"K{mesh} workflow failed: {outcome.code}")
        if not isinstance(outcome, PwDftScfWorkflowSucceeded):
            raise RuntimeError("SCF workflow returned an unknown outcome")
        observation = outcome.result.observation
        occurrence_bytes = tree_size(task.working_directory)
        if occurrence_bytes > MAXIMUM_BYTES_PER_OCCURRENCE:
            raise RuntimeError(f"K{mesh} exceeded the retained-byte bound")
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
                "observed_wavefunction_cutoff_ev": (
                    observation.wavefunction_cutoff_ev
                ),
                "diagnostics": [
                    {
                        "code": item.code,
                        "severity": item.severity.value,
                        "message": item.message,
                    }
                    for item in observation.diagnostics
                ],
                "retained_bytes": occurrence_bytes,
                "fired_transitions": fired,
            }
        )
        write_json(
            ROOT / "campaign-progress.json",
            {
                "status": "running",
                "completed_occurrences": occurrence_results,
            },
        )

    assessment = EnergyAxisConvergenceAssessor().assess(
        EnergyAxisConvergenceAssessmentRequest(
            axis=PwDftScfConvergenceAxis.kpoint,
            observations=tuple(observations),
            policy=recipe.policy,
        )
    )
    write_json(
        ROOT / "campaign-result.json",
        {
            "status": "succeeded",
            "occurrences": occurrence_results,
            "energy_convergence_assessment": asdict(assessment),
            "scientific_disposition": (
                "software workflow result only; requires independent review before "
                "scientific acceptance"
            ),
        },
    )
    manifest["status"] = "completed"
    write_json(ROOT / "campaign-manifest.json", manifest)


if __name__ == "__main__":
    main()
