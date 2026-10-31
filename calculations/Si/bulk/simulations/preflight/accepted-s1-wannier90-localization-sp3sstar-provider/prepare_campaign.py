from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from projectkoios.integrations.wannier90 import Wannier90LocalizationInputPreparer

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-sp3sstar-20261031T081246Z"
)
SUPERSEDED_PREPARATION = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-sp3sstar-20261031T075500Z/"
    "prepared-input"
)
PREPROCESSING_RESULT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-sp3sstar-20261031T073157Z/"
    "preprocessing-result.json"
)
CONVERTER_RESULT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-pw2wannier90-sp3sstar-20261031T074802Z/"
    "converter-result.json"
)
DECISION = Path(
    "/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint/"
    "calculations/Si/bulk/simulations/wannier-interface-decision.md"
)
PROJECTKOIOS = Path(
    "/Users/eugene/worktrees/projectkoios-simulations-pw-dft-wannierization-tranche-1"
)
EXECUTABLE = Path("/Users/eugene/projects/wannier90-3.1.0/wannier90.x")
EXPECTED_EXECUTABLE_SHA256 = (
    "c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd"
)
BASE_REVISION = "e146f3722e87ca2de2243421a94448cfa6e27037"
PREPROCESSING_SHA256 = (
    "d68e18bc9ee1138ca2e392198ab15b80e43ebf3ce319fb5ff0d7b772172191ee"
)
CONVERTER_SHA256 = "3e68cd8fd3b9b5438772bc73fbcae9d835ffd819ca6155aa9989703a28def823"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observation(path: Path) -> dict[str, object]:
    return {"path": str(path), "byte_size": path.stat().st_size, "sha256": sha256(path)}


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if ROOT.exists():
        raise RuntimeError("localization provider preflight root already exists")
    if sha256(EXECUTABLE) != EXPECTED_EXECUTABLE_SHA256:
        raise RuntimeError("wannier90.x identity mismatch")
    if sha256(PREPROCESSING_RESULT) != PREPROCESSING_SHA256:
        raise RuntimeError("preprocessing result identity mismatch")
    if sha256(CONVERTER_RESULT) != CONVERTER_SHA256:
        raise RuntimeError("converter result identity mismatch")
    ROOT.mkdir(parents=True)
    source = ROOT / "source-input"
    source.mkdir()
    for name in (
        "silicon.win",
        "silicon.nnkp",
        "silicon.eig",
        "silicon.amn",
        "silicon.mmn",
    ):
        shutil.copyfile(SUPERSEDED_PREPARATION / name, source / name)
    preparation = Wannier90LocalizationInputPreparer().prepare(
        source_directory=source,
        output_directory=ROOT / "prepared-input",
        seedname="silicon",
        kpoint_count=64,
        band_count=12,
        wannier_count=10,
        neighbor_count=8,
        parent_preprocessing_sha256=PREPROCESSING_SHA256,
        parent_converter_sha256=CONVERTER_SHA256,
    )
    implementation = (
        PROJECTKOIOS
        / "src/python/projectkoios/integrations/wannier90/localization_execution.py"
    )
    public_api = (
        PROJECTKOIOS / "src/python/projectkoios/integrations/wannier90/__init__.py"
    )
    tests = (
        PROJECTKOIOS
        / "tests/projectkoios/integrations/wannier90/test__Wannier90LocalizationRunner.py"
    )
    preflight = {
        "schema_version": 1,
        "purpose": "first rank-10 Wannier90 localization and Hamiltonian occurrence",
        "status": "awaiting-explicit-bounded-authorization",
        "execution_performed": False,
        "projectkoios_provider": {
            "base_revision": BASE_REVISION,
            "implementation": observation(implementation),
            "public_api": observation(public_api),
            "software_verification": {
                "full_test_result": "692 passed, 7 skipped, 202 subtests passed",
                "focused_localization_tests": "5 passed",
                "ruff": "passed",
                "focused_mypy": "passed",
                "wheel_build": "passed",
                "full_mypy": (
                    "blocked by two pre-existing preprocessing.py errors caused by "
                    "the installed PhysKit export mismatch"
                ),
                "bounded_review_outcome": "NO_BLOCKING_FINDINGS",
            },
            "tests": observation(tests),
        },
        "prepared_input_manifest": observation(preparation.manifest_path),
        "prepared_input": {
            "directory": str(preparation.output_directory),
            "route_kind": "first-rank-reducing-amn-mmn-non-spin",
            "file_count": 5,
            "total_byte_count": preparation.manifest.total_byte_count,
            "kpoint_count": 64,
            "band_count": 12,
            "wannier_count": 10,
            "neighbor_count": 8,
            "unk_staged": False,
            "spn_staged": False,
        },
        "parent_preprocessing": observation(PREPROCESSING_RESULT),
        "parent_conversion": observation(CONVERTER_RESULT),
        "decision": observation(DECISION),
        "executable": {"version": "3.1.0", **observation(EXECUTABLE)},
        "planned_command": [str(EXECUTABLE), "silicon"],
        "resource_bounds": {
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
            "native_completion_phrase_required": True,
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
        "authorization_request": {
            "maximum_invocations": 1,
            "retries": 0,
            "stop_on_failure": True,
        },
        "scientific_disposition": (
            "preflight only; no localization, interpolation, component-operator, "
            "or Slater-Koster result"
        ),
    }
    write_json(ROOT / "campaign-preflight.json", preflight)


if __name__ == "__main__":
    main()
