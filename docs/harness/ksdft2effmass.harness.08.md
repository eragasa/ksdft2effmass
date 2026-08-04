# PI Harness Package-Extraction Readiness

## Objective

H5 demonstrates that the generic harness can become a separate package without publishing it. The extraction test must succeed without project-local Python, local textual resources, `.pi` state, or scientific modules.

## Extraction unit

The generic extraction unit is

```text
python/src/ksdft2effmass/harness/pi/
    excluding local/

harness/pi/
```

The following remain in `ksdft2effmass`:

```text
python/src/ksdft2effmass/harness/pi/local/
harness/local/
.pi/
```

## Disposable package construction

Create a disposable standalone source tree containing only:

- generic Python modules;
- generic skills and references;
- generic templates and schemas;
- approved packaging metadata;
- generic tests;
- explicit dependencies.

No source file may be recovered implicitly from the parent repository during the test.

## Required checks

Verify:

- isolated build;
- isolated installation;
- public imports;
- CLI entry points if approved;
- schema discovery;
- skill discovery;
- resource-manifest validation;
- validator execution;
- generic tests with no local tree;
- wheel contents;
- sdist contents;
- dependency metadata;
- absence of repository-relative paths;
- absence of project-domain imports.

## Leakage audit

The generic package must not require:

- `ksdft2effmass` scientific modules;
- backend-neutral CPN implementation classes;
- QE;
- Wannier90;
- SNAKES;
- `.pi` runtime state;
- `harness/local`;
- repository documentation;
- Git metadata.

Searches for project-specific names are useful structural checks but do not replace semantic review.

## Package identity

H5 should propose, but not publish:

- distribution name;
- import namespace;
- CLI name;
- initial semantic version;
- Python requirement;
- dependency ranges;
- package-data inventory;
- license and notices;
- compatibility policy.

The incubation namespace does not force the eventual distribution or import name.

## Project compatibility

After standalone extraction succeeds, the project-local overlay must still pass against the extracted package candidate. This verifies both directions of the boundary:

```text
generic package works without project
and
project-local overlay works with generic package
```

## Acceptance boundary

Acceptance of H5 establishes package-extraction readiness only. It does not:

- publish a package;
- release a version;
- launch P2;
- authorize external execution;
- establish scientific validation;
- establish uncertainty quantification.

P2 requires separate explicit activation after accepted P1 and accepted H5.

## Navigation

- [Previous: Migration and shadow replay](./ksdft2effmass.harness.07.md)
- [Index](./ksdft2effmass.harness.00.md)
