# Third-party dependency notices

This notice identifies separately installed third-party dependencies whose
licenses differ from the Apache-2.0 license of `ksdft2effmass`. It does not
change the license of project-owned source code.

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
