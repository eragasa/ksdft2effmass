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
- [External-tool lifecycle](external-tool-lifecycle.md)
- [Troubleshooting](troubleshooting.md)

## Current status

The operator-record package is implemented and accepted. The periodic KS/GKS electronic-structure, external-tool, and CPN workflow architecture is human-accepted. P0 was accepted as `CONDITIONAL_PASS`, P0A was accepted and closed, and P1 was human-accepted as `PASS` through `P1-HC03` on 2026-08-04. P2 is active and its provenance/external-tool record implementation is provisional pending correction review, replacement replay, parent verification, and human acceptance. It does not authorize external-tool or scientific execution. H5 and P3–P11 remain inactive; the SNAKES adapter, authoritative persistence, concrete scientific workflows, QE/Wannier adapters, and production/scientific execution remain deferred or unauthorized according to their controlling tasks.

Architecture documentation begins at the [version-isolated architecture index](../architecture/index.md). Calculation stages and evidence gates begin at the [computational registry](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/computational/ksdft2effmass.computational.00.md). Scientific questions and limitations begin at the [research registry](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/research/ksdft2effmass.00.md).
