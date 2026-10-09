"""Version-one definition and wire adaptation for the reduction challenge.

The canonical Python names describe adversarial challenges to assumptions used by the
periodic-1D reduction workflow. Historical schema-one JSON keys containing ``stress``
remain unchanged because they are wire identities, not mechanical-stress semantics.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np

from ksdft2effmass.analysis.model_systems.periodic_1d import (
    PeriodicFourierPotential1D,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.serialization import JsonCodec

from ..serialization import Periodic1DCampaignJsonDecoder


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DReductionChallengePotentialShape:
    """Bind one stable challenge-case identifier to a finite Fourier potential.

    Parameters
    ----------
    identifier
        Nonempty exact built-in string used to correlate input and result inventories.
    potential
        Real periodic Fourier potential in the dimensionless Appendix G convention.
        Its period and all coefficients must carry :class:`Unitless`.

    Raises
    ------
    TypeError
        If either value has the wrong exact representation.
    ValueError
        If the identifier is empty or any potential quantity is not unitless.

    Notes
    -----
    This campaign control is not a complete parent Hamiltonian or represented
    operator. The numerical verifier composes it with an explicit kinetic term and a
    finite representation.
    """

    identifier: str
    potential: PeriodicFourierPotential1D

    def __post_init__(self) -> None:
        """Validate the stable identifier and dimensionless potential convention."""
        self._check_args_identifier()
        self._check_args_potential()

    def _check_args_identifier(self) -> None:
        """Require a nonempty exact built-in string identifier."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a built-in str")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")

    def _check_args_potential(self) -> None:
        """Require one exact finite-Fourier potential with unitless quantities."""
        if type(self.potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        quantities = (
            self.potential.period,
            self.potential.constant_coefficient,
            self.potential.cosine_coefficients,
            self.potential.sine_coefficients,
        )
        if any(not isinstance(quantity.unit, Unitless) for quantity in quantities):
            raise ValueError("challenge potential shapes must be explicitly unitless")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DReductionChallengeCampaignDefinition:
    """Retain the closed controls for the Appendix G reduction challenge.

    Parameters
    ----------
    experiment_id
        Stable identity shared with the retained result document.
    potential_strengths
        Increasing dimensionless amplitudes challenged by the campaign.
    plane_wave_cutoffs, finite_difference_points
        Increasing finite-representation controls. They remain distinct numerical
        discretizations and do not jointly prove convergence.
    plane_wave_reference_cutoff
        Finite plane-wave reference cutoff, strictly larger than the sweep cutoffs.
    compared_band_count
        Number of increasing finite-representation eigenvalues compared.
    challenged_band_indices
        Increasing subset of compared band indices used by mesh and isolation cases.
    potential_shapes
        Ordered named finite-Fourier challenge potentials with a common period.
    reciprocal_mesh_sizes
        Increasing mesh-size controls for sampling and hopping reconstruction.
    hopping_range_cells, withheld_mesh_size
        Primary range-truncation and independent withheld-mesh controls.
    isolation_gap_threshold
        Positive dimensionless applicability threshold for scalar isolated bands.
    route_challenge_potential_strength
        Dimensionless potential strength for the route challenges.
    route_challenge_mesh_size
        Reciprocal-mesh size for gauge and fitting-route challenges.
    route_challenge_hopping_range_cells
        Cell range of the challenged fitted hopping model.

    Raises
    ------
    TypeError
        If a field has the wrong exact representation.
    ValueError
        If units, ordering, uniqueness, positivity, index bounds, common period, or
        cross-control relationships are invalid.

    Notes
    -----
    Expected trends are not acceptance criteria. In particular, closed gaps and route
    defects under altered mathematics are retained observations rather than forced
    passes. This DataObject owns campaign controls, not a physical parent model,
    retained space, represented operator, convergence result, or scientific claim.
    """

    experiment_id: str
    potential_strengths: VectorQuantity
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    finite_difference_points: tuple[int, ...]
    compared_band_count: int
    challenged_band_indices: tuple[int, ...]
    potential_shapes: tuple[Periodic1DReductionChallengePotentialShape, ...]
    reciprocal_mesh_sizes: tuple[int, ...]
    hopping_range_cells: int
    withheld_mesh_size: int
    isolation_gap_threshold: ScalarQuantity
    route_challenge_potential_strength: ScalarQuantity
    route_challenge_mesh_size: int
    route_challenge_hopping_range_cells: int

    def __post_init__(self) -> None:
        """Validate intrinsic controls and their closed cross-field relationships."""
        self._check_args_experiment_identity()
        self._check_args_potential_strengths()
        self._check_args_scalar_controls()
        self._check_args_ordered_integer_inventories()
        self._check_args_positive_integer_controls()
        self._check_args_potential_shapes()
        self._check_args_cross_control_relationships()

    def _check_args_experiment_identity(self) -> None:
        """Require a nonempty exact built-in experiment identity."""
        if type(self.experiment_id) is not str:
            raise TypeError("experiment_id must be a built-in str")
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")

    def _check_args_potential_strengths(self) -> None:
        """Require a nonempty increasing unitless amplitude inventory."""
        if type(self.potential_strengths) is not VectorQuantity:
            raise TypeError("potential_strengths must be VectorQuantity")
        if not isinstance(self.potential_strengths.unit, Unitless):
            raise ValueError("potential_strengths must be unitless")
        values = self.potential_strengths.magnitude
        if values.size == 0:
            raise ValueError("potential_strengths must be nonempty")
        if np.any(np.diff(values) <= 0.0):
            raise ValueError("potential_strengths must be strictly increasing")

    def _check_args_scalar_controls(self) -> None:
        """Require exact unitless threshold and route-amplitude quantities."""
        for name, quantity in (
            ("isolation_gap_threshold", self.isolation_gap_threshold),
            (
                "route_challenge_potential_strength",
                self.route_challenge_potential_strength,
            ),
        ):
            if type(quantity) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if not isinstance(quantity.unit, Unitless):
                raise ValueError(f"{name} must be unitless")
        if self.isolation_gap_threshold.magnitude <= 0.0:
            raise ValueError("isolation_gap_threshold must be positive")

    def _check_args_ordered_integer_inventories(self) -> None:
        """Require nonempty, unique, increasing exact-integer inventories."""
        for name, inventory in (
            ("plane_wave_cutoffs", self.plane_wave_cutoffs),
            ("finite_difference_points", self.finite_difference_points),
            ("challenged_band_indices", self.challenged_band_indices),
            ("reciprocal_mesh_sizes", self.reciprocal_mesh_sizes),
        ):
            if type(inventory) is not tuple or not inventory:
                raise TypeError(f"{name} must be a nonempty tuple")
            if any(type(item) is not int for item in inventory):
                raise TypeError(f"{name} must contain built-in integers")
            if tuple(sorted(set(inventory))) != inventory:
                raise ValueError(f"{name} must be unique and increasing")

    def _check_args_positive_integer_controls(self) -> None:
        """Require exact positive integers for dimensions, meshes, and ranges."""
        for name, value in (
            ("plane_wave_reference_cutoff", self.plane_wave_reference_cutoff),
            ("compared_band_count", self.compared_band_count),
            ("hopping_range_cells", self.hopping_range_cells),
            ("withheld_mesh_size", self.withheld_mesh_size),
            ("route_challenge_mesh_size", self.route_challenge_mesh_size),
            (
                "route_challenge_hopping_range_cells",
                self.route_challenge_hopping_range_cells,
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")

    def _check_args_potential_shapes(self) -> None:
        """Require an ordered unique inventory of owned common-period shapes."""
        if type(self.potential_shapes) is not tuple or not self.potential_shapes:
            raise TypeError("potential_shapes must be a nonempty tuple")
        if any(
            type(shape) is not Periodic1DReductionChallengePotentialShape
            for shape in self.potential_shapes
        ):
            raise TypeError("every potential shape must use the owned record")
        identifiers = tuple(shape.identifier for shape in self.potential_shapes)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("potential shape identifiers must be unique")
        reference_period = self.potential_shapes[0].potential.period.magnitude
        if any(
            shape.potential.period.magnitude != reference_period
            for shape in self.potential_shapes[1:]
        ):
            raise ValueError("all challenge potential shapes must use one period")

    def _check_args_cross_control_relationships(self) -> None:
        """Require index, discretization, route, and mesh controls to agree."""
        if self.compared_band_count < 2:
            raise ValueError("compared_band_count must be at least two")
        if self.challenged_band_indices[0] < 0:
            raise ValueError("challenged_band_indices must be nonnegative")
        if self.challenged_band_indices[-1] >= self.compared_band_count:
            raise ValueError("challenged band index lies outside compared bands")
        if self.plane_wave_cutoffs[0] <= 0:
            raise ValueError("plane_wave_cutoffs must be positive")
        if any(
            2 * cutoff + 1 < self.compared_band_count
            for cutoff in self.plane_wave_cutoffs
        ):
            raise ValueError(
                "every plane-wave sweep dimension must contain the compared bands"
            )
        required_isolation_bands = self.challenged_band_indices[-1] + 2
        if 2 * self.plane_wave_cutoffs[-1] + 1 < required_isolation_bands:
            raise ValueError(
                "finest plane-wave sweep dimension must contain every challenged "
                "band and its upper neighbor"
            )
        if self.finite_difference_points[0] <= 0:
            raise ValueError("finite_difference_points must be positive")
        if any(
            points < self.compared_band_count
            for points in self.finite_difference_points
        ):
            raise ValueError(
                "every finite-difference grid must contain the compared bands"
            )
        if any(
            shape.potential.harmonic_count > 2 * self.plane_wave_reference_cutoff
            for shape in self.potential_shapes
        ):
            raise ValueError(
                "potential-shape harmonics must fit the reference plane-wave matrix"
            )
        if any(
            mesh_size < 2 or mesh_size % 2 != 0
            for mesh_size in self.reciprocal_mesh_sizes
        ):
            raise ValueError(
                "reciprocal_mesh_sizes must contain even values of at least two"
            )
        if self.plane_wave_reference_cutoff <= self.plane_wave_cutoffs[-1]:
            raise ValueError("reference cutoff must exceed every sweep cutoff")
        if self.route_challenge_mesh_size not in self.reciprocal_mesh_sizes:
            raise ValueError("route challenge mesh must occur in reciprocal mesh sizes")
        if self.route_challenge_hopping_range_cells != self.hopping_range_cells:
            raise ValueError("route challenge and primary hopping ranges must agree")

    @property
    def period(self) -> ScalarQuantity:
        """Return the explicit common period of all challenge potential shapes.

        Returns
        -------
        ScalarQuantity
            Shared dimensionless direct-cell period.
        """
        return self.potential_shapes[0].potential.period


class Periodic1DReductionChallengeCampaignJsonSerializer(
    JsonCodec[Periodic1DReductionChallengeCampaignDefinition, bytes]
):
    """Adapt the historical schema-one challenge-input wire.

    Notes
    -----
    Canonical object attributes use reduction-challenge terminology. Serialization
    deliberately retains historical ``stress`` keys and the evidence-status literal so
    existing bytes and downstream wire identity are not silently rewritten.
    """

    __slots__ = ()

    decoder = Periodic1DCampaignJsonDecoder()

    def deserialize(
        self, payload: bytes
    ) -> Periodic1DReductionChallengeCampaignDefinition:
        """Decode strict historical JSON without executing any challenge case.

        Parameters
        ----------
        payload
            Exact UTF-8 schema-one input bytes.

        Returns
        -------
        Periodic1DReductionChallengeCampaignDefinition
            Typed immutable campaign controls.

        Raises
        ------
        TypeError
            If the payload or any decoded field has the wrong representation.
        ValueError
            If strict JSON, schema identity, units, controls, or correlations are
            invalid.
        """
        root = self.decoder.document(payload)
        expected = {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "potential_strengths",
            "plane_wave_cutoffs",
            "plane_wave_reference_cutoff",
            "finite_difference_points",
            "compared_band_count",
            "stress_band_indices",
            "potential_shapes",
            "reciprocal_mesh_sizes",
            "hopping_range_cells",
            "withheld_mesh_size",
            "isolation_gap_threshold",
            "route_stress_potential_strength",
            "route_stress_mesh_size",
            "route_stress_hopping_range_cells",
        }
        if set(root) != expected:
            raise ValueError("challenge input fields must match schema version one")
        if self.decoder.integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported challenge input schema version")
        if (
            self.decoder.string(root["evidence_status"], "evidence_status")
            != "illustrative numerical stress test"
        ):
            raise ValueError("unexpected evidence_status")
        # Historical field spellings are mapped explicitly; canonical attribute names
        # must never be inferred by normalizing arbitrary JSON keys.
        return Periodic1DReductionChallengeCampaignDefinition(
            self.decoder.string(root["experiment_id"], "experiment_id"),
            self.decoder.vector(root["potential_strengths"], "potential_strengths"),
            self.decoder.integers(root["plane_wave_cutoffs"], "plane_wave_cutoffs"),
            self.decoder.integer(
                root["plane_wave_reference_cutoff"], "plane_wave_reference_cutoff"
            ),
            self.decoder.integers(
                root["finite_difference_points"], "finite_difference_points"
            ),
            self.decoder.integer(root["compared_band_count"], "compared_band_count"),
            self.decoder.integers(root["stress_band_indices"], "stress_band_indices"),
            tuple(
                self._deserialize_potential_shape(item)
                for item in self.decoder.array(
                    root["potential_shapes"], "potential_shapes"
                )
            ),
            self.decoder.integers(
                root["reciprocal_mesh_sizes"], "reciprocal_mesh_sizes"
            ),
            self.decoder.integer(root["hopping_range_cells"], "hopping_range_cells"),
            self.decoder.integer(root["withheld_mesh_size"], "withheld_mesh_size"),
            self.decoder.scalar(
                root["isolation_gap_threshold"], "isolation_gap_threshold"
            ),
            self.decoder.scalar(
                root["route_stress_potential_strength"],
                "route_stress_potential_strength",
            ),
            self.decoder.integer(
                root["route_stress_mesh_size"], "route_stress_mesh_size"
            ),
            self.decoder.integer(
                root["route_stress_hopping_range_cells"],
                "route_stress_hopping_range_cells",
            ),
        )

    def serialize(self, value: Periodic1DReductionChallengeCampaignDefinition) -> bytes:
        """Encode canonical schema-one UTF-8 JSON with historical keys.

        Parameters
        ----------
        value
            Exact canonical reduction-challenge definition.

        Returns
        -------
        bytes
            Canonical sorted compact JSON terminated by one newline.

        Raises
        ------
        TypeError
            If ``value`` is not the exact definition type.
        ValueError
            If JSON encoding encounters a nonfinite numeric value.
        """
        if type(value) is not Periodic1DReductionChallengeCampaignDefinition:
            raise TypeError(
                "value must be Periodic1DReductionChallengeCampaignDefinition"
            )
        document = {
            "schema_version": 1,
            "experiment_id": value.experiment_id,
            "evidence_status": "illustrative numerical stress test",
            "potential_strengths": value.potential_strengths.magnitude.tolist(),
            "plane_wave_cutoffs": list(value.plane_wave_cutoffs),
            "plane_wave_reference_cutoff": value.plane_wave_reference_cutoff,
            "finite_difference_points": list(value.finite_difference_points),
            "compared_band_count": value.compared_band_count,
            "stress_band_indices": list(value.challenged_band_indices),
            "potential_shapes": [
                self._serialize_potential_shape(shape)
                for shape in value.potential_shapes
            ],
            "reciprocal_mesh_sizes": list(value.reciprocal_mesh_sizes),
            "hopping_range_cells": value.hopping_range_cells,
            "withheld_mesh_size": value.withheld_mesh_size,
            "isolation_gap_threshold": value.isolation_gap_threshold.magnitude,
            "route_stress_potential_strength": (
                value.route_challenge_potential_strength.magnitude
            ),
            "route_stress_mesh_size": value.route_challenge_mesh_size,
            "route_stress_hopping_range_cells": (
                value.route_challenge_hopping_range_cells
            ),
        }
        return (
            json.dumps(
                document,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")

    def _deserialize_potential_shape(
        self, value: object
    ) -> Periodic1DReductionChallengePotentialShape:
        """Decode one closed named finite-Fourier potential record."""
        shape = self.decoder.mapping(value, "potential shape")
        if set(shape) != {"id", "constant", "cosine_coefficients", "sine_coefficients"}:
            raise ValueError("potential shape fields are invalid")
        potential = PeriodicFourierPotential1D(
            ScalarQuantity(2.0 * np.pi, Unitless()),
            self.decoder.scalar(shape["constant"], "constant"),
            self.decoder.vector(shape["cosine_coefficients"], "cosine_coefficients"),
            self.decoder.vector(shape["sine_coefficients"], "sine_coefficients"),
        )
        return Periodic1DReductionChallengePotentialShape(
            self.decoder.string(shape["id"], "id"), potential
        )

    @staticmethod
    def _serialize_potential_shape(
        shape: Periodic1DReductionChallengePotentialShape,
    ) -> dict[str, object]:
        """Encode one exact canonical potential-shape control."""
        if type(shape) is not Periodic1DReductionChallengePotentialShape:
            raise TypeError("shape must be Periodic1DReductionChallengePotentialShape")
        return {
            "id": shape.identifier,
            "constant": shape.potential.constant_coefficient.magnitude,
            "cosine_coefficients": (
                shape.potential.cosine_coefficients.magnitude.tolist()
            ),
            "sine_coefficients": shape.potential.sine_coefficients.magnitude.tolist(),
        }
