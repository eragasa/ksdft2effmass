"""Versioned Appendix G isolated-band campaign input contract."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass

from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.serialization import JsonCodec

from ..serialization import (
    Periodic1DCampaignJsonDecoder,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DIsolatedBandCampaignDefinition:
    """Retain the closed version-one isolated-band study controls.

    Parameters
    ----------
    experiment_id
        Nonempty wire identity shared with the retained result document.
    lattice_period, reciprocal_vector, reciprocal_energy, potential_strength
        Explicitly unitless scalar controls in the Appendix G convention.
    plane_wave_cutoffs
        Unique increasing positive Galerkin cutoffs used by the parent sweep.
    plane_wave_reference_cutoff
        Positive reference cutoff strictly larger than every sweep cutoff.
    finite_difference_points
        Unique increasing periodic-grid sizes of at least three points.
    parent_sample_momenta
        Nonempty unitless momenta for retained parent diagnostics.
    compared_band_count
        Positive number of bands fitting every compared parent representation.
    common_low_mode_cutoff
        Positive shared Fourier cutoff fitting every plane-wave basis and
        finite-difference grid.
    reciprocal_mesh_size
        Positive number of reciprocal samples used by the finite Fourier pair.
    hopping_ranges
        Unique increasing nonnegative truncation ranges in lattice cells.
    withheld_mesh_size
        Positive size of the separately evaluated withheld reciprocal mesh.
    weak_potential_strengths
        Nonempty positive unitless strengths for the weak-potential comparison.

    Raises
    ------
    TypeError
        If a field does not use its exact declared representation.
    ValueError
        If an inventory, positivity condition, reciprocal duality relation, or
        cross-field size condition is invalid.

    Notes
    -----
    This immutable definition records campaign controls only. It is not a physical
    model, finite Hamiltonian, retained space, represented operator, effective model,
    execution record, convergence result, or acceptance decision. The unitless
    convention does not itself supply a physical unit conversion.
    """

    experiment_id: str
    lattice_period: ScalarQuantity
    reciprocal_vector: ScalarQuantity
    reciprocal_energy: ScalarQuantity
    potential_strength: ScalarQuantity
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    finite_difference_points: tuple[int, ...]
    parent_sample_momenta: VectorQuantity
    compared_band_count: int
    common_low_mode_cutoff: int
    reciprocal_mesh_size: int
    hopping_ranges: tuple[int, ...]
    withheld_mesh_size: int
    weak_potential_strengths: VectorQuantity

    def __post_init__(self) -> None:
        """Validate intrinsic campaign-definition invariants."""
        self._check_args_identity()
        self._check_args_quantities()
        self._check_args_vectors()
        self._check_args_inventories()
        self._check_args_positive_integers()
        self._check_args_cross_field_relations()

    def _check_args_identity(self) -> None:
        """Require one nonempty exact built-in experiment identity."""
        if type(self.experiment_id) is not str:
            raise TypeError("experiment_id must be a built-in str")
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")

    def _check_args_quantities(self) -> None:
        """Require exact unitless scalar campaign quantities."""
        for quantity_name, quantity in (
            ("lattice_period", self.lattice_period),
            ("reciprocal_vector", self.reciprocal_vector),
            ("reciprocal_energy", self.reciprocal_energy),
            ("potential_strength", self.potential_strength),
        ):
            if type(quantity) is not ScalarQuantity:
                raise TypeError(f"{quantity_name} must be ScalarQuantity")
            if not isinstance(quantity.unit, Unitless):
                raise ValueError(f"{quantity_name} must be unitless")

    def _check_args_vectors(self) -> None:
        """Require nonempty exact unitless vector campaign quantities."""
        for vector_name, vector in (
            ("parent_sample_momenta", self.parent_sample_momenta),
            ("weak_potential_strengths", self.weak_potential_strengths),
        ):
            if type(vector) is not VectorQuantity:
                raise TypeError(f"{vector_name} must be VectorQuantity")
            if not isinstance(vector.unit, Unitless):
                raise ValueError(f"{vector_name} must be unitless")
            if vector.magnitude.size == 0:
                raise ValueError(f"{vector_name} must be nonempty")

    def _check_args_inventories(self) -> None:
        """Require nonempty unique increasing exact-integer inventories."""
        for inventory_name, inventory in (
            ("plane_wave_cutoffs", self.plane_wave_cutoffs),
            ("finite_difference_points", self.finite_difference_points),
            ("hopping_ranges", self.hopping_ranges),
        ):
            if (
                type(inventory) is not tuple
                or not inventory
                or any(type(item) is not int for item in inventory)
            ):
                raise TypeError(f"{inventory_name} must be a nonempty integer tuple")
            if tuple(sorted(set(inventory))) != inventory:
                raise ValueError(f"{inventory_name} must be unique and increasing")

    def _check_args_positive_integers(self) -> None:
        """Require positive exact built-in scalar integer controls."""
        for integer_name, integer_value in (
            ("plane_wave_reference_cutoff", self.plane_wave_reference_cutoff),
            ("compared_band_count", self.compared_band_count),
            ("common_low_mode_cutoff", self.common_low_mode_cutoff),
            ("reciprocal_mesh_size", self.reciprocal_mesh_size),
            ("withheld_mesh_size", self.withheld_mesh_size),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{integer_name} must be a built-in int")
            if integer_value <= 0:
                raise ValueError(f"{integer_name} must be positive")

    def _check_args_cross_field_relations(self) -> None:
        """Validate positivity, basis-fit, reference, and reciprocal-duality rules."""
        if self.lattice_period.magnitude <= 0.0:
            raise ValueError("lattice_period must be positive")
        if self.reciprocal_vector.magnitude <= 0.0:
            raise ValueError("reciprocal_vector must be positive")
        if self.reciprocal_energy.magnitude <= 0.0:
            raise ValueError("reciprocal_energy must be positive")
        if self.hopping_ranges[0] < 0:
            raise ValueError("hopping_ranges must be nonnegative")
        if self.plane_wave_cutoffs[0] <= 0:
            raise ValueError("plane_wave_cutoffs must be positive")
        if self.finite_difference_points[0] < 3:
            raise ValueError("finite_difference_points must be at least three")
        if self.plane_wave_reference_cutoff <= self.plane_wave_cutoffs[-1]:
            raise ValueError("reference cutoff must exceed every sweep cutoff")
        if self.common_low_mode_cutoff > self.plane_wave_cutoffs[0]:
            raise ValueError("common low-mode cutoff must fit every plane-wave basis")
        if 2 * self.common_low_mode_cutoff + 1 > self.finite_difference_points[0]:
            raise ValueError(
                "common low-mode dimension must fit every finite-difference grid"
            )
        smallest_parent_dimension = min(
            2 * self.plane_wave_cutoffs[0] + 1,
            self.finite_difference_points[0],
        )
        if self.compared_band_count > smallest_parent_dimension:
            raise ValueError("compared bands must fit every parent representation")
        if (self.weak_potential_strengths.magnitude <= 0.0).any():
            raise ValueError("weak_potential_strengths must be positive")
        if not math.isclose(
            self.lattice_period.magnitude * self.reciprocal_vector.magnitude,
            2.0 * math.pi,
            rel_tol=1.0e-12,
            abs_tol=1.0e-12,
        ):
            raise ValueError("lattice period and reciprocal vector must be dual")


class Periodic1DIsolatedBandCampaignJsonSerializer(
    JsonCodec[Periodic1DIsolatedBandCampaignDefinition, bytes]
):
    """Decode and canonically encode the retained isolated-band input."""

    __slots__ = ()

    decoder = Periodic1DCampaignJsonDecoder()

    def deserialize(self, payload: bytes) -> Periodic1DIsolatedBandCampaignDefinition:
        """Decode strict version-one JSON without executing the campaign.

        Parameters
        ----------
        payload
            Exact UTF-8 JSON bytes containing the closed isolated input schema.

        Returns
        -------
        Periodic1DIsolatedBandCampaignDefinition
            Immutable validated campaign controls with explicit unitless quantities.

        Raises
        ------
        TypeError
            If the wire or a field has an unsupported exact representation.
        ValueError
            If JSON, schema, status, fields, controls, or intrinsic correlations are
            invalid.
        UnicodeDecodeError
            If ``payload`` is not valid UTF-8.
        OverflowError
            If an integer cannot be represented by a required binary64 value.
        """
        root = self.decoder.document(payload)
        expected = {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "dimensionless_convention",
            "potential_strength",
            "plane_wave_cutoffs",
            "plane_wave_reference_cutoff",
            "finite_difference_points",
            "parent_sample_momenta",
            "compared_band_count",
            "common_low_mode_cutoff",
            "reciprocal_mesh_size",
            "hopping_ranges",
            "withheld_mesh_size",
            "weak_potential_strengths",
        }
        if set(root) != expected:
            raise ValueError("isolated-band input fields must match schema version one")
        if self.decoder.integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported isolated-band input schema version")
        if (
            self.decoder.string(root["evidence_status"], "evidence_status")
            != "illustrative numerical experiment"
        ):
            raise ValueError("unexpected evidence_status")
        convention = self.decoder.mapping(
            root["dimensionless_convention"], "dimensionless_convention"
        )
        if set(convention) != {
            "lattice_period",
            "reciprocal_vector",
            "reciprocal_energy",
        }:
            raise ValueError("dimensionless_convention fields are invalid")
        return Periodic1DIsolatedBandCampaignDefinition(
            self.decoder.string(root.get("experiment_id"), "experiment_id"),
            self.decoder.scalar(convention.get("lattice_period"), "lattice_period"),
            self.decoder.scalar(
                convention.get("reciprocal_vector"), "reciprocal_vector"
            ),
            self.decoder.scalar(
                convention.get("reciprocal_energy"), "reciprocal_energy"
            ),
            self.decoder.scalar(root.get("potential_strength"), "potential_strength"),
            self.decoder.integers(root.get("plane_wave_cutoffs"), "plane_wave_cutoffs"),
            self.decoder.integer(
                root.get("plane_wave_reference_cutoff"), "plane_wave_reference_cutoff"
            ),
            self.decoder.integers(
                root.get("finite_difference_points"), "finite_difference_points"
            ),
            self.decoder.vector(
                root.get("parent_sample_momenta"), "parent_sample_momenta"
            ),
            self.decoder.integer(
                root.get("compared_band_count"), "compared_band_count"
            ),
            self.decoder.integer(
                root.get("common_low_mode_cutoff"), "common_low_mode_cutoff"
            ),
            self.decoder.integer(
                root.get("reciprocal_mesh_size"), "reciprocal_mesh_size"
            ),
            self.decoder.integers(root.get("hopping_ranges"), "hopping_ranges"),
            self.decoder.integer(root.get("withheld_mesh_size"), "withheld_mesh_size"),
            self.decoder.vector(
                root.get("weak_potential_strengths"), "weak_potential_strengths"
            ),
        )

    def serialize(self, value: Periodic1DIsolatedBandCampaignDefinition) -> bytes:
        """Return canonical version-one UTF-8 JSON.

        Parameters
        ----------
        value
            Exact immutable isolated-band campaign definition.

        Returns
        -------
        bytes
            Deterministic canonical JSON for schema version one.

        Raises
        ------
        TypeError
            If ``value`` is not exactly
            :class:`Periodic1DIsolatedBandCampaignDefinition`.
        """
        if type(value) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("value must be Periodic1DIsolatedBandCampaignDefinition")
        document = {
            "schema_version": 1,
            "experiment_id": value.experiment_id,
            "evidence_status": "illustrative numerical experiment",
            "dimensionless_convention": {
                "lattice_period": value.lattice_period.magnitude,
                "reciprocal_vector": value.reciprocal_vector.magnitude,
                "reciprocal_energy": value.reciprocal_energy.magnitude,
            },
            "potential_strength": value.potential_strength.magnitude,
            "plane_wave_cutoffs": list(value.plane_wave_cutoffs),
            "plane_wave_reference_cutoff": value.plane_wave_reference_cutoff,
            "finite_difference_points": list(value.finite_difference_points),
            "parent_sample_momenta": value.parent_sample_momenta.magnitude.tolist(),
            "compared_band_count": value.compared_band_count,
            "common_low_mode_cutoff": value.common_low_mode_cutoff,
            "reciprocal_mesh_size": value.reciprocal_mesh_size,
            "hopping_ranges": list(value.hopping_ranges),
            "withheld_mesh_size": value.withheld_mesh_size,
            "weak_potential_strengths": (
                value.weak_potential_strengths.magnitude.tolist()
            ),
        }
        return (
            json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode()
