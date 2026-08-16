# Third-party dependency notices

This notice identifies separately installed or narrowly vendored third-party
materials whose licenses differ from the Apache-2.0 license of
`ksdft2effmass`. It does not change the license of project-owned source code.

## SNAKES

`ksdft2effmass` optionally depends on SNAKES when installed with the `workflow`
extra. SNAKES is resolved and installed as a separate Python distribution; its
source and license files are not part of the `ksdft2effmass` wheel.

- Distribution name: `SNAKES`
- Import name: `snakes`
- Supported dependency range: `>=0.9.33,<0.10`
- Copyright: © 2007–2021 Franck Pommereau
- Upstream project: <https://codeberg.org/fpom/snakes>
- Upstream license declaration: GNU Lesser General Public License version 2.1
  or, at the user's option, any later version (`LGPL-2.1-or-later`)

The SNAKES 0.9.33 distribution inspected during the bounded P0 preflight
contains `LICENCE.md` and `share/doc/python-snakes/COPYING`, both containing GNU
LGPL version 3 text. This project records that observed distribution fact
separately from the upstream `LGPL-2.1-or-later` grant. This is a project
packaging decision, not a general legal conclusion.

SNAKES is not covered by the project's Apache-2.0 license. The project must not
vendor or embed SNAKES source, copy or modify its implementation, redistribute a
SNAKES fork, or bundle SNAKES into a standalone executable, application bundle,
or container intended for distribution without a new human license checkpoint.

## Elsevier `elsarticle` LaTeX files

The P01 working-manuscript directory vendors two files from Elsevier's
`elsarticle` bundle for reproducible document formatting:

- `docs/publications/papers/ksdft2effmass.P01/latex/elsarticle.cls` — bundle
  version 3.5, dated 2026-01-09, SHA-256
  `d8188310e61a6fff568fc79985464b302eb956c4286eca0b5e1e002c32117b54`;
- `docs/publications/papers/ksdft2effmass.P01/latex/elsarticle-num.bst` — style
  version 2.1, SHA-256
  `7b23372397ae57f72b1318601e10c0f792e7c17a6db9734058525e09d92b9b65`.

Both file headers state copyright © 2007–2026 Elsevier Ltd and permit
distribution under the LaTeX Project Public License, version 1.3 or, at the
recipient's option, any later version (`LPPL-1.3-or-later`). The files retain
their upstream copyright and license notices.

- Upstream package record: <https://ctan.org/pkg/elsarticle>
- License text identified by the file headers:
  <https://www.latex-project.org/lppl/lppl-1-3c/>

The human PI explicitly authorized this vendoring and license disposition on
2026-08-16. These files are not covered by the project's Apache-2.0 license.
Vendoring another bundle file, modifying these files, or changing their license
requires a new human licensing decision.
