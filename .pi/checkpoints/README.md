# Historical human-decision archive

This directory is retained because calculation manifests, execution
authorizations, schemas, tests, and checksum catalogs identify exact checkpoint
paths and bytes. The JSON records document historical human decisions and
protected-execution boundaries.

This is not an active repository task, agent, or control-plane system. Do not add
new development-planning state here. Do not move, rewrite, or delete existing
records unless every bound calculation and checksum contract is explicitly
migrated with human authorization.

`checkpoint.schema.json` is retained to interpret the archived records. A record's
presence establishes only its represented historical decision and does not grant
new execution, release, publication, or destructive-operation authority.
