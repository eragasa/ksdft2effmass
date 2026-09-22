Development prerequisite resolution
===================================

.. currentmodule:: ksdft2effmass.harness

Development prerequisite resolution matches consumer-owned requirements to explicit
references for owner-retained results.  It does not infer completion from Task status,
selection, review, test passage, paths alone, or generated projections.

A :class:`DevelopmentPrerequisiteContract` is an immutable sidecar bound to one exact
consumer Task and its SHA-256 :class:`ContentIdentity`.  The immutable DataObject can
represent an incomplete contract, but the resolver checks that its requirements cover
every canonical Task and external prerequisite edge exactly once and fails closed on
any mismatch.  Requirements select the single accepted
``effective_not_revoked`` lineage policy. Result references retain their owner, kind,
claim, producer revision, retention boundary, content identity, and effective,
superseded, or revoked lineage without copying the result payload.

The fieldless :class:`DevelopmentPrerequisiteResolver` consumes the exact Task,
content identity, contract, and complete explicit observations. Every observation,
including a negative observation, identifies its exact owner and retention boundary.
Each edge resolves to
``satisfied``, ``missing``, ``conflicting``, ``superseded``, ``revoked``,
``unavailable``, or ``indeterminate``.  A complete successful absence observation is
``missing``; an identified object that cannot be obtained is ``unavailable``; failed
observation, integrity, or version determination is ``indeterminate``.  The aggregate
is satisfied only when every edge is satisfied and no blocking aggregate diagnostic
exists.

Resolution is software eligibility evidence only.  It performs no repository
discovery, persistence, serialization, selection, activation, authorization, repair,
or successor choice and grants no protected or scientific execution authority.

Diagnostics
-----------

Diagnostic identities are stable public result values. Aggregate diagnostics describe
contract or observation-set closure; edge diagnostics describe one declared edge.

.. list-table:: Resolver diagnostics
   :header-rows: 1

   * - Identity
     - Placement and trigger
   * - ``prerequisite.contract.task-id-mismatch``
     - Aggregate: contract consumer identity differs from the supplied Task.
   * - ``prerequisite.contract.task-content-mismatch``
     - Aggregate: contract content identity differs from the supplied Task bytes.
   * - ``prerequisite.contract.edge-coverage-mismatch``
     - Aggregate: requirements do not cover every declared edge exactly once.
   * - ``prerequisite.observation.undeclared-edge``
     - Aggregate: an observation names an edge not declared by the Task.
   * - ``prerequisite.contract.invalid``
     - Edge: aggregate Task binding or requirement coverage is invalid.
   * - ``prerequisite.observation.missing``
     - Edge: no observation was supplied; this is not a complete absence observation.
   * - ``prerequisite.observation.duplicate``
     - Edge: more than one observation was supplied for the edge.
   * - ``prerequisite.observation.binding-mismatch``
     - Edge: observation owner or retention boundary differs from the requirement.
   * - ``prerequisite.requirement.unsupported-lineage-policy``
     - Edge: the requirement does not select the implemented policy.
   * - ``prerequisite.result.binding-mismatch``
     - Edge: a found result differs from an exact requirement binding.
   * - ``prerequisite.result.duplicate-identity``
     - Edge: found references repeat one result identity.
   * - ``prerequisite.result.multiple-effective``
     - Edge: more than one distinct effective result matches.
   * - ``prerequisite.result.superseded``
     - Edge: every matching result is superseded.
   * - ``prerequisite.result.revoked``
     - Edge: every matching result is revoked.
   * - ``prerequisite.result.lineage-conflict``
     - Edge: non-effective matching results report contradictory lineage.

Owner-supplied diagnostics for ``unavailable`` and ``indeterminate`` observations are
also preserved as edge diagnostics; their identities remain owned by that observation
contract rather than this resolver.

API reference
-------------

.. autoclass:: DevelopmentPrerequisiteKind
   :members:
.. autoclass:: DevelopmentPrerequisiteLineage
   :members:
.. autoclass:: DevelopmentPrerequisiteLineagePolicy
   :members:
.. autoclass:: DevelopmentPrerequisiteObservationStatus
   :members:
.. autoclass:: DevelopmentPrerequisiteOutcome
   :members:
.. autoclass:: DevelopmentPrerequisiteAggregateStatus
   :members:
.. autoclass:: DevelopmentPrerequisiteRequirement
   :members:
.. autoclass:: DevelopmentPrerequisiteContract
.. autoclass:: RetainedPrerequisiteResultReference
.. autoclass:: RetainedPrerequisiteObservation
   :members:
.. autoclass:: DevelopmentPrerequisiteEdgeResult
.. autoclass:: DevelopmentPrerequisiteResolutionResult
   :members:
.. autoclass:: DevelopmentPrerequisiteResolver
   :members:
