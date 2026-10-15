# Single-band experiment and reusable-Workflow extraction

## Status

The maintained direction is implemented as two one-way layers:

```text
experiments/periodic-reduction/single-band-fourier-reduction/periodic1d
    -> ksdft2effmass.analysis.single_band_reduction
        -> reusable model, transform, fit, and diagnostic Actions
```

The publication-independent experiment-family identity is

```text
ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction
```

Historical `M1` and `isolated-band` material is outside this implementation slice and
is not rewritten. Selecting one band does not itself establish spectral isolation; the
new experiment retains sampled external-gap diagnostics and makes no continuum gap
claim.

## Experiment ownership

The experiment owns:

- selection of the finite Fourier toy parent;
- plane-wave and finite-difference sweep inventories;
- the finite represented parent reference;
- explicit retained-band selection;
- disjoint training and evaluation coordinates;
- fitting-weight and hopping-range inventories;
- experiment-specific controls and interpretation; and
- future protocol, serialization, verification, and evidence policy.

The experiment Action performs deterministic in-process calculations only. It performs
no file I/O, external execution, scientific acceptance, or evidence retention.

## Reusable Workflow ownership

`ksdft2effmass.analysis.single_band_reduction` owns a model-independent request over
already identified single-band training and evaluation samples. It composes:

- the complete centered finite Fourier transform;
- modular hopping Hermiticity;
- symmetric finite-range truncation;
- separate training and evaluation errors;
- Parseval diagnostics;
- the weighted direct-fit route in the same representatives;
- direct-versus-mediated route comparison; and
- scalar band-shape diagnostics.

Its request and result contain no experiment identity, parent model, band-selection
policy, scientific adequacy threshold, wire schema, retained path, or publication
label. Public numeric tolerances carry explicit units, Boolean numeric controls are
rejected, and result objects preserve exact request/source/model correlations.

## Optimization ownership

KSD owns reciprocal geometry, units, training/evaluation roles, construction of
Fourier design rows and target columns, hopping-record construction, route meaning,
domain diagnostics, and interpretation.

`projectkoios-optimization` owns the reusable unit-free complex positive-weight
multiple-right-hand-side linear least-squares kernel. KSD's
`BlockHoppingLeastSquaresFitter1D` is the domain adapter: it owns Fourier construction,
unit conversion, coefficient-to-hopping mapping, reconstruction, and KSD diagnostics,
while delegating the numerical solve to the reviewed owner API pinned at commit
`d9a82252faa1b41d82cce11149329aa91b84dff0`. The least-squares capability is unchanged
from its reviewed parent revision `6c3f73cd5f1810c8de915e1559658ea4b79c2357`. The KSD Workflow introduces no second
`lstsq` implementation, owner-neutral solver ABC, or competing generic least-squares
result. Owner and adapter qualification remain separate from scientific validation.

## Verification

The reusable Workflow tests use multiple supplied scalar-band datasets without a
parent-model contract. They cover exact finite-range recovery, uniform and nonuniform
weights, explicit range inventories, one-band admission, and Boolean-control rejection.
The owner adapter tests additionally cover multiple matrix entries as right-hand-side
columns, raw positive objective-weight forwarding, full-rank condition propagation,
and rank-deficient disposition. A bounded independent owner-contract review reported
`NO_BLOCKING_FINDINGS`; that review is software-integration evidence, not scientific
validation.

The experiment tests cover model-specific parent refinement, selected-band reduction,
sampled external gaps, disjoint coordinate roles, publication-independent identity,
and delegation to the reusable result contract.

Passing tests establishes software behavior only. No result currently constitutes a
frozen experiment version, retained run, publication evidence, physical band-isolation
certificate, continuum-convergence result, material validation, adequate-range
selection, or uncertainty quantification.

## Remaining work before a retained experiment

1. Review the experiment controls and assign an immutable experiment-version identity.
2. Add strict experiment-local input and result schemas.
3. Add an independent verifier that does not use the producer Workflow as its oracle.
4. Freeze source, dependency, protocol, and adapter identities.
5. Run only the authorized local synthetic experiment.
6. Retain compact evidence and publish it through a publication-side reference
   manifest.
