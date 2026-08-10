SQLite-hybrid harness control
=============================

``harness/state/harness-control.sqlite3`` is the authoritative structured
control store for Tasks, evidence and maintained tests, agents and routed
skills, harness resources, and durable decision references. Source code, test
bodies, prompts, skill instructions, schemas, fixtures, narrative documentation,
and exact human responses remain authoritative ordinary files.

The tracked database excludes mutable test-run history, tool events, timing,
token usage, sessions, and telemetry. The reserved
``.pi/cache/harness-observations.sqlite3`` path remains deferred and inactive.

The migration boundary accepts an explicit absolute repository root and writes
through ``HarnessControlMigrator.execute``. By default it preserves the existing
module-inventory ingestion behavior. Callers may instead supply
``HarnessControlMigrationRequest.evidence_module_ownership_path`` as a
root-confined repository-relative path to a closed schema-version-1 ownership
input. The input uses the ``PythonConformanceValidator`` ownership contract
(``path``, ``mode``, ``evidence_class``, and exactly one ``sut`` or ``artifact``
owner), is validated with the explicitly named module bytes, and represents the
complete desired module set. A successful migration therefore supports module
addition, removal or move, and ownership-kind changes while rebuilding
authoritative SQLite and regenerating deterministic SQL and projections.

The migrator stages and verifies the authoritative database, deterministic SQL,
every projection, and the projection manifest before publication. Publication
uses same-directory atomic replacement for each file and retains the complete
prior generation as backups until every replacement succeeds. If an individual
replacement fails, the migrator rolls back all replacements before reporting the
failure, leaving the previously published generation mutually consistent. This
is a process-level failure-atomic rollback guarantee; it is not filesystem-level
multi-file atomicity across a process crash, power loss, or storage failure.

The thin control command exposes the same input as
``migrate --evidence-module-ownership PATH``; the option is invalid for
``verify``.

``HarnessControlVerifier`` checks
SQLite integrity and foreign keys, reconstructs a database from the deterministic
SQL export, compares ordered semantic digests and raw database identities, and
regenerates projections for exact comparison. Passing these checks establishes
software-contract consistency only.

.. currentmodule:: ksdft2effmass.harness.pi.local

.. autoclass:: HarnessControlMigrationRequest
.. autoclass:: HarnessControlMigrationResult
.. autoclass:: HarnessControlMigrator
   :members:
.. autoclass:: HarnessControlVerificationResult
.. autoclass:: HarnessControlVerifier
   :members:
