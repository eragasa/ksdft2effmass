"""S110-independent CSD0/CSD1 producer for the blocked common-space rank gate."""

from __future__ import annotations

import hashlib
import importlib
import json
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path
from typing import TextIO, cast

import numpy as np
from numpy.typing import NDArray
from projectkoios.integrations.wannier90 import (
    Wannier90DisentanglementMatrixParser,
    Wannier90ProjectionParser,
    Wannier90UnitaryMatrixParser,
)

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]
type ComplexArray = NDArray[np.complex128]
type FloatArray = NDArray[np.float64]

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
REPOSITORY = ROOT.parents[4]
DIAGNOSIS_OWNER = BULK / "analysis/c6-b20-w21-slater-koster-definition-fit"
DEFAULT_REQUEST = DIAGNOSIS_OWNER / "common-space-diagnosis-request.json"
DEFAULT_ENTRYPOINT = DIAGNOSIS_OWNER / "run_common_space_diagnosis.py"
RESULT_NAME = "result.json"
SUMMARY_NAME = "human-readable-summary.txt"
MANIFEST_NAME = "manifest.json"
PROGRESS_INTERVAL = 36
EXPECTED_REQUEST_ID = "CSD0-CSD1-c6-b20-w21-common-space-diagnosis-v1"
EXPECTED_REQUEST_STATUS = (
    "implementation-development-request-no-retained-execution-authority"
)
EXPECTED_STAGES = ("CSD0", "CSD1")
EXPECTED_SOURCE_LABELS = (
    "S30_untruncated_characterization",
    "S105_full_support_disposition",
    "S110_blocked_result",
    "hopping_first_protocol",
    "AMN",
    "gauge",
    "disentanglement",
)
EXPECTED_PROVIDER_MODULES = (
    "projectkoios.integrations.wannier90",
    "projectkoios.integrations.wannier90._matrix_conventions",
    "projectkoios.integrations.wannier90._parsing",
    "projectkoios.integrations.wannier90.interface_data",
    "projectkoios.integrations.wannier90.unitary_matrices",
    "projectkoios.integrations.wannier90.disentanglement_matrices",
)
# Immutable S110 bytes use legacy A/B labels. They are accepted only at this explicit
# correlation boundary and are mapped positionally to the descriptive current labels.
RETAINED_S110_BASIS_ORDER = (
    "A:s",
    "A:px",
    "A:py",
    "A:pz",
    "A:s-star",
    "B:s",
    "B:px",
    "B:py",
    "B:pz",
    "B:s-star",
)
EXPECTED_BASIS_ORDER = (
    "diamond_origin_center:s",
    "diamond_origin_center:px",
    "diamond_origin_center:py",
    "diamond_origin_center:pz",
    "diamond_origin_center:s-star",
    "diamond_body_diagonal_quarter_center:s",
    "diamond_body_diagonal_quarter_center:px",
    "diamond_body_diagonal_quarter_center:py",
    "diamond_body_diagonal_quarter_center:pz",
    "diamond_body_diagonal_quarter_center:s-star",
)
EXPECTED_CLAIM_BOUNDARY = (
    "Read-only no-calculator reconstruction of the S110 common-space rank gate. It "
    "authorizes no fit, QE or Wannier90 execution, target-space change, evidence "
    "promotion, symmetry attribution, or scientific acceptance."
)


