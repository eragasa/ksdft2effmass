# P2-A03 ExternalExecutionStatus partial correction

Status: **deterministic validation passed; P2-A03 remains open**

Starting revision: `e6640d81c6e500698547eb72ccdea3fc508509db`.

The completed human file-level audit authorized correction of only
`test__ExternalExecutionStatus.py`. Production
`external_execution.py` remained byte-identical at SHA-256
`432cda6da77b46a9441b7f0465b789423bba3dc77f8b9c696ff368e9c55024c9`.

The correction preserves `SV-PROV-042`, `SV-PROV-182`, `SV-PROV-183`, and
`SV-PROV-184`. New `SV-PROV-282` owns successful declared-name lookup; new
`SV-PROV-283` owns wrong-semantic-type value construction. Five historical
collected nodes map one-to-one to closest current successors, while the newly
independent successful name-lookup owner has no historical predecessor.

The module now has six direct, unparameterized evidence owners: exact vocabulary,
value construction, name lookup, unknown-value rejection, wrong-type rejection,
and unknown-name rejection. It uses concrete `field`, `method__call`, and
`method__getitem` surfaces, a literal public-member oracle, exact exception
categories, specific seven-field prose, and no Ruff suppression.

Validation results:

- supplied-path structural validator: PASS; one class-owned module, six evidence
  owners, no helpers, no parameterized functions, and zero findings;
- exact collection and execution: six collected, six passed;
- diagnostic module coverage while exercising `ExternalExecutionStatus`: 15%
  overall for `external_execution.py` (225 statements, 166 missed, 158 branches,
  zero partial); all status vocabulary and lookup/rejection behavior was directly
  exercised, while unrelated request/result/failure classes were intentionally
  outside this one-module correction;
- Ruff format and lint: PASS;
- focused mypy over production and the corrected test: PASS;
- public package import/API module: three passed;
- production hash and unrelated-file preservation: PASS;
- `git diff --check`: PASS.

The other five P2-A03 modules remain untouched and unaudited. The next human
file-level audit target is `test__ExternalFailureStage.py`. P2-A03 remains
`pending_read_only_audit`; P2-HC06 remains pending and is not superseded.
