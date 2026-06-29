"""
parameter_registry.py
=====================

Registry of all supported Physion chemistries and
simulation levels.

This module ONLY stores registry information.

No loading logic should exist here.
Loading, validation and JSON parsing are handled
by loader.py.
"""

# ==========================================================
# Supported Chemistries
# ==========================================================

CHEMISTRIES = {

    "lco_graphite": {
        "name": "LCO / Graphite",
        "enabled": True,
    },

    "lfp_graphite": {
        "name": "LFP / Graphite",
        "enabled": True,
    },

    "nmc_graphite": {
        "name": "NMC / Graphite",
        "enabled": True,
    },

    "nca_graphite": {
        "name": "NCA / Graphite",
        "enabled": True,
    },

}


# ==========================================================
# Supported Simulation Levels
# ==========================================================

LEVELS = {

    "basic": {

        "dataset_suffix": "simple",

        "priority": 1,

    },

    "advanced": {

        "dataset_suffix": "user",

        "priority": 2,

    },

    "industrial": {

        "dataset_suffix": "industrial",

        "priority": 3,

    },

}


# ==========================================================
# Convenience Constants
# ==========================================================

SUPPORTED_CHEMISTRIES = tuple(CHEMISTRIES.keys())

SUPPORTED_LEVELS = tuple(LEVELS.keys())