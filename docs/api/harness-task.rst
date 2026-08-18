Project-local HarnessTask contract
==================================

``HarnessTask`` is the project-local schema-version-3 representation of one
operational Task. Canonical Task definitions live in ``harness/tasks/*.json``;
their ``parent_task_id`` and ``task_prerequisite_ids`` fields collectively define
the development Task graph. Child identities are derived from those fields and
are never stored on parent Tasks.

``HarnessTaskRegistry`` is an immutable in-memory index over explicitly supplied
canonical Tasks. It is not a second persisted catalog or topology authority.
``harness/tasks/*.json`` records are the canonical topology and lifecycle surfaces.
``harness/task-graph.json``, the Task tables in
``harness/state/harness-control.sqlite3``, and any retained chain-shaped views are
deterministic read or compatibility projections.

``DevelopmentTaskSelection`` separately represents only the current active Task
reference, explicit activation-receipt references, and the disabled automatic
successor policy. The canonical version-1 record is
``harness/task-selection.json``. Selection grants no authority and contains no
Task hierarchy, prerequisites, lifecycle status, scope, sequence, protected-action
permission, or scientific Workflow state. Task-state inspection consumes exact canonical Task and selection paths plus an
optional operation-scoped ownership manifest. Ownership is neither embedded in the
Task nor discovered from an ambient registry. Retired chain adapters remain historical
compatibility surfaces only and do not feed current inspection or selection.

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
     - Strictly decode explicit version-3 JSON bytes.
   * - ``HarnessTaskGraphValidator``
     - Validate one complete, explicitly supplied structural Task graph.
   * - ``HarnessTaskRegistry``
     - Index explicitly supplied Tasks and derive child and prerequisite identities without storing graph edges independently.
   * - ``DevelopmentTaskSelection``
     - Own minimal current selection facts without Task content or authority.
   * - ``DevelopmentTaskSelectionSerializer`` and ``DevelopmentTaskSelectionDeserializer``
     - Own the strict canonical version-1 selection-state JSON wire format.

Only ``HarnessTask`` and ``DevelopmentTaskSelection`` are serialized by this
surface. Neither is added to the
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
and invalid intrinsic values. Live Task schema versions other than 3 are rejected.

``HarnessTaskRegistry`` requires a nonempty unique Task-ID-sorted tuple. Its
identity lookup returns the exact registered object. Child lookup derives from
``parent_task_id`` and prerequisite lookup returns the canonical
``task_prerequisite_ids`` tuple. Recursive descendant lookup returns proper
descendants in deterministic depth-first pre-order, fails closed on a reachable
parent cycle, and performs no lifecycle, prerequisite, selection, or authority
interpretation. Cross-record existence and complete cycle policy remains with
``HarnessTaskGraphValidator``.

Canonical selection JSON has four required fields in constructor order:
``schema_version``, ``active_task_id``, ``explicit_activation_receipt_ids``, and
``automatic_successor_activation``. Version 1 requires sorted unique receipt
references and literal ``false`` automatic succession. The repository record may
represent one selected Task and receipt references or an inactive state; historical
chain activation lists are not converted into current authority.

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

.. currentmodule:: ksdft2effmass.harness

.. autoclass:: HarnessTask
.. autoclass:: HarnessTaskSerializer
   :members:
.. autoclass:: HarnessTaskDeserializer
   :members:
.. autoclass:: HarnessTaskRegistry
   :members:
.. autoclass:: DevelopmentTaskSelection
.. autoclass:: DevelopmentTaskSelectionSerializer
   :members:
.. autoclass:: DevelopmentTaskSelectionDeserializer
   :members:

``HarnessTaskGraphValidator`` remains on the transitional project-local validation
boundary until normalized Architecture-v2 Harness validation supplies its normative
result contract.

.. currentmodule:: ksdft2effmass.harness.pi.local

.. autoclass:: HarnessTaskGraphValidator
   :members:
