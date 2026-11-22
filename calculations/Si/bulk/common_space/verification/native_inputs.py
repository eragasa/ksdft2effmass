"""Declared native-byte correlation and shared parsing, not full CSD0 admission."""

from __future__ import annotations

import hashlib
import importlib
from dataclasses import dataclass
from importlib.metadata import version
from math import isfinite
from pathlib import Path
from typing import ClassVar

from ksdft2effmass.serialization.enums import StrWireEnum
from projectkoios.integrations.wannier90 import (
    Wannier90DisentanglementMatrixData,
    Wannier90DisentanglementMatrixParser,
    Wannier90NativeArtifact,
    Wannier90NativeArtifactCorrelationResult,
    Wannier90NativeArtifactCorrelator,
    Wannier90NativeArtifactIdentity,
    Wannier90TrialOrbitalOverlapData,
    Wannier90TrialOrbitalOverlapParser,
    Wannier90UnitaryMatrixData,
    Wannier90UnitaryMatrixParser,
)


class CommonSpaceTrialConvention(StrWireEnum):
    """The one explicitly supported native-to-atomic trial convention."""

    two_center_sp3s_star = "two-center-eight-sp3-two-radial-s-to-atomic-sp3s-star"


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceProviderModuleIdentity:
    """One caller-declared parser source identity, without a deployment path."""

    module_name: str
    sha256: str

    def __post_init__(self) -> None:
        if type(self.module_name) is not str or not self.module_name:
            raise ValueError("module_name must be a nonempty built-in string")
        if (
            type(self.sha256) is not str
            or len(self.sha256) != 64
            or any(value not in "0123456789abcdef" for value in self.sha256)
        ):
            raise ValueError("sha256 must be lowercase SHA-256 hexadecimal")


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceProviderBinding:
    """Exact consumed provider-source closure, not process or scientific attestation."""

    REQUIRED_MODULES: ClassVar[tuple[str, ...]] = (
        "projectkoios.integrations.wannier90",
        "projectkoios.integrations.wannier90._matrix_conventions",
        "projectkoios.integrations.wannier90._parsing",
        "projectkoios.integrations.wannier90.artifacts",
        "projectkoios.integrations.wannier90.interface_data",
        "projectkoios.integrations.wannier90.unitary_matrices",
        "projectkoios.integrations.wannier90.disentanglement_matrices",
    )

    distribution_version: str
    modules: tuple[CommonSpaceProviderModuleIdentity, ...]

    def __post_init__(self) -> None:
        if type(self.distribution_version) is not str or not self.distribution_version:
            raise ValueError("distribution_version must be a nonempty built-in string")
        if type(self.modules) is not tuple or any(
            type(module) is not CommonSpaceProviderModuleIdentity
            for module in self.modules
        ):
            raise TypeError("modules must be a tuple of provider module identities")
        if (
            tuple(module.module_name for module in self.modules)
            != self.REQUIRED_MODULES
        ):
            raise ValueError(
                "provider module closure must be complete and in declared order"
            )

    def authenticate(self) -> None:
        """Compare current source bytes to supplied declarations before parsing."""
        if version("projectkoios-simulations") != self.distribution_version:
            raise RuntimeError("provider distribution version differs from declaration")
        for declaration in self.modules:
            module = importlib.import_module(declaration.module_name)
            if module.__file__ is None:
                raise RuntimeError("provider module has no source-file identity")
            observed = hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
            if observed != declaration.sha256:
                raise RuntimeError(
                    f"provider module SHA-256 differs: {declaration.module_name}"
                )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceNativeInputContract:
    """Explicit native roles, dimensions, point order, and declared state labels.

    This contract is restricted to the spinless scalar-relativistic non-SOC two-center
    ten-orbital trial convention. Geometry and energy-reference identities are opaque
    caller declarations, not verified physical associations. Overlaps and fractional
    coordinates are dimensionless; no Hamiltonian or energy subtraction occurs.

    Coordinates must be nested built-in tuples of finite built-in floats. No grid,
    origin, periodic normalization, or coordinate tolerance is inferred. Parent-band
    count is a built-in integer at least ten. AMN has no coordinate records: its point
    order is a caller-declared cross-artifact correlation, not established by count.
    Equal dimensions do not authenticate common parent-band or gauge state spaces;
    those physical source associations remain full-CSD0 obligations.
    """

    ATOMIC_BASIS_ORDER: ClassVar[tuple[str, ...]] = tuple(
        f"{center}:{orbital}"
        for center in (
            "diamond_origin_center",
            "diamond_body_diagonal_quarter_center",
        )
        for orbital in ("s", "px", "py", "pz", "s-star")
    )

    trial_overlap_identity: Wannier90NativeArtifactIdentity
    gauge_identity: Wannier90NativeArtifactIdentity
    disentanglement_identity: Wannier90NativeArtifactIdentity
    ordered_fractional_kpoints: tuple[tuple[float, float, float], ...]
    parent_band_count: int
    atomic_basis_order: tuple[str, ...]
    trial_convention: CommonSpaceTrialConvention
    geometry_identity: str
    energy_reference_identity: str

    def __post_init__(self) -> None:
        if any(
            type(identity) is not Wannier90NativeArtifactIdentity
            for identity in self.identities
        ):
            raise TypeError(
                "native identities must use the exact provider identity type"
            )
        if len({identity.name for identity in self.identities}) != 3:
            raise ValueError("native artifact roles must use three distinct names")
        if type(self.parent_band_count) is not int or self.parent_band_count < 10:
            raise ValueError(
                "parent_band_count must be a built-in integer at least ten"
            )
        if (
            type(self.ordered_fractional_kpoints) is not tuple
            or not self.ordered_fractional_kpoints
        ):
            raise ValueError("ordered_fractional_kpoints must be a nonempty tuple")
        for point in self.ordered_fractional_kpoints:
            if (
                type(point) is not tuple
                or len(point) != 3
                or any(
                    type(value) is not float or not isfinite(value) for value in point
                )
            ):
                raise ValueError(
                    "fractional coordinates must be tuple triples of finite built-in floats"
                )
        if len(set(self.ordered_fractional_kpoints)) != len(
            self.ordered_fractional_kpoints
        ):
            raise ValueError("ordered fractional k points must be unique")
        if (
            type(self.atomic_basis_order) is not tuple
            or self.atomic_basis_order != self.ATOMIC_BASIS_ORDER
        ):
            raise ValueError(
                "atomic_basis_order differs from the explicit two-center trial basis"
            )
        if type(self.trial_convention) is not CommonSpaceTrialConvention:
            raise TypeError("trial_convention must be a CommonSpaceTrialConvention")
        for label in (self.geometry_identity, self.energy_reference_identity):
            if type(label) is not str or not label:
                raise ValueError(
                    "geometry and energy-reference identities must be nonempty built-in strings"
                )

    @property
    def identities(self) -> tuple[Wannier90NativeArtifactIdentity, ...]:
        return (
            self.trial_overlap_identity,
            self.gauge_identity,
            self.disentanglement_identity,
        )

    def require_ordered_index(self, index: int) -> None:
        """Reject booleans, strings, and indices outside the declared point order."""
        if type(index) is not int or not 0 <= index < len(
            self.ordered_fractional_kpoints
        ):
            raise ValueError(
                "ordered_index must be a built-in integer in the declared point set"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceParsedNativeInputs:
    """Immutable shared parsed records with exact native correlation receipts.

    Obtain this object through CommonSpaceNativeInputLoader. Its receipt establishes
    native-byte equality to caller declarations, not reviewed membership, a complete
    CSD0 ledger, native-decimal uncertainty, or retained-execution authority.
    """

    contract: CommonSpaceNativeInputContract
    provider_binding: CommonSpaceProviderBinding
    source_correlation: Wannier90NativeArtifactCorrelationResult
    trial_overlaps: Wannier90TrialOrbitalOverlapData
    gauge: Wannier90UnitaryMatrixData
    disentanglement: Wannier90DisentanglementMatrixData

    def __post_init__(self) -> None:
        if (
            type(self.contract) is not CommonSpaceNativeInputContract
            or type(self.provider_binding) is not CommonSpaceProviderBinding
            or type(self.source_correlation)
            is not Wannier90NativeArtifactCorrelationResult
            or type(self.trial_overlaps) is not Wannier90TrialOrbitalOverlapData
            or type(self.gauge) is not Wannier90UnitaryMatrixData
            or type(self.disentanglement) is not Wannier90DisentanglementMatrixData
        ):
            raise TypeError(
                "parsed native inputs must use their exact declared record types"
            )
        if self.source_correlation.expected_identities != self.contract.identities:
            raise ValueError("native correlation receipt differs from contract")
        point_count = len(self.contract.ordered_fractional_kpoints)
        if (
            self.trial_overlaps.kpoint_count != point_count
            or self.gauge.kpoint_count != point_count
            or self.disentanglement.kpoint_count != point_count
            or self.trial_overlaps.band_count != self.contract.parent_band_count
            or self.disentanglement.band_count != self.contract.parent_band_count
            or self.trial_overlaps.trial_orbital_count != 10
            or self.gauge.wannier_count != 10
            or self.disentanglement.wannier_count != 10
        ):
            raise ValueError("parsed native dimensions differ from explicit contract")
        for coordinates in (
            self.gauge.fractional_kpoints,
            self.disentanglement.fractional_kpoints,
        ):
            for index, declared in enumerate(self.contract.ordered_fractional_kpoints):
                observed = tuple(float(value) for value in coordinates.magnitude[index])
                if observed != declared:
                    raise ValueError(
                        "parsed ordered k points differ from explicit contract"
                    )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceNativeInputLoader:
    """Authenticate all supplied immutable bytes before shared provider parsing.

    No paths are read for native data, and no parser, filename inference, alternate
    source, missing-module fallback, or producer computational input is introduced.
    Parser source files are read only to check their explicitly declared identities.
    """

    contract: CommonSpaceNativeInputContract
    provider_binding: CommonSpaceProviderBinding
    artifacts: tuple[Wannier90NativeArtifact, ...]

    def __post_init__(self) -> None:
        if type(self.contract) is not CommonSpaceNativeInputContract:
            raise TypeError("contract must be a CommonSpaceNativeInputContract")
        if type(self.provider_binding) is not CommonSpaceProviderBinding:
            raise TypeError("provider_binding must be a CommonSpaceProviderBinding")
        if type(self.artifacts) is not tuple or any(
            type(artifact) is not Wannier90NativeArtifact for artifact in self.artifacts
        ):
            raise TypeError(
                "artifacts must be a tuple of exact native artifact records"
            )

    def execute(self) -> CommonSpaceParsedNativeInputs:
        self.provider_binding.authenticate()
        correlation = Wannier90NativeArtifactCorrelator().execute(
            expected_identities=self.contract.identities,
            artifacts=self.artifacts,
        )
        payloads = {artifact.name: artifact.payload for artifact in self.artifacts}
        return CommonSpaceParsedNativeInputs(
            contract=self.contract,
            provider_binding=self.provider_binding,
            source_correlation=correlation,
            trial_overlaps=Wannier90TrialOrbitalOverlapParser(
                payload=payloads[self.contract.trial_overlap_identity.name]
            ).parse(),
            gauge=Wannier90UnitaryMatrixParser().execute(
                payloads[self.contract.gauge_identity.name]
            ),
            disentanglement=Wannier90DisentanglementMatrixParser().execute(
                payloads[self.contract.disentanglement_identity.name]
            ),
        )
