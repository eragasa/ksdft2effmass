"""Versioned Appendix G composite-band campaign input contract."""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.periodic import (
    PeriodicOperatorReference,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)
from ksdft2effmass.periodic1d import (
    Periodic1DFourierHamiltonianToyModel,
    Periodic1DRetainedBandGroupDefinition,
    Periodic1DSelectedBandRetentionDefinition,
)
from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.serialization.json import JsonValue


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignDefinition:
    """Retain the closed version-one Appendix G composite-study controls.

    Parameters
    ----------
    experiment_id
        Nonempty stable identity shared by the encoded input and result.
    period
        Positive direct-lattice period in the historical dimensionless coordinate
        convention.
    potential_strength_over_recoil
        Cosine-potential amplitude divided by the recoil-energy scale :math:`E_G`.
    plane_wave_cutoff
        Positive symmetric reciprocal-index cutoff. The finite parent representation
        therefore has dimension ``2 * plane_wave_cutoff + 1``.
    reciprocal_mesh_size
        Even count of at least two ordered half-open reciprocal samples used for the
        complete discrete Fourier representation.
    withheld_mesh_size
        Positive count of distinct samples used only for withheld comparisons.
    parent_model
        Explicit untruncated Fourier Hamiltonian parent. This is not the finite
        plane-wave representation used by retained-operator adoption.
    retained_band_groups
        Ordered, nonoverlapping, parent-qualified contiguous-band definitions.
    hopping_ranges_cells
        Unique increasing nonnegative symmetric cell ranges used by the finite-range
        study.
    external_gap_threshold
        Positive sampled external-isolation threshold in units of :math:`E_G`.
    direct_route_range_cells
        One member of ``hopping_ranges_cells`` used by the direct-fit comparison.
    controlled_gauge_amplitude, rough_gauge_amplitude
        Dimensionless historical gauge-control amplitudes.

    Raises
    ------
    TypeError
        If a field uses the wrong exact semantic representation.
    ValueError
        If identities, units, dimensions, mesh parity, parent conventions, retained
        selections, or ordered controls violate the closed schema-one contract.

    Notes
    -----
    This DataObject owns campaign controls, not a calculated retained space, finite
    representation, represented operator, effective model, convergence result, or
    scientific acceptance decision. Parent-model, finite-representation, retention,
    gauge, Fourier, truncation, and comparison errors remain distinct.
    """

    experiment_id: str
    period: ScalarQuantity
    potential_strength_over_recoil: ScalarQuantity
    plane_wave_cutoff: int
    reciprocal_mesh_size: int
    withheld_mesh_size: int
    parent_model: Periodic1DFourierHamiltonianToyModel = field(compare=False)
    retained_band_groups: tuple[Periodic1DRetainedBandGroupDefinition, ...]
    hopping_ranges_cells: tuple[int, ...]
    external_gap_threshold: ScalarQuantity
    direct_route_range_cells: int
    controlled_gauge_amplitude: ScalarQuantity
    rough_gauge_amplitude: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate the closed campaign identity and control graph."""
        self._check_args_identity_and_quantities()
        self._check_args_integer_controls()
        self._check_args_parent_model()
        self._check_args_retained_band_groups()
        self._check_args_hopping_ranges()

    def _check_args_identity_and_quantities(self) -> None:
        """Require an exact identity and unitless scalar control representations."""
        if type(self.experiment_id) is not str:
            raise TypeError("experiment_id must be a built-in str")
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        for quantity_name, quantity in (
            ("period", self.period),
            ("potential_strength_over_recoil", self.potential_strength_over_recoil),
            ("external_gap_threshold", self.external_gap_threshold),
            ("controlled_gauge_amplitude", self.controlled_gauge_amplitude),
            ("rough_gauge_amplitude", self.rough_gauge_amplitude),
        ):
            if type(quantity) is not ScalarQuantity:
                raise TypeError(f"{quantity_name} must be ScalarQuantity")
            if not isinstance(quantity.unit, Unitless):
                raise ValueError(f"{quantity_name} must be unitless")
        if self.period.magnitude <= 0.0:
            raise ValueError("period must be positive")
        if self.external_gap_threshold.magnitude <= 0.0:
            raise ValueError("external_gap_threshold must be positive")

    def _check_args_integer_controls(self) -> None:
        """Require positive exact integers for finite dimensions and route control."""
        for integer_name, integer_value in (
            ("plane_wave_cutoff", self.plane_wave_cutoff),
            ("reciprocal_mesh_size", self.reciprocal_mesh_size),
            ("withheld_mesh_size", self.withheld_mesh_size),
            ("direct_route_range_cells", self.direct_route_range_cells),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{integer_name} must be a built-in int")
            if integer_value <= 0:
                raise ValueError(f"{integer_name} must be positive")
        if self.reciprocal_mesh_size < 2 or self.reciprocal_mesh_size % 2 != 0:
            raise ValueError(
                "reciprocal_mesh_size must be an even integer greater than or "
                "equal to 2"
            )

    def _check_args_parent_model(self) -> None:
        """Bind controls to the exact schema-one untruncated cosine parent."""
        if type(self.parent_model) is not Periodic1DFourierHamiltonianToyModel:
            raise TypeError("parent_model must be Periodic1DFourierHamiltonianToyModel")
        if self.parent_model.potential.period != self.period:
            raise ValueError("parent model period must equal campaign period")
        parent_potential = self.parent_model.potential
        # The historical wire stores one cosine amplitude rather than an arbitrary
        # Fourier series. Keep that schema convention explicit instead of inferring it
        # from a model name or from the eventual represented matrix dimension.
        if (
            parent_potential.constant_coefficient != ScalarQuantity(0.0, Unitless())
            or parent_potential.cosine_coefficients.magnitude.shape != (1,)
            or parent_potential.cosine_coefficients.magnitude[0]
            != self.potential_strength_over_recoil.magnitude
            or parent_potential.sine_coefficients.magnitude.shape != (1,)
            or parent_potential.sine_coefficients.magnitude[0] != 0.0
            or self.parent_model.recoil_energy != ScalarQuantity(1.0, Unitless())
        ):
            raise ValueError("parent model must match schema-one cosine convention")

    def _check_args_retained_band_groups(self) -> None:
        """Require unique nonoverlapping selections supported by the finite parent."""
        if (
            not isinstance(self.retained_band_groups, tuple)
            or not self.retained_band_groups
        ):
            raise TypeError("retained_band_groups must be a nonempty tuple")
        if any(
            type(group) is not Periodic1DRetainedBandGroupDefinition
            for group in self.retained_band_groups
        ):
            raise TypeError(
                "every retained group must be Periodic1DRetainedBandGroupDefinition"
            )
        identifiers = tuple(group.identifier for group in self.retained_band_groups)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("retained group identifiers must be unique")
        expected_parent = PeriodicOperatorReference(
            model_id=self.parent_model.model_id,
            operator_id=f"{self.parent_model.model_id}.bloch-hamiltonian",
            state_space_id=self.parent_model.state_space_id,
            spatial_dimension=1,
        )
        for group in self.retained_band_groups:
            retention = group.retained_bands.retention
            if retention.parent_operator != expected_parent:
                raise ValueError(
                    "every retained group must reference the declared untruncated "
                    "parent operator"
                )
            if retention.reciprocal_domain_id != (
                self.parent_model.reciprocal_domain_id
            ):
                raise ValueError(
                    "every retained group must reference the declared parent "
                    "reciprocal domain"
                )
        occupied_indices = [
            band_index
            for group in self.retained_band_groups
            for band_index in range(group.lower_index, group.upper_index + 1)
        ]
        if len(set(occupied_indices)) != len(occupied_indices):
            raise ValueError("retained band groups must not overlap")
        finite_parent_dimension = 2 * self.plane_wave_cutoff + 1
        if max(occupied_indices) >= finite_parent_dimension:
            raise ValueError("retained band indices must fit the finite parent")

    def _check_args_hopping_ranges(self) -> None:
        """Require ordered nonnegative ranges containing the direct route."""
        if (
            not isinstance(self.hopping_ranges_cells, tuple)
            or not self.hopping_ranges_cells
            or any(type(value) is not int for value in self.hopping_ranges_cells)
        ):
            raise TypeError("hopping_ranges_cells must be a nonempty integer tuple")
        if tuple(sorted(set(self.hopping_ranges_cells))) != self.hopping_ranges_cells:
            raise ValueError("hopping ranges must be unique and increasing")
        if self.hopping_ranges_cells[0] < 0:
            raise ValueError("hopping ranges must be nonnegative")
        if self.direct_route_range_cells not in self.hopping_ranges_cells:
            raise ValueError("direct route range must occur in hopping ranges")


class Periodic1DCompositeCampaignJsonSerializer(
    JsonCodec[Periodic1DCompositeCampaignDefinition, bytes]
):
    """Decode and canonically encode the retained version-one composite input.

    Notes
    -----
    Decoding constructs the explicit untruncated Fourier parent and parent-qualified
    retained-band definitions required by the campaign contract. It does not construct
    the cutoff plane-wave parent representation, retained mathematical spaces or
    operators, gauge-dependent represented forms, or any numerical result.
    """

    __slots__ = ()

    decoder = Periodic1DCampaignJsonDecoder()

    def deserialize(self, payload: bytes) -> Periodic1DCompositeCampaignDefinition:
        """Decode strict campaign JSON without executing the study.

        Parameters
        ----------
        payload
            Exact UTF-8 schema-one composite-input bytes.

        Returns
        -------
        Periodic1DCompositeCampaignDefinition
            Immutable typed controls with explicit parent and retention definitions.

        Raises
        ------
        TypeError
            If a JSON primitive has the wrong exact semantic representation.
        ValueError
            If decoding, schema, units, values, or intrinsic correlations are invalid.
        """
        root = self.decoder.document(payload)
        expected = {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "period",
            "potential_strength_over_recoil",
            "plane_wave_cutoff",
            "reciprocal_mesh_size",
            "withheld_mesh_size",
            "retained_band_groups",
            "hopping_ranges_cells",
            "external_gap_threshold",
            "direct_route_range_cells",
            "controlled_gauge_amplitude",
            "rough_gauge_amplitude",
        }
        if set(root) != expected:
            raise ValueError("composite input fields must match schema version one")
        if self.decoder.integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported composite input schema version")
        if (
            self.decoder.string(root["evidence_status"], "evidence_status")
            != "illustrative numerical verification"
        ):
            raise ValueError("unexpected evidence_status")
        experiment_id = self.decoder.string(root["experiment_id"], "experiment_id")
        period = ScalarQuantity(self.decoder.real(root["period"], "period"), Unitless())
        strength = ScalarQuantity(
            self.decoder.real(
                root["potential_strength_over_recoil"],
                "potential_strength_over_recoil",
            ),
            Unitless(),
        )
        parent_model = self._parent_model(experiment_id, period, strength)
        groups = tuple(
            self.decode_group(value, experiment_id, parent_model)
            for value in self.decoder.array(
                root["retained_band_groups"], "retained_band_groups"
            )
        )
        return Periodic1DCompositeCampaignDefinition(
            experiment_id,
            period,
            strength,
            self.decoder.integer(root["plane_wave_cutoff"], "plane_wave_cutoff"),
            self.decoder.integer(root["reciprocal_mesh_size"], "reciprocal_mesh_size"),
            self.decoder.integer(root["withheld_mesh_size"], "withheld_mesh_size"),
            parent_model,
            groups,
            tuple(
                self.decoder.integer(value, "hopping range")
                for value in self.decoder.array(
                    root["hopping_ranges_cells"], "hopping_ranges_cells"
                )
            ),
            ScalarQuantity(
                self.decoder.real(
                    root["external_gap_threshold"], "external_gap_threshold"
                ),
                Unitless(),
            ),
            self.decoder.integer(
                root["direct_route_range_cells"], "direct_route_range_cells"
            ),
            ScalarQuantity(
                self.decoder.real(
                    root["controlled_gauge_amplitude"], "controlled_gauge_amplitude"
                ),
                Unitless(),
            ),
            ScalarQuantity(
                self.decoder.real(
                    root["rough_gauge_amplitude"], "rough_gauge_amplitude"
                ),
                Unitless(),
            ),
        )

    def serialize(self, value: Periodic1DCompositeCampaignDefinition) -> bytes:
        """Return canonical UTF-8 JSON retaining historical field meanings.

        Parameters
        ----------
        value
            Exact composite campaign definition to encode.

        Returns
        -------
        bytes
            Canonical sorted, compact, newline-terminated UTF-8 JSON.

        Raises
        ------
        TypeError
            If ``value`` is not an exact composite campaign definition.
        """
        if type(value) is not Periodic1DCompositeCampaignDefinition:
            raise TypeError("value must be Periodic1DCompositeCampaignDefinition")
        payload = {
            "schema_version": 1,
            "experiment_id": value.experiment_id,
            "evidence_status": "illustrative numerical verification",
            "period": value.period.magnitude,
            "potential_strength_over_recoil": (
                value.potential_strength_over_recoil.magnitude
            ),
            "plane_wave_cutoff": value.plane_wave_cutoff,
            "reciprocal_mesh_size": value.reciprocal_mesh_size,
            "withheld_mesh_size": value.withheld_mesh_size,
            "retained_band_groups": [
                self.encode_group(group) for group in value.retained_band_groups
            ],
            "hopping_ranges_cells": list(value.hopping_ranges_cells),
            "external_gap_threshold": value.external_gap_threshold.magnitude,
            "direct_route_range_cells": value.direct_route_range_cells,
            "controlled_gauge_amplitude": value.controlled_gauge_amplitude.magnitude,
            "rough_gauge_amplitude": value.rough_gauge_amplitude.magnitude,
        }
        return (
            json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")

    def decode_group(
        self,
        value: JsonValue,
        experiment_id: str,
        parent_model: Periodic1DFourierHamiltonianToyModel,
    ) -> Periodic1DRetainedBandGroupDefinition:
        """Decode one parent-qualified retained contiguous-band group.

        Parameters
        ----------
        value
            Strict immutable JSON value for one group object.
        experiment_id
            Stable campaign identity used to construct explicit retention identities.
        parent_model
            Exact untruncated parent referenced by the encoded definition.

        Returns
        -------
        Periodic1DRetainedBandGroupDefinition
            Named contiguous-band selection with complete parent-qualified retention.

        Raises
        ------
        TypeError
            If a field uses the wrong exact JSON representation.
        ValueError
            If fields are missing, extra, empty, noncontiguous, or unordered.
        """
        group = self.decoder.mapping(value, "retained band group")
        if set(group) != {"id", "band_indices"}:
            raise ValueError("retained band group fields are invalid")
        indices = self.decoder.array(group["band_indices"], "band_indices")
        if not indices:
            raise ValueError("band_indices must be nonempty")
        parsed = tuple(self.decoder.integer(item, "band index") for item in indices)
        if parsed != tuple(range(parsed[0], parsed[-1] + 1)):
            raise ValueError("band_indices must be contiguous and increasing")
        identifier = self.decoder.string(group["id"], "id")
        selection = ContiguousBandSelection(parsed[0], parsed[-1])
        retention = PeriodicRetentionDefinition(
            retention_id=f"{experiment_id}.retention.{identifier}",
            parent_operator=PeriodicOperatorReference(
                model_id=parent_model.model_id,
                operator_id=f"{parent_model.model_id}.bloch-hamiltonian",
                state_space_id=parent_model.state_space_id,
                spatial_dimension=1,
            ),
            retained_space_id=f"{experiment_id}.retained-space.{identifier}",
            kind=PeriodicRetentionKind.SELECTED_BANDS,
            rank=selection.band_count,
            ordered_state_labels=tuple(f"band-{index}" for index in parsed),
            reciprocal_domain_id=parent_model.reciprocal_domain_id,
            construction_record_id=(
                f"{experiment_id}.selection.{identifier}.contiguous-bands"
            ),
            assumption_ids=(),
            provenance_id=f"{experiment_id}.encoded-input",
        )
        return Periodic1DRetainedBandGroupDefinition(
            identifier,
            Periodic1DSelectedBandRetentionDefinition(retention, selection),
        )

    def encode_group(
        self, value: Periodic1DRetainedBandGroupDefinition
    ) -> dict[str, JsonValue]:
        """Encode one retained contiguous-band group representation.

        Parameters
        ----------
        value
            Exact parent-qualified retained band-group definition.

        Returns
        -------
        dict
            Historical ``id`` and ordered ``band_indices`` wire representation.

        Raises
        ------
        TypeError
            If ``value`` has the wrong exact semantic type.
        """
        if type(value) is not Periodic1DRetainedBandGroupDefinition:
            raise TypeError("value must be Periodic1DRetainedBandGroupDefinition")
        return {
            "id": value.identifier,
            "band_indices": list(range(value.lower_index, value.upper_index + 1)),
        }

    @staticmethod
    def _parent_model(
        experiment_id: str,
        period: ScalarQuantity,
        strength: ScalarQuantity,
    ) -> Periodic1DFourierHamiltonianToyModel:
        """Compose the schema-one cosine parent without changing wire bytes."""
        potential = PeriodicFourierPotential1D(
            period=period,
            constant_coefficient=ScalarQuantity(0.0, Unitless()),
            cosine_coefficients=VectorQuantity(
                np.asarray([strength.magnitude], dtype=np.float64), Unitless()
            ),
            sine_coefficients=VectorQuantity(
                np.asarray([0.0], dtype=np.float64), Unitless()
            ),
        )
        return Periodic1DFourierHamiltonianToyModel(
            model_id=f"{experiment_id}.parent",
            state_space_id=f"{experiment_id}.bloch-state-space",
            reciprocal_domain_id=f"{experiment_id}.primitive-reduced-zone",
            potential=potential,
            recoil_energy=ScalarQuantity(1.0, Unitless()),
        )
