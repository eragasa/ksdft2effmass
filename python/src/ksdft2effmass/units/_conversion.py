"""Authoritative in-memory native-to-metal conversion composition."""

from __future__ import annotations

import math
from dataclasses import dataclass
from decimal import Decimal, localcontext

from ._model import (
    AuthorityReference,
    ContentIdentity,
    MetalUnitConversionAuthority,
    MetalUnitConversionCatalog,
    MetalUnitConversionDefinition,
    MetalUnitConversionFailure,
    MetalUnitConversionFailureCode,
    MetalUnitConversionLimitation,
    MetalUnitConversionOutcome,
    MetalUnitConversionRequest,
    MetalUnitConversionResult,
    MetalUnitConversionSuccess,
    MetalUnitInventory,
    NumericalPolicy,
    PhysicalDimension,
    UnitIdentity,
    UnitScalar,
)

_IMPLEMENTATION_IDENTITY = "ksdft2effmass.units.MetalQuantityConverter.v1"
_NUMERICAL_POLICY = NumericalPolicy(
    identity="ksdft2effmass.units.decimal-scale-binary64.v1",
    version=1,
)
_LAMMPS_UNITS_AUTHORITY = AuthorityReference(
    identity="lammps.units-command",
    version="stable_22Jul2025_update6@9c5ab448c78a14fd534619622162ba418d6a1fb1",
    url=(
        "https://raw.githubusercontent.com/lammps/lammps/"
        "stable_22Jul2025_update6/doc/src/units.rst"
    ),
    content_identity=ContentIdentity(
        "sha256:442a188db85bacf28bbbe47541382c09aa6ba6f2a8271bc2aadbf35d16987834"
    ),
)
#: Exact canonical dimensional inventory pinned to the retained LAMMPS document.
METAL_UNIT_INVENTORY = MetalUnitInventory(
    identity="ksdft2effmass.units.metal-canonical-inventory",
    version=1,
    content_identity=ContentIdentity(
        "sha256:a6c80626e92f510b17bae0a2d3854624b796c5abdd62409b5993fad33db53120"
    ),
    authority=_LAMMPS_UNITS_AUTHORITY,
    mass_unit=UnitIdentity.GRAM_PER_MOLE,
    distance_unit=UnitIdentity.ANGSTROM,
    time_unit=UnitIdentity.PICOSECOND,
    energy_unit=UnitIdentity.ELECTRON_VOLT,
    velocity_unit=UnitIdentity.ANGSTROM_PER_PICOSECOND,
    force_unit=UnitIdentity.ELECTRON_VOLT_PER_ANGSTROM,
    torque_unit=UnitIdentity.ELECTRON_VOLT,
    temperature_unit=UnitIdentity.KELVIN,
    pressure_unit=UnitIdentity.BAR,
    dynamic_viscosity_unit=UnitIdentity.POISE,
    charge_unit=UnitIdentity.ELEMENTARY_CHARGE_MULTIPLE,
    dipole_unit=UnitIdentity.ELEMENTARY_CHARGE_ANGSTROM,
    electric_field_unit=UnitIdentity.VOLT_PER_ANGSTROM,
    density_unit=UnitIdentity.GRAM_PER_CENTIMETER_POWER_DIMENSION,
)

_AUTHORITY = MetalUnitConversionAuthority(
    lammps_units_document=_LAMMPS_UNITS_AUTHORITY,
    nist_codata_adjustment=AuthorityReference(
        identity="nist.codata.complete-listing",
        version="2022 CODATA adjustment",
        url="https://physics.nist.gov/cuu/Constants/Table/allascii.txt",
        content_identity=ContentIdentity(
            "sha256:77fb90e66c40db3e6eb16630bc9c88e4c7c8beddbe5e71be406f2f26e3f67e67"
        ),
    ),
    bipm_si_brochure=AuthorityReference(
        identity="bipm.si-brochure.english",
        version="9th edition (2019), updated in 2026, asset version 7.0",
        url=(
            "https://www.bipm.org/documents/20126/41483022/"
            "SI-Brochure-9-EN.pdf/2d2b50bf-f2b4-9661-f402-5f9d66e4b507"
            "?version=7.0"
        ),
        content_identity=ContentIdentity(
            "sha256:5442eea2c680caf77a9d96879205a97f57c7c270b98a0bd0126c18fefe47e02c"
        ),
        doi="10.59161/AUEZ1291",
    ),
)

