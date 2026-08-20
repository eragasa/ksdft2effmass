r"""Software verification of retained QEXSD extraction artifact.

Evidence profile: claim_bearing

Bounded artifact scope: exact external XML through canonical retained JSON.

Facet and represented meaning

The artifact binds source identity, raw preservation, semantic translation, and
wire bytes.

Intrinsic and cross-object scope

Source nonmutation, package ownership, schema, and retained-record agreement are
covered.

VVUQ and scientific exclusions

The artifact is provenance input, not scientific validation, convergence evidence,
or UQ.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import jsonschema  # type: ignore[import-untyped]
import pytest
from qexsd_fixtures import actual_qexsd_path

from ksdft2effmass.io.quantum_espresso.qexsd import (
    ConstructQexsdKohnShamPlaneWaveRecord,
    ParseQexsdDocument,
    QexsdDocument,
    QexsdSource,
)
from ksdft2effmass.ksdft.pw import (
    KohnShamPlaneWaveCalculationRecord,
    KohnShamPlaneWaveCalculationRecordJsonSerializer,
)

pytestmark = pytest.mark.software_verification
REPOSITORY_ROOT = Path(__file__).resolve().parents[7]
SOURCE_SHA256 = "2ad68bf1f16d6fda3873f5967677a81e81f16a9f88a797701134c0e5fecdd1d9"
SOURCE_BYTES = 55068


def extract_actual() -> tuple[
    QexsdDocument, KohnShamPlaneWaveCalculationRecord, bytes, tuple[int, int]
]:
    """Return raw and semantic records with source modification times.

    Evidence ID: Helper owns no identifier.

    Requirement: Support the named tests without owning evidence.

    Method: Read the fixed path and call the public transformations.

    Oracle: Caller-owned identity constants control the support operation.

    Acceptance: Return deterministic controlled support data.

    Interpretation: Failures block the consuming evidence owners.

    Limitations: This helper makes no independent evidence or scientific claim.

    Provenance: The consuming tests state the retained artifact provenance.
    """
    path = actual_qexsd_path()
    before = path.stat()
    content = path.read_bytes()
    source = QexsdSource(
        str(path.resolve(strict=True)), SOURCE_SHA256, SOURCE_BYTES, content
    )
    document = ParseQexsdDocument().execute(source)
    record = ConstructQexsdKohnShamPlaneWaveRecord().execute(document)
    after = path.stat()
    return document, record, content, (before.st_mtime_ns, after.st_mtime_ns)


def test_artifact__actual_extraction__preserves_raw_and_constructs_semantics() -> None:
    """Evidence ID: SV-PERIODIC-018

    Requirement: Exact external bytes preserve raw values and yield explicit
    semantics.

    Method: Read only the authorized path and execute both public transformations.

    Oracle: Fixed source identity and independently listed XML observations.

    Acceptance: Identity, raw matrices, scales, units, weights, arrays, energy,
    and grids match.

    Interpretation: Failure indicates external drift or extraction-contract drift.

    Limitations: This one QEXSD artifact does not establish broader format support.

    Provenance: artifact-inventory.json data-file-schema identity.
    """
    document, record, content, mtimes = extract_actual()
    assert hashlib.sha256(content).hexdigest() == SOURCE_SHA256
    assert len(content) == SOURCE_BYTES
    assert mtimes[0] == mtimes[1]
    assert document.atomic_structure_alat == 10.2
    assert document.reciprocal_lattice_coefficients == (
        (-1.0, -1.0, 1.0),
        (1.0, 1.0, 1.0),
        (-1.0, 1.0, -1.0),
    )
    assert record.structure.direct_lattice.vectors[0] == (-5.1, 0.0, 5.1)
    assert record.structure.sites[1].coordinates == (2.55, 2.55, 2.55)
    assert record.k_point_sampling.raw_coordinates[0] == (0.125, 0.125, 0.125)
    assert sum(record.k_point_sampling.weights) == 2.0
    assert record.spectrum.band_count == 4
    assert record.total_energy.value == -7.922263630348509
    assert (
        record.plane_wave.fft_grid
        == record.plane_wave.fft_smooth
        == record.plane_wave.fft_box
        == (20, 20, 20)
    )
    assert record.exit_status == 0


def test_artifact__retained_json__matches_runtime_schema_and_round_trip() -> None:
    """Evidence ID: SV-PERIODIC-019

    Requirement: Retained JSON equals canonical runtime bytes and validates
    against v1.

    Method: Compare bytes, validate the closed schema, and deserialize/reserialize.

    Oracle: Canonical serializer rules, retained bytes, and maintained schema.

    Acceptance: Byte equality, schema success, and exact round trip all hold.

    Interpretation: Failure indicates runtime, fixture, or schema drift.

    Limitations: Wire agreement is software verification only.

    Provenance: Retained ksdft-plane-wave-calculation-record.json version 1.
    """
    _, record, _, _ = extract_actual()
    serializer = KohnShamPlaneWaveCalculationRecordJsonSerializer()
    actual = serializer.serialize(record).encode()
    root = REPOSITORY_ROOT / "calculations/bulk-silicon/qe-example01-si-scf-davidson"
    retained = (root / "ksdft-plane-wave-calculation-record.json").read_bytes()
    assert actual == retained
    schema_root = (
        REPOSITORY_ROOT / "specification/ksdft-plane-wave-calculation-record/v1"
    )
    schema = json.loads(
        (schema_root / "ksdft-plane-wave-calculation-record.schema.json").read_text()
    )
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(json.loads(retained), schema)
    assert (
        serializer.serialize(serializer.deserialize(retained.decode())).encode()
        == retained
    )


def test_public_api__package__exports_exact_defining_modules_without_old_aliases() -> (
    None
):
    """Evidence ID: SV-PERIODIC-020

    Requirement: Public classes have selected owners, and the six named old
    periodic imports are absent.

    Method: Check defining modules and the periodic package namespace.

    Oracle: Selected package architecture and relocation table.

    Acceptance: All defining modules and absent legacy names match exactly.

    Interpretation: Failure indicates ownership or compatibility-alias drift.

    Limitations: Import ownership alone establishes no scientific behavior.

    Provenance: Active Task architecture correction instruction.
    """
    import ksdft2effmass.periodic as periodic
    from ksdft2effmass.integration.quantumespresso.qexsd import (
        QexsdDocument as CanonicalQexsdDocument,
    )
    from ksdft2effmass.integration.quantumespresso.qexsd import (
        QexsdDocumentParser,
    )
    from ksdft2effmass.integration.quantumespresso.qexsd import (
        QexsdSource as CanonicalQexsdSource,
    )

    assert QexsdSource is CanonicalQexsdSource
    assert QexsdDocument is CanonicalQexsdDocument
    assert ParseQexsdDocument is QexsdDocumentParser
    assert QexsdSource.__module__ == (
        "ksdft2effmass.integration.quantumespresso.qexsd.records"
    )
    assert QexsdDocument.__module__ == (
        "ksdft2effmass.integration.quantumespresso.qexsd.records"
    )
    assert ParseQexsdDocument.__module__ == (
        "ksdft2effmass.integration.quantumespresso.qexsd.parsing"
    )
    assert QexsdDocumentParser.__name__ == "QexsdDocumentParser"
    assert (
        ConstructQexsdKohnShamPlaneWaveRecord.__module__
        == "ksdft2effmass.io.quantum_espresso.qexsd.construction"
    )
    assert (
        KohnShamPlaneWaveCalculationRecord.__module__
        == "ksdft2effmass.ksdft.pw.records"
    )
    assert (
        KohnShamPlaneWaveCalculationRecordJsonSerializer.__module__
        == "ksdft2effmass.ksdft.pw.serialization"
    )
    assert not hasattr(periodic, "QexsdSource")
    assert not hasattr(periodic, "QexsdDocument")
    assert not hasattr(periodic, "ParseQexsdDocument")
    assert not hasattr(periodic, "PeriodicCalculationRecord")
    assert not hasattr(periodic, "ConstructPeriodicCalculationRecord")
    assert not hasattr(periodic, "PeriodicCalculationRecordJsonSerializer")
