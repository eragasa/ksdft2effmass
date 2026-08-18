Project-local compatibility adapters
====================================

Six public adapter ActionObjects convert explicitly supplied project-local bytes or
records into generic harness records. They perform no repository
discovery, persistence, activation, protected execution, or scientific
validation.  The supported package import path remains
``ksdft2effmass.harness.pi.local``.  The module
``ksdft2effmass.harness.pi.local.adapters`` remains a compatibility facade;
concrete behavior is owned by the Task, control-record, ownership, resource, and
evidence modules.

R2.2 audit and decomposition
----------------------------

The completed R2.2 Task is **Audit and decompose project-local adapters**. The table
below is retained historical disposition; the v2 Task-graph cutover later retired
``TaskRecordAdapter`` and ``ChainRecordAdapter`` after canonical Task and selection
inputs replaced their live role.
Repository inspection found no maintained internal production instantiation and
no maintained command or script caller for any of the nine adapters.  That
finding establishes maintained repository non-use only.  Each currently
exported public API remains a compatibility obligation.  Removing one requires
a separately authorized compatibility or deprecation decision; repository
non-use alone neither authorizes nor permanently prohibits removal.

Retained historical bytes identify prior formats and behavior.  Their mere
existence does not prove that a live public adapter remains necessary.  Tests and
historical references are verification or retained evidence, not production
callers.

The exact completed disposition is:

* adapters audited: **9**;
* adapters relocated: **9**;
* adapters removed: **0**;
* public imports preserved: **9**; and
* ``execute`` signatures preserved: **9**.

.. list-table:: R2.2 adapter dispositions
   :header-rows: 1
   :widths: 12 15 10 10 12 15 15 18 18

   * - ActionObject
     - ``execute`` parameters after ``self``
     - Maintained internal production caller
     - Maintained command or script caller
     - Supported public import
     - Current input format
     - Retained historical input
     - Actual compatibility obligation
     - Final R2.2 disposition
   * - ``TaskRecordAdapter``
     - ``task_documents, chain_bytes, activation_bytes``
     - None found
     - None found; documentation mentions external-command compatibility
     - Package import and ``local.adapters`` facade
     - Version-3 Task JSON, chain JSON, activation JSON, and explicitly supplied Markdown
     - Version-1/2 Task JSON, bootstrap Markdown, and retained activation records
     - Exported class, exact signature, documented mixed-format behavior, and result contract
     - Relocated to ``task_adapters``; facade retained; not removed
   * - ``ChainRecordAdapter``
     - ``chain_bytes, task_records, activation_bytes``
     - None found
     - None found
     - Package import and ``local.adapters`` facade
     - Chain JSON, adapted Task references, and activation JSON
     - Retained H4 chain and activation fixtures
     - Exported class, exact signature, and chain-view result contract
     - Relocated to ``task_adapters``; facade retained; not removed
   * - ``CheckpointRecordAdapter``
     - ``checkpoint_documents``
     - None found
     - None found
     - Package import and ``local.adapters`` facade
     - Explicit checkpoint JSON path/byte pairs
     - Retained resolved-checkpoint fixtures
     - Exported class, exact signature, and checkpoint adaptation contract
     - Relocated to ``control_record_adapters``; facade retained; not removed
   * - ``AgentRecordAdapter``
     - ``agent_documents``
     - None found
     - None found
     - Package import and ``local.adapters`` facade
     - Agent Markdown front matter containing ``name`` and ``acceptanceRole``
     - Retained agent-document fixtures and historical records
     - Exported class, exact signature, and front-matter adaptation contract
     - Relocated to ``control_record_adapters``; facade retained; not removed
   * - ``OwnershipManifestAdapter``
     - ``manifest_bytes``
     - None found
     - None found
     - Package import and ``local.adapters`` facade
     - Version-2 ownership-manifest JSON
     - Version-1 ownership manifests and local ``boundary_owned`` spelling
     - Exported class, exact signature, and supported version-1/2 behavior
     - Relocated to ``ownership_adapters``; facade retained; not removed
   * - ``ChecksumCatalogAdapter``
     - ``catalog_bytes``
     - None found
     - None found
     - Package import and ``local.adapters`` facade
     - UTF-8 ``sha256sum``-style catalog bytes
     - Retained checksum catalogs
     - Exported class, exact signature, and catalog parsing contract
     - Relocated to ``resource_adapters``; facade retained; not removed
   * - ``SkillInventoryAdapter``
     - ``inventory_bytes, descriptor_bytes``
     - None found
     - None found
     - Package import and ``local.adapters`` facade
     - Skill-inventory JSON and versioned descriptor JSON
     - Retained capability inventories and descriptors
     - Exported class, exact signature, descriptor selection, and ordering contract
     - Relocated to ``resource_adapters``; facade retained; not removed
   * - ``EvidenceModuleSelector``
     - ``module_payloads, profile``
     - None found
     - None found
     - Package import and ``local.adapters`` facade
     - Explicit module path/byte pairs and a project profile
     - Retained profile and module-selection fixtures
     - Exported class, exact signature, path-scope selection, and ordering contract
     - Relocated to ``evidence_adapters``; facade retained; not removed

R2.2 decomposed the adapter monolith into five contract-specific modules and
retained a compatibility facade. R2.7 subsequently removed the unused
``EvidenceOwnershipManifestAdapter`` closure. The v2 Task-graph cutover retired the two
chain-owned adapters, leaving six operational adapters. Retired development-chain
bytes remain non-operational history rather than supported adapter input.

The remaining adapters preserve their behavior, public imports, and signatures. The
SQLite ``dbcontrol`` package
does not depend on these adapters.

API reference
-------------

.. currentmodule:: ksdft2effmass.harness.pi.local

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
.. autoclass:: EvidenceModuleSelector
   :members:
