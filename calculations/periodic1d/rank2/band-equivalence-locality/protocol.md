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

## Five-stage contract

1. `simulations/run_01_experiment.py` produces a versioned simulation result.
2. `simulations/run_02_experiment_verification.py` independently verifies that result.
3. `analysis/run_03_analysis.py` consumes only verified simulation output.
4. `analysis/run_04_analysis_verification.py` independently verifies the analysis.
5. `analysis/run_05_plots.py` consumes verified analysis output.

These paths are contractual targets, not assertions that the stages already exist.

## Migration boundary

The active mathematical and numerical specification currently remains in the maintained
experiment and the `Ragasa2026a` v3 manuscript. Migration must preserve numerical values,
model conventions, development status, and provenance. Historical retained artifacts
must remain byte-identical and are referenced rather than moved.

Production controls, a maintained version identifier, immutable run identity, retained
execution, public archive, and scientific validation remain open.