#: Exact authorized native-to-canonical conversion-definition catalog.
METAL_UNIT_CONVERSION_CATALOG = MetalUnitConversionCatalog(
    identity="ksdft2effmass.units.metal-native-conversions",
    version=1,
    content_identity=ContentIdentity(
        "sha256:f8555a74b689f05a2f9267030b627c690839c26c4ad6d582e236d366f113fe7e"
    ),
    definitions=(
        MetalUnitConversionDefinition(
            identity="hartree-to-electron-volt",
            version=1,
            content_identity=ContentIdentity(
                "sha256:2fb00672d6de492db9619b4e532fbef55cc0029f4e7644f3def5eae5510d626b"
            ),
            source_unit=UnitIdentity.HARTREE,
            target_unit=UnitIdentity.ELECTRON_VOLT,
            source_dimension=PhysicalDimension.ENERGY,
            target_dimension=PhysicalDimension.ENERGY,
            decimal_scale=Decimal("27.211386245981"),
            standard_uncertainty=Decimal("0.000000000030"),
            numerical_policy=_NUMERICAL_POLICY,
            authority=_AUTHORITY,
            implementation_identity=_IMPLEMENTATION_IDENTITY,
        ),
        MetalUnitConversionDefinition(
            identity="rydberg-to-electron-volt",
            version=1,
            content_identity=ContentIdentity(
                "sha256:b2aaace372a88fba0d321664512c9fcd00e49094741903e28aa0cd43ee924154"
            ),
            source_unit=UnitIdentity.RYDBERG,
            target_unit=UnitIdentity.ELECTRON_VOLT,
            source_dimension=PhysicalDimension.ENERGY,
            target_dimension=PhysicalDimension.ENERGY,
            decimal_scale=Decimal("13.6056931229905"),
            standard_uncertainty=Decimal("0.000000000015"),
            numerical_policy=_NUMERICAL_POLICY,
            authority=_AUTHORITY,
            implementation_identity=_IMPLEMENTATION_IDENTITY,
        ),
        MetalUnitConversionDefinition(
            identity="bohr-to-angstrom",
            version=1,
            content_identity=ContentIdentity(
                "sha256:91adb62af983494f479467b143c4507b945af1e34f23d801fa3e9f172fac609c"
            ),
            source_unit=UnitIdentity.BOHR,
            target_unit=UnitIdentity.ANGSTROM,
            source_dimension=PhysicalDimension.LENGTH,
            target_dimension=PhysicalDimension.LENGTH,
            decimal_scale=Decimal("0.529177210544"),
            standard_uncertainty=Decimal("0.000000000082"),
            numerical_policy=_NUMERICAL_POLICY,
            authority=_AUTHORITY,
            implementation_identity=_IMPLEMENTATION_IDENTITY,
        ),
        MetalUnitConversionDefinition(
            identity="unified-atomic-mass-unit-to-gram-per-mole",
            version=1,
            content_identity=ContentIdentity(
                "sha256:12590b98302929d722bd5fa9f662c8da3534fdc576f86ceaea4c278727cea77b"
            ),
            source_unit=UnitIdentity.UNIFIED_ATOMIC_MASS_UNIT,
            target_unit=UnitIdentity.GRAM_PER_MOLE,
            source_dimension=PhysicalDimension.ATOMIC_MASS,
            target_dimension=PhysicalDimension.MOLAR_MASS,
            decimal_scale=Decimal("1.00000000105"),
            standard_uncertainty=Decimal("0.00000000031"),
            numerical_policy=_NUMERICAL_POLICY,
            authority=_AUTHORITY,
            implementation_identity=_IMPLEMENTATION_IDENTITY,
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class MetalQuantityConverter:
    """Convert explicit native scalars into demonstrated canonical metal units.

    Parameters
    ----------
    catalog
        Exact immutable conversion-definition catalog. Every definition's
        implementation identity must match this converter implementation.

    Raises
    ------
    TypeError
        If ``catalog`` is not a :class:`MetalUnitConversionCatalog`.
    ValueError
        If any definition targets a different converter implementation identity.
    """

    catalog: MetalUnitConversionCatalog = METAL_UNIT_CONVERSION_CATALOG

    def __post_init__(self) -> None:
        if type(self.catalog) is not MetalUnitConversionCatalog:
            raise TypeError("catalog must be MetalUnitConversionCatalog")
        if any(
            definition.implementation_identity != _IMPLEMENTATION_IDENTITY
            for definition in self.catalog.definitions
        ):
            raise ValueError(
                "every definition must target this converter implementation"
            )

    @property
    def implementation_identity(self) -> str:
        """Return the exact converter implementation identity.

        Returns
        -------
        str
            Stable identity correlated by every accepted conversion definition.
        """
        return _IMPLEMENTATION_IDENTITY

    def convert(self, request: MetalUnitConversionRequest) -> MetalUnitConversionResult:
        """Convert one scalar or return a closed represented failure.

        Parameters
        ----------
        request
            Exact finite source scalar, requested target unit, and optional source
            correlation.

        Returns
        -------
        MetalUnitConversionSuccess or MetalUnitConversionFailure
            Correlated success for a finite represented output, or a closed
            unsupported, overflow, or underflow failure.

        Raises
        ------
        TypeError
            If ``request`` is not a :class:`MetalUnitConversionRequest`.

        Notes
        -----
        The exact source binary64 value is converted to ``Decimal`` without loss,
        multiplied by the selected exact decimal scale at precision 80, and rounded
        once to binary64. Conversion-factor uncertainty is retained on the cited
        definition but is not propagated into the output scalar.
        """
        if type(request) is not MetalUnitConversionRequest:
            raise TypeError("request must be MetalUnitConversionRequest")
        definition = self.catalog.definition_for(
            request.source.unit, request.target_unit
        )
        if definition is None:
            return MetalUnitConversionFailure(
                outcome=MetalUnitConversionOutcome.UNSUPPORTED,
                code=MetalUnitConversionFailureCode.UNSUPPORTED_UNIT_PAIR,
                request=request,
                definition=None,
                catalog_identity=self.catalog.identity,
                catalog_version=self.catalog.version,
                catalog_content_identity=self.catalog.content_identity,
                limitations=(),
            )

        with localcontext() as context:
            context.prec = 80
            exact_output = Decimal.from_float(request.source.value) * (
                definition.decimal_scale
            )
        output_value = float(exact_output)
        limitations = (
            MetalUnitConversionLimitation.BINARY64_OUTPUT_ROUNDED,
            MetalUnitConversionLimitation.FACTOR_UNCERTAINTY_NOT_PROPAGATED,
        )
        if not math.isfinite(output_value):
            return MetalUnitConversionFailure(
                outcome=MetalUnitConversionOutcome.OVERFLOW,
                code=MetalUnitConversionFailureCode.BINARY64_OVERFLOW,
                request=request,
                definition=definition,
                catalog_identity=self.catalog.identity,
                catalog_version=self.catalog.version,
                catalog_content_identity=self.catalog.content_identity,
                limitations=limitations,
            )
        if request.source.value != 0.0 and output_value == 0.0:
            return MetalUnitConversionFailure(
                outcome=MetalUnitConversionOutcome.UNDERFLOW,
                code=MetalUnitConversionFailureCode.NONZERO_ROUNDED_TO_ZERO,
                request=request,
                definition=definition,
                catalog_identity=self.catalog.identity,
                catalog_version=self.catalog.version,
                catalog_content_identity=self.catalog.content_identity,
                limitations=limitations,
            )
        return MetalUnitConversionSuccess(
            outcome=MetalUnitConversionOutcome.CONVERTED,
            request=request,
            output=UnitScalar(output_value, request.target_unit),
            definition=definition,
            catalog_identity=self.catalog.identity,
            catalog_version=self.catalog.version,
            catalog_content_identity=self.catalog.content_identity,
            limitations=limitations,
        )
