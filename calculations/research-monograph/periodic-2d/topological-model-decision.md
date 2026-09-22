# Decision support: topological obstruction benchmark

## Decision boundary

At this decision boundary, the periodic-2D Task included a human-requested
genuinely topological or Chern-band obstruction test. The accepted scalar continuum cosine family is
real and spinless, has zero Chern diagnostic, and cannot supply the requested
nonzero-Chern case without introducing a different operator class. Selecting
that operator fixes the scientific meaning of the test and therefore requires a
human decision.

The benchmark must provide:

- an exactly declared two-dimensional Bloch operator and state space;
- a gapped isolated band or composite subspace with independently checked
  nonzero Chern number;
- a gauge-invariant lattice-curvature and Wilson-loop calculation;
- an explicit failure of a globally smooth periodic frame or exponentially
  localized single-band Wannier representation;
- a control in the trivial parameter regime;
- a finite-mesh refinement study; and
- a claim boundary excluding material validation and any assertion about the
  scalar cosine parent.

## Option A — Qi–Wu–Zhang square-lattice two-band model

Use the two-component square-lattice Bloch Hamiltonian

$$
H(\mathbf k)=\sin k_x\,\sigma_x+\sin k_y\,\sigma_y
 +(m+\cos k_x+\cos k_y)\sigma_z.
$$

Evaluate a trivial mass and a Chern-nontrivial mass on the same square
Brillouin-zone meshes used by the exercise.

**Advantages:** smallest exact matrix; same square reciprocal topology; known
gap-closing boundaries; inexpensive refinement; clear distinction between a
rank-one Chern band and the complete rank-two trivial bundle; direct Wilson,
curvature, gauge, and localization tests.

**Risks:** this is a lattice two-component model rather than a continuum
plane-wave reduction, so it tests the topology/localization boundary as a
separate controlled model rather than as a continuation of the cosine parent.

## Option B — square-lattice Hofstadter model

Use a rational magnetic flux per plaquette, an enlarged magnetic unit cell, and
the corresponding multi-band Harper/Hofstadter Bloch operator.

**Advantages:** retains a square real-space lattice and makes magnetic
translation, band Chern numbers, and the obstruction visible in a spatially
explicit tight-binding model.

**Risks:** magnetic gauge, flux denominator, enlarged-cell ordering, multiple
Chern bands, and gap selection add several new numerical conventions. These can
obscure the single requested obstruction and make direct comparison with the
existing scalar exercise less transparent.

## Option C — Haldane honeycomb model

Use the two-band honeycomb Haldane Hamiltonian with complex next-nearest-neighbor
hopping, comparing trivial and Chern phases.

**Advantages:** canonical real-space Chern-insulator model with a direct
connection between complex hopping, broken time reversal, Berry curvature, and
Wannier obstruction.

**Risks:** changes the lattice from square to honeycomb, introduces a two-site
basis and nonorthogonal primitive vectors, and therefore combines topology with
a geometry and ordering migration.

## Recommendation

Choose **Option A**, the Qi–Wu–Zhang model. It adds the minimum operator structure
needed for a nonzero Chern band, retains the square Brillouin-zone organization,
and isolates the topological obstruction from magnetic-cell or lattice-geometry
complexity. The result must remain a separate topological control and must not
be described as a topological phase of the scalar continuum cosine family.

## Human decision

The human explicitly selected a combined Option E at
`RM-PERIODIC-2D-TOPOLOGICAL-MODEL-HC03`: implement all three models as separate
controlled benchmarks. Their state spaces, parameters, convergence records,
Chern and Wilson diagnostics, obstruction evidence, and limitations must remain
distinct. Their errors must not be combined, and none may be identified with
the scalar continuum cosine parent.

## Consequence of deferral

Without completed calculations, the current zero-Chern scalar result remains
only a trivial control. No claim about a genuine Wannier obstruction can yet be
made.
