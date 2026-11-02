# Periodic-2D/3D calculation migration retirement audit

## Scope

This audit closes duplicate experiment-side execution surfaces after the maintained
calculation compositions were installed by merge commit
`a5fc0e99b8e4a91dfd3006692255b1acb522a03d`. It does not authorize or report a new
scientific calculation, retained execution, convergence claim, sealing action, or
evidence promotion.

The `calculations/` tree owns scientific protocols, executable composition, replaceable
output locations, retained execution packages when separately admitted, and
calculation-facing reports. Scoped `experiments/` locations now preserve legacy identity
and forward pointers only.

## Admission findings

The retirement audit found all 24 experiment-side executable entrypoints to have
calculation-owned successors:

| Family | Experiment-side entrypoints | Calculation owner |
|---|---:|---|
| Cross-dimensional comparison | 2 | `calculations/band-equivalence-dimensional-comparison/` |
| Periodic-2D orthogonal locality | 4 | `calculations/periodic2d/rank2/orthogonal/band-equivalence-locality/` |
| Periodic-2D hexagonal-metric locality | 4 | `calculations/periodic2d_rank2_hexagonal/band_equivalence_hopping_locality/` |
| Periodic-3D simple-cubic locality | 4 | `calculations/periodic3d_rank2_simple_cubic/band_equivalence_hopping_locality/` |
| Periodic-3D FCC/diamond locality | 4 | `calculations/periodic3d_rank2_fcc_diamond/band_equivalence_hopping_locality/` |
| Periodic-2D synthetic strain | 3 | `calculations/periodic2d_rank2_rhombic_path/band_equivalence_hopping_locality/` |
| Periodic-3D Bain path | 3 | `calculations/periodic3d_rank2_bain_path/band_equivalence_hopping_locality/` |

For the four locality families, the scientific code differs only in calculation-owned
output placement. For the dimensional comparison, the calculation successor reads the
four calculation-owned family definitions and writes under its own analysis tree. For
the strain studies, the calculation successors additionally use the current typed wire
names and canonical byte-writing route. No experiment-side executable has behavior that
is absent from its calculation successor.

The 28 experiment-side analysis README and ignore files describe the retired output
locations or invocation paths. Their calculation-owned counterparts document the current
output locations. They therefore retire with the duplicate entrypoints.

## Preserved legacy identity

Scoped `experiments/` READMEs preserve campaign identities and point to calculation
owners. The periodic-2D/3D rank-two protocols and applicable bibliographies are
calculation-owned. Shared periodic multiband parity and synthetic-strain donor protocols
are maintained under `calculations/periodic/multiband/`. Legacy files are not duplicate
protocol authority.

## Deletion inventory

The retirement removes 52 tracked duplicate files:

- 24 executable Python entrypoints;
- 12 locality-family analysis READMEs;
- 4 locality-family analysis ignore contracts;
- 4 synthetic-strain analysis READMEs;
- 6 synthetic-strain analysis ignore contracts; and
- 1 dimensional-comparison analysis README plus 1 ignore contract.

Git history preserves the exact predecessor bytes. No retained execution directory,
retained result, protocol, bibliography, scientific source module, or ignored calculation
output is deleted.

## Runtime and parity disposition

A parameterized temporary-tree regression executes all 19 JSON-producing
calculation-owned development writers covered by this retirement: nominal,
first-refinement, and second-refinement writers for four locality families; three writers
for each strain family; and the shell--scale decision-landscape writer. It checks that
every JSON output is emitted as nonempty bytes, is readmitted through its owning typed
record, and is reproduced as the same canonical bytes. The five retired render-only
entrypoints are not serialization writers and are covered by their calculation-owned
successors rather than this byte regression.

This is software-behavior and wire-format evidence only. The closure did not perform a
full-resolution predecessor/successor numerical comparison or image comparison. The
corresponding numerical-parity and image/data-parity checklist items remain open and no
convergence or scientific-validation claim is made.

## Required closure checks

The closure is complete only if:

1. no maintained consumer names a retired experiment-side executable or output path;
2. publication figure provenance points to the calculation-owned generator and output;
3. calculation and experiment READMEs state the split ownership consistently;
4. migration checklists identify calculation-owned protocol authority and legacy forward
   pointers explicitly; and
5. focused script, documentation-link, formatting, and source-consumer checks pass.

## Closure validation

At the earlier executable-retirement baseline, the bounded closure checks produced the
following software evidence; the later context-first protocol migration requires its own
focused checks:

- 122 focused band-equivalence/locality and dimensional-comparison tests passed,
  including all 19 JSON-producing calculation-writer cases and strict retained-refinement
  record admission checks;
- Ruff formatting and lint checks passed for 1,320 source and test files;
- mypy passed for 527 source files and for the new writer regression;
- the 84-source Sphinx build passed with warnings treated as errors;
- all 22 relative links added or changed across the 24 changed Markdown files resolved;
- the retired-path consumer search returned no maintained references to experiment-owned
  executables or output paths;
- the staged retirement inventory contained exactly the documented 52 deletions while
  the then-required experiment identity, protocol, and bibliography surfaces remained; and
- lock validation, bytecode compilation, and Git whitespace validation passed.

These checks establish the stated software migration behavior only. They do not establish
numerical convergence, scientific validation, retained-evidence status, or publication
acceptance.
