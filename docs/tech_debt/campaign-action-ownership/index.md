# Periodic campaign Action ownership and module decomposition

## Status

**Safe to defer after the current canonical source moves, but before adding another
consumer or widening these APIs.** The affected synthetic campaigns retain typed,
immutable inputs and results, explicit scientific limitations, and focused regression
evidence. The debt concerns internal ownership clarity and maintainability; it does not
indicate a known change to retained bytes, formulas, tolerances, ordering, numerical
results, or scientific dispositions.

The row-063, row-064, and row-066 migration already completed two bounded corrections:

- historical `*Actionizer` class names were replaced by domain-specific Constructor,
  Resolver, Comparator, Analyzer, and Extractor names without compatibility aliases;
- canonical campaign imports no longer load `ksdft2effmass.campaigns.periodic_1d`.

Those corrections do not by themselves complete the deeper decomposition described
below.

## Current hotspots

### Continuum refinement

[`periodic1d/campaign/refinement/continuum/workflow.py`](../../../python/src/ksdft2effmass/periodic1d/campaign/refinement/continuum/workflow.py)
currently contains the versioned contracts, strict input adaptation, parent loading,
four numerical operation owners, provenance, result serialization, calculation
composition, and file Workflow in one module. In particular:

- `ContinuumHamiltonianConstructor.modes()` remains public static behavioral logic on a
  class namespace;
- `BoundSpectrumResolver` reaches back to that class-level operation to obtain Fourier
  labels;
- centered-mode ordering, Fourier-to-site reconstruction, Hamiltonian construction,
  spectrum resolution, state comparison, and operator-difference analysis do not yet
  share one explicit request-scoped representation-convention owner; and
- independent verification mechanics remain grouped with verification request/result
  contracts in the large `verification.py` module.

### Route reconciliation

[`periodic1d/campaign/reconciliation/route/workflow.py`](../../../python/src/ksdft2effmass/periodic1d/campaign/reconciliation/route/workflow.py)
currently groups closed contracts, strict decoding, baseline authentication, alignment,
real-space extraction, Bloch-fiber extraction, provenance, and Workflow composition.
`RealSpaceExtractor` and `BlochFiberExtractor` are numerically independent by design,
but their request, compatibility, and result boundaries should be easier to inspect
without traversing the complete campaign module.

### Finite-rank oracle reference shape

The canonical
[`periodic1d/campaign/oracle/finite_rank`](../../../python/src/ksdft2effmass/periodic1d/campaign/oracle/finite_rank/)
family already separates contracts, input decoding, parent data, numerical Actions,
comparison, independent reconstruction, verification, and Workflow composition. It is
a useful local shape for decomposition, but it is not a generic framework, base-class
hierarchy, registry, factory, strategy abstraction, or plugin point.

## Deferred correction

When these modules are next materially changed:

1. Split continuum-refinement contracts, strict input decoding, parent loading,
   numerical Actions, retained-result serialization, independent reconstruction, and
   Workflow composition into defining modules with reviewed facades.
2. Split route-reconciliation contracts, input decoding, baseline loading, alignment,
   route-specific extraction, provenance, and Workflow composition along the same
   domain boundaries.
3. Replace public static numerical behavior such as `modes()` with a cohesive
   instantiated owner or an immutable request-owned representation convention.
4. Pass exact ordered Fourier labels or a typed representation object explicitly to
   consumers rather than reaching through another operation class.
5. Introduce operation-specific immutable Requests and Results where they clarify
   state-space, ordering, unit, parent, and provenance boundaries; do not add wrappers
   that merely rename positional arguments.
6. Keep Results limited to intrinsic immutable structure and retained algebra. Do not
   make them replay private Action kernels or accept caller-supplied execution
   witnesses.
7. Keep `__post_init__` short and delegate cohesive intrinsic checks to named
   `_check_args_*` methods, consistent with the separate
   [post-init debt record](../post-init-validation-structure/index.md).
8. Preserve the deliberately independent production and verification numerical
   implementations.

## Preservation requirements

The correction must preserve:

- exact retained input and result bytes and their documented SHA-256 identities;
- closed schema fields, source authentication, confinement, and provenance boundaries;
- half-open grids, Fourier-mode ordering, seam orientation, transform normalization,
  energy references, units, and sign conventions;
- separate parent-model, discretization, finite-size, embedding, reduction,
  interpolation, sampling/aliasing, and comparison errors;
- independent real-space and Bloch-fiber route implementations;
- existing negative or unavailable scientific dispositions; and
- public exception taxonomy, binary64/complex128 overflow behavior, dense/sparse
  scaling documentation, and possible `MemoryError` boundaries.

No calculator execution, retained-artifact rewrite, dependency change, compatibility
alias, dynamic discovery, generic workflow engine, or scientific reinterpretation is
part of this debt.

## Completion criteria

This debt is complete when:

- each affected class is documented under its defining module in the architecture
  hierarchy and Sphinx API;
- public numerical behavior is owned by instantiated, request-scoped domain Actions;
- the large continuum and route modules are decomposed without circular or
  canonical-to-transitional dependencies;
- production and independent-verification implementations remain separate;
- focused and broader campaign tests, strict typing, Ruff, formatting, strict Sphinx,
  architecture-link checks, optimized-runtime tests, and import-independence gates
  pass; and
- retained content identities and scientific claim boundaries remain unchanged.
