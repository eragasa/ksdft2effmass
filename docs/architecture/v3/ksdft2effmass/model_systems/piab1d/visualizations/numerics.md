# Numerical contract

Every numerical array, quantity, mask, selection, and diagnostic displayed by PIAB1D is
copied from `Piab1dVisualizationData`. The package does not rerun the PhysKit solver,
construct a Hamiltonian, calculate an eigensystem, select a retained dimension, evaluate
a quadrature rule, fit a convergence order, or decompose an operator.

Presentation may select recorded series, normalize axes using recorded quantities, and
arrange already authenticated values into the existing thirteen figures. Wavefunction
curves use the recorded coordinate and state arrays; the renderer does not renormalize
or phase-align them. Logarithmic axes reject invalid supplied extents rather than
silently clipping them.

The package migration must prove byte-identical canonical projection JSON and exact
plot-enum equality. PNG bytes are not required to be cross-platform identical unless a
separate visual-regression contract says so.
