# `Periodic1DFourierLocalityRangeResult` numerics

Representatives are derived as every integer from `-R` through `R`. Both complex
coefficient vectors have length `2R+1` and use the same ordering. Construction and
evaluation candidates are separate real vectors for each route.

The root evaluates each coefficient vector with

\[
E_R(k)=\sum_{r=-R}^{R} e^{2\pi i kr}t_r
\]

and compares it with the corresponding stored candidate. Scalar Hermiticity requires
`t_{-r}=conj(t_r)`. Direct-design rank and condition number are correlated with the
construction design matrix.

Stored channels keep truncation maximum/root-mean-square error, mediated total error,
direct total error, omitted coefficient norm, Parseval comparison, training residual,
coefficient defect, sampled defect, bandwidth, curvature, and imaginary residual
separate.

Application passage is derived from each route's stored total maximum error. At root
admission, stored and recomputed decisive errors must produce the same inclusive
threshold disposition.
