"""
parameter_registry.py
=====================

Registry of all supported chemistries and simulation levels.

This module only defines where parameter sets are located.
Loading is handled by loader.py.
"""

# ============================================================
# Supported simulation levels
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
# Supported chemistries
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
# Parameter file registry
# ============================================================

PARAMETER_REGISTRY = {

    # Lithium Metal
    ("lithium_metal", "basic"):
        "physion_core.params.basic.lithium_metal",

    ("lithium_metal", "advanced"):
        "physion_core.params.advanced.lithium_metal",

    ("lithium_metal", "industrial"):
        "physion_core.params.industrial.lithium_metal",

    # LFP
    ("lfp", "basic"):
        "physion_core.params.basic.lfp",

    ("lfp", "advanced"):
        "physion_core.params.advanced.lfp",

    ("lfp", "industrial"):
        "physion_core.params.industrial.lfp",

    # NMC
    ("nmc", "basic"):
        "physion_core.params.basic.nmc",

    ("nmc", "advanced"):
        "physion_core.params.advanced.nmc",

    ("nmc", "industrial"):
        "physion_core.params.industrial.nmc",

    # Lithium Sulfur
    ("lithium_sulfur", "basic"):
        "physion_core.params.basic.lithium_sulfur",

    ("lithium_sulfur", "advanced"):
        "physion_core.params.advanced.lithium_sulfur",

    ("lithium_sulfur", "industrial"):
        "physion_core.params.industrial.lithium_sulfur",
}