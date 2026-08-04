# Architecture Review — PI Harness Initialization

## Verdict: PASS

The initialization is internally consistent and remains bounded to control-plane records, maintained documentation, and verification evidence. No harness production implementation, scientific implementation, dependency change, package extraction/publication, or scientific execution began.

## Scope and identity

- Review profile: read-only architecture review
- Project: `pi-harness-incubation`
- Active task: H0 read-only inventory/preflight
- Attempt: `01329831`
- Skill: `design-data-action-objects`
- Skill SHA-256: `d501c3ce01d16481958833753326751f3a7789e0ad0ebef601b41934cb1e88db`
- Mutations by reviewer: none

## Findings

### Blocker / high severity

None.

### Medium severity — retained future decisions, not initialization failures

1. **H2/H3 documentation ordering remains intentionally ambiguous.**
   `docs/harness/ksdft2effmass.harness.00.md`, under “Project sequence,” renders H2 followed by H3. The authoritative `.pi/chains/pi-harness-incubation.chain.json` instead defines H2 and H3 as siblings after accepted H1, with concurrency permitted only after independently validated, disjoint ownership manifests establish safe repository concurrency. This conflict is correctly retained as `INIT-F007` in `.pi/evidence/pi-harness-incubation/initialization/reconciliation-findings.md`.

   **Required correction:** H0/H1 must decide whether the durable diagram should show sibling/concurrent eligibility. Until then, the chain controls and concurrency remains unauthorized.

2. **Future H2/H3 production ownership is not yet established.**
   `.pi/tasks/pi-harness-incubation-H2-python-core.md` and `pi-harness-incubation-H3-resources.md` require future task-specific ownership manifests, but `.pi/chains/pi-harness-incubation.chain.json` does not yet name them. Current agent records do not authorize the planned generic/local implementation paths, as recorded by `INIT-F008`.

   This is not a defect for initialization or read-only H0, and the production ownership preflight must not be demanded here.

   **Required correction before H2/H3 launch:** add chain-bound manifests naming separate implementation, test, and documentation writers plus independent read-only reviewers; declare non-overlapping paths and deterministic completion validators; run each task’s ownership preflight. H2/H3 concurrency must remain disabled unless both manifests independently pass and prove disjoint ownership.

### Low severity / residual control risks

3. **Initialization baseline is worktree-relative rather than independently commit-derived.**
   `.pi/evidence/pi-harness-incubation/initialization/baseline.json` names initialization base commit `03400a4adf83e2444d744d57439d3cfe8848780d`, but `validate_initialization.py` compares current files with hashes stored in that baseline rather than independently reconstructing protected hashes from the named commit. It also inventories protected files through `git ls-files`, so an untracked file outside the four specifically prohibited prospective roots would not enter the aggregate.

   The reviewed `git status` and diff show no such protected changes, so this does not fail the present initialization.

   **Recommended hardening:** later bind baseline derivation to the recorded commit and separately reject untracked content under protected roots.

## Architecture assessment

### Task decomposition and dependencies

The decomposition is coherent:

- H0: read-only inventory and ownership classification;
- H1: human-approved contract and extraction boundary;
- H2: generic Python implementation;
- H3: generic/local textual-resource extraction;
- H4: local integration, shadow replay, and controlled cutover;
- H5: isolated extraction-readiness demonstration without publication.

The exact authoritative dependency graph is:

```text
P1 accepted → H0 → H1 → {H2, H3} → H4 → H5
```

H4 requires both accepted H2 and accepted H3. H5 requires accepted H4.

H2/H3 concurrency is not currently authorized. The activation gate correctly requires:

1. accepted H1;
2. independently validated task definitions/manifests;
3. disjoint path ownership;
4. demonstrated safe repository concurrency.

Otherwise they run sequentially.

### Generic/local boundaries

The planned ownership split is consistently stated across the chain, tasks, and documentation:

