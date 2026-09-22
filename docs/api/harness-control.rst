SQLite-hybrid Harness projections
=================================

``harness/state/harness-control.sqlite3`` is the authoritative structured
control store for Tasks, evidence and maintained tests, agents and routed
skills, harness resources, and durable decision references. Source code, test
bodies, Task records, prompts, skill instructions, schemas, fixtures, narrative
documentation, and exact human responses remain authoritative ordinary files.

The tracked database excludes mutable test-run history, tool events, timing,
token usage, sessions, and telemetry. The reserved
``.pi/cache/harness-observations.sqlite3`` path remains deferred and inactive.

Migration and publication
-------------------------

The maintained ``harness_projection.py sync`` command resolves the exact
``harness/configuration.json`` and referenced ``.pi/settings.json`` bytes into one
immutable ``HarnessConfiguration``. It constructs one private immutable projection
request from that value and the Python test modules enumerated beneath its configured
test root. Persistence, evidence-policy, resource, and catalog paths come only from
the resolved configuration; superseded per-input command flags are unsupported.
Before database ingestion,
``PiHarnessAgentDefinitionResolver`` composes each exact descriptor with that
configuration into immutable ``PiHarnessAgentDefinition``.
Low-level explicit requests remain only as bounded injected test seams and are not a
second maintained canonical route. Generated evidence inventories are projections and
are never accepted as migration inputs.

One private project-local builder constructs the complete candidate database,
deterministic SQL, projection manifest, and every projection in a caller-owned
temporary workspace. ``local.control`` depends on domain owners and the persistence
mechanics in ``local.dbcontrol``. The two public compatibility facade modules
``local.dbcontrol.migration`` and ``local.dbcontrol.verification`` are the narrow
explicit exception: they preserve their accepted import and defining-module identities
while delegating to private control orchestration. Database, schema, encoding,
ingestion, resource, projection, record, and input-selection mechanics do not depend on
``local.control``.

The generation result is an immutable data-only descriptor. The private
synchronization action validates that complete candidate and remains the sole
maintained publisher. Its publication boundary exclusively reads candidate bytes and
prepares maintained destinations. Publication stages each output,
verifies the staged database, and retains backups until all replacements
succeed. A replacement failure restores the prior complete generation. This is
a process-level rollback guarantee, not filesystem-wide atomicity across a
crash, power loss, or storage failure.

The maintained projection command is:

.. code-block:: text

   python3 -m ksdft2effmass.harness.cli harness-projection sync --repository-root <ABSOLUTE_ROOT>
   python3 -m ksdft2effmass.harness.cli harness-projection check --repository-root <ABSOLUTE_ROOT>

The maintained command is ``python3 -m ksdft2effmass.harness.cli harness-projection``. The former ``python/src/cli/harness_control.py`` compatibility entry point and public
``HarnessControl*`` Python API have been removed. The private v1 implementation
remains only behind the maintained projection command until replacement behavior
exists and passes the applicable compatibility checks.

Verification
------------

The private check action derives canonical maintained inputs from repository-owned
source configuration and uses the same private builder in an isolated temporary
workspace. It publishes nothing. Verification establishes:

* SQLite ``integrity_check`` and foreign-key integrity;
* schema and control-schema-version agreement;
* normalized ordered logical table agreement;
* exact canonical SQL agreement;
* exact projection-manifest agreement; and
* exact agreement for every publisher-owned projection, including missing,
  changed, and unexpected owned-artifact detection.

SQLite database files are not canonical byte representations. Raw SHA-256
values are reported diagnostically, but raw-byte inequality alone is not drift.
Candidate workspaces are removed after success and failure. Verification never
searches for or deletes repository-wide sidecar, staging, backup, WAL, or SHM
files.

Repository validation
---------------------

``HarnessValidator.execute`` composes existing structural domain owners into six
stably ordered real ``HarnessValidationCheck`` records: ``python_conformance``,
``resources``, ``task_graph``, ``checkpoints``, ``skills``, and ``control_state``. The
former ``python_evidence`` check value is unsupported rather than retained as an
alias.
Canonical Python conformance inputs flow directly through
``PythonConformanceValidator`` to ``python_conformance``; canonical repository projection
inputs separately flow through the private check action to ``control_state``.
The result has no elapsed-duration or telemetry field. The Action invokes no CLI,
parses no CLI output, and executes none of pytest, Ruff, mypy, or Sphinx. Those
limitations remain explicit claim boundaries rather than placeholder checks.

