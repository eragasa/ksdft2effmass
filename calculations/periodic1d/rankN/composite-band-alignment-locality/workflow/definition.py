"""Frozen controls for the higher-rank D1 P0/G0 development calculation."""

from __future__ import annotations

from dataclasses import dataclass

FAMILY_ID = (
    "ksdft2effmass.campaign.periodic-reduction.periodic1d."
    "higher-rank-composite-band-alignment-and-locality"
)
VERSION_ID = f"{FAMILY_ID}.v1"
PRODUCER_METHOD_ID = f"{VERSION_ID}.schema-free-development-calculator.v1"
VERIFIER_METHOD_ID = (
    "ksdft2effmass.verify.periodic-reduction.periodic1d."
    "higher-rank-composite-band-alignment-and-locality.direct-formula.v1"
)

RANKS = (3, 4, 8, 16)
DEPTHS = (1, 2, 4, 8)
CONSTRUCTION_MESH_SIZES = (513, 1025, 2049)
FINAL_CONSTRUCTION_MESH_SIZE = CONSTRUCTION_MESH_SIZES[-1]
EVALUATION_MESH_SIZE = 8191
EXACT_ISOLATION = 2.1
SUPPORTS = (0, 1, 2, 4, 8, 16, 32, 64, 128)
CHANNELS = ("A0", "A1", "A2", "A3")


@dataclass(frozen=True, slots=True)
class HigherRankD1CaseDefinition:
    """Select one prespecified finite D1 rank/depth case."""

    rank: int
    depth: int

    def __post_init__(self) -> None:
        """Reject noncanonical ranks and depths without coercion."""
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank not in RANKS:
            raise ValueError(f"rank must be one of {RANKS}")
        if type(self.depth) is not int:
            raise TypeError("depth must be a built-in int")
        if self.depth not in DEPTHS:
            raise ValueError(f"depth must be one of {DEPTHS}")

    @property
    def case_id(self) -> str:
        """Return the canonical rank-major/depth-minor case identity."""
        return f"r{self.rank:02d}-L{self.depth:02d}"

    @property
    def ambient_dimension(self) -> int:
        """Return the property-by-construction parent-fiber dimension."""
        return 2 * self.rank

    @property
    def basis_identifier(self) -> str:
        """Return the ordered retained-coordinate basis identity."""
        return f"D1-P0-G0-retained-basis-r{self.rank:02d}"


@dataclass(frozen=True, slots=True)
class HigherRankD1Definition:
    """Retain the complete immutable D1 case ordering and global controls."""

    cases: tuple[HigherRankD1CaseDefinition, ...] = tuple(
        HigherRankD1CaseDefinition(rank, depth) for rank in RANKS for depth in DEPTHS
    )
    construction_mesh_sizes: tuple[int, ...] = CONSTRUCTION_MESH_SIZES
    evaluation_mesh_size: int = EVALUATION_MESH_SIZE
    supports: tuple[int, ...] = SUPPORTS
    channels: tuple[str, ...] = CHANNELS
    energy_reference: float = 1.0

    def __post_init__(self) -> None:
        """Require the exact v1 inventories and positive binary64 energy scale."""
        expected_cases = tuple(
            HigherRankD1CaseDefinition(rank, depth)
            for rank in RANKS
            for depth in DEPTHS
        )
        if type(self.cases) is not tuple or self.cases != expected_cases:
            raise ValueError("cases must equal the exact rank-major D1 v1 inventory")
        if self.construction_mesh_sizes != CONSTRUCTION_MESH_SIZES:
            raise ValueError("construction_mesh_sizes must equal the D1 v1 inventory")
        if type(self.evaluation_mesh_size) is not int:
            raise TypeError("evaluation_mesh_size must be a built-in int")
        if self.evaluation_mesh_size != EVALUATION_MESH_SIZE:
            raise ValueError("evaluation_mesh_size must equal the D1 v1 value")
        if self.supports != SUPPORTS:
            raise ValueError("supports must equal the D1 v1 inventory")
        if self.channels != CHANNELS:
            raise ValueError("channels must equal the D1 v1 inventory")
        if type(self.energy_reference) is not float:
            raise TypeError("energy_reference must be a built-in float")
        if self.energy_reference != 1.0:
            raise ValueError("D1 v1 requires energy_reference=1.0")


__all__ = [
    "CHANNELS",
    "CONSTRUCTION_MESH_SIZES",
    "DEPTHS",
    "EVALUATION_MESH_SIZE",
    "EXACT_ISOLATION",
    "FAMILY_ID",
    "FINAL_CONSTRUCTION_MESH_SIZE",
    "PRODUCER_METHOD_ID",
    "RANKS",
    "SUPPORTS",
    "VERIFIER_METHOD_ID",
    "VERSION_ID",
    "HigherRankD1CaseDefinition",
    "HigherRankD1Definition",
]
