"""Root calculated and independently verified diagnostic records."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..definitions import BandEquivalenceLocalityFamilyEnum
from .case import CaseDiagnostic


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityDiagnostics(BaseTypedRecord):
    """Retain calculated diagnostics without artifact provenance or evidence claims."""

    family: BandEquivalenceLocalityFamilyEnum
    status: str
    construction_size: int
    evaluation_size: int
    cases: tuple[CaseDiagnostic, ...]

    def __post_init__(self) -> None:
        if type(self.family) is not BandEquivalenceLocalityFamilyEnum:
            raise TypeError("family must be BandEquivalenceLocalityFamilyEnum")
        if type(self.status) is not str:
            raise TypeError("status must be a built-in string")
        if type(self.construction_size) is not int or self.construction_size < 4:
            raise ValueError("construction_size must be at least four")
        if type(self.evaluation_size) is not int or self.evaluation_size < 3:
            raise ValueError("evaluation_size must be at least three")
        if (
            type(self.cases) is not tuple
            or not self.cases
            or any(type(case) is not CaseDiagnostic for case in self.cases)
        ):
            raise TypeError("cases must contain CaseDiagnostic values")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "family": self.family.to_wire(),
            "status": self.status,
            "construction_size": self.construction_size,
            "evaluation_size": self.evaluation_size,
            "cases": self.cases,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "family",
            "status",
            "construction_size",
            "evaluation_size",
            "cases",
        }
        if set(values) != required:
            raise ValueError("BandEquivalenceLocalityDiagnostics fields do not match")
        family_wire = values["family"]
        status = values["status"]
        construction_size = values["construction_size"]
        evaluation_size = values["evaluation_size"]
        cases_values = values["cases"]
        if type(construction_size) is not int or type(evaluation_size) is not int:
            raise TypeError("integer fields must use exact built-in types")
        if type(status) is not str:
            raise TypeError("string fields must use exact built-in types")
        if type(family_wire) is not str:
            raise TypeError("enum fields must decode to built-in strings")
        if not isinstance(cases_values, tuple) or any(
            not isinstance(item, Mapping) for item in cases_values
        ):
            raise TypeError("cases must decode to a tuple of mappings")
        return cls(
            family=BandEquivalenceLocalityFamilyEnum.from_wire(family_wire),
            status=status,
            construction_size=construction_size,
            evaluation_size=evaluation_size,
            cases=tuple(CaseDiagnostic.from_dict(item) for item in cases_values),
        )


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityVerificationDiagnostics(BaseTypedRecord):
    """Retain independent numerical checks without artifact provenance."""

    family: BandEquivalenceLocalityFamilyEnum
    passes: bool
    maximum_stored_identity_defect: float
    maximum_independent_parent_defect: float
    maximum_independent_band_defect: float

    def __post_init__(self) -> None:
        if type(self.family) is not BandEquivalenceLocalityFamilyEnum:
            raise TypeError("family must be BandEquivalenceLocalityFamilyEnum")
        for value, name in (
            (self.maximum_stored_identity_defect, "maximum_stored_identity_defect"),
            (
                self.maximum_independent_parent_defect,
                "maximum_independent_parent_defect",
            ),
            (
                self.maximum_independent_band_defect,
                "maximum_independent_band_defect",
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "family": self.family.to_wire(),
            "passes": self.passes,
            "maximum_stored_identity_defect": self.maximum_stored_identity_defect,
            "maximum_independent_parent_defect": self.maximum_independent_parent_defect,
            "maximum_independent_band_defect": self.maximum_independent_band_defect,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "family",
            "passes",
            "maximum_stored_identity_defect",
            "maximum_independent_parent_defect",
            "maximum_independent_band_defect",
        }
        if set(values) != required:
            raise ValueError(
                "BandEquivalenceLocalityVerificationDiagnostics fields do not match"
            )
        family_wire = values["family"]
        passes = values["passes"]
        maximum_stored_identity_defect = values["maximum_stored_identity_defect"]
        maximum_independent_parent_defect = values["maximum_independent_parent_defect"]
        maximum_independent_band_defect = values["maximum_independent_band_defect"]
        if (
            type(maximum_stored_identity_defect) is not float
            or type(maximum_independent_parent_defect) is not float
            or type(maximum_independent_band_defect) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if type(passes) is not bool:
            raise TypeError("Boolean fields must use exact built-in types")
        if type(family_wire) is not str:
            raise TypeError("enum fields must decode to built-in strings")
        return cls(
            family=BandEquivalenceLocalityFamilyEnum.from_wire(family_wire),
            passes=passes,
            maximum_stored_identity_defect=maximum_stored_identity_defect,
            maximum_independent_parent_defect=maximum_independent_parent_defect,
            maximum_independent_band_defect=maximum_independent_band_defect,
        )
