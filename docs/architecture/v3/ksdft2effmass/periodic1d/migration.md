# Migration sequence

## Definition of done

Periodic1D matches the PIAB1D/QHO1D architectural style when each selected scientific
family has:

- concrete immutable typed configuration and result owners;
- one direct producer over reviewed reusable behavior;
- exact canonical result bytes and constructor-restored invariants;
- a byte-owning independent verifier with operation-named comparisons;
- a verifier-derived authenticated visualization projection;
- a closed renderer inventory owned by concrete classes in the appropriate installed
  source subpackage rather than by temporary planning documentation;
- direct module-scope calculate → verify → render scripts under its calculation owner;
- explicit unsealed or sealed provenance state; and
- an exact disposition for every predecessor import, wire, artifact, and consumer.

The program is not done merely because files share PIAB1D/QHO1D names or inherit common
base classes.

## Phase 0 — freeze the current boundary

Before source mutation:

1. inventory every supported `ksdft2effmass.periodic1d` import and caller;
2. inventory the M1--M3 definitions, results, serializers, verifier inputs, schema IDs,
   retained artifacts, publication consumers, and exact Git recovery references;
3. record which historical wires must remain decodable and which are provenance-only;
4. record current numerical cases and expected values without weakening tolerances; and
5. identify every calculation-local reusable kernel that must move to an installed
   domain owner or be deleted.

**Gate:** every current public symbol and retained byte surface has one target owner or
explicit historical disposition. No source deletion occurs in this phase.

## Phase 1 — complete the Mathieu1D direct vertical slice

Use `calculations/mathieu1d/` as the first periodic direct-lifecycle implementation
because it already has a typed study donor, strict retained schemas, a Git-bound package
verifier, and a concrete model-system owner.

Implement model-owned configuration, result sections, analyzer, byte-owning independent
verification, authenticated visualization data, and direct calculation, verification,
and rendering scripts. The historical `study/` and retained `v1` packages remain separate
until exact parity and consumer migration are proven.

This phase does not redefine Mathieu1D as the compatible rank-one null control.

**Gate:** calculate → verify → render works from Python-authored controls; rendering
rejects unauthenticated data; historical retained bytes are unchanged.

## Phase 2 — implement the compatible rank-one null control

Implement the distinct
`calculations/periodic1d/rank1/fourier-locality/` family. Reuse scalar Fourier behavior
that has the same meaning, but retain the compatible parent definition and explicit
operator-trivial phase result.

**Gate:** the calculation emits no false gauge-locality channel, independently verifies
the complete transform and declared truncation/fitting routes, and remains distinct from
Mathieu1D in scientific scope and provenance.

## Phase 3 — split the rank-two families

Migrate the two rank-two questions independently:

1. `band-equivalence-versus-hopping-locality` owns exact band-equivalence construction,
   restricted-alignment comparison, hopping locality, and finite-range consequences;
2. `composite-band-alignment-locality` owns its selected parent, sampling roles,
   pointwise/global alignment policy, and block-locality diagnostics.

Move reusable calculation-local behavior into cohesive installed owners only after its
meaning and callers are identified. Do not copy `workflow/` trees into source, and do
not preserve Workflow-shaped public APIs.

**Gate:** each family has separate typed wires, independent verification, rendering,
tolerances, execution record, and claim boundary. Neither imports the other's
calculation tree.

## Phase 4 — constrained admissible sets and sensitivity

Rebuild admissible-set composition over authenticated typed upstream results. Keep the
confirmatory family, scalar demonstration, and post-hoc threshold-sensitivity analysis
as separate calculation records. Verification reconstructs quadratics, witnesses,
threshold comparisons, and separation certificates without invoking the producer.

**Gate:** upstream result digests are explicit dependencies; stored pass labels are not
oracles; changing thresholds cannot mutate or masquerade as the confirmatory result.

## Phase 5 — higher rank

Migrate the higher-rank composite calculation only after rank-two contracts expose the
reusable behavior it actually needs. Preserve declared rank, frame, sewing, alignment,
and scalar-ledger semantics. Do not infer higher-rank validation from rank-two tests.

**Gate:** typed result and verification wires exist, every decisive value has an
independent check, authenticated rendering is closed, and any retained execution uses a
fresh identifier.

## Phase 6 — add selected formal certificates only after native freeze

Formal integration is optional and proposition-specific. It begins only after one study
has a frozen native configuration, schema, producer, byte-owning independent verifier,
and retained conforming package. KSD then defines a strict compact export of exact
rationals or documented outward rational intervals bound to the native result digest.
Formal does not invent the runtime wire, and KSD does not treat binary64 JSON as exact.

**Gate:** request and checker-result schemas reject unknown fields and versions, missing
mandatory data, noncanonical bytes, incomplete finite coverage, digest mismatch, failed
numerical verification, invalid weights, space or unit mismatches, failed sewing or
Hermiticity gates, split equal-radius ties, and joint decisions formed from different
candidates. An obligation whose interval overlaps a decisive threshold is recorded as
`unresolved`; a claimed decisive pass, failure, or joint decision is not accepted. The
checked conclusion remains separate from scientific acceptance or evidence promotion.

## Phase 7 — retire predecessor and temporary planning surfaces

For each implemented study, migrate its section of
[`visualization.md`](visualization.md) into concrete projection, plot, subplot, figure,
renderer, and visualizer classes under the selected installed source owner. Add public API
documentation and tests there. When all eight sections have moved, reduce the temporary
page to source links or remove it so it cannot compete with the implementation.

For each old module, calculation-local package, script, or artifact:

1. prove all maintained imports and consumers use the selected owner directly;
2. prove historical recovery from exact Git objects and checksum graphs;
3. prove retained publication and evidence manifests remain valid;
4. run package, documentation, schema, checksum, and calculation-stage checks; and
5. request separate authorization for every destructive removal.

Remove no compatibility facade, retained wire decoder, historical artifact, branch,
worktree, or calculation data merely because the successor tests pass.

## Per-phase checks

Each implementation phase runs, at minimum:

- focused unit and integration tests for constructors, analysis, serialization,
  independent verification, tamper rejection, and authenticated rendering;
- direct-script AST checks and one fresh copied calculate → verify → render execution
  following [`direct-scripts.md`](direct-scripts.md);
- strict mypy over touched production and test files;
- Ruff and formatting checks;
- schema and canonical-wire checks where schemas are retained;
- exact-rational, directed-rounding, enclosure, and fail-closed checks for any formal
  certificate export;
- `compileall` for direct scripts;
- Sphinx with warnings treated as errors when public documentation changes;
- affected report or publication builds in scratch; and
- `git diff --check` plus retained-artifact digest checks.

Passing these checks establishes software behavior only. Scientific validation,
continuum convergence, evidence sealing, execution retention, publication, and release
remain separate scopes.
