"""Exact encoded result-document ownership for the isolated periodic-2D campaign.

This module owns wire bytes and their derived content identity only. Decoding,
scientific interpretation, calculation provenance, numerical verification, convergence,
uncertainty quantification, and acceptance remain responsibilities of explicit campaign
Actions and evidence owners.
"""

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandResultDocument:
    """Retain one exact encoded version-one periodic-2D result document.

    Parameters
    ----------
    payload
        Exact nonempty built-in :class:`bytes` for the encoded result document. The
        supplied byte object is retained without decoding, normalization, coercion, or
        copying.

    Raises
    ------
    TypeError
        If ``payload`` is not exact built-in :class:`bytes`; byte subclasses are not
        accepted.
    ValueError
        If ``payload`` is empty.

    Notes
    -----
    This DataObject assigns no schema, physical-model, finite-representation,
    retained-space, operator, basis, gauge, geometry, unit, provenance, convergence,
    validation, uncertainty, or acceptance meaning. SHA-256 establishes content
    identity only.
    """

    payload: bytes

    def __post_init__(self) -> None:
        """Delegate validation of the intrinsic exact-byte invariant."""
        self._check_args_payload()

    def _check_args_payload(self) -> None:
        """Require one nonempty exact built-in byte representation."""
        if type(self.payload) is not bytes:
            raise TypeError("payload must be exact built-in bytes")
        if not self.payload:
            raise ValueError("payload must be nonempty")

    @property
    def sha256(self) -> str:
        """Return the lowercase SHA-256 content identity.

        Returns
        -------
        str
            A 64-character lowercase hexadecimal digest of the exact retained bytes.

        Notes
        -----
        The digest is derived from ``payload`` on access. It does not authenticate an
        author, repository location, calculation, provenance chain, or scientific claim.
        """
        # Hash the encapsulated bytes directly: canonical re-encoding would change the
        # identity boundary and silently conflate wire retention with serialization.
        return hashlib.sha256(self.payload).hexdigest()
