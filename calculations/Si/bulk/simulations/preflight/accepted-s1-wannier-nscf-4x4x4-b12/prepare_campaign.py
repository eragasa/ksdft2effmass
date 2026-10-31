from __future__ import annotations

import hashlib
import json
from pathlib import Path

from projectkoios.integrations.quantumespresso.pw.inputfile.base import QeAtomicSpecies
from projectkoios.integrations.quantumespresso.pw.nscf.cards import (
    QeNscfDiagonalization,
    QeNscfOccupations,
    QeNscfVerbosity,
)
from projectkoios.integrations.quantumespresso.pw.nscf.configuration import (
    QeNscfKPoint,
    QeNscfProjectionConfiguration,
)
from projectkoios.integrations.quantumespresso.pw.nscf.execution import (
    QeNscfCalculationRunner,
    QeNscfCalculationRunRequest,
)
from projectkoios.integrations.quantumespresso.pw.nscf.projection import (
    QeNscfInputProjector,
)
from projectkoios.physkit.periodic.unit_cell import UnitCellJsonCodec
from projectkoios.simulations.structure import (
    StructureRecord,
    StructureRepresentation,
    StructureResolution,
    TransferredStructureProvenance,
)

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier-nscf-4x4x4-b12-20261031T071339Z"
)
KSD_ROOT = Path("/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint")
SIMULATIONS_ROOT = KSD_ROOT / "calculations/Si/bulk/simulations"
STRUCTURE = SIMULATIONS_ROOT / (
    "structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
)
DECISION = SIMULATIONS_ROOT / "wannier-interface-decision.md"
PARENT_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-parent-scf-gamma-k10-c42-20261031T070321Z"
)
PARENT_SAVED_STATE_ROOT = PARENT_ROOT / "run/tmp"
PARENT_MANIFEST = PARENT_ROOT / "scf-saved-state-manifest.json"
EXECUTABLE = Path("/Users/eugene/projects/q-e-qe-7.5/build/bin/pw.x")
PSEUDOPOTENTIAL = Path(
    "/Users/eugene/opt/pseudopotentials/quantum-espresso/sssp/1.3.0/"
    "sets/PBE/efficiency/Si.pbe-n-rrkjus_psl.1.0.0.UPF"
)
OUTPUT = ROOT / "preflight-output"
CONFIGURATION = ROOT / "calculation.toml"
STRUCTURE_ID = "Si.PrimitiveUnitCell.RightHanded.RelaxedS1"
STRUCTURE_SHA256 = "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03"
DECISION_SHA256 = "191b3c9657271d4aa08096bae0509ba9c0b4976123317977a0a80fe45e8fd9d6"
PARENT_MANIFEST_SHA256 = (
    "2b80acf2bc53dcbc5c667d50c4747036704a640c86cdf5902a98e998e21aefb9"
)
EXECUTABLE_SHA256 = "87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910"
PSEUDOPOTENTIAL_SHA256 = (
    "ae3aefd0811f9499dbc4a72f1f9ae02ef4fc7f3568bf6f559b68668719c69e2b"
)
TIMEOUT_SECONDS = 600.0
MAXIMUM_BYTES = 2 * 1024**3


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


def kpoints() -> tuple[QeNscfKPoint, ...]:
    return tuple(
        QeNscfKPoint(
            coordinates=(float(i) / 4.0, float(j) / 4.0, float(k) / 4.0),
            weight=1.0 / 64.0,
        )
        for i in range(4)
        for j in range(4)
        for k in range(4)
    )


