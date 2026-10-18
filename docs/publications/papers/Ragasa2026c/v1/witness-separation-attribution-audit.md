# Witness–separation attribution audit

## Purpose and status

This working audit records the attribution boundary for Paper 3's
witness-or-separation decision rule. It supports the concise attribution paragraph in
`manuscript.md` and `manuscript.tex`; it is not part of the rendered manuscript and is
not execution evidence.

The audit distinguishes:

1. elementary metric-space consequences;
2. established feasible-set and bounded-error terminology;
3. methods that can produce validated global bounds; and
4. the paper-specific assembly of those components into one thresholded model-comparison
   workflow.

## Bottom line

The workflow is a synthesis of standard metric-space facts, feasibility logic,
set-membership identification, and validated global optimization. The expressions
*common witness* and *certified positive separation* are used descriptively in this
paper. No claim is made that their combination is an established named theory or that
this paper originated the underlying mathematical facts.

The paper-specific contribution is the application of those ingredients to separately
thresholded spectral and aligned-operator admissible sets under a frozen model family,
alignment family, metric, and tolerance contract.

## Claim-by-claim disposition

| Claim | Attribution | Relation | Verification boundary |
|---|---|---|---|
| If $A\cap B\ne\varnothing$, then $\operatorname{dist}(A,B)=0$. | Standard definition of distance between sets; Rudin is cited as a general analysis source. | Immediate definitional consequence. | No theorem-number claim is needed. |
| Any $(a,b)\in A\times B$ gives $\operatorname{dist}(A,B)\le d(a,b)$. | Same definition. | Immediate property of an infimum. | No historical priority claim is made. |
| A certified lower bound $\operatorname{dist}(A,B)\ge L>0$ implies $A\cap B=\varnothing$. | Same definition. | Direct contradiction with $d(x,x)=0$ for a hypothetical common point. | This does not require compactness and is not presented as a contrapositive of a compact-set theorem. |
| Nonempty disjoint compact sets have an attained, strictly positive distance. | Standard compactness and extreme-value argument; Rudin is the manuscript's general source. | Classical metric-space result. | The exact Rudin theorem/page locator has not been checked against a physical copy, so the manuscript does not state one. |
| Failure of a local optimizer, plot, or finite search does not certify positive separation. | Neumaier's review distinguishes incomplete search from complete global methods. | Direct methodological support. | Applicability of a particular complete method to a future model family must be proved separately. |
| Interval methods can support validated enclosures used within complete search. | Moore, Kearfott, and Cloud. | Methodological background. | The book is not cited as the source of the elementary set-distance facts. |
| Threshold-consistent parameters form feasible parameter sets. | Milanese, Norton, Piet-Lahanier, and Walter, eds. | Direct conceptual precedent from bounded-error/set-membership identification. | The semiconductor Hamiltonian losses and alignment contracts remain specific to this work. |
| One workflow should seek either a common witness or a certified positive lower bound. | Composite of the preceding facts and methods. | Paper-specific formalization. | No evidence was found that the exact phrase is established terminology; absence from this search is not proof of originality. |

## Prior-art roles

### Metric-space analysis

Rudin is used only as a standard analysis anchor. Claims about zero distance from a
common point, feasible-pair upper bounds, and positive distance excluding intersection
follow directly from the infimum definition. Compactness supplies attainment and, for
disjoint compact sets, strict positivity.

The supplied preliminary audit associated these facts with Rudin's Theorem 4.16. That
locator has not been checked against a physical copy for this repository version.
Accordingly, neither manuscript states the theorem number or a page number.

### Set-membership identification

*Bounding Approaches to System Identification* establishes bounded-error and
set-membership estimation as a literature in which parameter values are retained or
excluded according to consistency with declared data and bounds. This supports the
feasible-set interpretation, not the paper's particular Hamiltonian losses or the name
of its integrated decision rule.

