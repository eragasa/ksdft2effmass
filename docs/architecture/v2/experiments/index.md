# Experiment architecture

## Purpose

This tree mirrors publication-independent experiment composition separately from the
installed `ksdft2effmass` package architecture.

- Source root: `experiments/`.
- Architecture root: `docs/architecture/v2/experiments/`.
- Mutable planning root: `docs/tasks/dev/experiments/`.
- Publication labels, task paths, architecture paths, and experiment identities remain distinct.

## Mirror rule

Every selected experiment package, subpackage, nested subpackage, source module, and
public class has one matching architecture directory.

- Each node contains `index.md`.
- Each node contains `science.md`.
- Each node contains `numerics.md`.
- Each node contains `implementation.md`.
- Each node contains `schematics.md`.
- Modules and classes use directories rather than sibling `<name>.md` files.
- Re-exported classes are documented only beneath their defining module.

## Architecture bundle

The five pages divide ownership without duplicating one another.

- [Science](science.md) documents scientific construction, assumptions, and interpretation.
- [Numerics](numerics.md) documents mathematical and numerical implementation steps.
- [Implementation](implementation.md) defines source mapping and dependency direction.
- [Schematics](schematics.md) visualizes composition and evidence flow.
- `index.md` provides status, navigation, evidence summary, and limitations.

## Child map

Only experiment domains with authored architecture appear below this root.

- Other existing experiment families remain valid even when their architecture has not yet migrated here.
- Directory presence does not imply implementation, versioning, execution, or validation.

## Dependency boundary

Experiments compose reusable capabilities but do not become installed library packages.

- Installed packages must not import experiment code.
- Experiments may import supported KSD capabilities.
- Experiments may consume reviewed PhysKit and numerical-owner contracts.
- Concrete controls, schemas, verification, evidence policy, and interpretation remain experiment-owned.
- Parameterization alone does not justify reusable workflow extraction.

## Evidence boundary

Architecture records contracts but supplies no scientific result or execution authority.

- Software verification remains distinct from numerical verification.
- Numerical verification remains distinct from scientific validation.
- Thresholds are not uncertainty models unless explicitly defined as such.
- Protected calculators, remote computation, retention, publication, and release require separate authority.
