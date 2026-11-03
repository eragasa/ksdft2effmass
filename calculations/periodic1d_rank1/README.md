# Periodic-1D rank-one context

**Status:** operation-first rank-one context with one local unsealed aggregate control

This calculation context owns periodic one-dimensional rank-one studies. Rank one has
no nontrivial internal unitary action on a scalar represented Hamiltonian, so this
context supplies the operator-trivial baseline for comparison with rank-two and
higher-rank periodic calculations.

## Model contract

`ksdft2effmass.periodic1d.rank1.model.blochhopping.Periodic1DRank1BlochHoppingModel`
binds an explicit periodic-1D lattice geometry to PhysKit's immutable ordinary-lattice
`DenseBlockHoppingModel`, fixes its scientific role as a parameterized `REDUCED_MODEL`,
enforces retained-space dimension one and exact Hermiticity, binds the physical scale
`E_a = hbar^2 / (m_e a^2)` without a factor `1/2`, and keeps
finite-DFT cyclic coefficients outside the ordinary model boundary. The calculation-owned [model research protocol](model/README.md) defines the canonical
\(R\)--\(k\) notation, parameter and unit contracts, conversion boundary, verification,
and claim exclusions. The source contract is documented in the
[architecture record](../../docs/architecture/v3/ksdft2effmass/periodic1d/rank1/model/blochhopping/index.md).

## Operation owners

- [`gauge_alignment/`](gauge_alignment/README.md) records the exact \(U(1)\)
  operator-trivial applicability boundary without manufacturing duplicate alignment
  cases.
- [`band_equivalence/`](band_equivalence/README.md) owns the retained scalar field and
  complete finite cyclic Fourier reconstruction.
- [`hopping_locality/`](hopping_locality/README.md) owns descriptive complete-coefficient
  and omitted-tail quantities before support removal.
- [`support_truncation/`](support_truncation/README.md) owns deliberate finite-support
  removal and its consequences.
- [`band_equivalence_hopping_locality/`](band_equivalence_hopping_locality/README.md)
  sequences the scalar control, Fourier reconstruction, locality, truncation,
  independent verification, and authenticated rendering.

Rank-one frame transport is not represented as a separate calculation operation because
phase transport cannot alter the scalar represented operator. If a future study evaluates
phase continuity itself, it must receive a separately reviewed operation owner rather
than being inferred from the present null control.

The staged implementation plan is maintained in
[`implementation.md`](implementation.md).

## Analysis order

The context follows the shared
[periodic analysis order](../periodic/multiband/analysis-order.md): establish the exact
parent, explicit lattice geometry, and scalar phase identity; reconstruct the complete
Fourier representation; measure descriptive locality; construct deliberate support
truncations; keep interpolation, truncation, and total errors separate; independently
verify admitted bytes; and render only verifier-authenticated values.

The current aggregate execution is explicitly unsealed and remains an illustrative
finite numerical control. The rank-owned hopping-locality and support-truncation
capabilities are implemented and tested, but their dedicated values are not yet serialized
as distinct retained execution artifacts. Nothing in this context establishes evidence
promotion, a global isolation theorem, material validation, publication acceptance, or a
software release.
