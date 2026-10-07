# AGENTS.md

## Project

`ksdft2effmass` is open-source research software for constructing and evaluating
reduced semiconductor Hamiltonians from first-principles Kohn–Sham DFT
calculations. Quantum ESPRESSO owns electronic-structure calculations and
Wannier90 owns Wannier localization; this package must not reimplement either.

Authoritative project surfaces are:

| Subject | Location |
|---|---|
| Physical and mathematical definitions | `specification/` |
| Scientific assumptions | `docs/research/` |
| Computational procedures and provenance | `docs/computational/`, `calculations/` |
| Python source | `python/src/ksdft2effmass/` |
| Python dependency declarations | `python/pyproject.toml` |
| Resolved Python dependencies | `python/uv.lock` |
| Architecture | `docs/architecture/` |

Read the relevant authoritative files before changing behavior. Do not create a
competing source-tree layout.

## Scientific integrity

Never fabricate or overstate numerical results, completed calculations,
convergence, validation, literature values, references, or software
capabilities. Distinguish calculated results, literature values, expected
behavior, illustrative examples, synthetic test data, placeholders, and
proposed work. Passing software tests establishes software behavior only; it
does not establish scientific correctness or validation.

Preserve the mathematical conventions in `specification/`. In particular:

- distinguish physical models, mathematical operators, and finite matrix
  representations;
- identify and align state spaces before subtracting operators;
- state basis, gauge, energy reference, units, and geometry conventions;
- distinguish projection, disentanglement, basis transformation, and
  truncation; and
- keep parent-model, numerical/discretization, and model-reduction errors
  separate unless their relationship is explicitly defined.

If an authoritative specification is ambiguous and the ambiguity materially
blocks the requested work, report it rather than choosing a convention by
preference.

## Protected actions

Obtain explicit human authorization before:

- production Quantum ESPRESSO or Wannier90 execution;
- remote, cluster, cloud, or other external computation;
- deleting calculation data or rewriting Git history;
- transmitting private, restricted, or unpublished project data;
- adding, replacing, or relicensing a dependency; or
- merging to `main`, publishing a package, creating or moving a version tag,
  creating a release, archiving software or data, or updating a DOI.

Before an authorized expensive calculation, report the executable, input
system, expected scale and outputs, and anticipated runtime/resources when
known. Do not change pseudopotentials, exchange-correlation approximations,
cutoffs, meshes, tolerances, crystal structures, Wannier windows/projections,
or energy-alignment conventions without applicable scientific authority.

`dev` is provisional active development. `main` is the latest reviewed
snapshot associated with a formal research output. Only signed semantic-version
tags identify reviewed software releases.

## Data and provenance

Do not commit large wavefunction, density, restart, scratch, or dense-matrix
outputs. Retain compact inputs, checksums, software versions, settings,
reproduction scripts, and status summaries. Never place credentials, keys,
tokens, scheduler secrets, private data, or restricted data in the repository.

Historical files in `.pi/checkpoints/` are retained because calculations and
provenance records identify exact checkpoint paths and hashes. Treat this
directory as an immutable provenance archive, not an active task or agent
control system. Do not move, rewrite, or delete these records unless every
bound calculation and checksum contract is explicitly migrated with human
authorization.

## Software design

Keep nontrivial behavior with its domain owner. Maintained data and result
objects must be operationally immutable. Use explicit types; do not introduce
`typing.Any` or use `object` as an unspecified software boundary. Public numeric
APIs must reject booleans and numeric strings unless their contract explicitly
accepts them, and must document scalar types, units, and overflow behavior.

Reusable behavior belongs to a cohesive domain object or action object; wire
mechanics belong to serializers. Avoid generic `Helper`, `Utils`, `Manager`,
`Handler`, or `Processor` containers. Supported public imports must be deliberate
and documented.

Code-smell reviews must flag caller-supplied “private” evaluation witnesses that can
bypass request/result correlation, and bespoke `object.__new__` plus
`object.__setattr__` field-population blocks that bypass maintained-object
constructors or invariants. Actions own request-to-value derivation; Results validate
intrinsic immutable invariants and must not replay an expensive Action merely to imply
that manual construction has authenticated provenance. Require explicit Action oracle
tests and state that manual Result construction is not evidence that the Action ran.

PhysKit owns the reusable lattice primitives imported by this package. Reusable
finite-periodic capabilities that remain local may stay until a separately reviewed
migration; do not duplicate them across repositories. This repository owns its
campaign, provenance, threshold, schema, route-reconciliation, and retained-result
policy. PhysKit must not depend on `ksdft2effmass`.

## Tests and documentation

Inspect `python/pyproject.toml` and relevant tests before choosing commands. Run
the cheapest affected checks first, then broader checks proportionate to the
change. Do not weaken expected values, tolerances, or test coverage merely to
obtain a pass.

Follow the structure used by nearby tests. New test modules should group tests
beneath one cohesive `Test...` class; do not restructure unrelated modules solely
for style. Tests should establish one named behavior with explicit tolerances where
applicable. Use framework temporary directories only for runtime scratch; maintained
resources belong under the relevant test tree.

Use reStructuredText for `.rst` files and MyST Markdown for existing `.md` files under
`doc/sphinx/`; use Markdown under `docs/`. Keep public source, tests, schemas,
examples, and documentation consistent. Build Sphinx with warnings treated as errors
when documentation changes.

## Working procedure

1. Inspect the current branch, worktree, relevant files, and uncommitted changes.
2. Make the smallest in-scope change and preserve unrelated work.
3. Run proportionate checks.
4. Report changed paths, checks, assumptions, and residual limitations.

Do not commit or push unless the current human instruction explicitly requests
it. Do not perform release, publication, protected execution, destructive
operations, history rewriting, or force-pushing without explicit authority.
