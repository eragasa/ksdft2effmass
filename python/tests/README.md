# Test markers

Markers describe independent properties of a test. Directory names do not assign
markers. Every newly added or substantively modified test module declares exactly one
boundary marker (`unit` or `integration`) and at least one evidence-claim marker.
Historical modules that predate this policy are classified incrementally when their
tests next change; their directory does not supply an implicit classification.

- `unit` identifies an isolated software boundary without repository artifacts,
  subprocesses, complete calculation composition, or external executables.
- `integration` identifies a boundary crossing through files, processes, serializers,
  scripts, packages, calculation owners, or external-program adapters.
- `expensive` identifies measured or structurally unavoidable work that is unsuitable
  for every bounded continuous-integration run. Every expensive test is also marked
  `integration`.
- `legacy_equivalence` identifies compatibility-only equivalence with a historical
  software surface. It must be paired with `software_verification`; it does not claim
  numerical equivalence, scientific validation, or retained-evidence validity.
- `software_verification`, `numerical_verification`, `scientific_validation`, and
  `uncertainty_quantification` state the kind of claim tested. They are independent of
  cost and boundary markers.

This marker cleanup does not create skips or change the disposition of tests whose
historical calculation subjects are absent. Migrating or retiring those subjects is a
separate provenance decision.

From `python/`, run the bounded suite with:

```console
uv run pytest -m "not expensive" tests
```

Run package-owned expensive tests explicitly with:

```console
uv run pytest -m expensive tests
```

Run bounded historical-compatibility checks with:

```console
uv run pytest -m "legacy_equivalence and not expensive" tests
```

Run costly historical-compatibility checks only when their compatibility surface
changes:

```console
uv run pytest -m "legacy_equivalence and expensive" tests
```

The calculation-local higher-rank full-case test is outside the package test tree. Run
it only when that numerical calculation changes:

```console
uv run pytest -c pyproject.toml -m expensive \
  ../calculations/periodic1d/rankN/composite-band-alignment-locality/tests
```

Passing tests establishes only their stated software or numerical behavior. It does
not establish scientific validation, convergence, uncertainty quantification,
retained-evidence admission, release, or publication acceptance.
