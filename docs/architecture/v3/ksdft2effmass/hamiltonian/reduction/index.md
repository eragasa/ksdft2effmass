# `ksdft2effmass.hamiltonian.reduction`

## Purpose and status

This implemented module reduces one finite Hamiltonian through one represented
spectral subspace and returns a correlated `ReducedHamiltonian`.

Source: `python/src/ksdft2effmass/hamiltonian/reduction.py`.

## Public contract

```python
reduction = SpectralReduction(
    hamiltonian=parent,
    spectral_subspace=subspace,
)
reduced_hamiltonian = reduction.reduced_hamiltonian
```

`SpectralReduction` is frozen, slotted, keyword-only, and eager. Construction performs
structural checks, combines the exact coordinate maps supplied by the retained
subspace with the parent Hamiltonian, and stores one immutable result. The
`reduced_hamiltonian` property returns
that result by identity. No numerical acceptance tolerance is applied.

## Coordinate contract

`SpectralSubspace` declares rectangular coordinate maps:

- `reduction_map`, with shape $M\times N$, maps parent coordinates to reduced
  coordinates; and
- `embedding_map`, with shape $N\times M$, maps reduced coordinates to parent
  coordinates.

Its projector is the related parent-space representation $P=RL$, not a substitute for
the two maps. Hamiltonian square-matrix validation remains with `Hamiltonian` and
`SpectralReduction`. This supports explicit oblique implementations without assuming
orthogonality.

For `OrthogonalSpectralSubspace` with basis $\Phi_M$,

$$
H_M=\Phi_M^{\mathsf T}H\Phi_M,
\qquad
H_M^{\mathrm{embedded}}=\Phi_M H_M\Phi_M^{\mathsf T}.
$$

Sparse parent input is multiplied directly and is not first densified. The declared
embedded result is dense because it represents the full parent-coordinate matrix.
Real and complex Hamiltonian quantities retain their scalar field and unit.

## Ownership boundary

The action does not solve eigenpairs, select retained dimension, compute norms, apply
acceptance thresholds, serialize results, or interpret physical adequacy. PhysKit owns
generic quantities and eigendecomposition; model-specific callers own selection and
acceptance.

## Evidence

Focused tests cover sparse real, dense complex, and explicit oblique reductions.
Passing them establishes implementation behavior only.
