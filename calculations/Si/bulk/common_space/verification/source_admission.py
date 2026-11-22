"""Campaign-specific correlation of reviewed source assertions and prerequisites."""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from typing import ClassVar

from ksdft2effmass.serialization.enums import StrWireEnum
from projectkoios.integrations.wannier90 import (
    Wannier90NativeArtifact,
    Wannier90NativeArtifactCorrelator,
    Wannier90NativeArtifactIdentity,
)

from .native_inputs import CommonSpaceParsedNativeInputs
from .native_precision import CommonSpaceNativeRoundingModel

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class CommonSpaceReviewScope(StrWireEnum):
    """Trust context of a reviewed declaration, not execution authorization."""

    synthetic = "synthetic-development-only"
    retained = "reviewed-retained-source-declaration"


class CommonSpaceEvidenceRole(StrWireEnum):
    """Complete source inventory; no numeric producer output is consumed here."""

    request = "development-request"
    full_source = "S30-full-source"
    full_support = "S105-full-support"
    blocked_alignment = "S110-blocked-result"
    protocol = "hopping-first-protocol"
    state_assertions = "reviewed-state-assertions"
    producer_completion = "producer-completion-evidence"
    producer_reconstruction = "complete-rank-reconstruction"
    symmetry_inventory = "symmetry-related-point-inventory"


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceSourceEvidence:
    role: CommonSpaceEvidenceRole
    expected: Wannier90NativeArtifactIdentity
    artifact: Wannier90NativeArtifact

    def __post_init__(self) -> None:
        if (
            type(self.role) is not CommonSpaceEvidenceRole
            or type(self.expected) is not Wannier90NativeArtifactIdentity
            or type(self.artifact) is not Wannier90NativeArtifact
        ):
            raise TypeError("source evidence must use exact role and provider records")


