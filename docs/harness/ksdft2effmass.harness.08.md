# PI Harness Package-Extraction Readiness

## Objective

H5 is optional standalone extraction-readiness work after accepted H4 and
separate explicit H5 activation. It demonstrates that the generic harness can
become a separate package without publishing it. The extraction test must
succeed without project-local Python, local textual resources, `.pi` state, or
scientific modules.

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

H4 establishes accepted project-local integration, shadow replay, and cutover
behavior; it does not establish standalone package readiness, extract a package,
or publish one. H5 separately demonstrates standalone extraction readiness.

Acceptance of H5 establishes package-extraction readiness only. It does not:

- publish a package;
- release a version;
- launch P2;
- authorize external execution;
- establish scientific validation;
- establish uncertainty quantification.

H5 is not required for P2. After accepted H4, P2 may proceed only through its
own explicit human activation while P1 remains human-accepted. H5 may proceed
only through separate explicit H5 activation. Neither P2 nor H5 activates
automatically after H4, and H5 acceptance does not activate P2.

## Navigation

- [Previous: Migration and shadow replay](./ksdft2effmass.harness.07.md)
- [Index](./ksdft2effmass.harness.00.md)
