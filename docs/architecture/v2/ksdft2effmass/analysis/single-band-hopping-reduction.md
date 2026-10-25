# Reusable one-dimensional single-band hopping reduction

## Status

`ksdft2effmass.analysis.single_band_reduction` is the reusable scientific Workflow
extracted for publication-independent single-band experiments. It consumes already
identified training and evaluation band samples. It does not construct a parent,
select a band, define an experiment, serialize evidence, or decide scientific
adequacy.

## Contract

`SingleBandHoppingReductionRequest1D` supplies:

- one real band on every point of an even centered half-open transform mesh;
- one real band on caller-selected evaluation coordinates;
- a unique increasing symmetric-range inventory;
- one positive unitless fitting weight per training sample; and
- explicit reciprocal-coordinate, energy, squared-energy, reconstruction,
  Hermiticity, Parseval, and imaginary-residual tolerances.

Training values define the complete finite Fourier transform and direct fits.
Evaluation values are downstream diagnostics and cannot alter a model. The reusable
contract permits coincident roles when explicitly supplied; experiments may strengthen
this to a disjoint-coordinate requirement.

`SingleBandHoppingReductionWorkflow1D` constructs:

1. scalar reciprocal-operator samples from the training band;
2. the complete centered finite Fourier hopping representation;
3. complete-model modular Hermiticity diagnostics;
4. one symmetric truncation per requested range;
5. separate training and evaluation band-error diagnostics;
6. complete-mesh Parseval diagnostics;
7. a positive-weight direct fit in the same representative class;
8. coefficient and sampled-operator route comparison; and
9. evaluation-coordinate bandwidth, curvature, and imaginary-residual diagnostics.

The immutable result correlates every subresult with the exact request, source,
transform, model, weights, coordinates, and range inventory.

## Ownership

KSD owns reciprocal coordinates and representatives, units, Fourier and hopping
meaning, training/evaluation roles, construction of design rows from reciprocal
geometry, hopping-record construction, route meaning, Hermiticity, Parseval, band
errors, band shape, and interpretation.

The reusable unit-free complex positive-weight multiple-right-hand-side linear
least-squares kernel is owned by `projectkoios-optimization`. The KSD
`BlockHoppingLeastSquaresFitter1D` is its narrow domain adapter: KSD constructs the
Fourier design and flattened targets, passes positive objective weights without
pre-scaling, maps coefficient rows to unit-bearing hopping blocks, and independently
reconstructs domain diagnostics. The Workflow exposes no owner-neutral solver
interface and contains no second `lstsq` implementation.

The live reviewed owner dependencies are pinned to Optimization commit
`3cd32ea8985a855bcdbaffbf89af95e970b3bf14` and synchronized PhysKit commit
`2aaa4ba5ff4c51f5c5068ac895ef4ec5de293439` in `python/pyproject.toml` and
`python/uv.lock`. Immutable version-one retained-run provenance preserves the exact
revisions used by that execution independently of the advancing live lock. Owner
qualification and adapter verification remain distinct from KSD scientific validation.

## Experiment boundary

The first consumer is

```text
experiments/periodic-reduction/single-band-fourier-reduction/periodic1d/
```

That experiment owns the finite Fourier parent, represented-reference sweeps, retained
band and sampled-gap calculation, disjoint sample-role policy, fitting weights, ranges,
and future protocol/evidence interpretation. The installed package never imports the
experiment.

## Evidence and limitations

Direct software tests exercise two unrelated supplied scalar bands, uniform and
nonuniform fitting weights, exact finite-range recovery, strict rank-one admission,
and Boolean-control rejection. Experiment tests exercise parent refinement, explicit
band selection, sampled external gaps, disjoint roles, and delegation to the reusable
Workflow.

Passing these tests establishes software behavior only. It does not establish spectral
isolation over a continuum, continuum convergence, a scientifically adequate hopping
range, material transferability, uncertainty quantification, or publication evidence.
