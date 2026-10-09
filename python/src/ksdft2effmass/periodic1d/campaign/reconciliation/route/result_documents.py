"""Exact encoded result-document ownership for route reconciliation.

This module owns retained wire bytes and derived content identity only. Route identity,
state-space compatibility, comparison, execution provenance, convergence, scientific
validation, uncertainty quantification, and acceptance remain responsibilities of
explicit campaign Actions and evidence owners.
"""

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RouteReconciliationCampaignResultDocument:
    """Retain one exact encoded route-reconciliation result document.

    Parameters
    ----------
    payload
        Exact nonempty built-in :class:`bytes` for the encoded result wire. The
        supplied object is retained without decoding, normalization, coercion,
        re-encoding, or copying.

    Raises
    ------
    TypeError
        If ``payload`` is not exact built-in :class:`bytes`; byte subclasses are not
        accepted.
    ValueError
        If ``payload`` is empty.

    Notes
    -----
    The DataObject owns no repository location, schema, route identity, state-space
    alignment, basis, gauge, represented operator, comparison meaning, provenance,
    convergence, validation, uncertainty, or acceptance meaning. SHA-256 establishes
    content identity only.
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
        The digest does not authenticate an author, path, calculation, route,
        compatibility relation, provenance chain, or scientific claim.
        """
        # Hash the encapsulated wire directly; re-encoding would silently replace exact
        # content identity with serializer-dependent canonicalization.
        return hashlib.sha256(self.payload).hexdigest()
