# P2-A03 ExternalFailureStage partial correction

Status: **deterministic validation passed; P2-A03 remains open**

Starting revision: `134ee58a6a75182e0a425154c075291b7dd0ea91`.

The completed human file-level audit authorized correction of only
`test__ExternalFailureStage.py`. Production `external_execution.py` remained
byte-identical at SHA-256
`432cda6da77b46a9441b7f0465b789423bba3dc77f8b9c696ff368e9c55024c9`.

The correction preserves `SV-PROV-045`, `SV-PROV-185`, `SV-PROV-186`, and
`SV-PROV-187`. New `SV-PROV-284` owns successful declared-name lookup; new
`SV-PROV-285` owns wrong-semantic-type value construction. Seven historical
collected nodes map one-to-one to closest current successors. The three newly
independent successful name-lookup cases have no historical predecessors.

The module has six evidence owners and ten collected cases: exact vocabulary,
three value-construction cases, three name-lookup cases, and independent unknown
value, wrong-type, and unknown-name rejection. It uses concrete `field`,
`method__call`, and `method__getitem` surfaces and explicit public-member
oracles. A narrow `Any` cast is limited to enum class subscription because mypy
otherwise parses runtime `EnumType.__getitem__` syntax as type application; the
cast changes no runtime behavior.

Validation results:

- supplied-path structural validator: PASS; one class-owned module, six evidence
  owners, two parameterized functions, six static parameter cases, no helpers,
  and zero findings;
- exact collection and execution: ten collected, ten passed;
- diagnostic containing-module coverage: 15% for `external_execution.py` (225
  statements, 166 missed, 158 branches, zero partial); the branchless enum's
  exact vocabulary and inherited lookup/rejection behavior were directly
  exercised, while unrelated records were intentionally excluded;
- Ruff format and lint: PASS;
- focused mypy over production and corrected test: PASS after the documented
  narrow class-subscription cast;
- public package import/API module: three passed;
- production hash, unrelated-module preservation, and `git diff --check`: PASS.

The durable `ExternalExecutionStatus` correction remains unchanged. The other
four P2-A03 modules remain untouched and incomplete. The next human-audit target
is `test__ExternalFailureCode.py`. P2-A03 remains `pending_read_only_audit`;
P2-HC06 remains pending and is not superseded.
