# PI harness initialization reconciliation

## Authority and method

This initialization compared all nine maintained `docs/harness/` pages with `AGENTS.md`, the resolved P1 closeout, both controlling chains, current tasks/checkpoints, repository-local skills, ownership manifests/validators, Python packaging, and Sphinx/MyST policy. Documentation describes durable direction; `.pi` records own live state. No prospective statement is counted as implemented functionality.

## Authoritative status

- `P1-HC03` is resolved as Option A and P1 is closed as human-accepted `PASS`.
- No unresolved checkpoint existed at initialization.
- H0 is therefore activated as the sole harness task and is limited to read-only inventory/preflight.
- H1--H5 remain blocked.
- P2 now requires accepted P1, accepted H5, and separate explicit P2 activation. P2--P11 remain blocked.

## Findings

### INIT-F001 — prospective paths do not exist

The nine supplied harness pages were not recreated or substantively rewritten. During integration, one redundant trailing blank line was removed from pages `.00`--`.07` solely to satisfy the required `git diff --check` gate; the baseline retains both original supplied hashes and integrated hashes.

The four planned implementation/resource roots do not exist:

- `python/src/ksdft2effmass/harness/pi/`;
- `python/src/ksdft2effmass/harness/pi/local/`;
- `harness/pi/`;
- `harness/local/`.

Disposition: expected prospective architecture, not missing implementation. H0 must inventory requirements; H1 must approve a contract before H2/H3 create these roots.

### INIT-F002 — prospective interfaces are not implemented

The profile, record, resource-manifest, structured result, generic validator, package candidate, CLI, shadow replay, and extraction interfaces in pages `.02`--`.08` are proposals. Current scripts and schemas are requirements evidence only.

Disposition: retain as prospective; do not report functionality until its authorized task implements and verifies it.

### INIT-F003 — evidence surface vocabulary differs

`docs/harness/ksdft2effmass.harness.05.md` includes a distinct `boundary` test-function surface. The currently accepted shared test-evidence grammar uses `artifact` for maintained P1 boundary-owned modules and does not list `boundary` as an allowed function surface.

Disposition: material contract choice deferred to H0 classification and the H1 human checkpoint. Initialization does not change historical/current test names or either convention.

### INIT-F004 — generic skill proposal overlaps current owners

The proposed `write-research-evidence-tests` resource in page `.04` overlaps current responsibilities in `document-research-python`, `develop-operator-records`, `audit_evidence_identifiers.py`, P1 ownership validators, and task-ownership tooling.

Disposition: H0 must classify each responsibility and identify one source of truth before H1. No skill is created, moved, retired, or duplicated during initialization.

### INIT-F005 — current validators mix generic and project-local policy

The version-2 task-ownership schema/validator is mostly generic but defaults to a repository-specific chain and agent-record format. The version-1 path and P1 evidence validators embed P1 identities, class inventories, filenames, evidence prefixes, and migration history. The skill-capability validator embeds the current six-skill and CPN block inventories.

Disposition: H0 classification required. Do not extract these files wholesale or treat the existing decomposition as the future API.

### INIT-F006 — stale and duplicated control state existed

The backend-neutral chain retained a stale resolved EVIDENCE-DOC checkpoint in `pending_checkpoints`, and the P1 task retained stale prose saying that accepted EVIDENCE-DOC-1 still awaited acceptance.

Disposition: deterministic status correction applied during initialization. Historical checkpoint/evidence files were not rewritten.

### INIT-F007 — H2/H3 sequencing requires authoritative clarification

Harness page `.00` renders H2 then H3 linearly, while the authorized project sequence permits H2 and H3 after accepted H1 and allows concurrency only with disjoint validated ownership.

Disposition: the live harness chain is authoritative and records H2/H3 as sibling tasks after H1, with concurrency disabled until accepted H1 plus disjoint validated manifests. The architecture page is not rewritten during initialization; H0/H1 must decide whether its durable diagram needs later clarification.

### INIT-F008 — current agents do not establish future harness ownership

Current implementation/test agents are specialized for operator-record and CPN paths. Their agent records do not authorize future generic harness Python/resource paths.

Disposition: H0 remains parent-operated read-only preflight. H1 must establish task-specific agent/path ownership before H2 or H3 implementation. No production ownership is inferred from technical tool access.

### INIT-F009 — documentation collection gap

Sphinx previously did not collect `docs/harness/`. All 30 relative links within the nine-page set resolve.

Disposition: authorized later documentation-policy extension applied by adding exactly `harness/ksdft2effmass.harness.*.md` and the toctree target `harness/ksdft2effmass.harness.00`. Broad Markdown collection remains prohibited. Closed P0A evidence remains historical and unchanged.

### INIT-F010 — project-specific content must remain local

Current skills, validators, manifests, and records contain CPN IDs, operator terminology, repository roots, pytest markers, P0--P11 identities, `.pi` assumptions, and ksdft2effmass agent routing.

Disposition: H0 must classify these as split/local/deferred as appropriate. Generic resources and Python may receive such information only through explicit profiles or caller-supplied paths.

## Conflicts requiring later human decision

No conflict blocks project initialization or read-only H0 activation because the human instruction fixes the project boundary, H0--H5 dependency sequence, P2 gate, and initialization scope. H0 must carry INIT-F003, INIT-F004, INIT-F005, INIT-F007, INIT-F008, and INIT-F010 into its concluding genuine human checkpoint. They must not be silently resolved during inventory.

## Nonmutation boundary

Initialization adds control-plane records, documentation collection/navigation, reconciliation evidence, validators, and checksums only. It creates no harness Python/resource implementation, changes no dependency or lockfile, and changes no production source, specification, fixture, or test.
