# Five-scale maintenance disposition

**Decision date:** 2026-10-31
**Disposition:** retain as maintained calculation surfaces

Scientific authority has selected the maintenance alternative identified by
[`scientific-claim-use-audit.md`](scientific-claim-use-audit.md). The unmatched
five-scale parent-family, truncation, refinement, and diagnostic surfaces remain part of
the maintained calculation at
`calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/`.

## Maintained scope

The decision retains:

- the five parent hopping scales `0.0`, `0.25`, `0.5`, `0.75`, and `1.0`;
- the five-scale parent-family final-mesh and adjacent-mesh summary channels;
- the 2,805-row truncation-consequence inventory across all five scales;
- the threshold-adjacent truncation-refinement inventory at construction meshes 128,
  256, and 512;
- the claimed diagnostic quantities and calculation-owned figure compositions that
  consume those values; and
- the current development entrypoints and tests as maintained calculation
  compositions over installed scientific owners.

The tracked result and figure bytes remain unchanged. This decision does not rerun or
upgrade them.

## Ownership and migration consequence

The calculation root remains the maintained composition owner. Reusable scientific
behavior should migrate to cohesive installed owners under
`python/src/ksdft2effmass/periodic1d/band_equivalence_locality/`; calculation-local
scripts should retain only composition, effect adapters, and presentation wiring.

The existing `workflow/` tree remains a tracked donor while its still-maintained
scientific capabilities and consumers are replaced. Its pandas implementation, dataframe
API, and pandas dependency are not maintained requirements and need no one-to-one
successor. The donor is not approved for retirement or deletion while live consumers or
unmigrated scientific semantics remain. A later retirement review must demonstrate named
successor ownership, consumer migration, and parity for the maintained scientific scope.

## Evidence boundary

Maintenance is not evidence promotion. In particular, this decision does not:

- make the development tables or figures part of direct v2;
- authenticate the four truncation scales absent from direct v2;
- convert donor momentum convergence into the installed broader momentum disposition;
- establish continuum convergence, scientific validation, or material relevance;
- seal or promote either retained execution;
- authorize a new calculation or overwrite an existing result; or
- authorize publication, release, donor deletion, or dependency changes.

Any future retained execution covering the maintained five-scale scope requires a new
immutable execution identity, reviewed controls, and separate execution authorization.
Direct v1 and v2 must remain unchanged.

## Required follow-on work

1. Port the five-scale adjacent-mesh summary and truncation-family behavior to named
   installed owners without weakening the broader momentum diagnostic.
2. The claimed diagnostic semantics and figure inputs now have a typed
   calculation-local successor in `development_diagnostics.py`. It preserves the CSV
   column contracts and separate scientific channels without preserving the pandas
   dependency, dataframe interface, or donor implementation.
3. Consumer migration is complete at the source-import boundary. Five scientific
   producer entrypoints and three producer tests compose installed routes through
   `development_study.py`; diagnostic packaging and its test consume immutable CSV
   projections and canonical typed records. No maintained Python consumer imports
   `workflow/`. This source migration did not rerun or modify historical artifacts,
   extract donor schemas, or add a competing wire format.
4. Source integrity and complete-grid internal consistency are now bound in
   [`five-scale-consistency.md`](five-scale-consistency.md): exact
   source digests, all 2,805 truncation rows, all 495 refinement rows, derived
   summaries, and stored cutoff decisions are covered without rerunning a calculation.
   This does not establish the missing retained numerical parity or turn the earlier
   18,513-value direct-v2 overlap into full retained coverage.
5. Ragasa2026a v3 now distinguishes the historical donor's narrower `converged`
   summaries from the installed broader unresolved outcome, and it identifies passing
   unsealed direct v2 as partial active-family evidence that does not authenticate the
   unmatched five-scale development figures.
6. Implement the installed five-scale aggregate owners and obtain separate execution
   authorization under
   [`complete-five-scale-execution-plan.md`](complete-five-scale-execution-plan.md).
   Conduct a new reviewed retirement audit only after the retained numerical and
   momentum-semantic gaps are resolved, and before any donor removal.
