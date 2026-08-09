Project-local HarnessTask contract
==================================

``HarnessTask`` is the project-local schema-version-2 representation of one
operational Task.  JSON Task records are operational authority.  Human intake and
rendered documentation are maintained, non-executable views: they cannot activate
work, select successors, establish completion, or provide human acceptance.

This API is implementation infrastructure.  Its tests provide software
verification only; they do not validate scientific results.  The Stage-2A
representative data are synthetic and are not a migration packet.  Its
``HarnessTask`` is supplied manually: the example demonstrates serialization,
rendering, and byte comparison, not Markdown-to-JSON extraction.

Object ownership
----------------

.. list-table:: Immutable data and result objects
   :header-rows: 1

   * - Object
     - Owned state and boundary
   * - ``HarnessTask``
     - The sole serialized version-2 record and its 16 intrinsic fields.
   * - ``HarnessTaskDocumentSource``
     - Exact source bytes, revision, Git object, byte count, and identity.
   * - ``HarnessTaskSourceMapping``
     - One exact half-open source span and proposed disposition.
   * - ``HarnessTaskDocumentationContent``
     - Ordered opaque documentation-owned byte blocks.
   * - ``HarnessTaskProjectionProfile``
     - Sole authoritative template bytes, identity, and final-LF policy.
   * - ``HarnessTaskDocumentation``
     - Complete rendered bytes and identity.
   * - ``HarnessTaskDocumentationComparisonResult``
     - Exact byte differences, coverage, findings, and limitations.
   * - ``HarnessTaskMigrationReviewPacketRequest``
     - Every explicit runtime input required for packet preparation.
   * - ``HarnessTaskMigrationReviewPacket``
     - One validated exact request bundle.
   * - ``HarnessTaskMigrationReviewDocument``
     - Runtime-only exact UTF-8 human-review Markdown bytes, derived path, and identity.
   * - ``HarnessTaskMigrationFileDisposition``
     - Exact packet, generic human decision, and migration-specific outcome.

.. list-table:: Stateless actions
   :header-rows: 1

   * - ActionObject
     - Responsibility
   * - ``HarnessTaskSerializer``
     - Emit canonical JSON bytes for ``HarnessTask`` only.
   * - ``HarnessTaskDeserializer``
     - Strictly decode explicit version-2 JSON bytes.
   * - ``HarnessTaskGraphValidator``
     - Validate one complete explicitly supplied structural Task graph.
   * - ``HarnessTaskDocumentationRenderer``
     - Parse an explicit template once and substitute Task text and opaque blocks.
   * - ``HarnessTaskDocumentationComparator``
     - Report exact byte differences, mapping coverage, and block preservation.
   * - ``HarnessTaskMigrationReviewPacketPreparer``
     - Validate all cross-object agreement and return an immutable packet.
   * - ``HarnessTaskMigrationReviewPacketRenderer``
     - Render a validated packet as a deterministic complete before/after Markdown view.
   * - ``HarnessTaskMigrationFileDispositionRecorder``
     - Validate exact packet binding and the closed disposition table.

Serialized and runtime-only state
---------------------------------

Only ``HarnessTask`` is a new wire record.  It is not added to the generic
``WireRecordKind`` family.  Source, mapping, documentation, profile, comparison,
packet, and disposition objects are runtime-only.  Version-1 project JSON Task
records and Markdown Task adaptation remain supported by ``TaskRecordAdapter``;
version-2 dispatch adds no chain authority and preserves ``TaskStateInspector``
selection behavior.

Canonical Task JSON has the 16 fields in constructor order, UTF-8 without a BOM,
two-space indentation, literal Unicode, arrays for tuples, ``null`` for optional
absence, no trailing spaces, and exactly one final LF.  Deserialization may accept
noncanonical whitespace and key order but rejects duplicate, missing, and unknown
keys and all invalid intrinsic values.

Validation ownership
--------------------

Constructors own exact semantic types and intrinsic lexical, ordering, uniqueness,
identity, and cross-field invariants.  They do not check repository existence,
activation authority, lifecycle meaning, graph existence, documentation agreement,
completion, or human acceptance.

``HarnessTaskGraphValidator`` returns ``LocalValidationResult``.  Stage-2A fixes
issue precedence as lexical ``(code, path-or-empty, detail)`` order and defines:

.. list-table:: Structural graph codes
   :header-rows: 1

   * - Code
     - Meaning
   * - ``PIHL.TASK.DUPLICATE_ID``
     - More than one supplied Task has the same identity.
   * - ``PIHL.TASK.PARENT_MISSING``
     - A represented parent is absent from the complete supplied graph.
   * - ``PIHL.TASK.PARENT_CYCLE``
     - Parent relations contain a cycle.
   * - ``PIHL.TASK.PREREQUISITE_MISSING``
     - A Task prerequisite is absent from the supplied graph.
   * - ``PIHL.TASK.PREREQUISITE_CYCLE``
     - Task-prerequisite relations contain a cycle.
   * - ``PIHL.TASK.INTAKE_PATH_DUPLICATE``
     - Two Tasks bind the same intake path.
   * - ``PIHL.TASK.DOCUMENTATION_PATH_DUPLICATE``
     - Two Tasks bind the same maintained documentation path.

