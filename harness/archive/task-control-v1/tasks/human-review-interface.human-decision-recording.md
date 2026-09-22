# Implement pure human decision recording

Status: architecture_corrected_awaiting_human_review under `.pi/chains/human-review-interface.chain.json`

Task identity: `human-review-interface.human-decision-recording`

Starting revision: `ecd260042257efb868ad4262cc3a1b9a0159c16b` (`origin/dev`, synchronized with a clean worktree).

Prerequisite: the corrected AuditEvidenceIdentifiers review-packet pilot is recorded as `human_accepted_pass`; HRI-PILOT-F01 and HRI-PILOT-F02 are resolved.

This bounded slice adds the immutable public `HumanReviewDecision` ResultObject and fieldless `HumanReviewDecisionRecorder` ActionObject. Following the human-requested architecture correction, the decision stores the exact immutable packet itself, exact human response, caller-supplied normalized disposition, and contract-compatible explicit scope. Recording reconstructs the canonical `HumanReviewPreparer` result and rejects a packet whose relationships, ordering, or derived status differ. Recording performs no natural-language interpretation, authority inference, persistence, filesystem or Git action, checkpoint mutation, or successor activation.

The maintained demonstration is `.pi/evidence/human-review-interface/audit-evidence-identifiers-pilot-decision.md`. It represents the accepted corrected pilot decision as software verification only and does not define a JSON wire format.

Focused software-verification evidence, public imports, maintained structural evidence validation, Ruff, mypy, deterministic repeated construction, exact response preservation, packet nonmutation, profile/resource identity, documentation links, control-plane parsing, dependency identity, and diff checks are required before handoff.

A possible `human-review-interface.persistence-evaluation` remains proposed and inactive. This task does not authorize JSON serialization, schemas, SQLite, checkpoints, reviewer spawning, successor activation, scientific work, or protected work. The corrected implementation returns for direct human review. The correction also renames the failed-check packet status to `blocked_by_failed_observation`, makes `HumanReviewDecisionRecorder` the sole public recording ActionObject name without a compatibility alias, and preserves the inactive item-level proposal as a distinct future session architecture rather than redefining current public packet and decision types.
