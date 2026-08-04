# P0A packaging and documentation configuration report

## Result before human acceptance

Implementation, required read-only review, and parent-verification result:
`PASS`, pending the human decision at `P0A-HC01`.

P0A declares SNAKES only in the optional `workflow` extra, declares MyST and a
bounded Sphinx range only in `docs`, refreshes the uv lock, adds the SNAKES
third-party notice, and configures Sphinx to collect the maintained Markdown
user guide without collecting every Markdown file under `docs/`.

This result is packaging/configuration software evidence. It does not implement
or verify a project CPN contract/runtime and is not numerical verification,
scientific validation, uncertainty quantification, or authorization for
scientific execution.

## Resolved dependency identities

| Dependency | Declared range | Locked version | Selected portable/source artifact SHA-256 |
|---|---|---:|---|
| SNAKES | `>=0.9.33,<0.10` in `workflow` | 0.9.33 | sdist `af8c3046bfedf3e088b6bf37d451ad6aeeb79716f68a6253e44ddbd1c7e250f3` |
| MyST Parser | `>=5.1,<6` in `docs` | 5.1.0 | universal wheel `9c91c52b3cdb4d94a6506e4fab4e2f296c7623a0da0dcbe6de1565c3dad67a8a` |
| Sphinx | `>=8,<10` in `docs` | 9.1.0 | universal wheel `c84fdd4e782504495fe4f2c0b3413d6c2bf388589bb352d439b2a3bb99991978` |

The refreshed `python/uv.lock` SHA-256 is
`186504b6dc24b054c15ef01ed3219c6829f83585a0d7c6a551d79ede37cb7368`.
The lock retains complete registry URLs, hashes, sizes, and upload times. The
locked SNAKES and MyST identities match the accepted P0 evidence.

Ordinary `uv lock` added only SNAKES, MyST, and MyST's previously absent
Markdown dependencies (`markdown-it-py`, `mdit-py-plugins`, and `mdurl`); it did
not perform a general upgrade. Graphviz is absent from Python metadata.

## Documentation collection and navigation policy

`docs/conf.py` keeps both root and nested RST sources and admits Markdown only
through these include patterns:

```python
["*.rst", "**/*.rst", "user-guide/*.md"]
```

The maintained build therefore contains 17 RST sources and exactly 13
`docs/user-guide/*.md` sources. Architecture, computational, research,
conference, paper, and meeting Markdown remain repository/Obsidian sources and
are not implicit Sphinx documents.

All 13 user-guide pages are listed in one explicit RST toctree. The obsolete 13
user-guide `:download:` entries were removed. Four architecture downloads remain
under an explicitly uncollected-source heading and therefore do not duplicate
rendered MyST navigation. The three directory links were replaced with concrete
repository source URLs. Links from collected user-guide pages to intentionally
excluded architecture Markdown were likewise converted to source URLs. Relative
links among collected user-guide pages remain relative.

The maintained mixed build passed with warnings as errors under locked Sphinx
9.1.0 and a separate lower-range Sphinx 8.2.3 compatibility environment, both
with MyST 5.1.0.

## License and redistribution treatment

`THIRD_PARTY_NOTICES.md` identifies distribution/import names `SNAKES`/
`snakes`, range `>=0.9.33,<0.10`, copyright 2007–2021 Franck Pommereau, Codeberg
upstream, and the explicit upstream `LGPL-2.1-or-later` grant. The exact 0.9.33
sdist README hash is
`f3755596bd28357a6c0736c9ff88be8cb4c28b4d035dd5e5b711a736b0b8d5cf`.
The notice separately records that the inspected distribution contains LGPLv3
text.

SNAKES remains a separately installed dependency and is not Apache-2.0 project
code. The project wheel contains no SNAKES package, source, scripts, data,
`dist-info`, or license files. Vendoring, copying/modification, fork
redistribution, or bundled executable/application/container distribution remains
prohibited without a new human license checkpoint. This is the binding project
packaging treatment from `P0-HC01`, not a general legal conclusion.

## Verification summary

