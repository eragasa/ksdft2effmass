"""Independent predecessor-map relation helpers."""

from __future__ import annotations


def has_complete_predecessor_pairs(
    old_ids: tuple[str, ...],
    new_ids: tuple[str, ...],
    pairs: tuple[tuple[str, str], ...],
) -> bool:
    """Return whether one-to-one pairs exactly cover both declared inventories."""
    return (
        len(pairs) == len(old_ids) == len(new_ids)
        and len({old for old, _ in pairs}) == len(pairs)
        and len({new for _, new in pairs}) == len(pairs)
        and {old for old, _ in pairs} == set(old_ids)
        and {new for _, new in pairs} == set(new_ids)
    )
