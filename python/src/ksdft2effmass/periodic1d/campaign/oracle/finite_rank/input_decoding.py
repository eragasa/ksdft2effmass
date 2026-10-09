"""Strict input-document decoding for the finite-rank-oracle campaign."""

from __future__ import annotations

from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization.json import JsonValue

from .contracts import (
    FiniteRankOracleCampaignInput,
    FiniteRankOracleSourceIdentity,
    FiniteRankOracleTolerances,
    FiniteRankParentContract,
    FiniteRankSpecialControls,
    RankOneOracleContract,
)


class FiniteRankOracleCampaignInputDeserializer:
    """Identify one immutable source artifact.

    Parameters
    ----------
    path
        Nonempty repository-relative path of an authenticated compact source. sha256
        Lowercase 64-character SHA-256 content identity.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    __slots__ = ("_decoder",)

    def __init__(self) -> None:
        """Bind the maintained campaign JSON decoder."""
        self._decoder = Periodic1DCampaignJsonDecoder()

    def execute(self, payload: bytes) -> FiniteRankOracleCampaignInput:
        """Decode strict UTF-8 JSON into the closed version-one input.

        Parameters
        ----------
        payload
            Exact immutable encoded JSON bytes.

        Returns
        -------
        FiniteRankOracleCampaignInput
            Closed immutable version-one finite-rank-oracle input.

        Raises
        ------
        TypeError
            An argument does not have the required exact public type.
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        root = self._decoder.document(payload)
        if set(root) != {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "source_identities",
            "parent_contract",
            "rank_one_contract",
            "special_controls",
            "tolerances",
        }:
            raise ValueError("input fields must match the version-one contract")
        if self._decoder.integer(root["schema_version"], "schema version") != 1:
            raise ValueError("unsupported schema version")
        if root["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status mismatch")
        sources = tuple(
            FiniteRankOracleSourceIdentity(
                self._decoder.nonempty_string(item["path"], "source path"),
                self._decoder.sha256(item["sha256"], "source sha256"),
            )
            for item in self._records(root["source_identities"], "sources")
        )
        parent = self._decoder.mapping(root["parent_contract"], "parent")
        rank_one = self._decoder.mapping(root["rank_one_contract"], "rank one")
        special = self._decoder.mapping(root["special_controls"], "special")
        tolerances = self._decoder.mapping(root["tolerances"], "tolerances")
        return FiniteRankOracleCampaignInput(
            self._decoder.nonempty_string(root["experiment_id"], "experiment id"),
            sources,
            FiniteRankParentContract(
                self._decoder.nonempty_string(parent["composite_group_id"], "group id"),
                self._decoder.integer(parent["hopping_range_cells"], "hopping range"),
                self._decoder.real(parent["supercell_momentum"], "momentum"),
                self._decoder.nonempty_string(parent["energy_unit"], "energy unit"),
                self._decoder.nonempty_string(
                    parent["site_orbital_ordering"], "ordering"
                ),
            ),
            RankOneOracleContract(
                self._decoder.integers(rank_one["supercell_sizes"], "cell counts"),
                self._decoder.reals(
                    rank_one["attractive_magnitudes"], "attractive magnitudes"
                ),
                self._decoder.real(rank_one["orbital_angle_radians"], "orbital angle"),
                self._decoder.real(
                    rank_one["orbital_relative_phase_radians"], "orbital phase"
                ),
                self._decoder.integer(rank_one["defect_site"], "defect site"),
                self._decoder.nonempty_string(
                    rank_one["resolvent_equation"], "equation"
                ),
                self._decoder.nonempty_string(rank_one["root_domain"], "root domain"),
                self._decoder.nonempty_string(
                    rank_one["root_selection"], "root selection"
                ),
            ),
            FiniteRankSpecialControls(
                self._decoder.integer(special["cell_count"], "special cell count"),
                self._decoder.real(
                    special["attractive_magnitude"], "special attraction"
                ),
                self._decoder.real(special["repulsive_magnitude"], "repulsion"),
                self._decoder.real(special["threshold_magnitude"], "threshold"),
                self._decoder.integer(special["spin_degeneracy"], "spin degeneracy"),
            ),
            FiniteRankOracleTolerances(
                self._decoder.real(tolerances["root_interval"], "root interval"),
                self._decoder.real(tolerances["secular_residual"], "secular residual"),
                self._decoder.real(tolerances["energy_agreement"], "energy agreement"),
                self._decoder.real(tolerances["eigen_residual"], "eigen residual"),
                self._decoder.real(
                    tolerances["projector_agreement"], "projector agreement"
                ),
                self._decoder.real(
                    tolerances["bound_state_edge_margin"], "edge margin"
                ),
            ),
        )

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        """Adapt one JSON array to the record sequence required by this schema."""
        return tuple(
            self._decoder.mapping(item, name)
            for item in self._decoder.array(value, name)
        )
