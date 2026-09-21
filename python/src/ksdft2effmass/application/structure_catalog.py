"""Command boundary for deriving and persisting one canonical structure entry."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from ksdft2effmass.integration.materials_project import (
    PymatgenStructureSymmetryAnalyzer,
)
from ksdft2effmass.persistence import SQLiteAtomicRevisionStore
from ksdft2effmass.structures.catalog import (
    StructureCatalogEntry,
    StructureCatalogEntrySerializer,
    StructureCatalogRepository,
    StructureCatalogRole,
    StructureCatalogWriteStatus,
)

_DEFAULT_DATABASE = (
    Path.home()
    / "projects"
    / "ksdft2effmass"
    / "structures"
    / "structure-catalog.sqlite3"
)


class StructureCatalogImportCommand:
    """Own explicit snapshot adaptation, catalog persistence, and compact output.

    The command is the application composition boundary for file paths, analyzer
    parameters, the external SQLite location, and terminal reporting.
    """

    def execute(self, arguments: tuple[str, ...] | None = None) -> int:
        """Import one exact Materials Project snapshot into the structure catalog.

        Parameters
        ----------
        arguments
            Command arguments excluding the executable name, or ``None`` to use
            ``sys.argv`` through ``argparse``.

        Returns
        -------
        int
            Zero after a committed or exact unchanged import.

        Raises
        ------
        FileExistsError
            The retained manifest path exists with different bytes.
        RuntimeError
            The domain repository returns conflict or operational failure.
        OSError
            A required file or directory operation fails.
        TypeError
            Canonical snapshot fields or analyzer parameters have wrong types.
        ValueError
            Canonical snapshot, analyzer parameters, or derived symmetry is invalid.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("snapshot", type=Path)
        parser.add_argument("manifest", type=Path)
        parser.add_argument("--database", type=Path, default=_DEFAULT_DATABASE)
        parser.add_argument("--material-id", required=True)
        parser.add_argument("--symprec-angstrom", type=float, default=0.01)
        parser.add_argument("--angle-tolerance-degree", type=float, default=5.0)
        namespace = parser.parse_args(arguments)
        snapshot_path: Path = namespace.snapshot
        snapshot = snapshot_path.read_bytes()
        source_digest = hashlib.sha256(snapshot).hexdigest()
        symmetry = PymatgenStructureSymmetryAnalyzer().execute(
            snapshot,
            symprec_angstrom=namespace.symprec_angstrom,
            angle_tolerance_degree=namespace.angle_tolerance_degree,
        )
        material_id: str = namespace.material_id
        entry = StructureCatalogEntry(
            identity=f"materials-project:{material_id}",
            role=StructureCatalogRole.EXTERNAL_REFERENCE,
            source_database="Materials Project",
            source_record_id=material_id,
            source_url=f"https://materialsproject.org/materials/{material_id}",
            source_content_id=f"sha256:{source_digest}",
            source_snapshot=snapshot,
            symmetry=symmetry,
            limitations=(
                "external reference geometry, not the production PBE-relaxed lattice",
                "symmetry classification depends on retained tolerances",
                "successful retrieval and classification do not establish "
                "scientific validation",
            ),
        )
        database_path: Path = namespace.database.expanduser().resolve()
        database_path.parent.mkdir(parents=True, exist_ok=True)
        repository = StructureCatalogRepository(
            SQLiteAtomicRevisionStore(
                database_path,
                busy_timeout_ms=5000,
                max_payload_bytes=16 * 1024 * 1024,
            )
        )
        result = repository.write(entry)
        if result.status not in {
            StructureCatalogWriteStatus.COMMITTED,
            StructureCatalogWriteStatus.UNCHANGED,
        }:
            raise RuntimeError("structure catalog write did not commit")
        manifest: Path = namespace.manifest
        payload = StructureCatalogEntrySerializer().serialize(entry)
        if manifest.exists():
            if manifest.read_bytes() != payload:
                raise FileExistsError("existing catalog manifest has different bytes")
        else:
            manifest.parent.mkdir(parents=True, exist_ok=True)
            with manifest.open("xb") as stream:
                stream.write(payload)
        print(
            f"status={result.status.value} entry={entry.identity} "
            f"revision={result.revision_identity} database={database_path}"
        )
        return 0


def main() -> int:
    """Run the framework-owned command-line entry point.

    Returns
    -------
    int
        Process exit status returned by ``StructureCatalogImportCommand``.
    """
    return StructureCatalogImportCommand().execute()


if __name__ == "__main__":
    raise SystemExit(main())
