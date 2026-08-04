# User guide

This guide covers installation, external dependencies, workflow operation, provenance, and troubleshooting. It does not replace the scientific specifications, architecture decisions, computational protocols, or research records.

## Contents

- [Installation](installation.md)
- [External dependencies](external-dependencies.md)
- [Periodic electronic-structure backends](dft-backends.md)
- [PAW and pseudopotential capabilities](paw-and-pseudopotential-backends.md)
- [Workflow model](workflow-model.md)
- [Colored Petri Nets](colored-petri-nets.md)
- [Quantum ESPRESSO](quantum-espresso.md)
- [ABINIT](abinit.md)
- [Cross-backend verification](cross-backend-verification.md)
- [Wannier90](wannier90.md)
- [Provenance and artifacts](provenance-and-artifacts.md)
- [Troubleshooting](troubleshooting.md)

## Current status

The operator-record package is implemented and accepted. The periodic KS/GKS electronic-structure, external-tool, and CPN workflow architecture is human-accepted. Bounded P0 was accepted as `CONDITIONAL_PASS`, and bounded P0A packaging/configuration was accepted and closed. `P1-HC01` Option A and `P1-HC02` Option B are resolved. The earlier independent final review reported only deterministic stale prose/evidence findings for the consolidated correction cycle; after correction, reviews and parent verification completed. Final P1 acceptance was granted as Option A through `P1-HC03` on 2026-08-04, and P1 is closed as human-accepted `PASS`. No successor was selected or launched. The P1 contract is distinct from the still-deferred SNAKES adapter, authoritative persistence, concrete scientific workflows, and external execution. QE remains the planned initial production backend; P2–P11 and production/scientific execution remain blocked and unauthorized.

Architecture decisions are maintained in the [CPN workflow architecture](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/architecture/colored-petri-net-workflows.md) and neighboring `docs/architecture/` records. Calculation stages and evidence gates begin at the [computational registry](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/computational/ksdft2effmass.computational.00.md). Scientific questions and limitations begin at the [research registry](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/research/ksdft2effmass.00.md).
