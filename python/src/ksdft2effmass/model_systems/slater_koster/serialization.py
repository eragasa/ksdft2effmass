"""Deterministic typed-JSON serialization for diamond ``sp3s*`` models."""

from __future__ import annotations

from collections.abc import Mapping

from projectkoios.physkit.units import ScalarQuantity

from ksdft2effmass.serialization import (
    SerializableValue,
    TypedJsonMappingSerializer,
)

from .model import DiamondSp3sStarModel
from .parameters import ELECTRON_VOLT


class DiamondSp3sStarModelJsonSerializer:
    """Serialize one model definition without filesystem effects.

    The wire document records inputs and conventions, not a sampled Hamiltonian or a
    scientific-fit disposition. Encoding is delegated to the repository's canonical
    :class:`TypedJsonMappingSerializer`.
    """

    __slots__ = ("_serializer",)

    def __init__(self) -> None:
        self._serializer = TypedJsonMappingSerializer()

    def serialize(self, model: DiamondSp3sStarModel) -> bytes:
        """Return canonical sorted UTF-8 JSON with a terminal newline."""
        if type(model) is not DiamondSp3sStarModel:
            raise TypeError("model must be DiamondSp3sStarModel")
        parameters = model.parameters
        onsite: Mapping[str, SerializableValue] = {
            "E_p": parameters.onsite.p,
            "E_s": parameters.onsite.s,
            "E_s_star": parameters.onsite.s_star,
        }
        first_neighbor: Mapping[str, SerializableValue] = {
            "V1_pp_pi": parameters.first_neighbor.pp_pi,
            "V1_pp_sigma": parameters.first_neighbor.pp_sigma,
            "V1_s_star_p_sigma": parameters.first_neighbor.s_star_p_sigma,
            "V1_sp_sigma": parameters.first_neighbor.sp_sigma,
            "V1_ss_sigma": parameters.first_neighbor.ss_sigma,
            "fixed_V1_s_s_star_sigma": ScalarQuantity(0.0, ELECTRON_VOLT),
            "fixed_V1_s_star_s_star_sigma": ScalarQuantity(0.0, ELECTRON_VOLT),
        }
        second_neighbor: Mapping[str, SerializableValue] = {
            "V2_pp_pi": parameters.second_neighbor.pp_pi,
            "V2_pp_sigma": parameters.second_neighbor.pp_sigma,
            "V2_s_s_star_sigma": parameters.second_neighbor.s_s_star_sigma,
            "V2_s_star_p_sigma": parameters.second_neighbor.s_star_p_sigma,
            "V2_s_star_s_star_sigma": (parameters.second_neighbor.s_star_s_star_sigma),
            "V2_sp_sigma": parameters.second_neighbor.sp_sigma,
            "V2_ss_sigma": parameters.second_neighbor.ss_sigma,
        }
        record: Mapping[str, SerializableValue] = {
            "basis_order": (
                "A:s",
                "A:px",
                "A:py",
                "A:pz",
                "A:s_star",
                "B:s",
                "B:px",
                "B:py",
                "B:pz",
                "B:s_star",
            ),
            "geometry": {
                "basis_fractional_primitive": (
                    (0.0, 0.0, 0.0),
                    (0.25, 0.25, 0.25),
                ),
                "first_neighbor_A_to_B_target_cells": tuple(
                    bond.target_cell for bond in model.geometry.first_neighbor_bonds
                ),
                "lattice_parameter": model.geometry.lattice_parameter,
                "normalized_direct_basis_vector_axis": "columns",
                "normalized_direct_basis_vectors": (
                    (0.5, 0.0, 0.5),
                    (0.5, 0.5, 0.0),
                    (0.0, 0.5, 0.5),
                ),
                "second_neighbor_positive_target_cells": tuple(
                    bond.target_cell
                    for bond in model.geometry.second_neighbor_positive_bonds
                ),
            },
            "model": "homopolar-diamond-spinless-sp3s-star",
            "parameter_order": parameters.parameter_names,
            "parameters": {
                "first_neighbor": first_neighbor,
                "onsite": onsite,
                "second_neighbor": second_neighbor,
            },
            "phase_convention": (
                "exp(+2*pi*i*k_fractional dot full_primitive_displacement); "
                "Bloch sums include R+tau"
            ),
            "schema_version": 1,
        }
        return self._serializer.serialize(record)
