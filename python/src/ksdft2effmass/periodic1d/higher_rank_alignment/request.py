"""Immutable requests for higher-rank periodic frame transport."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .configuration import Periodic1DHigherRankAlignmentConfiguration


def _nonempty_identifier(value: str, name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in string")
    if not value:
        raise ValueError(f"{name} must be nonempty")


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankAlignmentTransportRequest(BaseTypedRecord):
    """Select one frame-transport calculation and its physical identities.

    Parameters
    ----------
    configuration
        Exact frozen higher-rank study configuration.
    retained_rank
        Built-in integer dimension ``r`` of the transported retained subspace. It must
        belong to the configured inventory ``(3, 4, 8, 16)``.
    circuit_depth
        Built-in integer synthetic-gauge circuit depth ``L``. It must belong to the
        configured inventory ``(1, 2, 4, 8)``.
    construction_mesh_size
        Built-in integer number ``M`` of points on the unshifted one-dimensional
        construction mesh. It must belong to ``(513, 1025, 2049)``.
    ambient_basis_identifier
        Nonempty identity of the ordered ambient basis. It has no physical unit.
    retained_frame_identifier
        Nonempty identity of the rank-``r`` frame family. It has no physical unit.
    endpoint_sewing_identifier
        Nonempty identity of the reciprocal-endpoint sewing map. It has no physical
        unit.

    Notes
    -----
    Python integers do not overflow. The finite allowed inventories bound every numeric
    field. Boolean values are rejected even though ``bool`` is an ``int`` subclass.
    """

    configuration: Periodic1DHigherRankAlignmentConfiguration
    retained_rank: int
    circuit_depth: int
    construction_mesh_size: int
    ambient_basis_identifier: str
    retained_frame_identifier: str
    endpoint_sewing_identifier: str

    def __post_init__(self) -> None:
        """Validate the selected case, mesh, and semantic identities."""
        if type(self.configuration) is not Periodic1DHigherRankAlignmentConfiguration:
            raise TypeError(
                "configuration must be Periodic1DHigherRankAlignmentConfiguration"
            )
        for value, name, allowed in (
            (self.retained_rank, "retained_rank", self.configuration.retained_ranks),
            (self.circuit_depth, "circuit_depth", self.configuration.circuit_depths),
            (
                self.construction_mesh_size,
                "construction_mesh_size",
                self.configuration.construction_mesh_sizes,
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value not in allowed:
                raise ValueError(f"{name} is not in the configured inventory")
        _nonempty_identifier(
            self.ambient_basis_identifier,
            "ambient_basis_identifier",
        )
        _nonempty_identifier(
            self.retained_frame_identifier,
            "retained_frame_identifier",
        )
        _nonempty_identifier(
            self.endpoint_sewing_identifier,
            "endpoint_sewing_identifier",
        )

    @property
    def case_identity(self) -> str:
        """Return the rank/depth identity ``rNN-LNN`` for this request."""
        return f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}"

    @property
    def ambient_dimension(self) -> int:
        """Return the configured ambient dimension ``2 * retained_rank``."""
        return self.configuration.ambient_dimension(self.retained_rank)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "configuration": self.configuration,
            "retained_rank": self.retained_rank,
            "circuit_depth": self.circuit_depth,
            "construction_mesh_size": self.construction_mesh_size,
            "ambient_basis_identifier": self.ambient_basis_identifier,
            "retained_frame_identifier": self.retained_frame_identifier,
            "endpoint_sewing_identifier": self.endpoint_sewing_identifier,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "configuration",
            "retained_rank",
            "circuit_depth",
            "construction_mesh_size",
            "ambient_basis_identifier",
            "retained_frame_identifier",
            "endpoint_sewing_identifier",
        }
        if set(values) != required:
            raise ValueError("higher-rank transport request fields do not match")
        configuration_value = values["configuration"]
        if not isinstance(configuration_value, Mapping):
            raise TypeError("configuration must decode to a mapping")
        configuration = Periodic1DHigherRankAlignmentConfiguration.from_dict(
            configuration_value
        )
        retained_rank = values["retained_rank"]
        circuit_depth = values["circuit_depth"]
        construction_mesh_size = values["construction_mesh_size"]
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must decode to a built-in integer")
        if type(circuit_depth) is not int:
            raise TypeError("circuit_depth must decode to a built-in integer")
        if type(construction_mesh_size) is not int:
            raise TypeError("construction_mesh_size must decode to a built-in integer")
        ambient_basis_identifier = values["ambient_basis_identifier"]
        retained_frame_identifier = values["retained_frame_identifier"]
        endpoint_sewing_identifier = values["endpoint_sewing_identifier"]
        if (
            type(ambient_basis_identifier) is not str
            or type(retained_frame_identifier) is not str
            or type(endpoint_sewing_identifier) is not str
        ):
            raise TypeError("transport identities must decode to built-in strings")
        return cls(
            configuration=configuration,
            retained_rank=retained_rank,
            circuit_depth=circuit_depth,
            construction_mesh_size=construction_mesh_size,
            ambient_basis_identifier=ambient_basis_identifier,
            retained_frame_identifier=retained_frame_identifier,
            endpoint_sewing_identifier=endpoint_sewing_identifier,
        )


__all__ = ["Periodic1DHigherRankAlignmentTransportRequest"]
