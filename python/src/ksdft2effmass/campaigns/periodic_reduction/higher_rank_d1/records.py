"""Immutable scalar records for the schema-free higher-rank D1 calculation."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    MatrixErrorDecompositionDiagnostics,
    MatrixFieldComparisonDiagnostics,
    MatrixFieldHermiticityDiagnostics,
    MatrixFieldIsometryDiagnostics,
    MatrixProjectorFieldDiagnostics,
    ScalarRefinementDiagnostics,
)

from ._validation import (
    require_exact_instance,
    require_exact_tuple,
    require_nonnegative_float,
)
from .alignment import (
    HigherRankD1A1NumericallyUnresolvedSelection,
    HigherRankD1A1QualifiedSelection,
    HigherRankD1A1RankDeficientSelection,
    HigherRankD1A1Selection,
    HigherRankD1A2NumericallyUnresolvedSelection,
    HigherRankD1A2RankDeficientSelection,
    HigherRankD1A2Selection,
    HigherRankD1A2SelectionResult,
)
from .definition import (
    CHANNELS,
    CONSTRUCTION_MESH_SIZES,
    DEPTHS,
    EVALUATION_MESH_SIZE,
    EXACT_ISOLATION,
    FINAL_CONSTRUCTION_MESH_SIZE,
    RANKS,
    SUPPORTS,
)
from .transport import (
    HigherRankD1TransportClosureRankDeficientDiagnostics,
    HigherRankD1TransportDiagnostics,
    HigherRankD1TransportLinkRankDeficientDiagnostics,
    HigherRankD1TransportNumericallyUnresolvedDiagnostics,
    HigherRankD1TransportResult,
)


@dataclass(frozen=True, slots=True)
class HigherRankD1Gate:
    """Retain one inclusive qualification comparison."""

    path: str
    value: float
    tolerance: float
    passes: bool

    @classmethod
    def evaluate(cls, path: str, value: float, tolerance: float) -> Self:
        """Construct one gate from its inclusive comparison."""
        return cls(path, value, tolerance, value <= tolerance)

    def __post_init__(self) -> None:
        if type(self.path) is not str or not self.path.startswith("/"):
            raise ValueError("path must be a nonempty JSON-Pointer-like string")
        require_nonnegative_float(self.value, "value")
        require_nonnegative_float(self.tolerance, "tolerance")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        if self.passes is not (self.value <= self.tolerance):
            raise ValueError("passes must match the inclusive comparison")


@dataclass(frozen=True, slots=True)
class HigherRankD1ScalarLedgerEntry:
    """Bind one stable diagnostic path to one finite nonnegative scalar."""

    path: str
    value: float

    def __post_init__(self) -> None:
        if type(self.path) is not str or not self.path.startswith("/"):
            raise ValueError("path must be a JSON-Pointer-like string")
        require_nonnegative_float(self.value, "value")


@dataclass(frozen=True, slots=True)
class HigherRankD1ScalarLedger:
    """Retain one ordered, unique collection of named D1 scalar diagnostics."""

    entries: tuple[HigherRankD1ScalarLedgerEntry, ...]

    def __post_init__(self) -> None:
        require_exact_tuple(
            self.entries, HigherRankD1ScalarLedgerEntry, "entries"
        )
        if not self.entries:
            raise ValueError("entries must be nonempty")
        paths = self.paths
        if len(set(paths)) != len(paths):
            raise ValueError("scalar ledger paths must be unique")

    @property
    def paths(self) -> tuple[str, ...]:
        """Return paths in their retained deterministic order."""
        return tuple(entry.path for entry in self.entries)

    def value(self, path: str) -> float:
        """Return the scalar bound to one exact retained path."""
        if type(path) is not str or not path.startswith("/"):
            raise ValueError("path must be a JSON-Pointer-like string")
        for entry in self.entries:
            if entry.path == path:
                return entry.value
        raise KeyError(path)

    def with_prefix(self, prefix: str) -> HigherRankD1ScalarLedger:
        """Return a new ledger with one validated prefix prepended to every path."""
        if type(prefix) is not str or not prefix.startswith("/"):
            raise ValueError("prefix must be a JSON-Pointer-like string")
        return HigherRankD1ScalarLedger(
            tuple(
                HigherRankD1ScalarLedgerEntry(f"{prefix}{entry.path}", entry.value)
                for entry in self.entries
            )
        )


@dataclass(frozen=True, slots=True)
class HigherRankD1ResidualSummary:
    """Retain maximum/RMS Frobenius residuals and rank normalization."""

    maximum: float
    rms: float
    normalized_maximum: float
    normalized_rms: float
    normalization: float

    def __post_init__(self) -> None:
        for name in (
            "maximum",
            "rms",
            "normalized_maximum",
            "normalized_rms",
            "normalization",
        ):
            require_nonnegative_float(getattr(self, name), name)
        if self.normalization <= 0.0:
            raise ValueError("normalization must be positive")
        if self.normalized_maximum != self.maximum / self.normalization:
            raise ValueError("normalized_maximum is inconsistent")
        if self.normalized_rms != self.rms / self.normalization:
            raise ValueError("normalized_rms is inconsistent")


@dataclass(frozen=True, slots=True)
class HigherRankD1FourierDiagnostics:
    """Retain complete-transform identities without retaining coefficient tensors."""

    representative_count: int
    representative_inventory_ordered_unique: bool
    inversion_closed: bool
    index_bijection_passes: bool
    no_nyquist_disposition: str
    normalized_reconstruction_defect: float
    normalized_hermitian_pairing_defect: float
    sample_mean_squared_frobenius_norm: float
    coefficient_sum_squared_frobenius_norm: float
    relative_parseval_defect: float
    gates: tuple[HigherRankD1Gate, ...]

    def __post_init__(self) -> None:
        if type(self.representative_count) is not int or self.representative_count <= 0:
            raise ValueError("representative_count must be a positive built-in int")
        for name in (
            "representative_inventory_ordered_unique",
            "inversion_closed",
            "index_bijection_passes",
        ):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f"{name} must be a built-in bool")
        if self.no_nyquist_disposition != "inapplicable-odd-centered-no-nyquist":
            raise ValueError("no_nyquist_disposition is invalid")
        for name in (
            "normalized_reconstruction_defect",
            "normalized_hermitian_pairing_defect",
            "sample_mean_squared_frobenius_norm",
            "coefficient_sum_squared_frobenius_norm",
            "relative_parseval_defect",
        ):
            require_nonnegative_float(getattr(self, name), name)
        require_exact_tuple(self.gates, HigherRankD1Gate, "gates")


@dataclass(frozen=True, slots=True)
class HigherRankD1BlockNorm:
    """Retain one bounded Fourier block norm without retaining its matrix."""

    translation: int
    raw_frobenius_norm: float
    normalized_frobenius_norm: float

    def __post_init__(self) -> None:
        if type(self.translation) is not int:
            raise TypeError("translation must be a built-in int")
        require_nonnegative_float(self.raw_frobenius_norm, "raw_frobenius_norm")
        require_nonnegative_float(
            self.normalized_frobenius_norm, "normalized_frobenius_norm"
        )


@dataclass(frozen=True, slots=True)
class HigherRankD1TailDiagnostics:
    """Retain raw and normalized complete-matrix omitted Fourier weights."""

    squared_weight: float
    l2_norm: float
    block_l1_norm: float
    normalized_squared_weight: float
    normalized_l2_norm: float
    normalized_block_l1_norm: float

    def __post_init__(self) -> None:
        for name in (
            "squared_weight",
            "l2_norm",
            "block_l1_norm",
            "normalized_squared_weight",
            "normalized_l2_norm",
            "normalized_block_l1_norm",
        ):
            require_nonnegative_float(getattr(self, name), name)
        if self.l2_norm != math.sqrt(self.squared_weight):
            raise ValueError("l2_norm must be the square root of squared_weight")


@dataclass(frozen=True, slots=True)
class HigherRankD1SupportMonotonicity:
    """Retain one preceding-support increase check."""

    preceding_support: int
    normalized_squared_weight_increase: float
    normalized_l2_norm_increase: float
    normalized_l1_norm_increase: float
    passes: bool

    def __post_init__(self) -> None:
        if type(self.preceding_support) is not int or self.preceding_support < 0:
            raise ValueError("preceding_support must be a nonnegative built-in int")
        for name in (
            "normalized_squared_weight_increase",
            "normalized_l2_norm_increase",
            "normalized_l1_norm_increase",
        ):
            require_nonnegative_float(getattr(self, name), name)
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")


@dataclass(frozen=True, slots=True)
class HigherRankD1SupportDiagnostics:
    """Retain all locality and error channels for one explicit symmetric support."""

    support: int
    translations: tuple[int, ...]
    tail: HigherRankD1TailDiagnostics
    monotonicity: tuple[HigherRankD1SupportMonotonicity, ...]
    sample_parseval_left: float
    sample_parseval_right: float
    relative_parseval_defect: float
    truncation: MatrixFieldComparisonDiagnostics
    total: MatrixFieldComparisonDiagnostics
    decomposition: MatrixErrorDecompositionDiagnostics
    gates: tuple[HigherRankD1Gate, ...]

    def __post_init__(self) -> None:
        if type(self.support) is not int or self.support not in SUPPORTS:
            raise ValueError("support must belong to the D1 inventory")
        expected = tuple(range(-self.support, self.support + 1))
        if self.translations != expected:
            raise ValueError("translations must equal the explicit symmetric support")
        if type(self.tail) is not HigherRankD1TailDiagnostics:
            raise TypeError("tail must be HigherRankD1TailDiagnostics")
        require_exact_tuple(
            self.monotonicity,
            HigherRankD1SupportMonotonicity,
            "monotonicity",
        )
        for name in (
            "sample_parseval_left",
            "sample_parseval_right",
            "relative_parseval_defect",
        ):
            require_nonnegative_float(getattr(self, name), name)
        if type(self.truncation) is not MatrixFieldComparisonDiagnostics:
            raise TypeError("truncation must be MatrixFieldComparisonDiagnostics")
        if type(self.total) is not MatrixFieldComparisonDiagnostics:
            raise TypeError("total must be MatrixFieldComparisonDiagnostics")
        if type(self.decomposition) is not MatrixErrorDecompositionDiagnostics:
            raise TypeError("decomposition must be MatrixErrorDecompositionDiagnostics")
        require_exact_tuple(self.gates, HigherRankD1Gate, "gates")


@dataclass(frozen=True, slots=True)
class HigherRankD1ParetoPoint:
    """Retain one final-mesh support--error objective and nondominance flag."""

    support: int
    retained_block_count: int
    normalized_total_operator_error: float
    normalized_total_spectrum_error: float
    pareto_efficient: bool

    def __post_init__(self) -> None:
        if type(self.support) is not int or self.support not in SUPPORTS:
            raise ValueError("support must belong to the D1 inventory")
        if type(self.retained_block_count) is not int:
            raise TypeError("retained_block_count must be a built-in int")
        if self.retained_block_count != 2 * self.support + 1:
            raise ValueError("retained_block_count is inconsistent")
        require_nonnegative_float(
            self.normalized_total_operator_error,
            "normalized_total_operator_error",
        )
        require_nonnegative_float(
            self.normalized_total_spectrum_error,
            "normalized_total_spectrum_error",
        )
        if type(self.pareto_efficient) is not bool:
            raise TypeError("pareto_efficient must be a built-in bool")


@dataclass(frozen=True, slots=True)
class HigherRankD1ChannelMeshDiagnostics:
    """Retain every applicable diagnostic for one mesh and alignment channel."""

    channel: str
    mesh_size: int
    alignment_status: str
    downstream_applicability: str
    frame_residual: HigherRankD1ResidualSummary
    projector_residual: HigherRankD1ResidualSummary
    represented_operator: MatrixFieldComparisonDiagnostics
    represented_hermiticity: MatrixFieldHermiticityDiagnostics
    fourier: HigherRankD1FourierDiagnostics
    block_norms: tuple[HigherRankD1BlockNorm, ...]
    interpolation: MatrixFieldComparisonDiagnostics
    supports: tuple[HigherRankD1SupportDiagnostics, ...]
    pareto_role: str
    pareto_points: tuple[HigherRankD1ParetoPoint, ...]
    scalar_ledger: HigherRankD1ScalarLedger
    gates: tuple[HigherRankD1Gate, ...]

    def __post_init__(self) -> None:
        if type(self.channel) is not str:
            raise TypeError("channel must be a built-in str")
        if self.channel not in CHANNELS:
            raise ValueError("channel must belong to the D1 inventory")
        if type(self.mesh_size) is not int:
            raise TypeError("mesh_size must be a built-in int")
        if self.mesh_size not in CONSTRUCTION_MESH_SIZES:
            raise ValueError("mesh_size must belong to the D1 inventory")
        if type(self.alignment_status) is not str:
            raise TypeError("alignment_status must be a built-in str")
        if type(self.downstream_applicability) is not str:
            raise TypeError("downstream_applicability must be a built-in str")
        if self.downstream_applicability != "applicable":
            raise ValueError("this qualified record must be applicable")
        if self.alignment_status != "qualified":
            raise ValueError("alignment_status must be qualified")
        if type(self.frame_residual) is not HigherRankD1ResidualSummary:
            raise TypeError("frame_residual must be HigherRankD1ResidualSummary")
        if type(self.projector_residual) is not HigherRankD1ResidualSummary:
            raise TypeError("projector_residual must be HigherRankD1ResidualSummary")
        if type(self.represented_operator) is not MatrixFieldComparisonDiagnostics:
            raise TypeError(
                "represented_operator must be MatrixFieldComparisonDiagnostics"
            )
        if type(self.represented_hermiticity) is not MatrixFieldHermiticityDiagnostics:
            raise TypeError(
                "represented_hermiticity must be MatrixFieldHermiticityDiagnostics"
            )
        if type(self.fourier) is not HigherRankD1FourierDiagnostics:
            raise TypeError("fourier must be HigherRankD1FourierDiagnostics")
        require_exact_tuple(self.block_norms, HigherRankD1BlockNorm, "block_norms")
        if type(self.interpolation) is not MatrixFieldComparisonDiagnostics:
            raise TypeError("interpolation must be MatrixFieldComparisonDiagnostics")
        if type(self.pareto_role) is not str:
            raise TypeError("pareto_role must be a built-in str")
        if self.pareto_role not in (
            "primary-outcome",
            "control-only",
            "not-final-mesh",
            "inapplicable-technical-qualification",
        ):
            raise ValueError("pareto_role is invalid")
        require_exact_tuple(self.supports, HigherRankD1SupportDiagnostics, "supports")
        if len(self.supports) != len(SUPPORTS):
            raise ValueError("supports must cover the complete D1 inventory")
        if tuple(item.support for item in self.supports) != SUPPORTS:
            raise ValueError("support order is invalid")
        require_exact_tuple(
            self.pareto_points, HigherRankD1ParetoPoint, "pareto_points"
        )
        if self.mesh_size == CONSTRUCTION_MESH_SIZES[-1]:
            if self.pareto_points and len(self.pareto_points) != len(SUPPORTS):
                raise ValueError("applicable final-mesh Pareto points must be complete")
            if not self.pareto_points and self.pareto_role != (
                "inapplicable-technical-qualification"
            ):
                raise ValueError(
                    "omitted final-mesh Pareto points require a disposition"
                )
        elif self.pareto_points:
            raise ValueError("nonfinal meshes cannot retain Pareto points")
        if type(self.scalar_ledger) is not HigherRankD1ScalarLedger:
            raise TypeError("scalar_ledger must be HigherRankD1ScalarLedger")
        require_exact_tuple(self.gates, HigherRankD1Gate, "gates")


@dataclass(frozen=True, slots=True)
class HigherRankD1InapplicableChannelMeshDiagnostics:
    """Retain a bounded alignment disposition without unavailable numerics."""

    mesh_size: int
    channel: str
    alignment_status: str
    downstream_applicability: str

    def __post_init__(self) -> None:
        for name in ("channel", "alignment_status", "downstream_applicability"):
            if type(getattr(self, name)) is not str:
                raise TypeError(f"{name} must be a built-in str")
        if type(self.mesh_size) is not int:
            raise TypeError("mesh_size must be a built-in int")
        if self.mesh_size not in CONSTRUCTION_MESH_SIZES:
            raise ValueError("mesh_size must belong to the D1 inventory")
        allowed = (
            (
                "A1",
                "aggregate-rank-deficient",
                "inapplicable-aggregate-rank-deficient",
            ),
            (
                "A1",
                "alignment-numerically-unresolved",
                "inapplicable-alignment-numerically-unresolved",
            ),
            (
                "A2",
                "pointwise-rank-deficient",
                "inapplicable-pointwise-rank-deficient",
            ),
            (
                "A2",
                "alignment-numerically-unresolved",
                "inapplicable-alignment-numerically-unresolved",
            ),
        )
        if (
            self.channel,
            self.alignment_status,
            self.downstream_applicability,
        ) not in allowed:
            raise ValueError("inapplicable alignment disposition is invalid")


type HigherRankD1ChannelMeshRecord = (
    HigherRankD1ChannelMeshDiagnostics | HigherRankD1InapplicableChannelMeshDiagnostics
)


@dataclass(frozen=True, slots=True)
class HigherRankD1MeshDiagnostics:
    """Retain qualification, transport, alignment, and channels for one mesh."""

    mesh_size: int
    sampled_isolation: float
    sampled_attack_angle: float
    coordinate_maximum_defect: float
    parent_hermiticity: MatrixFieldHermiticityDiagnostics
    reference_isometry: MatrixFieldIsometryDiagnostics
    candidate_isometry: MatrixFieldIsometryDiagnostics
    gauge_isometry: MatrixFieldIsometryDiagnostics
    reference_projector: MatrixProjectorFieldDiagnostics
    candidate_projector: MatrixProjectorFieldDiagnostics
    projector_equality: HigherRankD1ResidualSummary
    parent_retained_spectrum_maximum: float
    parent_retained_spectrum_rms: float
    transport: HigherRankD1TransportResult
    a2_selection: HigherRankD1A2SelectionResult
    channels: tuple[HigherRankD1ChannelMeshRecord, ...]
    gates: tuple[HigherRankD1Gate, ...]

    def __post_init__(self) -> None:
        if type(self.mesh_size) is not int:
            raise TypeError("mesh_size must be a built-in int")
        if self.mesh_size not in CONSTRUCTION_MESH_SIZES:
            raise ValueError("mesh_size must belong to the D1 inventory")
        for name in (
            "sampled_isolation",
            "sampled_attack_angle",
            "coordinate_maximum_defect",
            "parent_retained_spectrum_maximum",
            "parent_retained_spectrum_rms",
        ):
            require_nonnegative_float(getattr(self, name), name)
        require_exact_instance(
            self.parent_hermiticity,
            MatrixFieldHermiticityDiagnostics,
            "parent_hermiticity",
        )
        require_exact_instance(
            self.reference_isometry,
            MatrixFieldIsometryDiagnostics,
            "reference_isometry",
        )
        require_exact_instance(
            self.candidate_isometry,
            MatrixFieldIsometryDiagnostics,
            "candidate_isometry",
        )
        require_exact_instance(
            self.gauge_isometry,
            MatrixFieldIsometryDiagnostics,
            "gauge_isometry",
        )
        require_exact_instance(
            self.reference_projector,
            MatrixProjectorFieldDiagnostics,
            "reference_projector",
        )
        require_exact_instance(
            self.candidate_projector,
            MatrixProjectorFieldDiagnostics,
            "candidate_projector",
        )
        require_exact_instance(
            self.projector_equality,
            HigherRankD1ResidualSummary,
            "projector_equality",
        )
        if not isinstance(
            self.transport,
            (
                HigherRankD1TransportDiagnostics,
                HigherRankD1TransportLinkRankDeficientDiagnostics,
                HigherRankD1TransportClosureRankDeficientDiagnostics,
                HigherRankD1TransportNumericallyUnresolvedDiagnostics,
            ),
        ):
            raise TypeError("transport has an invalid record type")
        if not isinstance(
            self.a2_selection,
            (
                HigherRankD1A2Selection,
                HigherRankD1A2RankDeficientSelection,
                HigherRankD1A2NumericallyUnresolvedSelection,
            ),
        ):
            raise TypeError("a2_selection has an invalid record type")
        if self.transport.mesh_size != self.mesh_size:
            raise ValueError("transport mesh_size must match the mesh record")
        if self.a2_selection.mesh_size != self.mesh_size:
            raise ValueError("A2 mesh_size must match the mesh record")
        if type(self.channels) is not tuple or any(
            not isinstance(
                channel,
                (
                    HigherRankD1ChannelMeshDiagnostics,
                    HigherRankD1InapplicableChannelMeshDiagnostics,
                ),
            )
            for channel in self.channels
        ):
            raise TypeError("channels contain an invalid record type")
        if tuple(channel.channel for channel in self.channels) != CHANNELS:
            raise ValueError("channels must follow the D1 order")
        require_exact_tuple(self.gates, HigherRankD1Gate, "gates")


@dataclass(frozen=True, slots=True)
class HigherRankD1RefinementRecord:
    """Bind one named mandatory scalar to its frozen refinement comparison."""

    path: str
    diagnostics: ScalarRefinementDiagnostics

    def __post_init__(self) -> None:
        if type(self.path) is not str or not self.path.startswith("/"):
            raise ValueError("path must be a JSON-Pointer-like string")
        if type(self.diagnostics) is not ScalarRefinementDiagnostics:
            raise TypeError("diagnostics must be ScalarRefinementDiagnostics")


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankD1CaseResult:
    """Retain one complete schema-free rank/depth result without mesh tensors."""

    case_id: str
    rank: int
    depth: int
    exact_isolation: float
    exact_attack_angle_bound: float
    basis_identifier: str
    energy_unit: str
    energy_reference: str
    evaluation_mesh_size: int
    construction_evaluation_disjoint: bool
    evaluation_noninfluence_confirmed: bool
    a1_selection: HigherRankD1A1Selection
    meshes: tuple[HigherRankD1MeshDiagnostics, ...]
    gates: tuple[HigherRankD1Gate, ...]
    refinement: tuple[HigherRankD1RefinementRecord, ...]
    failed_gate_paths: tuple[str, ...]
    qualification: str

    def __post_init__(self) -> None:
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank not in RANKS:
            raise ValueError("rank must belong to the D1 inventory")
        if type(self.depth) is not int:
            raise TypeError("depth must be a built-in int")
        if self.depth not in DEPTHS:
            raise ValueError("depth must belong to the D1 inventory")
        if type(self.case_id) is not str:
            raise TypeError("case_id must be a built-in str")
        if self.case_id != f"r{self.rank:02d}-L{self.depth:02d}":
            raise ValueError("case_id is inconsistent")
        require_nonnegative_float(self.exact_isolation, "exact_isolation")
        if self.exact_isolation != EXACT_ISOLATION:
            raise ValueError("exact_isolation must equal the D1 certificate")
        require_nonnegative_float(
            self.exact_attack_angle_bound, "exact_attack_angle_bound"
        )
        if type(self.basis_identifier) is not str or not self.basis_identifier:
            raise ValueError("basis_identifier must be a nonempty string")
        expected_basis = f"D1-P0-G0-retained-basis-r{self.rank:02d}"
        if self.basis_identifier != expected_basis:
            raise ValueError("basis_identifier is inconsistent with rank")
        if type(self.energy_unit) is not str:
            raise TypeError("energy_unit must be a built-in str")
        if type(self.energy_reference) is not str:
            raise TypeError("energy_reference must be a built-in str")
        if self.energy_unit != "E_ref":
            raise ValueError("energy_unit must be E_ref")
        if self.energy_reference != "zero-of-P0-formulas":
            raise ValueError("energy_reference is invalid")
        if self.evaluation_mesh_size != EVALUATION_MESH_SIZE:
            raise ValueError("evaluation_mesh_size must equal the D1 inventory")
        if type(self.construction_evaluation_disjoint) is not bool:
            raise TypeError("construction_evaluation_disjoint must be a built-in bool")
        if type(self.evaluation_noninfluence_confirmed) is not bool:
            raise TypeError("evaluation_noninfluence_confirmed must be a built-in bool")
        if self.construction_evaluation_disjoint is not True:
            raise ValueError("construction and evaluation coordinates must be disjoint")
        if self.evaluation_noninfluence_confirmed is not True:
            raise ValueError("evaluation mesh must not influence construction")
        if not isinstance(
            self.a1_selection,
            (
                HigherRankD1A1QualifiedSelection,
                HigherRankD1A1RankDeficientSelection,
                HigherRankD1A1NumericallyUnresolvedSelection,
            ),
        ):
            raise TypeError("a1_selection has an invalid record type")
        if self.a1_selection.selection_mesh_size != FINAL_CONSTRUCTION_MESH_SIZE:
            raise ValueError("A1 selection must use the final construction mesh")
        require_exact_tuple(self.meshes, HigherRankD1MeshDiagnostics, "meshes")
        if tuple(mesh.mesh_size for mesh in self.meshes) != CONSTRUCTION_MESH_SIZES:
            raise ValueError("meshes must follow the D1 construction order")
        if type(self.qualification) is not str:
            raise TypeError("qualification must be a built-in str")
        if self.qualification not in (
            "qualified",
            "invalid-mandatory-gate",
            "numerically-unresolved",
        ):
            raise ValueError("qualification is invalid")
        numerically_unresolved = (
            self.a1_selection.status == "alignment-numerically-unresolved"
            or any(
                mesh.a2_selection.status == "alignment-numerically-unresolved"
                or mesh.transport.status == "transport-numerically-unresolved"
                for mesh in self.meshes
            )
        )
        expected = (
            "numerically-unresolved"
            if numerically_unresolved
            else (
                "qualified" if not self.failed_gate_paths else "invalid-mandatory-gate"
            )
        )
        if self.qualification != expected:
            raise ValueError("qualification must match failed_gate_paths")
        require_exact_tuple(self.gates, HigherRankD1Gate, "gates")
        require_exact_tuple(self.refinement, HigherRankD1RefinementRecord, "refinement")
        if type(self.failed_gate_paths) is not tuple or any(
            type(path) is not str or not path.startswith("/")
            for path in self.failed_gate_paths
        ):
            raise TypeError("failed_gate_paths must contain JSON-Pointer-like strings")
        if len(set(self.failed_gate_paths)) != len(self.failed_gate_paths):
            raise ValueError("failed_gate_paths must be unique")


@dataclass(frozen=True, slots=True)
class HigherRankD1CalculationResult:
    """Retain complete ordered schema-free D1 coverage."""

    cases: tuple[HigherRankD1CaseResult, ...]
    overall_qualification: str
    lifecycle: str = "replaceable-schema-free-development"

    @classmethod
    def aggregate(cls, cases: tuple[HigherRankD1CaseResult, ...]) -> Self:
        """Aggregate ordered case outcomes into one campaign qualification."""
        require_exact_tuple(cases, HigherRankD1CaseResult, "cases")
        expected_count = len(RANKS) * len(DEPTHS)
        if len(cases) != expected_count:
            overall = "incomplete-coverage"
        elif any(case.qualification == "numerically-unresolved" for case in cases):
            overall = "numerically-unresolved"
        elif any(case.qualification != "qualified" for case in cases):
            overall = "invalid-mandatory-gate"
        else:
            overall = "qualified"
        return cls(cases, overall)

    def __post_init__(self) -> None:
        require_exact_tuple(self.cases, HigherRankD1CaseResult, "cases")
        if not self.cases:
            raise ValueError("cases must be nonempty")
        expected_ids = tuple(
            f"r{rank:02d}-L{depth:02d}" for rank in RANKS for depth in DEPTHS
        )
        observed_ids = tuple(case.case_id for case in self.cases)
        if observed_ids != expected_ids and self.overall_qualification != (
            "incomplete-coverage"
        ):
            raise ValueError("partial or reordered coverage must be marked incomplete")
        if observed_ids == expected_ids:
            expected_qualification = (
                "numerically-unresolved"
                if any(
                    case.qualification == "numerically-unresolved"
                    for case in self.cases
                )
                else (
                    "qualified"
                    if all(case.qualification == "qualified" for case in self.cases)
                    else "invalid-mandatory-gate"
                )
            )
            if self.overall_qualification != expected_qualification:
                raise ValueError("overall_qualification is inconsistent with cases")
        if type(self.overall_qualification) is not str:
            raise TypeError("overall_qualification must be a built-in str")
        if self.overall_qualification not in (
            "qualified",
            "invalid-mandatory-gate",
            "numerically-unresolved",
            "incomplete-coverage",
        ):
            raise ValueError("overall_qualification is invalid")
        if type(self.lifecycle) is not str:
            raise TypeError("lifecycle must be a built-in str")
        if self.lifecycle != "replaceable-schema-free-development":
            raise ValueError(
                "lifecycle must preserve the development evidence boundary"
            )


__all__ = [
    "HigherRankD1BlockNorm",
    "HigherRankD1CalculationResult",
    "HigherRankD1ChannelMeshRecord",
    "HigherRankD1CaseResult",
    "HigherRankD1ChannelMeshDiagnostics",
    "HigherRankD1FourierDiagnostics",
    "HigherRankD1InapplicableChannelMeshDiagnostics",
    "HigherRankD1Gate",
    "HigherRankD1MeshDiagnostics",
    "HigherRankD1ParetoPoint",
    "HigherRankD1RefinementRecord",
    "HigherRankD1ResidualSummary",
    "HigherRankD1ScalarLedger",
    "HigherRankD1ScalarLedgerEntry",
    "HigherRankD1SupportDiagnostics",
    "HigherRankD1SupportMonotonicity",
    "HigherRankD1TailDiagnostics",
]