class CommonSpaceVerificationJson:
    """Independent wire mechanics; never import producer comparison/serialization."""

    @staticmethod
    def encode(value: JsonValue) -> bytes:
        return (
            json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"
        ).encode()

    @staticmethod
    def decode(payload: bytes) -> JsonValue:
        if type(payload) is not bytes:
            raise TypeError("JSON payload must be immutable bytes")

        def pairs(values: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
            result: dict[str, JsonValue] = {}
            for key, value in values:
                if key in result:
                    raise ValueError("duplicate JSON key")
                result[key] = value
            return result

        def nonfinite(value: str) -> JsonValue:
            raise ValueError(f"nonfinite JSON constant: {value}")

        def finite_float(value: str) -> float:
            number = float(value)
            if not isfinite(number):
                raise ValueError("nonfinite JSON numeric value")
            return number

        result: JsonValue = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_constant=nonfinite,
            parse_float=finite_float,
        )
        return result

    @staticmethod
    def rational(value: Fraction) -> JsonValue:
        if type(value) is not Fraction:
            raise TypeError("rational wire encoding requires a built-in Fraction")
        return [hex(value.numerator), hex(value.denominator)]

    @staticmethod
    def read_rational(value: JsonValue) -> Fraction:
        """Decode canonical hexadecimal integer strings only at this wire boundary."""
        if type(value) is not list or len(value) != 2:
            raise ValueError("rational wire value must contain two hexadecimal strings")
        numerator, denominator = value
        if type(numerator) is not str or type(denominator) is not str:
            raise ValueError("rational wire components must be strings")
        top, bottom = int(numerator, 16), int(denominator, 16)
        if bottom <= 0:
            raise ValueError("rational denominator must be positive")
        result = Fraction(top, bottom)
        if [hex(result.numerator), hex(result.denominator)] != value:
            raise ValueError("rational wire value is not canonical")
        return result

    @staticmethod
    def identity(value: Wannier90NativeArtifactIdentity) -> JsonValue:
        return {
            "name": value.name,
            "byte_count": value.byte_count,
            "sha256": value.sha256,
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceSourceAdmission:
    """Verify all source identities and a separately reviewed semantic assertion.

    Expected identities and review reference must come from an upstream reviewed
    declaration, not observed bytes. This class checks exact correlation to that trust
    root; it cannot prove the truth or authorship of a supplied scientific assertion.
    Higher arithmetic precision is not an admission prerequisite: decisive error
    bounds and independent agreement need no extra precision artifact. Arithmetic
    ambiguity or comparison disagreement still cannot pass the numerical gate.
    No review flag grants execution authority. Native source paths are not accepted,
    so there is no path-resolution fallback or repository-root escape at this API.
    """

    producer_prerequisite_roles: ClassVar[tuple[CommonSpaceEvidenceRole, ...]] = (
        CommonSpaceEvidenceRole.producer_reconstruction,
        CommonSpaceEvidenceRole.symmetry_inventory,
    )

    parsed_inputs: CommonSpaceParsedNativeInputs
    rounding_model: CommonSpaceNativeRoundingModel
    frozen_rank_threshold: Fraction
    review_scope: CommonSpaceReviewScope
    review_reference: str
    parent_band_state_identity: str
    gauge_state_identity: str
    evidence: tuple[CommonSpaceSourceEvidence, ...]

    def __post_init__(self) -> None:
        if type(self.parsed_inputs) is not CommonSpaceParsedNativeInputs:
            raise TypeError("parsed_inputs must use the exact parsed native record")
        if type(self.rounding_model) is not CommonSpaceNativeRoundingModel:
            raise TypeError("rounding_model must be explicit")
        if (
            type(self.frozen_rank_threshold) is not Fraction
            or self.frozen_rank_threshold < 0
        ):
            raise ValueError("frozen threshold must be a nonnegative built-in Fraction")
        if type(self.review_scope) is not CommonSpaceReviewScope:
            raise TypeError("review_scope must be a CommonSpaceReviewScope")
        if any(
            type(value) is not str or not value
            for value in (
                self.review_reference,
                self.parent_band_state_identity,
                self.gauge_state_identity,
            )
        ):
            raise ValueError("review, band-space and gauge identities must be explicit")
        if type(self.evidence) is not tuple or any(
            type(value) is not CommonSpaceSourceEvidence for value in self.evidence
        ):
            raise TypeError("evidence must be a typed immutable tuple")
        if tuple(value.role for value in self.evidence) != tuple(
            CommonSpaceEvidenceRole
        ):
            raise ValueError("complete ordered source evidence inventory is required")
        contract = self.parsed_inputs.contract
        if (
            contract.parent_band_count != 20
            or len(contract.ordered_fractional_kpoints) != 216
        ):
            raise ValueError(
                "C6 admission requires 216 points, 20 parent bands and rank ten"
            )
        # Uniqueness is already required by the native contract. Together with
        # 216 points and six declared values per axis this proves Cartesian coverage.
        # Axis values/physical spacings still require review: never snap or infer them.
        if any(
            len({point[axis] for point in contract.ordered_fractional_kpoints}) != 6
            for axis in range(3)
        ):
            raise ValueError(
                "C6 source must contain the complete declared six-by-six-by-six grid"
            )
        if contract.ordered_fractional_kpoints[0] != (0.0, 0.0, 0.0):
            raise ValueError("C6 ordered source must begin at Gamma")

    def assertion_payload(self) -> bytes:
        """Canonical assertion expected from review; generating it is not admission."""
        wire = CommonSpaceVerificationJson
        contract = self.parsed_inputs.contract
        values: dict[str, JsonValue] = {
            "record_type": "common-space-source-assertions-v1",
            "review_scope": self.review_scope.to_wire(),
            "review_reference": self.review_reference,
            "parent_band_state_identity": self.parent_band_state_identity,
            "gauge_state_identity": self.gauge_state_identity,
            "geometry_identity": contract.geometry_identity,
            "energy_reference_identity": contract.energy_reference_identity,
            "operator_energy_unit": "electronvolt",
            "overlap_unit": "dimensionless",
            "spin_convention": "spinless scalar-relativistic non-SOC",
            "point_order_convention": "Gamma-origin-6-cubed-declared-order",
            "ordered_fractional_kpoints": [
                list(point) for point in contract.ordered_fractional_kpoints
            ],
            "parent_band_count": 20,
            "retained_rank": 10,
            "atomic_basis_order": list(contract.atomic_basis_order),
            "trial_convention": contract.trial_convention.to_wire(),
            "native_identities": [
                wire.identity(value) for value in contract.identities
            ],
            "native_component_errors": [
                wire.rational(self.rounding_model.amn_component_error),
                wire.rational(self.rounding_model.gauge_component_error),
                wire.rational(self.rounding_model.disentanglement_component_error),
            ],
            "parsing_assumption": "correctly-rounded-IEEE-binary64",
            "frozen_rank_threshold": wire.rational(self.frozen_rank_threshold),
            "source_ledger": [
                {"role": item.role.to_wire(), "identity": wire.identity(item.expected)}
                for item in self.evidence
                if item.role
                not in (
                    CommonSpaceEvidenceRole.state_assertions,
                    CommonSpaceEvidenceRole.producer_completion,
                    *self.producer_prerequisite_roles,
                )
            ],
        }
        return wire.encode(values)

    def authenticate(self) -> None:
        """Check all evidence bytes before inspecting reviewed prerequisite assertions."""
        self.parsed_inputs.provider_binding.authenticate()
        Wannier90NativeArtifactCorrelator().execute(
            expected_identities=tuple(value.expected for value in self.evidence),
            artifacts=tuple(value.artifact for value in self.evidence),
        )
        by_role = {value.role: value for value in self.evidence}
        assertion = by_role[CommonSpaceEvidenceRole.state_assertions]
        wire = CommonSpaceVerificationJson
        if (
            wire.encode(wire.decode(assertion.artifact.payload))
            != self.assertion_payload()
        ):
            raise ValueError(
                "reviewed source assertions do not match the native/precision contract"
            )
        completion = wire.decode(
            by_role[CommonSpaceEvidenceRole.producer_completion].artifact.payload
        )
        expected_completion: dict[str, JsonValue] = {
            "record_type": "common-space-producer-prerequisites-v1",
            "state_assertions_sha256": assertion.expected.sha256,
            "full_grid_reconstruction_complete": True,
            "symmetry_inventory_complete": True,
            "completed_evidence": [
                {
                    "role": role.to_wire(),
                    "identity": wire.identity(by_role[role].expected),
                }
                for role in self.producer_prerequisite_roles
            ],
            "review_scope": self.review_scope.to_wire(),
        }
        if wire.encode(completion) != wire.encode(expected_completion):
            raise ValueError(
                "complete source-bound producer prerequisite evidence is required"
            )
