"""Independent verifier artifacts and explicit post-computation reference decoding."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from projectkoios.integrations.wannier90 import (
    Wannier90NativeArtifact,
)

from .grid_verification import (
    CommonSpaceIndependentGridResult,
    CommonSpaceIndependentVerification,
    CommonSpaceProducerCorrelation,
    CommonSpaceVerificationOutcome,
)
from .producer_result import CommonSpaceProducerResultAdapter
from .source_admission import (
    CommonSpaceSourceAdmission,
    CommonSpaceVerificationJson,
    JsonValue,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceIndependentResultSerializer:
    """Portable compact exact-number result, without dense matrices or local paths."""

    result: CommonSpaceIndependentGridResult

    def __post_init__(self) -> None:
        if type(self.result) is not CommonSpaceIndependentGridResult:
            raise TypeError("result must be a completed independent grid result")

    def encode(self) -> bytes:
        wire = CommonSpaceVerificationJson
        points: list[JsonValue] = []
        for index, point in enumerate(self.result.points):
            arithmetic = point.assessment.arithmetic
            direction = point.direction
            points.append(
                {
                    "ordered_index": index,
                    "fractional_kpoint": list(
                        point.assessment.overlap.fractional_kpoint
                    ),
                    "resolved_rank": point.assessment.resolved_rank,
                    "arithmetic_rank_lower_bound": arithmetic.rank_lower_bound,
                    "arithmetic_rank_upper_bound": arithmetic.rank_upper_bound,
                    "eigenvalue_intervals": [
                        [wire.rational(value.lower), wire.rational(value.upper)]
                        for value in arithmetic.eigenvalue_intervals
                    ],
                    "arithmetic_failure": arithmetic.failure.to_wire()
                    if arithmetic.failure
                    else None,
                    "hermiticity_defect_bound": wire.rational(
                        arithmetic.hermiticity_defect_bound
                    ),
                    "orthonormality_defect_bound": wire.rational(
                        arithmetic.orthonormality_defect_bound
                    )
                    if arithmetic.orthonormality_defect_bound is not None
                    else None,
                    "spectral_error_bound": wire.rational(
                        arithmetic.spectral_error_bound
                    )
                    if arithmetic.spectral_error_bound is not None
                    else None,
                    "eigenpair_residual_bounds": [
                        wire.rational(value)
                        for value in arithmetic.eigenpair_residual_bounds
                    ],
                    "native_error_bound": wire.rational(
                        point.assessment.uncertainty.native_error_bound
                    ),
                    "parsing_error_bound": wire.rational(
                        point.assessment.uncertainty.parsing_error_bound
                    ),
                    "uncertainty_bound_covered": point.assessment.uncertainty_bound_covered,
                    "unitary_invariance_passed": point.unitary_invariance_passed,
                    "direction_outcome": direction.outcome.to_wire(),
                    "nominal_atomic_weights": [
                        wire.rational(value) for value in direction.nominal_weights
                    ],
                    "atomic_weight_intervals": [
                        [wire.rational(value.lower), wire.rational(value.upper)]
                        for value in direction.orbital_intervals
                    ],
                    "group_weight_intervals_s_p_s_star": [
                        [wire.rational(value.lower), wire.rational(value.upper)]
                        for value in direction.group_intervals
                    ],
                    "arithmetic_projector_error": wire.rational(
                        direction.arithmetic_projector_error
                    )
                    if direction.arithmetic_projector_error is not None
                    else None,
                    "input_projector_error": wire.rational(
                        direction.input_projector_error
                    )
                    if direction.input_projector_error is not None
                    else None,
                    "rayleigh_residual_squared": wire.rational(
                        direction.rayleigh_residual_squared
                    )
                    if direction.rayleigh_residual_squared is not None
                    else None,
                    "eigenvalue_gap_lower": wire.rational(
                        direction.eigenvalue_gap_lower
                    )
                    if direction.eigenvalue_gap_lower is not None
                    else None,
                }
            )
        admission = self.result.admission
        provider = admission.parsed_inputs.provider_binding
        payload: dict[str, JsonValue] = {
            "record_type": "common-space-independent-verification-v1",
            "review_scope": admission.review_scope.to_wire(),
            "review_reference": admission.review_reference,
            "outcome": self.result.outcome.to_wire(),
            "source_assertions": wire.decode(admission.assertion_payload()),
            "provider_version": provider.distribution_version,
            "provider_modules": [
                {"module_name": value.module_name, "sha256": value.sha256}
                for value in provider.modules
            ],
            "source_ledger": [
                {
                    "role": value.role.to_wire(),
                    "identity": wire.identity(value.expected),
                }
                for value in admission.evidence
            ],
            "points": points,
            "deficient_indices": list(self.result.deficient_indices),
        }
        return wire.encode(payload)


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceVerificationRun:
    """Compute and exclusively retain a separate independent verifier record.

    Shared authenticated parsing precedes this API. Reject an existing/dangling-symlink
    output root before verifier admission or arithmetic. File writes are exclusive;
    this is not descriptor-bound protection against a hostile concurrent filesystem.
    No native paths, numerical producer reference, execution authority, or fit are
    accepted. Producer evidence bytes are authenticated as prerequisites, not parsed
    for numerical values.
    """

    admission: CommonSpaceSourceAdmission
    output_root: Path

    def __post_init__(self) -> None:
        if type(self.admission) is not CommonSpaceSourceAdmission or not isinstance(
            self.output_root, Path
        ):
            raise TypeError("verification run requires admission and an output Path")

    def execute(self) -> CommonSpaceIndependentGridResult:
        if self.output_root.exists() or self.output_root.is_symlink():
            raise FileExistsError("independent verification output root must not exist")
        result = CommonSpaceIndependentVerification(admission=self.admission).execute()
        content = CommonSpaceIndependentResultSerializer(result=result).encode()
        implementation: list[JsonValue] = []
        for path in sorted(Path(__file__).parent.glob("*.py")):
            payload = path.read_bytes()
            implementation.append(
                {
                    "name": path.name,
                    "byte_count": len(payload),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                }
            )
        manifest: dict[str, JsonValue] = {
            "record_type": "common-space-independent-verification-manifest-v1",
            "result": {
                "name": "independent-verification.json",
                "byte_count": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            },
            "implementation": implementation,
            "review_scope": self.admission.review_scope.to_wire(),
        }
        self.output_root.mkdir(parents=True, exist_ok=False)
        with (self.output_root / "independent-verification.json").open("xb") as stream:
            stream.write(content)
        with (self.output_root / "manifest.json").open("xb") as stream:
            stream.write(CommonSpaceVerificationJson.encode(manifest))
        return result


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceProducerCorrelationRun:
    """Compare authenticated original producer bytes without rewriting independence.

    The adapter obtains the producer result only from the independent result's
    reviewed source evidence, never from a manually normalized substitute.
    """

    independent: CommonSpaceIndependentGridResult
    output_root: Path

    def __post_init__(self) -> None:
        if type(
            self.independent
        ) is not CommonSpaceIndependentGridResult or not isinstance(
            self.output_root, Path
        ):
            raise TypeError(
                "correlation requires an independent result and output Path"
            )

    def execute(self) -> CommonSpaceVerificationOutcome:
        destination = self.output_root / "producer-correlation.json"
        if destination.exists() or destination.is_symlink():
            raise FileExistsError("producer correlation record must not exist")
        independent_bytes = CommonSpaceIndependentResultSerializer(
            result=self.independent
        ).encode()
        if (
            self.output_root / "independent-verification.json"
        ).read_bytes() != independent_bytes:
            raise ValueError(
                "retained independent result differs from the completed computation"
            )
        wire = CommonSpaceVerificationJson
        manifest_bytes = (self.output_root / "manifest.json").read_bytes()
        manifest = wire.decode(manifest_bytes)
        result_identity = wire.identity(
            Wannier90NativeArtifact(
                "independent-verification.json", independent_bytes
            ).identity
        )
        if (
            type(manifest) is not dict
            or set(manifest)
            != {"record_type", "result", "implementation", "review_scope"}
            or manifest["record_type"]
            != "common-space-independent-verification-manifest-v1"
            or wire.encode(manifest["result"]) != wire.encode(result_identity)
            or manifest["review_scope"]
            != self.independent.admission.review_scope.to_wire()
        ):
            raise ValueError("independent manifest differs from the completed result")
        producer = CommonSpaceProducerResultAdapter(
            independent=self.independent
        ).execute()
        mismatches = CommonSpaceProducerCorrelation(
            independent=self.independent, producer=producer
        ).execute()
        if (
            self.independent.outcome
            is CommonSpaceVerificationOutcome.numerically_inconclusive
        ):
            outcome = CommonSpaceVerificationOutcome.numerically_inconclusive
        elif mismatches:
            outcome = CommonSpaceVerificationOutcome.producer_mismatch
        else:
            outcome = CommonSpaceVerificationOutcome.rank_diagnosis_correlated
        record: dict[str, JsonValue] = {
            "record_type": "common-space-producer-correlation-v1",
            "review_scope": self.independent.admission.review_scope.to_wire(),
            "outcome": outcome.to_wire(),
            "independent_result": result_identity,
            "independent_manifest": wire.identity(
                Wannier90NativeArtifact("manifest.json", manifest_bytes).identity
            ),
            "producer_result": wire.identity(producer.producer_result_identity),
            "mismatches": list(mismatches),
        }
        with destination.open("xb") as stream:
            stream.write(wire.encode(record))
        return outcome
