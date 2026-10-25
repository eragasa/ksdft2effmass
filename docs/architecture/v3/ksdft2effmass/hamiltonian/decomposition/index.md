# `ksdft2effmass.hamiltonian.decomposition`

## Purpose and status

This implemented module owns one concrete reusable Hamiltonian-decomposition
composition.

Source: `python/src/ksdft2effmass/hamiltonian/decomposition.py`.

## Public contract

The package initializer exports only
[`HamiltonianDecomposition`](HamiltonianDecomposition/index.md), a concrete facade that
runs calculation, independent verification, and visualization in order. It consumes
the operators-owned `ReducedHamiltonian`. Its concrete runner, verifier, visualizer,
and result records remain module collaborators and are not package exports.

## Required composition

```text
HamiltonianDecomposition
├── ReducedHamiltonian
├── HamiltonianDecompositionRunner
├── HamiltonianDecompositionVerifier
└── HamiltonianDecompositionVisualizer
```

The facade performs:

```text
run → verify → visualize → correlate results
```

A failed verification stops before visualization. The correlated result retains the
calculation, verification, and immutable PNG visualization.

## Existing-owner relationship

The implemented low-level decomposition and retained model-class mathematics remain in
[`ksdft2effmass.analysis.operators`](../../analysis/operators/index.md). This module
composes those scientific owners with independent verification and visualization; it
does not copy their numerical kernels into a second implementation.

Scientific interpretation, numerical behavior, implementation detail, and schematics
are separated into neighboring pages.

## Explicit non-goals

This module does not introduce:

- an abstract base-class hierarchy;
- a plugin or registry mechanism;
- a generic calculation-study framework;
- directory-layout enforcement;
- execution identity, sealing, or publication policy;
- a replacement for model-specific scientific inputs; or
- PIAB1D-specific decomposition subclasses or stage classes.

## Evidence

The focused source tests exercise two- and three-dimensional represented Hamiltonians,
independent verification, rendering, numeric-control rejection, and the single-symbol
package export. Historical PIAB1D artifacts remain evidence of their original producer
state and were not rewritten by this source addition.
