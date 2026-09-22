"""Quantum ESPRESSO binding for cataloged pseudopotential artifacts.

The adapter accepts only the project-selected native UPF2 representation and returns
an immutable reference suitable for later QE simulation composition.  Format
admission does not establish that QE has parsed the file successfully, that another
representation is numerically equivalent, or that a scientific calculation is
authorized.
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
class QuantumEspressoPseudopotentialReference:
    """Represent one cataloged UPF2 file bound to Quantum ESPRESSO composition.

    Parameters
    ----------
    source_entry_identity
        Exact backend-neutral source-library entry identity.
    content_identity
        Complete SHA-256 of the UPF2 bytes.
    filename
        Portable UPF basename used by a later QE input or staging plan.
    local_path
        Absolute content-addressed external-library path.
    """

    source_entry_identity: str
    content_identity: PseudopotentialSha256
    filename: str
    local_path: Path

    def __post_init__(self) -> None:
        """Validate the exact UPF reference representation."""
        if type(self.source_entry_identity) is not str:
            raise TypeError("source_entry_identity must be a built-in str")
        if not self.source_entry_identity:
            raise ValueError("source_entry_identity must not be empty")
        if type(self.content_identity) is not PseudopotentialSha256:
            raise TypeError("content_identity must be a PseudopotentialSha256")
        if type(self.filename) is not str:
            raise TypeError("filename must be a built-in str")
        if not self.filename.lower().endswith(".upf"):
            raise ValueError("filename must have a .upf suffix")
        if not isinstance(self.local_path, Path):
            raise TypeError("local_path must be pathlib.Path")
        if not self.local_path.is_absolute() or ".." in self.local_path.parts:
            raise ValueError("local_path must be absolute without parent traversal")


@dataclass(frozen=True, slots=True)
class QuantumEspressoPseudopotentialAdapter:
    """Bind a cataloged UPF2 artifact to Quantum ESPRESSO composition."""

    def execute(
        self, entry: PseudopotentialCatalogEntry
    ) -> QuantumEspressoPseudopotentialReference:
        """Return a QE reference for one exact UPF2 catalog entry.

        Parameters
        ----------
        entry
            Backend-neutral catalog entry whose artifact must be UPF2.

        Returns
        -------
        QuantumEspressoPseudopotentialReference
            Immutable QE-native reference retaining source and content identities.

        Raises
        ------
        TypeError
            If ``entry`` is not the exact catalog-entry type.
        ValueError
            If the artifact is not UPF2 or its filename lacks a ``.upf`` suffix.

        Notes
        -----
        The operation performs no file read or integrity check.  Verify current bytes
        with ``PseudopotentialArtifactVerifier`` before run staging.
        """
        if type(entry) is not PseudopotentialCatalogEntry:
            raise TypeError("entry must be a PseudopotentialCatalogEntry")
        if entry.artifact.format is not PseudopotentialArtifactFormat.UPF2:
            raise ValueError("Quantum ESPRESSO project bindings require UPF2")
        return QuantumEspressoPseudopotentialReference(
            source_entry_identity=entry.source_entry.identity,
            content_identity=entry.artifact.content_identity,
            filename=entry.artifact.filename,
            local_path=entry.local_path,
        )
