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

Stable ``SV-PROV`` identifiers declared by the maintained modules cover the
surface under
``python/tests/software_verification/ksdft2effmass/provenance`` and the
artifact/boundary modules under
``python/tests/software_verification/ksdft2effmass/integration``.  For the
external-tool decomposition specifically, the durable tools-decomposition
boundary inventory recorded 13 class-owned software-verification modules, 85
test functions with 85 unique evidence owners, and 145 collected cases.  Of
those boundary nodes, 24 were one-to-one mappings of historical nodes and 121
were genuinely new.  Ordered P2 audit items maintain their own current
inventories, so test functions, evidence owners, and collection counts evolve
as bounded evidence corrections are cleared.  These quantities are different,
and the boundary counts do not describe the entire P2 verification tree.

The actions correction separately assigns class-owned modules to the two
statuses, the issue enum, the two results, and the two stateless actions.  The
evidence checks:

* artifact identity, specification, reference, location, manifest, provenance,
  and directed lineage construction and owner-local invariants, including real
  UTC calendar dates, timestamp ordering, and direct manifest self-dependency
  rejection;
* tool identity/specification, declared capability, installation observation,
  capability verification, immutable request, completed result, and structured
  failure distinctions, with explicit attempt and optional retry-parent IDs;
* exact comparison of caller-supplied digest/u64 observations and
  three-identity request/result-or-failure correlation, including derived
  non-wire statuses, all mismatch subsets, and exact request, correlation, then
  attempt issue order;
* every public export, ``StrEnum`` vocabulary, and ``ProvenanceJsonError``
  taxonomy;
* strict runtime/schema/fixture agreement, including duplicate/unknown-key, BOM,
  malformed Unicode/JSON, floating/non-finite number, Boolean/numeric-string u64,
  path, ordering, and overflow rejection;
* production import direction: the declaration, observation, and execution
  record modules do not depend on actions or serialization, while actions and
  serialization import only the exact record/result families they consume;
* absence of harness, CPN, SNAKES, backend, scheduler, subprocess-client, or
  mutable-client dependencies; and
* installed-wheel availability of the package and version-1 specification.

The schema is
``specification/provenance/v1/provenance-v1.schema.json``.  Its valid fixture
set has one golden record for every serializer-supported record/result shape;
invalid fixtures exercise strict-parser and represented-invariant failures.
Canonical output is compact sorted-key UTF-8 JSON followed by one line feed.
The schema owns exact wire members, required/null forms, primitive types, enum
values, patterns, numeric bounds, unique arrays, and declared conditional
shapes.  The strict parser additionally owns duplicate-key, BOM, malformed JSON,
and floating lexical-form rejection.  Each decomposed public record or result owns its intrinsic validation directly
in its own ``__post_init__``, without shared or private validator helpers; each
stateless action owns validation of its direct ``execute`` inputs.  Python constructors own intrinsic
and record-local relational checks that the schema does not claim to complete,
including NFC, deterministic lexical ordering, actual calendar dates, timestamp
ordering, direct non-self manifest/provenance/lineage/retry relations,
location-alternative consistency, and status derivation.  Cross-record existence
and graph-wide cycle detection remain separate repository or workflow concerns.
Boundary evidence constructs records after schema checks rather than treating
schema acceptance alone as full runtime relational validity.

Interpretation and limitations
------------------------------

The supported public import remains exactly ``ksdft2effmass.provenance``.  The
internal modules ``external_tools``, ``tool_observations``, and
``external_execution`` are not promised direct-import paths.  The removed
``tools.py`` had no supported module-path contract.  The internal
``ExternalExecutionOutcome`` alias adds no stored wrapper and is not a
package-level public export.  This decomposition does not change the accepted
public object set, version-1 serialization, schema, or fixture meaning.

A passing structural evidence validator establishes conformance to its checked
module shape, ownership metadata, naming, and inventory relations.  It does not
establish oracle independence, semantic completeness, runtime behavior,
acyclicity beyond its explicit import checks, mathematical or scientific
correctness, numerical verification, scientific validation, uncertainty
quantification, or human acceptance.  Passing focused tests establishes their
software-verification assertions only.

A passing identity comparison establishes exact agreement of represented digest
and byte-size values supplied after observation elsewhere.  It does not
establish that the action observed a file or computed the digest.  A passing
correlation comparison establishes request, correlation, and attempt identity
agreement only.  The status is derived from issue-tuple emptiness and is not
stored or serialized.  A matching structured failure is therefore correlated,
while a completed result with any join mismatch is not.  Completion and
identity correlation remain separate claims.  Retry-parent lineage and separate
authorization remain outside that derived status.
``VerificationStatus.VERIFIED`` establishes only the represented
software-capability observation.  ``COMPLETED`` establishes only completion at
the external boundary.  ``RunManifest.output_artifact_ids`` are preallocated
expected identities and may therefore be nonempty in ``DECLARED``; they do not
establish that output bytes were observed.

No test invokes QE, Wannier90, a scheduler, a network, or a filesystem-backed
artifact resolver.  Tests use synthetic records and fixtures.  They do not
establish file observation, format validity, provenance truth, external-execution
validity, executable correctness, SCF convergence, parser/scientific adapter
correctness, numerical acceptance or accuracy, physical correctness,
scientific validation, uncertainty quantification, Rust conformance,
authorization, or human acceptance.
Future concrete QE/Wannier adapters and their separately classified evidence
remain owned by later tasks; this contract is not a plugin framework.

The API intentionally has no generic raw argument, environment-value,
verification-detail, or failure-message channel.  Credentials and live handles
remain categorically prohibited.  Tests verify the closed field inventory and
lexical invariants; they cannot prove that an opaque identifier, version, path,
or separately referenced record is semantically secret-free.  Callers remain
responsible for never encoding credentials, tokens, private keys, or other
secrets in those values.
