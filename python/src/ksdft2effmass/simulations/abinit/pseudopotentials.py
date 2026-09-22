"""ABINIT binding for cataloged pseudopotential artifacts.

The adapter accepts only the project-selected native PSP8 representation and returns
an immutable reference suitable for later ABINIT simulation composition.  Although
ABINIT can read some norm-conserving UPF files, this boundary deliberately requires
the matched PseudoDojo PSP8 representation selected by the project decision.
Format admission does not establish successful calculator parsing, cross-format
numerical equivalence, or execution authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.simulations.dft import (
    PseudopotentialArtifactFormat,
    PseudopotentialCatalogEntry,
    PseudopotentialSha256,
)


@dataclass(frozen=True, slots=True)
class AbinitPseudopotentialReference:
    """Represent one cataloged PSP8 file bound to ABINIT composition.

    Parameters
    ----------
    source_entry_identity
        Exact backend-neutral source-library entry identity.
    content_identity
        Complete SHA-256 of the PSP8 bytes.
    filename
        Portable PSP8 basename used by a later ABINIT input or staging plan.
    local_path
        Absolute content-addressed external-library path.
    """

    source_entry_identity: str
    content_identity: PseudopotentialSha256
    filename: str
    local_path: Path

    def __post_init__(self) -> None:
        """Validate the exact PSP8 reference representation."""
        if type(self.source_entry_identity) is not str:
            raise TypeError("source_entry_identity must be a built-in str")
        if not self.source_entry_identity:
            raise ValueError("source_entry_identity must not be empty")
        if type(self.content_identity) is not PseudopotentialSha256:
            raise TypeError("content_identity must be a PseudopotentialSha256")
        if type(self.filename) is not str:
            raise TypeError("filename must be a built-in str")
        if not self.filename.lower().endswith(".psp8"):
            raise ValueError("filename must have a .psp8 suffix")
        if not isinstance(self.local_path, Path):
            raise TypeError("local_path must be pathlib.Path")
        if not self.local_path.is_absolute() or ".." in self.local_path.parts:
            raise ValueError("local_path must be absolute without parent traversal")


@dataclass(frozen=True, slots=True)
class AbinitPseudopotentialAdapter:
    """Bind a cataloged PSP8 artifact to ABINIT simulation composition."""

    def execute(
        self, entry: PseudopotentialCatalogEntry
    ) -> AbinitPseudopotentialReference:
        """Return an ABINIT reference for one exact PSP8 catalog entry.

        Parameters
        ----------
        entry
            Backend-neutral catalog entry whose artifact must be PSP8.

        Returns
        -------
        AbinitPseudopotentialReference
            Immutable ABINIT-native reference retaining source and content identities.

        Raises
        ------
        TypeError
            If ``entry`` is not the exact catalog-entry type.
        ValueError
            If the artifact is not PSP8 or its filename lacks a ``.psp8`` suffix.

        Notes
        -----
        The operation performs no file read or integrity check.  Verify current bytes
        with ``PseudopotentialArtifactVerifier`` before run staging.
        """
        if type(entry) is not PseudopotentialCatalogEntry:
            raise TypeError("entry must be a PseudopotentialCatalogEntry")
        if entry.artifact.format is not PseudopotentialArtifactFormat.PSP8:
            raise ValueError("ABINIT project bindings require PSP8")
        return AbinitPseudopotentialReference(
            source_entry_identity=entry.source_entry.identity,
            content_identity=entry.artifact.content_identity,
            filename=entry.artifact.filename,
            local_path=entry.local_path,
        )
