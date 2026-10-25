"""Typed access to the accepted Vogl et al. (1983) Table 1 transcription."""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, fields
from enum import StrEnum
from pathlib import Path
from typing import TypedDict, cast

TABLE_SCHEMA = "ksdft2effmass.calculations.Si.bulk.vogl1983-table1.v1"
TABLE_STATUS = "accepted-table-transcription"
TABLE_UNIT = "eV"
FOUR_DECIMAL_PATTERN = re.compile(r"-?\d+\.\d{4}")


class Vogl1983Compound(StrEnum):
    """Compounds represented by Vogl et al. (1983), Table 1."""

    C = "C"
    SI = "Si"
    GE = "Ge"
    SN = "Sn"
    SIC = "SiC"
    ALP = "AlP"
    ALAS = "AlAs"
    ALSB = "AlSb"
    GAP = "GaP"
    GAAS = "GaAs"
    GASB = "GaSb"
    INP = "InP"
    INAS = "InAs"
    INSB = "InSb"
    ZNSE = "ZnSe"
    ZNTE = "ZnTe"


@dataclass(frozen=True, slots=True)
class Vogl1983Table1Parameters:
    """One 13-parameter Table 1 row, in electronvolts."""

    e_s_a: float
    e_p_a: float
    e_s_c: float
    e_p_c: float
    e_s_star_a: float
    e_s_star_c: float
    v_s_s: float
    v_x_x: float
    v_x_y: float
    v_s_a_p_c: float
    v_s_c_p_a: float
    v_s_star_a_p_c: float
    v_p_a_s_star_c: float

    def __post_init__(self) -> None:
        """Reject non-finite table parameters."""
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, bool) or not isinstance(value, float):
                raise TypeError(f"{field.name} must be a float")
            if not math.isfinite(value):
                raise ValueError(f"{field.name} must be finite")


PARAMETER_KEYS = tuple(field.name for field in fields(Vogl1983Table1Parameters))


@dataclass(frozen=True, slots=True)
class Vogl1983Table1Row:
    """A compound label and its immutable Table 1 parameters."""

    compound: Vogl1983Compound
    parameters: Vogl1983Table1Parameters


class _SourceDocument(TypedDict):
    citation: str
    doi: str
    table: str
    source_pdf_sha256: str
    source_page_id: str
    rendered_region_id: str
    transcription_proposal_sha256: str
    acceptance: str


class _RowDocument(TypedDict):
    compound: str
    values: dict[str, str]


class _TableDocument(TypedDict):
    schema: str
    status: str
    unit: str
    source: _SourceDocument
    parameter_order: list[str]
    rows: list[_RowDocument]


@dataclass(frozen=True, slots=True)
class Vogl1983Table1:
    """The complete accepted 16-row Table 1 transcription."""

    rows: tuple[Vogl1983Table1Row, ...]
    citation: str
    doi: str
    source_pdf_sha256: str
    source_page_id: str
    rendered_region_id: str
    transcription_proposal_sha256: str
    acceptance: str

    def __post_init__(self) -> None:
        """Require each declared compound exactly once."""
        compounds = tuple(row.compound for row in self.rows)
        if len(compounds) != len(Vogl1983Compound):
            raise ValueError("Table 1 must contain exactly 16 rows")
        if len(set(compounds)) != len(compounds):
            raise ValueError("Table 1 compound labels must be unique")
        if set(compounds) != set(Vogl1983Compound):
            raise ValueError("Table 1 compound inventory differs")

    @classmethod
    def from_json(cls, path: Path) -> Vogl1983Table1:
        """Load and validate the canonical Table 1 JSON document."""
        document = cast(
            _TableDocument,
            json.loads(path.read_text(encoding="utf-8")),
        )
        if document["schema"] != TABLE_SCHEMA:
            raise ValueError("Table 1 schema differs")
        if document["status"] != TABLE_STATUS:
            raise ValueError("Table 1 status differs")
        if document["unit"] != TABLE_UNIT:
            raise ValueError("Table 1 unit must be eV")
        if tuple(document["parameter_order"]) != PARAMETER_KEYS:
            raise ValueError("Table 1 parameter order differs")

        rows = tuple(cls._parse_row(row) for row in document["rows"])
        source = document["source"]
        if source["doi"] != "10.1016/0022-3697(83)90064-1":
            raise ValueError("Vogl source DOI differs")
        if source["table"] != "Table 1":
            raise ValueError("Vogl source table differs")
        return cls(
            rows=rows,
            citation=source["citation"],
            doi=source["doi"],
            source_pdf_sha256=source["source_pdf_sha256"],
            source_page_id=source["source_page_id"],
            rendered_region_id=source["rendered_region_id"],
            transcription_proposal_sha256=source["transcription_proposal_sha256"],
            acceptance=source["acceptance"],
        )

    @staticmethod
    def _parse_row(document: _RowDocument) -> Vogl1983Table1Row:
        values = document["values"]
        if tuple(values) != PARAMETER_KEYS:
            raise ValueError(
                f"Table 1 parameter keys differ for {document['compound']}"
            )
        for key, text in values.items():
            if FOUR_DECIMAL_PATTERN.fullmatch(text) is None:
                raise ValueError(
                    f"Table 1 value {document['compound']} {key} is not four-decimal text"
                )
        parameters = Vogl1983Table1Parameters(
            **{key: float(values[key]) for key in PARAMETER_KEYS}
        )
        return Vogl1983Table1Row(
            compound=Vogl1983Compound(document["compound"]),
            parameters=parameters,
        )

    @property
    def compounds(self) -> tuple[Vogl1983Compound, ...]:
        """Return compounds in printed Table 1 order."""
        return tuple(row.compound for row in self.rows)

    def parameters_for(
        self, compound: Vogl1983Compound | str
    ) -> Vogl1983Table1Parameters:
        """Return the parameters for one exact compound label."""
        selected = Vogl1983Compound(compound)
        for row in self.rows:
            if row.compound is selected:
                return row.parameters
        raise AssertionError("validated Table 1 is missing a declared compound")
