from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path

from ksdft2effmass.integration.quantum_espresso.qexsd import (
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)
from projectkoios.integrations.quantumespresso.saved_state import (
    QeSavedStateManifestJsonCodec,
    QeSavedStateManifestVerifier,
)
from projectkoios.physkit import units as _physkit_units
from projectkoios.physkit.numeric import as_f64_array
from projectkoios.physkit.periodic.unit_cell import UnitCellJsonCodec
from projectkoios.physkit.units import (
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)
from projectkoios.simulations.calculator_input import CalculatorInputSourceReference

# The retained ProjectKoios tranche imports the converter's former class name, while
# the installed PhysKit surface exports the operational singleton. Bind that public
# singleton under the expected runtime name without changing either dependency.
if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER

Wannier90PreprocessingInput = importlib.import_module(
    "projectkoios.integrations.wannier90"
).Wannier90PreprocessingInput

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-sp3sstar-20261031T073157Z"
)
KSD_ROOT = Path("/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint")
SIMULATIONS_ROOT = KSD_ROOT / "calculations/Si/bulk/simulations"
STRUCTURE = SIMULATIONS_ROOT / (
    "structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
)
DECISION = SIMULATIONS_ROOT / "wannier-interface-decision.md"
NSCF_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier-nscf-4x4x4-b12-david-20261031T072258Z"
)
NSCF_RUN = NSCF_ROOT / "run"
NSCF_INPUT = NSCF_RUN / "pw.in"
NSCF_QEXSD = NSCF_RUN / "tmp/system.save/data-file-schema.xml"
NSCF_MANIFEST = NSCF_RUN / "nscf-saved-state-manifest.json"
EXECUTABLE = Path("/Users/eugene/projects/wannier90-3.1.0/wannier90.x")
STRUCTURE_ID = "Si.PrimitiveUnitCell.RightHanded.RelaxedS1"
STRUCTURE_SHA256 = "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03"
DECISION_SHA256 = "00ba0cb19789ff7349bf3b37784c4222eba758f90dd5be9d28c368763a892015"
NSCF_MANIFEST_SHA256 = (
    "cab588c939b3b9bdea95496458be414f465f38fb036d1ade62405f8d602bf4ce"
)
EXECUTABLE_SHA256 = "c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd"
SEEDNAME = "silicon"
OUTER_WINDOW_EV = (-5.85, 19.02)
TIMEOUT_SECONDS = 120.0
MAXIMUM_BYTES = 16 * 1024**2
_ANGSTROM_SQUARED = PhysicalUnit("angstrom ** 2")
_ELECTRON_VOLT = PhysicalUnit("eV")


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


def approved_kpoints() -> tuple[tuple[float, float, float], ...]:
    return tuple(
        (float(i) / 4.0, float(j) / 4.0, float(k) / 4.0)
        for i in range(4)
        for j in range(4)
        for k in range(4)
    )


def input_kpoints(path: Path) -> tuple[tuple[float, float, float], ...]:
    lines = path.read_text(encoding="ascii").splitlines()
    marker = lines.index("K_POINTS crystal")
    count = int(lines[marker + 1])
    rows = tuple(
        tuple(float(value) for value in line.split()[:3])
        for line in lines[marker + 2 : marker + 2 + count]
    )
    if any(len(row) != 3 for row in rows):
        raise RuntimeError("malformed NSCF k-point row")
    return rows


