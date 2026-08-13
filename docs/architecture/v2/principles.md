# Architecture v2 principles

## Separate authorities

1. `HarnessTask` controls development work only.
2. `DevelopmentTaskSelection` selects at most the authorized development work.
3. `Campaign` is a calculator-independent scientific workflow definition.
4. `CampaignRun` is one execution state of a `Campaign`.
5. `Simulation` specifies one scientific operation without recording its result.
6. `SimulationExecutionResult` records calculator observations without making a
   scientific conclusion.
7. `ScientificAnalysis` deterministically interprets normalized observations.
8. `ScientificDisposition` records an explicit scientific conclusion or
   parameter selection.

No authority is inferred from another lifecycle. Process success is not
scientific acceptance, and software verification is not numerical verification
or scientific validation.

## CPN as the campaign definition

A `Campaign` owns a `CpnDefinition` and its initial `CpnMarking`. Ordering,
authorization, dependency, failure, retry, recovery, and terminal scientific
workflow state are expressed through CPN places, tokens, guards, inscriptions,
and firing semantics. A separate campaign dependency graph is forbidden.

## Immutable specifications and results

Data records are immutable or operationally immutable. Intrinsic invariants
belong to the represented record. External effects, compatibility decisions,
serialization, deterministic analysis, and scientific policy belong to explicit
action owners. Input specifications and observed results are distinct objects.

## Calculator independence

Generic workflow contracts do not import calculator-specific packages.
Calculator-specific packages may implement `SimulationExecutor` and typed
`Simulation` payloads. Scientific domains do not import calculator packages.
Mechanical I/O does not own campaign policy or scientific disposition.

## Exact identity and lineage

Canonical inputs, executable identities, artifact identities, request/result
correlation, and parent-child lineage are explicit. Portable identity is distinct
from deployment location. Missing identity or incompatible lineage fails closed.

## Determinism and bounded effects

CPN enablement, firing, normalization, analysis, and projection are deterministic
for explicit inputs. External calculators are bounded side-effect boundaries;
the architecture does not claim that their numerical behavior is made
deterministic merely by orchestration.

## Extension policy

Meaningful extension points are public concrete immutable records and narrowly
demonstrated protocols. No universal electronic-structure calculator base,
mutable global registry, plugin service locator, or generic backend registry is
introduced without demonstrated multi-implementation need.

## Evidence boundaries

Software verification, repository conformance, calculator process success,
numerical verification, scientific validation, uncertainty quantification, and
human disposition remain separately named and evidenced. A
`ScientificDisposition` cites the applicable analyses and authority; it cannot be
manufactured from an exit code or terminal CPN marking alone.
