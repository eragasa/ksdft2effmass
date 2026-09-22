# Stage B implementation blocker: twist gauge and bare D4 covariance

## Status

Execution-free implementation exposed a mathematical incompatibility in the
accepted Stage B contract before the accepted scalar parent was read or
executed. Stage B implementation is incomplete and Stage B execution remains
unauthorized. The finding comes from authored nearest-neighbour toy
coefficients and is not a scientific or material result.

The blocking decision is represented by
`.pi/checkpoints/research-monograph-impurity-defect-2d-stage-b-twist-gauge.json`.

## Conflicting frozen requirements

The accepted design simultaneously requires:

1. the generic base twist $(0.37,-0.23)$;
2. componentwise reduction of every transformed twist to $[0,1)$;
3. the bare site permutation
   $U_M|s\rangle=|Ms\bmod8\rangle$; and
4. exact full-Hamiltonian covariance
   $H(M\phi\bmod1)=U_MH(\phi)U_M^\dagger$.

These statements do not determine a consistent finite-matrix gauge. Even the
identity operation reduces $(0.37,-0.23)$ to $(0.37,0.77)$. Those twists label
the same boundary-condition fibre, but their matrices are related by a
site-dependent gauge transformation rather than by the identity matrix in a
uniform-link representation.

A seam-periodic representation makes twists invariant under integer shifts,
but a rotation moves the seams. Its full Hamiltonian is therefore related by a
twist-dependent gauge-decorated symmetry, not by the frozen bare site
permutation. A uniform-link representation has exact bare-permutation
covariance for an unreduced lift $M\phi$, but replacing that lift by
$M\phi\bmod1$ again introduces a nontrivial diagonal gauge.

## Toy behavioral evidence

A deterministic $8\times8$ nearest-neighbour scalar toy parent was used; it did
not read the accepted periodic-2D parent or the accepted Stage A result.

- In a uniform-link representation, bare-permutation covariance is exact for
  the unreduced lift $M\phi$.
- Reducing the identity-transformed generic twist from $(0.37,-0.23)$ to
  $(0.37,0.77)$ produces a nonzero maximum-entry matrix mismatch (about
  $7.65\times10^{-1}$ for unit toy hopping).
- In a seam-periodic representation, componentwise twist reduction is exact,
  but bare quarter-turn covariance has a nonzero maximum-entry mismatch (about
  $1.32$ for unit toy hopping).

The magnitudes are illustrative software-test observations only. Their role is
to demonstrate that the mismatch is structural and far above the frozen
$10^{-10}$ covariance tolerance; they are not retained Stage B evidence.

## Decision boundary

The implementation cannot select a twist gauge by convenience because the
choice changes the mathematical covariance operator and retained metadata. The
human-owned choices are:

- use a centred twist representative with a uniform-link gauge and retain bare
  site-permutation covariance;
- retain $[0,1)$ representatives and use a twist-dependent gauge-decorated
  covariance unitary; or
- retain both reduced metadata and an explicit unreduced lift, with covariance
  evaluated in the lifted uniform-link gauge.

No runner, verifier, or test may present any of these as the accepted Stage B
contract until the checkpoint is resolved.
