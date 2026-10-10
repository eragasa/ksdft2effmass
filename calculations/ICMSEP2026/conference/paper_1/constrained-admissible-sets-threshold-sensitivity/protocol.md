# Post-hoc M3 operator-threshold sensitivity protocol

## Status

This is an explicitly **post-hoc exploratory reanalysis** of the sealed M3 retained
quadratic losses. It was motivated after inspecting the two designed M3 thresholds. It
is not part of the prospective M3 confirmatory protocol and must not be presented as a
blind prediction.

No electronic-structure, localization, remote, or external calculator is executed.
The analysis reads only the retained M3 `result.json` whose SHA-256 is fixed in
`input.json`.

## Question

At the frozen spectral threshold

\[
\tau_S=0.03,
\]

how does the exact distance between the spectral and operator admissible sets change as
the operator threshold varies from `0.3075` to `0.335`?

The interval contains the designed separated threshold `0.31`, the designed compatible
threshold `0.33`, and the compatibility transition.

## Analytic reduction

The retained M3 quadratics are axis aligned to numerical tolerance, have the same
positive quadratic matrix, and have centers on `energy_shift_ratio = 0` to numerical
tolerance. For a quadratic

\[
L^2(s,\lambda)=m+q_s(s-c_s)^2+q_\lambda(\lambda-c_\lambda)^2,
\]

the accepted interval at `s = 0` is reconstructed analytically. The spectral set's
minimum accepted splitting is fixed by `tau_S`. For each operator threshold, the
maximum accepted splitting is the maximum over all feasible members of the frozen
nine-angle family.

Within the plotted interval, the closest spectral and operator points share `s = 0`.
Therefore

\[
\delta^*(\tau_O)=
\max\left(0,\lambda_{S,\min}-\lambda_{O,\max}(\tau_O)\right).
\]

The compatibility transition is the minimum operator loss at the fixed spectral
boundary point. At and above that value, an explicit common point exists. A second
crossing records where the positive distance falls below the frozen `0.05` resolution;
positive distances below that line are mathematically separated but are not assigned
the M3 `certified-separated` disposition. Below the minimum feasible operator threshold,
the operator set would be empty; the plotted interval begins above that boundary.

## Outputs and limits

`analyze.py` writes `result.json`, `figure-data.csv`,
`operator-threshold-sensitivity.png`, `report.md`, and `software.json`.
`verify_result.py` independently reconstructs the analytic curve without importing
`analyze.py` or package producer Actions.

The diagram characterizes only the frozen synthetic two-parameter family, fixed
spectral threshold, compact domain, and nine constant rotations. It is not a threshold
calibration, uncertainty analysis, material result, or evidence for arbitrary
momentum-dependent alignment families. SHA-256 identifies bytes but does not establish
chronology.