def main() -> None:
    allowed_existing = {
        "prepare_campaign.py",
        "preparation-attempts.json",
        "superseded-compact-projection-preflight",
    }
    if any(path.name not in allowed_existing for path in ROOT.iterdir()):
        raise RuntimeError("preflight root contains an undeclared path")
    for path, expected, label in (
        (STRUCTURE, STRUCTURE_SHA256, "structure"),
        (DECISION, DECISION_SHA256, "interface decision"),
        (NSCF_MANIFEST, NSCF_MANIFEST_SHA256, "NSCF manifest"),
        (EXECUTABLE, EXECUTABLE_SHA256, "Wannier90 executable"),
    ):
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"{label} identity mismatch")
    manifest = QeSavedStateManifestJsonCodec().loads(NSCF_MANIFEST.read_bytes())
    saved_state_paths = QeSavedStateManifestVerifier().verify(
        manifest, NSCF_RUN / "tmp"
    )
    if len(saved_state_paths) != 67:
        raise RuntimeError("unexpected NSCF saved-state inventory")
    kpoints = approved_kpoints()
    if input_kpoints(NSCF_INPUT) != kpoints:
        raise RuntimeError("NSCF input k-point order differs from the approved grid")
    qexsd_payload = NSCF_QEXSD.read_bytes()
    qexsd = QuantumEspressoXsdDocumentParser().execute(
        QexsdSource(
            canonical_path=str(NSCF_QEXSD),
            sha256=hashlib.sha256(qexsd_payload).hexdigest(),
            byte_count=len(qexsd_payload),
            content=qexsd_payload,
        )
    )
    eigenvalues_ev = tuple(
        value * 27.211386245988 for row in qexsd.eigenvalues for value in row
    )
    if (
        qexsd.exit_status != 0
        or qexsd.sampled_k_point_count != 64
        or qexsd.band_count != 12
        or min(eigenvalues_ev) <= OUTER_WINDOW_EV[0]
        or max(eigenvalues_ev) >= OUTER_WINDOW_EV[1]
    ):
        raise RuntimeError("QEXSD does not satisfy the preprocessing declaration")
    unit_cell = UnitCellJsonCodec().loads(
        STRUCTURE.read_text(encoding="utf-8"), expected_structure_id=STRUCTURE_ID
    )
    source = CalculatorInputSourceReference(
        simulation_id="si.accepted-s1.wannier-nscf-4x4x4-b12-david",
        representation="qe-nscf-saved-state-manifest",
        schema_version=1,
        byte_size=NSCF_MANIFEST.stat().st_size,
        sha256=NSCF_MANIFEST_SHA256,
    )
    declaration = Wannier90PreprocessingInput(
        input_id="si.accepted-s1.wannier90-preprocessing.sp3sstar",
        source=source,
        seedname=SEEDNAME,
        calculator_version_constraint="==3.1.0",
        num_bands=12,
        num_wann=10,
        unit_cell=unit_cell,
        projections=("Si:sp3", "Si:l=0:r=2"),
        mp_grid=(4, 4, 4),
        kpoints_reciprocal_fractional=MatrixQuantity(as_f64_array(kpoints), Unitless()),
        localization_iterations=100,
        localization_tolerance=ScalarQuantity(1.0e-10, _ANGSTROM_SQUARED),
        localization_convergence_window=3,
        write_hr=True,
        outer_window=(
            ScalarQuantity(OUTER_WINDOW_EV[0], _ELECTRON_VOLT),
            ScalarQuantity(OUTER_WINDOW_EV[1], _ELECTRON_VOLT),
        ),
        frozen_window=None,
        disentanglement_iterations=200,
        disentanglement_tolerance=ScalarQuantity(1.0e-10, _ANGSTROM_SQUARED),
        disentanglement_convergence_window=3,
        disentanglement_mix_ratio=ScalarQuantity(0.5, Unitless()),
        coordinate_precision=12,
    )
    prepared = declaration.prepare()
    if len(prepared.artifacts) != 1:
        raise RuntimeError("preprocessing declaration produced an unexpected artifact")
    artifact = prepared.artifacts[0]
    if artifact.filename != "silicon.win" or artifact.content != declaration.render():
        raise RuntimeError("prepared input differs from deterministic rendering")
    input_directory = ROOT / "input"
    input_directory.mkdir(mode=0o700)
    native_input = input_directory / artifact.filename
    native_input.write_bytes(artifact.content)
    prepared_record = ROOT / "prepared-input-record.json"
    prepared_record.write_bytes(prepared.canonical_bytes)
    write_json(
        ROOT / "campaign-preflight.json",
        {
            "schema_version": 1,
            "status": "awaiting-explicit-bounded-authorization",
            "execution_performed": False,
            "authorization_request": {
                "maximum_invocations": 1,
                "retries": 0,
                "stop_on_failure": True,
            },
            "purpose": "first sp3s-star Wannier90 neighbor-topology preprocessing qualification",
            "scientific_disposition": (
                "preflight only; no NNKP topology, interface, localization, or "
                "production-adequacy result"
            ),
            "projectkoios_revision": "e146f3722e87ca2de2243421a94448cfa6e27037",
            "integration_gap": (
                "the current tranche provides pure render/prepare and NNKP parsing but "
                "not the planned first-party preprocessing execution provider"
            ),
            "planned_command": [str(EXECUTABLE), "-pp", SEEDNAME],
            "executable": observation(EXECUTABLE),
            "decision": observation(DECISION),
            "structure": observation(STRUCTURE),
            "parent_nscf": {
                "manifest": observation(NSCF_MANIFEST),
                "saved_state_root": str(NSCF_RUN / "tmp"),
                "verified_file_count": len(saved_state_paths),
                "qexsd": observation(NSCF_QEXSD),
            },
            "prepared_input_record": {
                **observation(prepared_record),
                "record_sha256": prepared.sha256,
                "record_byte_size": prepared.byte_size,
            },
            "native_input": observation(native_input),
            "expected_output": "silicon.nnkp",
            "candidate": {
                "seedname": SEEDNAME,
                "num_bands": 12,
                "num_wann": 10,
                "projections": ["Si:sp3", "Si:l=0:r=2"],
                "mp_grid": [4, 4, 4],
                "kpoint_count": 64,
                "outer_window_ev": list(OUTER_WINDOW_EV),
                "qexsd_eigenvalue_range_ev": [
                    min(eigenvalues_ev),
                    max(eigenvalues_ev),
                ],
                "energy_reference": "native QE Kohn-Sham eigenvalue reference",
                "frozen_window": None,
                "localization_iterations": 100,
                "localization_tolerance_angstrom_squared": 1.0e-10,
                "localization_convergence_window": 3,
                "disentanglement_iterations": 200,
                "disentanglement_tolerance_angstrom_squared": 1.0e-10,
                "disentanglement_convergence_window": 3,
                "disentanglement_mix_ratio": 0.5,
                "write_hr": True,
            },
            "acceptance": {
                "required_return_code": 0,
                "required_output": "silicon.nnkp",
                "required_semantic_checks": [
                    "bounded NNKP parsing",
                    "source direct-lattice agreement",
                    "derived reciprocal-lattice agreement including 2 pi",
                    "source-ordered 64-point agreement",
                    "excluded-band agreement",
                    "expanded projection inventory sufficient for rank 10",
                ],
            },
            "resource_bounds": {
                "processes": 1,
                "timeout_seconds": TIMEOUT_SECONDS,
                "maximum_retained_bytes": MAXIMUM_BYTES,
            },
        },
    )


if __name__ == "__main__":
    main()
