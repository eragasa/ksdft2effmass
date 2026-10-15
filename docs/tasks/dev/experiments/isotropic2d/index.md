# Isotropic 2-D model-adequacy experiment

## Task status

This development task is the first stage of the selected dimensionality and anisotropy
sequence. It plans the maintained successor for the prospective square-symmetric
hopping-shell study.

Experiment-family identity:

```text
ksdft2effmass.campaign.model-adequacy.periodic2d.hopping-shell-hierarchy
```

Historical planning label `HSH-1` remains an alias only. This task path is mutable work
coordination; it is not an experiment-version ID, run ID, evidence identity, or
publication reference.

## Authoritative inputs

- Sequence definition: `docs/architecture/v2/experiments/model-adequacy/dimensional-anisotropy-ladder.md`
- [Isotropic 2-D experiment architecture](../../../../architecture/v2/experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/index.md)
- [Maintained prospective protocol](../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/protocol.md)
- [Exact orbit and support inventory](../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/orbit-support-inventory.md)
- [Projection and loss design](../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/projection-and-loss-design.md)
- [Sample-role design](../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/sample-role-design.md)
- [Threshold and resolution design](../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/threshold-design.md)
- [Legacy HSH design bundle](../../../../architecture/v2/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/index.md)
- [Shared admissible-set evidence semantics](../../../../architecture/v2/ksdft2effmass/analysis/model_adequacy/admissible-set-evidence-semantics.md)
- [Draft historical protocol](../../../../../calculations/ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/protocol.md)

The historical calculation directory is a design source, not the maintained experiment
owner. The publication-independent maintained design now lives at
`experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/`; future concrete
composition belongs there as well.

## Definition of done for the development stage

Before the isotropic 3-D task advances to implementation, this task must provide:

1. a publication-independent experiment directory and stable family identity;
2. an exact square-symmetric scalar parent binding and source digests;
3. a reviewed orbit inventory, maximal coordinate embedding, and nested support classes;
4. frozen objective-construction, evaluation, withheld, and locality roles;
5. nonuniform positive spectral weights and complete-block operator weights;
6. frozen coefficient domain, thresholds, metric, resolution, and certificate premises;
7. strict input and result schemas with canonical serialization;
8. independent reconstruction that does not call the producer;
9. reviewed exact dependency and adapter identities; and
10. tests and an evidence policy that preserve the bounded synthetic nonclaim.

The maintained experiment must remain outside `python/src/`. It consumes reviewed owner
contracts directly when their boundaries fit. One concrete need and clear semantic
ownership are sufficient to extract the smallest complete reusable capability before KSD
creates a duplicate; a second implementation or consumer is not required.

## Completed development decisions

The maintained prospective protocol now selects:

- the exact retained donor and current byte digests;
- the 225-member centered domain;
- eight ordered square-symmetry operations;
- 36 canonical ordered orbits and deterministic member order;
- the common maximal coefficient embedding;
- the eight support prefixes with active dimensions `(1, 2, 3, 4, 6, 12, 27, 36)`;
- represented-block counts `(1, 5, 9, 13, 25, 61, 161, 225)`;
- the complete-block multiplicity metric;
- separate `1.0e-12 * E_G` source-consistency controls and the projected 36-coefficient target;
- the common shift $\Delta E=-0.08796825852205918\,E_G$;
- the common box half-width `0.11426128163399648 * E_G` selected before hierarchy inspection;
- a positive nonuniform square-symmetric spectral-weight formula with full-rank active designs;
- one 225-point objective-construction mesh, disjoint symmetry-closed 480-point evaluation and 480-point withheld subsets, and a complete-block locality role;
- prospective spectral/operator RMS thresholds `0.001004` and `0.00007310` and separation resolution `0.000005`, selected through disclosed outcome-informed design; and
- the existing-experiment-shaped execution graph through `definition.py`,
  `experiment.py`, `results.py`, `verify.py`, and `serialization.py`, without a nested
  execution framework.

Optimization's arbitrary-dimensional closed-box positive-definite quadratic minimizer is
reviewed and live development is exactly bound at
`projectkoios-optimization@f6bdecc418e46240087d1dfb1c22dac396cdc455`. Its public
contract is unchanged from the earlier revision used by the disclosed threshold-design
calculation. KSD will consume it directly and will not add a local generic solver.

## Current blockers

Active-quadratic tolerances, conservative-arithmetic method, intersection/separation
methods, schemas, remaining method identities, and retained-evidence policy are not
frozen. No immutable `.v1`, implementation, retained run, or scientific result exists.

## Protected boundary

This task authorizes no Quantum ESPRESSO, Wannier90, remote, cluster, production, or
retained scientific execution. Passing future software tests will not establish
scientific validation or material relevance.
