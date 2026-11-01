# Rank-specialization crosswalk

The finite-periodic transform, orthonormal frame transport, complex-unitary
Procrustes, interpolation, support-tail, and matrix-field diagnostic mechanisms are
not intrinsically restricted to the D1-v1 rank inventory. Their reuse does not make
distinct rank-specialized studies scientifically interchangeable.

| Boundary | Rank one | Rank two | D1-v1 higher-rank family |
|---|---|---|---|
| Retained gauge group | $U(1)$ phase | $U(2)$ | $U(r)$ for $r\in\{3,4,8,16\}$ |
| Represented-operator effect | A scalar represented Hamiltonian satisfies $U^\dagger H U=H$; the four gauge alignments therefore collapse at the operator level. | Non-Abelian basis changes can alter block locality while preserving spectra. | Non-Abelian basis changes are the object of the frozen rank/depth comparison. |
| Maintained scientific owner | `ksdft2effmass.periodic1d.fourier_locality` | `ksdft2effmass.periodic1d.composite_band_alignment` | `ksdft2effmass.periodic1d.rankN.band_alignment.composite` |
| Relationship to shared mechanisms | Uses the scalar Fourier-locality specialization rather than a degenerate matrix gauge-alignment inventory. | May reuse rank-generic orthonormal numerical mechanisms, but retains its own model, controls, tolerances, evidence identity, and verification contract. | Admits exactly ranks `3`, `4`, `8`, and `16` under the D1-v1 model and protocol. |
| Present disposition | Not admitted to D1 v1. | Not admitted to D1 v1 and not replaced by it. | Implemented producer inventory; independent verification and retained execution remain absent. |

## Why rank one remains separate

The D1 analytic model normalizes orbital and attack coordinates by $r-1$ and constructs
nearest-neighbor Givens rotations. Neither construction exists at $r=1$. This is not
merely an input-validation issue: a $1\times1$ Hermitian represented operator is
unchanged by its $U(1)$ basis phase. Treating identity, global-unitary,
pointwise-unitary, and known-inverse-oracle as four distinct operator-locality cases
would therefore misstate the scientific question.

## Why rank two is not added implicitly

The orthonormal matrix machinery is meaningful at $r=2$, but mechanically admitting
`2` to the D1 configuration would not reproduce the maintained rank-two study. The
D1 nearest-neighbor brickwork also degenerates at rank two because alternating layers
contain no pair to rotate. A rank-two use of shared mechanisms must bind the reviewed
rank-two model, mesh, tolerance, verification, and evidence contracts rather than
inherit D1-v1 values.

## D1-v1 inventory interpretation

The tuple `(3, 4, 8, 16)` is an intentional scientific and evidence boundary. It is not
a claim that Optimization's Procrustes solver, PhysKit's orthonormal transport, or the
finite-periodic transform kernels are numerically incapable of rank two. Changing the
D1 inventory would change protocol scope and canonical result bytes and therefore
requires a separately reviewed scientific decision.
