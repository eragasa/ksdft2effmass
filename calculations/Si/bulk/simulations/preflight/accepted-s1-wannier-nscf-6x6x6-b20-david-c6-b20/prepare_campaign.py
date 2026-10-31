from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from projectkoios.physkit import units as _physkit_units

if not hasattr(_physkit_units, "MODEL_SYSTEM_UNIT_CONVERTER"):
    _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER = (  # type: ignore[attr-defined]
        _physkit_units.ModelSystemUnitConverter
    )

from projectkoios.integrations.quantumespresso.pw.inputfile.base import (  # noqa: E402
    QeAtomicSpecies,
)
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
from projectkoios.integrations.quantumespresso.saved_state import (
    QeSavedStateManifestJsonCodec,
    QeSavedStateManifestVerifier,
)
from projectkoios.physkit.periodic.unit_cell import UnitCellJsonCodec
from projectkoios.simulations.structure import (
    StructureRecord,
    StructureRepresentation,
    StructureResolution,
    TransferredStructureProvenance,
)

from ksdft2effmass.serialization import TypedJsonMappingSerializer

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[2]
SIMULATIONS = BULK / "simulations"
ANALYSIS = BULK / "analysis"
STRUCTURE = SIMULATIONS / ("structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json")
ACCEPTED_PAIR = SIMULATIONS / "accepted-stable-pair.json"
RECOMMENDATION_ROOT = ANALYSIS / "construction-mesh-adequacy-recommendation"
RECOMMENDATION = RECOMMENDATION_ROOT / "recommendation.json"
MESH_MANIFEST = RECOMMENDATION_ROOT / "construction-mesh-candidates.json"
PROTOCOL = BULK / "research-protocol/research-protocol.tex"
DECISION = SIMULATIONS / "c6-b20-aiida-moderate-parent-band-decision.md"
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
PROPOSED_OCCURRENCE = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20-v1"
)
RENDERED = ROOT / "rendered"
INPUT = ROOT / "pw.in"
CONFIGURATION = ROOT / "calculation.toml"
PREFLIGHT = ROOT / "campaign-preflight.json"
AUTHORIZATION_REQUEST = ROOT / "authorization-request.json"
AIIDA_REFERENCE = ROOT / "aiida-workflow-reference.json"
STRUCTURE_ID = "Si.PrimitiveUnitCell.RightHanded.RelaxedS1"
TIMEOUT_SECONDS = 600.0
MAXIMUM_RETAINED_BYTES = 512 * 1024**2


@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    """Bind one exact C6-B20 preflight dependency."""

    label: str
    path: Path
    byte_size: int
    sha256: str


class ArtifactAuthenticator:
    """Authenticate exact files and reject symlinks."""

    __slots__ = ()

    def execute(self, identity: ArtifactIdentity) -> dict[str, object]:
        if not identity.path.is_file() or identity.path.is_symlink():
            raise RuntimeError(f"{identity.label} is not a regular file")
        payload = identity.path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        if len(payload) != identity.byte_size or digest != identity.sha256:
            raise RuntimeError(f"{identity.label} identity mismatch")
        return {
            "path": str(identity.path),
            "byte_size": len(payload),
            "sha256": digest,
        }


class ParentSavedStateAuthenticator:
    """Verify the accepted parent manifest and every bound saved-state artifact."""

    __slots__ = ()

    def execute(self) -> dict[str, object]:
        payload = PARENT_MANIFEST.read_bytes()
        manifest = QeSavedStateManifestJsonCodec().loads(payload)
        verified = QeSavedStateManifestVerifier().verify(
            manifest, PARENT_SAVED_STATE_ROOT
        )
        return {
            "manifest_path": str(PARENT_MANIFEST),
            "manifest_byte_size": len(payload),
            "manifest_sha256": hashlib.sha256(payload).hexdigest(),
            "saved_state_root": str(PARENT_SAVED_STATE_ROOT),
            "verified_file_count": len(verified),
            "verified_total_bytes": sum(path.stat().st_size for path in verified),
            "copy_performed": False,
        }


