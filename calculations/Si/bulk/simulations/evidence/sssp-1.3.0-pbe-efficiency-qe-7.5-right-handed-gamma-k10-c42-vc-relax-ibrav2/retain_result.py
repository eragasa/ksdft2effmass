from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

from ksdft2effmass.integration.quantum_espresso.qexsd import (
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)
from projectkoios.integrations.quantumespresso.pw.vc_relax.bravais import (
    QeFccPrimitiveBravaisMapping,
)
from projectkoios.integrations.quantumespresso.pw.vc_relax.data_extraction import (
    QeVcRelaxDataExtractor,
)
from projectkoios.physkit.periodic.unit_cell import UnitCellJsonCodec
from projectkoios.physkit.units import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    PhysicalUnit,
    ScalarQuantity,
)

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-bulk-vc-relax-ibrav2-gamma-k10-c42-20261031T061128Z"
)
RUN = ROOT / "run"
RESULT = ROOT / "result"
S1_ID = "Si.PrimitiveUnitCell.RightHanded.RelaxedS1"
QEXSD_RELATIVE_PATH = "tmp/system.save/data-file-schema.xml"


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    RESULT.mkdir(exist_ok=True)
    allowed_existing = {
        f"{S1_ID}.json",
        "relaxation-result.json",
        "postprocessing-provenance.json",
        "postprocessing-attempts.json",
    }
    unexpected = {path.name for path in RESULT.iterdir()} - allowed_existing
    if unexpected:
        raise ValueError(f"result directory contains unexpected files: {unexpected}")

    qexsd_path = RUN / QEXSD_RELATIVE_PATH
    qexsd_content = qexsd_path.read_bytes()
    qexsd_sha256 = sha256_bytes(qexsd_content)
    document = QuantumEspressoXsdDocumentParser().execute(
        QexsdSource(
            f"/external/{ROOT.name}/{QEXSD_RELATIVE_PATH}",
            qexsd_sha256,
            len(qexsd_content),
            qexsd_content,
        )
    )
    stdout = (RUN / "pw.out").read_bytes()
    stderr = (RUN / "pw.err").read_bytes()
    data = QeVcRelaxDataExtractor().extract(
        stdout_payload=stdout,
        stderr_payload=stderr,
        qexsd_document=document,
    )
    if not (data.job_completed and data.scf_converged and data.optimizer_converged):
        raise ValueError("retained QE output does not report completed convergence")
    if data.final_structure is None:
        raise ValueError("canonical QEXSD extraction produced no final structure")
    if document.exit_status != 0:
        raise ValueError("QEXSD exit status is not zero")
    if not data.consistency.terminal_status_matches:
        raise ValueError("stdout and QEXSD terminal status disagree")
    if not data.consistency.atom_count_matches:
        raise ValueError("stdout and QEXSD atom count disagree")

    s1 = QeFccPrimitiveBravaisMapping().restore_source_basis(
        data.final_structure.unit_cell
    )
    if float(np.linalg.det(s1.A.magnitude)) <= 0.0:
        raise ValueError("restored S1 source basis is not right-handed")
    s1_path = RESULT / f"{S1_ID}.json"
    s1_path.write_text(
        UnitCellJsonCodec().dumps(s1, structure_id=S1_ID),
        encoding="utf-8",
    )
    decoded = UnitCellJsonCodec().loads(
        s1_path.read_text(encoding="utf-8"),
        expected_structure_id=S1_ID,
    )
    if not np.allclose(decoded.H.magnitude, s1.H.magnitude, rtol=0.0, atol=0.0):
        raise RuntimeError("serialized S1 lattice failed exact round trip")

    total_energy_ry = data.stdout.total_energy_ry
    if total_energy_ry is None or not math.isfinite(total_energy_ry):
        raise ValueError("final total energy is unavailable or non-finite")
    final_energy_ev = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
        ScalarQuantity(total_energy_ry, PhysicalUnit("rydberg")),
        PhysicalUnit("electron_volt"),
    ).magnitude
    flags = tuple(
        token
        for token in (
            "IEEE_INVALID_FLAG",
            "IEEE_DIVIDE_BY_ZERO",
            "IEEE_OVERFLOW_FLAG",
            "IEEE_UNDERFLOW_FLAG",
        )
        if token.encode("ascii") in stderr
    )
    result = {
        "schema_version": 1,
        "status": "completed-provisional-s1",
        "scientific_acceptance": False,
        "execution": {
            "invocations": 1,
            "retries": 0,
            "returncode": 0,
            "job_completed": data.job_completed,
            "scf_converged": data.scf_converged,
            "optimizer_converged": data.optimizer_converged,
            "bfgs_steps": data.stdout.bfgs_step_count,
            "trajectory_records": len(data.steps),
        },
        "qexsd": {
            "parser": (
                "ksdft2effmass.integration.quantum_espresso.qexsd."
                "QuantumEspressoXsdDocumentParser"
            ),
            "qexsd_version": document.qexsd_version,
            "declared_unit_system": document.declared_unit_system_label,
            "exit_status": document.exit_status,
            "source_path": document.source_path,
            "byte_size": document.source_byte_count,
            "sha256": document.source_sha256,
            "stdout_terminal_status_matches": (
                data.consistency.terminal_status_matches
            ),
            "stdout_atom_count_matches": data.consistency.atom_count_matches,
        },
        "final_observations": {
            "conventional_lattice_parameter_angstrom": (
                s1.lattice_parameter.magnitude
            ),
            "primitive_volume_angstrom_cubed": float(abs(np.linalg.det(s1.H.magnitude))),
            "final_scf_total_energy_ry_per_cell": total_energy_ry,
            "final_scf_total_energy_ev_per_atom": final_energy_ev / 2.0,
            "optimizer_terminal_pressure_kbar": data.stdout.optimizer_pressure_kbar,
            "final_scf_pressure_kbar": data.stdout.pressure_kbar,
            "optimizer_terminal_maximum_force_ry_per_bohr": (
                data.stdout.optimizer_maximum_atomic_force_ry_per_bohr
            ),
            "optimizer_terminal_stress_ry_per_bohr_cubed": (
                data.stdout.optimizer_stress_ry_per_bohr_cubed
            ),
            "final_scf_stress_ry_per_bohr_cubed": (
                data.stdout.stress_ry_per_bohr_cubed
            ),
            "stress_sign_convention": "compression-positive",
            "cell_pressure_tolerance_kbar": 0.5,
            "force_tolerance_ry_per_bohr": 3.8893807597e-4,
        },
        "geometry_verification": {
            "source_basis_determinant_sign": "positive",
            "source_basis_restoration": (
                "projectkoios QeFccPrimitiveBravaisMapping.restore_source_basis"
            ),
            "qexsd_native_fractional_positions": [
                atom.position_fractional.magnitude.tolist()
                for atom in data.final_structure.unit_cell.atomic_basis.atoms
            ],
            "restored_source_fractional_positions": [
                atom.position_fractional.magnitude.tolist()
                for atom in s1.atomic_basis.atoms
            ],
        },
        "native_diagnostics": {
            "ieee_flags": flags,
            "disposition": (
                "retained native QE diagnostics; not an automatic blocker because "
                "the run completed, converged, and produced finite retained results"
            ),
        },
        "provisional_structure": {
            "structure_id": S1_ID,
            "path": str(s1_path),
            "byte_size": s1_path.stat().st_size,
            "sha256": sha256(s1_path),
            "disposition": (
                "provisional S1; fresh k-point and cutoff confirmation is required"
            ),
        },
        "artifacts": {
            relative: {
                "byte_size": (RUN / relative).stat().st_size,
                "sha256": sha256(RUN / relative),
            }
            for relative in (
                "pw.in",
                "pw.out",
                "pw.err",
                "execution.json",
                "artifact-manifest.json",
                QEXSD_RELATIVE_PATH,
            )
        },
    }
    write_json(RESULT / "relaxation-result.json", result)


if __name__ == "__main__":
    main()