- generic Python: `python/src/ksdft2effmass/harness/pi/`;
- project-local Python: `python/src/ksdft2effmass/harness/pi/local/`;
- generic resources: `harness/pi/`;
- project-local resources: `harness/local/`;
- runtime state: `.pi/`;
- maintained architecture: `docs/harness/`.

The required dependency direction is project-local to generic. Generic code/resources must not import or implicitly discover project-local state. Profiles and resource roots must be explicit. H1 retains human authority over the public internal API, immutable record/action/result boundaries, serialization/version policies, structured errors, path confinement, and compatibility.

Potential overlap between H2’s optional local adapters and H4’s local integration is appropriately deferred to H1’s disjoint ownership plan.

### Documentation and `.pi` source-of-truth split

The split is explicit and consistent:

- `docs/harness/` owns maintained explanatory architecture;
- `.pi/tasks/` owns task scope/status;
- `.pi/checkpoints/` owns human decisions;
- `.pi/chains/` owns dependencies and authorization;
- `.pi/evidence/` owns retained evidence.

Prospective interfaces in `docs/harness/ksdft2effmass.harness.02.md` through `.08.md` are not treated as implemented capabilities. `AGENTS.md`, the harness chain, and reconciliation evidence reinforce this distinction.

### P2 gate

Both chains and the P2 task agree that P2 requires all three:

1. accepted P1;
2. accepted H5;
3. separate explicit P2 activation.

Accepted H5 cannot auto-launch P2. P2–P11 and production/scientific execution remain blocked.

### VVUQ classification

The classification is correct:

- software verification: required;
- numerical verification: only for an actual numerical algorithm;
- scientific validation: not applicable to the harness itself;
- uncertainty quantification: not applicable to the harness itself.

Shadow parity is correctly classified as software verification and not as scientific correctness.

### Retained H0/H1 conflicts

`INIT-F003`, `INIT-F004`, `INIT-F005`, `INIT-F007`, `INIT-F008`, and `INIT-F010` are explicitly retained for H0 classification and the later genuine human checkpoint. Initialization does not silently settle:

- `boundary` versus accepted evidence-surface vocabulary;
- overlap of the proposed evidence-writing skill with current owners;
- generic/project-local validator decomposition;
- H2/H3 diagram and concurrency representation;
- future ownership;
- project-specific leakage and profile boundaries.

### No implementation or scientific work

Confirmed by inspection and deterministic validation:

- no prospective Python/resource root exists;
- no `python/src/`, `python/tests/`, or `specification/` change appears in the current diff;
- `python/pyproject.toml` and `python/uv.lock` match the baseline;
- no dependency, lockfile, schema, fixture, scientific-source, or test mutation occurred;
- production execution and package publication remain false;
- no generated build output remains.

## Files inspected

- `AGENTS.md`
- `README.md`
- `.pi/chains/backend-neutral-kohn-sham-qe.chain.json`
- `.pi/chains/pi-harness-incubation.chain.json`
- `.pi/checkpoints/P1-HC03-final-acceptance.json`
- `.pi/evidence/backend-neutral-cpn-P1-contract/P1-HC03-resolution.json`
- all six `.pi/tasks/pi-harness-incubation-H*.md` records
- all nine `docs/harness/ksdft2effmass.harness.*.md` pages
- initialization reconciliation, baseline, and validator
- task-ownership README and validator
- skill-capability inventory and validator
- applicable architecture and operator-record skills
- current Git status and diff

## Residual risks

- H0/H1 still require protected human decisions on retained contract and ownership conflicts.
- H2/H3 must not launch without chain-bound validated ownership manifests.
- The linear H2→H3 documentation diagram may mislead readers until clarified.
- The initialization baseline validator could be hardened against commit-derivation and untracked-file gaps.
- Passing initialization checks establishes control-plane consistency only, not future implementation correctness, scientific validation, UQ, extraction readiness, or human acceptance of H0.
