"""
Physion parameter datasets.

This package contains all JSON datasets used by
the Physion parameter loader.

Each JSON file represents one chemistry and one
simulation level.

Naming convention
-----------------
<chemistry>_<anode>_<level>.json

Examples
--------
lfp_graphite_simple.json
lfp_graphite_user.json
lfp_graphite_industrial.json
nmc_graphite_simple.json
"""

from pathlib import Path

DATASET_DIRECTORY = Path(__file__).parent

__all__ = [
    "DATASET_DIRECTORY",
]