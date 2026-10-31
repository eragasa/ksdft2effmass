from __future__ import annotations

import hashlib
import importlib
from collections import Counter
from pathlib import Path

from projectkoios.physkit import units as _physkit_units

if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = (  # type: ignore[attr-defined]
        _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER
    )
if not hasattr(_physkit_units, "MODEL_SYSTEM_UNIT_CONVERTER"):
    _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER = (  # type: ignore[attr-defined]
        _physkit_units.ModelSystemUnitConverter
    )

from projectkoios.integrations.quantumespresso.saved_state import (  # noqa: E402
    QeSavedStateManifestJsonCodec,
    QeSavedStateManifestVerifier,
)
from projectkoios.physkit.numeric import as_f64_array  # noqa: E402
from projectkoios.physkit.periodic.unit_cell import UnitCellJsonCodec  # noqa: E402
from projectkoios.physkit.units import (  # noqa: E402
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)
from projectkoios.simulations.calculator_input import (  # noqa: E402
    CalculatorInputSourceReference,
)

from ksdft2effmass.integration.quantum_espresso.qexsd import (  # noqa: E402
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)
from ksdft2effmass.serialization import TypedJsonMappingSerializer  # noqa: E402

Wannier90PreprocessingInput = importlib.import_module(
    "projectkoios.integrations.wannier90"
).Wannier90PreprocessingInput

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[2]
SIMULATIONS = BULK / "simulations"
STRUCTURE = SIMULATIONS / ("structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json")
PROTOCOL = BULK / "research-protocol/research-protocol.tex"
DECISION = SIMULATIONS / "c6-b20-w21-outer-window-decision.md"
NSCF_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20-v1"
)
NSCF_RUN = NSCF_ROOT / "run"
NSCF_INPUT = NSCF_ROOT / "pw.in"
NSCF_QEXSD = NSCF_RUN / "tmp/system.save/data-file-schema.xml"
NSCF_MANIFEST = NSCF_RUN / "nscf-saved-state-manifest.json"
TARGET_SPACE_ANALYSIS = NSCF_ROOT / "target-space-analysis.json"
EXECUTABLE = Path("/Users/eugene/projects/wannier90-3.1.0/wannier90.x")
PROPOSED_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-c6-b20-w21-v1"
)
NATIVE_INPUT = ROOT / "silicon.win"
PREPARED_RECORD = ROOT / "prepared-input-record.json"
PREFLIGHT = ROOT / "campaign-preflight.json"
AUTHORIZATION_REQUEST = ROOT / "authorization-request.json"
STRUCTURE_ID = "Si.PrimitiveUnitCell.RightHanded.RelaxedS1"
OUTER_WINDOW_EV = (-6.0, 21.0)
FROZEN_WINDOW_EV = (-5.85, 8.0)
_ANGSTROM_SQUARED = PhysicalUnit("angstrom ** 2")
_ELECTRON_VOLT = PhysicalUnit("eV")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, object]:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def input_kpoints(path: Path) -> tuple[tuple[float, float, float], ...]:
    lines = path.read_text(encoding="ascii").splitlines()
    marker = lines.index("K_POINTS crystal")
    count = int(lines[marker + 1])
    rows = tuple(
        tuple(float(value) for value in line.split()[:3])
        for line in lines[marker + 2 : marker + 2 + count]
    )
    if count != 216 or len(rows) != count or any(len(row) != 3 for row in rows):
        raise RuntimeError("malformed C6 NSCF k-point inventory")
    return rows


def window_counts(
    eigenvalues_ev: tuple[tuple[float, ...], ...],
    window: tuple[float, float],
) -> tuple[int, ...]:
    return tuple(
        sum(window[0] <= value <= window[1] for value in row) for row in eigenvalues_ev
    )


