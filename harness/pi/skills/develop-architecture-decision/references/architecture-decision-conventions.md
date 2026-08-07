# Architecture decision conventions

## Claim and authority discipline

An architecture decision artifact is advisory. Label material claims as **Observed fact**, **Inference**, **Human choice**, **Implementation consequence**, or **Deferred question**. Cite repository paths for observed facts. Apply the repository's authority order and report conflicting accepted identities without choosing between them. Historical evidence describes prior events; it does not establish current authority or ownership.

Do not collapse authority, ownership, dependency, state, persistence, dispatch, history, migration, and runtime into a single implementation preference. Do not introduce scientific meaning, numerical results, VVUQ claims, dependencies, execution authority, or release authority.

## Applicability and option identity

An applicable decision has exactly three materially distinct, defensible conceptual architectures. They must differ in consequential allocation or flow across the architecture dimensions, not merely by flags, filenames, environment values, provider selection, deployment size, or other configuration. A status-quo option is permitted only when it satisfies the declared requirements and is honestly defensible.

Before drafting, build a private identity table spanning:

1. authority and decision rights;
2. owner and dependency direction;
3. mutable and immutable state;
4. persistence boundary and format;
5. dispatch/runtime control flow;
6. retained history and provenance;
7. migration and compatibility; and
8. failure recovery and reversibility.

If the table cannot establish three distinct defensible architectures, return `deterministic`, `underspecified`, or `unsuitable`, name the missing or controlling information, and stop without a checkpoint.

## Exact decision-document structure

Use these level-two headings exactly once, in this order, with no additional level-two headings:

## Problem
## Observed current behavior
## Decision requirements
## Option A
## Option B
## Option C
## Three-option comparison
## Recommendation
## Deferred questions
## Human decision required

`Observed current behavior` separates facts from inferences. `Decision requirements` separates accepted requirements from human choices still open.

Each Option A/B/C section must include these labeled items exactly once:

- **Conceptual model**
- **Authority**
- **Ownership/dependency**
- **Runtime/dispatch**
- **Migration**
- **Reversibility**
- **Failures**
- **Complexity**
- **Maintenance**
- **Context-window consequences**
- **Future compatibility**
- **Advantage**
- **Risk**

Discuss state, persistence, and history explicitly within the conceptual, runtime/dispatch, migration, or failure facets. The comparison uses the same criteria and factual baseline for A, B, and C. Make exactly one recommendation; preserve all three options after recommending.

## Checkpoint proposal

The checkpoint is a concise decision interface, not a duplicate decision analysis. It cites the decision-document path and presents:

- `A — <actual summarized Option A architecture>`;
- `B — <actual summarized Option B architecture>`;
- `C — <actual summarized Option C architecture>`; and
- `D — Reconsider or defer`.

The summaries must distinguish actual conceptual models. Never substitute generic accept, correct, reject, approve, revise, or fail choices. Do not persist a final checkpoint unless a separate authority explicitly assigns that write.

## CPN request, result, retry, and idempotency

The immutable request binds `request_identity`, `task_id`, `parent_workflow_id`, `attempt_id`, requested capability, artifact identities, authority inputs, expected output schema/paths, permitted mutation scope (none), and termination policy. Guard evaluation may inspect tokens but may not invoke the skill.

A success result correlates those identities and records skill identity/hash, input identities, the decision-document and checkpoint-proposal artifacts, recommendation, commands/results, warnings, empty mutation summary, and `stop_before_implementation`. A failure retains partial findings and classifies conflict, missing input, deterministic, underspecified, unsuitable, or malformed request as applicable.

Retry requires immutable authorization, a new attempt identity, and retained prior results. Identical artifact identities yield observationally idempotent read-only analysis; changed inputs require a new request snapshot. Never overwrite successor results or historical findings.

## Exclusions

Do not implement or select an option; alter ownership, dispatch, persistence, dependencies, history, runtime, or release state; activate successor work; create configuration variants to reach three; duplicate the analysis in the checkpoint; or infer VVUQ, scientific correctness, successful execution, or human acceptance from this procedure.
