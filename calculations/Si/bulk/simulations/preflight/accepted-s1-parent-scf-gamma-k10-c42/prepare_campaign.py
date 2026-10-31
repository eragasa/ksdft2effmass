from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

from projectkoios.integrations.quantumespresso.pw.scf.integration import (
    QePwDftScfIntegration,
)
from projectkoios.physkit.periodic.unit_cell import UnitCellJsonCodec
from projectkoios.physkit.units import MODEL_SYSTEM_UNIT_CONVERTER, PhysicalUnit
from projectkoios.simulations.dft.pseudopotential.library import PseudopotentialLibrary
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
from projectkoios.simulations.workflows.pw_dft_scf.recipe import (
    PwDftScfKpointConvergenceRecipe,
    PwDftScfSingleCalculationRecipe,
)
from tools.pw_dft_scf.environment import WorkflowRunnerEnvironment

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-parent-scf-gamma-k10-c42-20261031T070321Z"
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
KSD_ROOT = Path("/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint")
SIMULATIONS_ROOT = KSD_ROOT / "calculations/Si/bulk/simulations"
STRUCTURE_PATH = SIMULATIONS_ROOT / (
    "structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
)
ACCEPTED_PAIR_PATH = SIMULATIONS_ROOT / "accepted-stable-pair.json"
RELAXATION_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-bulk-vc-relax-ibrav2-gamma-k10-c42-20261031T061128Z"
)
MESH_DENSITY = 10
WAVEFUNCTION_CUTOFF_RY = 42.0
TIMEOUT_SECONDS = 600.0
MAXIMUM_BYTES = 2 * 1024**3
STRUCTURE_ID = "Si.PrimitiveUnitCell.RightHanded.RelaxedS1"
STRUCTURE_BYTES = 758
STRUCTURE_SHA256 = "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03"
ACCEPTED_PAIR_SHA256 = (
    "953ba609c2c8a4be4c6049fa882592b050b16ffcf9080098bd8bfa4b829fc84b"
)
EXECUTABLE_SHA256 = "87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observed(path: Path) -> dict[str, object]:
    return {"path": str(path), "byte_size": path.stat().st_size, "sha256": sha256(path)}


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if any(path.name != "prepare_campaign.py" for path in ROOT.iterdir()):
        raise RuntimeError("preflight root must contain only prepare_campaign.py")
    if sha256(ACCEPTED_PAIR_PATH) != ACCEPTED_PAIR_SHA256:
        raise RuntimeError("accepted stable-pair identity mismatch")
    accepted = json.loads(ACCEPTED_PAIR_PATH.read_text())
    if accepted["status"] != "accepted":
        raise RuntimeError("stable pair is not accepted")
    if not EXECUTABLE.is_file() or EXECUTABLE.is_symlink():
        raise RuntimeError("QE executable is unavailable or symbolic")
    if sha256(EXECUTABLE) != EXECUTABLE_SHA256:
        raise RuntimeError("QE executable SHA-256 mismatch")
    structure_content = STRUCTURE_PATH.read_bytes()
    if (
        len(structure_content) != STRUCTURE_BYTES
        or sha256(STRUCTURE_PATH) != STRUCTURE_SHA256
    ):
        raise RuntimeError("accepted S1 identity mismatch")
    unit_cell = UnitCellJsonCodec().loads(
        structure_content.decode("utf-8"), expected_structure_id=STRUCTURE_ID
    )
    relaxation_calculation = RELAXATION_ROOT / "calculation.toml"
    relaxation_evidence = RELAXATION_ROOT / "result/relaxation-result.json"
    structure_record = StructureRecord(
        structure_id=STRUCTURE_ID,
        representation=StructureRepresentation.primitive,
        schema_version=1,
        sha256=STRUCTURE_SHA256,
        byte_size=STRUCTURE_BYTES,
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
                sha256=sha256(relaxation_calculation),
            ),
            relaxation_evidence=StructureProvenanceReference(
                stable_id="si-bulk-vc-relax-ibrav2-gamma-k10-c42-result",
                representation="ksdft2effmass-relaxation-result-json",
                schema_version=1,
                byte_size=relaxation_evidence.stat().st_size,
                sha256=sha256(relaxation_evidence),
            ),
            scope=ObservedStructureScope.atomic_positions_and_cell,
            publication_operation="ksdft2effmass.qe-vc-relax.publish-source-basis",
            publication_version="1",
            result_sha256=STRUCTURE_SHA256,
        ),
    )
    structure = StructureResolution(
        record=structure_record, path=STRUCTURE_PATH, unit_cell=unit_cell
    )
    environment = WorkflowRunnerEnvironment.load(RUNNER_CONFIG)
    loaded = environment.loader.load(SOURCE_CAMPAIGN)
    source_recipe = loaded.campaign.recipe
    if not isinstance(source_recipe, PwDftScfKpointConvergenceRecipe):
        raise TypeError("source campaign is not k-point convergence")
    cutoff_ev = WAVEFUNCTION_CUTOFF_RY * MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
        PhysicalUnit("rydberg"), PhysicalUnit("eV")
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
            mesh=(MESH_DENSITY, MESH_DENSITY, MESH_DENSITY),
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
        mesh_density=MESH_DENSITY, wavefunction_cutoff_ev=cutoff_ev
    )
    request = recipe.request_for(coordinate, scope="preflight")
    projection_configuration = environment.loader.qe_projection_configuration(
        loaded.projection_profile_id
    )
    integration = QePwDftScfIntegration(
        artifact_root=ROOT, projection_configuration=projection_configuration
    )
    prepared = integration.project(request, structure)
    library = PseudopotentialLibrary(root=PSEUDOPOTENTIAL_ROOT)
    pseudopotential = specification.simulation.pseudopotentials[0]
    library.resolve(pseudopotential)
    preflight_root = ROOT / "preflight"
    preflight_root.mkdir(mode=0o700)
    artifact = prepared.artifacts[0]
    (preflight_root / "pw.in").write_bytes(artifact.content)
    manifest = {
        "schema_version": 1,
        "status": "awaiting-explicit-bounded-authorization",
        "execution_performed": False,
        "authorization_request": {
            "maximum_invocations": 1,
            "retries": 0,
            "stop_on_failure": True,
        },
        "purpose": "new accepted-pair parent SCF and saved-state source for downstream NSCF",
        "scientific_disposition": "preflight only; no parent SCF has run",
        "projectkoios_revision": "e146f3722e87ca2de2243421a94448cfa6e27037",
        "preparation_script": observed(ROOT / "prepare_campaign.py"),
        "accepted_pair": observed(ACCEPTED_PAIR_PATH),
        "structure": {
            "structure_id": STRUCTURE_ID,
            "path": str(STRUCTURE_PATH),
            "byte_size": STRUCTURE_BYTES,
            "sha256": STRUCTURE_SHA256,
        },
        "executable": observed(EXECUTABLE),
        "pseudopotential": {
            "collection": "SSSP 1.3.0 PBE efficiency",
            "root": str(PSEUDOPOTENTIAL_ROOT),
            "filename": pseudopotential.filename,
            "byte_size": pseudopotential.byte_size,
            "sha256": pseudopotential.sha256,
        },
        "settings": {
            "mesh": [10, 10, 10],
            "mesh_shift": [0, 0, 0],
            "wavefunction_cutoff_ry": 42.0,
            "charge_density_cutoff_ry": 336.0,
            "electronic_tolerance_ry": projection_configuration.electronic_tolerance_ry,
            "maximum_electronic_iterations": specification.electronic_convergence.maximum_electronic_iterations,
            "occupation": specification.occupation.method.value,
            "spatial_symmetry": specification.kpoint_sampling.use_spatial_symmetry,
            "time_reversal": specification.kpoint_sampling.use_time_reversal,
        },
        "occurrence": {
            "evaluation_id": request.evaluation_id,
            "prepared_input_sha256": prepared.sha256,
            "pw_input": observed(preflight_root / "pw.in"),
            "occurrence_role": "accepted-pair-parent-scf",
            "saved_state_role": "source for a separately authorized downstream NSCF",
        },
        "resource_bounds": {
            "processes": 1,
            "timeout_seconds": TIMEOUT_SECONDS,
            "maximum_retained_bytes": MAXIMUM_BYTES,
        },
        "nonreuse_boundary": (
            "The native pw.in may equal the K10/C42 confirmation input, but this must be a new occurrence with a new execution record and saved-state lineage."
        ),
    }
    write_json(ROOT / "campaign-preflight.json", manifest)


if __name__ == "__main__":
    main()
