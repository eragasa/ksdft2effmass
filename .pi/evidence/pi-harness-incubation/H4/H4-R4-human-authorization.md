# H4 R4/E4 validator-stabilization authorization

Authorize one final bounded H4 validator-stabilization correction and one R4/E4
cycle.

Correct only:

1. resource/leakage scanning so generated Python cache artifacts are excluded
   deterministically:
   - ignore `__pycache__/`;
   - ignore `*.pyc` and `*.pyo`;
   - inspect only declared maintained textual-resource paths or explicitly
     supported textual suffixes;
   - do not silently ignore an undecodable file that is declared as a maintained
     textual resource;
   - do not rely on `PYTHONDONTWRITEBYTECODE` as the production fix;

2. completion validation so it does not hard-code the incidental focused pytest
   total.
   - remove the fixed `23 passed` expectation;
   - do not replace it with fixed `39 passed`;
   - require focused pytest exit status zero;
   - require the maintained test-module/evidence-ID inventory independently;
   - if a count is reported, compare it with the count observed from the same
     recorded run rather than a number embedded in validator source.

Add focused negative tests proving:

- an imported validator may create `__pycache__` without causing leakage-scan
  failure;
- a declared maintained textual resource with invalid UTF-8 still fails;
- generated `.pyc` and `.pyo` files are ignored;
- a nonzero focused pytest result fails completion;
- a passing focused suite is accepted without a hard-coded total;
- a falsified reported test count is rejected when a count is retained.

Then:

1. create exactly one R4 containing these corrections;
2. execute one isolated replay of R4;
3. create E4 referencing R4;
4. run focused tests, Ruff, mypy, H3 validation, live-consumer aggregation,
   rollback proof, and H4 completion;
5. request one targeted integration confirmation;
6. if all pass, perform the already authorized controlled local-route cutover,
   rerun the operational consumer and rollback proof, close H4, commit, push,
   and stop.

Keep the maintained route `legacy` until every R4/E4 gate passes.

Do not create R5/E5. If another material blocker appears, retain legacy, stop,
and report that H4 cutover is not ready rather than continuing replay iteration.

Do not activate P2, H5, scientific/external execution, publication, or release
work before successful H4 closure.
