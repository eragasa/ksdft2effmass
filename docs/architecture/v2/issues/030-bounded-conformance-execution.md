# V2-ISSUE-030: Bounded conformance execution contract

**Severity:** High
**Scope:** Candidate-controlled validator execution, confinement, process outcomes, and retained ValidationResult evidence
**Status:** Open

## Current conflict

Development conformance executes candidate-controlled behavioral checks after identifying trusted inputs, but no contract closes process launch, executable and command identity, root and working directory, sanitized environment, limits, timeout/cancellation/signal behavior, output capture, partial evidence, or mapping to the normative validation outcomes.

## Affected contracts

- [`docs/architecture/v2/ksdft2effmass/harness/conformance.md`](../ksdft2effmass/harness/conformance.md) — behavioral checks execute candidate-controlled code while the bounded execution and isolation contract remains unresolved.
- [`docs/architecture/v2/ksdft2effmass/harness/compiler-architecture.md`](../ksdft2effmass/harness/compiler-architecture.md) — generic compiler failures do not cover validator launch, timeout, resource exhaustion, signals, truncation, or partial evidence.
- [`docs/architecture/v2/ksdft2effmass/harness/validation.md`](../ksdft2effmass/harness/validation.md) — normative validation outcomes lack a defined mapping from bounded process outcomes.
- [`docs/architecture/v2/ksdft2effmass/application/index.md`](../ksdft2effmass/application/index.md) — composition supplies validator dependencies without identifying a complete bounded-execution capability.

## Missing contract

Conformance lacks a bounded validator-execution boundary covering exact tool and command identity, trusted root and working directory, sanitized environment, resource and time limits, cancellation and signals, captured output and artifact identities, partial evidence, a closed process outcome, and deterministic mapping to normative validation results.

## Exclusions and claim boundary

The concrete process-isolation mechanism is excluded. This record authorizes no candidate execution and establishes no implementation, verification, scientific validation, uncertainty quantification, or human acceptance.
