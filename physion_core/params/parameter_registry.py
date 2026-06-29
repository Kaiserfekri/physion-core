"""
parameter_registry.py
=====================

Registry of all supported chemistries and simulation levels.

This module contains registry data only.
Parameter loading is handled by loader.py.
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