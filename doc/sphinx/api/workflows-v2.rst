Provisional workflow v2
=======================

``ksdft2effmass.workflows.v2`` is a temporary compatibility boundary for the
future ProjectKoios Workflows owner.  It does not replace or alias the established
``ksdft2effmass.workflows`` v1 package.  The v2 core and runtime perform no
calculator execution, scientific interpretation, scheduling, queueing, or automatic
retry of ambiguous effects.

The architecture and migration limits are recorded in
``docs/architecture/v2/ksdft2effmass/workflows/v2/index.md`` and the corresponding
technical-debt record.  Software verification establishes implementation behavior
only; it does not establish scientific validation or protected-execution authority.

Engine-neutral core
-------------------

The core owns immutable identities, definitions, run and state snapshots, validation,
transition processing, and deterministic replay.  It performs no persistence or
external effect.

.. automodule:: ksdft2effmass.workflows.v2.core
   :members:
   :member-order: bysource
   :show-inheritance:

Private local revision persistence
----------------------------------

The persistence package stores opaque revision bytes.  Domain validation and workflow
meaning remain outside the store.

.. automodule:: ksdft2effmass.workflows.v2.persistence
   :members:
   :member-order: bysource
   :show-inheritance:

Bounded foreground runtime
--------------------------

The runtime owns append-only events, deterministic foreground plans, exact
attempt-bound authorization correlation, application-owned worker handoff, query-only
reconciliation, replay, and final transition gating.  Every public runtime operation
uses one immutable request, one concrete actionizer, and one immutable result.

.. automodule:: ksdft2effmass.workflows.v2.runtime
   :members:
   :member-order: bysource
   :show-inheritance:
