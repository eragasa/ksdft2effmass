"""Typed direct-lifecycle records for band-equivalence locality calculations."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from types import MappingProxyType
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .verification import BandEquivalenceLocalityVerification
from .visualizations.data import BandEquivalenceLocalityVisualizationData


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityExecution(BaseTypedRecord):
    """Describe one completed unsealed direct calculation execution."""

    schema_version: int
    calculation_family: str
    study_family: str
    execution_id: str
    created_utc: str
    outcome: str
    evidence_status: str
    configuration_path: str
    configuration_sha256: str
    result_path: str
    result_sha256: str
    script_sha256: str
    software_versions: Mapping[str, str]
    claim_boundary: str
    sealed: bool

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be a built-in integer")
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        for value, name in (
            (self.calculation_family, "calculation_family"),
            (self.study_family, "study_family"),
            (self.execution_id, "execution_id"),
            (self.created_utc, "created_utc"),
            (self.outcome, "outcome"),
            (self.evidence_status, "evidence_status"),
            (self.configuration_path, "configuration_path"),
            (self.result_path, "result_path"),
            (self.claim_boundary, "claim_boundary"),
        ):
            if type(value) is not str or not value:
                raise TypeError(f"{name} must be a nonempty built-in string")
        try:
            created = datetime.fromisoformat(self.created_utc)
        except ValueError as error:
            raise ValueError("created_utc must be an ISO-8601 timestamp") from error
        if created.utcoffset() != timedelta(0):
            raise ValueError("created_utc must identify UTC")
        if self.outcome != "completed":
            raise ValueError("outcome must be completed")
        if self.evidence_status != "calculated result — unsealed":
            raise ValueError("evidence_status must identify an unsealed result")
        if self.configuration_path != "inputs/configuration.json":
            raise ValueError("configuration_path must identify the typed request")
        if self.result_path != "results/result.json":
            raise ValueError("result_path must identify the typed result")
        for digest, name in (
            (self.configuration_sha256, "configuration_sha256"),
            (self.result_sha256, "result_sha256"),
            (self.script_sha256, "script_sha256"),
        ):
            if (
                type(digest) is not str
                or len(digest) != 64
                or any(character not in "0123456789abcdef" for character in digest)
            ):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
        if not isinstance(self.software_versions, Mapping):
            raise TypeError("software_versions must be a mapping")
        versions: dict[str, str] = {}
        for name, value in self.software_versions.items():
            if type(name) is not str or not name:
                raise TypeError("software-version names must be nonempty strings")
            if type(value) is not str or not value:
                raise TypeError("software-version values must be nonempty strings")
            versions[name] = value
        required_versions = {
            "ksdft2effmass",
            "numpy",
            "projectkoios-optimization",
            "projectkoios-physkit",
            "scipy",
        }
        if set(versions) != required_versions:
            raise ValueError("software_versions must match the direct inventory")
        object.__setattr__(
            self,
            "software_versions",
            MappingProxyType(dict(sorted(versions.items()))),
        )
        if type(self.sealed) is not bool:
            raise TypeError("sealed must be a built-in boolean")
        if self.sealed:
            raise ValueError("sealed must be false")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "schema_version": self.schema_version,
            "calculation_family": self.calculation_family,
            "study_family": self.study_family,
            "execution_id": self.execution_id,
            "created_utc": self.created_utc,
            "outcome": self.outcome,
            "evidence_status": self.evidence_status,
            "configuration_path": self.configuration_path,
            "configuration_sha256": self.configuration_sha256,
            "result_path": self.result_path,
            "result_sha256": self.result_sha256,
            "script_sha256": self.script_sha256,
            "software_versions": self.software_versions,
            "claim_boundary": self.claim_boundary,
            "sealed": self.sealed,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "schema_version",
            "calculation_family",
            "study_family",
            "execution_id",
            "created_utc",
            "outcome",
            "evidence_status",
            "configuration_path",
            "configuration_sha256",
            "result_path",
            "result_sha256",
            "script_sha256",
            "software_versions",
            "claim_boundary",
            "sealed",
        }
        if set(values) != required:
            raise ValueError("band-equivalence execution fields do not match")
        software_versions = values["software_versions"]
        if not isinstance(software_versions, Mapping):
            raise TypeError("software_versions must decode to a mapping")
        typed_versions: dict[str, str] = {}
        for name, value in software_versions.items():
            if type(name) is not str or type(value) is not str:
                raise TypeError("software versions must decode to strings")
            typed_versions[name] = value
        schema_version = values["schema_version"]
        sealed = values["sealed"]
        if type(schema_version) is not int or type(sealed) is not bool:
            raise TypeError("execution scalar fields have invalid types")
        string_names = (
            "calculation_family",
            "study_family",
            "execution_id",
            "created_utc",
            "outcome",
            "evidence_status",
            "configuration_path",
            "configuration_sha256",
            "result_path",
            "result_sha256",
            "script_sha256",
            "claim_boundary",
        )
        strings: dict[str, str] = {}
        for name in string_names:
            value = values[name]
            if type(value) is not str:
                raise TypeError(f"{name} must decode to a built-in string")
            strings[name] = value
        return cls(
            schema_version=schema_version,
            calculation_family=strings["calculation_family"],
            study_family=strings["study_family"],
            execution_id=strings["execution_id"],
            created_utc=strings["created_utc"],
            outcome=strings["outcome"],
            evidence_status=strings["evidence_status"],
            configuration_path=strings["configuration_path"],
            configuration_sha256=strings["configuration_sha256"],
            result_path=strings["result_path"],
            result_sha256=strings["result_sha256"],
            script_sha256=strings["script_sha256"],
            software_versions=typed_versions,
            claim_boundary=strings["claim_boundary"],
            sealed=sealed,
        )


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityExecutionVerification(BaseTypedRecord):
    """Bind independent verification to one exact direct result."""

    schema_version: int
    schema: str
    calculation_family: str
    study_family: str
    execution_id: str
    verification: BandEquivalenceLocalityVerification
    visualization_data: BandEquivalenceLocalityVisualizationData
    comparison_count: int
    result_sha256: str
    script_sha256: str
    claim_boundary: str

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be a built-in integer")
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        for value, name in (
            (self.schema, "schema"),
            (self.calculation_family, "calculation_family"),
            (self.study_family, "study_family"),
            (self.execution_id, "execution_id"),
            (self.claim_boundary, "claim_boundary"),
        ):
            if type(value) is not str or not value:
                raise TypeError(f"{name} must be a nonempty built-in string")
        expected_schema = (
            f"ksdft2effmass.{self.calculation_family}-verification.direct.v1"
        )
        if self.schema != expected_schema:
            raise ValueError("schema must match the calculation family")
        if type(self.verification) is not BandEquivalenceLocalityVerification:
            raise TypeError("verification must be BandEquivalenceLocalityVerification")
        if (
            type(self.visualization_data)
            is not BandEquivalenceLocalityVisualizationData
        ):
            raise TypeError(
                "visualization_data must be BandEquivalenceLocalityVisualizationData"
            )
        if (
            hashlib.sha256(self.visualization_data.to_json()).hexdigest()
            != self.verification.visualization_data_sha256
        ):
            raise ValueError("verification authenticates different visualization data")
        if type(self.comparison_count) is not int:
            raise TypeError("comparison_count must be a built-in integer")
        if self.comparison_count != len(self.verification.checks):
            raise ValueError("comparison_count must match the verification inventory")
        for digest, name in (
            (self.result_sha256, "result_sha256"),
            (self.script_sha256, "script_sha256"),
        ):
            if (
                type(digest) is not str
                or len(digest) != 64
                or any(character not in "0123456789abcdef" for character in digest)
            ):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
        if self.result_sha256 != self.verification.subject_sha256:
            raise ValueError("verification authenticates different result bytes")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "schema_version": self.schema_version,
            "schema": self.schema,
            "calculation_family": self.calculation_family,
            "study_family": self.study_family,
            "execution_id": self.execution_id,
            "verification": self.verification,
            "visualization_data": self.visualization_data,
            "comparison_count": self.comparison_count,
            "result_sha256": self.result_sha256,
            "script_sha256": self.script_sha256,
            "claim_boundary": self.claim_boundary,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "schema_version",
            "schema",
            "calculation_family",
            "study_family",
            "execution_id",
            "verification",
            "visualization_data",
            "comparison_count",
            "result_sha256",
            "script_sha256",
            "claim_boundary",
        }
        if set(values) != required:
            raise ValueError(
                "band-equivalence verification-execution fields do not match"
            )
        verification = values["verification"]
        visualization_data = values["visualization_data"]
        if not isinstance(verification, Mapping) or not isinstance(
            visualization_data, Mapping
        ):
            raise TypeError("verification values must decode to mappings")
        schema_version = values["schema_version"]
        comparison_count = values["comparison_count"]
        if type(schema_version) is not int or type(comparison_count) is not int:
            raise TypeError("verification scalar fields have invalid types")
        string_names = (
            "schema",
            "calculation_family",
            "study_family",
            "execution_id",
            "result_sha256",
            "script_sha256",
            "claim_boundary",
        )
        strings: dict[str, str] = {}
        for name in string_names:
            value = values[name]
            if type(value) is not str:
                raise TypeError(f"{name} must decode to a built-in string")
            strings[name] = value
        return cls(
            schema_version=schema_version,
            schema=strings["schema"],
            calculation_family=strings["calculation_family"],
            study_family=strings["study_family"],
            execution_id=strings["execution_id"],
            verification=BandEquivalenceLocalityVerification.from_dict(verification),
            visualization_data=BandEquivalenceLocalityVisualizationData.from_dict(
                visualization_data
            ),
            comparison_count=comparison_count,
            result_sha256=strings["result_sha256"],
            script_sha256=strings["script_sha256"],
            claim_boundary=strings["claim_boundary"],
        )


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRendering(BaseTypedRecord):
    """Authenticate the closed rendering inventory of one verified execution."""

    schema_version: int
    schema: str
    calculation_family: str
    study_family: str
    execution_id: str
    outcome: str
    verification_sha256: str
    figures: Mapping[str, str]
    script_sha256: str
    claim_boundary: str

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be a built-in integer")
        if self.schema_version != 1:
            raise ValueError("schema_version must equal 1")
        for value, name in (
            (self.schema, "schema"),
            (self.calculation_family, "calculation_family"),
            (self.study_family, "study_family"),
            (self.execution_id, "execution_id"),
            (self.outcome, "outcome"),
            (self.claim_boundary, "claim_boundary"),
        ):
            if type(value) is not str or not value:
                raise TypeError(f"{name} must be a nonempty built-in string")
        expected_schema = f"ksdft2effmass.{self.calculation_family}-rendering.direct.v1"
        if self.schema != expected_schema:
            raise ValueError("schema must match the calculation family")
        if self.outcome != "completed":
            raise ValueError("outcome must be completed")
        for digest, name in (
            (self.verification_sha256, "verification_sha256"),
            (self.script_sha256, "script_sha256"),
        ):
            if (
                type(digest) is not str
                or len(digest) != 64
                or any(character not in "0123456789abcdef" for character in digest)
            ):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
        if not isinstance(self.figures, Mapping):
            raise TypeError("figures must be a mapping")
        figures: dict[str, str] = {}
        for filename, digest in self.figures.items():
            if type(filename) is not str or not filename.endswith(".png"):
                raise ValueError("figure names must be built-in PNG filenames")
            if (
                type(digest) is not str
                or len(digest) != 64
                or any(character not in "0123456789abcdef" for character in digest)
            ):
                raise ValueError("figure values must be lowercase SHA-256 digests")
            figures[filename] = digest
        if not figures:
            raise ValueError("figures must not be empty")
        object.__setattr__(
            self,
            "figures",
            MappingProxyType(dict(sorted(figures.items()))),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "schema_version": self.schema_version,
            "schema": self.schema,
            "calculation_family": self.calculation_family,
            "study_family": self.study_family,
            "execution_id": self.execution_id,
            "outcome": self.outcome,
            "verification_sha256": self.verification_sha256,
            "figures": self.figures,
            "script_sha256": self.script_sha256,
            "claim_boundary": self.claim_boundary,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "schema_version",
            "schema",
            "calculation_family",
            "study_family",
            "execution_id",
            "outcome",
            "verification_sha256",
            "figures",
            "script_sha256",
            "claim_boundary",
        }
        if set(values) != required:
            raise ValueError("band-equivalence rendering fields do not match")
        schema_version = values["schema_version"]
        figures = values["figures"]
        if type(schema_version) is not int:
            raise TypeError("schema_version must decode to a built-in integer")
        if not isinstance(figures, Mapping):
            raise TypeError("figures must decode to a mapping")
        typed_figures: dict[str, str] = {}
        for filename, digest in figures.items():
            if type(filename) is not str or type(digest) is not str:
                raise TypeError("figure inventory must decode to strings")
            typed_figures[filename] = digest
        string_names = (
            "schema",
            "calculation_family",
            "study_family",
            "execution_id",
            "outcome",
            "verification_sha256",
            "script_sha256",
            "claim_boundary",
        )
        strings: dict[str, str] = {}
        for name in string_names:
            value = values[name]
            if type(value) is not str:
                raise TypeError(f"{name} must decode to a built-in string")
            strings[name] = value
        return cls(
            schema_version=schema_version,
            schema=strings["schema"],
            calculation_family=strings["calculation_family"],
            study_family=strings["study_family"],
            execution_id=strings["execution_id"],
            outcome=strings["outcome"],
            verification_sha256=strings["verification_sha256"],
            figures=typed_figures,
            script_sha256=strings["script_sha256"],
            claim_boundary=strings["claim_boundary"],
        )


__all__ = [
    "BandEquivalenceLocalityExecution",
    "BandEquivalenceLocalityExecutionVerification",
    "BandEquivalenceLocalityRendering",
]
