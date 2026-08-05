Provenance contract software verification
=========================================

Evidence classification
-----------------------

P2 evidence is software verification of immutable Python records, stateless
actions, structured errors, strict JSON, the version-1 schema and fixtures,
public imports, dependency direction, and wheel contents.  It is not numerical
verification, scientific validation, uncertainty quantification, external-tool
execution evidence, or acceptance of a scientific calculation.  Those other
VVUQ classes are not applicable to this nonnumerical contract and no claim is
made for them.

Maintained evidence
-------------------

Stable identifiers ``SV-PROV-001`` through ``SV-PROV-075`` cover the maintained
surface under
``python/tests/software_verification/ksdft2effmass/provenance`` and the five
artifact/boundary modules under
``python/tests/software_verification/ksdft2effmass/integration``.  The evidence
checks:

* artifact identity, specification, reference, location, manifest, provenance,
  and directed lineage construction and owner-local invariants, including real
  UTC calendar dates, timestamp ordering, and direct manifest self-dependency
  rejection;
* tool identity/specification, declared capability, installation observation,
  capability verification, immutable request, completed result, and structured
  failure distinctions, with explicit attempt and optional retry-parent IDs;
* exact digest/u64 verification and three-identity
  request/result-or-failure correlation, including derived non-wire statuses;
* every public export, ``StrEnum`` vocabulary, and ``ProvenanceJsonError``
  taxonomy;
* strict runtime/schema/fixture agreement, including duplicate/unknown-key, BOM,
  malformed Unicode/JSON, floating/non-finite number, Boolean/numeric-string u64,
  path, ordering, and overflow rejection;
* production import direction and absence of harness, CPN, SNAKES, backend,
  scheduler, subprocess-client, or mutable-client dependencies; and
* installed-wheel availability of the package and version-1 specification.

The schema is
``specification/provenance/v1/provenance-v1.schema.json``.  Its valid fixture
set has one golden record for every serializer-supported record/result shape;
invalid fixtures exercise strict-parser and represented-invariant failures.
Canonical output is compact sorted-key UTF-8 JSON followed by one line feed.
The schema owns exact wire members, required/null forms, primitive types, enum
values, patterns, numeric bounds, unique arrays, and declared conditional
shapes.  The strict parser additionally owns duplicate-key, BOM, malformed JSON,
and floating lexical-form rejection.  Each public record owns its intrinsic constructor validation directly, without
shared callable field validators.  Python constructors own intrinsic and
record-local relational checks that the schema does not claim to complete,
including NFC, deterministic lexical ordering, actual calendar dates, timestamp
ordering, direct non-self manifest/provenance/lineage/retry relations,
location-alternative consistency, and status derivation.  Cross-record existence
and graph-wide cycle detection remain separate repository or workflow concerns.
Boundary evidence constructs records after schema checks rather than treating
schema acceptance alone as full runtime relational validity.

Interpretation and limitations
------------------------------

A passing identity comparison establishes exact represented digest and byte-size
agreement, not format validity, provenance truth, local availability, or
scientific meaning.  A passing correlation comparison establishes request,
correlation, and attempt identity agreement only.  Retry-parent lineage and
separate authorization remain outside that derived status.
``VerificationStatus.VERIFIED`` establishes only the represented
software-capability observation.  ``COMPLETED`` establishes only completion at
the external boundary.  ``RunManifest.output_artifact_ids`` are preallocated
expected identities and may therefore be nonempty in ``DECLARED``; they do not
establish that output bytes were observed.

No test invokes QE, Wannier90, a scheduler, a network, or a filesystem-backed
artifact resolver.  Tests use synthetic records and fixtures.  They do not
establish executable correctness, SCF convergence, parser/scientific adapter
correctness, numerical accuracy, physical-model validity, scientific validation,
uncertainty propagation, Rust conformance, authorization, or human acceptance.
Future concrete QE/Wannier adapters and their separately classified evidence
remain owned by later tasks; this contract is not a plugin framework.

The API intentionally has no generic raw argument, environment-value,
verification-detail, or failure-message channel.  Credentials and live handles
remain categorically prohibited.  Tests verify the closed field inventory and
lexical invariants; they cannot prove that an opaque identifier, version, path,
or separately referenced record is semantically secret-free.  Callers remain
responsible for never encoding credentials, tokens, private keys, or other
secrets in those values.
