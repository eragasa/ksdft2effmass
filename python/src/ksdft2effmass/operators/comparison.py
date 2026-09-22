r"""Comparison Workflow for compatible represented operator records.

This module owns only the concrete reusable composition
``compatibility -> represented difference -> residual analysis``.  Lower layers
own compatibility auditing, signed subtraction, nonfinite difference detection,
residual norm algorithms, roundoff allowance, and metric-result construction.
No generic Workflow base class is introduced.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .difference import OperatorRecordDifferencer
from .records import OperatorRecord
from .residuals import OperatorRecordComparisonResult, OperatorRecordResidualAnalyzer


@dataclass(frozen=True, slots=True)
class OperatorRecordComparator:
    """Specialized concrete Workflow ActionObject for residual comparison.

    Parameters
    ----------
    differencer
        Dependency that enforces compatibility and constructs the public signed
        represented difference ``candidate - reference``.
    residual_analyzer
        Dependency that computes residual norms from the represented difference.

    Notes
    -----
    This Workflow owns orchestration only.  It does not inspect compatibility
    fields, subtract matrices, calculate norms, repair metric ordering, or
    duplicate validation owned by lower-level public objects.
    """

    differencer: OperatorRecordDifferencer = field(
        default_factory=OperatorRecordDifferencer
    )
    residual_analyzer: OperatorRecordResidualAnalyzer = field(
        default_factory=OperatorRecordResidualAnalyzer
    )

    def __post_init__(self) -> None:
        """Validate the two explicit concrete Workflow dependencies.

        Raises
        ------
        TypeError
            If ``differencer`` is not an
            :class:`~ksdft2effmass.operators.difference.OperatorRecordDifferencer`.
        TypeError
            If ``residual_analyzer`` is not an
            :class:`~ksdft2effmass.operators.residuals.OperatorRecordResidualAnalyzer`.

        Notes
        -----
        This private dataclass hook verifies only the concrete dependencies
        required by the Workflow composition. It applies no compatibility,
        subtraction, residual-norm, roundoff, unit-conversion, physical, or
        scientific policy; those policies remain on lower-level public objects
        or outside the implemented fixed-representation comparison scope.
        """

        if not isinstance(self.differencer, OperatorRecordDifferencer):
            msg = "differencer must be an OperatorRecordDifferencer"
            raise TypeError(msg)
        if not isinstance(self.residual_analyzer, OperatorRecordResidualAnalyzer):
            msg = "residual_analyzer must be an OperatorRecordResidualAnalyzer"
            raise TypeError(msg)

    def execute(
        self, reference: OperatorRecord, candidate: OperatorRecord
    ) -> OperatorRecordComparisonResult:
        r"""Execute represented differencing followed by residual analysis.

        Parameters
        ----------
        reference
            Reference :class:`~ksdft2effmass.operators.records.OperatorRecord`
            supplied to the differencer. It provides the subtracted term in the
            inherited represented-difference sign convention.
        candidate
            Candidate :class:`~ksdft2effmass.operators.records.OperatorRecord`
            supplied to the differencer. It provides the positive term in

            .. math::

               \Delta\mathbf H
               =
               \mathbf H_{\mathrm{candidate}}
               -
               \mathbf H_{\mathrm{reference}}.

        Returns
        -------
        OperatorRecordComparisonResult
            Structural residual-metric result produced by
            :class:`~ksdft2effmass.operators.residuals.OperatorRecordResidualAnalyzer`.
            The metric unit is inherited from the compatible records through the
            represented difference, and stored metrics satisfy the exact ordering
            ``maximum_absolute_residual <= spectral_residual <= frobenius_residual``.

        Raises
        ------
        TypeError
            If either record input is invalid for the lower-level compatibility
            analyzer or residual analyzer.
        ksdft2effmass.operators.compatibility.IncompatibleOperatorRecordsError
            If exact representation compatibility fails before subtraction.
        ksdft2effmass.operators.difference.OperatorRecordDifferenceNumericalError
            If compatible finite records produce a nonfinite represented
            difference during signed subtraction.
        ksdft2effmass.operators.residuals.OperatorRecordComparisonNumericalError
            If residual metric computation, singular-value analysis, metric
            restoration, or material metric-order checking fails numerically.

        Notes
        -----
        This method performs orchestration only. The differencer owns
        compatibility enforcement and signed subtraction; the residual analyzer
        owns norm algorithms, scale handling, and roundoff policy. The Workflow
        introduces no hidden mutation or global state. The returned result is a
        software-verification measurement of an already-compatible fixed
        representation. It does not establish physical equivalence, impurity
        interpretation, scientific acceptability, basis alignment, unit
        conversion, or energy-zero alignment.
        """

        difference = self.differencer.execute(reference, candidate)
        return self.residual_analyzer.execute(difference)
