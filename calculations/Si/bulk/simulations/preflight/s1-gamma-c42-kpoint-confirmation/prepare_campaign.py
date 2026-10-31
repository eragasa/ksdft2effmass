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
from projectkoios.simulations.workflows.pw_dft_scf.recipe import (
    PwDftScfKpointConvergenceRecipe,
)
from tools.pw_dft_scf.environment import WorkflowRunnerEnvironment

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-s1-kpoint-confirmation-c42-gamma-20261031T064459Z"
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
STRUCTURE_PATH = (
    KSD_ROOT / "calculations/Si/bulk/simulations/structures/"
    "Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
)
RELAXATION_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-bulk-vc-relax-ibrav2-gamma-k10-c42-20261031T061128Z"
)
MESHES = (6, 8, 10, 12)
WAVEFUNCTION_CUTOFF_RY = 42.0
TIMEOUT_SECONDS = 600.0
MAXIMUM_BYTES_PER_OCCURRENCE = 2 * 1024**3
STRUCTURE_ID = "Si.PrimitiveUnitCell.RightHanded.RelaxedS1"
STRUCTURE_BYTES = 758
STRUCTURE_SHA256 = "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03"
EXECUTABLE_SHA256 = "87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observed(path: Path) -> dict[str, object]:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if any(path.name != "prepare_campaign.py" for path in ROOT.iterdir()):
        raise RuntimeError("preflight root must contain only prepare_campaign.py")
    if not EXECUTABLE.is_file() or EXECUTABLE.is_symlink():
        raise RuntimeError("QE executable is unavailable or symbolic")
    if sha256(EXECUTABLE) != EXECUTABLE_SHA256:
        raise RuntimeError("QE executable SHA-256 mismatch")

    structure_content = STRUCTURE_PATH.read_bytes()
    if len(structure_content) != STRUCTURE_BYTES:
        raise RuntimeError("S1 byte-size mismatch")
    if hashlib.sha256(structure_content).hexdigest() != STRUCTURE_SHA256:
        raise RuntimeError("S1 SHA-256 mismatch")
    unit_cell = UnitCellJsonCodec().loads(
        structure_content.decode("utf-8"),
        expected_structure_id=STRUCTURE_ID,
    )

    relaxation_calculation = RELAXATION_ROOT / "calculation.toml"
    relaxation_evidence = RELAXATION_ROOT / "result/relaxation-result.json"
    if sha256(relaxation_calculation) != (
        "ce110125f22c12701444d8b9d9b4ce771501648f4c5b1bb5def1934fafd683cf"
    ):
        raise RuntimeError("relaxation calculation identity mismatch")
    if sha256(relaxation_evidence) != (
        "ed139c5c1cfdc0a9cba1e1fabd7db4a8d6ca4b4dde0db0149cd909ff9a1ae235"
    ):
        raise RuntimeError("relaxation evidence identity mismatch")

    s0_reference = StructureRecordReference(
        structure_id="Si.PrimitiveUnitCell.RightHanded",
        representation=StructureRepresentation.primitive,
        schema_version=1,
        byte_size=692,
        sha256="7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a",
    )
    structure_record = StructureRecord(
        structure_id=STRUCTURE_ID,
        representation=StructureRepresentation.primitive,
        schema_version=1,
        sha256=STRUCTURE_SHA256,
        byte_size=STRUCTURE_BYTES,
        provenance=ObservedStructureProvenance(
            starting_structure=s0_reference,
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
        record=structure_record,
        path=STRUCTURE_PATH,
        unit_cell=unit_cell,
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
        mesh_densities=MESHES,
        policy=source_recipe.policy,
    )
    projection_configuration = environment.loader.qe_projection_configuration(
        loaded.projection_profile_id
    )
    if projection_configuration.charge_density_cutoff_ratio != 8.0:
        raise RuntimeError("charge-density cutoff ratio changed")
    integration = QePwDftScfIntegration(
        artifact_root=ROOT,
        projection_configuration=projection_configuration,
    )
    library = PseudopotentialLibrary(root=PSEUDOPOTENTIAL_ROOT)
    requests = tuple(
        recipe.request_for(coordinate, scope="preflight")
        for coordinate in recipe.coordinates()
    )
    prepared_inputs = tuple(
        integration.project(request, structure) for request in requests
    )

    preflight_root = ROOT / "preflight"
    preflight_root.mkdir(mode=0o700)
    occurrences: list[dict[str, object]] = []
    for mesh, request, prepared in zip(MESHES, requests, prepared_inputs, strict=True):
        artifacts = prepared.artifacts
        if len(artifacts) != 1 or artifacts[0].filename != "pw.in":
            raise RuntimeError("expected exactly one pw.in artifact")
        artifact = artifacts[0]
        coordinate_root = preflight_root / f"K{mesh}"
        coordinate_root.mkdir(mode=0o700)
        (coordinate_root / artifact.filename).write_bytes(artifact.content)
        occurrences.append(
            {
                "mesh": [mesh, mesh, mesh],
                "shift": [0, 0, 0],
                "wavefunction_cutoff_ry": WAVEFUNCTION_CUTOFF_RY,
                "charge_density_cutoff_ry": 336.0,
                "evaluation_id": request.evaluation_id,
                "prepared_input_sha256": prepared.sha256,
                "pw_input": observed(coordinate_root / "pw.in"),
            }
        )

    pseudopotential = specification.simulation.pseudopotentials[0]
    library.resolve(pseudopotential)
    manifest = {
        "schema_version": 1,
        "status": "awaiting-explicit-bounded-authorization",
        "execution_performed": False,
        "authorization_request": {
            "maximum_invocations": 4,
            "retries": 0,
            "stop_on_first_failure": True,
            "coordinates_in_order": [f"K{mesh}" for mesh in MESHES],
        },
        "purpose": (
            "first stage of fresh setting confirmation on provisional S1; "
            "fixed-C42 Gamma-centered k-point axis"
        ),
        "scientific_disposition": (
            "preflight only; no setting or stable structure/settings pair is accepted"
        ),
        "projectkoios_revision": "e146f3722e87ca2de2243421a94448cfa6e27037",
        "preparation_script": observed(ROOT / "prepare_campaign.py"),
        "structure": {
            "structure_id": STRUCTURE_ID,
            "role": "provisional S1",
            "path": str(STRUCTURE_PATH),
            "byte_size": STRUCTURE_BYTES,
            "sha256": STRUCTURE_SHA256,
            "relaxation_calculation": observed(relaxation_calculation),
            "relaxation_evidence": observed(relaxation_evidence),
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
            "mesh_densities": list(MESHES),
            "mesh_shift": [0, 0, 0],
            "wavefunction_cutoff_ry": WAVEFUNCTION_CUTOFF_RY,
            "charge_density_cutoff_ry": 336.0,
            "electronic_tolerance_ry": (
                projection_configuration.electronic_tolerance_ry
            ),
            "maximum_electronic_iterations": (
                specification.electronic_convergence.maximum_electronic_iterations
            ),
            "occupation": specification.occupation.method.value,
            "spatial_symmetry": specification.kpoint_sampling.use_spatial_symmetry,
            "time_reversal": specification.kpoint_sampling.use_time_reversal,
            "calculation_owned_selection_rule": (
                "select the smallest sampled mesh whose absolute total-energy "
                "difference from K12 is <= 1.0 meV/atom"
            ),
        },
        "occurrences": occurrences,
        "resource_bounds": {
            "processes_per_occurrence": 1,
            "timeout_seconds_per_occurrence": TIMEOUT_SECONDS,
            "maximum_bytes_per_occurrence": MAXIMUM_BYTES_PER_OCCURRENCE,
        },
        "continuation_rule": (
            "If K10 remains selected, separately preflight the cutoff axis at K10. "
            "If the selected mesh changes, stop and declare the successor cutoff/"
            "relaxation branch before further calculator execution."
        ),
    }
    write_json(ROOT / "campaign-preflight.json", manifest)


if __name__ == "__main__":
    main()
