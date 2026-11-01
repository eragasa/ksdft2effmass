"""Canonical replaceable cache for development-only higher-rank results.

Cache admission establishes byte integrity, canonical typed decoding, and complete case
inventory only.  It is explicitly not independent scientific verification and cannot
promote development results into retained evidence.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Self, final

from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DRankNAlignmentCalculationResult,
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

_CACHE_FORMAT = "ksdft2effmass.higher-rank-development-result-cache.v1"
_CACHE_ROLE = "replaceable-development-result-cache"
_ADMISSION_ROLE = "replaceable-development-cache-integrity-admission"
_ADMISSION_METHOD = "canonical-typed-byte-integrity-and-inventory.v1"
_MANIFEST_FILE_NAME = "manifest.json"
_ADMISSION_FILE_NAME = "admission.json"


def _sha256(wire: bytes) -> str:
    return hashlib.sha256(wire).hexdigest()


def _validate_digest(value: str, name: str) -> None:
    if type(value) is not str or len(value) != 64:
        raise ValueError(f"{name} must be a 64-character SHA-256 digest")
    if any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{name} must use lowercase hexadecimal")


def _exact_fields(
    values: Mapping[str, SerializableValue], expected: frozenset[str]
) -> None:
    if frozenset(values) != expected:
        raise ValueError("cache record fields do not match the closed contract")


def _string(values: Mapping[str, SerializableValue], key: str) -> str:
    value = values[key]
    if type(value) is not str:
        raise TypeError(f"{key} must be a built-in string")
    return value


def _integer(values: Mapping[str, SerializableValue], key: str) -> int:
    value = values[key]
    if type(value) is not int:
        raise TypeError(f"{key} must be a built-in integer")
    return value


def _boolean(values: Mapping[str, SerializableValue], key: str) -> bool:
    value = values[key]
    if type(value) is not bool:
        raise TypeError(f"{key} must be a built-in boolean")
    return value


def _mapping(value: SerializableValue, name: str) -> Mapping[str, SerializableValue]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return value


def _atomic_write(destination: Path, wire: bytes) -> None:
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.write_bytes(wire)
    temporary.replace(destination)


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankDevelopmentCacheEntry(BaseTypedRecord):
    """Bind one canonical result file to its exact case and digest."""

    case_identity: str
    retained_rank: int
    circuit_depth: int
    file_name: str
    result_sha256: str
    byte_count: int

    def __post_init__(self) -> None:
        if type(self.case_identity) is not str or not self.case_identity:
            raise ValueError("case_identity must be a nonempty built-in string")
        if (
            self.retained_rank
            not in Periodic1DRankNAlignmentConfiguration.RETAINED_RANKS
        ):
            raise ValueError("retained_rank is outside the frozen inventory")
        if (
            self.circuit_depth
            not in Periodic1DRankNAlignmentConfiguration.CIRCUIT_DEPTHS
        ):
            raise ValueError("circuit_depth is outside the frozen inventory")
        expected_file_name = f"result-r{self.retained_rank}-l{self.circuit_depth}.json"
        if self.file_name != expected_file_name:
            raise ValueError("file_name must be the canonical case file name")
        _validate_digest(self.result_sha256, "result_sha256")
        if type(self.byte_count) is not int or self.byte_count <= 0:
            raise ValueError("byte_count must be a positive built-in integer")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "case_identity": self.case_identity,
            "retained_rank": self.retained_rank,
            "circuit_depth": self.circuit_depth,
            "file_name": self.file_name,
            "result_sha256": self.result_sha256,
            "byte_count": self.byte_count,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _exact_fields(
            values,
            frozenset(
                {
                    "case_identity",
                    "retained_rank",
                    "circuit_depth",
                    "file_name",
                    "result_sha256",
                    "byte_count",
                }
            ),
        )
        return cls(
            case_identity=_string(values, "case_identity"),
            retained_rank=_integer(values, "retained_rank"),
            circuit_depth=_integer(values, "circuit_depth"),
            file_name=_string(values, "file_name"),
            result_sha256=_string(values, "result_sha256"),
            byte_count=_integer(values, "byte_count"),
        )


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankDevelopmentCacheManifest(BaseTypedRecord):
    """Describe the complete canonical development-result cache."""

    artifact_role: str
    scientific_evidence: bool
    cache_format: str
    family_identity: str
    version_identity: str
    calculation_infrastructure_sha256: str
    entries: tuple[HigherRankDevelopmentCacheEntry, ...]

    def __post_init__(self) -> None:
        if self.artifact_role != _CACHE_ROLE:
            raise ValueError("artifact_role must identify the development cache")
        if self.scientific_evidence is not False:
            raise ValueError("development cache cannot claim scientific evidence")
        if self.cache_format != _CACHE_FORMAT:
            raise ValueError("cache_format is unsupported")
        configuration = Periodic1DRankNAlignmentConfiguration
        if self.family_identity != configuration.FAMILY_IDENTITY:
            raise ValueError("family_identity does not match the frozen family")
        if self.version_identity != configuration.VERSION_IDENTITY:
            raise ValueError("version_identity does not match the frozen version")
        _validate_digest(
            self.calculation_infrastructure_sha256,
            "calculation_infrastructure_sha256",
        )
        if type(self.entries) is not tuple or any(
            type(entry) is not HigherRankDevelopmentCacheEntry for entry in self.entries
        ):
            raise TypeError("entries must contain exact cache-entry records")
        expected = tuple(
            (rank, depth)
            for rank in configuration.RETAINED_RANKS
            for depth in configuration.CIRCUIT_DEPTHS
        )
        actual = tuple(
            (entry.retained_rank, entry.circuit_depth) for entry in self.entries
        )
        if actual != expected:
            raise ValueError("entries must match the complete frozen case order")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "artifact_role": self.artifact_role,
            "scientific_evidence": self.scientific_evidence,
            "cache_format": self.cache_format,
            "family_identity": self.family_identity,
            "version_identity": self.version_identity,
            "calculation_infrastructure_sha256": (
                self.calculation_infrastructure_sha256
            ),
            "entries": self.entries,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _exact_fields(
            values,
            frozenset(
                {
                    "artifact_role",
                    "scientific_evidence",
                    "cache_format",
                    "family_identity",
                    "version_identity",
                    "calculation_infrastructure_sha256",
                    "entries",
                }
            ),
        )
        entries_value = values["entries"]
        if type(entries_value) is not tuple:
            raise TypeError("entries must decode as a tuple")
        entries = tuple(
            HigherRankDevelopmentCacheEntry.from_dict(
                _mapping(item, f"entries[{index}]")
            )
            for index, item in enumerate(entries_value)
        )
        return cls(
            artifact_role=_string(values, "artifact_role"),
            scientific_evidence=_boolean(values, "scientific_evidence"),
            cache_format=_string(values, "cache_format"),
            family_identity=_string(values, "family_identity"),
            version_identity=_string(values, "version_identity"),
            calculation_infrastructure_sha256=_string(
                values, "calculation_infrastructure_sha256"
            ),
            entries=entries,
        )


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankDevelopmentCacheAdmission(BaseTypedRecord):
    """Bind successful cache-integrity checks to exact manifest bytes."""

    artifact_role: str
    scientific_evidence: bool
    independent_scientific_verification: bool
    cache_format: str
    admission_method: str
    manifest_sha256: str
    canonical_manifest_pass: bool
    entry_digest_pass: bool
    exact_result_round_trip_pass: bool
    complete_case_inventory_pass: bool

    def __post_init__(self) -> None:
        if self.artifact_role != _ADMISSION_ROLE:
            raise ValueError("artifact_role must identify cache-integrity admission")
        if self.scientific_evidence is not False:
            raise ValueError("cache admission cannot claim scientific evidence")
        if self.independent_scientific_verification is not False:
            raise ValueError(
                "cache admission is not independent scientific verification"
            )
        if self.cache_format != _CACHE_FORMAT:
            raise ValueError("cache_format is unsupported")
        if self.admission_method != _ADMISSION_METHOD:
            raise ValueError("admission_method is unsupported")
        _validate_digest(self.manifest_sha256, "manifest_sha256")
        checks = (
            self.canonical_manifest_pass,
            self.entry_digest_pass,
            self.exact_result_round_trip_pass,
            self.complete_case_inventory_pass,
        )
        if any(value is not True for value in checks):
            raise ValueError("cache admission requires every integrity check to pass")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "artifact_role": self.artifact_role,
            "scientific_evidence": self.scientific_evidence,
            "independent_scientific_verification": (
                self.independent_scientific_verification
            ),
            "cache_format": self.cache_format,
            "admission_method": self.admission_method,
            "manifest_sha256": self.manifest_sha256,
            "canonical_manifest_pass": self.canonical_manifest_pass,
            "entry_digest_pass": self.entry_digest_pass,
            "exact_result_round_trip_pass": self.exact_result_round_trip_pass,
            "complete_case_inventory_pass": self.complete_case_inventory_pass,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = frozenset(
            {
                "artifact_role",
                "scientific_evidence",
                "independent_scientific_verification",
                "cache_format",
                "admission_method",
                "manifest_sha256",
                "canonical_manifest_pass",
                "entry_digest_pass",
                "exact_result_round_trip_pass",
                "complete_case_inventory_pass",
            }
        )
        _exact_fields(values, fields)
        return cls(
            artifact_role=_string(values, "artifact_role"),
            scientific_evidence=_boolean(values, "scientific_evidence"),
            independent_scientific_verification=_boolean(
                values, "independent_scientific_verification"
            ),
            cache_format=_string(values, "cache_format"),
            admission_method=_string(values, "admission_method"),
            manifest_sha256=_string(values, "manifest_sha256"),
            canonical_manifest_pass=_boolean(values, "canonical_manifest_pass"),
            entry_digest_pass=_boolean(values, "entry_digest_pass"),
            exact_result_round_trip_pass=_boolean(
                values, "exact_result_round_trip_pass"
            ),
            complete_case_inventory_pass=_boolean(
                values, "complete_case_inventory_pass"
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankDevelopmentCacheWriteRequest:
    """Bind complete calculated results and one replaceable cache directory."""

    calculation_results: tuple[Periodic1DRankNAlignmentCalculationResult, ...]
    cache_directory: Path
    calculation_infrastructure_sha256: str

    def __post_init__(self) -> None:
        if type(self.calculation_results) is not tuple or any(
            type(result) is not Periodic1DRankNAlignmentCalculationResult
            for result in self.calculation_results
        ):
            raise TypeError("calculation_results must contain exact result records")
        if not isinstance(self.cache_directory, Path):
            raise TypeError("cache_directory must be pathlib.Path")
        _validate_digest(
            self.calculation_infrastructure_sha256,
            "calculation_infrastructure_sha256",
        )
        expected = tuple(
            (rank, depth)
            for rank in Periodic1DRankNAlignmentConfiguration.RETAINED_RANKS
            for depth in Periodic1DRankNAlignmentConfiguration.CIRCUIT_DEPTHS
        )
        actual = tuple(
            (result.request.retained_rank, result.request.circuit_depth)
            for result in self.calculation_results
        )
        if actual != expected:
            raise ValueError("calculation_results must match the complete case order")


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankDevelopmentCacheReadRequest:
    """Bind one replaceable development-cache directory."""

    cache_directory: Path

    def __post_init__(self) -> None:
        if not isinstance(self.cache_directory, Path):
            raise TypeError("cache_directory must be pathlib.Path")


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankDevelopmentCacheReadResult:
    """Return admitted manifest identity and complete reconstructed results."""

    manifest: HigherRankDevelopmentCacheManifest
    manifest_sha256: str
    calculation_results: tuple[Periodic1DRankNAlignmentCalculationResult, ...]

    def __post_init__(self) -> None:
        if type(self.manifest) is not HigherRankDevelopmentCacheManifest:
            raise TypeError("manifest must be the exact cache-manifest record")
        _validate_digest(self.manifest_sha256, "manifest_sha256")
        if type(self.calculation_results) is not tuple or any(
            type(result) is not Periodic1DRankNAlignmentCalculationResult
            for result in self.calculation_results
        ):
            raise TypeError("calculation_results must contain exact result records")


@final
class HigherRankDevelopmentCacheWriter:
    """Write one canonical result file per case and one canonical manifest."""

    __slots__ = ("_request",)

    def __init__(self, request: HigherRankDevelopmentCacheWriteRequest) -> None:
        if type(request) is not HigherRankDevelopmentCacheWriteRequest:
            raise TypeError("request must be HigherRankDevelopmentCacheWriteRequest")
        self._request = request

    @property
    def request(self) -> HigherRankDevelopmentCacheWriteRequest:
        return self._request

    def execute(self) -> HigherRankDevelopmentCacheManifest:
        destination = self.request.cache_directory
        destination.mkdir(parents=True, exist_ok=True)
        entries: list[HigherRankDevelopmentCacheEntry] = []
        for result in self.request.calculation_results:
            wire = result.to_json()
            rank = result.request.retained_rank
            depth = result.request.circuit_depth
            file_name = f"result-r{rank}-l{depth}.json"
            _atomic_write(destination / file_name, wire)
            entries.append(
                HigherRankDevelopmentCacheEntry(
                    case_identity=result.request.case_identity,
                    retained_rank=rank,
                    circuit_depth=depth,
                    file_name=file_name,
                    result_sha256=_sha256(wire),
                    byte_count=len(wire),
                )
            )
        configuration = self.request.calculation_results[0].request.configuration
        manifest = HigherRankDevelopmentCacheManifest(
            artifact_role=_CACHE_ROLE,
            scientific_evidence=False,
            cache_format=_CACHE_FORMAT,
            family_identity=configuration.family_identity,
            version_identity=configuration.version_identity,
            calculation_infrastructure_sha256=(
                self.request.calculation_infrastructure_sha256
            ),
            entries=tuple(entries),
        )
        _atomic_write(destination / _MANIFEST_FILE_NAME, manifest.to_json())
        return manifest


@final
class HigherRankDevelopmentCacheReader:
    """Read and validate canonical cache bytes without claiming verification."""

    __slots__ = ("_request",)

    def __init__(self, request: HigherRankDevelopmentCacheReadRequest) -> None:
        if type(request) is not HigherRankDevelopmentCacheReadRequest:
            raise TypeError("request must be HigherRankDevelopmentCacheReadRequest")
        self._request = request

    @property
    def request(self) -> HigherRankDevelopmentCacheReadRequest:
        return self._request

    def execute(self) -> HigherRankDevelopmentCacheReadResult:
        directory = self.request.cache_directory
        manifest_wire = (directory / _MANIFEST_FILE_NAME).read_bytes()
        manifest = HigherRankDevelopmentCacheManifest.from_json(manifest_wire)
        if manifest.to_json() != manifest_wire:
            raise ValueError("manifest bytes are not canonical")
        results: list[Periodic1DRankNAlignmentCalculationResult] = []
        for entry in manifest.entries:
            wire = (directory / entry.file_name).read_bytes()
            if len(wire) != entry.byte_count:
                raise ValueError(f"cached byte count changed for {entry.file_name}")
            if _sha256(wire) != entry.result_sha256:
                raise ValueError(f"cached digest changed for {entry.file_name}")
            result = Periodic1DRankNAlignmentCalculationResult.from_json(wire)
            if result.to_json() != wire:
                raise ValueError(f"cached result is not canonical: {entry.file_name}")
            if (
                result.request.case_identity != entry.case_identity
                or result.request.retained_rank != entry.retained_rank
                or result.request.circuit_depth != entry.circuit_depth
            ):
                raise ValueError(f"cached result identity changed: {entry.file_name}")
            results.append(result)
        return HigherRankDevelopmentCacheReadResult(
            manifest=manifest,
            manifest_sha256=_sha256(manifest_wire),
            calculation_results=tuple(results),
        )


@final
class HigherRankDevelopmentCacheIntegrityVerifier:
    """Admit exact cache bytes after canonical integrity and inventory checks."""

    __slots__ = ("_request",)

    def __init__(self, request: HigherRankDevelopmentCacheReadRequest) -> None:
        if type(request) is not HigherRankDevelopmentCacheReadRequest:
            raise TypeError("request must be HigherRankDevelopmentCacheReadRequest")
        self._request = request

    @property
    def request(self) -> HigherRankDevelopmentCacheReadRequest:
        return self._request

    def execute(self) -> HigherRankDevelopmentCacheAdmission:
        loaded = HigherRankDevelopmentCacheReader(self.request).execute()
        admission = HigherRankDevelopmentCacheAdmission(
            artifact_role=_ADMISSION_ROLE,
            scientific_evidence=False,
            independent_scientific_verification=False,
            cache_format=_CACHE_FORMAT,
            admission_method=_ADMISSION_METHOD,
            manifest_sha256=loaded.manifest_sha256,
            canonical_manifest_pass=True,
            entry_digest_pass=True,
            exact_result_round_trip_pass=True,
            complete_case_inventory_pass=True,
        )
        _atomic_write(
            self.request.cache_directory / _ADMISSION_FILE_NAME,
            admission.to_json(),
        )
        return admission


@final
class HigherRankDevelopmentAdmittedCacheReader:
    """Read cache results only when exact integrity admission matches the manifest."""

    __slots__ = ("_request",)

    def __init__(self, request: HigherRankDevelopmentCacheReadRequest) -> None:
        if type(request) is not HigherRankDevelopmentCacheReadRequest:
            raise TypeError("request must be HigherRankDevelopmentCacheReadRequest")
        self._request = request

    @property
    def request(self) -> HigherRankDevelopmentCacheReadRequest:
        return self._request

    def execute(self) -> HigherRankDevelopmentCacheReadResult:
        admission_wire = (
            self.request.cache_directory / _ADMISSION_FILE_NAME
        ).read_bytes()
        admission = HigherRankDevelopmentCacheAdmission.from_json(admission_wire)
        if admission.to_json() != admission_wire:
            raise ValueError("cache admission bytes are not canonical")
        loaded = HigherRankDevelopmentCacheReader(self.request).execute()
        if admission.manifest_sha256 != loaded.manifest_sha256:
            raise ValueError("cache admission does not bind the current manifest")
        return loaded


__all__ = [
    "HigherRankDevelopmentAdmittedCacheReader",
    "HigherRankDevelopmentCacheAdmission",
    "HigherRankDevelopmentCacheEntry",
    "HigherRankDevelopmentCacheIntegrityVerifier",
    "HigherRankDevelopmentCacheManifest",
    "HigherRankDevelopmentCacheReadRequest",
    "HigherRankDevelopmentCacheReadResult",
    "HigherRankDevelopmentCacheReader",
    "HigherRankDevelopmentCacheWriteRequest",
    "HigherRankDevelopmentCacheWriter",
]
