Project-local HarnessTask contract
==================================

``HarnessTask`` is the project-local schema-version-2 representation of one
operational Task. JSON owns operational Task fields after migration. Markdown
retains maintained human explanation, while chain JSON owns ordering and
activation. ``TaskRecordAdapter`` temporarily supports Markdown, version-1 JSON,
and version-2 JSON; ``TaskStateInspector`` preserves selected-state inspection.

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
     - Own the 16 intrinsic version-2 Task fields and their invariants.
   * - ``HarnessTaskSerializer``
     - Emit canonical UTF-8 JSON for ``HarnessTask``.
   * - ``HarnessTaskDeserializer``
     - Strictly decode explicit version-2 JSON bytes.
   * - ``HarnessTaskGraphValidator``
     - Validate one complete, explicitly supplied structural Task graph.

Only ``HarnessTask`` is serialized by this surface. It is not added to the
generic ``WireRecordKind`` family. Constructors own exact semantic types and
intrinsic lexical, ordering, uniqueness, and cross-field invariants. They do not
check repository existence, activation authority, lifecycle meaning,
documentation agreement, completion, or human acceptance.

Canonical Task JSON
-------------------

Canonical JSON has the 16 fields in constructor order, UTF-8 without a BOM,
two-space indentation, literal Unicode, arrays for tuples, ``null`` for optional
absence, and exactly one final LF. Deserialization accepts noncanonical whitespace
and key order but rejects duplicate, missing, and unknown keys, unsupported
versions, invalid UTF-8, BOMs, and invalid intrinsic values.

``HarnessTaskGraphValidator`` returns ``LocalValidationResult`` with findings in
lexical ``(code, path-or-empty, detail)`` order. It defines duplicate-ID,
missing-parent, parent-cycle, missing-prerequisite, prerequisite-cycle,
duplicate-intake-path, and duplicate-documentation-path findings under the
``PIHL.TASK`` namespace. Status meaning, chain selection, repository discovery,
and file I/O are excluded.

Migration and documentation boundary
------------------------------------

The bounded migration procedure is:

#. start from existing authoritative Markdown;
#. have the human identify operational fields;
#. prepare candidate canonical ``HarnessTask`` JSON;
#. retain narrative Markdown;
#. review an ordinary Git diff; and
#. record an explicit human decision.

This procedure is not a reusable migration workflow engine. Existing Markdown
remains authoritative for the six unmigrated Tasks. Deterministic
JSON-to-Markdown rendering is deferred unless one real migration later
demonstrates a recurring need. Tests for this API provide software verification
only; they do not migrate a Task, activate work, establish scientific validity,
or provide human acceptance.

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
