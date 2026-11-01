# Prospective composite-band alignment and locality protocol

## Status

This is the publication-independent direct successor to the historical Conference Paper
1 `M2` protocol. It freezes the parity-preserving scientific and numerical meaning
implemented by the typed calculate → independently verify → authenticated render
lifecycle. It is not an immutable experiment version and records no new retained run or
evidence.

The historical files and checksums under
`calculations/ICMSEP2026/conference/paper_1/multiband-alignment/` remain unchanged.

## Parent and state spaces

The selected parent is the exact finite four-dimensional Hermitian periodic-one-
dimensional block-hopping model retained by the historical protocol. At every declared
reciprocal point, the lowest two ordered eigenstates define the retained rank-two
spectral space. The protocol requires the retained/excluded finite-mesh gap to exceed
the declared energy threshold.

The ambient basis is the ordered four-state coefficient basis shown in the typed
configuration. Retained frames contain the lowest two ordered eigenvectors as columns;
unitaries act on their right. Energies and hopping blocks use the dimensionless reference
energy `E_ref`, the energy zero is the exact parent onsite convention, and reduced
momenta use reciprocal period one on the centered half-open interval. The direct
rank-first study context realizes this reduced convention with the explicit lattice
geometry $a_0=1\,\mathrm{bohr}$; this geometry supplies units and does not alter the
legacy dimensionless result wire. Operators are compared only after their state spaces
are explicitly aligned.

## Sample roles

- The centered half-open 64-point reciprocal mesh constructs frames, transformations,
  represented operators, Fourier blocks, and finite-range models.
- The disjoint 257-point staggered mesh evaluates already fixed finite-range models.
- Evaluation values cannot alter the parent, frames, attack, transformations, ranges,
  thresholds, or selected result fields.

The maintained schema must call the first role **objective construction** or
**construction**, not training; no statistical model is learned.

## Frame contract

The successor preserves backend-qualified eigenvector-diagonal frames selected from the
lowest two eigenpairs. It retains:

- numerical backend and version;
- ordered eigenvalues;
- input-Hermiticity and residual diagnostics;
- frame orthonormality;
- retained projector and retained/excluded boundary gap; and
- any translated backend failure.

The selected frames are not canonical across eigensolver backends. Within an exactly or
numerically degenerate retained cluster, their coordinates are backend-selected. A
projector-derived deterministic frame would be a different protocol and is not silently
substituted.

## Transport, attack, and alignment

1. Construct the reciprocal frame path with identity sewing.
2. Apply polar parallel transport and distribute the selected closure transformation.
3. Apply the known right-unitary rank-two rotation
   \[
   A(k)=\begin{pmatrix}\cos\theta(k)&-\sin\theta(k)\\
   \sin\theta(k)&\cos\theta(k)\end{pmatrix},
   \qquad
   \theta(k)=0.30+0.65\sin(2\pi k)+0.30\sin(4\pi k).
   \]
4. Select a distinct Procrustes transformation at every construction point.
5. Separately select one unitary from the equal-weight ordered aggregate covariance.

For both Procrustes families, the candidate acts on the right toward the reference.
Optimization combines absolute cutoff `1e-14` and relative cutoff `1e-12` using the
maximum rule. A covariance is full rank only when both singular values exceed the
applied cutoff. A rank-deficient covariance is rejected without returning a
transformation; no null-space completion is part of this protocol. Backend-validation
absolute tolerance is `1e-12` and relative tolerance is zero.

Pointwise and one-global-unitary alignment are different feasible families. Neither is
presented as an approximation to the other.

## Represented operators and locality

Represent the parent Hamiltonian in transported-reference, attacked, pointwise-aligned,
and globally aligned frames. Fourier-transform the transported-reference, attacked, and
pointwise-aligned represented paths using the declared finite positive-exponent
convention. Retain complete block families and reconstruct each source path before
truncation.

Convert each even cyclic transform to an ordinary integer-lattice inventory before
range truncation. Remove only the negative Nyquist representative `-32` and report its
normalized conversion power

\[
P_{c,\mathrm{Nyq}}=\frac{\lVert t_{c,-32}\rVert_F^2}{2E_\mathrm{ref}^2}.
\]

This conversion power is not an off-node spectral error and is not silently pooled with
ordinary support deletion. The complete ordinary inventory is `-31, …, 31`.

On the disjoint evaluation mesh, let `h_c^ord` be the complete ordinary interpolant,
`h_c^(R)` its symmetric range truncation, and `h_c^dir` the directly evaluated channel
field. The reference and pointwise direct fields are the complete ordinary reference
field. The attacked direct field is obtained by applying the declared analytic attack to
that reference field at each evaluation point. Report separately:

- interpolation: `h_c^ord - h_c^dir`;
- deliberate truncation: `h_c^(R) - h_c^ord`; and
- total consequence: `h_c^(R) - h_c^dir`.

Each channel retains the maximum normalized Frobenius residual
`||Δh||_F / (sqrt(2) E_ref)` and the maximum sorted two-band residual. These maxima are
not added as independent scalar errors; only the corresponding pointwise triangle
inequality is available.

Apply symmetric hopping ranges `0, 1, 2, 3, 4, 6, 8`. For each range and channel,
retain the ordinary omitted-block L2 norm, construction total spectral error, and the
disjoint-evaluation truncation and total Hamiltonian and spectral errors. Locality,
conversion, interpolation, and truncation are frame-dependent diagnostics, not
invariant physical observables.

## Independent verification

The producer-independent verifier must reconstruct the parent samples, frame/projector
diagnostics, attack, alignment objectives, represented operators, cyclic and ordinary Fourier blocks, conversion power,
direct evaluation fields, truncations, and separated interpolation/truncation/total
Hamiltonian and spectral errors without calling the producer Action or an owner
alignment solver. It must independently establish that every accepted pointwise and
aggregate covariance is numerically full rank under the retained cutoff.

Shared BLAS/LAPACK and array-library lineage must be disclosed. Numerical agreement
establishes bounded software behavior only; it does not establish continuum convergence,
material validity, uncertainty bounds, or scientific acceptance.

## Migration and evidence gates

The source lifecycle now closes strict typed configuration, result, verification, and
visualization field inventories; canonical typed JSON; owner dependencies; independent
reconstruction; and direct effect adapters. It does not create a schema-v1 compatibility
artifact or decode historical campaign bytes at runtime.

Before assigning `.v1` or retaining a maintained run:

1. complete independent source and scientific-protocol review;
2. define the retained execution and evidence-sealing policy;
3. keep historical M2 and monograph publication references bound to their exact bytes;
4. preserve the completed M3 consumer migration and M2 source-retirement recovery
   record; and
5. obtain explicit retained-execution authorization.

Open owner replacements are tracked as
[`TECH_DEBT`](../../../../docs/tasks/tech_debt/composite-band-alignment-and-locality/index.md).
