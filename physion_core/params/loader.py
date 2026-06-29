"""
loader.py
=========

Central parameter loader for Physion.

Responsibilities
----------------
- Locate parameter datasets
- Read JSON datasets
- Resolve callable chemistry functions
- Validate datasets
- Attach metadata
- Attach enabled features
- Cache loaded parameter sets

This is the ONLY module allowed to load parameter
datasets from disk.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from physion_core.chemistry import functions

from physion_core.params.defaults import (
    DEFAULT_CHEMISTRY,
    DEFAULT_LEVEL,
)

from physion_core.params.features import (
    BASIC,
    ADVANCED,
    INDUSTRIAL,
)

from physion_core.params.metadata import (
    build_metadata,
)

from physion_core.params.parameter_registry import (
    CHEMISTRIES,
    LEVELS,
)

from physion_core.params.validators import (
    validate,
)

# ==========================================================
# Dataset location
# ==========================================================

_DATASET_DIRECTORY = (
    Path(__file__).parent / "datasets"
)

# ==========================================================
# Internal cache
# ==========================================================

_CACHE: dict[
    tuple[str, str],
    dict[str, Any],
] = {}

# ==========================================================
# Feature map
# ==========================================================

_FEATURES = {

    "basic": BASIC,

    "advanced": ADVANCED,

    "industrial": INDUSTRIAL,

}
# ==========================================================
# Dataset filename
# ==========================================================

def _dataset_filename(
    chemistry: str,
    level: str,
) -> str:
    """
    Build dataset filename.

    Example
    -------
    nmc_graphite
    industrial

    ->
    nmc_graphite_industrial.json
    """

    suffix = LEVELS[level]["dataset_suffix"]

    return f"{chemistry}_{suffix}.json"


# ==========================================================
# Dataset path
# ==========================================================

def _dataset_path(
    chemistry: str,
    level: str,
) -> Path:
    """
    Return full dataset path.
    """

    return (
        _DATASET_DIRECTORY
        / _dataset_filename(
            chemistry,
            level,
        )
    )


# ==========================================================
# Read JSON
# ==========================================================

def _read_json(
    path: Path,
) -> dict[str, Any]:
    """
    Read a JSON parameter file.
    """

    if not path.exists():

        raise FileNotFoundError(

            f"Dataset not found:\n{path}"

        )

    with open(

        path,

        "r",

        encoding="utf-8",

    ) as file:

        return json.load(file)
        # ==========================================================
# Resolve chemistry functions
# ==========================================================

def _resolve_functions(
    params: dict[str, Any],
) -> dict[str, Any]:
    """
    Replace function names stored inside the JSON
    dataset with real callable Python objects.
    """

    resolved = copy.deepcopy(params)

    def walk(obj):

        if isinstance(obj, dict):

            for key, value in obj.items():

                if isinstance(value, str):

                    if hasattr(functions, value):

                        obj[key] = getattr(
                            functions,
                            value,
                        )

                else:

                    walk(value)

        elif isinstance(obj, list):

            for item in obj:

                walk(item)

    walk(resolved)

    return resolved


# ==========================================================
# Attach enabled features
# ==========================================================

def _attach_features(
    params: dict[str, Any],
    level: str,
) -> None:
    """
    Attach enabled feature flags.
    """

    params["features"] = copy.deepcopy(

        _FEATURES[level]

    )


# ==========================================================
# Attach metadata
# ==========================================================

def _attach_metadata(
    params: dict[str, Any],
    chemistry: str,
    level: str,
) -> None:
    """
    Attach metadata object.
    """

    params["metadata"] = build_metadata(

        chemistry=chemistry,

        level=level,

        description=CHEMISTRIES[
            chemistry
        ]["name"],

    )


# ==========================================================
# Validate parameter set
# ==========================================================

def _validate(
    chemistry: str,
    params: dict[str, Any],
) -> None:
    """
    Validate parameter dictionary.
    """

    validate(

        chemistry,

        params,

    )
    # ==========================================================
# Public API
# ==========================================================

def load_parameters(
    chemistry: str | None = None,
    level: str | None = None,
) -> dict[str, Any]:
    """
    Load a Physion parameter set.

    Parameters
    ----------
    chemistry
        Chemistry name.

    level
        Simulation level.

    Returns
    -------
    dict
        Fully resolved parameter dictionary.
    """

    chemistry = chemistry or DEFAULT_CHEMISTRY
    level = level or DEFAULT_LEVEL

    chemistry = chemistry.lower()
    level = level.lower()

    if chemistry not in CHEMISTRIES:

        raise ValueError(

            f"Unsupported chemistry: {chemistry}"

        )

    if level not in LEVELS:

        raise ValueError(

            f"Unsupported level: {level}"

        )

    cache_key = (

        chemistry,

        level,

    )

    if cache_key in _CACHE:

        return copy.deepcopy(

            _CACHE[cache_key]

        )

    dataset = _read_json(

        _dataset_path(

            chemistry,

            level,

        )

    )

    dataset = _resolve_functions(

        dataset

    )

    _attach_features(

        dataset,

        level,

    )

    _attach_metadata(

        dataset,

        chemistry,

        level,

    )

    _validate(

        chemistry,

        dataset,

    )

    _CACHE[cache_key] = copy.deepcopy(

        dataset

    )

    return copy.deepcopy(

        dataset

    )


# ==========================================================
# Cache utilities
# ==========================================================

def clear_cache() -> None:
    """
    Clear parameter cache.
    """

    _CACHE.clear()


def cache_size() -> int:
    """
    Return number of cached parameter sets.
    """

    return len(_CACHE)


def available_chemistries() -> list[str]:
    """
    Return supported chemistries.
    """

    return sorted(

        CHEMISTRIES.keys()

    )


def available_levels() -> list[str]:
    """
    Return supported simulation levels.
    """

    return sorted(

        LEVELS.keys()

    )
    # ==========================================================
# Backward compatible public API
# ==========================================================

def load(
    chemistry: str | None = None,
    level: str | None = None,
) -> dict[str, Any]:
    """
    Main public loader API.
    """

    return load_parameters(
        chemistry=chemistry,
        level=level,
    )