The maintained renderer is:

.. code-block:: text

   python3 -m ksdft2effmass.harness.cli validate-harness --repository-root <ABSOLUTE_ROOT>

It returns zero when no check is ``FAIL`` (``WARN`` is permitted), one for an
expected failing check, two for invalid command input or request construction,
and three for an unexpected command-boundary exception. Structural repository
validation does not establish numerical verification, scientific validation,
uncertainty quantification, protected execution, or human acceptance.

Python conformance API
----------------------

The public Python conformance owner is
``ksdft2effmass.harness.pi.conformance.python``. The former
``ksdft2effmass.harness.pi.evidence`` facade is retired; repository evidence
artifact paths are unaffected.

.. currentmodule:: ksdft2effmass.harness.pi.conformance.python

.. autoclass:: PythonModuleSource
.. autoclass:: PythonConformanceRequest
   :members: legacy_module_level
.. autoclass:: PythonConformanceFinding
.. autoclass:: PythonConformanceResult
.. autoclass:: PythonConformanceValidator
   :members:

Harness configuration API
-------------------------

Source and resolved configuration use schema 2 and require
``catalogs.task_catalog`` with ordered ``research_root``, ``simulation_root`` and
``software_root`` members. JSON uses exact ordered members, two-space indentation,
literal UTF-8 Unicode and one final LF. Schema 1 and the flat ``task_root`` member
are rejected; historical fixtures are refusal evidence, not runtime compatibility.

``HarnessCatalogConfiguration`` requires ``task_catalog`` as its first argument,
followed by ``agent_roots``, ``checkpoint_roots`` and ``skill_roots``. There is no
flat-layout option. Resolution-result, normalized Pi and snapshot-framing versions
remain independently at 1; they are not obsolete configuration formats.

The three categorized roots are explicit normalized repository-relative strings.
They must not be equal or nested by path components, including case-folded
aliases. Near-prefix siblings are permitted; inputs are not silently normalized.
Other catalog roots retain their existing ordering and exact-distinctness rules.
Filesystem existence, actual aliases, confinement, Task classification and
execution authority are not properties of configuration values.

Local consumers read all three configured catalogs, reject duplicate IDs and
symlinked inputs, and retain actual source paths through SQL and projection.
Dependencies may cross catalogs; placement confers no authority. Control database
schema 4 stores current schema-3 Tasks, including optional documentation paths,
and has no historical Task-alias table. This is software structure, not scientific
validation or proof against concurrent filesystem replacement.

.. currentmodule:: ksdft2effmass.harness

.. autoclass:: HarnessConfiguration
.. autoclass:: HarnessConfigurationSource
.. autoclass:: HumanReviewConfiguration
.. autoclass:: HarnessPersistenceConfiguration
.. autoclass:: PythonConformanceConfiguration
.. autoclass:: HarnessResourceConfiguration
.. autoclass:: HarnessCatalogConfiguration
.. autoclass:: TaskCatalogConfiguration
.. autoclass:: ContentIdentity
.. autoclass:: SnapshotIdentity
.. autoclass:: HarnessConfigurationSourceBinding
.. autoclass:: HarnessConfigurationResolutionFinding
.. autoclass:: HarnessConfigurationResolutionResult
.. autoclass:: HarnessConfigurationResolver
   :members:
.. autoclass:: HarnessConfigurationSourceJsonSerializer
   :members:
.. autoclass:: HarnessConfigurationSourceJsonDeserializer
   :members:
.. autoclass:: HarnessConfigurationJsonSerializer
   :members:
.. autoclass:: HarnessConfigurationJsonDeserializer
   :members:
.. autoclass:: HarnessConfigurationValidator
   :members:

.. currentmodule:: ksdft2effmass.harness.pi

.. autoclass:: PiHarnessConfiguration
.. autoclass:: PiHarnessConfigurationDeserializer
   :members:
.. autoclass:: PiHarnessAgentDefinition
.. autoclass:: PiHarnessAgentDefinitionResolver
   :members:

.. currentmodule:: ksdft2effmass.harness.pi.local

.. autoclass:: HarnessValidationRequest
.. autoclass:: HarnessValidationCheck
.. autoclass:: HarnessValidationResult
.. autoclass:: HarnessValidator
   :members:
