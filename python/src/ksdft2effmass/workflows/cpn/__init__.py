# python/src/ksdft2effmass/workflows/cpn/__init__.py
"""Public backend-neutral Colored Petri Net contract.

The namespace exports immutable project DataObjects/ResultObjects and stateless
ActionObjects for version-1 definition validation, multiset enablement, and
firing. It exports no SNAKES object, persistence repository, external executor,
scientific payload, identity generator, or concrete workflow. Passing its
software-verification tests is not scientific validation or UQ.
"""

from .errors import (
    CpnBindingError,
    CpnContractError,
    CpnDefinitionError,
    CpnErrorCode,
    CpnErrorDetail,
    CpnFiringError,
    CpnGuardEvaluationError,
    CpnMarkingError,
    TransitionNotEnabledError,
)
from .execution import (
    FiringRequest,
    FiringResult,
    TransitionEnablementResult,
    TransitionEnabler,
    TransitionFirer,
)
from .expressions import (
    CpnExpressionEvaluator,
    GuardEvaluationResult,
    GuardExpression,
    GuardOperator,
    TokenFieldAssignment,
    TokenTemplate,
    ValueExpression,
    ValueExpressionKind,
)
from .markings import CpnMarking, PlaceMarking, TokenBinding, TransitionBinding
from .model import (
    ArcDefinition,
    ArcDirection,
    ColorDefinition,
    CpnNetDefinition,
    InputArcMode,
    InputInscription,
    OutputInscription,
    PlaceDefinition,
    TokenPattern,
    TransitionDefinition,
)
from .tokens import (
    ContractValue,
    ContractValueKind,
    CpnToken,
    OutcomeScope,
    OutcomeStatus,
    OutcomeTerminality,
    TokenField,
    TokenOutcome,
)
from .validation import (
    CpnDefinitionValidator,
    CpnIssueCode,
    CpnMarkingValidator,
    CpnValidationIssue,
    CpnValidationResult,
)

__all__ = [
    "ArcDefinition",
    "ArcDirection",
    "ColorDefinition",
    "ContractValue",
    "ContractValueKind",
    "CpnBindingError",
    "CpnContractError",
    "CpnDefinitionError",
    "CpnDefinitionValidator",
    "CpnErrorCode",
    "CpnErrorDetail",
    "CpnExpressionEvaluator",
    "CpnFiringError",
    "CpnGuardEvaluationError",
    "CpnIssueCode",
    "CpnMarking",
    "CpnMarkingError",
    "CpnMarkingValidator",
    "CpnNetDefinition",
    "CpnToken",
    "CpnValidationIssue",
    "CpnValidationResult",
    "FiringRequest",
    "FiringResult",
    "GuardEvaluationResult",
    "GuardExpression",
    "GuardOperator",
    "InputArcMode",
    "InputInscription",
    "OutcomeScope",
    "OutcomeStatus",
    "OutcomeTerminality",
    "OutputInscription",
    "PlaceDefinition",
    "PlaceMarking",
    "TokenBinding",
    "TokenField",
    "TokenFieldAssignment",
    "TokenOutcome",
    "TokenPattern",
    "TokenTemplate",
    "TransitionBinding",
    "TransitionDefinition",
    "TransitionEnablementResult",
    "TransitionEnabler",
    "TransitionFirer",
    "TransitionNotEnabledError",
    "ValueExpression",
    "ValueExpressionKind",
]
