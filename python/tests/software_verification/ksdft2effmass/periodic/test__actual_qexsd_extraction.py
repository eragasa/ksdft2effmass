r"""Software verification of actual QEXSD extraction.

Evidence profile: claim_bearing

Bounded artifact scope: exact accepted external XML and retained canonical JSON
identity.

Facet and represented meaning

This integration evidence binds explicit source bytes through both transformations to
JSON.

Intrinsic and cross-object scope

Source identity, deterministic extraction, schema, imports, and nonmutation are covered.

VVUQ and scientific exclusions

The accepted external artifact is trusted provenance input, not a numerical-
verification,
scientific-validation, convergence-sufficiency, UQ, or production-suitability oracle.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import jsonschema  # type: ignore[import-untyped]
import pytest
from qexsd_fixtures import actual_qexsd_path

from ksdft2effmass.periodic import (
    ConstructPeriodicCalculationRecord,
    ParseQexsdDocument,
    PeriodicCalculationRecord,
    PeriodicCalculationRecordJsonSerializer,
    QexsdDocument,
    QexsdSource,
)

pytestmark = pytest.mark.software_verification

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
SOURCE_SHA256 = "2ad68bf1f16d6fda3873f5967677a81e81f16a9f88a797701134c0e5fecdd1d9"
SOURCE_BYTES = 55068
RECORD_SHA256 = "d88a1d562155f7e89fe7903fffe57b475355f00c187611e0ebc341f33a7a4605"
RECORD_BYTES = 3036


def extract_actual() -> tuple[PeriodicCalculationRecord, bytes, tuple[int, int]]:
    """Read the explicit source and execute both transformations.

    Evidence ID: Helper owns no identifier.

    Requirement: Support the named tests without owning evidence.

    Method: Read the one explicit external path and call public transformations.

    Oracle: Caller-supplied path and identity constants define the support operation.

    Acceptance: Return deterministic controlled support data.

    Interpretation: Failure blocks the evidence owners that consume this helper.

    Limitations: This helper makes no independent evidence or scientific claim.
    """
    path = actual_qexsd_path()
    before = path.stat()
    content = path.read_bytes()
    source = QexsdSource(
        str(path.resolve(strict=True)), SOURCE_SHA256, SOURCE_BYTES, content
    )
    document = ParseQexsdDocument().execute(source)
    record = ConstructPeriodicCalculationRecord().execute(document)
    after = path.stat()
    return record, content, (before.st_mtime_ns, after.st_mtime_ns)


def test_artifact__actual_extraction__is_deterministic() -> None:
    """Evidence ID: SV-PERIODIC-018

    Requirement: The accepted exact XML deterministically yields observed dimensions
    and values.

    Method: Open only the inventory-selected path read-only, verify identity in
    QexsdSource,
    and independently execute parsing and semantic construction twice.

    Oracle: The accepted inventory fixes source identity; XML values independently
    fix the
    expected ordered observations listed in this test.

    Acceptance: Both records are equal; source hash/count, counts, shapes, units,
    energy,
    grids, weight sum, and status exactly match the declared observations.

    Interpretation: Failure indicates source drift, parser/semantic drift, or stale
    observations.

    Limitations: This one QE 7.2 QEXSD configuration is not exhaustive format
    support and
    establishes no convergence, numerical verification, scientific validation, or UQ.

    Provenance: artifact-inventory.json metadata.data-file-schema at SHA-256
    2ad68bf1f16d6fda3873f5967677a81e81f16a9f88a797701134c0e5fecdd1d9.
    """
    first, source_bytes, mtimes = extract_actual()
    second, second_bytes, second_mtimes = extract_actual()
    assert first == second
    assert source_bytes == second_bytes
    assert hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256
    assert len(source_bytes) == SOURCE_BYTES
    assert mtimes[0] == mtimes[1] == second_mtimes[0] == second_mtimes[1]
    assert (len(first.species), first.atom_count, first.k_point_count) == (1, 2, 10)
    assert (
        len(first.direct_lattice_vectors),
        len(first.direct_lattice_vectors[0]),
    ) == (3, 3)
    assert (
        len(first.reciprocal_lattice_vectors),
        len(first.reciprocal_lattice_vectors[0]),
    ) == (3, 3)
    assert (len(first.eigenvalues), len(first.eigenvalues[0])) == (10, 4)
    assert first.occupations is not None
    assert (len(first.occupations), len(first.occupations[0])) == (10, 4)
    assert sum(first.k_point_weights) == 2.0
    assert first.total_energy == -7.922263630348509
    assert first.total_energy_unit == "Hartree atomic units"
    assert first.fft_grid == first.fft_smooth == first.fft_box == (20, 20, 20)
    assert first.exit_status == 0


def test_artifact__retained_json__matches_runtime_schema_and_exact_identity() -> None:
    """Evidence ID: SV-PERIODIC-019

    Requirement: Retained JSON is exact canonical output, schema-valid, and round-
    trippable.

    Method: Compare runtime canonical bytes with the retained fixture and validate
    decoded JSON
    against the maintained Draft 2020-12 closed schema.

    Oracle: Serializer canonical rules, the retained identity contract, and the
    public schema
    independently fix the accepted result.

    Acceptance: Bytes and SHA-256 match, schema validation passes, and round trip is
    exact.

    Interpretation: Failure indicates retained/runtime/schema drift or source
    identity drift.

    Limitations: Wire agreement is software verification only; no physical claim
    follows.

    Provenance: Retained repository fixture periodic-calculation-record.json schema
    version 1.
    """
    record, _, _ = extract_actual()
    serializer = PeriodicCalculationRecordJsonSerializer()
    actual = serializer.serialize(record).encode("utf-8")
    calculation_root = (
        REPOSITORY_ROOT / "calculations/bulk-silicon/qe-example01-si-scf-davidson"
    )
    retained = (calculation_root / "periodic-calculation-record.json").read_bytes()
    assert actual == retained
    assert len(retained) == RECORD_BYTES
    assert hashlib.sha256(retained).hexdigest() == RECORD_SHA256
    schema_root = REPOSITORY_ROOT / "specification/periodic-calculation-record/v1"
    schema = json.loads(
        (schema_root / "periodic-calculation-record.schema.json").read_text(
            encoding="utf-8"
        )
    )
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(json.loads(retained), schema)
    assert (
        serializer.serialize(serializer.deserialize(retained.decode("utf-8"))).encode()
        == retained
    )


def test_public_api__package__exports_stable_defining_modules() -> None:
    """Evidence ID: SV-PERIODIC-020

    Requirement: Public extraction classes have stable package imports and defining
    modules.

    Method: Inspect public class module identities without private imports or
    filesystem discovery.

    Oracle: The implemented public package contract fixes each defining owner.

    Acceptance: Each class reports its documented defining module exactly.

    Interpretation: Failure indicates accidental redefinition or public import drift.

    Limitations: Import identity does not establish execution, numerical, or
    scientific behavior.
    """
    assert QexsdSource.__module__ == "ksdft2effmass.periodic.records"
    assert QexsdDocument.__module__ == "ksdft2effmass.periodic.records"
    assert ParseQexsdDocument.__module__ == "ksdft2effmass.periodic.qexsd"
    assert PeriodicCalculationRecord.__module__ == "ksdft2effmass.periodic.records"
    assert (
        ConstructPeriodicCalculationRecord.__module__
        == "ksdft2effmass.periodic.construction"
    )
    assert (
        PeriodicCalculationRecordJsonSerializer.__module__
        == "ksdft2effmass.periodic.serialization"
    )
