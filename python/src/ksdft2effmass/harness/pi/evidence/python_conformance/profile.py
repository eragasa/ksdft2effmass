"""Closed version-one Python test-evidence profile policy loading."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

EVIDENCE_CLASSES = frozenset(
    {
        "software_verification",
        "numerical_verification",
        "scientific_validation",
        "uncertainty_quantification",
    }
)
PROFILE_IDS = frozenset({"routine", "claim_bearing"})
MODULE_FIELDS = frozenset(
    {"Evidence profile", "Bounded artifact scope", "VVUQ and scientific exclusions"}
)
TEST_FIELDS = frozenset(
    {
        "Evidence ID",
        "Requirement",
        "Method",
        "Oracle",
        "Acceptance",
        "Interpretation",
        "Limitations",
        "Provenance",
    }
)
PROFILE_KEYS = {
    "profile_id",
    "behavior_version",
    "required_module_metadata",
    "optional_module_metadata",
    "forbidden_module_metadata",
    "required_test_fields",
    "optional_test_fields",
    "forbidden_test_fields",
    "identifier_requirement",
    "oracle_requirement",
    "acceptance_requirement",
    "limitations_requirement",
    "provenance_requirement",
    "migration_requirement",
}


@dataclass(frozen=True, slots=True)
class EvidenceProfilePolicy:
    """One immutable validated evidence-profile rule set, retaining all policy."""

    profile_id: str
    required_module_metadata: tuple[str, ...]
    optional_module_metadata: tuple[str, ...]
    forbidden_module_metadata: tuple[str, ...]
    required_test_fields: tuple[str, ...]
    optional_test_fields: tuple[str, ...]
    forbidden_test_fields: tuple[str, ...]
    identifier_requirement: str
    oracle_requirement: str
    acceptance_requirement: str
    limitations_requirement: str
    provenance_requirement: str
    migration_requirement: str


@dataclass(frozen=True, slots=True)
class EvidenceProfileMatrix:
    """Closed immutable evidence-class/profile compatibility policy."""

    profiles: Mapping[str, EvidenceProfilePolicy]
    combinations: frozenset[tuple[str, str]]


def _string_array(value: Any, allowed: frozenset[str]) -> tuple[str, ...] | None:
    if (
        type(value) is not list
        or any(type(item) is not str or item not in allowed for item in value)
        or len(value) != len(set(value))
        or value != sorted(value)
    ):
        return None
    return tuple(value)


def _load_profile_matrix(
    payload: bytes,
) -> tuple[EvidenceProfileMatrix | None, str | None]:
    """Load the exact closed behavior-version-one policy resource.

    The function owns generic profile-resource shape and semantic closure.  It
    performs no filesystem access and reports one deterministic diagnostic text
    rather than partially accepting malformed policy.
    """
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if type(value) is not dict or set(value) != {
        "schema_version",
        "behavior_version",
        "evidence_classes",
        "profiles",
        "combinations",
    }:
        return None, "profile matrix must be a closed versioned object"
    if value["schema_version"] != 1 or value["behavior_version"] != 1:
        return None, "profile matrix supports only schema and behavior version 1"
    classes = _string_array(value["evidence_classes"], EVIDENCE_CLASSES)
    if classes is None or frozenset(classes) != EVIDENCE_CLASSES:
        return None, "profile matrix must declare every supported evidence class"
    raw_profiles = value["profiles"]
    if type(raw_profiles) is not list:
        return None, "profiles must be an array"
    profiles: dict[str, EvidenceProfilePolicy] = {}
    for item in raw_profiles:
        if type(item) is not dict or set(item) != PROFILE_KEYS:
            return None, "each profile must use the exact version-one fields"
        profile_id = item["profile_id"]
        if type(profile_id) is not str or profile_id not in PROFILE_IDS:
            return None, "profile identity is unsupported"
        if profile_id in profiles or item["behavior_version"] != 1:
            return None, "profile identities must be unique at behavior version 1"
        module_groups = tuple(
            _string_array(item[name], MODULE_FIELDS)
            for name in (
                "required_module_metadata",
                "optional_module_metadata",
                "forbidden_module_metadata",
            )
        )
        test_groups = tuple(
            _string_array(item[name], TEST_FIELDS)
            for name in (
                "required_test_fields",
                "optional_test_fields",
                "forbidden_test_fields",
            )
        )
        if any(group is None for group in module_groups + test_groups):
            return None, "profile requirement declarations are malformed"
        module_values = tuple(item for group in module_groups for item in group or ())
        test_values = tuple(item for group in test_groups for item in group or ())
        if len(module_values) != len(set(module_values)) or len(test_values) != len(
            set(test_values)
        ):
            return (
                None,
                "required, optional, and forbidden declarations must be disjoint",
            )
        for name, allowed in (
            ("identifier_requirement", {"required"}),
            ("oracle_requirement", {"required", "optional"}),
            ("acceptance_requirement", {"required"}),
            ("limitations_requirement", {"required", "optional"}),
            (
                "provenance_requirement",
                {"optional", "required_when_external_reference"},
            ),
            ("migration_requirement", {"required_when_predecessor_exists"}),
        ):
            if item[name] not in allowed:
                return None, f"{name} declaration is unsupported"
        profiles[profile_id] = EvidenceProfilePolicy(
            profile_id,
            tuple(item["required_module_metadata"]),
            tuple(item["optional_module_metadata"]),
            tuple(item["forbidden_module_metadata"]),
            tuple(item["required_test_fields"]),
            tuple(item["optional_test_fields"]),
            tuple(item["forbidden_test_fields"]),
            item["identifier_requirement"],
            item["oracle_requirement"],
            item["acceptance_requirement"],
            item["limitations_requirement"],
            item["provenance_requirement"],
            item["migration_requirement"],
        )
    if frozenset(profiles) != PROFILE_IDS:
        return (
            None,
            "profile matrix must declare routine and claim_bearing exactly once",
        )
    raw_combinations = value["combinations"]
    if type(raw_combinations) is not list:
        return None, "combinations must be an array"
    combinations: list[tuple[str, str]] = []
    for item in raw_combinations:
        if type(item) is not dict or set(item) != {
            "evidence_class",
            "evidence_profile",
        }:
            return None, "combination declarations are malformed"
        pair = (item["evidence_class"], item["evidence_profile"])
        if pair[0] not in EVIDENCE_CLASSES or pair[1] not in PROFILE_IDS:
            return None, "combination declaration is unsupported"
        combinations.append(pair)
    expected = frozenset(
        {
            ("software_verification", "routine"),
            ("software_verification", "claim_bearing"),
            ("numerical_verification", "claim_bearing"),
            ("scientific_validation", "claim_bearing"),
            ("uncertainty_quantification", "claim_bearing"),
        }
    )
    if (
        len(combinations) != len(set(combinations))
        or frozenset(combinations) != expected
    ):
        return None, "class/profile combinations must be unique and complete"
    return (
        EvidenceProfileMatrix(MappingProxyType(profiles), frozenset(combinations)),
        None,
    )


class _EvidenceProfileMatrixLoader:
    """Own closed generic evidence-profile matrix loading."""

    __slots__ = ()

    def execute(
        self, payload: bytes
    ) -> tuple[EvidenceProfileMatrix | None, str | None]:
        """Load one explicit profile matrix without filesystem access."""
        return _load_profile_matrix(payload)


class _EvidenceProfileCombinationRule:
    """Own evidence-class/profile combination compatibility."""

    __slots__ = ()

    def execute(
        self,
        entries: tuple[dict[str, Any], ...],
        matrix: EvidenceProfileMatrix,
    ) -> tuple[tuple[str, str], ...]:
        """Return one deterministic finding per unsupported declaration."""
        return tuple(
            (
                "TE.PROFILE_COMBINATION",
                "evidence_class/evidence_profile combination is unsupported",
            )
            for entry in entries
            if entry.get("evidence_profile") is not None
            and (entry.get("evidence_class"), entry.get("evidence_profile"))
            not in matrix.combinations
        )