class C6MeshLoader:
    """Load the exact ordered C6 mesh from the protocol-bound recommendation."""

    __slots__ = ()

    def execute(self) -> tuple[QeNscfKPoint, ...]:
        record = json.loads(MESH_MANIFEST.read_text(encoding="utf-8"))
        candidates = record["candidates"]
        candidate = next(item for item in candidates if item["label"] == "C6")
        if (
            candidate["grid"] != [6, 6, 6]
            or candidate["offset"] != [0, 0, 0]
            or candidate["point_count"] != 216
            or candidate["disposition"] != "first-successor"
        ):
            raise RuntimeError("C6 mesh declaration changed")
        points = tuple(
            QeNscfKPoint(
                coordinates=tuple(item["fractional_reciprocal_coordinates"]),
                weight=item["qe_crystal_weight"],
            )
            for item in candidate["points"]
        )
        if len(points) != 216:
            raise RuntimeError("C6 mesh must contain 216 points")
        if abs(sum(point.weight for point in points) - 1.0) > 1.0e-14:
            raise RuntimeError("C6 weights must sum to one")
        return points


class C6B20NscfPreflight:
    """Render and bind an exact no-execution C6-B20 NSCF preflight."""

    __slots__ = ()

    def execute(self) -> None:
        authenticator = ArtifactAuthenticator()
        sources = {
            key: authenticator.execute(identity) for key, identity in ARTIFACTS.items()
        }
        parent = ParentSavedStateAuthenticator().execute()
        unit_cell = UnitCellJsonCodec().loads(
            STRUCTURE.read_text(encoding="utf-8"),
            expected_structure_id=STRUCTURE_ID,
        )
        structure_record = StructureRecord(
            structure_id=STRUCTURE_ID,
            representation=StructureRepresentation.primitive,
            schema_version=1,
            sha256=ARTIFACTS["structure"].sha256,
            byte_size=ARTIFACTS["structure"].byte_size,
            provenance=TransferredStructureProvenance(
                source="ksdft2effmass.accepted-stable-pair",
                revision=ARTIFACTS["accepted_pair"].sha256,
                record_path=(
                    "calculations/Si/bulk/simulations/structures/"
                    "Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
                ),
                source_sha256=ARTIFACTS["structure"].sha256,
                result_sha256=ARTIFACTS["structure"].sha256,
            ),
        )
        points = C6MeshLoader().execute()
        projection_configuration = QeNscfProjectionConfiguration(
            species=(
                QeAtomicSpecies(
                    symbol="Si",
                    mass_amu=28.086,
                    pseudopotential_filename=PSEUDOPOTENTIAL.name,
                ),
            ),
            kpoints=points,
            band_count=20,
            wavefunction_cutoff_ry=42.0,
            charge_density_cutoff_ry=336.0,
            electronic_tolerance_ry=1.0e-12,
            occupations=QeNscfOccupations.fixed,
            verbosity=QeNscfVerbosity.high,
            iprint=2,
            diagonalization=QeNscfDiagonalization.davidson,
            full_diagonalization_accuracy=True,
            prefix="system",
            pseudo_dir="./",
            outdir="./tmp/",
            input_filename="pw.in",
            parent_saved_state_manifest_sha256=ARTIFACTS["parent_manifest"].sha256,
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
        INPUT.write_text(projection.rendered_input.text, encoding="ascii")
        CONFIGURATION.write_text(self._configuration(), encoding="utf-8")
        self._reset_dry_run_output()
        result = QeNscfCalculationRunner().run(
            QeNscfCalculationRunRequest(
                configuration_path=CONFIGURATION,
                execute=False,
                timeout_seconds=TIMEOUT_SECONDS,
            )
        )
        rendered = result.output_directory / "pw.in"
        if rendered.read_bytes() != INPUT.read_bytes():
            raise RuntimeError("maintained NSCF runner changed the approved input")
        serializer = TypedJsonMappingSerializer()
        AIIDA_REFERENCE.write_bytes(serializer.serialize(self._aiida_reference()))
        preflight = self._preflight(sources, parent, result.input_manifest)
        PREFLIGHT.write_bytes(serializer.serialize(preflight))
        input_identity = self._identity(INPUT)
        request = self._authorization_request(input_identity)
        AUTHORIZATION_REQUEST.write_bytes(serializer.serialize(request))

    @staticmethod
    def _reset_dry_run_output() -> None:
        if not RENDERED.exists():
            return
        if RENDERED.is_symlink() or not RENDERED.is_dir():
            raise RuntimeError("dry-run output is not a regular directory")
        children = tuple(RENDERED.iterdir())
        expected = {"input-manifest.json", "pw.in"}
        if {path.name for path in children} != expected:
            raise RuntimeError("dry-run output contains unexpected files")
        if any(path.is_symlink() or not path.is_file() for path in children):
            raise RuntimeError("dry-run output contains non-regular files")
        for path in children:
            path.unlink()
        RENDERED.rmdir()

    @staticmethod
    def _configuration() -> str:
        return f'''schema_version = 1
calculation_id = "si-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20"
phase = "nscf"
integration_id = "quantum-espresso"

[source_input]
path = "{INPUT}"
byte_size = {INPUT.stat().st_size}
sha256 = "{hashlib.sha256(INPUT.read_bytes()).hexdigest()}"

[structure]
path = "{STRUCTURE}"
structure_id = "{STRUCTURE_ID}"
byte_size = {STRUCTURE.stat().st_size}
sha256 = "{ARTIFACTS["structure"].sha256}"

[calculator]
program = "pw.x"
program_version = "7.5"
path = "{EXECUTABLE}"
byte_size = {EXECUTABLE.stat().st_size}
sha256 = "{ARTIFACTS["executable"].sha256}"

[parent_scf]
output_directory = "{PARENT_ROOT}"
saved_state_root = "{PARENT_SAVED_STATE_ROOT}"
manifest_path = "{PARENT_MANIFEST}"
manifest_byte_size = {PARENT_MANIFEST.stat().st_size}
manifest_sha256 = "{ARTIFACTS["parent_manifest"].sha256}"
calculation = "scf"
prefix = "system"

[pseudopotential]
symbol = "Si"
filename = "{PSEUDOPOTENTIAL.name}"
path = "{PSEUDOPOTENTIAL}"
byte_size = {PSEUDOPOTENTIAL.stat().st_size}
sha256 = "{ARTIFACTS["pseudopotential"].sha256}"
mass_amu = 28.086

[sampling]
kpoint_grid = [6, 6, 6]
kpoint_offset = [0, 0, 0]
band_count = 20
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
diagonalization = "david"
diago_full_acc = true
disable_symmetry = true
disable_time_reversal = true
coordinate_precision = 8
kpoint_precision = 12

[output]
directory = "{RENDERED}"

[qualification]
statements = [
  "C6-B20 changes only the parent-band count from 12 to 20 relative to C6.",
  "The 216 points use the authenticated C6 ordering and unit total weight.",
  "Structure, parent, pseudopotential, cutoffs, mesh, and NSCF controls stay fixed.",
  "Factor-two band-count heuristic follows pinned AiiDA workflow 3.1.0.",
  "Rank and outer-window selection remain separate downstream scientific decisions.",
  "Dry-run rendering and saved-state verification grant no execution authority.",
]
'''

    @staticmethod
    def _aiida_reference() -> dict[str, object]:
        commit = "1c0115cb7c77541a0bd549bc05005df435d651b6"
        repository = "https://github.com/aiidateam/aiida-wannier90-workflows"
        return {
            "schema_version": 1,
            "software": "aiida-wannier90-workflows",
            "release": "3.1.0",
            "commit": commit,
            "commit_url": f"{repository}/commit/{commit}",
            "retrieved_utc_date": "2026-10-31",
            "sources": [
                {
                    "role": "moderate protocol num_bands_factor authority",
                    "path": (
                        "src/aiida_wannier90_workflows/workflows/protocols/"
                        "base/wannier90.yaml"
                    ),
                    "url": (
                        f"{repository}/blob/{commit}/src/aiida_wannier90_workflows/"
                        "workflows/protocols/base/wannier90.yaml#L6-L25"
                    ),
                    "byte_size": 1_820,
                    "sha256": (
                        "f6b2bd7e95a4b8be387c12a35d9eef83a7e28a4f3c0128dbec8f8990f37890c7"
                    ),
                },
                {
                    "role": "band-count estimator implementation authority",
                    "path": "src/aiida_wannier90_workflows/utils/pseudo/__init__.py",
                    "url": (
                        f"{repository}/blob/{commit}/src/aiida_wannier90_workflows/"
                        "utils/pseudo/__init__.py#L292-L342"
                    ),
                    "byte_size": 24_840,
                    "sha256": (
                        "53d9fdcef7afc5ad0f0e93bc9c567a78343b249737ab1d97514c20b0e564e609"
                    ),
                },
                {
                    "role": "workflow software citation guidance",
                    "path": "README.md",
                    "url": f"{repository}/tree/{commit}#support-and-citations",
                    "byte_size": 3_088,
                    "sha256": (
                        "8123884ae67330600a013c3263e2d9d9a43f87518340a7120678c604befa2ce1"
                    ),
                },
            ],
            "moderate_num_bands_factor": 2.0,
            "campaign_application": {
                "spin_character": "non-spin-polarized",
                "nspin_multiplier": 1,
                "valence_electron_count": 8,
                "declared_projection_count": 10,
                "estimator_terms": [8, 8, 20, 14],
                "selected_parent_band_count": 20,
            },
            "adaptation_boundary": (
                "Only the factor-two moderate band-count heuristic is adopted. The "
                "campaign retains its SSSP 1.3 PBE efficiency pseudopotential and "
                "declared projection family; it does not adopt or claim execution of "
                "the complete AiiDA workflow protocol."
            ),
        }

    @staticmethod
    def _preflight(
        sources: dict[str, dict[str, object]],
        parent: dict[str, object],
        input_manifest: Path,
    ) -> dict[str, object]:
        observed_c6_saved_bytes = 58_433_245
        band_ratio = 20.0 / 12.0
        return {
            "schema_version": 1,
            "status": "authorization-required",
            "execution_performed": False,
            "purpose": ("C6-B20 one-variable parent-band-inventory NSCF preflight"),
            "sources": sources,
            "parent_saved_state_verification": parent,
            "configuration": C6B20NscfPreflight._identity(CONFIGURATION),
            "rendered_input": C6B20NscfPreflight._identity(INPUT),
            "runner_input_manifest": C6B20NscfPreflight._identity(input_manifest),
            "aiida_workflow_reference": C6B20NscfPreflight._identity(AIIDA_REFERENCE),
            "candidate": {
                "label": "C6-B20",
                "changed_coordinate": ("parent-band count 12 to 20"),
                "grid": [6, 6, 6],
                "offset": [0, 0, 0],
                "kpoint_count": 216,
                "ordering": "lexicographic i,j,k with k fastest",
                "weight_per_kpoint": 1.0 / 216.0,
                "band_count": 20,
                "wannier_rank_downstream": 10,
                "wavefunction_cutoff_ry": 42.0,
                "charge_density_cutoff_ry": 336.0,
                "electronic_tolerance_ry": 1.0e-12,
                "occupations": "fixed",
                "diagonalization": "david",
                "full_diagonalization_accuracy": True,
                "disable_symmetry": True,
                "disable_time_reversal": True,
            },
            "resource_planning": {
                "processes": 1,
                "timeout_seconds": TIMEOUT_SECONDS,
                "maximum_retained_bytes": MAXIMUM_RETAINED_BYTES,
                "band_count_relative_to_C6_B12": band_ratio,
                "linear_saved_state_estimate_bytes": round(
                    observed_c6_saved_bytes * band_ratio
                ),
                "observed_comparators": {
                    "C6_B12_216_point_wall_seconds": 28.04,
                    "C6_B12_saved_state_bytes": observed_c6_saved_bytes,
                },
                "linear_wall_time_estimate_seconds_range": [42.06, 56.08],
                "estimate_nonclaim": (
                    "planning estimate only; runtime and retained bytes are not "
                    "guaranteed to scale linearly"
                ),
            },
            "stop_policy": {
                "unconverged_eigenvalue_diagnostic": "block",
                "nonfinite_values": "block",
                "corrupt_or_inconsistent_qexsd": "block",
                "timeout": "block-with-no-automatic-retry",
                "nonzero_return_code": "block-with-no-automatic-retry",
            },
            "scientific_disposition": (
                "preflight only; no C6-B20 NSCF, Wannier interface, provider "
                "eligibility, or scientific adequacy result"
            ),
        }

    @staticmethod
    def _authorization_request(input_identity: dict[str, object]) -> dict[str, object]:
        return {
            "schema_version": 1,
            "status": "authorization-required",
            "authorization_granted": False,
            "requested_occurrence": {
                "purpose": "C6-B20 6x6x6 20-band Davidson parent-inventory NSCF",
                "proposed_root": str(PROPOSED_OCCURRENCE),
                "executable": str(EXECUTABLE),
                "command": [str(EXECUTABLE), "-in", "pw.in"],
                "input": input_identity,
                "parent_manifest_sha256": ARTIFACTS["parent_manifest"].sha256,
                "pseudopotential_sha256": ARTIFACTS["pseudopotential"].sha256,
                "kpoint_count": 216,
                "band_count": 20,
                "maximum_invocations": 1,
                "retries": 0,
                "processes": 1,
                "timeout_seconds": TIMEOUT_SECONDS,
                "maximum_retained_bytes": MAXIMUM_RETAINED_BYTES,
            },
            "requested_filesystem_actions": {
                "create_fresh_occurrence_root": True,
                "verify_and_copy_parent_saved_state": True,
                "copy_pseudopotential": True,
                "mutate_parent_saved_state": False,
            },
            "required_retained_outputs": [
                "authorization.json",
                "campaign-preflight.json",
                "calculation.toml",
                "pw.in",
                "run/execution.json",
                "run/pw.out",
                "run/pw.err",
                "run/tmp/system.save/data-file-schema.xml",
                "run/nscf-saved-state-manifest.json",
                "run/artifact-manifest.json",
                "nscf-result.json",
                "campaign-result.json",
            ],
            "downstream_not_authorized": [
                "20-band target-window selection",
                "Wannier90 preprocessing",
                "pw2wannier90 conversion",
                "Wannier90 localization",
                "C8",
                "C12",
                "successor confirmation parent",
                "automatic retry",
            ],
            "boundary": (
                "continuing recommendation and preflight preparation does not itself "
                "authorize this exact pw.x invocation"
            ),
        }

    @staticmethod
    def _identity(path: Path) -> dict[str, object]:
        payload = path.read_bytes()
        return {
            "path": str(path),
            "byte_size": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }


ARTIFACTS = {
    "structure": ArtifactIdentity(
        "accepted S1 structure",
        STRUCTURE,
        758,
        "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03",
    ),
    "accepted_pair": ArtifactIdentity(
        "accepted stable pair",
        ACCEPTED_PAIR,
        2_770,
        "953ba609c2c8a4be4c6049fa882592b050b16ffcf9080098bd8bfa4b829fc84b",
    ),
    "recommendation": ArtifactIdentity(
        "construction-mesh recommendation",
        RECOMMENDATION,
        4_595,
        "990eeae5b57b91a9b81ab39a23ef54510e130967aa9f1236de79c5408fdebf87",
    ),
    "mesh_manifest": ArtifactIdentity(
        "construction-mesh candidates",
        MESH_MANIFEST,
        514_520,
        "1e5ebb9dffa6a97a2f2445cfd6290aff4cd3d6c06c15e4e0e7d6bbde7826c803",
    ),
    "protocol": ArtifactIdentity(
        "research protocol",
        PROTOCOL,
        20_492,
        "02b7c1a3bff4e1024e21fd6e2b28810f76b1a374c876936e9cc8980559211ce8",
    ),
    "decision": ArtifactIdentity(
        "C6-B20 parent-band decision",
        DECISION,
        4_826,
        "781aa4242d69c4eb70b8c762182171eb0e491356341c7a4735d80f5173b35c4b",
    ),
    "parent_manifest": ArtifactIdentity(
        "accepted parent saved-state manifest",
        PARENT_MANIFEST,
        10_763,
        "2b80acf2bc53dcbc5c667d50c4747036704a640c86cdf5902a98e998e21aefb9",
    ),
    "executable": ArtifactIdentity(
        "QE pw.x executable",
        EXECUTABLE,
        9_673_048,
        "87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910",
    ),
    "pseudopotential": ArtifactIdentity(
        "SSSP silicon pseudopotential",
        PSEUDOPOTENTIAL,
        1_299_382,
        "ae3aefd0811f9499dbc4a72f1f9ae02ef4fc7f3568bf6f559b68668719c69e2b",
    ),
}


def main() -> None:
    C6B20NscfPreflight().execute()


if __name__ == "__main__":
    main()
