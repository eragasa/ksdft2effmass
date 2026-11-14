# Test conventions

New or substantively revised class-owned tests use these names:

```text
test__ClassName__split_slug.py
test__ClassName__split_slug
```

The split slug names one observable requirement. Every test has a concise docstring,
and non-obvious fixtures, reference arithmetic, tolerances, or representation choices
have inline rationale comments. Split unrelated requirements into separate tests;
retain multiple assertions only when they describe one correlated invariant. Prefer
one array-level comparison over assertion loops, and use parameterization when the
same behavior is exercised over multiple cases. Setup and extraction helpers must not
hide assertion trains.

# Test markers

Markers describe independent properties of a test. Directory names do not assign
markers. Every newly added or substantively modified test module declares exactly one
boundary marker (`unit` or `integration`) and at least one evidence-claim marker.
Historical modules that predate this policy are classified incrementally when their
tests next change; their directory does not supply an implicit classification. CI
checks every changed `python/tests/**/test*.py` module with strict mypy and enforces
this boundary/evidence marker rule.

- `unit` identifies an isolated software boundary without repository artifacts,
  subprocesses, complete calculation composition, or external executables.
- `integration` identifies a boundary crossing through files, processes, serializers,
  scripts, packages, calculation owners, or external-program adapters.
- `expensive` identifies measured or structurally unavoidable work that is unsuitable
  for every bounded continuous-integration run. Every expensive test is also marked
  `integration`.
- `software_verification`, `numerical_verification`, `scientific_validation`, and
  `uncertainty_quantification` state the kind of claim tested. They are independent of
  cost and boundary markers.

Historical calculation subjects require an explicit test disposition. Maintained
campaign replay may use exact, digest-bound test resources under
`tests/resources/historical_calculations/` rather than restoring a superseded
calculation layout. Defect-2D Folding and Null-Alignment Controls use active typed
public contracts and an authored synthetic calculation package replayed from
`calculations/periodic2d_rank_defect/`. The same owner retains a separate accepted-
historical-synthetic parent-qualification package; routine tests authenticate its
manifest and exercise compact calculation and independent-verification inventories
rather than rerunning the complete 11,340 route constructions. Removed Stage B/C
execution contracts are not retained as skipped test modules. The maintained
defect-model plotter instead uses a scalar test-owned projection. These dispositions do
not promote fixtures to active calculation owners or strengthen scientific claims.

From `python/`, run the bounded suite with:

```console
uv run pytest -m "not expensive" tests
```

Run package-owned expensive tests explicitly with:

```console
uv run pytest -m expensive tests
```

The maintained rank-N calculation-local structural and plotting tests are outside the
package test tree. Run their bounded subset with:

```console
uv run pytest -c pyproject.toml -m "not expensive" \
  ../calculations/periodic1d/rankN/composite-band-alignment-locality/tests
```

If that calculation later adds an expensive full-case test, run it explicitly with the
same path and `-m expensive` only when the numerical calculation changes.

Passing tests establishes only their stated software or numerical behavior. It does
not establish scientific validation, convergence, uncertainty quantification,
retained-evidence admission, release, or publication acceptance.
