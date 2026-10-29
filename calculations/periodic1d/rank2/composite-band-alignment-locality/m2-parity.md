# Historical M2 finite parity record

## Evidence boundary

This record compares an in-memory run of the direct source lifecycle with the exact
historical M2 result at revision
`c5d34a93b4710a4a430738c404c775865d418d42`. The historical result SHA-256 is
`3bb30d20f73d2d4ae8ea55a493d50978c5094dbecfcd22237dd8c32760b0f3da`.
No successor execution directory was created, and these values are provisional software
regression evidence rather than retained scientific evidence.

## Named channels

| Channel | Historical M2 | Direct source | Absolute difference |
|---|---:|---:|---:|
| minimum sampled retained/excluded gap | `1.0566461211497047` | `1.0566461211497054` | `6.7e-16` |
| minimum neighbor/closure overlap singular value | `0.9999828868735376` | `0.9999828868735373` | `3.3e-16` |
| attack frame Frobenius defect | `1.5056428951173264` | `1.5056428951173255` | `8.9e-16` |
| attacked represented-operator defect | `0.9972076810972811` | `0.9972076810972789` | `2.2e-15` |
| one-global-unitary frame defect | `1.1309249755520259` | `1.1309249755520259` | `0.0` |
| one-global-unitary operator defect | `0.7442844384409566` | `0.7442844384409564` | `2.2e-16` |
| attacked omitted-block norm at range 4 | `0.00827965689448627` | `0.008279656894486311` | `4.2e-17` |
| attacked construction spectral error at range 4 | `0.006375530149533293` | `0.006375530149533404` | `1.1e-16` |
| reference evaluation spectral error at range 4 | `2.486919115085584e-09` | `2.486917893840257e-09` | `1.22e-15` |
| pointwise evaluation spectral error at range 4 | `2.486918893040979e-09` | `2.4869177828179545e-09` | `1.11e-15` |

The parent, frame-defect, represented-operator, omitted-norm, construction-error, and
reference/pointwise evaluation channels reproduce within the direct verification
absolute tolerance `1e-11`.

## Deliberate convention adaptation

The direct source uses the current canonical KSD polar-transport and centered Fourier
owners. Their closure-phase sign and complete block coordinates are not asserted to be
byte-identical to the historical campaign implementation. The attacked evaluation error
therefore remains a semantic regression rather than an exact-value parity channel. At
range 4, historical M2 reports `0.006429434409208734`, while the direct source reports
`0.006429588433655653`; both are derived from separately fixed 64-point transforms and
the same exact 257-point evaluation inventory.

This difference is not hidden by a compatibility transform. The successor stores and
independently verifies its own current convention, while the historical bytes remain the
authority for historical publication claims.