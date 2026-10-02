"""Version-one isolated-band campaign wire mechanics."""

from __future__ import annotations

import json

from ksdft2effmass.serialization import JsonCodec

from ..definition import Periodic2DIsolatedBandCampaignDefinition
from .decoding import JsonValue, Periodic2DCampaignJsonDecoder


class Periodic2DIsolatedBandCampaignJsonSerializer(
    JsonCodec[Periodic2DIsolatedBandCampaignDefinition, bytes]
):
    """Decode and canonically encode the version-one isolated-band input."""

    __slots__ = ()

    decoder = Periodic2DCampaignJsonDecoder()

    def deserialize(self, payload: bytes) -> Periodic2DIsolatedBandCampaignDefinition:
        """Decode strict version-one JSON without executing the campaign."""
        root = self.decoder.document(payload)
        expected = {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "dimensionless_convention",
            "isotropic_potential",
            "anisotropic_control",
            "coupling_sequence",
            "plane_wave_cutoffs",
            "plane_wave_reference_cutoff",
            "finite_difference_points",
            "parent_sample_momenta",
            "parent_coupling",
            "compared_band_count",
            "common_low_mode_cutoff",
            "reciprocal_mesh_size",
            "withheld_mesh_size",
            "hopping_shell_squared_radii",
            "effective_mass_step",
            "topology_tolerances",
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
        convention = self._closed_mapping(
            root["dimensionless_convention"],
            "dimensionless_convention",
            {"lattice_period", "reciprocal_vector", "reciprocal_energy"},
        )
        isotropic = self._closed_mapping(
            root["isotropic_potential"],
            "isotropic_potential",
            {"lambda_x", "lambda_y"},
        )
        anisotropic = self._closed_mapping(
            root["anisotropic_control"],
            "anisotropic_control",
            {"lambda_x", "lambda_y", "lambda_xy"},
        )
        topology = self._closed_mapping(
            root["topology_tolerances"],
            "topology_tolerances",
            {"minimum_neighbor_overlap", "chern_integer_defect"},
        )
        momentum_values = self.decoder.array(
            root["parent_sample_momenta"], "parent_sample_momenta"
        )
        momenta: list[tuple[float, float]] = []
        for index, value in enumerate(momentum_values):
            pair = self.decoder.array(value, f"parent_sample_momenta[{index}]")
            if len(pair) != 2:
                raise ValueError("each parent momentum must have two entries")
            momenta.append(
                (
                    self.decoder.real(pair[0], f"parent_sample_momenta[{index}][0]"),
                    self.decoder.real(pair[1], f"parent_sample_momenta[{index}][1]"),
                )
            )
        return Periodic2DIsolatedBandCampaignDefinition(
            experiment_id=self.decoder.string(root["experiment_id"], "experiment_id"),
            lattice_period=self.decoder.real(
                convention["lattice_period"], "lattice_period"
            ),
            reciprocal_vector=self.decoder.real(
                convention["reciprocal_vector"], "reciprocal_vector"
            ),
            reciprocal_energy=self.decoder.real(
                convention["reciprocal_energy"], "reciprocal_energy"
            ),
            lambda_x=self.decoder.real(isotropic["lambda_x"], "lambda_x"),
            lambda_y=self.decoder.real(isotropic["lambda_y"], "lambda_y"),
            anisotropic_lambda_x=self.decoder.real(
                anisotropic["lambda_x"], "anisotropic lambda_x"
            ),
            anisotropic_lambda_y=self.decoder.real(
                anisotropic["lambda_y"], "anisotropic lambda_y"
            ),
            anisotropic_lambda_xy=self.decoder.real(
                anisotropic["lambda_xy"], "anisotropic lambda_xy"
            ),
            coupling_sequence=self.decoder.reals(
                root["coupling_sequence"], "coupling_sequence"
            ),
            plane_wave_cutoffs=self.decoder.integers(
                root["plane_wave_cutoffs"], "plane_wave_cutoffs"
            ),
            plane_wave_reference_cutoff=self.decoder.integer(
                root["plane_wave_reference_cutoff"], "plane_wave_reference_cutoff"
            ),
            finite_difference_points=self.decoder.integers(
                root["finite_difference_points"], "finite_difference_points"
            ),
            parent_sample_momenta=tuple(momenta),
            parent_coupling=self.decoder.real(
                root["parent_coupling"], "parent_coupling"
            ),
            compared_band_count=self.decoder.integer(
                root["compared_band_count"], "compared_band_count"
            ),
            common_low_mode_cutoff=self.decoder.integer(
                root["common_low_mode_cutoff"], "common_low_mode_cutoff"
            ),
            reciprocal_mesh_size=self.decoder.integer(
                root["reciprocal_mesh_size"], "reciprocal_mesh_size"
            ),
            withheld_mesh_size=self.decoder.integer(
                root["withheld_mesh_size"], "withheld_mesh_size"
            ),
            shell_squared_radii=self.decoder.integers(
                root["hopping_shell_squared_radii"],
                "hopping_shell_squared_radii",
            ),
            effective_mass_step=self.decoder.real(
                root["effective_mass_step"], "effective_mass_step"
            ),
            minimum_neighbor_overlap=self.decoder.real(
                topology["minimum_neighbor_overlap"], "minimum_neighbor_overlap"
            ),
            chern_integer_defect=self.decoder.real(
                topology["chern_integer_defect"], "chern_integer_defect"
            ),
        )

    def serialize(self, record: Periodic2DIsolatedBandCampaignDefinition) -> bytes:
        """Return deterministic canonical version-one UTF-8 JSON."""
        if type(record) is not Periodic2DIsolatedBandCampaignDefinition:
            raise TypeError("record must be Periodic2DIsolatedBandCampaignDefinition")
        document: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": record.experiment_id,
            "evidence_status": "illustrative numerical experiment",
            "dimensionless_convention": {
                "lattice_period": record.lattice_period,
                "reciprocal_vector": record.reciprocal_vector,
                "reciprocal_energy": record.reciprocal_energy,
            },
            "isotropic_potential": {
                "lambda_x": record.lambda_x,
                "lambda_y": record.lambda_y,
            },
            "anisotropic_control": {
                "lambda_x": record.anisotropic_lambda_x,
                "lambda_y": record.anisotropic_lambda_y,
                "lambda_xy": record.anisotropic_lambda_xy,
            },
            "coupling_sequence": list(record.coupling_sequence),
            "plane_wave_cutoffs": list(record.plane_wave_cutoffs),
            "plane_wave_reference_cutoff": record.plane_wave_reference_cutoff,
            "finite_difference_points": list(record.finite_difference_points),
            "parent_sample_momenta": [
                [momentum_x, momentum_y]
                for momentum_x, momentum_y in record.parent_sample_momenta
            ],
            "parent_coupling": record.parent_coupling,
            "compared_band_count": record.compared_band_count,
            "common_low_mode_cutoff": record.common_low_mode_cutoff,
            "reciprocal_mesh_size": record.reciprocal_mesh_size,
            "withheld_mesh_size": record.withheld_mesh_size,
            "hopping_shell_squared_radii": list(record.shell_squared_radii),
            "effective_mass_step": record.effective_mass_step,
            "topology_tolerances": {
                "minimum_neighbor_overlap": record.minimum_neighbor_overlap,
                "chern_integer_defect": record.chern_integer_defect,
            },
        }
        return (
            json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")

    def _closed_mapping(
        self,
        value: JsonValue,
        name: str,
        expected_fields: set[str],
    ) -> dict[str, JsonValue]:
        mapping = self.decoder.mapping(value, name)
        if set(mapping) != expected_fields:
            raise ValueError(f"{name} fields must match schema version one")
        return mapping