The Springer record was checked on 18 October 2026. It identifies Mario Milanese, John
Norton, Hélène Piet-Lahanier, and Éric Walter as editors, Springer/Plenum as the 1996
publisher, and DOI
[`10.1007/978-1-4757-9545-5`](https://doi.org/10.1007/978-1-4757-9545-5).

### Complete and validated global search

Neumaier's survey covers constrained global optimization and continuous constraint
satisfaction with explicit emphasis on complete techniques, branch-and-bound, interval
arithmetic, constraint propagation, relaxations, and reliability. It supports the
manuscript's epistemic distinction between a failed incomplete search and a valid global
certificate. It does not prove that any named algorithm is applicable to the paper's
future higher-rank or material-scale families.

The Cambridge publisher record was checked on 18 October 2026 and confirms the title,
author, journal, volume, pages, year, and DOI
[`10.1017/S0962492904000194`](https://doi.org/10.1017/S0962492904000194).

Moore, Kearfott, and Cloud is retained as background for interval arithmetic and
validated enclosures. Its DOI metadata are recorded, but an exact chapter locator for a
specific separation-bound algorithm has not been selected. The manuscript therefore
cites the book only for methodology.

### Model validation and ordinary optimization

Ljung's model-validation treatment is useful background for assessing model adequacy,
but statistical residual validation is not identical to a deterministic positive-distance
certificate. Nocedal and Wright provide optimization background and local/constrained
methods, but failed local search is not a global exclusion result. Neither source is
needed for the concise manuscript paragraph.

Farkas' lemma is an exact alternative theorem for linear inequality systems. It is an
analogy, not a source for the nonlinear metric-space workflow, and is not used in the
Paper 3 proposition.

## Manuscript attribution decision

Paper 3 cites four sources at the point where the proposition is interpreted:

- Rudin for standard metric-space analysis;
- Milanese et al. for feasible-set/set-membership precedent;
- Neumaier for complete global search and the incomplete-search distinction; and
- Moore, Kearfott, and Cloud for interval-analysis methodology.

The manuscript describes the integrated wording as a *paper-specific synthesis*. It does
not call it a new theory, a universal infeasibility solver, or established terminology.
It also retains the distinctions between:

- a verified point in the intersection;
- a feasible pair giving only an upper bound;
- a globally valid positive lower bound;
- a failed search with no certificate; and
- an empty individual admissible set, which is reported separately.

## Candidate references not used as direct support

| Reference | Permitted role | Excluded attribution |
|---|---|---|
| Farkas (1902) | Linear-convex analogy where its premises actually apply. | Source of the general nonlinear set-distance rule. |
| Nocedal and Wright (2006) | Numerical-optimization background and candidate-search methods. | Source of a certified global lower bound from failed local search. |
| Ljung (1999) | Model-validation background. | Deterministic positive-separation theorem. |

## Verification limits and release checklist

- Check the desired Rudin theorem and page locator against an owned or library copy
  before adding a pinpoint citation.
- If a specific interval branch-and-bound algorithm is named, read and cite the exact
  applicable section rather than relying on a general book citation.
- Do not infer originality from failure to locate the exact phrase in this search.
- Do not describe an integer-looking, optimizer-derived, or finite-grid quantity as a
  separation certificate unless the global lower-bound premises are independently
  verified.
- Keep Farkas' lemma restricted to linear systems satisfying its hypotheses.
- Preserve the distinction between parameter-space distance and physical uncertainty,
  energy, or probability.

## Checked bibliographic records

1. W. Rudin, *Principles of Mathematical Analysis*, 3rd ed., McGraw-Hill, New York,
   1976. General bibliographic record accepted; exact internal locator remains unchecked.
2. M. Milanese, J. Norton, H. Piet-Lahanier, and É. Walter, eds., *Bounding Approaches
   to System Identification*, Plenum Press, New York, 1996.
   DOI: [`10.1007/978-1-4757-9545-5`](https://doi.org/10.1007/978-1-4757-9545-5).
3. A. Neumaier, “Complete Search in Continuous Global Optimization and Constraint
   Satisfaction,” *Acta Numerica* **13**, 271–369 (2004).
   DOI: [`10.1017/S0962492904000194`](https://doi.org/10.1017/S0962492904000194).
4. R. E. Moore, R. B. Kearfott, and M. J. Cloud, *Introduction to Interval Analysis*,
   SIAM, Philadelphia, 2009.
   DOI: [`10.1137/1.9780898717716`](https://doi.org/10.1137/1.9780898717716).
5. J. Nocedal and S. J. Wright, *Numerical Optimization*, 2nd ed., Springer, New York,
   2006. DOI: [`10.1007/978-0-387-40065-5`](https://doi.org/10.1007/978-0-387-40065-5).
6. J. Farkas, “Theorie der einfachen Ungleichungen,” *Journal für die reine und
   angewandte Mathematik* **124**, 1–27 (1902).
   DOI: [`10.1515/crll.1902.124.1`](https://doi.org/10.1515/crll.1902.124.1).
7. L. Ljung, *System Identification: Theory for the User*, 2nd ed., Prentice Hall PTR,
   Upper Saddle River, New Jersey, 1999. The chapter-level model-validation locator from
   the preliminary audit remains to be checked against the book before use as a pinpoint
   citation.
