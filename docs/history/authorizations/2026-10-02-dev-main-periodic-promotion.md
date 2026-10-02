# Development-to-main periodic promotion authorization

## Status

Resolved human authorization for one protected `dev`-to-`main` promotion and its
necessary authorization-record integration.

## Human instructions

The operator selected the promotion route verbatim:

> branch → dev → main

After pull request #28 merged the periodic branch into `dev`, the operator repeatedly
instructed:

> continue

The operator was then shown the exact protected boundary, told that this authorization
would be persisted before the merge and that synchronization would remain separate,
and responded verbatim:

> authorized

## Audited promotion boundary

The protected promotion is represented by pull request #29:

- URL: `https://github.com/eragasa/ksdft2effmass/pull/29`;
- audited `main` base: `db176a01d019e452d2ecbd732bbbaf7690616fdb`;
- periodic integration head before this authorization record:
  `dev@694d4045ceaafbc03591c0f7caab22e848049844`;
- incorporated periodic feature head:
  `37cc9b8fe0ea87a402162dbbcb983ec9b28a2512`; and
- required check: `Python 3.14`.

This record is integrated into `dev` through one documentation-only pull request before
pull request #29 is merged. That merge necessarily advances the exact `dev` head shown
above. The final authorized promotion head is therefore the resulting `dev` merge
commit containing this record, provided no other tree change enters that integration
and pull request #29 reruns its required check successfully against that exact head.

## Verification evidence

Before authorization-record integration:

- pull request #28 merged cleanly into `dev` at
  `694d4045ceaafbc03591c0f7caab22e848049844`;
- the exact `dev` push CI run `36993717862` passed;
- pull request #29 CI run `37000634872` passed;
- the periodic integration boundary passed Ruff formatting and lint, production-source
  mypy, Sphinx warnings-as-errors, changed-document link and checklist validation, and
  `git diff --check`;
- the bounded local pytest profile reported 4,387 passed, three external-QEXSD skips,
  and 133 expensive retained tests deselected; and
- 77 focused periodic tests passed.

The final authorization-record pull request and the updated pull request #29 must each
pass the required `Python 3.14` check. These are software and documentation checks only.
They do not establish scientific validation, uncertainty quantification, publication
acceptance, or release status.

## Authorized operation

The authorization covers exactly this sequence:

1. commit and push this authorization record on a dedicated branch;
2. integrate that documentation-only branch into `dev` through a normal pull-request
   merge after its required check succeeds;
3. verify that updated pull request #29 contains the resulting exact `dev` head, remains
   mergeable against the audited `main` base, and passes the required check;
4. merge pull request #29 into `main` with a normal merge commit; and
5. fetch and verify that `origin/main` equals the pull request's reported merge commit
   and contains the authorized `dev` head.

The feature and authorization branches are retained. Synchronizing `dev` to the
accepted `main` merge commit remains a separate subsequent operation.

## Excluded actions

This authorization does not permit force-pushing, history rewriting, deletion of a
remote branch, tag creation or movement, GitHub Release creation, package publication,
archive deposit, DOI changes, production electronic-structure or Wannier90 execution,
scientific-result modification, or any remote update other than the exact development
and main pull-request merges above.
