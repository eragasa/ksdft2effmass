Project-local compatibility adapters
====================================

The nine public adapter ActionObjects convert explicitly supplied project-local
bytes or records into generic harness records.  They perform no repository
discovery, persistence, activation, protected execution, or scientific
validation.  The supported import path remains
``ksdft2effmass.harness.pi.local``.  The former
``ksdft2effmass.harness.pi.local.adapters`` module is a compatibility facade;
concrete behavior is owned by the Task, control-record, ownership, resource, and
evidence modules.

R2.2 disposition audit
----------------------

The audit found no maintained production-module instantiation or maintained
command/script caller for any adapter.  Tests and historical references are
verification or retained evidence, not live callers.  Repository inspection
cannot prove the absence of third-party imports, however, and all nine names are
part of the fixed public package surface.  Several adapters also consume current
or retained inputs.  Therefore none satisfies both required deletion conditions:
proved absence of a supported external consumer and proved absence of a required
archived input.

.. list-table:: Public adapter dispositions
   :header-rows: 1
   :widths: 12 18 9 9 12 14 9 17

   * - ActionObject
     - ``execute`` parameters after ``self``
     - Production callers
     - Commands/scripts
     - Maintained documentation
     - Resource or archived input
     - Projection relation
     - R2.2 disposition
   * - ``TaskRecordAdapter``
     - ``task_documents, chain_bytes, activation_bytes``
     - None found
     - External-command compatibility is documented; implementation not found
     - :doc:`harness-task` retains projected-JSON and mixed Task compatibility
     - Archived Markdown and version-1 Tasks; current version-2/3 Task JSON
     - Reads deterministic Task JSON projections and retained source records
     - Relocate to the Task owner; retain public and facade imports and exact signature
   * - ``ChainRecordAdapter``
     - ``chain_bytes, task_records, activation_bytes``
     - None found
     - None found
     - Retained H4 compatibility inventory
     - Retained chain and activation fixtures
     - Adapts chain compatibility records
     - Relocate beside Task records; retain public and facade imports and exact signature
   * - ``CheckpointRecordAdapter``
     - ``checkpoint_documents``
     - None found
     - None found
     - Retained H4 compatibility inventory
     - Durable checkpoint JSON and retained checkpoint fixtures
     - Not projection-only
     - Relocate to the control-record owner; retain public and facade imports and exact signature
   * - ``AgentRecordAdapter``
     - ``agent_documents``
     - None found
     - None found
     - Retained H4 compatibility inventory
     - Maintained agent Markdown front matter
     - Not projection-only
     - Relocate to the control-record owner; retain public and facade imports and exact signature
   * - ``OwnershipManifestAdapter``
     - ``manifest_bytes``
     - None found
     - None found
     - Ownership compatibility extension and retained H4 inventory
     - Live version-2 and retained version-1 ownership manifests
     - Not projection-only
     - Relocate to the ownership owner; retain version-1 behavior, imports, and exact signature
   * - ``ChecksumCatalogAdapter``
     - ``catalog_bytes``
     - None found
     - None found
     - Retained H4 compatibility inventory
     - Retained ``sha256sum`` catalogs used as historical integrity evidence
     - Catalogs may be generated snapshots but remain retained inputs
     - Relocate to the resource owner; retain public and facade imports and exact signature
   * - ``SkillInventoryAdapter``
     - ``inventory_bytes, descriptor_bytes``
     - None found
     - None found
     - Retained H4 compatibility inventory
     - Maintained skill inventory and versioned descriptor resources
     - Joins maintained resource records
     - Relocate to the resource owner; retain public and facade imports and exact signature
   * - ``EvidenceOwnershipManifestAdapter``
     - ``manifest_bytes``
     - None found
     - None found
     - Version-1 ownership compatibility extension
     - Retained P1 evidence-ownership manifest
     - Not projection-only
     - Relocate to the evidence owner; retain P1 mapping, imports, and exact signature
   * - ``EvidenceModuleSelector``
     - ``module_payloads, profile``
     - None found
     - None found
     - Retained H4 compatibility inventory
     - Explicit test-module bytes and maintained profile scope rules
     - Selects source bytes; does not translate a projection
     - Relocate to the evidence owner; retain public and facade imports and exact signature

The dispositions preserve compatibility adapter version 1 because behavior,
public imports, and signatures do not change.  A future removal or semantic
change requires a separately authorized public-contract disposition and the
applicable compatibility version change.  The SQLite ``dbcontrol`` package does
not depend on these adapters.

API reference
-------------

.. currentmodule:: ksdft2effmass.harness.pi.local

.. autoclass:: TaskRecordAdapter
   :members:
.. autoclass:: ChainRecordAdapter
   :members:
.. autoclass:: CheckpointRecordAdapter
   :members:
.. autoclass:: AgentRecordAdapter
   :members:
.. autoclass:: OwnershipManifestAdapter
   :members:
.. autoclass:: ChecksumCatalogAdapter
   :members:
.. autoclass:: SkillInventoryAdapter
   :members:
.. autoclass:: EvidenceOwnershipManifestAdapter
   :members:
.. autoclass:: EvidenceModuleSelector
   :members:
