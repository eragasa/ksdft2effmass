# Context-Management and Coordination-Overhead Instrument

## Purpose

This instrument records how explicit context management affects coordination,
recovery, rework, and defect interception during a development episode. It does
not assume that every harness artifact is beneficial or that every observed
correction was caused by the harness.

## Observation modes

| Mode | Meaning |
| --- | --- |
| `contemporaneous` | Recorded while the episode and relevant event were active |
| `retrospective_repository` | Derived later from versioned repository evidence |
| `mixed` | Some fields were contemporaneous and others retrospectively coded |
| `not_recorded` | The evidence does not support the observation |

## Observed quantities

- episode start and end revisions;
- participating agent roles;
- subagent dispatches and their task boundaries;
- handoffs between roles or contexts;
- repository skills invoked;
- protected checkpoints and human decisions;
- parent-agent interventions;
- corrective cycles and redispatches;
- context-loss, ambiguity, or missing-state events;
- recovery from repository evidence;
- fresh-session reconstruction probes;
- coordination-only artifacts;
- implementation, verification, and human-disposition outcomes.

## Derived coordination load

For episode $e$, define

$$
\mathbf L_C^{(e)}
=
\left(
N_{\mathrm{dispatch}}^{(e)},
N_{\mathrm{handoff}}^{(e)},
N_{\mathrm{skill}}^{(e)},
N_{\mathrm{checkpoint}}^{(e)},
N_{\mathrm{intervention}}^{(e)},
N_{\mathrm{rework}}^{(e)}
\right).
$$

Each count must state its source paths and derivation rule. Counts are not
equivalent to time, cognitive effort, token consumption, or economic cost.

## Missing-data rules

- Never infer prompts, model identifiers, timestamps, active time, runtimes, or
  token counts from file order or commit count.
- Use `null`, `unknown`, `not recorded`, or the episode schema's equivalent
  whenever evidence is unavailable.
- Historical records are not rewritten to create measurements that were not
  collected.
- A derived count must be reproducible from retained paths at the cited
  revision.

## Interpretation boundaries

- A large coordination load does not by itself establish waste.
- A successful task does not establish that the harness caused success.
- A defect found during review supports defect interception only when the
  finding and correction are retained.
- Recovery is established only when the required state is reconstructed from
  declared durable evidence without relying on unavailable conversational
  history.
- Reduced total cost requires comparable measurements across episodes or a
  defensible counterfactual; it must not be inferred from artifact counts alone.

