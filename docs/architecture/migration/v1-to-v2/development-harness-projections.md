# Development-harness projection migration

## Purpose

This page defines the incremental replacement of the implemented v1
`HarnessControl*` projection path by the Architecture v2 development-harness
compiler and projection boundary. The v1 names are compatibility surfaces during
migration, not permanent aliases for v2 objects.

Repository sources remain authoritative throughout. Generated SQLite, SQL,
manifests, and other projections grant no Task, operation, protected-action, or
scientific authority.

## Increments

### 1. Name and locate the command by its actual effect

The maintained command is `python/src/cli/harness_projection.py`. It directly owns
argument parsing, command-boundary path selection, rendering, and exit codes. The
private `local._commands.harness_control` indirection and temporary
`python/src/cli/harness_control.py` compatibility entry point are removed. Maintained
documentation and callers use only `harness_projection.py`.

### 2. Introduce the immutable artifact-set boundary

Replace the private generation aggregate with the accepted v2 `HarnessArtifact`,
`HarnessArtifactManifest`, `HarnessArtifactSetIdentity`, `HarnessArtifactSet`, and
`HarnessProjectionResult` contracts. Projection returns one complete immutable
candidate set; it does not publish or compare it.

### 3. Separate synchronization and comparison

Move publication into `HarnessSynchronizer` and read-only drift comparison into
`HarnessStateComparator`. Both consume the same validated candidate artifact set.
The v1 `HarnessControlMigrator` and `HarnessControlVerifier` may delegate during
this increment but may not remain independent construction paths.

### 4. Introduce one closed source and compiler path

Add the explicit source contract, `HarnessRepositoryLoader`, closed
`HarnessSourceSnapshot`, `HarnessCompiler`, and complete immutable `HarnessState`.
Synchronization and checking use the same load, compile, validate, and project
path. No operation may rediscover or reinterpret authoritative sources after the
snapshot closes.

### 5. Cut over and remove v1 capability

After replacement behavior passes its accepted compatibility checks:

- keep the removed `python/src/cli/harness_control.py` entry point retired;
- remove every public `HarnessControlMigration*` and `HarnessControlVerification*`
  object and export;
- remove `HarnessControlMigrator` and `HarnessControlVerifier` rather than retaining
  aliases or delegating facades;
- remove the `local.dbcontrol` compatibility modules when no persistence mechanic
  still needs that namespace;
- migrate maintained callers, tests, and documentation to the v2 owners; and
- retain historical records as historical evidence without keeping executable
  compatibility capability.

The migration is incomplete while any old class remains callable through a public
or documented compatibility path.

## Compatibility rule

Compatibility is temporary and one-directional: an old entry point may delegate to
the new implementation during an intermediate increment, but new code may not
import an old entry point. No old name becomes a permanent alias, protocol,
subclass, alternate construction path, or second public spelling for a v2 object.
