"""Immutable inventories of explicitly declared periodic basis identities."""

from __future__ import annotations

from dataclasses import dataclass

from .basis import PeriodicBasisIdentity


@dataclass(frozen=True, slots=True)
class PeriodicBasisInventoryEntry[BasisT: PeriodicBasisIdentity]:
    """Bind one admitted retained rank to one exact ordered basis identity.

    Parameters
    ----------
    retained_rank
        Positive built-in retained-space dimension.
    basis_identity
        Explicit structured periodic basis whose coordinate count equals
        ``retained_rank``.
    """

    retained_rank: int
    basis_identity: BasisT

    def __post_init__(self) -> None:
        """Validate exact rank and basis correlation."""
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank <= 0:
            raise ValueError("retained_rank must be positive")
        if not isinstance(self.basis_identity, PeriodicBasisIdentity):
            raise TypeError("basis_identity must be a PeriodicBasisIdentity")
        if self.basis_identity.dimension != self.retained_rank:
            raise ValueError("basis identity dimension must match retained_rank")


@dataclass(frozen=True, slots=True)
class PeriodicBasisInventory[BasisT: PeriodicBasisIdentity]:
    """Own one immutable finite mapping from retained rank to basis identity.

    The inventory does not synthesize coordinates from rank. Every entry must be
    explicitly supplied by its composition owner. One inventory is homogeneous in
    dimensional concrete basis type and coordinate family.

    Parameters
    ----------
    entries
        Nonempty tuple of explicitly declared rank/basis entries.
    """

    entries: tuple[PeriodicBasisInventoryEntry[BasisT], ...]

    def __post_init__(self) -> None:
        """Require a unique, ordered, homogeneous rank inventory."""
        if type(self.entries) is not tuple or not self.entries:
            raise TypeError("entries must be a nonempty tuple")
        if any(
            type(entry) is not PeriodicBasisInventoryEntry for entry in self.entries
        ):
            raise TypeError(
                "entries must contain exact PeriodicBasisInventoryEntry values"
            )
        ranks = tuple(entry.retained_rank for entry in self.entries)
        if len(set(ranks)) != len(ranks):
            raise ValueError("entries must have unique retained ranks")
        if ranks != tuple(sorted(ranks)):
            raise ValueError("entries must be ordered by increasing retained rank")
        basis_type = type(self.entries[0].basis_identity)
        basis_family = self.entries[0].basis_identity.family
        if any(type(entry.basis_identity) is not basis_type for entry in self.entries):
            raise ValueError("entries must use one concrete dimensional basis type")
        if any(
            entry.basis_identity.family is not basis_family for entry in self.entries
        ):
            raise ValueError("entries must use one coordinate family")

    @property
    def retained_ranks(self) -> tuple[int, ...]:
        """Return admitted ranks in deterministic increasing order."""
        return tuple(entry.retained_rank for entry in self.entries)

    def basis_identity_for_rank(self, retained_rank: int) -> BasisT:
        """Return the explicitly declared basis for one admitted rank.

        Parameters
        ----------
        retained_rank
            Positive built-in rank selected by the caller.

        Returns
        -------
        BasisT
            Exact structured identity declared for ``retained_rank``.

        Raises
        ------
        TypeError
            If ``retained_rank`` is not a built-in integer.
        ValueError
            If no entry declares ``retained_rank``.
        """
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        for entry in self.entries:
            if entry.retained_rank == retained_rank:
                return entry.basis_identity
        raise ValueError("retained_rank is not declared by this basis inventory")


__all__ = ["PeriodicBasisInventory", "PeriodicBasisInventoryEntry"]