class C6B20W21PreprocessingPreflight:
    """Prepare the selected C6-B20-W21 preprocessing occurrence."""

    __slots__ = ()

    def execute(self) -> None:
        if PROPOSED_ROOT.exists():
            raise RuntimeError("proposed C6-B20-W21 preprocessing root already exists")
        expected = {
            STRUCTURE: (
                "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03"
            ),
            PROTOCOL: (
                "e3a04bd0e04bcf350bba8c2dab2ddddab973ce39beac1bc34c8e8e82a0da24a1"
            ),
            DECISION: (
                "a6f95574137f4b69fd42fc1040d21bc1fd4691487d36a6c1de643d5b1d3c1e2e"
            ),
            NSCF_INPUT: (
                "20a6ee6e55d632bb66b1afcaac91592bf49c73a3e53e275659d1ccb03e47e1f9"
            ),
            NSCF_QEXSD: (
                "2e1b5e157142d18210d18710fb9f5f3e813b17d8331acf96e11af9b9d4f7ef8c"
            ),
            NSCF_MANIFEST: (
                "24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac"
            ),
            TARGET_SPACE_ANALYSIS: (
                "976b605c1095e93fc99500ec93df0e7f495229afe83a2d185c666c6429daf444"
            ),
            EXECUTABLE: (
                "c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd"
            ),
        }
        for path, digest in expected.items():
            if not path.is_file() or path.is_symlink() or sha256(path) != digest:
                raise RuntimeError(f"source identity mismatch: {path}")
        manifest = QeSavedStateManifestJsonCodec().loads(NSCF_MANIFEST.read_bytes())
        saved_paths = QeSavedStateManifestVerifier().verify(manifest, NSCF_RUN / "tmp")
        if len(saved_paths) != 219:
            raise RuntimeError("unexpected C6-B20 NSCF saved-state inventory")
        qexsd_payload = NSCF_QEXSD.read_bytes()
        qexsd = QuantumEspressoXsdDocumentParser().execute(
            QexsdSource(
                canonical_path=str(NSCF_QEXSD),
                sha256=sha256(NSCF_QEXSD),
                byte_count=len(qexsd_payload),
                content=qexsd_payload,
            )
        )
        if (
            qexsd.exit_status != 0
            or qexsd.sampled_k_point_count != 216
            or qexsd.band_count != 20
        ):
            raise RuntimeError("C6-B20 QEXSD is not an eligible preprocessing source")
        eigenvalues_ev = tuple(
            tuple(value * 27.211386245988 for value in row) for row in qexsd.eigenvalues
        )
        outer_counts = window_counts(eigenvalues_ev, OUTER_WINDOW_EV)
        frozen_counts = window_counts(eigenvalues_ev, FROZEN_WINDOW_EV)
        if min(outer_counts) < 10 or max(frozen_counts) > 10:
            raise RuntimeError(
                "selected windows are dimensionally incompatible with rank 10"
            )
        if Counter(outer_counts) != Counter({12: 48, 13: 108, 14: 60}):
            raise RuntimeError("selected outer-window inventory changed")
        if Counter(frozen_counts) != Counter({4: 129, 5: 84, 6: 3}):
            raise RuntimeError("retained frozen-window inventory changed")
        band_12_maximum_ev = max(row[11] for row in eigenvalues_ev)
        band_15_minimum_ev = min(row[14] for row in eigenvalues_ev)
        if not band_12_maximum_ev < OUTER_WINDOW_EV[1] < band_15_minimum_ev:
            raise RuntimeError("selected upper-window clearance changed")
        kpoints = input_kpoints(NSCF_INPUT)
        unit_cell = UnitCellJsonCodec().loads(
            STRUCTURE.read_text(encoding="utf-8"),
            expected_structure_id=STRUCTURE_ID,
        )
        source = CalculatorInputSourceReference(
            simulation_id="si.accepted-s1.C6-B20.wannier-nscf-6x6x6-b20-david",
            representation="qe-nscf-saved-state-manifest",
            schema_version=1,
            byte_size=NSCF_MANIFEST.stat().st_size,
            sha256=expected[NSCF_MANIFEST],
        )
        declaration = Wannier90PreprocessingInput(
            input_id="si.accepted-s1.C6-B20-W21.wannier90-preprocessing",
            source=source,
            seedname="silicon",
            calculator_version_constraint="==3.1.0",
            num_bands=20,
            num_wann=10,
            unit_cell=unit_cell,
            projections=("Si:sp3", "Si:l=0:r=2"),
            mp_grid=(6, 6, 6),
            kpoints_reciprocal_fractional=MatrixQuantity(
                as_f64_array(kpoints), Unitless()
            ),
            localization_iterations=4000,
            localization_tolerance=ScalarQuantity(2.0e-9, _ANGSTROM_SQUARED),
            localization_convergence_window=6,
            write_hr=True,
            outer_window=(
                ScalarQuantity(OUTER_WINDOW_EV[0], _ELECTRON_VOLT),
                ScalarQuantity(OUTER_WINDOW_EV[1], _ELECTRON_VOLT),
            ),
            frozen_window=(
                ScalarQuantity(FROZEN_WINDOW_EV[0], _ELECTRON_VOLT),
                ScalarQuantity(FROZEN_WINDOW_EV[1], _ELECTRON_VOLT),
            ),
            disentanglement_iterations=4000,
            disentanglement_tolerance=ScalarQuantity(1.0e-10, Unitless()),
            disentanglement_convergence_window=3,
            disentanglement_mix_ratio=ScalarQuantity(0.2, Unitless()),
            coordinate_precision=12,
        )
        prepared = declaration.prepare()
        if len(prepared.artifacts) != 1:
            raise RuntimeError("unexpected preprocessing input artifact count")
        artifact = prepared.artifacts[0]
        rendered = declaration.render()
        if artifact.filename != "silicon.win" or artifact.content != rendered:
            raise RuntimeError("prepared input differs from pure rendering")
        NATIVE_INPUT.write_bytes(rendered)
        PREPARED_RECORD.write_bytes(prepared.canonical_bytes)
        serializer = TypedJsonMappingSerializer()
        preflight = {
            "schema_version": 1,
            "status": "authorization-required",
            "execution_performed": False,
            "purpose": ("C6-B20-W21 Wannier90 neighbor-topology preprocessing"),
            "sources": {
                "structure": identity(STRUCTURE),
                "research_protocol": identity(PROTOCOL),
                "target_space_decision": identity(DECISION),
                "target_space_analysis": identity(TARGET_SPACE_ANALYSIS),
                "nscf_input": identity(NSCF_INPUT),
                "nscf_qexsd": identity(NSCF_QEXSD),
                "nscf_saved_state_manifest": identity(NSCF_MANIFEST),
                "wannier90_executable": identity(EXECUTABLE),
            },
            "saved_state_verification": {
                "file_count": len(saved_paths),
                "total_bytes": sum(path.stat().st_size for path in saved_paths),
            },
            "prepared_input_record": identity(PREPARED_RECORD),
            "native_input": identity(NATIVE_INPUT),
            "planned_command": [str(EXECUTABLE), "-pp", "silicon"],
            "candidate": {
                "candidate_id": "C6-B20-W21",
                "num_bands": 20,
                "num_wann": 10,
                "mp_grid": [6, 6, 6],
                "kpoint_count": 216,
                "projections": ["Si:sp3", "Si:l=0:r=2"],
                "outer_window_ev": list(OUTER_WINDOW_EV),
                "outer_count_range": [min(outer_counts), max(outer_counts)],
                "outer_count_histogram": {
                    str(key): value
                    for key, value in sorted(Counter(outer_counts).items())
                },
                "band_12_upper_clearance_ev": (OUTER_WINDOW_EV[1] - band_12_maximum_ev),
                "band_15_lower_clearance_ev": (band_15_minimum_ev - OUTER_WINDOW_EV[1]),
                "frozen_window_ev": list(FROZEN_WINDOW_EV),
                "frozen_count_range": [min(frozen_counts), max(frozen_counts)],
                "frozen_count_histogram": {
                    str(key): value
                    for key, value in sorted(Counter(frozen_counts).items())
                },
                "localization_iterations": 4000,
                "localization_tolerance_angstrom_squared": 2.0e-9,
                "localization_convergence_window": 6,
                "disentanglement_iterations": 4000,
                "disentanglement_tolerance_fractional": 1.0e-10,
                "disentanglement_convergence_window": 3,
                "disentanglement_mix_ratio": 0.2,
            },
            "acceptance": {
                "required_return_code": 0,
                "required_output": "silicon.nnkp",
                "lattice_tolerances": {
                    "direct_angstrom": 1.0e-7,
                    "reciprocal_inverse_angstrom": 1.0e-7,
                    "fractional_kpoint": 1.0e-8,
                },
                "required_semantic_checks": [
                    "bounded NNKP parsing",
                    "source direct-lattice agreement",
                    "derived reciprocal-lattice agreement including 2 pi",
                    "source-ordered 216-point agreement",
                    "excluded-band agreement",
                    "projection inventory sufficient for rank 10",
                ],
            },
            "resource_bounds": {
                "processes": 1,
                "timeout_seconds": 120.0,
                "maximum_retained_bytes": 32 * 1024**2,
                "retries": 0,
            },
            "scientific_disposition": (
                "preflight only; no C6-B20-W21 NNKP topology, conversion, "
                "localization, represented operator, or intended-use result"
            ),
        }
        PREFLIGHT.write_bytes(serializer.serialize(preflight))
        request = {
            "schema_version": 1,
            "status": "authorization-required",
            "authorization_granted": False,
            "requested_occurrence": {
                "purpose": "C6-B20-W21 Wannier90 preprocessing",
                "proposed_root": str(PROPOSED_ROOT),
                "command": [str(EXECUTABLE), "-pp", "silicon"],
                "input": identity(NATIVE_INPUT),
                "maximum_invocations": 1,
                "retries": 0,
                "processes": 1,
                "timeout_seconds": 120.0,
                "maximum_retained_bytes": 32 * 1024**2,
            },
            "downstream_not_authorized": [
                "pw2wannier90 conversion",
                "Wannier90 localization",
                "C6-B30",
                "C8",
                "C12",
                "confirmation-parent execution",
                "component-operator construction",
                "Slater-Koster reduction",
                "automatic retry",
            ],
            "boundary": (
                "the consumed C6-B20 pw.x authorization and the outer-window "
                "decision do not authorize Wannier90 -pp"
            ),
        }
        AUTHORIZATION_REQUEST.write_bytes(serializer.serialize(request))


def main() -> None:
    C6B20W21PreprocessingPreflight().execute()


if __name__ == "__main__":
    main()
