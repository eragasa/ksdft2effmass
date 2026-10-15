# `Periodic2DHoppingShellHierarchyResult`

## Purpose and status

Prospective immutable top-level ResultObject for HSH-1. It is not implemented or
supported.

## Public contract

The object exposes the definition/source identity, projected-target diagnostics, fixed
metric, ordered tuple of class results, first class with a verified common witness, and
an optional certified minimum tested compatible class. It also retains hierarchy-level
limitations and explicit nonclaims.

Planned supported route:
`ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.Periodic2DHoppingShellHierarchyResult`.

## State and identity

Stable identity includes definition identity and exact source digests. Class results
appear exactly once in the frozen increasing shell order. The result retains source
projection defects and common metric coefficients rather than relying on an implicit
reconstruction convention.

## Invariants and failure behavior

The object enforces:

- complete one-to-one class coverage and exact nested active masks;
- a single common maximal-space metric and coefficient normalization;
- nonincreasing exact set-distance semantics without demanding nonoverlap of loose
  reported intervals;
- exact correlation of any first-witness class;
- certified minimality only when that class has a common witness and every smaller
  class is channel-empty or certified separated;
- no minimality when a smaller class is unresolved or invalid; and
- inherited compatibility of larger classes through exact witness embedding, without
  overwriting their independently retained diagnostics.

An invalid top-level source or nesting premise prevents construction. A class-level
`invalid-premise` is retained fail-honestly and blocks hierarchy conclusions.

## Dependencies and collaborators

The result composes ordered `Periodic2DHoppingShellClassResult` objects. The serializer
encodes it; the verifier reconstructs it. It cannot execute or access files.

## Data and action flow

Per-class results are assembled in frozen shell order, hierarchy logic is applied once,
and the complete immutable result is returned for verification and serialization.

## Serialization and compatibility

Schema v1 retains all class results and hierarchy logic explicitly. A future additional
class, changed shell ordering, or changed minimum-class semantics creates a new
definition and potentially a new schema version.

## Scientific and numerical boundary

Any minimum claim is explicitly “smallest tested compatible class under the frozen
problem definition.” The result cannot claim a physical minimum range, material
validity, or asymptotic locality.

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/results.py` | Class | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.results.Periodic2DHoppingShellHierarchyResult` | Top-level hierarchy result |

## Test mapping

Planned tests mutate class order, shell masks, metric normalization, first witness,
smaller-class dispositions, critical shell, inherited witnesses, and nonclaims. No test
exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | ResultObject absent | None |
| Numerical verification | Not evaluated | HSH-1 unexecuted | None |
| Scientific validation | Not evaluated | Synthetic hierarchy | None |
| Uncertainty quantification | Not evaluated | No uncertainty model | None |
| Human acceptance | Not evaluated | No accepted result | None |

## Limitations and deviations

The hierarchy-level wire vocabulary is not final. The object will retain bounded
results even when no minimum-class conclusion is available.
