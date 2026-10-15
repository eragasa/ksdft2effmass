# Isotropic 3-D model-adequacy experiment

## Task status

This development task is the second stage of the selected dimensionality and anisotropy
sequence. It follows the isotropic 2-D protocol boundary and introduces a third periodic
coordinate while preserving declared cubic axis-permutation symmetry.

Experiment-family identity:

```text
ksdft2effmass.campaign.model-adequacy.periodic3d.isotropic-hopping-support-hierarchy
```

This task path is mutable work coordination. It is not an experiment-version ID, run
ID, evidence identity, or publication reference.

## Authoritative inputs

- [Dimensionality and anisotropy ladder](../../../../architecture/v2/experiments/model-adequacy/dimensional-anisotropy-ladder.md)
- [Isotropic 3-D experiment architecture](../../../../architecture/v2/experiments/model-adequacy/periodic3d/isotropic-hopping-support-hierarchy/index.md)
- [Periodic 3-D experiment package](../../../../architecture/v2/experiments/model-adequacy/periodic3d/index.md)
- [Shared admissible-set evidence semantics](../../../../architecture/v2/ksdft2effmass/analysis/model_adequacy/admissible-set-evidence-semantics.md)
- [Isotropic 2-D predecessor task](../isotropic2d/index.md)

Concrete composition will belong under
`experiments/model-adequacy/periodic3d/isotropic-hopping-support-hierarchy/`. It must not
be implemented as a generic installed 3-D admissible-set framework.

## Scientific delta from isotropic 2-D

The task changes dimensionality while keeping the symmetry control explicit. Its future
protocol must define:

- one exact simple-cubic scalar synthetic parent and one scalar orbital per cell;
- the direct and reciprocal lattice conventions and reduced-coordinate map;
- full signed-permutation orbit construction, including multiplicities;
- a maximal common coefficient space and nested support classes;
- a cubic-symmetric nonuniform spectral weight that does not collapse to the operator
  channel through equal-weight Parseval equivalence;
- a complete-block operator loss, common domain, common metric, and resolution;
- disjoint objective-construction, evaluation, and locality roles; and
- certificate containment and conservative-arithmetic premises in the actual active
  dimension.

`isotropic` means cubic axis-permutation symmetry for this finite synthetic protocol; it
does not mean continuous rotational invariance.

## Sequencing gate

Implementation must not start by copying the anisotropic 3-D proposal and restoring
axis equality after the fact. First review the isotropic 2-D protocol and identify which
behavior is genuinely dimension-independent. Then freeze an independent isotropic 3-D
protocol and experiment version.

The later anisotropic 2-D and anisotropic 3-D stages remain separate experiment families.
Their results, thresholds, certificates, and validation domains cannot be inherited by
this task.

## Definition of done for the development stage

Before advancing to anisotropic 2-D implementation, this task must provide:

1. an exact reviewed parent, lattice, symmetry, coefficient inventory, and support order;
2. frozen channels, sample roles, domain, metric, thresholds, and resolution;
3. a reviewed certificate and conservative-arithmetic contract;
4. strict schemas and independent verification;
5. exact dependency and adapter identities;
6. adversarial symmetry, multiplicity, permutation, and role-isolation tests; and
7. a bounded synthetic evidence and interpretation policy.

No immutable `.v1`, implementation, retained run, or scientific result exists yet.

## Protected boundary

This task authorizes no Quantum ESPRESSO, Wannier90, remote, cluster, production, or
retained scientific execution. It is not a silicon approximation or material-validation
stage.
