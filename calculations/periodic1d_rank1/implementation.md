# Periodic-1D rank-one implementation checklist

This checklist tracks completion of the operation-first rank-one calculation context.
Existing source classes or in-memory tests do not complete an item until the declared
wire, independent-verification, and calculation-owner boundaries are satisfied.

## 1. Rank-one periodic model contract

- [x] Establish the dimension-neutral, periodic-1D, rank-one, rank-two, and rank-N
  `model/blochhopping` ownership hierarchy.
- [x] Compose PhysKit's immutable `DenseBlockHoppingModel` rather than duplicating reusable
  lattice-model storage in KSD.
- [x] Bind an explicit periodic-1D lattice geometry and physical length unit.
- [x] Enforce one spatial dimension and retained-space dimension exactly one.
- [x] Fix the rank-one Bloch-hopping scientific role as `REDUCED_MODEL`; expose no
  caller-selected toy role.
- [x] Preserve the PhysKit energy unit, energy-reference identity, and ordered basis
  identity.
- [x] Define `lattice_kinetic_energy_scale = hbar^2 / (m_e a^2)` without a factor
  `1/2`, so `hbar = m_e = a = E_a = 1` in the reduced convention.
- [x] Require physical energy-dimensional coefficient units, reject `Unitless` and mixed
  units at the model boundary, and require explicit PhysKit conversion.
- [x] Require exact ordinary-lattice Hermiticity, including conjugate displacement pairs
  and an exactly Hermitian onsite block.
- [x] Define ordinary-lattice-only model semantics and explicitly exclude silent
  finite-DFT cyclic interpretation or conversion.
- [x] Add focused strict-type, rank, dimension, immutability, and Hermiticity tests.

## 2. Freeze the aggregate contract

- [ ] Freeze the explicit periodic-1D lattice geometry and units.
- [ ] Freeze the aggregate configuration identity and child-operation inventory.
- [ ] Freeze canonical output paths, schemas, digests, and claim boundaries.
- [ ] Preserve the existing Fourier-locality result bytes rather than silently changing
  their wire contract.

## 3. Gauge alignment

- [ ] Serialize the exact rank-one `operator-trivial` applicability result.
- [ ] Retain the explicit `U(1)` group identity and lattice geometry.
- [ ] Independently verify the applicability result without invoking its producer.
- [ ] Confirm that no synthetic non-Abelian alignment or frame-transport channels are
  emitted.

## 4. Band equivalence

- [ ] Bind the existing Fourier-locality producer under the exact rank-one
  band-equivalence owner.
- [ ] Preserve complete cyclic reconstruction and interpolation channels.
- [ ] Keep finite sampled agreement distinct from continuum equality.
- [ ] Admit the existing producer-independent reconstruction under the operation wire.

## 5. Hopping locality

- [ ] Define canonical serialization for the existing rank-owned hopping-tail results.
- [ ] Retain source calculation, source mesh, range, and lattice geometry by identity.
- [ ] Independently reconstruct complete coefficients and omitted-tail quantities.
- [ ] Confirm that hopping-locality analysis removes no support.

## 6. Support truncation

- [ ] Define canonical serialization for retained coefficients and truncated candidates.
- [ ] Retain source calculation, source mesh, range, and lattice geometry by identity.
- [ ] Independently reconstruct every declared support result.
- [ ] Keep interpolation, truncation-only, and total errors as separate channels.

## 7. Aggregate study

- [ ] Define an immutable aggregate request and aggregate result.
- [ ] Correlate exact child results by identity and authenticated digest.
- [ ] Apply adjacent-mesh and final `128 -> 256` refinement decisions.
- [ ] Apply threshold, first-joint-passage, and sustained-passage decisions.
- [ ] Independently verify the aggregate without calling any production analyzer.

## 8. Execution effects

- [ ] Implement a calculation workflow that writes each child result and the aggregate.
- [ ] Implement an independent-verification workflow that owns admitted result bytes.
- [ ] Implement authenticated visualization-data projection from passing verification.
- [ ] Render only the closed figure inventory from authenticated values.
- [ ] Preserve direct lifecycle no-overwrite behavior and atomic directory publication.

## 9. New aggregate execution

- [ ] Select a new aggregate execution identity; do not overwrite or mutate
  `direct-controlled-four-state-n256`.
- [ ] Run the calculation workflow.
- [ ] Run independent verification.
- [ ] Run authenticated rendering.
- [ ] Record the execution as an illustrative finite unsealed control.

## 10. Sealing

- [ ] Define sealing only after the complete aggregate package is stable.
- [ ] Implement read-only package verification over source, dependency, input, result,
  verification, and figure digests.
- [ ] Keep sealing distinct from scientific validation, publication qualification, and
  release status.

## Scientific execution order

- [x] Establish the ordinary-lattice rank-one model contract.
- [ ] Establish the exact ambient parent, retained-field construction, configuration,
  units, and lattice geometry.
- [ ] Establish rank-one gauge applicability.
- [ ] Calculate band equivalence and complete Fourier reconstruction.
- [ ] Calculate descriptive hopping locality before support removal.
- [ ] Calculate deliberate support truncation and its separate error channels.
- [ ] Assemble aggregate refinement and passage decisions.
- [ ] Independently verify all admitted bytes.
- [ ] Render only verifier-authenticated values.
