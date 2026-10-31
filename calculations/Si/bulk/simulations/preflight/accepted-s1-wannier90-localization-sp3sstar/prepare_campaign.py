from __future__ import annotations

import hashlib
import importlib
import json
import shutil
from pathlib import Path

from projectkoios.physkit import units as _physkit_units
from projectkoios.physkit.units import PhysicalUnit

if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER

_artifacts = importlib.import_module("projectkoios.integrations.wannier90.artifacts")
_interface = importlib.import_module(
    "projectkoios.integrations.wannier90.interface_data"
)
_nnkp = importlib.import_module("projectkoios.integrations.wannier90.nnkp")
Wannier90NativeArtifact = _artifacts.Wannier90NativeArtifact
Wannier90NativeArtifactCorrelator = _artifacts.Wannier90NativeArtifactCorrelator
Wannier90EigenvalueParser = _interface.Wannier90EigenvalueParser
Wannier90NeighborOverlapParser = _interface.Wannier90NeighborOverlapParser
Wannier90ProjectionParser = _interface.Wannier90ProjectionParser
Wannier90NnkpParser = _nnkp.Wannier90NnkpParser

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-sp3sstar-20261031T075500Z"
)
PREPROCESSING = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-sp3sstar-20261031T073157Z"
)
CONVERTER = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-pw2wannier90-sp3sstar-20261031T074802Z"
)
DECISION = Path(
    "/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint/"
    "calculations/Si/bulk/simulations/wannier-interface-decision.md"
)
EXECUTABLE = Path("/Users/eugene/projects/wannier90-3.1.0/wannier90.x")
PROJECTKOIOS = Path(
    "/Users/eugene/worktrees/projectkoios-simulations-pw-dft-wannierization-tranche-1"
)
PROJECTKOIOS_REVISION = "e146f3722e87ca2de2243421a94448cfa6e27037"
STAGED = ROOT / "prepared-input"
EXPECTED_EXECUTABLE_SHA256 = (
    "c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd"
)
EXPECTED_INPUTS = {
    "silicon.amn": "1fbc2b98f9c7222c726d694afc2582b6e8fb28f6f9b4668357d80b322c938efc",
    "silicon.mmn": "1b4ebf8e6cff7c3c5491513707d969ddc988ed21a2dd2788bfdd6003de138e6f",
    "silicon.eig": "e2a86cbab7f14a607987fe5d965449541703ebece16db8500b2b1cb74ecb743a",
    "silicon.nnkp": "4dd17877e0f3bc0b19a0f74ce539a91bd8ceb1c66a18d3f733f08e5d8ce07014",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observation(path: Path) -> dict[str, object]:
    return {"path": str(path), "byte_size": path.stat().st_size, "sha256": sha256(path)}


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if ROOT.exists():
        raise RuntimeError("localization preflight root already exists")
    if sha256(EXECUTABLE) != EXPECTED_EXECUTABLE_SHA256:
        raise RuntimeError("wannier90.x identity mismatch")
    source_win = PREPROCESSING / "input/silicon.win"
    source_text = source_win.read_text(encoding="utf-8")
    marker = "write_hr = .true.\n"
    if source_text.count(marker) != 1 or "write_u_matrices" in source_text:
        raise RuntimeError("unexpected source WIN output-control inventory")
    localization_text = source_text.replace(
        marker, marker + "write_u_matrices = .true.\n"
    )
    ROOT.mkdir(parents=True)
    STAGED.mkdir()
    (STAGED / "silicon.win").write_text(localization_text, encoding="utf-8")
    sources = {
        "silicon.amn": CONVERTER / "run/silicon.amn",
        "silicon.mmn": CONVERTER / "run/silicon.mmn",
        "silicon.eig": CONVERTER / "run/silicon.eig",
        "silicon.nnkp": PREPROCESSING / "run/silicon.nnkp",
    }
    for name, source in sources.items():
        if sha256(source) != EXPECTED_INPUTS[name]:
            raise RuntimeError(f"{name} identity mismatch")
        shutil.copyfile(source, STAGED / name)
    artifacts = tuple(
        Wannier90NativeArtifact(name, (STAGED / name).read_bytes())
        for name in EXPECTED_INPUTS
    )
    expected = tuple(artifact.identity for artifact in artifacts)
    Wannier90NativeArtifactCorrelator().execute(expected, artifacts)
    nnkp = Wannier90NnkpParser().execute((STAGED / "silicon.nnkp").read_bytes())
    amn = Wannier90ProjectionParser().execute((STAGED / "silicon.amn").read_bytes())
    mmn = Wannier90NeighborOverlapParser().execute(
        (STAGED / "silicon.mmn").read_bytes()
    )
    eig = Wannier90EigenvalueParser().execute(
        (STAGED / "silicon.eig").read_bytes(), PhysicalUnit("eV")
    )
    if (amn.kpoint_count, amn.band_count, amn.projection_count) != (64, 12, 10):
        raise RuntimeError("AMN dimensions disagree")
    if (mmn.kpoint_count, mmn.band_count, mmn.neighbor_count) != (64, 12, 8):
        raise RuntimeError("MMN dimensions disagree")
    if (eig.kpoint_count, eig.band_count) != (64, 12):
        raise RuntimeError("EIG dimensions disagree")
    neighbors = tuple(
        (
            value.source_kpoint_index,
            value.target_kpoint_index,
            *value.reciprocal_cell_shift,
        )
        for value in nnkp.neighbors
    )
    if mmn.normalized_records != neighbors:
        raise RuntimeError("MMN and NNKP neighbor inventories disagree")
    manifest_entries = [
        {"role": "construction-input", **observation(STAGED / "silicon.win")},
        {"role": "preprocessing-topology", **observation(STAGED / "silicon.nnkp")},
        {"role": "interface-eigenvalues", **observation(STAGED / "silicon.eig")},
        {"role": "interface-projections", **observation(STAGED / "silicon.amn")},
        {"role": "interface-neighbor-overlaps", **observation(STAGED / "silicon.mmn")},
    ]
    manifest = {
        "schema_version": 1,
        "seedname": "silicon",
        "route_kind": "ordinary-amn-mmn-non-spin",
        "closed_input_inventory": manifest_entries,
        "file_count": len(manifest_entries),
        "total_bytes": sum(int(item["byte_size"]) for item in manifest_entries),
        "unk_staged": False,
        "spn_staged": False,
    }
    manifest_path = ROOT / "prepared-input-manifest.json"
    write_json(manifest_path, manifest)
    transformation = {
        "schema_version": 1,
        "source": observation(source_win),
        "prepared": observation(STAGED / "silicon.win"),
        "only_change": "insert write_u_matrices = .true. after write_hr = .true.",
        "reason": (
            "retain both square gauge and rectangular disentanglement matrices "
            "required by the declared 12-band to rank-10 construction"
        ),
        "changes_structure_mesh_projections_windows_or_convergence_controls": False,
        "requires_preprocessing_retry": False,
    }
    transformation_path = ROOT / "win-transformation.json"
    write_json(transformation_path, transformation)
    projectkoios_localization_doc = (
        PROJECTKOIOS / "../projectkoios-simulations-pw-dft-wannierization-architecture/"
        "docs/architecture/projectkoios/integrations/wannier90/localization/index.md"
    ).resolve()
    preflight = {
        "schema_version": 1,
        "purpose": "first rank-10 Wannier90 localization and Hamiltonian occurrence",
        "status": "blocked-missing-reviewed-projectkoios-localization-runner",
        "execution_performed": False,
        "projectkoios_revision": PROJECTKOIOS_REVISION,
        "projectkoios_capability": {
            "available": (
                "authenticated bounded input/output parsers and generic "
                "single-attempt execution substrate"
            ),
            "missing": (
                "reviewed production Wannier90 localization preparation and "
                "execution provider"
            ),
            "architecture": str(projectkoios_localization_doc),
            "execution_must_not_be_claimed_through_ad_hoc_substitution": True,
        },
        "candidate": {
            "seedname": "silicon",
            "route_kind": "ordinary-amn-mmn-non-spin",
            "band_count": 12,
            "wannier_count": 10,
            "kpoint_count": 64,
            "neighbor_count_per_kpoint": 8,
            "localization_maximum_iterations": 100,
            "localization_tolerance_angstrom_squared": 1e-10,
            "localization_convergence_window": 3,
            "disentanglement_maximum_iterations": 200,
            "disentanglement_tolerance_angstrom_squared": 1e-10,
            "disentanglement_convergence_window": 3,
            "disentanglement_mix_ratio": 0.5,
            "outer_window_ev": [-5.85, 19.02],
            "frozen_window": None,
            "write_hr": True,
            "write_u_matrices": True,
        },
        "prepared_input_manifest": observation(manifest_path),
        "win_transformation": observation(transformation_path),
        "parent_preprocessing": {
            "result": observation(PREPROCESSING / "preprocessing-result.json"),
            "nnkp": observation(PREPROCESSING / "run/silicon.nnkp"),
        },
        "parent_conversion": {
            "campaign_result": observation(CONVERTER / "campaign-result.json"),
            "converter_result": observation(CONVERTER / "converter-result.json"),
            "artifact_manifest": observation(CONVERTER / "run/artifact-manifest.json"),
        },
        "decision": observation(DECISION),
        "executable": observation(EXECUTABLE),
        "prospective_command": [str(EXECUTABLE), "silicon"],
        "prospective_resource_bounds": {
            "processes": 1,
            "timeout_seconds": 300.0,
            "maximum_retained_bytes": 67108864,
            "retries": 0,
            "stop_on_failure": True,
        },
        "required_outputs": [
            "silicon.wout",
            "silicon_hr.dat",
            "silicon_u.mat",
            "silicon_u_dis.mat",
        ],
        "mechanical_eligibility_checks": {
            "required_return_code": 0,
            "disentanglement_convergence_phrase_required": True,
            "wannierisation_convergence_phrase_required": True,
            "maximum_iteration_warning_forbidden": True,
            "wout_bounded_parse_and_finite_rank_10_final_state": True,
            "u_mat_shape": [64, 10, 10],
            "u_dis_mat_shape": [64, 12, 10],
            "hr_rank": 10,
            "ordered_kpoint_correlation_required": True,
            "unitary_isometry_tolerance": 1e-8,
            "kpoint_fractional_tolerance": 1e-10,
            "hamiltonian_hermiticity_tolerance_ev": 1e-8,
        },
        "authorization_state": (
            "not requested while the reviewed ProjectKoios localization runner "
            "is absent"
        ),
        "scientific_disposition": (
            "prepared-input evidence only; no localization, interpolation, "
            "component-operator, or Slater-Koster result"
        ),
    }
    write_json(ROOT / "campaign-preflight.json", preflight)


if __name__ == "__main__":
    main()