def main() -> None:
    if any(path.name != "prepare_campaign.py" for path in ROOT.iterdir()):
        raise RuntimeError("preflight root must contain only prepare_campaign.py")
    identities = (
        (STRUCTURE, STRUCTURE_SHA256, "structure"),
        (DECISION, DECISION_SHA256, "Wannier-interface decision"),
        (PARENT_MANIFEST, PARENT_MANIFEST_SHA256, "parent manifest"),
        (EXECUTABLE, EXECUTABLE_SHA256, "executable"),
        (PSEUDOPOTENTIAL, PSEUDOPOTENTIAL_SHA256, "pseudopotential"),
    )
    for path, expected, label in identities:
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"{label} identity mismatch")
    unit_cell = UnitCellJsonCodec().loads(
        STRUCTURE.read_text(), expected_structure_id=STRUCTURE_ID
    )
    structure_record = StructureRecord(
        structure_id=STRUCTURE_ID,
        representation=StructureRepresentation.primitive,
        schema_version=1,
        sha256=STRUCTURE_SHA256,
        byte_size=STRUCTURE.stat().st_size,
        provenance=TransferredStructureProvenance(
            source="ksdft2effmass.accepted-stable-pair",
            revision=sha256(SIMULATIONS_ROOT / "accepted-stable-pair.json"),
            record_path=(
                "calculations/Si/bulk/simulations/structures/"
                "Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
            ),
            source_sha256=STRUCTURE_SHA256,
            result_sha256=STRUCTURE_SHA256,
        ),
    )
    projection_configuration = QeNscfProjectionConfiguration(
        species=(
            QeAtomicSpecies(
                symbol="Si",
                mass_amu=28.086,
                pseudopotential_filename=PSEUDOPOTENTIAL.name,
            ),
        ),
        kpoints=kpoints(),
        band_count=12,
        wavefunction_cutoff_ry=42.0,
        charge_density_cutoff_ry=336.0,
        electronic_tolerance_ry=1.0e-12,
        occupations=QeNscfOccupations.fixed,
        verbosity=QeNscfVerbosity.high,
        iprint=2,
        diagonalization=QeNscfDiagonalization.conjugate_gradient,
        full_diagonalization_accuracy=True,
        prefix="system",
        pseudo_dir="./",
        outdir="./tmp/",
        input_filename="pw.in",
        parent_saved_state_manifest_sha256=PARENT_MANIFEST_SHA256,
        disable_symmetry=True,
        disable_time_reversal=True,
        coordinate_precision=8,
        kpoint_precision=12,
    )
    projection = QeNscfInputProjector(projection_configuration).project(
        StructureResolution(
            record=structure_record,
            path=STRUCTURE,
            unit_cell=unit_cell,
        )
    )
    source_root = ROOT / "source-input"
    source_root.mkdir(mode=0o700)
    source_input = source_root / "pw.in"
    source_input.write_text(projection.rendered_input.text, encoding="ascii")
    configuration = f'''schema_version = 1
calculation_id = "si-accepted-s1-wannier-nscf-4x4x4-b12"
phase = "nscf"
integration_id = "quantum-espresso"

[source_input]
path = "{source_input}"
byte_size = {source_input.stat().st_size}
sha256 = "{sha256(source_input)}"

[structure]
path = "{STRUCTURE}"
structure_id = "{STRUCTURE_ID}"
byte_size = {STRUCTURE.stat().st_size}
sha256 = "{STRUCTURE_SHA256}"

[calculator]
program = "pw.x"
program_version = "7.5"
path = "{EXECUTABLE}"
byte_size = {EXECUTABLE.stat().st_size}
sha256 = "{EXECUTABLE_SHA256}"

[parent_scf]
output_directory = "{PARENT_ROOT}"
saved_state_root = "{PARENT_SAVED_STATE_ROOT}"
manifest_path = "{PARENT_MANIFEST}"
manifest_byte_size = {PARENT_MANIFEST.stat().st_size}
manifest_sha256 = "{PARENT_MANIFEST_SHA256}"
calculation = "scf"
prefix = "system"

[pseudopotential]
symbol = "Si"
filename = "{PSEUDOPOTENTIAL.name}"
path = "{PSEUDOPOTENTIAL}"
byte_size = {PSEUDOPOTENTIAL.stat().st_size}
sha256 = "{PSEUDOPOTENTIAL_SHA256}"
mass_amu = 28.086

[sampling]
kpoint_grid = [4, 4, 4]
kpoint_offset = [0, 0, 0]
band_count = 12
wavefunction_cutoff_ry = 42.0
charge_density_cutoff_ry = 336.0
electronic_tolerance_ry = 1.0e-12
occupations = "fixed"

[qe]
prefix = "system"
pseudo_dir = "./"
outdir = "./tmp/"
input_filename = "pw.in"
verbosity = "high"
iprint = 2
diagonalization = "cg"
diago_full_acc = true
disable_symmetry = true
disable_time_reversal = true
coordinate_precision = 8
kpoint_precision = 12

[output]
directory = "{OUTPUT}"

[qualification]
statements = [
  "This is the approved first ten-orbital component-route qualification candidate, not production acceptance.",
  "The full unreduced Gamma-origin 4 x 4 x 4 grid has k varying fastest, then j, then i.",
  "Twelve retained bands support a rank-ten candidate with disentanglement; adequacy remains unproven.",
  "All twelve bands form the initial outer space and no frozen inner window is declared.",
  "Native QE coefficient evidence is retained in addition to the later spectral interface.",
  "Configuration content and dry-run rendering grant no calculator-execution authority.",
]
'''
    CONFIGURATION.write_text(configuration, encoding="utf-8")
    result = QeNscfCalculationRunner().run(
        QeNscfCalculationRunRequest(
            configuration_path=CONFIGURATION,
            execute=False,
            timeout_seconds=TIMEOUT_SECONDS,
        )
    )
    rendered = result.output_directory / "pw.in"
    if rendered.read_bytes() != source_input.read_bytes():
        raise RuntimeError("maintained NSCF runner changed the approved source input")
    manifest = {
        "schema_version": 1,
        "status": "awaiting-explicit-bounded-authorization",
        "execution_performed": False,
        "authorization_request": {
            "maximum_invocations": 1,
            "retries": 0,
            "stop_on_failure": True,
        },
        "purpose": "approved first ten-orbital component-route NSCF qualification candidate",
        "scientific_disposition": "preflight only; no NSCF, Wannier interface, or production adequacy result",
        "projectkoios_revision": "e146f3722e87ca2de2243421a94448cfa6e27037",
        "decision": observed(DECISION),
        "parent_handoff": {
            "output_directory": str(PARENT_ROOT),
            "saved_state_root": str(PARENT_SAVED_STATE_ROOT),
            "manifest": observed(PARENT_MANIFEST),
        },
        "configuration": observed(CONFIGURATION),
        "rendered_input": observed(rendered),
        "input_manifest": observed(result.input_manifest),
        "structure": observed(STRUCTURE),
        "executable": observed(EXECUTABLE),
        "pseudopotential": observed(PSEUDOPOTENTIAL),
        "candidate": {
            "grid": [4, 4, 4],
            "offset": [0, 0, 0],
            "kpoint_count": 64,
            "ordering": "lexicographic i,j,k with k fastest",
            "weight_per_kpoint": 0.015625,
            "band_count": 12,
            "wannier_rank": 10,
            "trial_projections": "Si:sp3;l=0:r=2",
            "outer_space": "all 12 retained bands",
            "frozen_inner_window": None,
            "disentanglement_required": True,
            "evidence_profile": "component-operator",
        },
        "resource_bounds": {
            "processes": 1,
            "timeout_seconds": TIMEOUT_SECONDS,
            "maximum_retained_bytes": MAXIMUM_BYTES,
        },
    }
    write_json(ROOT / "campaign-preflight.json", manifest)


if __name__ == "__main__":
    main()
