# Objective-construction and diagnostic sample roles

## Status

This document selects the exact reciprocal-coordinate and coefficient/block diagnostic
roles for the prospective isotropic two-dimensional hopping-shell hierarchy. The
selection precedes threshold and hierarchy-outcome inspection.

It records no calculated candidate result, threshold, witness, certificate, critical
class, scientific validation, or retained experiment evidence.

## Role vocabulary

The $15\times15$ source mesh has the role **objective construction**, not training. No
statistical or machine-learning model is trained. The mesh constructs the deterministic
spectral quadratic and therefore participates directly in admissible-set decisions.

Evaluation, withheld, and locality roles are diagnostic-only. They cannot change a
quadratic, coefficient box, weight, threshold, resolution, witness, certificate,
disposition, or minimum-class conclusion.

## Objective-construction mesh

Define

$$
K_{\mathrm{objective}}=
\left\{\left(\frac{i}{15},\frac{j}{15}\right):
 i,j\in\{-7,-6,\ldots,7\}\right\}.
$$

The exact order is `i` outer and `j` inner, both increasing. The set contains 225 points
and is the complete centered half-open reciprocal mesh used to create the donor hopping
family.

Only this set may:

- construct the spectral design matrix and target vector;
- carry the selected positive nonuniform objective weights;
- define the spectral quadratic and its box-constrained sublevel set;
- participate in threshold design through disclosed source-mesh channel minima; and
- affect common witnesses, support certificates, dispositions, or hierarchy conclusions.

The represented-operator objective separately uses all 225 maximal-domain hopping
blocks with multiplicity weights. Calling reciprocal points objective-construction
samples does not change that complete-block operator domain.

## Common 31-grid diagnostic inventory

Let

$$
I_{31}=\{-15,-14,\ldots,15\}
$$

and let a diagnostic point have reduced coordinate $(i/31,j/31)$. The complete grid has
961 points. Its only intersection with $K_{\mathrm{objective}}$ is $\Gamma=(0,0)$:
if $i/31=p/15$ within the declared representative ranges, coprimality of 15 and 31
requires $i=p=0$ in each coordinate.

The diagnostic inventory excludes $\Gamma$ and partitions the remaining 960 points by
integer parity. Both subsets use `i` outer and `j` inner, both increasing, with filtering
applied without a later sort.

## Evaluation role

Define

$$
K_{\mathrm{evaluation}}=
\left\{\left(\frac{i}{31},\frac{j}{31}\right):
 i,j\in I_{31},\ (i,j)\ne(0,0),\ i+j\equiv0\pmod2\right\}.
$$

This set contains 480 points. Evaluation occurs only after all decisive per-class
objects have been constructed. It reports, for explicitly identified retained points:

- maximum and root-mean-square spectral error against the fixed finite direct parent;
- the complete projected-target interpolation floor against that same parent; and
- exact correlation with class, point role, source, energy shift, and units.

Evaluation values are available for bounded diagnostic interpretation but cannot alter
the decisive hierarchy result.

## Withheld role

Define

$$
K_{\mathrm{withheld}}=
\left\{\left(\frac{i}{31},\frac{j}{31}\right):
 i,j\in I_{31},\ i+j\equiv1\pmod2\right\}.
$$

This set also contains 480 points. It is not inspected during projection, box, weight,
threshold, resolution, method, or figure-data-selection design. It is evaluated only
after the decisive hierarchy result is fixed and reports the same bounded spectral
comparators as the evaluation role.

The role is procedural withholding within one finite synthetic study. It is not a
random sample, independent physical dataset, uncertainty sample, or external validation
set.

## Symmetry and disjointness

The parity of $i+j$ is unchanged modulo two by sign changes and coordinate exchange.
Consequently each 31-grid subset is closed under all eight selected square-symmetry
operations. Excluding the origin from the even subset preserves closure because the
origin is a singleton orbit.

The sets satisfy

$$
|K_{\mathrm{objective}}|=225,
\qquad
|K_{\mathrm{evaluation}}|=|K_{\mathrm{withheld}}|=480,
$$

and

$$
K_{\mathrm{objective}}\cap K_{\mathrm{evaluation}}=
K_{\mathrm{objective}}\cap K_{\mathrm{withheld}}=
K_{\mathrm{evaluation}}\cap K_{\mathrm{withheld}}=\varnothing.
$$

The input constructor and independent verifier must reconstruct the counts, ordering,
closure, union, and pairwise disjointness rather than trust serialized labels.

## Direct-parent comparator

The historical donor result retains the $15\times15$ lowest-band energies and aggregated
errors from its $31\times31$ study, but it does not retain all 961 raw direct-parent
energies. The maintained experiment must therefore reconstruct the diagnostic comparator
from the exact selected finite parent:

- potential coefficients `(lambda_x, lambda_y, lambda_xy) = (0.5, 0.5, 0.30)`;
- plane-wave cutoff 3;
- the donor reciprocal and energy scales;
- lowest ordered scalar eigenvalue at each requested coordinate; and
- the common selected energy shift $\Delta E$.

This is deterministic local evaluation of the declared finite parent, not a continuum
oracle or external-calculator execution. Producer and independent verifier use separate
construction paths and retain their maximum correlation defect.

## Locality-diagnostic role

Locality diagnostics use the fixed maximal real-space inventory rather than an
additional reciprocal mesh:

- all 225 represented blocks;
- all 36 ordered orbit coefficients and multiplicities;
- each of the eight support masks;
- target and retained-point coefficients embedded in the common maximal space; and
- omitted blocks for each support class.

After decisive evidence is fixed, the diagnostics report complete-block omitted norms,
shell-resolved coefficient content, exact inactive-zero defects, and any declared
candidate/certificate-point locality summaries. They do not define the operator
threshold or serve as an alternative separation certificate.

## Execution isolation

`HoppingShellHierarchyExperiment.execute` must construct all decisive class evidence
from the objective spectral mesh and complete-block operator domain before evaluating
either 31-grid diagnostic subset or locality summaries. The immutable result keeps the
decisive hierarchy subtree separate from post-decision diagnostics.

Tests must establish that:

1. changing evaluation coordinates or comparator values cannot change decisive fields;
2. changing withheld coordinates or comparator values cannot change decisive fields;
3. changing locality-diagnostic requests cannot change decisive fields;
4. swapping diagnostic labels fails exact role correlation rather than silently
   relabeling values; and
5. no evaluation, withheld, or locality value is read by threshold, witness,
   certificate, or disposition selection.

The independent verifier reconstructs role inventories and decisive evidence separately.
Passing these tests establishes software role isolation only, not statistical
independence or scientific validation.
