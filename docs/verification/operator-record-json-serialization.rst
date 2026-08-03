Operator-record JSON serialization evidence
===========================================

Scope and contract
------------------

``OperatorRecordJsonSerializer`` is the sole ActionObject for the public
operator-record JSON text format. Version 1 uses deterministic sorted compact
JSON, nine fixed top-level fields (the schema version plus all eight
``OperatorRecord`` fields), and row-major complex entries encoded as
``[real, imaginary]`` finite-number pairs. ``deserialize()`` accepts only Python
``str`` input and reapplies serializer wire rules and public DataObject
invariants. No ``OperatorRecordJsonCodec``, ``encode()``, or ``decode()`` alias is
supported.

Executable evidence
-------------------

Runtime serializer behavior is separated into five software-verification facets:

* ``SV-ORJS-001`` through ``SV-ORJS-003`` cover the public contract;
* ``SV-ORJS-004`` through ``SV-ORJS-006`` cover deterministic encoding;
* ``SV-ORJS-007`` through ``SV-ORJS-011`` cover JSON and object structure;
* ``SV-ORJS-012`` through ``SV-ORJS-016`` cover scalar semantics, finite-number
  taxonomy, and DataObject invariant propagation;
* ``SV-ORJS-017`` through ``SV-ORJS-018`` cover exact deterministic round trips,
  including empty provenance, non-Hermitian matrices, extreme finite complex
  values, defensive ownership, and operational immutability.

The public schema has distinct integration ownership. ``SV-ORJSC-001`` validates
the draft-2020-12 schema itself, ``SV-ORJSC-002`` validates serializer output and
valid fixtures, and ``SV-ORJSC-003`` checks every invalid class expressible by the
schema. Cross-field dimension agreement, general matrix squareness/raggedness,
cell linear independence, and parser-level finite-number handling remain runtime
rules because the current JSON Schema does not express them completely.

Golden-fixture integration is separately owned by ``SV-ORJF-001`` through
``SV-ORJF-003``. These tests enumerate every ``valid/*.json`` and
``invalid/*.json`` artifact, require deterministic serializer round trips for the
valid corpus, and require the exact documented Python exception category for
every invalid artifact. Fixture tests do not duplicate detailed serializer or
DataObject assertions.

Interpretation and exclusions
-----------------------------

A pass establishes conformance of the tested Python implementation, public JSON
Schema, and golden artifacts to the approved version-1 software contract. A
failure may indicate implementation, schema, fixture, documentation, dependency,
or evidence drift and must be investigated rather than accepted by changing an
expected value. ``jsonschema`` is used as an established independent validator;
these tests do not validate that dependency itself.

The matrices and metadata are synthetic. This evidence performs no basis or
gauge alignment, unit conversion, physical interpretation, scientific
validation, or uncertainty quantification. It prepares a language-neutral wire
contract but provides no Rust implementation or Python/Rust conformance evidence.