Template and comparison rules
-----------------------------

``HarnessTaskProjectionProfile.template_bytes`` is the sole authoritative template
representation.  The maintained JSON resource stores one base64 encoding of those
bytes plus their SHA-256 identity; decoding creates no second editable template.
The renderer accepts only these token forms:

* ``{{task.FIELD}}`` for an exact public ``HarnessTask`` field; and
* ``{{content.MAPPING_ID}}`` for one opaque documentation block.

Every supplied content mapping must occur exactly once.  The template must be UTF-8,
but content blocks remain arbitrary bytes and are never decoded or reparsed.  Tuple
Task values render as Markdown bullets, Booleans as lowercase JSON text, optional
absence as ``None``, and scalar text exactly.  The renderer rejects unknown,
unsupported, unclosed, duplicate, or missing tokens and enforces the explicit
one-final-LF or no-final-LF policy without rewriting inserted opaque bytes.

The comparator applies byte-level ``SequenceMatcher`` opcodes in source order,
verifies ordered nonoverlapping mapping coverage and exact span identities, and
requires documentation-owned blocks to occur unchanged in source order.  Its
statuses are ``EXACT``, ``MAPPED_DIFFERENCES``, and ``UNMAPPED_DIFFERENCES``.
Zero-width rendered insertions are mechanically mapped when source mapping is
complete.  Coverage gaps and missing or changed documentation blocks are unmapped.
A mapped result is structural evidence only: it does not establish semantic
correctness or human acceptance.

File-specific human mediation
-----------------------------

Packet preparation recomputes canonical JSON, rendering, comparison, complete mapping
coverage, exact block selection, and generic packet canonicality.  The target must use
the candidate-derived review ID and subject, ``software_verification`` evidence class,
the exact accepted HarnessTask and migration-review contract references, the source
revision, and exactly the source and candidate-documentation paths.  The generic
packet must contain exact immutable observations binding source path, revision,
explicit Git-object value or absence, byte count and identity; candidate-JSON
identity; mappings and unmapped spans; rendered identity; comparison status and
differences; opaque-block preservation; and applicable limitations.  Missing,
altered, stale, empty, or unrelated material fails preparation.

The project-local public surface contains 21 HarnessTask interfaces: the accepted 19
plus the narrow ``HarnessTaskMigrationReviewDocument`` and
``HarnessTaskMigrationReviewPacketRenderer`` correction.  The renderer first
revalidates the packet, then emits complete original Markdown, canonical candidate
JSON, candidate maintained Markdown, mapping table, exact differences and unified
diff, opaque-block result, rollback identity, limitations, and exactly four choices.
It strictly decodes UTF-8, chooses a backtick fence longer than every enclosed
backtick run, and emits exactly one final LF.  Its document is a non-authoritative
runtime view.

The disposition recorder revalidates both the packet and the generic decision through
their public ActionObjects before requiring exact binding and applying this closed
table:

.. list-table:: Generic and migration dispositions
   :header-rows: 1

   * - Generic human-review disposition
     - Migration disposition
   * - ``accepted``
     - ``ACCEPT_FILE_MIGRATION``
   * - ``bounded_correction``
     - ``REVISE_CONTRACT_OR_MAPPING``
   * - ``rejected``
     - ``RETAIN_DOCUMENTATION_OWNERSHIP``
   * - ``deferred``
     - ``DEFER_FILE``

Neither packet preparation nor recording authenticates authority, interprets natural
language, mutates a file, activates Stage 2B, or selects another Task.

API reference
-------------

.. currentmodule:: ksdft2effmass.harness.pi.local

.. autoclass:: HarnessTask
.. autoclass:: HarnessTaskSerializer
   :members:
.. autoclass:: HarnessTaskDeserializer
   :members:
.. autoclass:: HarnessTaskGraphValidator
   :members:
.. autoclass:: HarnessTaskDocumentSource
.. autoclass:: HarnessTaskSourceDisposition
   :members:
.. autoclass:: HarnessTaskSourceMapping
.. autoclass:: HarnessTaskDocumentationContent
.. autoclass:: HarnessTaskProjectionProfile
.. autoclass:: HarnessTaskDocumentation
.. autoclass:: HarnessTaskDocumentationRenderer
   :members:
.. autoclass:: HarnessTaskDocumentationComparator
   :members:
.. autoclass:: HarnessTaskDocumentationComparisonResult
.. autoclass:: HarnessTaskMigrationReviewPacketRequest
.. autoclass:: HarnessTaskMigrationReviewPacketPreparer
   :members:
.. autoclass:: HarnessTaskMigrationReviewPacket
.. autoclass:: HarnessTaskMigrationReviewDocument
.. autoclass:: HarnessTaskMigrationReviewPacketRenderer
   :members:
.. autoclass:: HarnessTaskMigrationDisposition
   :members:
.. autoclass:: HarnessTaskMigrationFileDisposition
.. autoclass:: HarnessTaskMigrationFileDispositionRecorder
   :members:
