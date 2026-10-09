"""Authenticated parent-data loading for the finite-rank-oracle campaign."""

from __future__ import annotations

import hashlib
from pathlib import Path

from ksdft2effmass.periodic1d import (
    Periodic1DFiniteHoppingToyModel,
    Periodic1DHoppingBlock,
)
from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization.json import JsonValue

from .contracts import FiniteRankOracleCampaignInput, FiniteRankOracleParentData


class FiniteRankOracleParentModelAdapter:
    """Report semantic and canonical retained-result identity channels.

    Parameters
    ----------
    semantic_identity
        Whether independently reconstructed typed semantics equal the campaign
        result. canonical_byte_identity Whether canonical serialization reproduces
        the retained result bytes exactly. calculated_sha256 Lowercase SHA-256
        digest calculated from the exact retained bytes. retained_sha256 Lowercase
        SHA-256 digest declared by the retained result document.
    """

    __slots__ = ()

    MODEL_ID = "periodic1d.finite-rank-oracle-parent.v1"
    HERMITICITY_TOLERANCE = 1.0e-11

    def execute(
        self,
        specification: FiniteRankOracleCampaignInput,
        blocks: tuple[Periodic1DHoppingBlock, ...],
    ) -> Periodic1DFiniteHoppingToyModel:
        """Construct the exact maintained finite-hopping toy-model contract.

        Parameters
        ----------
        specification
            Closed typed campaign specification owning all scientific controls.
        blocks
            Ordered parent hopping blocks with explicit lattice displacements.

        Returns
        -------
        Periodic1DFiniteHoppingToyModel
            Maintained finite-hopping toy model preserving the authenticated parent
            convention.
        """
        return Periodic1DFiniteHoppingToyModel(
            model_id=self.MODEL_ID,
            blocks=blocks,
            energy_unit=specification.parent.energy_unit,
            hermiticity_tolerance=self.HERMITICITY_TOLERANCE,
        )


class FiniteRankOracleParentDataLoader:
    """Authenticate and adapt the accepted two-orbital parent.

    :class:`Periodic1DCampaignJsonDecoder` exposes shared source-document and primitive
    JSON mechanics and owns the periodic complex-pair matrix wire.
    This action owns source authentication, parent-group selection, and hopping-block
    adaptation.
    """

    __slots__ = ("_decoder", "_model_adapter")

    def __init__(self) -> None:
        """Bind maintained wire decoding and explicit parent-model adaptation."""
        self._decoder = Periodic1DCampaignJsonDecoder()
        self._model_adapter = FiniteRankOracleParentModelAdapter()

    def execute(
        self, specification: FiniteRankOracleCampaignInput, repository_root: Path
    ) -> FiniteRankOracleParentData:
        """Authenticate declared sources and load the selected parent hoppings.

        Parameters
        ----------
        specification
            Closed typed campaign specification owning all scientific controls.
        repository_root
            Explicit absolute root confining authenticated repository-relative access.

        Returns
        -------
        FiniteRankOracleParentData
            Authenticated selected parent model and immutable hopping observations.

        Raises
        ------
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        for identity in specification.sources:
            if self._sha256(repository_root / identity.path) != identity.sha256:
                raise ValueError(f"source identity mismatch: {identity.path}")
        composite_source = specification.sources[0]
        composite = self._decoder.document(
            (repository_root / composite_source.path).read_bytes()
        )
        groups = self._records(composite["groups"], "groups")
        matches = [
            item for item in groups if item["id"] == specification.parent.group_id
        ]
        if len(matches) != 1:
            raise ValueError("parent group must occur exactly once")
        hoppings: list[Periodic1DHoppingBlock] = []
        for record in self._records(
            matches[0]["smooth_hopping_blocks"], "hopping blocks"
        ):
            displacement = self._decoder.integer(
                record["representative_cells"], "displacement"
            )
            if abs(displacement) <= specification.parent.hopping_range:
                hoppings.append(
                    Periodic1DHoppingBlock(
                        displacement_cells=displacement,
                        matrix=self._decoder.complex_matrix(
                            record["matrix"], "hopping matrix"
                        ),
                    )
                )
        expected = tuple(
            range(
                -specification.parent.hopping_range,
                specification.parent.hopping_range + 1,
            )
        )
        blocks = tuple(hoppings)
        if tuple(item.displacement_cells for item in blocks) != expected:
            raise ValueError("parent hopping range is incomplete")
        return FiniteRankOracleParentData(
            self._model_adapter.execute(specification, blocks), specification.sources
        )

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        """Adapt one JSON array to parent-source records."""
        return tuple(
            self._decoder.mapping(item, name)
            for item in self._decoder.array(value, name)
        )

    def _sha256(self, path: Path) -> str:
        """Compute one source identity for this parent-data action."""
        return hashlib.sha256(path.read_bytes()).hexdigest()
