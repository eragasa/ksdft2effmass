# Isotropic 2-D hopping-shell hierarchy

## Identity and status

This package is the architecture home for the first stage of the selected sequence.

- Family ID: `ksdft2effmass.campaign.model-adequacy.periodic2d.hopping-shell-hierarchy`.
- Historical alias: `HSH-1`.
- Development task: `docs/tasks/dev/experiments/isotropic2d/`.
- Maintained calculation/design owner: `calculations/periodic2d/rank1/hopping-shell-hierarchy/`.
- Current status: maintained prospective protocol with an exact selected orbit/support inventory and periodic-1D-shaped package execution graph; no source package, immutable version, run, or result.

## Architecture bundle

The package pages summarize the experiment and defer future algorithm detail to mirrored
module and `ClassName` directories.

- [Science](science.md).
- [Numerics](numerics.md).
- [Implementation](implementation.md).
- [Schematics](schematics.md).

## Scientific role

The experiment asks for the smallest tested square-symmetric hopping-support class with
a common spectral/operator witness.

- The parent is a retained finite scalar periodic-2D target.
- Candidate classes are nested complete square-symmetry orbits.
- Smaller classes require channel emptiness or certified separation before minimality is claimed.
- The result remains synthetic and hierarchy-relative.

## Design inputs

The maintained prospective protocol owns current design decisions; older records remain
traceable donors.

- [Maintained prospective protocol](../../../../../../../calculations/periodic2d/rank1/hopping-shell-hierarchy/protocol.md).
- [Exact orbit and support inventory](../../../../../../../calculations/periodic2d/rank1/hopping-shell-hierarchy/orbit-support-inventory.md).
- [Projection and loss design](../../../../../../../calculations/periodic2d/rank1/hopping-shell-hierarchy/projection-and-loss-design.md).
- [Sample-role design](../../../../../../../calculations/periodic2d/rank1/hopping-shell-hierarchy/sample-role-design.md).
- [Threshold and resolution design](../../../../../../../calculations/periodic2d/rank1/hopping-shell-hierarchy/threshold-design.md).
- [Execution-structure donor](../../../../../../../calculations/periodic2d/rank1/hopping-shell-hierarchy/execution-structure.md).
- [Legacy HSH architecture bundle](../../../../ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/index.md).
- [Historical draft protocol](../../../../../../../calculations/ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/protocol.md).
- [Shared evidence semantics](../../../../ksdft2effmass/analysis/model_adequacy/admissible-set-evidence-semantics.md).
- No legacy `python/src` mapping authorizes implementation.

## Current gates

The maintained family cannot receive `.v1` until its exact controls and source ownership
are reviewed.

- Convert the selected donor binding, projection tolerances, 36 target coefficients, energy shift, box, and weights into strict canonical input.
- Freeze conservative arithmetic and active-quadratic reconstruction tolerances; prospective thresholds and resolution, the common metric, exact orbit/support inventory, coefficient domain, and spectral weights are selected already.
- Define strict schemas and independent verification.
- Pin exact dependency and method identities without pass-through facades.
- Encode and independently verify the selected objective-construction, evaluation, withheld, and locality role records.
