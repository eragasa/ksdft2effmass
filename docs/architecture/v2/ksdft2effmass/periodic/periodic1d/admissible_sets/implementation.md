# M3 implementation

## Algorithm

`Periodic1DConstrainedAdmissibleSetCalculator.execute()`:

1. executes the composed M2 baseline without subclassing it;
2. constructs the M3 training and staggered evaluation operator paths;
3. constructs exact spectral and represented-operator squared-loss quadratics over the
   continuous shift/splitting rectangle for every frozen angle;
4. evaluates the prospective witness and analytic threshold boundaries;
5. correlates each analytic quadratic with independently reconstructed coefficients
   and retained boundary evaluations;
6. evaluates the compatible case and retains its common witness;
7. evaluates the separated case and constructs a splitting-axis lower bound;
8. retains the three predeclared evaluation-role diagnostics;
9. summarizes range-one M2 locality for interpretive context; and
10. constructs one immutable result with bounded dispositions.

## Correlation enforcement

Definition and result objects enforce exact M2 rank, finite built-in numeric controls,
ordered unique case identities, threshold units, domain membership, loss-vector lengths,
quadratic/source correlation, role identities, locality inventory, witness consistency,
and certificate/disposition consistency.

## Serialization

The serializer emits
`ksdft2effmass.periodic1d.constrained-admissible-set-result.v1`. It preserves
M2 control identity, parameter meanings and units, all case thresholds and dispositions,
training/evaluation roles, analytic quadratics, locality evidence, and explicit
non-claims. Keys and separators are canonical and NaNs are forbidden.

## Independent reconstruction

`Periodic1DConstrainedAdmissibleSetResultVerifier` reconstructs M2 and M3 training paths,
finite-angle loss quadratics, all three evaluation roles, analytic coefficients, unclipped-set
premises, common witnesses, locality summaries, and the separation bound. The retained
standalone verifier additionally checks strict wire schemas, positive tolerances,
configuration materialization, and source/artifact integrity.

## Code mapping

| Stage | Source owner |
|---|---|
| Controls and mesh | `periodic1d/admissible_sets/definition.py` |
| Producer | `periodic1d/admissible_sets/calculate.py` |
| Proof/result objects | `periodic1d/admissible_sets/results.py` |
| Encoding | `periodic1d/admissible_sets/serialization.py` |
| Reconstruction | `periodic1d/admissible_sets/verify.py` |
| Confirmatory retained package | `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/` |
| Post-hoc sensitivity | `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets-threshold-sensitivity/` |

## External boundary

M3 is local synthetic work. It does not execute Quantum ESPRESSO, Wannier90, remote
resources, or schedulers. Its thresholds and dispositions have no direct material
acceptance meaning.
