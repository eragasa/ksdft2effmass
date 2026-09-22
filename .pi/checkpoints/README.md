# Human checkpoints

This directory stores durable, machine-readable checkpoints for genuine human
decisions. Checkpoints are operational control-plane records, not scientific
specifications or research results.

Use `checkpoint.schema.json` for every checkpoint JSON file. A checkpoint records
only the decision-bearing human message, necessary context, normalized outcome,
consequences, and evidence paths. Do not store full chat transcripts.

## Decision classes

- `deterministic_agent_correction`: the agent corrects, records, revalidates,
  and continues without a checkpoint because authoritative policy uniquely
  determines the correction.
- `standing_delegated_decision`: the agent cites a durable human policy that
  already resolves the choice, records the action, revalidates, and continues.
- `genuine_human_decision`: the agent creates or keeps a checkpoint because at
  least two materially different defensible options remain and the choice affects
  protected human authority.

New sessions must inspect unresolved checkpoints before invoking
`recommend-next-task`. If the current human message resolves a persisted checkpoint,
the `resolve-human-checkpoint` skill records the decision and resumes the blocked
task automatically.
