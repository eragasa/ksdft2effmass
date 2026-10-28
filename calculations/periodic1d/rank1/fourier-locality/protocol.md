# Rank-one single-band Fourier-locality protocol

**Lifecycle:** frozen controls and typed calculate → independently verify →
authenticated render implementation complete; provisional in-memory development control
passed; no retained execution or evidence promotion has occurred.

## Question

What Fourier interpolation and hopping-support truncation behavior does a scalar periodic retained Hamiltonian exhibit when evaluated under conventions compatible with the rank-two and higher-rank controlled families?

## Frozen parent and compatibility conventions

The scalar field is

\[
H(q)=\lambda_0(K(q)),\qquad
K(q)=T_0+e^{2\pi iq}T_{+1}+e^{-2\pi iq}T_{+1}^{\dagger},
\qquad -\tfrac12\le q<\tfrac12,
\]

where `λ₀` is the least ordered eigenvalue of the Hermitian fiber on the standard
`C⁴` basis and the parent hopping scale is exactly one. No homotopy-scale sweep belongs
to this rank-one control. The immutable parent identity is
`ksdft2effmass.periodic1d.controlled-four-state-parent.v1`. Its exact rational
coefficients, displayed matrices, and rejected alternatives are recorded in
[`scientific-control-decision.md`](scientific-control-decision.md). The exact positive
energy reference is `E_ref = 1`; parent matrix entries are exact dimensionless ratios to
that reference, while `K(q)` and `H(q)` have energy units `E_ref`.

The parent has exact ambient Fourier support `{-1, 0, 1}`. That fact does not imply
finite support of its lowest eigenvalue field. The momentum convention, forward negative
exponent, inverse positive exponent, forward factor `1/N`, and centered Born--von Karman
representatives follow the cross-rank convention in
[`donor-crosswalk.md`](donor-crosswalk.md).

## Frozen range and error-channel semantics

For each construction mesh `Q_N`, disjoint evaluation mesh `E_M`, and ordinary support
`S_R`, let `I_N` be the complete cyclic interpolant and `T_{N,R}` its deliberate
transform-mediated support truncation. The three distinct maximum-error channels are

\[
e_{\mathrm{int}}(N,M)=\max_{q\in E_M}|H(q)-I_N(q)|,
\]

\[
e_{\mathrm{trunc}}(N,R,M)=\max_{q\in E_M}|I_N(q)-T_{N,R}(q)|,
\]

and

\[
e_{\mathrm{tot}}(N,R,M)=\max_{q\in E_M}|H(q)-T_{N,R}(q)|.
\]

The pointwise residuals telescope, but these three maxima are not added. Independent
verification checks only the triangle inequality
`e_tot <= e_int + e_trunc` in addition to reconstructing every channel directly.
`e_int` is constant across `R` for fixed `N` and `M`; truncation and total errors are
support-indexed. Threshold and first-passage decisions use total error, never truncation
error.

The Mathieu-compatible attained range/error--locality table also retains, per `R`, the
omitted-block L2 norm, equal-weight direct-fit total error, and direct-versus-mediated
coefficient and sampled defects. The direct-fit route is separate: its residual is not
an interpolation or transform-truncation channel.

## Frozen finite controls

[`numerical-control-decision.md`](numerical-control-decision.md) freezes the exact mesh
point sets, all integer supports `0,...,15`, sampled gap gate, mixed consistency rule,
final construction-mesh stability gate, `1e-8 E_ref` application threshold, passage
semantics, finite two-objective error--complexity mask, and closed authenticated figure
inventory. The mask minimizes `(2*R + 1, e_tot(N,R))` separately for each construction
mesh; direct-fit and other diagnostic channels are not substituted as objectives.

The sampled gap is a finite qualification, not a global isolation theorem. Eigenvalue
samples, transform coefficients derived from them, interpolation and truncation errors,
and first-passage outcomes remain finite numerical quantities unless separately enclosed
by a proposition-specific certificate. No runtime Formal certificate is part of Phase 2.

## Implemented typed contracts

The family-specific immutable configuration binds the exact parent identity and rational
coefficient inventory. Correlated frozen result records store each authoritative value
once. Independent verification reconstructs the finite parent, transform, truncation,
direct fit, decision masks, refinement semantics, sampled-gap minimizer, and verifier-
derived visualization projection without invoking the production analyzer. Canonical
JSON bytes are the result wire and the verifier's exact subject. The closed renderer
admits only passing verification and the exact authenticated projection. No retained
execution exists.

## Rank-one alignment boundary

Only the no-alignment scalar channel is scientifically distinct. The following higher-rank alignment controls are inapplicable as separate represented-operator calculations:

- one global phase alignment;
- pointwise phase alignment;
- known-inverse phase control; and
- restricted internal rotation circuits.

They must be encoded as inapplicable, not emitted as duplicate numerical channels.

## Direct contract

1. `run_01_calculation.py` composes the approved typed configuration and writes one
   correlated scalar-locality result containing each authoritative value once;
2. `run_02_verification.py` owns the exact result bytes, independently reconstructs the
   parent, transform, truncation, fit, error, applicability, and first-passage channels,
   and derives an authenticated visualization projection; and
3. `run_03_render.py` admits only the passing typed verification and exact projection,
   then publishes the closed native figure inventory atomically.

There is no separate workflow or calculation-local analysis stage. Reusable analysis
belongs to installed domain owners, while rendering calculates no new scientific values.
The scripts implement these frozen contracts but have not been run as a retained
execution.

## Evidence boundary

A future separately authorized retained run may establish only the declared finite-mesh
scalar results after provenance and sealing review. The current provisional in-memory
result does not establish retained evidence. Neither lifecycle establishes a global
isolated band, higher-rank gauge behavior, continuum convergence, material applicability,
or validation of Mathieu1D. Evidence promotion requires separate authorization.
