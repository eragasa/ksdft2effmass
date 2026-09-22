"""Immutable records and closed value types for accepted-parent Stage C."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type ComplexMatrix = npt.NDArray[np.complex128]
type FloatPair = tuple[float, float]
type IntPair = tuple[int, int]
type IntMatrix2 = tuple[tuple[int, int], tuple[int, int]]
type MatrixKey = tuple[str, str]


@dataclass(frozen=True, slots=True)
class ParentHopping:
    """Represent one compact scalar-parent hopping coefficient."""

    displacement: IntPair
    value: complex

    def __post_init__(self) -> None:
        if not np.isfinite(self.value.real) or not np.isfinite(self.value.imag):
            raise ValueError("hopping value must be finite")


@dataclass(frozen=True, slots=True)
class LocalBond:
    """Represent one localized real bond change before its Hermitian reverse."""

    start: IntPair
    displacement: IntPair
    value: float

    def __post_init__(self) -> None:
        if self.displacement == (0, 0):
            raise ValueError("localized bond displacement must be nonzero")
        if not np.isfinite(self.value):
            raise ValueError("localized bond value must be finite")


@dataclass(frozen=True, slots=True)
class PointOperation:
    """Represent one exact integer point operation."""

    identifier: str
    matrix: IntMatrix2


@dataclass(frozen=True, slots=True)
class ParentFixture:
    """Own immutable authored parent data used by execution-free behavior."""

    isotropic_hoppings: tuple[ParentHopping, ...]
    anisotropic_energies: tuple[tuple[float, ...], ...]
    reciprocal_mesh_size: int
    hopping_maximum_squared_radius: int
    fixture_sha256: str


@dataclass(frozen=True, slots=True)
class ArtifactBinding:
    """Bind one exact repository artifact role, path, and SHA-256 identity."""

    role: str
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class StageCAcceptedParentExecutionAuthorization:
    """Represent one future exact protected-execution authorization."""

    authorization_id: str
    checkpoint_path: str
    checkpoint_sha256: str
    human_response_verbatim: str
    repository_root: str
    repository_revision: str
    machine_identity: str
    native_artifact_root: str
    artifacts: tuple[ArtifactBinding, ...]
    operation_inventory: tuple[str, ...]
    attempt_record_path: str
    result_path: str
    verification_log_path: str
    summary_svg_path: str
    report_path: str
    native_evidence_manifest_path: str
    checksum_catalog_path: str
    maximum_matrix_dimension: int
    maximum_execution_schedules: int
    maximum_route_evaluations: int
    maximum_bridge_records: int
    maximum_model_fit_records: int
    maximum_schedule_comparisons: int
    maximum_runtime_seconds: int
    maximum_peak_memory_gib: float
    maximum_retained_output_mib: float
    network_access: bool
    external_executables: tuple[str, ...]
    new_dependencies: tuple[str, ...]
    maximum_attempts: int
    retry_authorized: bool
    overwrite_existing: bool


@dataclass(frozen=True, slots=True)
class StageCResultContext:
    """Own exact claim, authority, source, and resource result metadata."""

    result_id: str
    evidence_status: str
    accepted_parent_read: bool
    source_mode: str
    operation_inventory: tuple[str, ...]
    input_identities: tuple[ArtifactBinding, ...]
    authorization_id: str | None
    authorization_path: str | None
    authorization_sha256: str | None
    checkpoint_path: str | None
    checkpoint_sha256: str | None
    human_response_verbatim: str | None
    repository_root: str | None
    repository_revision: str
    machine_identity: str | None
    native_artifact_root: str
    attempt_record_path: str
    result_path: str
    verification_log_path: str
    summary_svg_path: str
    report_path: str
    native_evidence_manifest_path: str
    checksum_catalog_path: str
    maximum_runtime_seconds: int
    maximum_peak_memory_gib: float
    maximum_retained_output_mib: float
    maximum_attempts: int
    retry_authorized: bool
    overwrite_existing: bool
    started_at: float | None


@dataclass(frozen=True, slots=True)
class ParentControls:
    """Own the adopted Stage C dimensions, inventories, and criteria."""

    nx: int
    ny: int
    twists: tuple[FloatPair, FloatPair]
    model_classes: tuple[str, ...]
    d4: tuple[PointOperation, ...]
    d2: tuple[PointOperation, ...]
    axis_swap: PointOperation
    defects: tuple[tuple[str, tuple[LocalBond, ...], str], ...]
    route_evaluations: int
    bridge_records: int
    model_fit_records: int
    schedule_comparisons: int
    criteria: dict[str, float]

    @property
    def dimension(self) -> int:
        """Return the exact represented dimension."""

        return self.nx * self.ny


@dataclass(frozen=True, slots=True)
class ParentCase:
    """Own one frozen parent, defect, twist, and orientation case."""

    case_id: str
    parent_family: str
    source_parent_id: str
    target_parent_id: str
    defect_id: str
    source_terms: tuple[LocalBond, ...]
    expected_model_class: str
    twist_id: str
    base_twist: FloatPair
    operation: PointOperation


@dataclass(frozen=True, slots=True)
class ParentScheduleResult:
    """Carry one fresh schedule as immutable JSON and matrix bytes."""

    schedule_id: str
    process_id: int
    payload_json: str
    recovered_matrices: tuple[tuple[MatrixKey, bytes], ...]
