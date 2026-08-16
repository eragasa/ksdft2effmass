# Repository-level direct simulation model in v1

The implemented calculator-specific parsing and construction boundaries are
detailed under
[`ksdft2effmass.io.quantum_espresso.qexsd`](../ksdft2effmass/io/quantum_espresso/qexsd/index.md).

## Implemented status

V1 has no public `Simulation`, `SimulationExecutor`, or `SimulationExecutionResult` object. A simulation is represented operationally by calculation-specific files and runner behavior.

## Effective direct-execution model

| Element | V1 representation |
|---|---|
| Scientific parameters | Native Quantum ESPRESSO input files and computational documentation |
| Calculator selection | Runner-owned `pw.x` executable configuration |
| Input identity | Checksums and compact preflight records |
| Pseudopotential identity | Exact file identity and retained provenance |
| Resource request | Runner arguments and preflight resource ceiling |
| Execution | Calculation-specific shell runner |
| Process result | Exit status, completion marker, warnings, and compact result record |
| Artifacts | Manifests, checksums, external locations, and retention policy |

```mermaid
flowchart LR
    input["Native QE input"] --> preflight["Preflight identities"]
    preflight --> runner["Direct runner"]
    runner --> pw["pw.x"]
    pw --> output["Native outputs"]
    output --> record["Compact result and artifact records"]
```

## Boundaries

Preflight binds repository revision, executable, input bytes, pseudopotential, processor count, run root, resource ceiling, and retained outputs. Runners invoke the calculator and capture operation-specific observations.

The direct result is not a general immutable execution-result contract. Process success and `JOB DONE.` do not establish numerical convergence, scientific validation, or human disposition.

## Historical executions

The accepted silicon Davidson SCF and bands tutorials each executed once through QE 7.2 with retained inputs and compact provenance. Eighteen direct convergence invocations—nine SCFs and nine linked NSCF diagnostics—are retained as historical bootstrap execution evidence. None is an authoritative `ScientificWorkflowRun`.

## Limitation

Calculator configuration, native input, process invocation, completion checks, and artifact retention are coupled in calculation-specific runners. No reusable calculator protocol separates simulation definition from execution result.
