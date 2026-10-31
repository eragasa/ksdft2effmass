# Protocol boundary

## Scientific object

The controlled parent is a one-dimensional periodic four-state Hamiltonian with onsite
and nearest-neighbor hopping blocks. At each reduced Bloch coordinate, the two lowest
bands define a retained rank-two subspace when the second-to-third-band gap satisfies the
declared gate. A transported periodic frame represents the retained operator as a
`2 x 2` Hermitian matrix field.

The comparison field is produced by the smooth real rotation

```math
U_a(q)=R(a\sin 2\pi q), \qquad 0\leq a\leq \pi/4.
```

The transformation preserves the ordered bands pointwise but generally changes Fourier
hopping blocks in the declared common coordinates. Only one global real rotation is
admissible during cross-representation comparison; the generating momentum-dependent
rotation is deliberately excluded.

## Numerical channel separation

The maintained calculation must report these channels independently:

1. parent and retained-space qualification;
2. frame transport and reciprocal-period closure;
3. exact pointwise band equivalence;
4. restricted global-alignment residual;
5. finite-cyclic Fourier representation and Nyquist conversion;
6. deliberate ordinary-lattice truncation;
7. disjoint-mesh interpolation error;
8. total sorted-band consequence; and
9. retained hopping-range decisions under prospectively declared tolerances.

The errors are not an automatically additive budget.

## Direct lifecycle contract

1. `run_01_calculation.py` composes simulation and analysis owners and retains one
   canonical calculation record containing the parent family, momentum refinement,
   adaptive-amplitude refinement, and truncation.
2. `run_02_verification.py` admits the exact retained bytes and independently verifies
   every aggregate channel before retaining canonical verification.
3. `run_03_render.py` admits stored aggregate and parent-family authentication and renders
   the closed six-figure family, momentum-refinement, adaptive-amplitude, and truncation
   inventory without rerunning scientific verification.

All three stages refuse overwrite. The controls embedded in the calculation script were
recovered from development work. Their later local execution required and received
separate authorization; this document by itself does not authorize a rerun, sealing,
promotion, or publication.

## Migration boundary

The maintained calculation owner now contains the development implementation, schemas,
tables, figures, and complete buildable prospective protocol bundle. The exact authority
and conflict rules for this concise boundary, the buildable bundle, implementation,
technical report, and publication consumers are recorded in
[`protocol-authority-and-historical-donors.md`](protocol-authority-and-historical-donors.md).
Historical M2, monograph-composite, finite-angle regression, and retained artifacts remain
distinct and Git-recoverable; they are referenced rather than restored, merged, or
rewritten.

Two immutable no-overwrite local run identities now exist: `v1` preserves a failed
independent-verification attempt, and `v2` preserves the byte-identical calculation with
passing aggregate verification and six admitted figures. Both remain unsealed. A
maintained protocol version, sealing disposition, public archive, and scientific
validation remain open.
