# Task catalog configuration — implementation progress

## Scope and authority

The active Task is `harness.task-catalog-configuration`. The human continuation in
`harness/intake/task-catalog-configuration.md` authorizes implementation under the
approved compatibility and classification choices. The parent is the sole writer;
no delegation, independent review, Task acceptance, Git closeout or protected
execution is claimed. `harness.task-status-details` remains inactive and outside
this implementation scope.

This record covers the **configuration value/wire slice**, not complete catalog
support or relocation. The live source and canonical Task locations are unchanged.

## Implemented boundary

- Public immutable `TaskCatalogConfiguration` with explicit research, simulation
  and software roots; exact built-in strings, existing lexical path rules and
  pairwise component-aware/case-folded non-overlap.
- Backward-compatible four-argument `HarnessCatalogConfiguration` construction,
  with an appended optional categorized component and exactly-one-layout rule.
- Source/resolved configuration schema 1 for flat roots and schema 2 for categorized
  roots. Both constructors enforce version/layout agreement. Both serializer pairs
  enforce exact members, ordering, scalar semantics and canonical bytes.
- Source resolution preserves the configuration version. Resolution-result schema,
  normalized Pi schema and snapshot framing remain version 1.
- A closed recursive JSON representation and owned codec replace affected erased
  wire dictionaries. Existing module-level behavior is now owned by configuration
  values, the lexical path policy, codec or resolver; no new generic registry,
  reflective lookup or unspecified-value boundary was introduced.
- Until the complete consumer slice is implemented, the existing control entry
  points reject categorized configuration explicitly before publication. They do
  not silently discover the legacy root. These temporary guards and their dedicated
  evidence must be replaced by positive consumer-integration evidence, not retained
  as the finished capability.

## Software evidence and documentation

Four literal wire fixtures live under
`python/tests/software_verification/ksdft2effmass/harness/resources/`:
`configuration-source-v1.json`, `configuration-source-v2.json`,
`configuration-resolved-v1.json` and `configuration-resolved-v2.json`. They were
not emitted by production serialization. Schema-1 source bytes preserve the
pre-cutover source; schema-2 fixtures use alternate catalog names.

The explicit test ownership file is `resources/task-catalog-configuration-ownership.json`
in that test tree. It binds four modules and 21 evidence owners covering intrinsic
values, catalog composition, source/resolved wire agreement and the interim CLI
refusal gate. The existing public export inventory is synchronized; the existing
legacy configuration tests, including their fixed snapshot digest, are preserved.

Documentation profile: **AUTHORIZED_DOCS_WRITE**. Authorized documentation paths
are `docs/api/harness-control.rst`,
`docs/architecture/v2/ksdft2effmass/harness/configuration.md`, and affected public
source docstrings in `python/src/ksdft2effmass/harness/configuration.py`. Public API
pages distinguish representable configuration from pending consumer support.
Immutable source/test/documentation identities and command logs are retained under
`/var/folders/42/g1m9r43x2_v4bkyg4csrsn100000gn/T/task-catalog-configuration-implementation.q93l2k46/`.

Checks passed: focused configuration/public-API tests (78 cases), strict mypy on
11 affected files, Ruff on those files, test conformance for all four new modules
(21 evidence owners), and Sphinx dummy/HTML with warnings as errors. The corrected
full suite reports **4,704 passed and three unchanged external-QEXSD skips in
81.55 seconds**. This is software verification, not external-artifact validation.
Final control checks use maintained projection sync/check, `validate-harness`,
exact Task inspection and `git diff --check`.

Initial structural/lint findings were corrected without weakening assertions;
wrong-type and invalid-value wire partitions now have separate evidence owners.
The first full run found that inserting the new public export among existing
exports shifted an existing prerequisite API slice. Appending the new export
instead preserves all existing export positions; the original prerequisite test
was left unchanged. The focused API regression and full suite then passed.
A newly added Task authority-reference path was also sorted before successful
projection synchronization. Failed attempts remain in the retained logs where
available; passing gates do not imply those initial attempts passed.

The additional broader compiler-ownership conformance diagnostic is **FAIL**, not
waived or relabeled PASS: two TEST_NAME and three HIDDEN_LOOP findings in the
unchanged `test__HarnessCompiler.py` and `test__HarnessRepositoryLoader.py` modules.
Their source identities and the validator sources match the pre-operation baseline;
`inherited-compiler-conformance.json` retains that comparison and the findings.
The changed public export inventory has no findings in this run. This inherited
compiler-evidence debt is **SAFE_TO_DEFER** for the configuration-only slice;
revisit under those evidence owners when changing their tests or undertaking
repository-wide conformance migration. The passing four-module catalog conformance
gate is distinct from this failing broader diagnostic.

## Parent adversarial checks and remaining work

The parent challenged shared-version relaxation, decoder/encoder agreement hiding
wrong field mappings, path-prefix confusion, and wire support being mistaken for
working discovery. Evidence uses independent literal bytes plus explicit expected
values, version/layout and Pi/result rejection cases, alias/near-prefix partitions,
and real CLI refusal cases. These checks are software verification, not independent
review, exhaustive security testing or scientific validation.

Consumer integration, actual source-path retention, duplicate/global-ID checks,
filesystem confinement, ownership-schema/live-reference updates and guarded
relocation remain required by the plan. No current check establishes their
completion or eliminates the separately deferred filesystem race concern.

For this bounded value/wire slice, the parent self-assessment is
**ReviewOutcome: NO_BLOCKING_FINDINGS** and **OperatorRequest: NONE**. This is not
an independent review or a whole-Task completion verdict. The explicit guards,
legacy byte oracle and version-boundary cases address the examined concerns
(**NO_ACTION_REQUIRED** at this slice). Remaining consumer implementation is
required work, not waived debt; the existing filesystem race concern remains
**SAFE_TO_DEFER** only within its previously declared scope and revisit condition.

The migration map is refreshed to 217 Tasks by adding the separately requested
status-details software Task. Existing five human-confirmed classifications remain
unchanged. Inventories are observations, not execution authority; recheck them at
cutover, preserve historical evidence, and do not rewrite signed/checksummed records.
