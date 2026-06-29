"""
parameter_registry.py
=====================

Registry of all supported chemistries and simulation levels.

This module only stores registry information.
Loading is handled by loader.py.
"""

# ============================================================
# Base Package
# ============================================================

BASE_PACKAGE = "physion_core.params"


# ============================================================
# Supported Chemistries
# ============================================================

CHEMISTRIES = {

    "lithium_metal": {
        "name": "Lithium Metal",
        "enabled": True,
    },

    "lfp": {
        "name": "Lithium Iron Phosphate",
        "enabled": True,
    },

    "nmc": {
        "name": "Nickel Manganese Cobalt",
        "enabled": True,
    },

    "lithium_sulfur": {
        "name": "Lithium Sulfur",
        "enabled": True,
    },

}


# ============================================================
# Supported Simulation Levels
# ============================================================

LEVELS = {

    "basic": {
        "name": "Basic",
        "priority": 1,
    },

    "advanced": {
        "name": "Advanced",
        "priority": 2,
    },

    "industrial": {
        "name": "Industrial",
        "priority": 3,
    },

}


# ============================================================
# Convenience Constants
# ============================================================

SUPPORTED_CHEMISTRIES = tuple(CHEMISTRIES.keys())

SUPPORTED_LEVELS = tuple(LEVELS.keys())


# ============================================================
# Parameter Module Registry
# ============================================================

PARAMETER_REGISTRY = {

    # --------------------------------------------------------
    # Lithium Metal
    # --------------------------------------------------------

    ("lithium_metal", "basic"):
        f"{BASE_PACKAGE}.basic.lithium_metal",

    ("lithium_metal", "advanced"):
        f"{BASE_PACKAGE}.advanced.lithium_metal",

    ("lithium_metal", "industrial"):
        f"{BASE_PACKAGE}.industrial.lithium_metal",

    # --------------------------------------------------------
    # LFP
    # --------------------------------------------------------

    ("lfp", "basic"):
        f"{BASE_PACKAGE}.basic.lfp",

    ("lfp", "advanced"):
        f"{BASE_PACKAGE}.advanced.lfp",

    ("lfp", "industrial"):
        f"{BASE_PACKAGE}.industrial.lfp",

    # --------------------------------------------------------
    # NMC
    # --------------------------------------------------------

    ("nmc", "basic"):
        f"{BASE_PACKAGE}.basic.nmc",

    ("nmc", "advanced"):
        f"{BASE_PACKAGE}.advanced.nmc",

    ("nmc", "industrial"):
        f"{BASE_PACKAGE}.industrial.nmc",

    # --------------------------------------------------------
    # Lithium Sulfur
    # --------------------------------------------------------

    ("lithium_sulfur", "basic"):
        f"{BASE_PACKAGE}.basic.lithium_sulfur",

    ("lithium_sulfur", "advanced"):
        f"{BASE_PACKAGE}.advanced.lithium_sulfur",

    ("lithium_sulfur", "industrial"):
        f"{BASE_PACKAGE}.industrial.lithium_sulfur",

}


# ============================================================
# Helper Functions
# ============================================================

def is_supported_chemistry(name: str) -> bool:
    """
    Check whether a chemistry is supported.
    """
    return name.lower() in SUPPORTED_CHEMISTRIES


def is_supported_level(level: str) -> bool:
    """
    Check whether a simulation level is supported.
    """
    return level.lower() in SUPPORTED_LEVELS


def is_registered(
    chemistry: str,
    level: str,
) -> bool:
    """
    Check whether a chemistry/level combination
    exists in the registry.
    """

    key = (
        chemistry.lower(),
        level.lower(),
    )

    return key in PARAMETER_REGISTRY


def get_parameter_module(
    chemistry: str,
    level: str,
) -> str:
    """
    Return the Python module containing the requested
    parameter set.

    Example
    -------
    get_parameter_module(
        chemistry="lithium_metal",
        level="industrial",
    )
    """

    chemistry = chemistry.lower()
    level = level.lower()

    if not is_supported_chemistry(chemistry):
        raise ValueError(
            f"Unsupported chemistry: {chemistry}"
        )

    if not is_supported_level(level):
        raise ValueError(
            f"Unsupported level: {level}"
        )

    if not CHEMISTRIES[chemistry]["enabled"]:
        raise ValueError(
            f"{chemistry} is currently disabled."
        )

    key = (
        chemistry,
        level,
    )

    if key not in PARAMETER_REGISTRY:
        raise KeyError(
            f"No parameter module registered for {key}"
        )

    return PARAMETER_REGISTRY[key]


def list_supported_chemistries() -> list[str]:
    """
    Return a list of supported chemistries.
    """
    return list(SUPPORTED_CHEMISTRIES)


def list_supported_levels() -> list[str]:
    """
    Return a list of supported simulation levels.
    """
    return list(SUPPORTED_LEVELS)