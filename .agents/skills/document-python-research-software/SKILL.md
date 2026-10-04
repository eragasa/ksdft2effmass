---
name: document-python-research-software
description: Document and review Python research software for scientist readers across source structure, NumPy-style docstrings, explanatory inline comments, validation decomposition, public API references, concepts, and architecture. Use for documentation-only work and for implementation changes that require these surfaces to remain synchronized with scientific assumptions, invariants, units, provenance, or model and representation boundaries.
---

# Document Python Research Software

Apply one scientist-facing documentation standard across implementation, tests, public
API pages, concepts, and architecture. Documentation must expose scientific meaning and
software boundaries without inventing scientific authority.

## Establish authority and scope

Before changing behavior or documentation:

1. Read the repository instructions and the relevant authoritative specifications,
   research assumptions, architecture documents, implementation, and tests.
2. Identify the exact files and public objects in scope.
3. Record whether each object is a scientific model, mathematical object, finite
   representation, retained space or operator, represented operator, effective model,
   campaign record, or supporting software owner.
4. Treat the authoritative project documents as controlling when this skill conflicts
   with a local convention.

Do not infer scientific identity, compatibility, alignment, role, or meaning from shape,
rank, coefficients, spectrum, route names, or perturbation structure.

## Structure source for scientific readability

Keep immutable data in cohesive DataObjects and executable behavior in cohesive Actions.
Do not introduce generic helpers, registries, factories, plugins, discovery mechanisms,
structural fallbacks, or compatibility aliases merely to simplify documentation.

For every new or materially changed `__post_init__` method:

- keep the entry point short;
- delegate distinct invariant families to documented, cohesive `_check_args_*`
  methods;
- preserve validation order and exception behavior unless behavior change is authorized;
- use exact public-boundary checks when the contract rejects booleans, numeric strings,
  coercible scalars, or semantic substitutes; and
- avoid both one large validation block and a proliferation of one-line check methods
  with no meaningful invariant boundary.

Name each check after the scientific or software invariant it protects. Do not use vague
names such as `validate`, `check_data`, or `ensure_valid`.

## Write scientist-facing source documentation

Use NumPy-style public docstrings. Document, as applicable:

- modeled subject and semantic category;
- mathematical definition or equation;
- basis, gauge, geometry, ordering, and state-space conventions;
- units, scalar types, shapes, and energy reference;
- parent identity and provenance;
- exactness, approximation, and truncation boundaries;
- the distinction among projection, disentanglement, basis transformation, and
  truncation;
- separate parent-model, numerical or discretization, and model-reduction errors unless
  an authoritative source defines their relationship;
- intrinsic invariants and validation failures;
- parameters, attributes, returns, and raised exceptions; and
- the distinction between software verification and scientific validation.

Add inline comments where a scientist would otherwise have to reconstruct intent from
implementation mechanics. Good comments explain:

- why a convention or invariant is required;
- how an equation maps to indices, coefficients, or matrix blocks;
- why an omitted value is exact zero rather than missing data;
- why two spaces or operators must be aligned before comparison or composition;
- where exactness ends and numerical approximation begins; and
- why provenance or component identity must remain separate after composition.

Place comments immediately before the relevant operation. Do not restate syntax, narrate
every assignment, impose a comment quota, or use comments to excuse unclear structure.
Prefer a well-named method or object when it can express the same idea precisely.

## Preserve scientific and provenance boundaries

Keep scientific models, finite parent representations, retained spaces, retained
operators, represented operators, comparisons, campaign results, and effective models
separate in both code and prose.

Preserve numerical inputs, payload bytes, identifiers, digests, reports, figures,
provenance, and retained artifacts. Do not overstate test results, numerical checks,
convergence, theorem status, literature support, uncertainty quantification, or
scientific validation.

When a type name is historically misleading, explain its actual ownership explicitly;
do not silently reclassify it from its shape or suffix.

## Synchronize documentation surfaces

Keep these surfaces consistent when they are relevant to the changed public contract:

- source docstrings and supported imports;
- tests and fixtures;
- Sphinx API pages and navigation;
- concept documentation;
- canonical architecture package, module, class, and applicable detail pages with their
  exact code, test, and Sphinx mappings;
- affected architecture decisions, inventories, and migration crosswalks;
- schemas and examples; and
- calculation or provenance documentation.

Use reStructuredText for existing `.rst` files, MyST Markdown for existing `.md`
files under Sphinx documentation, and Markdown under `docs/`. Do not modify a
manuscript unless explicitly authorized.

## Validate proportionately

Run the cheapest affected checks first, then broader checks proportionate to the change.
Include, as applicable:

1. inspection of `python/pyproject.toml` and relevant test configuration before choosing
   commands;
2. focused behavioral and invariant tests;
3. formatting and linting;
4. static typing;
5. broader affected test groups;
6. Sphinx with warnings treated as errors;
7. project-defined local-link checks for changed documentation;
8. retained checksum verification; and
9. `git diff --check`.

Do not weaken assertions, expected values, tolerances, or coverage to obtain a pass.
Generated documentation output must not remain in the repository.

## Apply an independent review gate

Before recommending a commit, obtain a fresh-context, read-only independent code-smell
review. Use a delegated reviewer only when that capability is available and explicitly
authorized. If no independent review route is available or authorized, stop with
`REVIEW_INCONCLUSIVE` and ask the operator to arrange or authorize one; never
self-certify independence. The review must inspect the current diff rather than an
earlier snapshot and assess:

- scientific category and ownership boundaries;
- immutability and DataObject/Action cohesion;
- `__post_init__` decomposition and invariant documentation;
- usefulness and accuracy of inline scientific comments;
- public imports, retired names, aliases, and stale references;
- consistency among source, tests, API, concept, and architecture documentation;
- scientific overclaiming; and
- unnecessary abstraction or duplication.

Classify findings as `MUST_FIX`, `HUMAN_DECISION_REQUIRED`, `SAFE_TO_DEFER`, or
`NO_ACTION_REQUIRED`. Correct valid blockers and ask the same reviewer to verify only
the corrections. End with exactly one outcome: `CHANGES_REQUIRED`,
`REVIEW_INCONCLUSIVE`, or `NO_BLOCKING_FINDINGS`.

## Report and stop at the authorization boundary

Report changed paths, validation commands and results, assumptions, review outcome, and
residual limitations. Passing checks establish software behavior only.

A documentation or review task does not authorize commits, pushes, pull requests,
merges, cleanup, releases, publication, destructive operations, dependency addition or
replacement or relicensing, transmission of private, restricted, or unpublished data,
production Quantum ESPRESSO or Wannier90 execution, remote or external computation, or
changes to scientific authority. It also does not authorize any other protected action
defined by repository instructions. Request each protected next operation separately.
