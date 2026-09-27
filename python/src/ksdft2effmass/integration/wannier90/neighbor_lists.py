"""Typed adaptation of Wannier90 ``.nnkp`` neighbor lists."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Wannier90NeighborListData:
    """Retain ordered native neighbors and optional parsed fractional k points.

    ``kpoints_fractional`` is ``None`` only when adapting a bounded legacy fixture
    that omits the native ``kpoints`` block. Interface preparation requires explicit
    parsed points and never treats absence as compatible.
    """

    neighbor_count: int
    records: tuple[tuple[int, int, int, int, int], ...]
    kpoints_fractional: tuple[tuple[float, float, float], ...] | None = None

    def __post_init__(self) -> None:
        """Validate positive indices and complete equal-size neighbor groups."""
        if type(self.neighbor_count) is not int:
            raise TypeError("neighbor_count must be a built-in int")
        if self.neighbor_count <= 0:
            raise ValueError("neighbor_count must be positive")
        if type(self.records) is not tuple:
            raise TypeError("records must be a built-in tuple")
        if not self.records:
            raise ValueError("records must be nonempty")
        if len(self.records) % self.neighbor_count != 0:
            raise ValueError("record count must be divisible by neighbor_count")
        for record in self.records:
            if type(record) is not tuple:
                raise TypeError("neighbor records must be built-in tuples")
            if len(record) != 5:
                raise ValueError("neighbor records must contain exactly five values")
            if any(type(value) is not int for value in record):
                raise TypeError("neighbor record values must be built-in integers")
            if record[0] <= 0 or record[1] <= 0:
                raise ValueError(
                    "native k-point indices must be one-based and positive"
                )
        kpoint_count = len(self.records) // self.neighbor_count
        counts = tuple(
            sum(record[0] == kpoint for record in self.records)
            for kpoint in range(1, kpoint_count + 1)
        )
        if any(count != self.neighbor_count for count in counts):
            raise ValueError("each first k point must own neighbor_count records")
        if self.kpoints_fractional is None:
            return
        if type(self.kpoints_fractional) is not tuple:
            raise TypeError("kpoints_fractional must be a built-in tuple or None")
        if len(self.kpoints_fractional) != kpoint_count:
            raise ValueError("parsed k-point count must agree with neighbor records")
        for kpoint in self.kpoints_fractional:
            if type(kpoint) is not tuple:
                raise TypeError("each fractional k point must be a built-in tuple")
            if len(kpoint) != 3:
                raise ValueError("each fractional k point must have three coordinates")
            if any(type(value) is not float for value in kpoint):
                raise TypeError(
                    "fractional k-point coordinates must be built-in floats"
                )
            if any(not math.isfinite(value) for value in kpoint):
                raise ValueError("fractional k-point coordinates must be finite")

    @property
    def kpoint_count(self) -> int:
        """Return the inferred reciprocal-point count."""
        return len(self.records) // self.neighbor_count


class Wannier90NeighborListParser:
    """Parse ``kpoints`` and ``nnkpts`` blocks from caller-supplied UTF-8 bytes."""

    __slots__ = ()

    def execute(self, payload: bytes) -> Wannier90NeighborListData:
        """Return optional fractional points and ordered neighbor records."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            lines = tuple(line.strip() for line in payload.decode("utf-8").splitlines())
        except UnicodeDecodeError as error:
            raise ValueError("nnkp payload must be valid UTF-8") from error
        try:
            begin = lines.index("begin nnkpts")
            end = lines.index("end nnkpts", begin + 1)
        except ValueError as error:
            raise ValueError("nnkp payload lacks one complete nnkpts block") from error
        block = tuple(line for line in lines[begin + 1 : end] if line)
        if not block:
            raise ValueError("nnkpts block must be nonempty")
        try:
            neighbor_count = int(block[0])
        except ValueError as error:
            raise ValueError("nnkpts neighbor count must be an integer") from error
        records: list[tuple[int, int, int, int, int]] = []
        for line in block[1:]:
            fields = line.split()
            if len(fields) != 5:
                raise ValueError("nnkpts entry must contain five integers")
            try:
                values = tuple(int(field) for field in fields)
            except ValueError as error:
                raise ValueError("nnkpts entry must contain integers") from error
            records.append((values[0], values[1], values[2], values[3], values[4]))
        kpoints: tuple[tuple[float, float, float], ...] | None = None
        if "begin kpoints" in lines:
            kpoint_begin = lines.index("begin kpoints")
            try:
                kpoint_end = lines.index("end kpoints", kpoint_begin + 1)
            except ValueError as error:
                raise ValueError(
                    "nnkp payload lacks a complete kpoints block"
                ) from error
            kpoint_block = tuple(
                line for line in lines[kpoint_begin + 1 : kpoint_end] if line
            )
            if not kpoint_block:
                raise ValueError("kpoints block must be nonempty")
            try:
                declared_kpoint_count = int(kpoint_block[0])
            except ValueError as error:
                raise ValueError("kpoints count must be an integer") from error
            parsed_kpoints: list[tuple[float, float, float]] = []
            for line in kpoint_block[1:]:
                fields = line.split()
                if len(fields) != 3:
                    raise ValueError("kpoints entry must contain three scalars")
                try:
                    coordinates = tuple(float(field) for field in fields)
                except ValueError as error:
                    raise ValueError(
                        "kpoints entry must contain numeric scalars"
                    ) from error
                parsed_kpoints.append((coordinates[0], coordinates[1], coordinates[2]))
            if len(parsed_kpoints) != declared_kpoint_count:
                raise ValueError("kpoints entries must match the declared count")
            kpoints = tuple(parsed_kpoints)
        return Wannier90NeighborListData(neighbor_count, tuple(records), kpoints)
