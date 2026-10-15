# Periodic 1-D constrained admissible sets

## Status

This is the new publication-independent experiment home for

```text
ksdft2effmass.campaign.model-adequacy.periodic1d.constrained-admissible-sets
```

The current implementation includes the first two migration slices and their reviewed
numerical-owner integration. It composes an exact rank-two KSD multiband baseline,
derives normalized spectral and represented-operator training quadratics, and owns the
bounded parameter rectangle, finite alignment
family, threshold cases, common-witness policy, containment checks, splitting-axis
certificate, resolution, dispositions, and independent verification.

It does **not yet** replace the complete historical calculation. Evaluation-only sample
diagnostics, candidate locality, strict wire schemas, and retained evidence must move
into this experiment before an immutable `.v1` can be assigned. The composed multiband
baseline also remains a KSD source capability pending its separate experiment-boundary
review. No retained run or publication evidence is created here.

Historical `M3` and conference labels are searchable aliases only; they are not the
maintained experiment identity. Existing evidence under `calculations/` remains
unchanged.

## Numerical ownership

The exact dependency

```text
projectkoios-optimization@f6bdecc418e46240087d1dfb1c22dac396cdc455
```

owns:

- unit-free complex affine-residual construction over real coordinates;
- unit-free positive-definite completed-square validation and evaluation;
- exact two-dimensional rectangle minimization;
- full-ellipsoid support points; and
- deterministic ordered finite-family filtering and first-on-tie selection.

This live development dependency advances the earlier owner baseline by a qualified
typing refactor; the consumed affine, quadratic, support, and selection contracts are
unchanged. No immutable experiment version or retained execution provenance is attached
to the former pin.

The experiment does not expose a generic solver or implement a generic box-clipped-set
distance algorithm. Full-ellipsoid support becomes certificate evidence only after the
experiment verifies that the support point lies in its declared rectangle.

`ConstrainedAdmissibleSetsExperimentVerifier` first invokes the independent verifier for
the composed multiband baseline, then independently reconstructs KSD complex-feature
quadratics, rectangle candidates, support points, finite choices, and certificate bounds
without calling the producer or Optimization solvers. The producer forwards deterministic
C-order complex observations, negated offsets, and raw normalization weights to the
owner constructor; the verifier retains direct KSD formulas. Dimensionless geometry defects and
parent-energy defects remain separate typed channels. Passing checks establishes bounded
software behavior only, not scientific validation or uncertainty quantification.

## Development checks

```console
cd experiments/model-adequacy/periodic1d/constrained-admissible-sets
uv lock --check
../../../../python/.venv/bin/pytest -q
../../../../python/.venv/bin/ruff check src tests
../../../../python/.venv/bin/mypy src tests
```
