# Periodic multiband development plan

## Purpose

The program asks how retained rank, spatial dimension, lattice geometry, internal basis structure, admissible alignment, and hopping support affect the joint recovery of spectra and represented operators. These axes must not be collapsed into one label.

## Plain-language progression

1. **One-dimensional rank-one null control.** Use the implemented scalar specialization with the same momentum, harmonic, energy, Fourier, mesh, support, and error conventions as the rank-two and higher-rank controlled family. Scalar phase conjugation leaves its represented Hamiltonian unchanged, so it is a locality baseline rather than a nontrivial alignment experiment.
2. **One-dimensional rank-two baseline.** Compare an unchanged retained spectrum with momentum-dependent rotations and measure the resulting hopping-locality cost.
3. **Two- and three-dimensional rank-two controls.** Repeat the comparison on orthogonal and nonorthogonal lattices while keeping retained rank equal to two.
4. **Synthetic geometry changes.** Separate geometry-only, frozen-response, and prescribed-response mechanisms along the two-dimensional rhombic and three-dimensional Bain paths.
5. **One-dimensional higher-rank calculation.** Compare retained ranks 3, 4, 8, and 16 and rotation depths 1, 2, 4, and 8 using a fixed retained subspace and real rotations.
6. **Moving retained subspaces.** Add projector motion only after its model, exterior-gap certificate, and verification contract are frozen.
7. **Complex internal transformations.** Add complex unitary transformations as a separately identified model class rather than treating them as evidence inherited from real rotations.
8. **Higher-rank two- and three-dimensional calculations.** Introduce these only after dimension-specific meshes, sewing, transport, support, resource, and verification rules exist.
9. **Cross-dimensional aggregation.** Compare only quantities with compatible definitions, normalization, sampling roles, and evidence status.
10. **Material-facing applications.** Keep first-principles and material validation outside the controlled-model program until separately authorized and evidenced.

## Rank-one boundary

The rank-one owner is [`calculations/periodic1d/rank1/fourier-locality/`](../../periodic1d/rank1/fourier-locality/). Its exact controlled four-state parent, lowest-ordered-eigenvalue scalar-field rule, Mathieu-compatible attained range/error--locality channels, separate interpolation/truncation/total-error semantics, exact finite meshes and supports, gates, tolerances, threshold, passage rules, and per-mesh attained error--complexity diagnostic are frozen and implemented through family-owned typed configuration and result wires, an independent verifier, authenticated rendering, and three direct stage scripts. The provisional in-memory development control reports all 725 named comparisons passing. No retained input, result, verification, figure, or execution directory exists, and no evidence promotion has occurred. The retained Mathieu1D package remains a separate periodic-potential benchmark and does not serve as this compatible specialization.

For a scalar represented Hamiltonian, global, pointwise, and known-inverse phase alignments are operator-identical. They must be marked inapplicable as distinct alignment channels rather than emitted as duplicated numerical results.

## Current higher-rank alignment controls

The current one-dimensional design compares four controls:

- **no alignment** — retain the attacked representation unchanged;
- **one global alignment** — fit one transformation and use it at every momentum;
- **pointwise alignment** — fit a separate complete transformation at each momentum;
- **known-inverse control** — use the exact generating inverse as an oracle diagnostic.

A future restricted-circuit fit is planned but has no selected optimizer or certificate policy. The oracle control is not evidence that a practical fitting method can recover the same transformation.

## Execution gates

A new calculation branch requires, in order:

1. an explicit model and input inventory;
2. construction and independent evaluation meshes;
3. qualification and failure rules;
4. producer output records;
5. producer-independent verification;
6. analysis inputs restricted to verified simulation results;
7. analysis verification and plotting contracts;
8. a calculation-owned technical report; and
9. a separately authorized retained run if evidence promotion is desired.

No empty dimensional packages or placeholder stage scripts should be created before these contracts exist.
