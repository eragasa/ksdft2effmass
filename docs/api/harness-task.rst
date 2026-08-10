Project-local HarnessTask contract
==================================

``HarnessTask`` is the project-local schema-version-3 representation of one
operational Task. The authoritative structured values and relationships live in
``harness/state/harness-control.sqlite3``. Task JSON and
``harness/task-graph.json`` are deterministic compatibility projections.
``TaskRecordAdapter`` continues to consume projected JSON for external command
compatibility, while ``TaskStateInspector`` verifies selected projected state
against SQLite when the tracked database is present.

The earlier 21-interface Stage-2A design was deferred because it modeled a
six-file migration procedure as a permanent subsystem. Migration-framework
renderers, comparators, packets, dispositions, commands, and skill routing are
not public architecture. No compatibility facades are retained for those
unaccepted interfaces.

Minimum object ownership
------------------------

.. list-table:: Retained public Task-model interfaces
   :header-rows: 1

   * - Interface
     - Responsibility
   * - ``HarnessTask``
     - Own the required version-3 Task fields, optional documentation path, and intrinsic invariants.
   * - ``HarnessTaskSerializer``
     - Emit canonical UTF-8 JSON for ``HarnessTask``.
   * - ``HarnessTaskDeserializer``
     - Strictly decode explicit version-3 or retained version-2 JSON bytes.
   * - ``HarnessTaskGraphValidator``
     - Validate one complete, explicitly supplied structural Task graph.

Only ``HarnessTask`` is serialized by this surface. It is not added to the
generic ``WireRecordKind`` family. Constructors own exact semantic types and
intrinsic lexical, ordering, uniqueness, and cross-field invariants. They do not
check repository existence, activation authority, lifecycle meaning,
documentation agreement, completion, or human acceptance.

Canonical Task JSON
-------------------

Canonical version-3 JSON has 17 required fields plus the optional
``documentation_path`` in constructor order, UTF-8 without a BOM, two-space
indentation, literal Unicode, arrays for tuples, ``null`` for optional absence,
and exactly one final LF. ``superseded_by_task_ids`` is required, sorted, unique,
and may be empty. It records identity succession only and grants no activation,
prerequisite, parent, completion, or acceptance authority. ``intake_path`` is
``null`` when no separate non-executable intake artifact exists; a non-null intake
path satisfies the same ``ResourcePath`` contract as other represented paths.
Deserialization accepts noncanonical whitespace and key order but rejects
duplicate, missing, and unknown keys, unsupported versions, invalid UTF-8, BOMs,
and invalid intrinsic values. Retained version 2 omits the supersession field and
is represented in memory with an empty tuple.

``HarnessTaskGraphValidator`` returns ``LocalValidationResult`` with findings in
lexical ``(code, path-or-empty, detail)`` order. It defines duplicate-ID,
missing-parent, parent-cycle, missing-prerequisite, prerequisite-cycle,
missing-supersession, supersession-cycle, duplicate-intake-path, and
duplicate-documentation-path findings under the ``PIHL.TASK`` namespace. Status
meaning, chain selection, repository discovery, and file I/O are excluded.

Migration and documentation boundary
------------------------------------

Canonical Task JSON owns operational contracts and status. Archived Markdown
preserves exact historical source meaning, and maintained computational pages
explain stable scientific rationale without copying mutable Task state. Version-3
supersession permits one predecessor to name multiple canonical replacements;
matching ``superseded_by`` graph edges remain identity relationships rather than
execution dependencies.

The former ignored ``.pi/cache/harness.sqlite`` bootstrap index and its builder
are retired. Existing ignored copies remain disposable and are not a second
control model. Tests for this API provide software verification only; they do
not migrate or activate a Task, authorize execution, establish scientific
validity, or provide human acceptance.

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
