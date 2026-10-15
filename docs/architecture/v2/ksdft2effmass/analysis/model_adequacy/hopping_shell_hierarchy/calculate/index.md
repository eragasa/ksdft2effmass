# `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.calculate`

## Purpose and status

Prospective pure producer module for HSH-1. No source module or calculated HSH-1 result
exists.

## Prospective public contract inventory

- [`Periodic2DHoppingShellHierarchyCalculator`](Periodic2DHoppingShellHierarchyCalculator/index.md) — stateless ActionObject whose `execute(definition)` method returns one immutable hierarchy result.

Orbit generation, source projection, quadratic restriction, bounded convex feasibility,
feasible-pair construction, candidate separating directions, conservative support
bounds, hierarchy resolution, and withheld evaluation are private cohesive behavior of
the calculator unless later review identifies a separately reusable domain owner.

## Represented action

The ActionObject maps one complete frozen definition to one deterministic result. Its
codomain contains no file handles, mutable arrays, optimizer instances, or serialized
bytes. It performs no external execution.

## Invariants and failure behavior

Execution fails before producing a result if top-level source projection, orbit
coverage, definition, or nesting premises are invalid. A class-local quadratic or
certificate premise failure may instead be retained explicitly as `invalid-premise`,
with no distance or hierarchy conclusion. An inability to decide valid nonempty
geometry is `unresolved-nonempty`; neither state may be presented as separation.

## Dependencies and neighboring owners

`definition` owns controls; `results` owns HSH proof/result invariants;
`analysis.model_adequacy.losses` owns normalized dimensionless completed-square storage
and evaluation; `serialization` owns HSH wire mechanics; and `verify` owns independent
reconstruction. The analysis package may consume `periodic2d` and NumPy/SciPy but cannot
call the verifier to manufacture confidence.

## Class navigation

- [`Periodic2DHoppingShellHierarchyCalculator`](Periodic2DHoppingShellHierarchyCalculator/index.md)

## Prospective code mapping

| Planned path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/calculate.py` | Module | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.calculate` | HSH-1 producer algorithms |
| same | Class | `...calculate.Periodic2DHoppingShellHierarchyCalculator` | Pure ActionObject |

## Test mapping

Planned software and numerical test owners and exact intended behaviors are listed in
[testing](../testing.md). No mapped test exists.

## Sphinx mapping

No Sphinx page exists. The intended page is
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license; algorithmic obligations derive from
the HSH-1 draft protocol.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Producer is not implemented | None |
| Numerical verification | Not evaluated | No oracle comparison or execution | None |
| Scientific validation | Not evaluated | Synthetic parent | None |
| Uncertainty quantification | Not evaluated | Thresholds are benchmark controls | None |
| Human acceptance | Not evaluated | No frozen confirmatory run | None |

## Limitations and deviations

The convex solver and outward-rounding backend are intentionally unspecified pending
pre-freeze review. Their identity will be explicit configuration, not hidden global
state.
