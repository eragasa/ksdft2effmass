# Anisotropic 3-D hopping-support hierarchy

## Identity and status

This package mirrors the preserved fourth-stage experiment proposal.

- Family ID: `ksdft2effmass.campaign.model-adequacy.periodic3d.anisotropic-hopping-support-hierarchy`.
- Maintained calculation/design owner: `calculations/periodic3d/rank1/anisotropic-hopping-support-hierarchy/`.
- Exact protocol: `protocol.md` in the calculation package.
- Exploratory design provenance: `threshold-design.md` in the calculation package.
- Current status: pre-version documentation only; no modules, classes, schemas, or result.

## Architecture bundle

The package pages summarize the frozen-form proposal without duplicating future
class-level algorithms.

- [Science](science.md).
- [Numerics](numerics.md).
- [Implementation](implementation.md).
- [Schematics](schematics.md).

## Scientific role

The experiment combines three periodic coordinates with deliberate removal of
axis-permutation symmetry.

- The parent is an exact orthorhombic scalar synthetic model.
- Candidate coordinates distinguish directional hopping content.
- Support classes are named groups rather than universal radius shells.
- The family remains separate from isotropic 3-D and bulk silicon.

## Sequencing gate

Advance design work is preserved but does not bypass the selected experiment order.

- Complete isotropic 2-D protocol ownership first.
- Complete isotropic 3-D protocol ownership second.
- Complete anisotropic 2-D protocol ownership third.
- Review this family's exact controls before implementation.
- Assign `.v1` only after schemas, verification, dependencies, tests, and evidence policy close.
