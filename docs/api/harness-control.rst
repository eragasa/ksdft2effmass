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
through ``HarnessControlMigrator.execute``. ``HarnessControlVerifier`` checks
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
