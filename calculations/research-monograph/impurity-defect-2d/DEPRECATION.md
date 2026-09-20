# Stage C historical CLI deprecation

`run_stage_c_parent.py` and `plot_stage_c_parent.py` are frozen historical entry
points. Retained Stage C results and provenance continue to identify their exact
historical bytes. They must not be rewritten, renamed, or reattributed.

For new authored-fixture operations, use:

- `run_stage_c_parent_v2.py`, which delegates argument adaptation to the
  encapsulated Workflows in `stage_c_parent.workflows`; and
- `plot_stage_c_parent_v2.py`, which delegates rendering to the supported public
  `ksdft2effmass.campaigns.research_monograph.StageCParentSvgPlotter`.

The version-two adapters add no scientific or numerical policy. They do not grant
accepted-parent execution authority, authorize another calculation attempt, establish
scientific validation, or establish uncertainty quantification. Any future protected
accepted-parent execution still requires a separately applicable authorization record
whose artifact identities and operation boundary cover that execution.