- `uv lock --check`: pass;
- isolated core install: pass; SNAKES and MyST absent;
- isolated `workflow` install: pass; SNAKES 0.9.33, MyST absent;
- isolated `docs` install: pass; MyST 5.1.0/Sphinx 9.1.0, SNAKES absent;
- project wheel build, clean install, import, and metadata assertions: pass;
- wheel SNAKES/Graphviz exclusion assertions: pass;
- Sphinx 9.1.0 and 8.2.3 warnings-as-errors builds: pass;
- explicit Markdown collection, navigation, local-link, and notice audit: pass;
- Ruff format/lint: pass;
- mypy: pass for 70 source files;
- pytest: 921 passed;
- no production CPN/scientific implementation or execution: confirmed.

## Deterministic corrections

- `P0A-001`: the initial proposed `uv tree --extra` command was unsupported by
  uv 0.11.25. It was replaced by locked whole-project `uv tree --depth 2`
  inspection; dependency placement was independently asserted from project and
  wheel metadata.
- `P0A-002`: the first combined evidence-format command stopped in `python/`
  after Ruff correctly reported two long hash literals, causing subsequent
  relative script paths to fail. Hash constants were split, Ruff passed, and the
  evidence scripts were rerun from the repository root.
- `P0A-003`: tooling review found verifier gates used removable Python `assert`
  statements and the manifest used undefined variables/prose placeholders. All
  authoritative gates now fail explicitly, malformed input is rejected under
  `python3 -O`, and `run_verification.sh` is an exact self-cleaning replay.
- `P0A-004`: review found stale pre-adoption status prose and an unsynchronized
  chain dependency flag. The affected computational, user-guide, repository
  index, and chain records now distinguish declared optional dependencies from
  the still-absent CPN runtime.
- `P0A-005`: correction re-review found the replay depended on an ignored local
  `.venv`, could mutate `python/.venv`, and left setuptools `python/build/`
  output. The generated output was removed; replay now builds from a disposable
  source copy and directs all uv environments under the trapped temporary root.
- `P0A-006`: documentation re-review found one remaining prospective P0 engine-
  reconsideration sentence. It now records the completed P0 outcome and requires
  separate authorization for any future comparison or reopening.
- `P0A-007`: final tooling review found uv's download cache still defaulted
  outside the trapped replay root. Replay now sets `UV_CACHE_DIR` under that
  root. Three additional minor completed-P0/current-task phrases were corrected
  to distinguish accepted P0, active packaging-only P0A, and separately
  authorized future work.
- `P0A-008`: final replay review found unqualified `python3` commands could
  resolve through a repository virtual environment on `PATH`. Replay now creates
  and uses a dedicated Python 3.14 evidence environment under the trapped root.

## Read-only review result

Packaging/license, documentation, tooling, and integration lanes passed after
corrections `P0A-003`--`P0A-008`. Review verified license facts and boundaries,
optional-extra isolation, exact lock identities, bounded 13-page MyST
collection/navigation, unconditional evidence gates, clean-checkout replay with
all environments/caches/builds under a trapped temporary root, synchronized
control-plane state, and absence of production/scientific implementation.
Detailed findings and residual risks are in `review-results.json`.

## Parent verification

Parent verification passed deterministic dependency/lock/configuration/notice
and link assertions, selected-artifact regeneration, `uv lock --check`, checkpoint
schema/dry-run validation, P0A/P1--P11 control-plane assertions, JSON and shell
syntax, production-source/test/import scope scans, generated-output scans, no
staged files, and `git diff --check`. The exact full isolated replay had already
passed after `P0A-008` and left no repository build, cache, bytecode, egg-info,
wheel, environment, or Graphviz output.

## Limitations and stop condition

The project CPN contract/runtime, neutral persistence, adapters, and scientific
workflows remain unimplemented. Graphviz was not installed or executed. No
remote, scheduler, QE, ABINIT, Wannier90, or scientific calculation ran.
Existing P1--P11 remain blocked. P0A must stop at its human checkpoint and may
not launch P1.
