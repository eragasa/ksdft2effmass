"""Public execution-free native-toolchain planning contracts.

The package owns immutable declarations and deterministic build-plan construction. It
performs no discovery, installation, dependency adoption, network access, filesystem
mutation, compilation, or executable invocation.
"""

from .planning import (
    NativeBuildFingerprint,
    NativeBuildFingerprinter,
    NativeBuildLimits,
    NativeBuildPlan,
    NativeBuildPlanner,
    NativeBuildRecipe,
    NativeBuildSpecification,
    NativeCMakeDefinition,
    NativeToolchainFingerprint,
    NativeToolchainFingerprinter,
    NativeToolchainSpecification,
    NativeToolContentIdentity,
    NativeToolContentNotPinned,
    NativeToolRole,
    NativeToolSha256ContentIdentity,
    NativeToolSpecification,
)

__all__ = [
    "NativeBuildFingerprint",
    "NativeBuildFingerprinter",
    "NativeBuildLimits",
    "NativeBuildPlan",
    "NativeBuildPlanner",
    "NativeBuildRecipe",
    "NativeBuildSpecification",
    "NativeCMakeDefinition",
    "NativeToolContentIdentity",
    "NativeToolContentNotPinned",
    "NativeToolRole",
    "NativeToolSha256ContentIdentity",
    "NativeToolSpecification",
    "NativeToolchainFingerprint",
    "NativeToolchainFingerprinter",
    "NativeToolchainSpecification",
]
