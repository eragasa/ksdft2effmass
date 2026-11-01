"""Shared rank-N band-alignment protocol inventories."""

RETAINED_RANKS = (3, 4, 8, 16)
CIRCUIT_DEPTHS = (1, 2, 4, 8)
CONSTRUCTION_MESH_SIZES = (513, 1025, 2049)

__all__ = [
    "CIRCUIT_DEPTHS",
    "CONSTRUCTION_MESH_SIZES",
    "RETAINED_RANKS",
]
