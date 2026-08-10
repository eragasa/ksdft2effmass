# Human intake: retire the H3 operational validator

The authoritative Task-local record is [`harness.simplification.resources.h3-validator-retirement.json`](harness.simplification.resources.h3-validator-retirement.json). This intake preserves the human-requested implementation boundary but is not an activation, status, completion, successor-selection, or acceptance record.

Retire `harness/pi/validation/validate_h3_resources.py` from current operation rather than merely repairing its two failures. Inventory every H3 gate first in a durable machine-readable disposition map. Preserve every still-valid resource contract through an appropriate maintained DataObject, ResultObject, ActionObject, focused test, or thin explicit-input CLI. Preserve historical H3 evidence unchanged.

Remove live manifest/profile registration, `current-h3-resources` replay dispatch, live H2/H4 completion or route dependencies, current-gate documentation, and obsolete phase terminology. Preserve generic and local manifests, schemas, valid and invalid fixtures, canonical vectors, project profiles, skill descriptors and references, current resource contracts, and accepted historical H3 tasks, checkpoints, reviews, checksums, and evidence.

Classify each current H3 failure as exactly one of `CURRENT_RESOURCE_CONTRACT_DEFECT`, `MISSING_FOCUSED_VALIDATION`, `OBSOLETE_H3_ONLY_INVARIANT`, or `HISTORICAL_EVIDENCE_INCONSISTENCY`. Do not make the old validator pass for its own sake.

Replace phase-era replay with maintained current harness validation composition using explicit repository/resource roots and profiles, structured immutable results, deterministic ordering, correct nested-failure propagation, separate invalid-input and internal-failure handling, no Git mutation, and no implicit working-directory authority. Prefer existing resource, profile, checksum, skill-resource, path-resolution, and serialization Actions. Generic executable logic belongs in `python/src/ksdft2effmass/harness/pi/`; project-local composition belongs in `python/src/ksdft2effmass/harness/pi/local/`.

Inspect all live callers, including the current replay wrapper, H4 route and replay tests, and `validate_h2_completion.py`. Use at most one final read-only harness integration review. Validate ownership of every retained gate, generic/local dependency direction, resource validity, nested failure propagation, focused tests, public imports, Ruff, focused mypy, documentation links, `git diff --check`, unchanged dependencies, absence of live validator references, and unchanged historical H3 evidence.

Delete the historical validator only after the disposition map is complete, every retained requirement has a current owner, live callers use the replacement, focused validation passes, and the bounded review has no unresolved material defect. Stop if a valid requirement has no coherent maintained owner without material scope expansion.

The parent documentation/JSON pilot's pending integration review completed and failed on the two H3 findings recorded in `.pi/evidence/docs-json/parent-integration-review.md`. The current human authorization treats completion of that review—not a passing result—as satisfying this Task's review precondition. The findings remain unchanged correction inputs; they are not reinterpreted as a pass.
