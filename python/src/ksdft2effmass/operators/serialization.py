"""Versioned JSON-compatible operator-record serialization action object."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, ClassVar

import numpy as np

from .records import Basis, EnergyReference, Geometry, OperatorRecord, StateSpace


class OperatorRecordJsonCodec:
    """Action object implementing the version-1 operator-record wire format."""

    SCHEMA_VERSION: ClassVar[int] = 1

    def encode(self, record: OperatorRecord) -> dict[str, Any]:
        """Encode ``record`` as JSON-compatible Python objects."""

        return {
            "schema_version": self.SCHEMA_VERSION,
            "identifier": record.identifier,
            "operator_kind": record.operator_kind,
            "matrix": self._encode_complex_matrix(record.matrix),
            "state_space": {
                "identifier": record.state_space.identifier,
                "kind": record.state_space.kind,
                "dimension": record.state_space.dimension,
                "domain": record.state_space.domain,
                "codomain": record.state_space.codomain,
            },
            "basis": {
                "identifier": record.basis.identifier,
                "kind": record.basis.kind,
                "ordering": list(record.basis.ordering),
                "orthonormal": record.basis.orthonormal,
            },
            "geometry": {
                "system": record.geometry.system,
                "cell": [list(vector) for vector in record.geometry.cell],
                "boundary_conditions": record.geometry.boundary_conditions,
                "coordinate_convention": record.geometry.coordinate_convention,
            },
            "energy_reference": {
                "zero": record.energy_reference.zero,
                "unit": record.energy_reference.unit,
                "value": record.energy_reference.value,
            },
            "provenance": dict(record.provenance),
        }

    def decode(self, data: Mapping[str, Any]) -> OperatorRecord:
        """Decode and validate a version-1 operator-record payload."""

        self._require_supported_schema(data)
        self._require_fields(data)
        state_space_payload = data["state_space"]
        basis_payload = data["basis"]
        geometry_payload = data["geometry"]
        energy_reference_payload = data["energy_reference"]
        return OperatorRecord(
            identifier=data["identifier"],
            operator_kind=data["operator_kind"],
            matrix=self._decode_complex_matrix(data["matrix"]),
            state_space=StateSpace(
                identifier=state_space_payload["identifier"],
                kind=state_space_payload["kind"],
                dimension=state_space_payload["dimension"],
                domain=state_space_payload["domain"],
                codomain=state_space_payload["codomain"],
            ),
            basis=Basis(
                identifier=basis_payload["identifier"],
                kind=basis_payload["kind"],
                ordering=tuple(basis_payload["ordering"]),
                orthonormal=basis_payload["orthonormal"],
            ),
            geometry=Geometry(
                system=geometry_payload["system"],
                cell=tuple(tuple(vector) for vector in geometry_payload["cell"]),
                boundary_conditions=geometry_payload["boundary_conditions"],
                coordinate_convention=geometry_payload["coordinate_convention"],
            ),
            energy_reference=EnergyReference(
                zero=energy_reference_payload["zero"],
                unit=energy_reference_payload["unit"],
                value=energy_reference_payload["value"],
            ),
            provenance=dict(data["provenance"]),
        )

    def _require_supported_schema(self, data: Mapping[str, Any]) -> None:
        version = data.get("schema_version")
        if version is None:
            msg = "operator-record payload missing schema_version"
            raise ValueError(msg)
        if version != self.SCHEMA_VERSION:
            msg = f"unsupported operator-record schema_version: {version!r}"
            raise ValueError(msg)

    def _require_fields(self, data: Mapping[str, Any]) -> None:
        required = {
            "schema_version",
            "identifier",
            "operator_kind",
            "matrix",
            "state_space",
            "basis",
            "geometry",
            "energy_reference",
            "provenance",
        }
        missing = required.difference(data)
        if missing:
            msg = f"operator-record payload missing required fields: {sorted(missing)}"
            raise ValueError(msg)

    def _encode_complex_matrix(self, matrix: np.ndarray) -> list[list[list[float]]]:
        return [
            [[float(value.real), float(value.imag)] for value in row]
            for row in matrix.tolist()
        ]

    def _decode_complex_matrix(self, data: Any) -> np.ndarray:
        try:
            rows = []
            row_length = None
            for row in data:
                decoded_row = []
                for value in row:
                    if not isinstance(value, list | tuple) or len(value) != 2:
                        msg = "complex matrix entries must be [real, imaginary] pairs"
                        raise ValueError(msg)
                    try:
                        real = float(value[0])
                        imaginary = float(value[1])
                    except (TypeError, ValueError) as exc:
                        msg = "complex matrix entries must contain numeric values"
                        raise ValueError(msg) from exc
                    if not np.isfinite(real) or not np.isfinite(imaginary):
                        msg = "complex matrix entries must contain finite values"
                        raise ValueError(msg)
                    decoded_row.append(complex(real, imaginary))
                if row_length is None:
                    row_length = len(decoded_row)
                elif len(decoded_row) != row_length:
                    msg = "complex matrix rows must not be ragged"
                    raise ValueError(msg)
                rows.append(decoded_row)
        except TypeError as exc:
            msg = "malformed complex matrix encoding"
            raise ValueError(msg) from exc
        return np.array(rows, dtype=np.complex128)
