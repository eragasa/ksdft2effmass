# Proposed repository changes

## Research question

Add this as RQ6 in
`docs/research/agentic-development-case-study/research-questions.md`:

```md
6. What coordination overhead is introduced by skills, role-separated
   subagents, checkpoints, and durable repository records, and what context
   reconstruction, rework, or integration failures do these mechanisms prevent
   or make recoverable?
```

## Propositions

Add these as propositions for examination, not conclusions:

```md
- externalizing task state shifts work from implicit context reconstruction to
  explicit, inspectable coordination;
- role-separated subagents preserve bounded working sets but increase handoff
  and integration cost;
- stable, reusable skills reduce the marginal cost of reloading procedural
  constraints;
- excessively fine task or checkpoint granularity increases coordination cost
  without necessarily improving defect interception or recoverability.
```

## Protocol addition

Add a section titled `Context-management evidence` to `protocol.md`. It should
state:

- observations are recorded at episode boundaries and protected decision
  boundaries;
- contemporaneous observations are distinguished from retrospective coding of
  repository artifacts;
- timestamps, model identifiers, token counts, runtimes, and prompts are never
  inferred when unavailable;
- event and artifact counts are preferred over unsupported estimates of active
  time;
- corrective cycles, checkpoints, and human interventions already represented
  elsewhere in an episode record are referenced rather than duplicated;
- causal claims require evidence of a mechanism, not merely correlation between
  a large harness and a successful task.

## Episode ordering

The episode identifiers should follow actual execution order:

| Episode | Task | Current evidence status |
| --- | --- | --- |
| `E03` | H0 inventory and ownership classification | Accepted; abstract retrospectively from contemporaneous H0 evidence |
| `E04` | H1 public contract | Accepted; abstract retrospectively from contemporaneous H1 evidence |
| `E05` | H3 textual resources | Accepted; abstract retrospectively from contemporaneous H3 evidence |
| `E06` | H2 generic Python harness | Active; use mixed measurement mode because the context instrument was introduced after activation |
| `E07` | H4 local integration and cutover | Future |
| `E08` | H5 extraction readiness | Future |

## Measurement representation

Do not initially collapse context-management cost into a single scalar. Record
the coordination-load vector

$$
\mathbf L_C
=
\left(
N_{\mathrm{dispatch}},
N_{\mathrm{handoff}},
N_{\mathrm{skill}},
N_{\mathrm{checkpoint}},
N_{\mathrm{intervention}},
N_{\mathrm{rework}}
\right).
$$

The components are counts of subagent dispatches, handoffs, skill invocations,
protected checkpoints, parent or human interventions, and corrective cycles.
Every count must identify its derivation rule and source artifacts.

Time- or token-based ratios may be added only when measurements are available
and consistently defined across episodes.

## Case-register publication metadata

Add metadata equivalent to:

```json
{
  "preprint_target": "arXiv",
  "primary_category": "cs.SE",
  "preprint_status": "planned",
  "manuscript_path": "docs/publications/papers/agentic-development-case-study/"
}
```

Preserve the existing intended peer-reviewed target. arXiv is a preprint
repository, not a replacement for journal review.

