"""Compatibility adapters for selected checksum and skill resources."""

from __future__ import annotations

from .. import (
    ArtifactIdentity,
    ChecksumEntry,
    ChecksumManifest,
    JsonRecordDeserializer,
    ResourcePath,
    SkillDescriptor,
    WireRecordKind,
)
from ._parsing import as_str, failure, parse_object, success
from .models import AdaptationResult, LocalIssue


def _invalid(area: str, path: str, exc: Exception) -> AdaptationResult:
    return failure(LocalIssue(f"PIHL.{area}.INVALID", path, str(exc)))


class ChecksumCatalogAdapter:
    """Normalize retained ``sha256sum``-style catalog bytes.

    The ActionObject represents catalog entries only. It does not read, hash,
    or verify the referenced files.
    """

    __slots__ = ()

    def execute(self, catalog_bytes: bytes) -> AdaptationResult:
        """Return a generic checksum manifest from exact catalog bytes.

        Parameters
        ----------
        catalog_bytes
            UTF-8 lines containing a digest, two spaces, and a path.

        Returns
        -------
        AdaptationResult
            A path-sorted checksum manifest on success, or deterministic local
            diagnostics for malformed text.

        Raises
        ------
        TypeError
            If ``catalog_bytes`` is not built-in ``bytes``.
        """
        if type(catalog_bytes) is not bytes:
            raise TypeError("catalog_bytes must be bytes")
        try:
            entries = []
            for line in catalog_bytes.decode("utf-8").splitlines():
                if not line:
                    continue
                digest, marker, path = line.partition("  ")
                if not marker:
                    raise ValueError("catalog line must use two-space separator")
                entries.append(
                    ChecksumEntry(1, path, ArtifactIdentity(1, "sha256", digest))
                )
            return success(
                ChecksumManifest(
                    1, tuple(sorted(entries, key=lambda value: value.path))
                )
            )
        except (UnicodeDecodeError, TypeError, ValueError) as exc:
            return _invalid("CHECKSUM", "catalog", exc)


class SkillInventoryAdapter:
    """Select canonical skills and decode generic descriptor bytes.

    The inventory supplies the accepted skill identities; descriptor decoding
    remains owned by the generic wire deserializer. This ActionObject performs
    no filesystem discovery or skill activation.
    """

    __slots__ = ()

    def execute(
        self,
        inventory_bytes: bytes,
        descriptor_bytes: tuple[tuple[ResourcePath, bytes], ...],
    ) -> AdaptationResult:
        """Return descriptors whose IDs match the explicit inventory.

        Parameters
        ----------
        inventory_bytes
            Exact project-local skill-inventory JSON bytes.
        descriptor_bytes
            Explicit ``(resource_path, descriptor_JSON_bytes)`` pairs.

        Returns
        -------
        AdaptationResult
            A skill-identity-sorted descriptor tuple on success, or
            deterministic local diagnostics for mismatch or malformed input.
        """
        inventory, issue = parse_object(inventory_bytes, "skill inventory")
        if issue is not None:
            return failure(issue)
        assert inventory is not None
        try:
            skills = inventory["skills"]
            names = {as_str(item["skill_name"], "skill_name") for item in skills}
            descriptors = []
            for path, payload in descriptor_bytes:
                decoded = JsonRecordDeserializer().execute(
                    WireRecordKind.SkillDescriptor, payload
                )
                if type(decoded.record) is not SkillDescriptor:
                    raise ValueError(f"invalid descriptor {path}")
                if decoded.record.skill_id not in names:
                    raise ValueError(f"descriptor {path} is absent from inventory")
                descriptors.append(decoded.record)
            descriptor_ids = [value.skill_id for value in descriptors]
            if not descriptor_ids or len(descriptor_ids) != len(set(descriptor_ids)):
                raise ValueError("descriptor selection must be nonempty and unique")
        except (KeyError, TypeError, ValueError) as exc:
            return _invalid("SKILL", "skill inventory", exc)
        return success(tuple(sorted(descriptors, key=lambda value: value.skill_id)))
