# V2-ISSUE-007: Observation normalization composition

**Severity:** Medium

**Scope:** Calculator output, mechanical I/O, normalization, and service composition

## Conflict

Architecture v2 generally assigns faithful native parsing to `ksdft2effmass.io` and calculator-specific normalization adapters to calculator packages. The scientific service and application composition diagrams do not compose those adapters explicitly, and the migration crosswalk still describes QEXSD parser and semantic construction across `io`, `periodic`, and `ksdft`. The executable path from `SimulationExecutionResult` to normalized observations is therefore incomplete.

## Affected contracts

- `calculators/quantum-espresso.md`
- `workflow/simulation-model.md` — *Normalization path*
- `workflow/service-model.md`
- `composition-root.md`
- `migration/v1-to-v2/index.md`

## Required resolution

State exact ownership of faithful parsing, calculator-specific normalization, normalization policy and result records, and normalization failures. Compose the required adapters explicitly and describe migration of the existing semantic constructor.

## Acceptance condition

One versioned identity-preserving operation path connects native artifacts to normalized periodic and Kohn–Sham observations without ambiguous package ownership.
