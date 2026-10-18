# Appendix A. Planned Protected Calculation Sequence

This appendix records proposed work. It does not authorize calculator execution.

Before execution, the campaign must bind an accepted production-lattice artifact,
authenticated full-precision inputs, exact executable and pseudopotential identities,
the physical branch, numerical settings, warning and stop policies, stage manifests,
and explicit execution authorization.

Subject to those gates, the planned sequence is:

1. qualify the production DFT parent across the declared convergence corners;
2. locate and identity-track the conduction valley;
3. construct and independently validate the ten-orbital Wannier representation;
4. freeze final thresholds, parameter domains, alignment family, search budgets, and
   map resolution;
5. search both admissible sets for each hierarchy member;
6. construct a common witness or separation bounds;
7. evaluate withheld band, valley, mass, and operator gates; and
8. repeat required sensitivity and independent checks before selection.

A failed prerequisite stops the sequence. Tutorial values, literature masses, or an
unreviewed numerical setting cannot fill a missing production record.

## Planning gates

| Gate | Required evidence before proceeding | Current status |
|---|---|---|
| Production lattice | Accepted `02.01.04` lattice artifact and provenance | Pending |
| Parent identity | Full inputs, executable, pseudopotential content hash, physical branch | Pending |
| Execution authority | Explicit authorization for the bounded production stage | Not authorized |
| Parent convergence | Cutoff/mesh corners and downstream-observable convergence | Pending |
| Branch identity | Cell-periodic overlap, fixed-projector correlation, and applicable symmetry witness | Pending implementation |
| Wannier qualification | Windows, projections, centers, spreads, interpolation, and support diagnostics | Pending |
| Threshold freeze | Measured floors and frozen thresholds before compatibility fitting | Pending |
| Compatibility search | Frozen classes, domains, budgets, witnesses, and bounds | Pending |
| Withheld validation | Disjoint band, valley, mass, and operator evidence | Pending |
| Model selection | Smallest compatible class or bounded inconclusive/incompatible disposition | Pending |

## Execution-planning requirements

Before any authorized expensive stage, report the executable, input system, expected
scale and outputs, and anticipated runtime and resources when known. Do not change the
pseudopotential, exchange–correlation approximation, cutoffs, meshes, tolerances,
structure, Wannier windows or projections, or energy-alignment convention without the
applicable scientific authority.
