Quantities of interest and DFT reference targets
================================================

A quantity of interest (QoI) states what scientific scalar is required. A DFT
calculation can produce observations from which that scalar is evaluated, but the
calculation is not itself the QoI and its value is not automatically physical truth.
The initial public analysis records preserve this distinction.

Definition and reference
------------------------

``ScalarQuantityOfInterestDefinition`` identifies:

* the modeled subject and an optional represented state-space identity when one is
  required;
* the complete convention set needed to interpret the value;
* the deterministic evaluator identity and version;
* the ordered normalized observations required by that evaluator;
* the completeness rule; and
* the output unit.

The definition contains no reference value, tolerance, fitting weight, loss,
calculator selection, native input, execution authority, or acceptance decision.

``ScalarQuantityOfInterestValue`` records a successful evaluator result. It binds the
complete QoI definition and finite value to the exact evaluator and normalized
observation-set ResultObject identities. Its ``unit`` property is the unit declared by
the QoI definition; the record performs no unit conversion.

``ScalarQuantityOfInterestEvaluationFailure`` is the disjoint failed result. Its
closed code distinguishes unavailable, incomplete, incompatible, invalid, and error
outcomes, and it contains no scalar value. A caller must not replace failure with zero,
NaN, or a default.

``DftScalarQuantityOfInterestReferenceTarget`` associates one successful scalar
evaluation with exact identities for the DFT calculation, calculator, method, source
result, producer provenance, artifact-manifest revision, and source manifest entries.
The target derives its quantity, value, and unit from the retained evaluation.

Reference provenance
--------------------

A DFT target is explicitly a **calculated result**. Its represented source must include
at least one lexically ordered, unique artifact-manifest entry. Artifact identity and
provenance correlation do not establish that the source calculation converged or that
the chosen physical model is adequate.

The optional parent-model and numerical-error assessment identities are separate:

* a parent-model assessment concerns limitations of the represented DFT model, such
  as the selected exchange-correlation approximation or pseudopotential model; and
* a numerical-error assessment concerns discretization or solver effects under that
  model, such as finite cutoff, reciprocal-space sampling, or incomplete convergence.

``None`` for either assessment means that no assessment is represented. It never
means zero error. Model-reduction error belongs to a later comparison between models
and is not a field of the DFT reference target.

DFT-to-LAMMPS comparison
------------------------

The intended later flow is:

.. code-block:: text

   DFT result ------> normalized observations ------> DFT reference QoI
                                                           |
   LAMMPS result ---> normalized observations ------> predicted QoI
                                                           |
                                                           v
                                                comparator or fitting loss

A later comparator must establish equality or explicit alignment of subject, any
applicable represented state space, geometry, units, normalization, energy reference,
ordering, and every other applicable convention before subtracting values. Tolerances, weights, and loss
functions belong to that comparator or fitting ActionObject, not to the QoI or
reference target.

Current limitations
-------------------

The implemented public slice is scalar and in-memory only. It defines successful and
failed evaluation ResultObjects but does not yet provide an evaluator ActionObject or
the normalized-observation payload consumed by one. It also provides no
vector/tensor/field values, LAMMPS binder or Simulation Task, serialization,
persistence, comparison, fitting, numerical verification, scientific validation, or
uncertainty quantification.
