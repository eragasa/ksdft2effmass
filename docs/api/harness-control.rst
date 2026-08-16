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

``HarnessControlMigrator.execute`` accepts one explicit
``HarnessControlMigrationRequest``. Canonical maintained requests supply normalized
``PiHarnessConfiguration``, Python evidence source modules, the profile matrix, the
predecessor map, and generic and local resource configuration explicitly.
``PiHarnessConfigurationDeserializer`` converts caller-supplied Pi project-settings
JSON bytes into the narrow immutable configuration. Before database ingestion,
``PiHarnessAgentDefinitionResolver`` composes each exact descriptor with that
configuration into immutable ``PiHarnessAgentDefinition``.
Noncanonical explicit requests with an empty evidence corpus and empty Pi Harness
configuration remain supported. Generated evidence inventories are projections and
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

The generation result is an immutable data-only descriptor. The migrator validates
that complete candidate and remains the sole maintained publisher through
``HarnessControlMigrator._publish_generation``, which exclusively reads candidate
bytes and prepares maintained destinations. Publication stages each output,
verifies the staged database, and retains backups until all replacements
succeed. A replacement failure restores the prior complete generation. This is
a process-level rollback guarantee, not filesystem-wide atomicity across a
crash, power loss, or storage failure.

The maintained projection command is:

.. code-block:: text

   python/.venv/bin/python python/src/cli/harness_projection.py sync --repository-root <ABSOLUTE_ROOT> --pi-settings .pi/settings.json <EXPLICIT_CANONICAL_INPUTS>
   python/.venv/bin/python python/src/cli/harness_projection.py check --repository-root <ABSOLUTE_ROOT>

The maintained command is ``python/src/cli/harness_projection.py``. The former
``python/src/cli/harness_control.py`` compatibility entry point has been removed. The
remaining ``HarnessControl*`` Python API is temporary and scheduled for removal after
its replacement behavior exists and passes the applicable compatibility checks.

Verification
------------

``HarnessControlVerifier.execute`` derives canonical maintained inputs from
repository-owned source configuration and uses the same private builder in an
isolated temporary workspace. It publishes nothing. Verification establishes:

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
stably ordered real ``HarnessValidationCheck`` records: ``python_evidence``,
``resources``, ``task_graph``, ``checkpoints``, ``skills``, and ``control_state``.
Canonical Python evidence inputs flow directly through
``PythonConformanceValidator`` to ``python_evidence``; canonical repository control
inputs separately flow through ``HarnessControlVerifier`` to ``control_state``.
The result has no elapsed-duration or telemetry field. The Action invokes no CLI,
parses no CLI output, and executes none of pytest, Ruff, mypy, or Sphinx. Those
limitations remain explicit claim boundaries rather than placeholder checks.

The maintained renderer is:

.. code-block:: text

   python/.venv/bin/python python/src/cli/validate_harness.py --repository-root <ABSOLUTE_ROOT>

It returns zero when no check is ``FAIL`` (``WARN`` is permitted), one for an
expected failing check, two for invalid command input or request construction,
and three for an unexpected command-boundary exception. Structural repository
validation does not establish numerical verification, scientific validation,
uncertainty quantification, protected execution, or human acceptance.

.. currentmodule:: ksdft2effmass.harness.pi

.. autoclass:: PiHarnessConfiguration
.. autoclass:: PiHarnessConfigurationDeserializer
   :members:
.. autoclass:: PiHarnessAgentDefinition
.. autoclass:: PiHarnessAgentDefinitionResolver
   :members:

.. currentmodule:: ksdft2effmass.harness.pi.local

.. autoclass:: HarnessControlMigrationRequest
.. autoclass:: HarnessControlMigrationResult
.. autoclass:: HarnessControlMigrator
   :members:
.. autoclass:: HarnessControlVerificationFinding
.. autoclass:: HarnessControlVerificationResult
.. autoclass:: HarnessControlVerifier
   :members:
.. autoclass:: HarnessValidationRequest
.. autoclass:: HarnessValidationCheck
.. autoclass:: HarnessValidationResult
.. autoclass:: HarnessValidator
   :members:
