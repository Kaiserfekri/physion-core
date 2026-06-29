"""
loader.py
=========

Physion Parameter Loader

Responsibilities
----------------
- Locate the correct dataset
- Load JSON parameter files
- Resolve function references
- Validate parameter sets
- Return simulation-ready dictionaries

This module is the only entry point for loading
parameter datasets.
"""

from __future__ import annotations

import copy
import importlib
import json
from pathlib import Path
from typing import Any

from physion_core.chemistry import functions

from .parameter_registry import (
    CHEMISTRIES,
    LEVELS,
)

from .validators import validate


# ==========================================================
# Paths
# ==========================================================

PACKAGE_DIR = Path(__file__).resolve().parent

DATASET_DIR = PACKAGE_DIR / "datasets"
# ==========================================================
# Registry Utilities
# ==========================================================

def _normalize_name(value: str) -> str:
    """
    Normalize chemistry and level names.
    """

    return value.strip().lower()


def _validate_chemistry(
    chemistry: str,
) -> str:
    """
    Validate chemistry name.
    """

    chemistry = _normalize_name(chemistry)

    if chemistry not in CHEMISTRIES:

        raise ValueError(
            f"Unsupported chemistry: '{chemistry}'"
        )

    if not CHEMISTRIES[chemistry]["enabled"]:

        raise ValueError(
            f"Chemistry '{chemistry}' is disabled."
        )

    return chemistry


def _validate_level(
    level: str,
) -> str:
    """
    Validate simulation level.
    """

    level = _normalize_name(level)

    if level not in LEVELS:

        raise ValueError(
            f"Unsupported level: '{level}'"
        )

    return level


def _dataset_filename(
    chemistry: str,
    level: str,
) -> str:
    """
    Return dataset filename.

    Example
    -------
    chemistry = "lfp_graphite"
    level = "advanced"

    -> lfp_graphite_user.json
    """

    chemistry = _validate_chemistry(chemistry)

    level = _validate_level(level)

    suffix = LEVELS[level]["dataset_suffix"]

    return f"{chemistry}_{suffix}.json"


def _dataset_path(
    chemistry: str,
    level: str,
) -> Path:
    """
    Return absolute dataset path.
    """

    filename = _dataset_filename(
        chemistry,
        level,
    )

    path = DATASET_DIR / filename

    if not path.exists():

        raise FileNotFoundError(
            f"Dataset not found:\n{path}"
        )

    return path
    # ==========================================================
# JSON Loader
# ==========================================================

def _read_json(
    path: Path,
) -> dict[str, Any]:
    """
    Read a JSON parameter dataset.

    Parameters
    ----------
    path
        Absolute path to the dataset.

    Returns
    -------
    dict
        Parameter dictionary.
    """

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    return copy.deepcopy(data)


def _load_dataset(
    chemistry: str,
    level: str,
) -> dict[str, Any]:
    """
    Load a dataset from disk.

    This function performs no function
    resolution and no validation.
    """

    dataset_path = _dataset_path(
        chemistry,
        level,
    )

    parameters = _read_json(
        dataset_path,
    )

    return parameters
    # ==========================================================
# Function Resolver
# ==========================================================

# Keys that should be resolved into callable objects.
FUNCTION_KEYS = {

    "U_anode",

    "U_cathode",

    "dU_anode_dT",

    "dU_cathode_dT",

    "D_anode",

    "D_cathode",

}


def _resolve_function(
    function_name: str,
):
    """
    Resolve a function name stored inside the JSON
    dataset into a Python callable.

    Example
    -------
    "U_anode_graphite"

        ↓

    functions.U_anode_graphite
    """

    try:

        return getattr(
            functions,
            function_name,
        )

    except AttributeError as exc:

        raise AttributeError(
            f"Unknown chemistry function: "
            f"'{function_name}'"
        ) from exc


def _resolve_functions(
    parameters: dict[str, Any],
) -> dict[str, Any]:
    """
    Replace function names with callable objects.

    Only keys listed in FUNCTION_KEYS are resolved.
    """

    resolved = copy.deepcopy(parameters)

    for key in FUNCTION_KEYS:

        if key not in resolved:
            continue

        value = resolved[key]

        if not isinstance(value, str):
            continue

        resolved[key] = _resolve_function(value)

    return resolved
    # ==========================================================
# Validation
# ==========================================================

def _validate_dataset(
    chemistry: str,
    parameters: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate a parameter dataset.

    Parameters
    ----------
    chemistry
        Chemistry name.

    parameters
        Parameter dictionary.

    Returns
    -------
    dict
        Validated parameter dictionary.
    """

    validate(
        chemistry=chemistry,
        params=parameters,
    )

    return parameters
    # ==========================================================
# Public API
# ==========================================================

def load(
    chemistry: str,
    level: str,
) -> dict[str, Any]:
    """
    Load a complete Physion parameter set.

    Workflow
    --------
    1. Locate dataset
    2. Read JSON
    3. Resolve function references
    4. Validate
    5. Return simulation-ready parameters
    """

    parameters = _load_dataset(
        chemistry,
        level,
    )

    parameters = _resolve_functions(
        parameters,
    )

    parameters = _validate_dataset(
        chemistry,
        parameters,
    )

    return parameters
    def available_chemistries() -> list[str]:
    """
    Return supported chemistries.
    """

    return sorted(
        CHEMISTRIES.keys(),
    )


def available_levels() -> list[str]:
    """
    Return supported simulation levels.
    """

    return sorted(
        LEVELS.keys(),
    )