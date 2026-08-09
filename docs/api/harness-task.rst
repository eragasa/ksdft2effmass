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

Operational migration-review commands
-------------------------------------

The project-local ``mediate-harness-task-migration`` skill owns authorization
routing, complete-document presentation, and the mandatory human stop.  Two thin
commands own only explicit filesystem observation, translation into the immutable
objects above, atomic immutable output creation or byte-identical recovery, and
canonical structured standard output.
The accepted ActionObjects remain authoritative for validation, serialization,
rendering, comparison, packet preparation, generic decision recording, and
migration-disposition compatibility.

Preparation uses only root-relative explicit paths beneath one resolved absolute
repository root::

   python/.venv/bin/python -m \
     ksdft2effmass.harness.pi.local.prepare_harness_task_migration_review \
     --repository-root /absolute/repository \
     --source-markdown synthetic/source.md \
     --source-revision 0123456789abcdef0123456789abcdef01234567 \
     --git-object 89abcdef0123456789abcdef0123456789abcdef \
     --candidate-task-json synthetic/candidate.json \
     --source-mapping-record synthetic/mapping.json \
     --projection-profile synthetic/profile.json \
     --output-review-document synthetic/review.md

Use ``--git-object-absent`` instead of ``--git-object`` only when absence is the
explicit source fact.  The version-1 mapping record is one closed JSON object with
``source_path``, ``source_revision``, ``git_object``, ``source_sha256``,
``byte_count``, ``documentation_path``, and ``mappings``.  Each mapping supplies the
existing ``HarnessTaskSourceMapping`` fields, representing identities as
``span_sha256`` and using the complete record's source identity.  The projection
profile uses the maintained version-1 base64 template representation documented
above.  Inputs must be regular nonsymlink files; traversal, ambient discovery, CWD
fallback, Git discovery, and source selection are rejected. An absent review output is
atomically created without replacement. An existing confined nonsymlink regular file
is accepted only when its bytes equal the reconstructed document; it is not rewritten
or otherwise mutated. A differing file is a deterministic conflict. The canonical
receipt uses stable ``result: available`` output, so creation and byte-identical recovery
produce byte-identical standard output. A later session reruns this same command with
the same durable inputs to recover the packet binding; session memory and terminal
output are not authority. Parent-component race hardening remains outside the
trusted-local command threat model.

After one explicit human response, disposition reconstructs all original material
and binds the exact generated document::

   python/.venv/bin/python -m \
     ksdft2effmass.harness.pi.local.record_harness_task_migration_disposition \
     --repository-root /absolute/repository \
     --source-markdown synthetic/source.md \
     --source-revision 0123456789abcdef0123456789abcdef01234567 \
     --git-object 89abcdef0123456789abcdef0123456789abcdef \
     --candidate-task-json synthetic/candidate.json \
     --source-mapping-record synthetic/mapping.json \
     --projection-profile synthetic/profile.json \
     --review-document synthetic/review.md \
     --expected-review-sha256 <digest> \
     --expected-review-byte-count <count> \
     --expected-packet-binding-sha256 <digest> \
     --human-response-file synthetic/verbatim-response.txt \
     --generic-disposition deferred \
     --migration-disposition DEFER_FILE \
     --output-disposition-record synthetic/disposition.json

The normalized generic value is supplied explicitly; the command never interprets
natural language.  Only ``bounded_correction`` accepts one or more
``--authorized-correction-scope`` values.  The exact compatibility table above
remains authoritative.  Success is exit status 0, deterministic invalidity or
incompatibility is 1, command/path/input invalidity is 2, and the last-resort
internal boundary is 3.

The review Markdown is the complete deterministic review surface but remains
non-authoritative.  Its SHA-256 and byte count are reported.  The canonical
version-1 disposition JSON is a project-local operational record, not a generic wire
kind or mutable workflow status.  No packet envelope is needed because the
recording command losslessly reconstructs the packet from the same explicit inputs.
Neither command changes the source or candidate, applies migration, prepares a next
file, activates a Task, or mutates chain/checkpoint state.  Stage 2B remains inactive;
Stage 2A acceptance remains a separate human decision.

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
