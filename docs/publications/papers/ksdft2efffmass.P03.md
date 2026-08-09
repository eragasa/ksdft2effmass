---
title: Context-Preservation Overhead in Harness-Based Agentic Development
status: research-note
date: 2026-08-04
---

# Context-Preservation Overhead in Harness-Based Agentic Development

## Purpose

This note records a candidate empirical contribution for the agentic-development paper. The observation is that a substantial fraction of development effort may be spent constructing and refining the harness rather than modifying the scientific software itself. In a long-horizon workflow, however, the harness is not merely auxiliary automation. It acts as an external memory and coordination system for work that cannot remain simultaneously available within one model context window.

The paper should therefore treat harness friction as a measurable systems tradeoff, not simply as wasted effort or anecdotal inconvenience.

## Core observation

Skills, subagents, task records, checkpoints, evidence artifacts, and integration reviews preserve different parts of the development state:

| Mechanism | Primary function |
| --- | --- |
| Skills | Reload stable procedures, constraints, and role-specific knowledge |
| Subagents | Isolate bounded working sets and prevent unrelated details from competing for one context window |
| Task and control-plane records | Preserve task state, dependencies, decisions, and acceptance conditions |
| Checkpoints | Preserve the state required to resume or review work across agent and session boundaries |
| Evidence artifacts | Preserve what was executed, observed, and validated |
| Parent integration review | Reconstruct global consistency from locally produced results |

These mechanisms reduce implicit context loss by converting it into explicit coordination work. The resulting friction includes dispatch preparation, skill loading, artifact production, handoff validation, reconciliation, and review.

## Candidate central claim

> In long-horizon agentic software development, bounded model context creates a tradeoff between local execution efficiency and global state preservation. Skills, subagents, checkpoints, and persistent control-plane artifacts reduce context loss and improve recoverability, but introduce measurable coordination overhead.

A stronger formulation, if supported by the evidence, is:

> The harness does not remove the context-window limitation. It converts otherwise implicit and potentially unrecoverable context loss into explicit, inspectable, and recoverable coordination work.

The second statement should remain a hypothesis until supported by prospective episode data.

## Research question

> **RQ:** How does explicit context management through skills, subagents, checkpoints, and persistent control-plane artifacts affect coordination overhead, recoverability, and implementation correctness in long-horizon scientific software development?

Possible subquestions are:

1. What fraction of total development effort is attributable to harness construction and operation?
2. Which harness mechanisms account for the largest coordination cost?
3. Which classes of context loss, rework, or defects are prevented or made recoverable by those mechanisms?
4. How does subagent task granularity affect handoff cost and integration failure?
5. Does harness overhead decline as procedures stabilize and become reusable?

## Cost model

Let the effective cost of an episode be

$$
C_{\mathrm{effective}}
=
C_{\mathrm{execution}}
+
C_{\mathrm{coordination}}
+
C_{\mathrm{rework}}
+
C_{\mathrm{recovery}},
$$

where:

- $C_{\mathrm{execution}}$ is the cost of implementing and validating the domain change;
- $C_{\mathrm{coordination}}$ is the cost of dispatches, handoffs, skill loading, checkpoints, and integration;
- $C_{\mathrm{rework}}$ is the cost of correcting rejected or inconsistent work;
- $C_{\mathrm{recovery}}$ is the cost of reconstructing lost task state after interruption or context displacement.

The harness is beneficial when an increase in $C_{\mathrm{coordination}}$ is offset by reductions in $C_{\mathrm{rework}}$ and $C_{\mathrm{recovery}}$, improved correctness, or the ability to complete work that would otherwise exceed the usable context horizon.

A descriptive harness-burden ratio may be recorded as

$$
R_H
=
\frac{C_{\mathrm{harness}}}
{C_{\mathrm{harness}}+C_{\mathrm{domain}}}.
$$

This ratio is not, by itself, a measure of waste. Its interpretation depends on the failures prevented, evidence preserved, and later reuse obtained from the harness work.

## Essential and accidental friction

The analysis should distinguish two categories.

**Essential friction** arises from boundaries that protect an actual requirement:

- externalizing decisions that must survive context loss;
- separating large, distinct working sets;
- verifying claims before acceptance;
- preserving execution and validation evidence;
- reconciling outputs produced under different local contexts.

**Accidental friction** does not protect a demonstrated boundary:

- repeatedly restating stable constraints;
- creating subagents for tasks too small to justify a handoff;
- duplicating reviews without distinct acceptance responsibilities;
- producing checkpoints that preserve no decision-relevant state;
- redesigning the control plane before every domain change.

This distinction prevents the paper from assuming that all observed harness overhead is necessary.

## Prospective episode measurements

For each development episode, record:

| Quantity | Suggested operational measure |
| --- | --- |
| Domain work | Domain files changed, domain commits, or bounded active time |
| Harness work | Control-plane and skill files changed, harness commits, or bounded active time |
| Agent structure | Number of subagent dispatches, roles, and handoffs |
| Skill use | Skills loaded and whether loading changed execution behavior |
| Artifact production | Task records, checkpoints, evidence files, and review reports produced |
| Parent intervention | Clarifications, corrections, redispatches, and manual integration actions |
| Rework | Rejected outputs, corrective cycles, and repeated implementation work |
| Defect interception | Defects detected before integration or human acceptance |
| Recovery | Whether work resumed from persistent artifacts without reconstructing state from conversation |
| Outcome | Completion, validation result, unresolved findings, and human acceptance |

Time estimates should be supplemented by artifact and event counts because conversational timestamps do not cleanly represent active work.

## Evidence strategy

Existing episodes may be analyzed retrospectively to identify candidate mechanisms and failure classes. They should not be used alone to estimate precise costs because their measurements were not designed prospectively.

Subsequent episodes should use a fixed instrument recorded during execution. The paper can then compare:

- episodes with different subagent granularity;
- first use versus reuse of an established skill or chain;
- episodes requiring corrective checkpoints versus episodes accepted on first review;
- recovery after interruption versus uninterrupted execution;
- coordination cost against defects intercepted and rework avoided.

The strongest evidence would be a paired or repeated-task comparison. If that is not feasible, a structured multiple-episode case study can support bounded claims about the observed repository and harness configuration.

## Scope limitation

The study should not claim that the measured ratios generalize to all agentic development. Harness cost depends on repository maturity, task novelty, scientific assurance requirements, model behavior, and the granularity of agent delegation. The defensible contribution is a characterized mechanism and an auditable case study showing how context preservation changes the distribution of development work.

## Candidate paper placement

This material fits in three places:

1. **Conceptual framework:** bounded context and externalized development state.
2. **Methods:** episode-level measures of coordination, rework, recovery, and correctness.
3. **Discussion:** harness friction as the observable cost of preserving state across bounded agent contexts.

## Candidate discussion paragraph

The observed harness burden should not be interpreted solely as automation overhead. The workflow used skills, bounded subagent roles, persistent task records, checkpoints, and evidence artifacts as an external memory hierarchy. These mechanisms preserved procedural constraints and task state that could not remain simultaneously active within a single model context. Their use increased dispatch, handoff, and integration work, but made the development process inspectable and recoverable across context boundaries. The relevant evaluation is therefore not whether the harness eliminated friction, but whether its coordination cost was offset by reduced context loss, lower rework or recovery cost, improved defect interception, and successful completion of work whose state exceeded one usable context window.
