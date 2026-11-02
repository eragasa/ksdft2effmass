"""Immutable periodic-3D rank-N aggregate analysis results."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from ksdft2effmass.gauge_alignment import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentGroupIdentity,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic3d.gauge_alignment.base import (
    Periodic3DGaugeAlignmentAnalysis,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence.base import (
    Periodic3DRankNBandEquivalence,
    Periodic3DRankNBandEquivalenceAnalysis,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.definition import (
    Periodic3DRankNGaugeAlignment,
)
from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StringWireEnum,
)

from .request import Periodic3DRankNBandEquivalenceHoppingLocalityRequest


def _nonnegative_float(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels:
    """Retain rank-normalized matrix and ordered-spectrum errors."""

    maximum_matrix_frobenius: float
    root_mean_square_matrix_frobenius: float
    maximum_ordered_spectrum: float
    root_mean_square_ordered_spectrum: float

    def __post_init__(self) -> None:
        for name, value in (
            ("maximum_matrix_frobenius", self.maximum_matrix_frobenius),
            (
                "root_mean_square_matrix_frobenius",
                self.root_mean_square_matrix_frobenius,
            ),
            ("maximum_ordered_spectrum", self.maximum_ordered_spectrum),
            (
                "root_mean_square_ordered_spectrum",
                self.root_mean_square_ordered_spectrum,
            ),
        ):
            _nonnegative_float(value, name)


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary:
    """Retain normalized total, onsite, and nononsite hopping powers."""

    total_power: float
    onsite_power: float
    nononsite_power: float

    def __post_init__(self) -> None:
        for name, value in (
            ("total_power", self.total_power),
            ("onsite_power", self.onsite_power),
            ("nononsite_power", self.nononsite_power),
        ):
            _nonnegative_float(value, name)
        if abs(self.total_power - self.onsite_power - self.nononsite_power) > 1.0e-12:
            raise ValueError("locality powers must satisfy total = onsite + nononsite")


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis:
    """Retain one complete physical-metric shell consequence."""

    ordinal_shell_index: int
    metric_shell_value: int
    retained_block_count: int
    reference_shell_power: float
    comparison_shell_power: float
    reference_omitted_power: float
    comparison_omitted_power: float
    reference_total_errors: Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    comparison_total_errors: Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    reference_truncation_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    comparison_truncation_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )

    def __post_init__(self) -> None:
        for value, name in (
            (self.ordinal_shell_index, "ordinal_shell_index"),
            (self.metric_shell_value, "metric_shell_value"),
            (self.retained_block_count, "retained_block_count"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if self.retained_block_count == 0:
            raise ValueError("retained_block_count must be positive")
        for name, float_value in (
            ("reference_shell_power", self.reference_shell_power),
            ("comparison_shell_power", self.comparison_shell_power),
            ("reference_omitted_power", self.reference_omitted_power),
            ("comparison_omitted_power", self.comparison_omitted_power),
        ):
            _nonnegative_float(float_value, name)
        error_type = Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
        for error_value, name in (
            (self.reference_total_errors, "reference_total_errors"),
            (self.comparison_total_errors, "comparison_total_errors"),
            (self.reference_truncation_errors, "reference_truncation_errors"),
            (self.comparison_truncation_errors, "comparison_truncation_errors"),
        ):
            if type(error_value) is not error_type:
                raise TypeError(f"{name} must be the exact error-channel type")


@dataclass(frozen=True, slots=True)
class Periodic3DRankNSupportSelected:
    """Retain one minimum tolerance-satisfying metric shell."""

    ordinal_shell_index: int
    metric_shell_value: int
    satisfying_error: float
    preceding_error: float | None

    def __post_init__(self) -> None:
        for value, name in (
            (self.ordinal_shell_index, "ordinal_shell_index"),
            (self.metric_shell_value, "metric_shell_value"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")
        _nonnegative_float(self.satisfying_error, "satisfying_error")
        if self.preceding_error is not None:
            _nonnegative_float(self.preceding_error, "preceding_error")
        if (self.ordinal_shell_index == 0) is not (self.preceding_error is None):
            raise ValueError("preceding_error must be absent exactly at shell zero")


@dataclass(frozen=True, slots=True)
class Periodic3DRankNSupportUnresolved:
    """Retain the unresolved support-selection error evidence."""

    comparison_count: int
    minimum_observed_error: float
    largest_support_error: float

    def __post_init__(self) -> None:
        if type(self.comparison_count) is not int:
            raise TypeError("comparison_count must be a built-in integer")
        if self.comparison_count <= 0:
            raise ValueError("comparison_count must be positive")
        _nonnegative_float(self.minimum_observed_error, "minimum_observed_error")
        _nonnegative_float(self.largest_support_error, "largest_support_error")
        if self.minimum_observed_error > self.largest_support_error:
            raise ValueError(
                "minimum_observed_error cannot exceed largest_support_error"
            )


type Periodic3DRankNSupportSelection = (
    Periodic3DRankNSupportSelected | Periodic3DRankNSupportUnresolved
)


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision:
    """Retain support decisions for both channels and error functionals."""

    tolerance: float
    reference_matrix: Periodic3DRankNSupportSelection
    reference_ordered_spectrum: Periodic3DRankNSupportSelection
    comparison_matrix: Periodic3DRankNSupportSelection
    comparison_ordered_spectrum: Periodic3DRankNSupportSelection

    def __post_init__(self) -> None:
        _nonnegative_float(self.tolerance, "tolerance")
        admitted = (Periodic3DRankNSupportSelected, Periodic3DRankNSupportUnresolved)
        for value, name in (
            (self.reference_matrix, "reference_matrix"),
            (self.reference_ordered_spectrum, "reference_ordered_spectrum"),
            (self.comparison_matrix, "comparison_matrix"),
            (self.comparison_ordered_spectrum, "comparison_ordered_spectrum"),
        ):
            if type(value) not in admitted:
                raise TypeError(f"{name} must be one exact support outcome")


@dataclass(frozen=True, slots=True)
class Periodic3DRankNFittedAlignmentEvidence:
    """Retain invariant evidence for one fitted unitary alignment."""

    sample_count: int
    minimum_numerical_rank: int
    minimum_cross_singular_value: float
    maximum_optimal_residual_frobenius_norm: float
    maximum_applied_rank_cutoff: float

    def __post_init__(self) -> None:
        for value, name in (
            (self.sample_count, "sample_count"),
            (self.minimum_numerical_rank, "minimum_numerical_rank"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        for name, float_value in (
            ("minimum_cross_singular_value", self.minimum_cross_singular_value),
            (
                "maximum_optimal_residual_frobenius_norm",
                self.maximum_optimal_residual_frobenius_norm,
            ),
            ("maximum_applied_rank_cutoff", self.maximum_applied_rank_cutoff),
        ):
            _nonnegative_float(float_value, name)


@dataclass(frozen=True, slots=True)
class Periodic3DRankNPrescribedAlignmentEvidence:
    """Identify a prescribed identity or construction-oracle alignment."""

    identifier: str

    def __post_init__(self) -> None:
        if type(self.identifier) is not str or not self.identifier:
            raise TypeError("identifier must be a nonempty built-in string")
        if self.identifier not in ("identity", "known-inverse-oracle"):
            raise ValueError("identifier must be one prescribed alignment")


type Periodic3DRankNAlignmentEvidence = (
    Periodic3DRankNFittedAlignmentEvidence | Periodic3DRankNPrescribedAlignmentEvidence
)


class Periodic3DRankNAlignmentInapplicabilityEnum(StringWireEnum):
    """Identify why one fitted alignment has no downstream aggregate values."""

    AGGREGATE_RANK_DEFICIENT = "aggregate-rank-deficient"
    POINTWISE_CONSTRUCTION_RANK_DEFICIENT = "pointwise-construction-rank-deficient"
    POINTWISE_EVALUATION_RANK_DEFICIENT = "pointwise-evaluation-rank-deficient"
    TRANSPORT_LINK_RANK_DEFICIENT = "transport-link-rank-deficient"


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis(
    Periodic3DGaugeAlignmentAnalysis,
):
    """Retain complete scalar evidence for one applicable alignment route."""

    identity: GaugeAlignmentAnalysisIdentity
    alignment: Periodic3DRankNGaugeAlignment
    alignment_evidence: Periodic3DRankNAlignmentEvidence
    maximum_aligned_frame_defect: float
    minimum_transport_singular_value: float
    maximum_transport_procrustes_residual: float
    maximum_transport_unitarity_defect: float
    maximum_transport_rank_cutoff: float
    maximum_absolute_closure_phases: tuple[float, ...]
    maximum_plaquette_phase: float
    maximum_direct_matrix_difference: float
    maximum_direct_ordered_spectrum_difference: float
    reference_reconstruction_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    comparison_reconstruction_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    reference_interpolation_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    comparison_interpolation_errors: (
        Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
    )
    reference_locality: Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary
    comparison_locality: Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary
    shells: tuple[Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis, ...]
    tolerance_decisions: tuple[
        Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision, ...
    ]

    def __post_init__(self) -> None:
        if type(self.identity) is not GaugeAlignmentAnalysisIdentity:
            raise TypeError("identity must be the exact gauge-analysis identity")
        if type(self.alignment) is not Periodic3DRankNGaugeAlignment:
            raise TypeError("alignment must be the exact periodic-3D enum")
        if type(self.alignment_evidence) not in (
            Periodic3DRankNFittedAlignmentEvidence,
            Periodic3DRankNPrescribedAlignmentEvidence,
        ):
            raise TypeError("alignment_evidence must be one exact evidence type")
        if (
            self.alignment
            in (
                Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            )
        ) is not (
            type(self.alignment_evidence) is Periodic3DRankNFittedAlignmentEvidence
        ):
            raise ValueError("alignment and evidence type are inconsistent")
        for name, value in (
            ("maximum_aligned_frame_defect", self.maximum_aligned_frame_defect),
            ("minimum_transport_singular_value", self.minimum_transport_singular_value),
            (
                "maximum_transport_procrustes_residual",
                self.maximum_transport_procrustes_residual,
            ),
            (
                "maximum_transport_unitarity_defect",
                self.maximum_transport_unitarity_defect,
            ),
            ("maximum_transport_rank_cutoff", self.maximum_transport_rank_cutoff),
            ("maximum_plaquette_phase", self.maximum_plaquette_phase),
            ("maximum_direct_matrix_difference", self.maximum_direct_matrix_difference),
            (
                "maximum_direct_ordered_spectrum_difference",
                self.maximum_direct_ordered_spectrum_difference,
            ),
        ):
            _nonnegative_float(value, name)
        if type(self.maximum_absolute_closure_phases) is not tuple or any(
            type(value) is not float or not math.isfinite(value) or value < 0.0
            for value in self.maximum_absolute_closure_phases
        ):
            raise TypeError("maximum_absolute_closure_phases must be finite floats")
        if not self.maximum_absolute_closure_phases:
            raise ValueError("maximum_absolute_closure_phases must be nonempty")
        error_type = Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels
        for error_value, name in (
            (self.reference_reconstruction_errors, "reference_reconstruction_errors"),
            (self.comparison_reconstruction_errors, "comparison_reconstruction_errors"),
            (self.reference_interpolation_errors, "reference_interpolation_errors"),
            (self.comparison_interpolation_errors, "comparison_interpolation_errors"),
        ):
            if type(error_value) is not error_type:
                raise TypeError(f"{name} must be the exact error type")
        locality_type = Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary
        if type(self.reference_locality) is not locality_type:
            raise TypeError("reference_locality must be the exact locality type")
        if type(self.comparison_locality) is not locality_type:
            raise TypeError("comparison_locality must be the exact locality type")
        if (
            type(self.shells) is not tuple
            or not self.shells
            or any(
                type(value)
                is not Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis
                for value in self.shells
            )
        ):
            raise TypeError("shells must contain exact nonempty shell analyses")
        if tuple(shell.ordinal_shell_index for shell in self.shells) != tuple(
            range(len(self.shells))
        ):
            raise ValueError("shells must follow contiguous ordinal order")
        if type(self.tolerance_decisions) is not tuple or any(
            type(value)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision
            for value in self.tolerance_decisions
        ):
            raise TypeError("tolerance_decisions must contain exact decisions")

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the explicit finite-rank gauge-analysis identity."""
        return self.identity


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
    Periodic3DGaugeAlignmentAnalysis,
):
    """Retain typed rank-deficiency evidence without downstream values."""

    identity: GaugeAlignmentAnalysisIdentity
    alignment: Periodic3DRankNGaugeAlignment
    reason: Periodic3DRankNAlignmentInapplicabilityEnum
    deficient_sample_count: int
    minimum_numerical_rank: int | None

    def __post_init__(self) -> None:
        if type(self.identity) is not GaugeAlignmentAnalysisIdentity:
            raise TypeError("identity must be the exact gauge-analysis identity")
        if type(self.alignment) is not Periodic3DRankNGaugeAlignment:
            raise TypeError("alignment must be the exact periodic-3D enum")
        if type(self.reason) is not Periodic3DRankNAlignmentInapplicabilityEnum:
            raise TypeError("reason must be the exact inapplicability enum")
        if type(self.deficient_sample_count) is not int:
            raise TypeError("deficient_sample_count must be a built-in integer")
        if self.deficient_sample_count <= 0:
            raise ValueError("deficient_sample_count must be positive")
        transport_failure = (
            self.reason
            is Periodic3DRankNAlignmentInapplicabilityEnum.TRANSPORT_LINK_RANK_DEFICIENT
        )
        if transport_failure:
            if self.minimum_numerical_rank is not None:
                raise ValueError(
                    "transport-link failure has no selected alignment rank"
                )
        else:
            if self.alignment not in (
                Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            ):
                raise ValueError("Procrustes rank deficiency requires a fitted route")
            if type(self.minimum_numerical_rank) is not int:
                raise TypeError("minimum_numerical_rank must be a built-in integer")
            if self.minimum_numerical_rank < 0:
                raise ValueError("minimum_numerical_rank must be nonnegative")

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the explicit finite-rank gauge-analysis identity."""
        return self.identity


type Periodic3DRankNBandEquivalenceHoppingLocalityAlignmentAnalysis = (
    Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
    | Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis
)


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis(
    Periodic3DRankNBandEquivalence
):
    """Retain all alignment routes for one analytic model case."""

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the exact case's represented band-subspace rank."""
        return (self.retained_rank,)

    model_identity: str
    case_identifier: str
    retained_rank: int
    circuit_depth: int
    parent_scale: float
    attack_coefficient: float
    minimum_sampled_external_gap: float
    alignments: tuple[
        Periodic3DRankNBandEquivalenceHoppingLocalityAlignmentAnalysis, ...
    ]

    def __post_init__(self) -> None:
        for string_value, name in (
            (self.model_identity, "model_identity"),
            (self.case_identifier, "case_identifier"),
        ):
            if type(string_value) is not str or not string_value:
                raise TypeError(f"{name} must be a nonempty built-in string")
        for integer_value, name in (
            (self.retained_rank, "retained_rank"),
            (self.circuit_depth, "circuit_depth"),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if integer_value <= 0:
                raise ValueError(f"{name} must be positive")
        _nonnegative_float(self.parent_scale, "parent_scale")
        _nonnegative_float(self.attack_coefficient, "attack_coefficient")
        _nonnegative_float(
            self.minimum_sampled_external_gap, "minimum_sampled_external_gap"
        )
        if type(self.alignments) is not tuple or any(
            type(value)
            not in (
                Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
                Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
            )
            for value in self.alignments
        ):
            raise TypeError("alignments must contain exact alignment analyses")
        if any(value.retained_rank != self.retained_rank for value in self.alignments):
            raise ValueError("alignment identities must match the case retained rank")
        if tuple(value.alignment for value in self.alignments) != (
            Periodic3DRankNGaugeAlignment.IDENTITY,
            Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        ):
            raise ValueError("alignments must follow the selected four-route inventory")


class Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum(StringWireEnum):
    """Identify the claim boundary of one aggregate software analysis."""

    SOFTWARE_QUALIFICATION_NOT_SCIENTIFIC_EVIDENCE = (
        "software-qualification-not-scientific-evidence"
    )


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis(
    BaseTypedRecord,
    Periodic3DRankNBandEquivalenceAnalysis[
        Periodic3DRankNBandEquivalenceHoppingLocalityRequest
    ],
):
    """Retain one complete periodic-3D rank-N aggregate software analysis."""

    WIRE_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic3d-rankN-band-equivalence-hopping-locality-analysis.v1"
    )

    request: Periodic3DRankNBandEquivalenceHoppingLocalityRequest
    status: Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum
    cases: tuple[Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis, ...]

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the analyzed band-subspace rank inventory."""
        return self.request.band_subspace_ranks

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError("request must be the exact periodic-3D rank-N request")
        if (
            type(self.status)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum
        ):
            raise TypeError("status must be the exact periodic-3D analysis-status enum")
        if type(self.cases) is not tuple or any(
            type(value) is not Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis
            for value in self.cases
        ):
            raise TypeError("cases must contain exact periodic-3D case analyses")
        if len(self.cases) != self.request.case_count:
            raise ValueError("cases must match the expanded request count")
        identities = tuple(case.model_identity for case in self.cases)
        if len(set(identities)) != len(identities):
            raise ValueError("case model identities must be unique")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "wire_identity": self.WIRE_IDENTITY,
            "request": self.request,
            "status": self.status.to_wire(),
            "cases": tuple(_case_mapping(case) for case in self.cases),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"wire_identity", "request", "status", "cases"}:
            raise ValueError("periodic-3D rank-N analysis fields do not match")
        wire_identity = values["wire_identity"]
        request = values["request"]
        status = values["status"]
        cases = values["cases"]
        if wire_identity != cls.WIRE_IDENTITY:
            raise ValueError("wire_identity must match the periodic-3D rank-N analysis")
        if not isinstance(request, Mapping):
            raise TypeError("request must decode to a mapping")
        if type(status) is not str:
            raise TypeError("status must decode to a built-in string")
        if type(cases) is not tuple or any(
            not isinstance(case, Mapping) for case in cases
        ):
            raise TypeError("cases must decode to a tuple of mappings")
        return cls(
            request=Periodic3DRankNBandEquivalenceHoppingLocalityRequest.from_dict(
                request
            ),
            status=Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum.from_wire(
                status
            ),
            cases=tuple(_case_from_mapping(case) for case in cases),
        )


def _error_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels,
) -> Mapping[str, SerializableValue]:
    return {
        "maximum_matrix_frobenius": value.maximum_matrix_frobenius,
        "root_mean_square_matrix_frobenius": value.root_mean_square_matrix_frobenius,
        "maximum_ordered_spectrum": value.maximum_ordered_spectrum,
        "root_mean_square_ordered_spectrum": value.root_mean_square_ordered_spectrum,
    }


def _error_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels:
    required = {
        "maximum_matrix_frobenius",
        "root_mean_square_matrix_frobenius",
        "maximum_ordered_spectrum",
        "root_mean_square_ordered_spectrum",
    }
    if set(values) != required or any(
        type(values[name]) is not float for name in required
    ):
        raise TypeError("error-channel fields must be exact built-in floats")
    return Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels(
        maximum_matrix_frobenius=values["maximum_matrix_frobenius"],  # type: ignore[arg-type]
        root_mean_square_matrix_frobenius=values["root_mean_square_matrix_frobenius"],  # type: ignore[arg-type]
        maximum_ordered_spectrum=values["maximum_ordered_spectrum"],  # type: ignore[arg-type]
        root_mean_square_ordered_spectrum=values["root_mean_square_ordered_spectrum"],  # type: ignore[arg-type]
    )


def _locality_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary,
) -> Mapping[str, SerializableValue]:
    return {
        "total_power": value.total_power,
        "onsite_power": value.onsite_power,
        "nononsite_power": value.nononsite_power,
    }


def _locality_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary:
    required = {"total_power", "onsite_power", "nononsite_power"}
    if set(values) != required or any(
        type(values[name]) is not float for name in required
    ):
        raise TypeError("locality fields must be exact built-in floats")
    return Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary(
        total_power=values["total_power"],  # type: ignore[arg-type]
        onsite_power=values["onsite_power"],  # type: ignore[arg-type]
        nononsite_power=values["nononsite_power"],  # type: ignore[arg-type]
    )


def _support_mapping(
    value: Periodic3DRankNSupportSelection,
) -> Mapping[str, SerializableValue]:
    if isinstance(value, Periodic3DRankNSupportSelected):
        if type(value) is not Periodic3DRankNSupportSelected:
            raise TypeError("selected support subclasses are not admitted")
        return {
            "disposition": "selected",
            "ordinal_shell_index": value.ordinal_shell_index,
            "metric_shell_value": value.metric_shell_value,
            "satisfying_error": value.satisfying_error,
            "preceding_error": value.preceding_error,
        }
    if isinstance(value, Periodic3DRankNSupportUnresolved):
        if type(value) is not Periodic3DRankNSupportUnresolved:
            raise TypeError("unresolved support subclasses are not admitted")
        return {
            "disposition": "unresolved",
            "comparison_count": value.comparison_count,
            "minimum_observed_error": value.minimum_observed_error,
            "largest_support_error": value.largest_support_error,
        }
    raise TypeError("support selection type is not admitted")


def _support_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNSupportSelection:
    disposition = values.get("disposition")
    if disposition == "selected":
        required = {
            "disposition",
            "ordinal_shell_index",
            "metric_shell_value",
            "satisfying_error",
            "preceding_error",
        }
        if set(values) != required:
            raise ValueError("selected support fields do not match")
        ordinal = values["ordinal_shell_index"]
        metric = values["metric_shell_value"]
        error = values["satisfying_error"]
        preceding = values["preceding_error"]
        if (
            type(ordinal) is not int
            or type(metric) is not int
            or type(error) is not float
        ):
            raise TypeError("selected support fields have invalid types")
        if preceding is not None and type(preceding) is not float:
            raise TypeError("preceding_error must decode to float or None")
        return Periodic3DRankNSupportSelected(ordinal, metric, error, preceding)
    if disposition == "unresolved":
        required = {
            "disposition",
            "comparison_count",
            "minimum_observed_error",
            "largest_support_error",
        }
        if set(values) != required:
            raise ValueError("unresolved support fields do not match")
        count = values["comparison_count"]
        minimum = values["minimum_observed_error"]
        largest = values["largest_support_error"]
        if (
            type(count) is not int
            or type(minimum) is not float
            or type(largest) is not float
        ):
            raise TypeError("unresolved support fields have invalid types")
        return Periodic3DRankNSupportUnresolved(count, minimum, largest)
    raise ValueError("support disposition is not recognized")


def _shell_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis,
) -> Mapping[str, SerializableValue]:
    return {
        "ordinal_shell_index": value.ordinal_shell_index,
        "metric_shell_value": value.metric_shell_value,
        "retained_block_count": value.retained_block_count,
        "reference_shell_power": value.reference_shell_power,
        "comparison_shell_power": value.comparison_shell_power,
        "reference_omitted_power": value.reference_omitted_power,
        "comparison_omitted_power": value.comparison_omitted_power,
        "reference_total_errors": _error_mapping(value.reference_total_errors),
        "comparison_total_errors": _error_mapping(value.comparison_total_errors),
        "reference_truncation_errors": _error_mapping(
            value.reference_truncation_errors
        ),
        "comparison_truncation_errors": _error_mapping(
            value.comparison_truncation_errors
        ),
    }


def _shell_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis:
    required = {
        "ordinal_shell_index",
        "metric_shell_value",
        "retained_block_count",
        "reference_shell_power",
        "comparison_shell_power",
        "reference_omitted_power",
        "comparison_omitted_power",
        "reference_total_errors",
        "comparison_total_errors",
        "reference_truncation_errors",
        "comparison_truncation_errors",
    }
    if set(values) != required:
        raise ValueError("shell fields do not match")
    integer_names = (
        "ordinal_shell_index",
        "metric_shell_value",
        "retained_block_count",
    )
    float_names = (
        "reference_shell_power",
        "comparison_shell_power",
        "reference_omitted_power",
        "comparison_omitted_power",
    )
    if any(type(values[name]) is not int for name in integer_names) or any(
        type(values[name]) is not float for name in float_names
    ):
        raise TypeError("shell scalar fields have invalid types")
    error_values = tuple(
        values[name]
        for name in (
            "reference_total_errors",
            "comparison_total_errors",
            "reference_truncation_errors",
            "comparison_truncation_errors",
        )
    )
    if any(not isinstance(value, Mapping) for value in error_values):
        raise TypeError("shell error fields must decode to mappings")
    return Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis(
        ordinal_shell_index=values["ordinal_shell_index"],  # type: ignore[arg-type]
        metric_shell_value=values["metric_shell_value"],  # type: ignore[arg-type]
        retained_block_count=values["retained_block_count"],  # type: ignore[arg-type]
        reference_shell_power=values["reference_shell_power"],  # type: ignore[arg-type]
        comparison_shell_power=values["comparison_shell_power"],  # type: ignore[arg-type]
        reference_omitted_power=values["reference_omitted_power"],  # type: ignore[arg-type]
        comparison_omitted_power=values["comparison_omitted_power"],  # type: ignore[arg-type]
        reference_total_errors=_error_from_mapping(error_values[0]),  # type: ignore[arg-type]
        comparison_total_errors=_error_from_mapping(error_values[1]),  # type: ignore[arg-type]
        reference_truncation_errors=_error_from_mapping(error_values[2]),  # type: ignore[arg-type]
        comparison_truncation_errors=_error_from_mapping(error_values[3]),  # type: ignore[arg-type]
    )


def _decision_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision,
) -> Mapping[str, SerializableValue]:
    return {
        "tolerance": value.tolerance,
        "reference_matrix": _support_mapping(value.reference_matrix),
        "reference_ordered_spectrum": _support_mapping(
            value.reference_ordered_spectrum
        ),
        "comparison_matrix": _support_mapping(value.comparison_matrix),
        "comparison_ordered_spectrum": _support_mapping(
            value.comparison_ordered_spectrum
        ),
    }


def _decision_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision:
    required = {
        "tolerance",
        "reference_matrix",
        "reference_ordered_spectrum",
        "comparison_matrix",
        "comparison_ordered_spectrum",
    }
    if set(values) != required or type(values["tolerance"]) is not float:
        raise ValueError("tolerance-decision fields do not match")
    nested = tuple(
        values[name]
        for name in (
            "reference_matrix",
            "reference_ordered_spectrum",
            "comparison_matrix",
            "comparison_ordered_spectrum",
        )
    )
    if any(not isinstance(value, Mapping) for value in nested):
        raise TypeError("support decisions must decode to mappings")
    return Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision(
        tolerance=values["tolerance"],
        reference_matrix=_support_from_mapping(nested[0]),  # type: ignore[arg-type]
        reference_ordered_spectrum=_support_from_mapping(nested[1]),  # type: ignore[arg-type]
        comparison_matrix=_support_from_mapping(nested[2]),  # type: ignore[arg-type]
        comparison_ordered_spectrum=_support_from_mapping(nested[3]),  # type: ignore[arg-type]
    )


def _evidence_mapping(
    value: Periodic3DRankNAlignmentEvidence,
) -> Mapping[str, SerializableValue]:
    if isinstance(value, Periodic3DRankNFittedAlignmentEvidence):
        if type(value) is not Periodic3DRankNFittedAlignmentEvidence:
            raise TypeError("fitted evidence subclasses are not admitted")
        return {
            "kind": "fitted",
            "sample_count": value.sample_count,
            "minimum_numerical_rank": value.minimum_numerical_rank,
            "minimum_cross_singular_value": value.minimum_cross_singular_value,
            "maximum_optimal_residual_frobenius_norm": (
                value.maximum_optimal_residual_frobenius_norm
            ),
            "maximum_applied_rank_cutoff": value.maximum_applied_rank_cutoff,
        }
    if isinstance(value, Periodic3DRankNPrescribedAlignmentEvidence):
        if type(value) is not Periodic3DRankNPrescribedAlignmentEvidence:
            raise TypeError("prescribed evidence subclasses are not admitted")
        return {"kind": "prescribed", "identifier": value.identifier}
    raise TypeError("alignment evidence type is not admitted")


def _evidence_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNAlignmentEvidence:
    kind = values.get("kind")
    if kind == "prescribed":
        if (
            set(values) != {"kind", "identifier"}
            or type(values["identifier"]) is not str
        ):
            raise TypeError("prescribed evidence fields have invalid types")
        return Periodic3DRankNPrescribedAlignmentEvidence(values["identifier"])
    if kind == "fitted":
        required = {
            "kind",
            "sample_count",
            "minimum_numerical_rank",
            "minimum_cross_singular_value",
            "maximum_optimal_residual_frobenius_norm",
            "maximum_applied_rank_cutoff",
        }
        if set(values) != required:
            raise ValueError("fitted evidence fields do not match")
        if (
            type(values["sample_count"]) is not int
            or type(values["minimum_numerical_rank"]) is not int
        ):
            raise TypeError("fitted evidence integer fields have invalid types")
        float_names = (
            "minimum_cross_singular_value",
            "maximum_optimal_residual_frobenius_norm",
            "maximum_applied_rank_cutoff",
        )
        if any(type(values[name]) is not float for name in float_names):
            raise TypeError("fitted evidence float fields have invalid types")
        return Periodic3DRankNFittedAlignmentEvidence(
            sample_count=values["sample_count"],
            minimum_numerical_rank=values["minimum_numerical_rank"],
            minimum_cross_singular_value=values["minimum_cross_singular_value"],  # type: ignore[arg-type]
            maximum_optimal_residual_frobenius_norm=values[
                "maximum_optimal_residual_frobenius_norm"
            ],  # type: ignore[arg-type]
            maximum_applied_rank_cutoff=values["maximum_applied_rank_cutoff"],  # type: ignore[arg-type]
        )
    raise ValueError("alignment evidence kind is not recognized")


def _identity_mapping(
    value: GaugeAlignmentAnalysisIdentity,
) -> Mapping[str, SerializableValue]:
    return {
        "represented_dimension": value.gauge_group_identity.represented_dimension,
        "alignment_sample_count": value.alignment_sample_count,
        "action_convention": value.action_convention.to_wire(),
        "inner_product_convention": value.inner_product_convention.to_wire(),
    }


def _identity_from_mapping(
    values: Mapping[str, SerializableValue],
) -> GaugeAlignmentAnalysisIdentity:
    required = {
        "represented_dimension",
        "alignment_sample_count",
        "action_convention",
        "inner_product_convention",
    }
    if set(values) != required:
        raise ValueError("gauge-analysis identity fields do not match")
    represented_dimension = values["represented_dimension"]
    sample_count = values["alignment_sample_count"]
    action = values["action_convention"]
    inner_product = values["inner_product_convention"]
    if type(represented_dimension) is not int or type(sample_count) is not int:
        raise TypeError("gauge-analysis dimensions must decode to integers")
    if type(action) is not str or type(inner_product) is not str:
        raise TypeError("gauge-analysis conventions must decode to strings")
    return GaugeAlignmentAnalysisIdentity(
        gauge_group_identity=GaugeAlignmentGroupIdentity.unitary(
            represented_dimension=represented_dimension
        ),
        alignment_sample_count=sample_count,
        action_convention=GaugeAlignmentActionConvention.from_wire(action),
        inner_product_convention=GaugeAlignmentInnerProductConvention.from_wire(
            inner_product
        ),
    )


def _alignment_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityAlignmentAnalysis,
) -> Mapping[str, SerializableValue]:
    if isinstance(
        value,
        Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis,
    ):
        if (
            type(value)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis  # noqa: E501
        ):
            raise TypeError("inapplicable alignment subclasses are not admitted")
        return {
            "disposition": "inapplicable",
            "analysis_identity": _identity_mapping(value.identity),
            "alignment": value.alignment.to_wire(),
            "reason": value.reason.to_wire(),
            "deficient_sample_count": value.deficient_sample_count,
            "minimum_numerical_rank": value.minimum_numerical_rank,
        }
    if not isinstance(
        value,
        Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
    ):
        raise TypeError("alignment-analysis type is not admitted")
    if (
        type(value)
        is not Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis
    ):
        raise TypeError("qualified alignment subclasses are not admitted")
    return {
        "disposition": "qualified",
        "analysis_identity": _identity_mapping(value.identity),
        "alignment": value.alignment.to_wire(),
        "alignment_evidence": _evidence_mapping(value.alignment_evidence),
        "maximum_aligned_frame_defect": value.maximum_aligned_frame_defect,
        "minimum_transport_singular_value": value.minimum_transport_singular_value,
        "maximum_transport_procrustes_residual": (
            value.maximum_transport_procrustes_residual
        ),
        "maximum_transport_unitarity_defect": value.maximum_transport_unitarity_defect,
        "maximum_transport_rank_cutoff": value.maximum_transport_rank_cutoff,
        "maximum_absolute_closure_phases": value.maximum_absolute_closure_phases,
        "maximum_plaquette_phase": value.maximum_plaquette_phase,
        "maximum_direct_matrix_difference": value.maximum_direct_matrix_difference,
        "maximum_direct_ordered_spectrum_difference": (
            value.maximum_direct_ordered_spectrum_difference
        ),
        "reference_reconstruction_errors": _error_mapping(
            value.reference_reconstruction_errors
        ),
        "comparison_reconstruction_errors": _error_mapping(
            value.comparison_reconstruction_errors
        ),
        "reference_interpolation_errors": _error_mapping(
            value.reference_interpolation_errors
        ),
        "comparison_interpolation_errors": _error_mapping(
            value.comparison_interpolation_errors
        ),
        "reference_locality": _locality_mapping(value.reference_locality),
        "comparison_locality": _locality_mapping(value.comparison_locality),
        "shells": tuple(_shell_mapping(shell) for shell in value.shells),
        "tolerance_decisions": tuple(
            _decision_mapping(decision) for decision in value.tolerance_decisions
        ),
    }


def _alignment_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityAlignmentAnalysis:
    disposition = values.get("disposition")
    alignment_wire = values.get("alignment")
    identity_value = values.get("analysis_identity")
    if type(alignment_wire) is not str:
        raise TypeError("alignment must decode to a built-in string")
    if not isinstance(identity_value, Mapping):
        raise TypeError("analysis_identity must decode to a mapping")
    alignment = Periodic3DRankNGaugeAlignment.from_wire(alignment_wire)
    analysis_identity = _identity_from_mapping(identity_value)
    if disposition == "inapplicable":
        required = {
            "disposition",
            "analysis_identity",
            "alignment",
            "reason",
            "deficient_sample_count",
            "minimum_numerical_rank",
        }
        if set(values) != required or type(values["reason"]) is not str:
            raise ValueError("inapplicable alignment fields do not match")
        count = values["deficient_sample_count"]
        rank = values["minimum_numerical_rank"]
        if type(count) is not int:
            raise TypeError("deficient_sample_count must be a built-in integer")
        if rank is not None and type(rank) is not int:
            raise TypeError("minimum_numerical_rank must decode to integer or None")
        return (
            Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis(
                identity=analysis_identity,
                alignment=alignment,
                reason=Periodic3DRankNAlignmentInapplicabilityEnum.from_wire(
                    values["reason"]
                ),
                deficient_sample_count=count,
                minimum_numerical_rank=rank,
            )
        )
    if disposition != "qualified":
        raise ValueError("alignment disposition is not recognized")
    required = {
        "disposition",
        "analysis_identity",
        "alignment",
        "alignment_evidence",
        "maximum_aligned_frame_defect",
        "minimum_transport_singular_value",
        "maximum_transport_procrustes_residual",
        "maximum_transport_unitarity_defect",
        "maximum_transport_rank_cutoff",
        "maximum_absolute_closure_phases",
        "maximum_plaquette_phase",
        "maximum_direct_matrix_difference",
        "maximum_direct_ordered_spectrum_difference",
        "reference_reconstruction_errors",
        "comparison_reconstruction_errors",
        "reference_interpolation_errors",
        "comparison_interpolation_errors",
        "reference_locality",
        "comparison_locality",
        "shells",
        "tolerance_decisions",
    }
    if set(values) != required:
        raise ValueError("qualified alignment fields do not match")
    mapping_names = (
        "alignment_evidence",
        "reference_reconstruction_errors",
        "comparison_reconstruction_errors",
        "reference_interpolation_errors",
        "comparison_interpolation_errors",
        "reference_locality",
        "comparison_locality",
    )
    if any(not isinstance(values[name], Mapping) for name in mapping_names):
        raise TypeError("qualified alignment nested fields must decode to mappings")
    float_names = (
        "maximum_aligned_frame_defect",
        "minimum_transport_singular_value",
        "maximum_transport_procrustes_residual",
        "maximum_transport_unitarity_defect",
        "maximum_transport_rank_cutoff",
        "maximum_plaquette_phase",
        "maximum_direct_matrix_difference",
        "maximum_direct_ordered_spectrum_difference",
    )
    if any(type(values[name]) is not float for name in float_names):
        raise TypeError("qualified alignment scalar diagnostics must be floats")
    phases = values["maximum_absolute_closure_phases"]
    shells = values["shells"]
    decisions = values["tolerance_decisions"]
    if type(phases) is not tuple or any(type(value) is not float for value in phases):
        raise TypeError("closure phases must decode to built-in floats")
    if type(shells) is not tuple or any(
        not isinstance(value, Mapping) for value in shells
    ):
        raise TypeError("shells must decode to mappings")
    if type(decisions) is not tuple or any(
        not isinstance(value, Mapping) for value in decisions
    ):
        raise TypeError("tolerance decisions must decode to mappings")
    return Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis(
        identity=analysis_identity,
        alignment=alignment,
        alignment_evidence=_evidence_from_mapping(values["alignment_evidence"]),  # type: ignore[arg-type]
        maximum_aligned_frame_defect=values["maximum_aligned_frame_defect"],  # type: ignore[arg-type]
        minimum_transport_singular_value=values["minimum_transport_singular_value"],  # type: ignore[arg-type]
        maximum_transport_procrustes_residual=values[
            "maximum_transport_procrustes_residual"
        ],  # type: ignore[arg-type]
        maximum_transport_unitarity_defect=values["maximum_transport_unitarity_defect"],  # type: ignore[arg-type]
        maximum_transport_rank_cutoff=values["maximum_transport_rank_cutoff"],  # type: ignore[arg-type]
        maximum_absolute_closure_phases=phases,
        maximum_plaquette_phase=values["maximum_plaquette_phase"],  # type: ignore[arg-type]
        maximum_direct_matrix_difference=values["maximum_direct_matrix_difference"],  # type: ignore[arg-type]
        maximum_direct_ordered_spectrum_difference=values[
            "maximum_direct_ordered_spectrum_difference"
        ],  # type: ignore[arg-type]
        reference_reconstruction_errors=_error_from_mapping(
            values["reference_reconstruction_errors"]  # type: ignore[arg-type]
        ),
        comparison_reconstruction_errors=_error_from_mapping(
            values["comparison_reconstruction_errors"]  # type: ignore[arg-type]
        ),
        reference_interpolation_errors=_error_from_mapping(
            values["reference_interpolation_errors"]  # type: ignore[arg-type]
        ),
        comparison_interpolation_errors=_error_from_mapping(
            values["comparison_interpolation_errors"]  # type: ignore[arg-type]
        ),
        reference_locality=_locality_from_mapping(values["reference_locality"]),  # type: ignore[arg-type]
        comparison_locality=_locality_from_mapping(values["comparison_locality"]),  # type: ignore[arg-type]
        shells=tuple(_shell_from_mapping(value) for value in shells),
        tolerance_decisions=tuple(_decision_from_mapping(value) for value in decisions),
    )


def _case_mapping(
    value: Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
) -> Mapping[str, SerializableValue]:
    return {
        "model_identity": value.model_identity,
        "case_identifier": value.case_identifier,
        "retained_rank": value.retained_rank,
        "circuit_depth": value.circuit_depth,
        "parent_scale": value.parent_scale,
        "attack_coefficient": value.attack_coefficient,
        "minimum_sampled_external_gap": value.minimum_sampled_external_gap,
        "alignments": tuple(_alignment_mapping(item) for item in value.alignments),
    }


def _case_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis:
    required = {
        "model_identity",
        "case_identifier",
        "retained_rank",
        "circuit_depth",
        "parent_scale",
        "attack_coefficient",
        "minimum_sampled_external_gap",
        "alignments",
    }
    if set(values) != required:
        raise ValueError("case-analysis fields do not match")
    if (
        type(values["model_identity"]) is not str
        or type(values["case_identifier"]) is not str
    ):
        raise TypeError("case identities must decode to built-in strings")
    if (
        type(values["retained_rank"]) is not int
        or type(values["circuit_depth"]) is not int
    ):
        raise TypeError("case rank and depth must decode to built-in integers")
    parent_scale = values["parent_scale"]
    attack_coefficient = values["attack_coefficient"]
    minimum_sampled_external_gap = values["minimum_sampled_external_gap"]
    if type(parent_scale) is not float:
        raise TypeError("parent_scale must decode to a built-in float")
    if type(attack_coefficient) is not float:
        raise TypeError("attack_coefficient must decode to a built-in float")
    if type(minimum_sampled_external_gap) is not float:
        raise TypeError("minimum_sampled_external_gap must decode to a built-in float")
    alignments = values["alignments"]
    if type(alignments) is not tuple or any(
        not isinstance(value, Mapping) for value in alignments
    ):
        raise TypeError("alignments must decode to a tuple of mappings")
    return Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis(
        model_identity=values["model_identity"],
        case_identifier=values["case_identifier"],
        retained_rank=values["retained_rank"],
        circuit_depth=values["circuit_depth"],
        parent_scale=parent_scale,
        attack_coefficient=attack_coefficient,
        minimum_sampled_external_gap=minimum_sampled_external_gap,
        alignments=tuple(_alignment_from_mapping(value) for value in alignments),
    )


__all__ = [
    "Periodic3DRankNAlignmentInapplicabilityEnum",
    "Periodic3DRankNBandEquivalenceHoppingLocalityAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityAnalysisStatusEnum",
    "Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels",
    "Periodic3DRankNBandEquivalenceHoppingLocalityInapplicableAlignmentAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityLocalitySummary",
    "Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityShellAnalysis",
    "Periodic3DRankNBandEquivalenceHoppingLocalityToleranceDecision",
    "Periodic3DRankNFittedAlignmentEvidence",
    "Periodic3DRankNPrescribedAlignmentEvidence",
    "Periodic3DRankNSupportSelected",
    "Periodic3DRankNSupportUnresolved",
]
