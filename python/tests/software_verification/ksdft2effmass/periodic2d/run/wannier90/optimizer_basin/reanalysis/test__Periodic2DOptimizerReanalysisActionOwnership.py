r"""Routine ownership evidence for row-053 Action decomposition.

Evidence profile: routine

The tests establish implementation ownership and collaborator composition only. They do
not authenticate retained artifacts or establish numerical or scientific validity.
"""

import inspect
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis import (
    authentication,
    correlation,
    decode,
    numerics,
    refinement,
    verify,
)
from ksdft2effmass.serialization.json import immutable as immutable_json

pytestmark = pytest.mark.software_verification


class TestPeriodic2DOptimizerReanalysisActionOwnership:
    """Own structural Action-conformance evidence for crosswalk row 053."""

    def test_actions__use_instantiated_owners_without_static_namespaces(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-OWNERSHIP-001.

        Requirement: Reusable decoding, authentication, correlation, numerical, and
        refinement behavior belongs to instantiated cohesive Actions rather than static
        or class-method utility namespaces.

        Acceptance: Every reviewed Action class has no static/class methods and exposes
        an instance ``execute`` operation.
        """
        action_classes = (
            authentication.OptimizerReanalysisRepositorySourceAuthenticator,
            authentication.Periodic2DOptimizerReanalysisSourceAuthenticator,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder,
            correlation.Periodic2DOptimizerReanalysisCorrelator,
            numerics.OptimizerReanalysisTerminalTraceClassifier,
            numerics.OptimizerReanalysisEndpointSpreadVerifier,
            numerics.SquareLatticeCenterSetTransformer,
            numerics.PeriodicCenterSetDistanceEvaluator,
            numerics.PeriodicCenterSetComparator,
            numerics.OptimizerReanalysisBasinPartitioner,
            refinement.OptimizerReanalysisRefinementVerifier,
            verify.Periodic2DOptimizerReanalysisCampaignVerifier,
        )

        for action_class in action_classes:
            assert callable(action_class().execute)
            assert not any(
                isinstance(member, (staticmethod, classmethod))
                for member in vars(action_class).values()
            )

    def test_verifier__composes_cohesive_request_scoped_actions(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-OWNERSHIP-002.

        Requirement: The top-level verifier owns orchestration, while schema decoding,
        compact authentication, campaign correlation, and refinement remain separate.

        Acceptance: A fresh verifier contains exact collaborator Action types and no
        private computational methods.
        """
        verifier_action = verify.Periodic2DOptimizerReanalysisCampaignVerifier()

        assert (
            type(verifier_action.decoder)
            is decode.Periodic2DOptimizerReanalysisDocumentDecoder
        )
        assert (
            type(verifier_action.source_authenticator)
            is authentication.Periodic2DOptimizerReanalysisSourceAuthenticator
        )
        assert (
            type(verifier_action.correlator)
            is correlation.Periodic2DOptimizerReanalysisCorrelator
        )
        assert (
            type(verifier_action.refinement_verifier)
            is refinement.OptimizerReanalysisRefinementVerifier
        )
        private_computations = {
            name
            for name, member in vars(type(verifier_action)).items()
            if name.startswith("_") and not name.startswith("__") and callable(member)
        }
        assert private_computations == set()

    def test_action_requests__reject_implicit_numeric_and_path_coercion(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-OWNERSHIP-003.

        Requirement: Numerical and repository-boundary requests reject booleans,
        integer center coordinates, and relative repository roots rather than coercing
        them into another representation.

        Acceptance: Each incompatible synthetic request raises its documented error.
        """
        centers = ((0.0, 0.0),)
        with pytest.raises(TypeError, match="coordinates must be binary64 floats"):
            numerics.PeriodicCenterSetComparisonRequest(
                first=((0, 0),),
                second=centers,
                include_square_lattice_symmetry=False,
            )
        with pytest.raises(TypeError, match="operation must be an integer"):
            numerics.SquareLatticeCenterSetTransformer().execute(
                centers,
                True,
            )
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            authentication.OptimizerReanalysisRepositorySourceAuthenticationRequest(
                repository_root=Path("relative"),
                declared_path="source.py",
                expected_sha256="0" * 64,
                label="source",
            )

    def test_reviewed_modules__have_no_module_functions(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-OWNERSHIP-004.

        Requirement: Row-053 and its changed shared immutable-JSON owner contain no
        module-level helper/function namespace.

        Acceptance: Introspection finds no function defined directly by a reviewed
        module.
        """
        modules = (
            authentication,
            correlation,
            decode,
            immutable_json,
            numerics,
            refinement,
            verify,
        )

        module_functions = {
            f"{module.__name__}.{name}"
            for module in modules
            for name, value in inspect.getmembers(module, inspect.isfunction)
            if value.__module__ == module.__name__
        }

        assert module_functions == set()

    def test_public_methods__retain_numpy_style_contract_sections(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-OWNERSHIP-005.

        Requirement: Every public-by-name reviewed method documents parameters,
        non-None returns, and applicable exceptions with NumPy-style sections.

        Acceptance: Introspection finds no reviewed method missing an applicable
        section; authentication/correlation name ``TypeError`` and numeric adapters name
        propagated ``OverflowError`` explicitly.
        """
        modules = (
            authentication,
            correlation,
            decode,
            immutable_json,
            numerics,
            refinement,
            verify,
        )
        missing: set[str] = set()
        for module in modules:
            classes = (
                value
                for _, value in inspect.getmembers(module, inspect.isclass)
                if value.__module__ == module.__name__
            )
            for class_ in classes:
                for name, method in inspect.getmembers(class_, inspect.isfunction):
                    if name.startswith("_"):
                        continue
                    docstring = inspect.getdoc(method) or ""
                    signature = inspect.signature(method)
                    has_parameters = "Parameters\n" in docstring
                    if len(signature.parameters) > 1 and not has_parameters:
                        missing.add(f"{class_.__name__}.{name}:Parameters")
                    if (
                        signature.return_annotation not in {None, type(None), "None"}
                        and "Returns\n" not in docstring
                    ):
                        missing.add(f"{class_.__name__}.{name}:Returns")
                    if "Raises\n" not in docstring:
                        missing.add(f"{class_.__name__}.{name}:Raises")

        typed_failure_methods = (
            authentication.OptimizerReanalysisRepositorySourceAuthenticator.execute,
            authentication.Periodic2DOptimizerReanalysisSourceAuthenticator.execute,
            correlation.Periodic2DOptimizerReanalysisCorrelator.execute,
        )
        for typed_method in typed_failure_methods:
            if "TypeError\n" not in (inspect.getdoc(typed_method) or ""):
                missing.add(f"{typed_method.__qualname__}:TypeError")
        overflow_adapters = (
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.source_result,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.source_configuration,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.source_endpoint,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.reanalysis_result,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.method,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.configuration,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.endpoint,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.spread_components,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.refinement,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.refinement_size,
            decode.Periodic2DOptimizerReanalysisDocumentDecoder.center_set,
        )
        for adapter in overflow_adapters:
            if "OverflowError\n" not in (inspect.getdoc(adapter) or ""):
                missing.add(f"{adapter.__qualname__}:OverflowError")

        assert missing == set()
