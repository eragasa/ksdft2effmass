# Deterministic stale-claim audit

## Scope and method

This audit searches the current authoritative and maintained files named by
`HARNESS-SEQ-HC01` for sibling/concurrency, dual H2/H3 prerequisites, H5-before-P2,
and automatic-activation claims. It separately searches immutable H0 records and
evidence. Matching is textual screening; the classifications below were checked
against the complete matched lines.

Commands:

```bash
rg -n -i 'H2.*H3|H3.*H2|concurr|eligible_tasks|accepted H2.*accepted H3|H5:human_accepted|accepted H5.*P2|P2.*accepted H5|P2.*H5|H5.*P2|automatic.*P2|P2.*automatic|H5 closure' \
  AGENTS.md .pi/chains/pi-harness-incubation.chain.json \
  .pi/chains/backend-neutral-kohn-sham-qe.chain.json \
  .pi/tasks/pi-harness-incubation-H{1-contract,2-python-core,3-resources,4-local-shadow-cutover,5-extraction-readiness}.md \
  .pi/tasks/backend-neutral-cpn-P2-tools-provenance.md \
  docs/harness/ksdft2effmass.harness.0{0,1,2,3,4,5,6,7,8}.md

rg -n -i 'concurr|eligible_tasks|H5:human_accepted|accepted H5.*P2|P2.*accepted H5|P2.*H5|H5.*P2|H2.*H3|H3.*H2' \
  .pi/evidence/pi-harness-incubation/H0 \
  .pi/checkpoints/H0-HC01-harness-inventory-and-h1-scope.json \
  .pi/tasks/pi-harness-incubation-H0-inventory.md
```

## Classification of current authoritative matches

| Match family | Classification | Disposition |
| --- | --- | --- |
| H1/H2/H3 order and non-overlap in `AGENTS.md`, both chains, H1--H3 tasks, and `.00.md`/`.04.md` | corrected authoritative state or corrected maintained documentation | All state H1 -> H3 -> H2; no sibling or alternative concurrency route remains. |
| H4 prerequisite and downstream P2/H5 branching in both chains and H4 task | corrected authoritative state | H4 requires accepted H2; accepted H4 activates neither branch. |
| P2/H5 mentions in `AGENTS.md`, both chains, H4/H5/P2 tasks, `.00.md`, and `.08.md` | corrected authoritative state or corrected maintained documentation | Every match says H5 is optional/not a P2 prerequisite, or that P2/H5 require separate activation. |
| `automatic_*` fields in the harness chain and automatic-activation prose in both chains/`.08.md` | corrected authoritative state or corrected maintained documentation | Every automatic activation flag is false. |
| “concurrently edited working notes” in H1 and harness documentation | unrelated context | These matches concern excluded personal worktree provenance, not H2/H3 execution concurrency. |
| “non-overlapping writer/reviewer ownership” in H1 | unrelated context | This is path-ownership safety, not a task-concurrency route. |

No `eligible_tasks` field, H2/H3 sibling prerequisite set, dual H4 prerequisite,
`H5:human_accepted` P2 prerequisite, accepted-H5-before-P2 rule, or unexplained
automatic-activation claim remains in current authoritative or maintained files.

## Classification of historical matches

Every match under `.pi/evidence/pi-harness-incubation/H0/`, the immutable
`.pi/checkpoints/H0-HC01-harness-inventory-and-h1-scope.json`, and
`.pi/tasks/pi-harness-incubation-H0-inventory.md` is **retained historical
evidence**. These records report the pre-decision inventory, then-current sibling
and P2-gate state, or the accepted H3-before-H2 recommendation. They were not
modified. In particular, historical `validate_h0.py` still encodes the old
pre-acceptance H5-before-P2 assertion; it is retained evidence and is not a
current post-reconciliation validator.

## Result

**PASS:** every match is classified as corrected authoritative state, corrected
maintained documentation, retained historical evidence, or unrelated context.
No unexplained live authoritative match remains.