@dataclass(frozen=True, slots=True, kw_only=True)
class FileSourceDeclaration:
    """One exact local file identity required by CSD0."""

    label: str
    location: str
    declared_path: str
    byte_size: int
    sha256: str

    def resolve(self) -> Path:
        """Resolve the declared path without fallback, escape, or inference."""
        path = Path(self.declared_path)
        if self.location == "repository":
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(
                    f"repository source path escapes its owner for {self.label}"
                )
            candidate = REPOSITORY / path
            resolved_repository = REPOSITORY.resolve()
            if not candidate.resolve().is_relative_to(resolved_repository):
                raise ValueError(
                    f"repository source path escapes its owner for {self.label}"
                )
            return candidate
        if self.location == "absolute" and path.is_absolute():
            return path
        raise ValueError(
            f"unsupported source location for {self.label}: {self.location}"
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ProviderModuleDeclaration:
    """One imported provider module and its exact source digest."""

    module_name: str
    sha256: str


@dataclass(frozen=True, slots=True, kw_only=True)
class StateSpaceDefinition:
    """The explicitly declared common-space dimensions and conventions."""

    construction_grid_size_per_axis: int
    kpoint_count: int
    parent_band_count: int
    retained_rank: int
    basis_order: tuple[str, ...]
    geometry: str
    spin_convention: str
    operator_units: str
    energy_reference: str

    def __post_init__(self) -> None:
        """Validate explicit positive dimensions and ordered basis coordinates."""
        for dimension_name, dimension in (
            ("construction_grid_size_per_axis", self.construction_grid_size_per_axis),
            ("kpoint_count", self.kpoint_count),
            ("parent_band_count", self.parent_band_count),
            ("retained_rank", self.retained_rank),
        ):
            if type(dimension) is not int or dimension <= 0:
                raise ValueError(f"{dimension_name} must be a positive integer")
        if len(self.basis_order) != self.retained_rank:
            raise ValueError("basis_order dimension differs from retained_rank")
        if len(set(self.basis_order)) != len(self.basis_order) or any(
            type(label) is not str or not label for label in self.basis_order
        ):
            raise ValueError("basis_order must contain unique nonempty strings")
        for text_name, text in (
            ("geometry", self.geometry),
            ("spin_convention", self.spin_convention),
            ("operator_units", self.operator_units),
            ("energy_reference", self.energy_reference),
        ):
            if type(text) is not str or not text:
                raise ValueError(f"{text_name} must be a nonempty string")


@dataclass(frozen=True, slots=True, kw_only=True)
class NativePrecisionDefinition:
    """Decimal precision retained by the three native Wannier90 artifacts."""

    amn_decimal_places: int
    gauge_decimal_places: int
    disentanglement_decimal_places: int

    def __post_init__(self) -> None:
        """Reject booleans, negative precision, and non-integer declarations."""
        for name, value in (
            ("amn_decimal_places", self.amn_decimal_places),
            ("gauge_decimal_places", self.gauge_decimal_places),
            ("disentanglement_decimal_places", self.disentanglement_decimal_places),
        ):
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer")


@dataclass(frozen=True, slots=True, kw_only=True)
class RetainedDiagnosisComparison:
    """The S110 values that an independent CSD1 run must reproduce."""

    deficient_indices: tuple[int, ...]
    minimum_singular_values: tuple[float, ...]
    native_uncertainty_bound: float
    gamma_atomic_orbital_weights: tuple[tuple[str, float], ...]

    def __post_init__(self) -> None:
        """Validate the finite retained comparison without admitting booleans."""
        if any(type(index) is not int or index < 0 for index in self.deficient_indices):
            raise ValueError("deficient_indices must contain nonnegative integers")
        if len(self.deficient_indices) != len(self.minimum_singular_values):
            raise ValueError("deficient indices and singular values differ in size")
        if any(
            type(value) not in {int, float} or not np.isfinite(value) or value < 0.0
            for value in self.minimum_singular_values
        ):
            raise ValueError("minimum_singular_values must be finite and nonnegative")
        if (
            type(self.native_uncertainty_bound) not in {int, float}
            or not np.isfinite(self.native_uncertainty_bound)
            or self.native_uncertainty_bound < 0.0
        ):
            raise ValueError("native_uncertainty_bound must be finite and nonnegative")
        labels = tuple(label for label, _value in self.gamma_atomic_orbital_weights)
        if len(set(labels)) != len(labels) or any(
            type(label) is not str or not label for label in labels
        ):
            raise ValueError("Gamma weight labels must be unique nonempty strings")
        if any(
            type(value) not in {int, float}
            or not np.isfinite(value)
            or not 0.0 <= value <= 1.0
            for _label, value in self.gamma_atomic_orbital_weights
        ):
            raise ValueError("Gamma weights must be finite values in [0, 1]")


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceDiagnosisRequest:
    """The complete CSD0/CSD1 request consumed by the diagnostic action."""

    request_id: str
    status: str
    file_sources: tuple[FileSourceDeclaration, ...]
    provider_distribution: str
    provider_version: str
    provider_modules: tuple[ProviderModuleDeclaration, ...]
    state_space: StateSpaceDefinition
    native_precision: NativePrecisionDefinition
    retained_comparison: RetainedDiagnosisComparison
    claim_boundary: str


@dataclass(frozen=True, slots=True, kw_only=True)
class FileIdentity:
    """One authenticated source identity."""

    label: str
    path: str
    byte_size: int
    sha256: str

    def to_json(self) -> JsonObject:
        """Return a strict JSON representation."""
        return {
            "label": self.label,
            "path": self.path,
            "byte_size": self.byte_size,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class ProviderIdentity:
    """The authenticated source identity of one imported provider module."""

    module_name: str
    path: str
    byte_size: int
    sha256: str

    def to_json(self) -> JsonObject:
        """Return a strict JSON representation."""
        return {
            "module_name": self.module_name,
            "path": self.path,
            "byte_size": self.byte_size,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class KPointDiagnosis:
    """One separately reconstructed rank and subspace-overlap diagnostic."""

    ordered_index: int
    fractional_coordinates: tuple[float, float, float]
    resolved_rank: int
    maximum_singular_value: float
    next_to_minimum_singular_value: float
    minimum_singular_value: float
    condition_number: float | None
    minimum_principal_cosine: float
    maximum_principal_angle_radians: float
    full_rank_gate_passed: bool

    def __post_init__(self) -> None:
        """Validate one finite diagnostic record and its optional condition number."""
        if type(self.ordered_index) is not int or self.ordered_index < 0:
            raise ValueError("ordered_index must be a nonnegative integer")
        if len(self.fractional_coordinates) != 3 or any(
            type(value) not in {int, float} or not np.isfinite(value)
            for value in self.fractional_coordinates
        ):
            raise ValueError("fractional_coordinates must contain three finite reals")
        if type(self.resolved_rank) is not int or self.resolved_rank < 0:
            raise ValueError("resolved_rank must be a nonnegative integer")
        for name, value in (
            ("maximum_singular_value", self.maximum_singular_value),
            ("next_to_minimum_singular_value", self.next_to_minimum_singular_value),
            ("minimum_singular_value", self.minimum_singular_value),
        ):
            if type(value) not in {int, float} or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if self.condition_number is not None and (
            type(self.condition_number) not in {int, float}
            or not np.isfinite(self.condition_number)
            or self.condition_number < 0.0
        ):
            raise ValueError("condition_number must be finite, nonnegative, or None")
        if (
            type(self.minimum_principal_cosine) not in {int, float}
            or not np.isfinite(self.minimum_principal_cosine)
            or not 0.0 <= self.minimum_principal_cosine <= 1.0
        ):
            raise ValueError("minimum_principal_cosine must be finite and in [0, 1]")
        if (
            type(self.maximum_principal_angle_radians) not in {int, float}
            or not np.isfinite(self.maximum_principal_angle_radians)
            or not 0.0 <= self.maximum_principal_angle_radians <= np.pi
        ):
            raise ValueError(
                "maximum_principal_angle_radians must be finite and in [0, pi]"
            )
        if type(self.full_rank_gate_passed) is not bool:
            raise ValueError("full_rank_gate_passed must be a boolean")

    def to_json(self) -> JsonObject:
        """Return a strict JSON representation."""
        return {
            "ordered_kpoint_index_zero_based": self.ordered_index,
            "fractional_reciprocal_coordinates": list(self.fractional_coordinates),
            "resolved_rank_at_native_bound": self.resolved_rank,
            "maximum_singular_value": self.maximum_singular_value,
            "next_to_minimum_singular_value": self.next_to_minimum_singular_value,
            "minimum_singular_value": self.minimum_singular_value,
            "condition_number": self.condition_number,
            "minimum_principal_cosine_after_trial_frame_orthonormalization": (
                self.minimum_principal_cosine
            ),
            "maximum_principal_angle_radians_after_trial_frame_orthonormalization": (
                self.maximum_principal_angle_radians
            ),
            "full_rank_gate_passed": self.full_rank_gate_passed,
        }


class HumanReadableProgressReporter:
    """Write deterministic, plain-text runtime progress to stdout and a transcript."""

    __slots__ = ("_lines", "_stream")

    def __init__(self, *, stream: TextIO) -> None:
        self._stream = stream
        self._lines: list[str] = []

    def line(self, text: str = "") -> None:
        """Write and retain one line immediately."""
        self._lines.append(text)
        self._stream.write(text + "\n")
        self._stream.flush()

    def heading(self, title: str) -> None:
        """Write one visually distinct heading."""
        self.line(title)
        self.line("=" * len(title))

    def stage(self, stage_id: str, description: str) -> None:
        """Announce one controlled stage."""
        self.line()
        self.line(f"[{stage_id}] {description}")

    def transcript(self) -> str:
        """Return the exact emitted transcript."""
        return "\n".join(self._lines) + "\n"


class CommonSpaceRankDiagnosis:
    """Authenticate inputs and reconstruct the S110 rank gate without fitting."""

    __slots__ = ()

    def execute(
        self,
        *,
        request_path: Path,
        output_root: Path,
        reporter: HumanReadableProgressReporter,
    ) -> JsonObject:
        """Run CSD0 and CSD1, then retain deterministic diagnostic artifacts."""
        request_candidate = request_path.absolute()
        if not request_candidate.is_file() or request_candidate.is_symlink():
            raise FileNotFoundError(
                f"request is absent, not a file, or a symlink: {request_candidate}"
            )
        request_path = request_candidate.resolve()
        output_root = output_root.resolve()
        if output_root.exists():
            raise FileExistsError(f"fresh output root already exists: {output_root}")
        output_paths = tuple(
            output_root / name for name in (RESULT_NAME, SUMMARY_NAME, MANIFEST_NAME)
        )
        for path in output_paths:
            if path.exists():
                raise FileExistsError(f"refusing to overwrite {path}")

        request = read_request(path=request_path)
        reporter.heading("C6-B20-W21 common-space rank diagnosis")
        reporter.line(f"Request: {request.request_id}")
        reporter.line("Execution class: read-only, no-calculator diagnostic")
        reporter.line("Authorized calculator invocations: 0")
        reporter.line("Authorized fit invocations: 0")

        reporter.stage("CSD0", "Authenticate the frozen evidence and software inputs")
        authenticated_files = tuple(
            authenticate_file(source, reporter) for source in request.file_sources
        )
        provider_identities = authenticate_provider(request, reporter)
        request_identity = identity_for_path("request", request_path)
        reporter.line(
            f"  [OK] {len(authenticated_files)} data/evidence files and "
            f"{len(provider_identities)} provider modules authenticated"
        )

        reporter.stage(
            "CSD1",
            "Reconstruct the 216-point trial-to-Wannier overlap rank gate",
        )
        analysis = reconstruct_rank_gate(request, reporter)
        reporter.line("  [OK] retained deficient-point inventory reproduced")
        reporter.line("  [OK] retained-subspace unitary-invariance control passed")

        scientific_status = cast(str, analysis["scientific_disposition"])
        reporter.stage("STATUS", "Report execution outcome and scientific disposition")
        reporter.line("  Execution outcome: COMPLETED")
        reporter.line(f"  Scientific disposition: {scientific_status}")
        reporter.line("  Fit invoked: NO")
        reporter.line("  QE or Wannier90 invoked: NO")
        reporter.line("  Independent CSD1 verifier: NOT IMPLEMENTED")
        reporter.line("  Higher-precision sensitivity extension: NOT IMPLEMENTED")
        reporter.line("  Symmetry-related point inventory extension: NOT IMPLEMENTED")
        reporter.line("  CSD2 symmetry attribution: NOT RUN")
        reporter.line("  Human CSD3 branch selection: REQUIRED")
        reporter.line()
        reporter.line("Interpretation:")
        reporter.line(
            "  The declared ten-dimensional atomic trial frame does not have ten "
            "resolved directions in the retained Wannier subspace at every source point."
        )
        reporter.line(
            "  This reproduces the common-space stop condition; it does not establish "
            "energy degeneracy or a symmetry irrep as the cause."
        )
        reporter.line()
        reporter.line("Next controlled step:")
        reporter.line(
            "  Audit whether authenticated parent-space symmetry actions exist for CSD2."
        )
        reporter.line(
            "  If they do not, record INSUFFICIENT_RETAINED_SYMMETRY_DATA and stop."
        )
        reporter.line()
        reporter.line("Artifacts:")
        reporter.line(f"  {output_root / RESULT_NAME}")
        reporter.line(f"  {output_root / SUMMARY_NAME}")
        reporter.line(f"  {output_root / MANIFEST_NAME}")

        result: JsonObject = {
            "schema_version": 1,
            "record_type": "c6_b20_w21_common_space_rank_diagnosis",
            "request_id": request.request_id,
            "execution_outcome": "completed",
            "scientific_disposition": scientific_status,
            "calculator_invocations": 0,
            "fit_invocations": 0,
            "CSD0": {
                "outcome": "passed",
                "request": request_identity.to_json(),
                "authenticated_files": [
                    identity.to_json() for identity in authenticated_files
                ],
                "provider_distribution": request.provider_distribution,
                "provider_version": request.provider_version,
                "provider_modules": [
                    identity.to_json() for identity in provider_identities
                ],
            },
            "CSD1": analysis,
            "independent_verification": {
                "outcome": "not-implemented",
                "reason": (
                    "the current implementation is a producer independent of S110; "
                    "a separately implemented CSD1 verifier is still required"
                ),
            },
            "CSD2": {
                "outcome": "not-run",
                "reason": "parent-space symmetry actions have not been authenticated",
            },
            "CSD3": {
                "outcome": "human-disposition-required",
                "authorization_inferred": False,
            },
            "claim_boundary": request.claim_boundary,
            "implementation_identity": identity_for_path(
                "implementation", Path(__file__).resolve()
            ).to_json(),
        }
        result_bytes = canonical_json(result)
        summary_bytes = reporter.transcript().encode("utf-8")
        manifest = build_manifest(
            request_path=request_path,
            result_bytes=result_bytes,
            summary_bytes=summary_bytes,
        )
        output_root.mkdir(parents=True, exist_ok=False)
        write_exclusive(output_root / RESULT_NAME, result_bytes)
        write_exclusive(output_root / SUMMARY_NAME, summary_bytes)
        write_exclusive(output_root / MANIFEST_NAME, canonical_json(manifest))
        return result


def read_request(*, path: Path) -> CommonSpaceDiagnosisRequest:
    """Read one strict CSD0/CSD1 development request."""
    payload = require_object(json.loads(path.read_text(encoding="utf-8")), "request")
    if require_integer(payload.get("schema_version"), "schema_version") != 1:
        raise ValueError("unsupported request schema_version")
    status = require_string(payload.get("status"), "status")
    if status != EXPECTED_REQUEST_STATUS:
        raise ValueError(f"unsupported request status: {status}")
    stages = tuple(
        require_string(value, f"stages[{index}]")
        for index, value in enumerate(require_list(payload.get("stages"), "stages"))
    )
    if stages != EXPECTED_STAGES:
        raise ValueError(f"stages must be exactly {EXPECTED_STAGES}")
    if (
        require_integer(
            payload.get("calculator_invocations_authorized"),
            "calculator_invocations_authorized",
        )
        != 0
    ):
        raise ValueError("the request must authorize zero calculator invocations")
    if (
        require_integer(
            payload.get("fit_invocations_authorized"), "fit_invocations_authorized"
        )
        != 0
    ):
        raise ValueError("the request must authorize zero fit invocations")

    source_payload = require_object(payload.get("sources"), "sources")
    if set(source_payload) != set(EXPECTED_SOURCE_LABELS):
        raise ValueError(f"sources must be exactly {EXPECTED_SOURCE_LABELS}")
    sources: list[FileSourceDeclaration] = []
    for label in EXPECTED_SOURCE_LABELS:
        declaration = require_object(source_payload.get(label), f"sources.{label}")
        sources.append(
            FileSourceDeclaration(
                label=label,
                location=require_string(
                    declaration.get("location"), f"sources.{label}.location"
                ),
                declared_path=require_string(
                    declaration.get("path"), f"sources.{label}.path"
                ),
                byte_size=require_integer(
                    declaration.get("byte_size"), f"sources.{label}.byte_size"
                ),
                sha256=require_sha256(
                    declaration.get("sha256"), f"sources.{label}.sha256"
                ),
            )
        )

    provider = require_object(payload.get("provider"), "provider")
    provider_distribution = require_string(
        provider.get("distribution"), "provider.distribution"
    )
    if provider_distribution != "projectkoios-simulations":
        raise ValueError("provider.distribution must be projectkoios-simulations")
    module_payload = require_object(provider.get("modules"), "provider.modules")
    if set(module_payload) != set(EXPECTED_PROVIDER_MODULES):
        raise ValueError(
            f"provider.modules must be exactly {EXPECTED_PROVIDER_MODULES}"
        )
    modules = tuple(
        ProviderModuleDeclaration(
            module_name=module_name,
            sha256=require_sha256(
                module_payload.get(module_name), f"provider.modules.{module_name}"
            ),
        )
        for module_name in EXPECTED_PROVIDER_MODULES
    )

    state = require_object(payload.get("state_space"), "state_space")
    basis_order = tuple(
        require_string(value, f"state_space.basis_order[{index}]")
        for index, value in enumerate(
            require_list(state.get("basis_order"), "state_space.basis_order")
        )
    )
    state_space = StateSpaceDefinition(
        construction_grid_size_per_axis=require_integer(
            state.get("construction_grid_size_per_axis"),
            "state_space.construction_grid_size_per_axis",
        ),
        kpoint_count=require_integer(
            state.get("kpoint_count"), "state_space.kpoint_count"
        ),
        parent_band_count=require_integer(
            state.get("parent_band_count"), "state_space.parent_band_count"
        ),
        retained_rank=require_integer(
            state.get("retained_rank"), "state_space.retained_rank"
        ),
        basis_order=basis_order,
        geometry=require_string(state.get("geometry"), "state_space.geometry"),
        spin_convention=require_string(
            state.get("spin_convention"), "state_space.spin_convention"
        ),
        operator_units=require_string(
            state.get("operator_units"), "state_space.operator_units"
        ),
        energy_reference=require_string(
            state.get("energy_reference"), "state_space.energy_reference"
        ),
    )
    expected_state_space = StateSpaceDefinition(
        construction_grid_size_per_axis=6,
        kpoint_count=216,
        parent_band_count=20,
        retained_rank=10,
        basis_order=EXPECTED_BASIS_ORDER,
        geometry="two-site primitive bulk-silicon cell retained from S30",
        spin_convention="spinless scalar-relativistic non-SOC",
        operator_units="electronvolt",
        energy_reference="unchanged native S30 Wannier reference",
    )
    if state_space != expected_state_space:
        raise ValueError("state_space differs from the frozen C6-B20-W21 definition")

    precision = require_object(payload.get("native_precision"), "native_precision")
    native_precision = NativePrecisionDefinition(
        amn_decimal_places=require_integer(
            precision.get("AMN_decimal_places"), "native_precision.AMN_decimal_places"
        ),
        gauge_decimal_places=require_integer(
            precision.get("gauge_decimal_places"),
            "native_precision.gauge_decimal_places",
        ),
        disentanglement_decimal_places=require_integer(
            precision.get("disentanglement_decimal_places"),
            "native_precision.disentanglement_decimal_places",
        ),
    )

    if native_precision != NativePrecisionDefinition(
        amn_decimal_places=12,
        gauge_decimal_places=10,
        disentanglement_decimal_places=10,
    ):
        raise ValueError("native_precision differs from the frozen native-file policy")

    retained = require_object(
        payload.get("retained_diagnosis_comparison"),
        "retained_diagnosis_comparison",
    )
    indices = tuple(
        require_integer(value, f"retained indices[{index}]")
        for index, value in enumerate(
            require_list(
                retained.get("deficient_kpoint_indices_zero_based"),
                "retained deficient indices",
            )
        )
    )
    minimum_values = tuple(
        require_float(value, f"retained minimum singular values[{index}]")
        for index, value in enumerate(
            require_list(
                retained.get("minimum_singular_values"),
                "retained minimum singular values",
            )
        )
    )
    if len(indices) != len(minimum_values):
        raise ValueError(
            "retained deficient indices and singular values differ in size"
        )
    gamma_payload = require_object(
        retained.get("gamma_atomic_orbital_weights"),
        "retained gamma weights",
    )
    gamma_weights = tuple(
        (label, require_float(gamma_payload.get(label), f"gamma weight {label}"))
        for label in basis_order
    )
    comparison = RetainedDiagnosisComparison(
        deficient_indices=indices,
        minimum_singular_values=minimum_values,
        native_uncertainty_bound=require_float(
            retained.get("native_uncertainty_bound"),
            "retained native uncertainty bound",
        ),
        gamma_atomic_orbital_weights=gamma_weights,
    )

    claim_boundary = require_string(payload.get("claim_boundary"), "claim_boundary")
    if claim_boundary != EXPECTED_CLAIM_BOUNDARY:
        raise ValueError(
            "claim_boundary differs from the fail-closed development scope"
        )

    request_id = require_string(payload.get("request_id"), "request_id")
    if request_id != EXPECTED_REQUEST_ID:
        raise ValueError(f"unsupported request_id: {request_id}")

    return CommonSpaceDiagnosisRequest(
        request_id=request_id,
        status=status,
        file_sources=tuple(sources),
        provider_distribution=provider_distribution,
        provider_version=require_string(provider.get("version"), "provider.version"),
        provider_modules=modules,
        state_space=state_space,
        native_precision=native_precision,
        retained_comparison=comparison,
        claim_boundary=claim_boundary,
    )


def authenticate_file(
    declaration: FileSourceDeclaration,
    reporter: HumanReadableProgressReporter,
) -> FileIdentity:
    """Authenticate one exact file and explain the check to the operator."""
    path = declaration.resolve()
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"source is absent, not a file, or a symlink: {path}")
    identity = identity_for_path(declaration.label, path)
    if identity.byte_size != declaration.byte_size:
        raise RuntimeError(
            f"source byte size differs for {declaration.label}: "
            f"{identity.byte_size} != {declaration.byte_size}"
        )
    if identity.sha256 != declaration.sha256:
        raise RuntimeError(
            f"source SHA-256 differs for {declaration.label}: {identity.sha256}"
        )
    reporter.line(
        f"  [OK] {declaration.label}: {identity.byte_size:,} bytes, "
        f"sha256 {identity.sha256[:12]}…"
    )
    return identity


def authenticate_provider(
    request: CommonSpaceDiagnosisRequest,
    reporter: HumanReadableProgressReporter,
) -> tuple[ProviderIdentity, ...]:
    """Authenticate the installed provider distribution and parser module sources."""
    observed_version = version(request.provider_distribution)
    if observed_version != request.provider_version:
        raise RuntimeError(
            f"provider version differs: {observed_version} != {request.provider_version}"
        )
    reporter.line(
        f"  [OK] provider distribution: {request.provider_distribution} "
        f"{observed_version}"
    )
    identities: list[ProviderIdentity] = []
    for declaration in request.provider_modules:
        module = importlib.import_module(declaration.module_name)
        source_name = getattr(module, "__file__", None)
        if type(source_name) is not str:
            raise RuntimeError(
                f"provider module has no source path: {declaration.module_name}"
            )
        path = Path(source_name).resolve()
        file_identity = identity_for_path(declaration.module_name, path)
        if file_identity.sha256 != declaration.sha256:
            raise RuntimeError(
                f"provider module SHA-256 differs for {declaration.module_name}: "
                f"{file_identity.sha256}"
            )
        identity = ProviderIdentity(
            module_name=declaration.module_name,
            path=str(path),
            byte_size=file_identity.byte_size,
            sha256=file_identity.sha256,
        )
        identities.append(identity)
        reporter.line(
            f"  [OK] {declaration.module_name}: sha256 {identity.sha256[:12]}…"
        )
    return tuple(identities)


def validate_retained_source_contract(
    *,
    request: CommonSpaceDiagnosisRequest,
    source_paths: dict[str, Path],
) -> None:
    """Match declared semantics and comparison values to authenticated retained JSON."""
    s30 = require_object(
        json.loads(
            source_paths["S30_untruncated_characterization"].read_text(encoding="utf-8")
        ),
        "S30 result",
    )
    if (
        require_string(s30.get("stage_id"), "S30 stage_id")
        != "S30-untruncated-characterization"
        or require_string(s30.get("status"), "S30 status")
        != "S30-untruncated-characterization-complete"
        or require_integer(s30.get("calculator_invocations"), "S30 calculators") != 0
        or s30.get("structural_reconstruction_verified") is not True
    ):
        raise RuntimeError("authenticated S30 semantic contract differs")

    s105 = require_object(
        json.loads(
            source_paths["S105_full_support_disposition"].read_text(encoding="utf-8")
        ),
        "S105 result",
    )
    s105_disposition = require_object(s105.get("disposition"), "S105 disposition")
    s105_oracle = require_object(s105.get("oracle_boundary"), "S105 oracle boundary")
    if (
        require_string(s105.get("stage_id"), "S105 stage_id")
        != "S105-spatial-truncation-disposition"
        or require_string(s105.get("status"), "S105 status")
        != "complete-full-support-retained-S110-definition-ready"
        or s105_disposition.get("H_T_equals_H_W") is not True
        or s105_disposition.get("spatial_truncation_applied") is not False
        or require_integer(
            s105_disposition.get("selected_representative_count"),
            "S105 selected representative count",
        )
        != 383
        or any(value is not False for value in s105_oracle.values())
    ):
        raise RuntimeError("authenticated S105 semantic contract differs")

    s110 = require_object(
        json.loads(source_paths["S110_blocked_result"].read_text(encoding="utf-8")),
        "S110 result",
    )
    fixed_source = require_object(s110.get("fixed_source"), "S110 fixed_source")
    model_definition = require_object(
        s110.get("provisional_model_definition"), "S110 model definition"
    )
    alignment_gate = require_object(s110.get("alignment_gate"), "S110 alignment gate")
    if (
        require_string(s110.get("stage_id"), "S110 stage_id")
        != "S110-slater-koster-definition-fit"
        or require_string(s110.get("status"), "S110 status")
        != "blocked-orbital-alignment-rank-deficient-no-fit"
        or require_integer(s110.get("calculator_invocations"), "S110 calculators") != 0
        or require_integer(s110.get("fit_invocations"), "S110 fits") != 0
        or require_integer(fixed_source.get("rank"), "S110 rank")
        != request.state_space.retained_rank
        or require_string(fixed_source.get("spin_convention"), "S110 spin convention")
        != request.state_space.spin_convention
        or require_string(fixed_source.get("energy_reference"), "S110 energy reference")
        != "unchanged native S30 Wannier reference in eV"
        or tuple(
            require_string(value, f"S110 orbital_order[{index}]")
            for index, value in enumerate(
                require_list(
                    model_definition.get("orbital_order"), "S110 orbital order"
                )
            )
        )
        != RETAINED_S110_BASIS_ORDER
        or request.state_space.basis_order != EXPECTED_BASIS_ORDER
        or require_integer(
            alignment_gate.get("AMN_native_decimal_places"),
            "S110 AMN precision",
        )
        != request.native_precision.amn_decimal_places
        or require_integer(
            alignment_gate.get("gauge_native_decimal_places"),
            "S110 gauge precision",
        )
        != request.native_precision.gauge_decimal_places
        or require_integer(
            alignment_gate.get("disentanglement_native_decimal_places"),
            "S110 disentanglement precision",
        )
        != request.native_precision.disentanglement_decimal_places
    ):
        raise RuntimeError("authenticated S110 state-space contract differs")

    deficient_payload = require_list(
        alignment_gate.get("deficient_kpoints"), "S110 deficient k-points"
    )
    retained_indices: list[int] = []
    retained_minima: list[float] = []
    for index, value in enumerate(deficient_payload):
        point = require_object(value, f"S110 deficient k-point[{index}]")
        retained_indices.append(
            require_integer(
                point.get("ordered_kpoint_index_zero_based"),
                f"S110 deficient k-point[{index}] index",
            )
        )
        retained_minima.append(
            require_float(
                point.get("minimum_singular_value"),
                f"S110 deficient k-point[{index}] minimum",
            )
        )
    gamma_payload = require_object(
        alignment_gate.get("gamma_null_direction_atomic_orbital_weights"),
        "S110 Gamma weights",
    )
    retained_gamma = tuple(
        (
            descriptive_label,
            require_float(
                gamma_payload.get(retained_label),
                f"S110 Gamma weight {retained_label}",
            ),
        )
        for retained_label, descriptive_label in zip(
            RETAINED_S110_BASIS_ORDER,
            EXPECTED_BASIS_ORDER,
            strict=True,
        )
    )
    if (
        tuple(retained_indices) != request.retained_comparison.deficient_indices
        or tuple(retained_minima) != request.retained_comparison.minimum_singular_values
        or require_float(
            alignment_gate.get("singular_value_native_uncertainty_bound"),
            "S110 native uncertainty bound",
        )
        != request.retained_comparison.native_uncertainty_bound
        or retained_gamma != request.retained_comparison.gamma_atomic_orbital_weights
    ):
        raise RuntimeError("request comparison values differ from authenticated S110")


def reconstruct_rank_gate(
    request: CommonSpaceDiagnosisRequest,
    reporter: HumanReadableProgressReporter,
) -> JsonObject:
    """Reconstruct the complete singular-value field without importing S110 code."""
    source_paths = {source.label: source.resolve() for source in request.file_sources}
    validate_retained_source_contract(request=request, source_paths=source_paths)
    reporter.line("  Authenticated S30, S105, and S110 semantic contracts matched")
    projections = Wannier90ProjectionParser().execute(source_paths["AMN"].read_bytes())
    gauge = Wannier90UnitaryMatrixParser().execute(source_paths["gauge"].read_bytes())
    disentanglement = Wannier90DisentanglementMatrixParser().execute(
        source_paths["disentanglement"].read_bytes()
    )
    state = request.state_space
    if (
        projections.kpoint_count != state.kpoint_count
        or projections.band_count != state.parent_band_count
        or projections.projection_count != state.retained_rank
        or gauge.kpoint_count != state.kpoint_count
        or gauge.wannier_count != state.retained_rank
        or disentanglement.kpoint_count != state.kpoint_count
        or disentanglement.band_count != state.parent_band_count
        or disentanglement.wannier_count != state.retained_rank
    ):
        raise RuntimeError(
            "parsed artifact dimensions differ from the frozen state space"
        )
    reporter.line(
        f"  Parsed dimensions: {state.kpoint_count} k-points, "
        f"{state.parent_band_count} parent bands, rank {state.retained_rank}"
    )

    kpoints = np.asarray(gauge.fractional_kpoints.magnitude, dtype=np.float64)
    disentanglement_kpoints = np.asarray(
        disentanglement.fractional_kpoints.magnitude, dtype=np.float64
    )
    expected_kpoints = gamma_grid(state.construction_grid_size_per_axis)
    if not np.allclose(kpoints, disentanglement_kpoints, atol=1.0e-12, rtol=0.0):
        raise RuntimeError("gauge and disentanglement k-point orders differ")
    if not np.allclose(kpoints, expected_kpoints, atol=1.0e-10, rtol=0.0):
        raise RuntimeError("artifacts do not use the declared Gamma-origin grid order")

    transform = atomic_to_projection_transform()
    if transform.shape != (state.retained_rank, state.retained_rank):
        raise RuntimeError("atomic-to-projection transformation dimension changed")
    unitarity_defect = float(
        np.max(np.abs(transform.conj().T @ transform - np.eye(state.retained_rank)))
    )
    if unitarity_defect != 0.0:
        raise RuntimeError("atomic-to-projection transformation is not exactly unitary")

    amn_matrices = tuple(
        np.asarray(value.magnitude, dtype=np.complex128)
        for value in projections.matrices
    )
    maximum_amn = max(float(np.max(np.abs(value))) for value in amn_matrices)
    native_bound = singular_value_uncertainty_bound(
        maximum_amn=maximum_amn,
        parent_band_count=state.parent_band_count,
        retained_rank=state.retained_rank,
        precision=request.native_precision,
    )
    retained_bound = request.retained_comparison.native_uncertainty_bound
    if abs(native_bound - retained_bound) > np.finfo(np.float64).eps:
        raise RuntimeError(
            f"native uncertainty bound differs: {native_bound} != {retained_bound}"
        )
    reporter.line(
        f"  Native-format singular-value uncertainty bound: {native_bound:.16e}"
    )
    reporter.line(
        "  Computing raw overlap singular values, normalized principal angles, and "
        "unitary-invariance controls…"
    )

    records: list[KPointDiagnosis] = []
    deficient: list[KPointDiagnosis] = []
    gamma_weights: tuple[tuple[str, float], ...] | None = None
    maximum_invariance_difference = 0.0
    for index in range(state.kpoint_count):
        u_dis = np.asarray(
            disentanglement.matrices[index].magnitude, dtype=np.complex128
        )
        u_matrix = np.asarray(gauge.matrices[index].magnitude, dtype=np.complex128)
        retained_frame = u_dis @ u_matrix
        atomic_trial_columns = amn_matrices[index] @ transform.conj().T
        overlap = retained_frame.conj().T @ atomic_trial_columns
        _left, singular_values, right_adjoint = np.linalg.svd(
            overlap, full_matrices=False
        )
        trial_left, trial_singular_values, _trial_right = np.linalg.svd(
            atomic_trial_columns, full_matrices=False
        )
        if float(trial_singular_values[-1]) <= 0.0:
            raise RuntimeError(
                f"atomic trial columns are rank deficient at index {index}"
            )
        retained_left, retained_singular_values, _retained_right = np.linalg.svd(
            retained_frame, full_matrices=False
        )
        if float(retained_singular_values[-1]) <= 0.0:
            raise RuntimeError(f"retained frame is rank deficient at index {index}")
        principal_cosines = np.linalg.svd(
            retained_left.conj().T @ trial_left,
            compute_uv=False,
        )
        minimum_principal_cosine = float(np.clip(principal_cosines[-1], 0.0, 1.0))
        maximum_principal_angle = float(np.arccos(minimum_principal_cosine))
        resolved_rank = int(np.count_nonzero(singular_values > native_bound))
        minimum = float(singular_values[-1])
        condition_number = (
            float(singular_values[0] / minimum) if minimum > 0.0 else None
        )
        record = KPointDiagnosis(
            ordered_index=index,
            fractional_coordinates=cast(
                tuple[float, float, float],
                tuple(float(value) for value in kpoints[index]),
            ),
            resolved_rank=resolved_rank,
            maximum_singular_value=float(singular_values[0]),
            next_to_minimum_singular_value=float(singular_values[-2]),
            minimum_singular_value=minimum,
            condition_number=condition_number,
            minimum_principal_cosine=minimum_principal_cosine,
            maximum_principal_angle_radians=maximum_principal_angle,
            full_rank_gate_passed=resolved_rank == state.retained_rank,
        )
        records.append(record)
        if not record.full_rank_gate_passed:
            deficient.append(record)
            reporter.line(
                f"  [BLOCKED POINT] index {index}, k={record.fractional_coordinates}, "
                f"rank {resolved_rank}/{state.retained_rank}, "
                f"sigma_min={minimum:.16e}"
            )
        if index == 0:
            null_vector = right_adjoint[-1].conj()
            gamma_weights = tuple(
                (label, float(abs(value) ** 2))
                for label, value in zip(state.basis_order, null_vector, strict=True)
            )

        phases = np.exp(
            1j
            * (index + 1)
            * np.arange(1, state.retained_rank + 1, dtype=np.float64)
            / 37.0
        )
        retained_basis_unitary = np.diag(phases.astype(np.complex128))
        rotated_singular_values = np.linalg.svd(
            retained_basis_unitary.conj().T @ overlap,
            compute_uv=False,
        )
        maximum_invariance_difference = max(
            maximum_invariance_difference,
            float(np.max(np.abs(rotated_singular_values - singular_values))),
        )
        completed = index + 1
        if completed % PROGRESS_INTERVAL == 0 or completed == state.kpoint_count:
            reporter.line(
                f"  Progress: {completed}/{state.kpoint_count} k-points analyzed"
            )

    if gamma_weights is None:
        raise RuntimeError("Gamma deficient-direction weights were not constructed")
    observed_indices = tuple(record.ordered_index for record in deficient)
    expected_indices = request.retained_comparison.deficient_indices
    if observed_indices != expected_indices:
        raise RuntimeError(
            f"deficient-point inventory differs: {observed_indices} != {expected_indices}"
        )
    for record, expected_minimum in zip(
        deficient,
        request.retained_comparison.minimum_singular_values,
        strict=True,
    ):
        if abs(record.minimum_singular_value - expected_minimum) > native_bound:
            raise RuntimeError(
                f"minimum singular value at index {record.ordered_index} differs beyond "
                "the native-format uncertainty bound"
            )
    retained_weights = dict(request.retained_comparison.gamma_atomic_orbital_weights)
    maximum_gamma_weight_difference = max(
        abs(value - retained_weights[label]) for label, value in gamma_weights
    )
    if maximum_gamma_weight_difference > native_bound:
        raise RuntimeError(
            "Gamma deficient-direction weights differ beyond the native-format bound"
        )
    invariance_tolerance = 64.0 * np.finfo(np.float64).eps * state.retained_rank
    if maximum_invariance_difference > invariance_tolerance:
        raise RuntimeError(
            "retained-subspace unitary basis change altered overlap singular values"
        )

    gamma_weight_mapping = {label: value for label, value in gamma_weights}
    combined_s = (
        gamma_weight_mapping["diamond_origin_center:s"]
        + gamma_weight_mapping["diamond_body_diagonal_quarter_center:s"]
    )
    combined_s_star = (
        gamma_weight_mapping["diamond_origin_center:s-star"]
        + gamma_weight_mapping["diamond_body_diagonal_quarter_center:s-star"]
    )
    reporter.line(
        f"  Gamma unresolved direction: {100.0 * combined_s_star:.3f}% combined s*, "
        f"{100.0 * combined_s:.3f}% combined s"
    )
    reporter.line(
        "  Scientific gate: BLOCKED — a unitary rank-10 common-space map is not "
        "defined under the declared contract"
    )

    return {
        "outcome": "rank-deficiency-reproduced",
        "producer_scope": "projector-rank-reconstruction-subset",
        "unimplemented_CSD1_extensions": [
            "separately implemented independent verification",
            "higher-precision sensitivity using the same retained decimal data",
            "symmetry-related deficient-point inventory",
        ],
        "scientific_disposition": "blocked-orbital-alignment-rank-deficient-no-fit",
        "formula": (
            "B(k) = [U_dis(k) U(k)]^dagger A(k) T^dagger; rank is resolved against "
            "the conservative native-format singular-value uncertainty bound"
        ),
        "state_space": {
            "construction_grid_size_per_axis": state.construction_grid_size_per_axis,
            "kpoint_count": state.kpoint_count,
            "parent_band_count": state.parent_band_count,
            "retained_rank": state.retained_rank,
            "basis_order": list(state.basis_order),
            "geometry": state.geometry,
            "spin_convention": state.spin_convention,
            "operator_units": state.operator_units,
            "energy_reference": state.energy_reference,
        },
        "maximum_native_AMN_absolute_value": maximum_amn,
        "singular_value_native_uncertainty_bound": native_bound,
        "deficient_kpoint_count": len(deficient),
        "deficient_kpoints": [record.to_json() for record in deficient],
        "gamma_null_direction_atomic_orbital_weights": cast(
            JsonObject, gamma_weight_mapping
        ),
        "gamma_combined_orbital_weights": {
            "s": combined_s,
            "s-star": combined_s_star,
            "p": 1.0 - combined_s - combined_s_star,
        },
        "complete_kpoint_diagnostics": [record.to_json() for record in records],
        "retained_result_reproduction": {
            "deficient_indices_match": True,
            "minimum_singular_values_within_native_uncertainty_bound": True,
            "gamma_weights_within_native_uncertainty_bound": True,
            "maximum_gamma_weight_absolute_difference": (
                maximum_gamma_weight_difference
            ),
        },
        "unitary_basis_invariance_control": {
            "scope": (
                "diagnostic-only momentum-point-dependent unitary basis changes within "
                "the retained rank-10 subspace; not a candidate pointwise model "
                "alignment Q(k)"
            ),
            "maximum_singular_value_absolute_difference": (
                maximum_invariance_difference
            ),
            "tolerance": invariance_tolerance,
            "passed": True,
            "interpretation": (
                "energy-degenerate retained eigenvectors may be unitarily mixed without "
                "changing these singular values; degeneracy is therefore not established "
                "as the cause of the rank loss"
            ),
        },
        "principal_angle_note": (
            "Principal angles are computed only after independently orthonormalizing "
            "both represented ten-column frames. Raw B(k) singular values remain the frozen gate "
            "because unnormalized AMN columns are not principal-angle cosines."
        ),
        "fit_invoked": False,
        "calculator_invocations": 0,
        "next_stage": (
            "CSD2 must authenticate parent-space symmetry actions or record "
            "INSUFFICIENT_RETAINED_SYMMETRY_DATA"
        ),
    }


def atomic_to_projection_transform() -> ComplexArray:
    """Return the exact two-site atomic-to-eight-hybrid-plus-two-s transformation."""
    transform = np.zeros((10, 10), dtype=np.complex128)
    hybrids = 0.5 * np.asarray(
        (
            (1.0, 1.0, 1.0, 1.0),
            (1.0, 1.0, -1.0, -1.0),
            (1.0, -1.0, 1.0, -1.0),
            (1.0, -1.0, -1.0, 1.0),
        ),
        dtype=np.complex128,
    )
    transform[0:4, 0:4] = hybrids
    transform[5:9, 4:8] = hybrids
    transform[4, 8] = 1.0
    transform[9, 9] = 1.0
    transform.setflags(write=False)
    return transform


def singular_value_uncertainty_bound(
    *,
    maximum_amn: float,
    parent_band_count: int,
    retained_rank: int,
    precision: NativePrecisionDefinition,
) -> float:
    """Bound overlap singular-value perturbations from declared native precision."""
    if type(maximum_amn) not in {int, float} or not np.isfinite(maximum_amn):
        raise ValueError("maximum_amn must be a finite real number")
    if maximum_amn < 0.0:
        raise ValueError("maximum_amn must be nonnegative")
    if type(parent_band_count) is not int or parent_band_count <= 0:
        raise ValueError("parent_band_count must be a positive integer")
    if type(retained_rank) is not int or retained_rank <= 0:
        raise ValueError("retained_rank must be a positive integer")
    gauge_rounding = 0.5 * 10.0 ** (-precision.gauge_decimal_places)
    disentanglement_rounding = 0.5 * 10.0 ** (-precision.disentanglement_decimal_places)
    amn_rounding = 0.5 * 10.0 ** (-precision.amn_decimal_places)
    composite_element_bound = retained_rank * (
        gauge_rounding
        + disentanglement_rounding
        + gauge_rounding * disentanglement_rounding
    )
    projected_element_bound = parent_band_count * (
        maximum_amn * composite_element_bound
        + amn_rounding * (1.0 + composite_element_bound)
    )
    return retained_rank * projected_element_bound


def gamma_grid(size: int) -> FloatArray:
    """Return the lexicographic Gamma-origin cubic fractional grid."""
    if type(size) is not int or size <= 0:
        raise ValueError("grid size must be a positive integer")
    values = np.arange(size, dtype=np.float64) / float(size)
    return np.asarray(
        tuple(
            (first, second, third)
            for first in values
            for second in values
            for third in values
        ),
        dtype=np.float64,
    )


def identity_for_path(label: str, path: Path) -> FileIdentity:
    """Return one local file identity."""
    content = path.read_bytes()
    return FileIdentity(
        label=label,
        path=str(path),
        byte_size=len(content),
        sha256=hashlib.sha256(content).hexdigest(),
    )


def build_manifest(
    *, request_path: Path, result_bytes: bytes, summary_bytes: bytes
) -> JsonObject:
    """Build one deterministic artifact manifest."""
    implementation = Path(__file__).resolve()
    cli = DEFAULT_ENTRYPOINT
    return {
        "schema_version": 1,
        "record_type": "c6_b20_w21_common_space_rank_diagnosis_manifest",
        "artifacts": [
            artifact_record(RESULT_NAME, result_bytes),
            artifact_record(SUMMARY_NAME, summary_bytes),
            identity_for_path("request", request_path).to_json(),
            identity_for_path("implementation", implementation).to_json(),
            identity_for_path("entrypoint", cli).to_json(),
        ],
    }


def artifact_record(path: str, content: bytes) -> JsonObject:
    """Return one identity record for bytes not yet written."""
    return {
        "path": path,
        "byte_size": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def canonical_json(payload: JsonObject) -> bytes:
    """Encode one deterministic JSON object."""
    return (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def write_exclusive(path: Path, content: bytes) -> None:
    """Create one artifact without replacing retained bytes."""
    with path.open("xb") as stream:
        stream.write(content)


def require_object(value: JsonValue, name: str) -> JsonObject:
    """Return one exact JSON object."""
    if type(value) is not dict:
        raise ValueError(f"{name} must be an object")
    return value


def require_list(value: JsonValue, name: str) -> list[JsonValue]:
    """Return one exact JSON array."""
    if type(value) is not list:
        raise ValueError(f"{name} must be an array")
    return value


def require_string(value: JsonValue, name: str) -> str:
    """Return one nonempty JSON string."""
    if type(value) is not str or not value:
        raise ValueError(f"{name} must be a nonempty string")
    return value


def require_integer(value: JsonValue, name: str) -> int:
    """Return one JSON integer without admitting booleans."""
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    return value


def require_float(value: JsonValue, name: str) -> float:
    """Return one finite JSON real number without admitting booleans."""
    if type(value) not in {int, float}:
        raise ValueError(f"{name} must be a real number")
    result = float(cast(int | float, value))
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def require_sha256(value: JsonValue, name: str) -> str:
    """Return one lowercase SHA-256 hexadecimal digest."""
    result = require_string(value, name)
    if len(result) != 64 or any(
        character not in "0123456789abcdef" for character in result
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")
    return result
