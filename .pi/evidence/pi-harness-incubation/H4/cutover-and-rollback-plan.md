# H4 cutover and rollback plan

## Current decision

The H4 test/parity writer gates pass after deterministic handoffs. All selected shadow pairs are `equivalent` or cited `intentional`; none is `defect` or `deferred`. The retained legacy route remains authoritative until required independent review and human H4 acceptance/cutover. This evidence does not itself authorize cutover.

## Verified cutover prerequisites

- The local package exports exactly 30 names, including `EvidenceOwnershipRelation` and `AdaptEvidenceOwnershipManifest`; the accepted generic package remains exactly 41 names.
- Explicit current-tree roots load the v2 profile/manifests without ambient discovery.
- The retained P1 task ownership manifest passes `AdaptOwnershipManifest`.
- The separately retained P1 test-ownership manifest passes `AdaptEvidenceOwnershipManifest`; `boundary_owned` becomes `artifact_owned` agreement metadata with exact left/right identities, direction `none`, and preserved `SV-CPN-027`, `028`, `087`, and `088`.
- `AdaptSkillInventory` selects only the explicitly supplied `document-python-research-software` descriptor. The separate live validator establishes six canonical skill identities.
- The v2 profile supports `SV-HL-001..013`; generic H4 evidence audit reports 13 occurrences and zero issues.
- Focused tests, H3/skill/checkpoint/ownership validators, Ruff, mypy, checksums, and the H4 completion gate pass as recorded in `validation-results.json`.

## Controlled cutover

The concrete consumer is `.pi/skills/validate_harness.py`; the single persistent route owner is `harness/local/validation-route.json`. Before human acceptance it must remain `{"rollback_route":"legacy","route":"legacy","schema_version":1}`. The retained replay program exposes `--side legacy --no-write` and `--side local --no-write`, so the consumer can invoke the identical exact eight-pair suite without mutating retained evidence. After independent reviewers report no blockers and the human H4 checkpoint authorizes cutover, change only the route owner's `route` value to `local`, then invoke the consumer with absolute `--repository-root` and `--route-config` paths. Retain legacy commands and accepted H1-H3 catalogs. Only clean-revision replay pairs classified equivalent or explicitly cited intentional may be routed authoritative.

## Rollback: route versus resources

Route rollback and resource restoration are deliberately distinct operations. `RollBackValidationRoute.execute(RouteConfiguration(ValidationRoute.LOCAL))` produces the pure legacy/legacy route decision; operational rollback changes only `harness/local/validation-route.json` back to `route: legacy` and reruns the consumer and replay side suite. This action does **not** restore deleted or renamed skill/profile resources. If old bytes are required, create a separate worktree or perform an explicitly authorized Git restoration from starting revision `de8659bc5858a52de8f866ec73a14487bf480432`; never describe route rollback as resource restoration. Accepted H1-H3 checksum catalogs remain historical rollback oracles, not current H4 parity inputs. Do not delete local tests or retained parity evidence.

## Stop conditions

Stop and retain legacy authority on any defect/deferred classification, unexpected checksum difference, nonzero selected H4 generic audit, ownership failure, missing explicit root, failed independent review, or absent human cutover authorization.
