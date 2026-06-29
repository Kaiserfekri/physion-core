"""
validators.py
=============

Validation utilities for Physion parameter sets.

Responsibilities
----------------
- Validate common parameters
- Validate chemistry-specific parameters
- Provide a single validation entry point
"""

from __future__ import annotations

from typing import Any

# ==========================================================
# Exception
# ==========================================================

class ParameterValidationError(ValueError):
    """
    Raised when a parameter set is invalid.
    """
    pass


# ==========================================================
# Generic Validators
# ==========================================================

def require_keys(
    params: dict[str, Any],
    required: list[str],
) -> None:
    """
    Ensure required keys exist.
    """

    missing = [
        key
        for key in required
        if key not in params
    ]

    if missing:
        raise ParameterValidationError(
            f"Missing required parameters: {missing}"
        )


def positive(
    params: dict[str, Any],
    keys: list[str],
) -> None:
    """
    Ensure parameters are strictly positive.
    """

    for key in keys:

        if key not in params:
            continue

        if params[key] <= 0:

            raise ParameterValidationError(
                f"{key} must be > 0"
            )


def bounded(
    params: dict[str, Any],
    key: str,
    low: float,
    high: float,
) -> None:
    """
    Ensure parameter lies inside a range.
    """

    if key not in params:
        return

    value = params[key]

    if not (low <= value <= high):

        raise ParameterValidationError(
            f"{key} must be between {low} and {high}"
        )


# ==========================================================
# Common Validation
# ==========================================================

def validate_common(
    params: dict[str, Any],
) -> None:
    """
    Validation required for every chemistry.
    """

    require_keys(
        params,
        [
            "capacity_anode",
            "capacity_cathode",
            "electrolyte",
            "mechanical",
            "degradation",
        ],
    )

    positive(
        params,
        [
            "capacity_anode",
            "capacity_cathode",
        ],
    )


# ==========================================================
# Chemistry Specific Validators
# ==========================================================

def validate_lco_graphite(
    params: dict[str, Any],
) -> None:
    """
    Validation for LCO / Graphite.
    """
    return


def validate_lfp_graphite(
    params: dict[str, Any],
) -> None:
    """
    Validation for LFP / Graphite.
    """
    return


def validate_nmc_graphite(
    params: dict[str, Any],
) -> None:
    """
    Validation for NMC / Graphite.
    """
    return


def validate_nca_graphite(
    params: dict[str, Any],
) -> None:
    """
    Validation for NCA / Graphite.
    """
    return


# ==========================================================
# Validation Registry
# ==========================================================

CHEMISTRY_VALIDATORS = {

    "lco_graphite":
        validate_lco_graphite,

    "lfp_graphite":
        validate_lfp_graphite,

    "nmc_graphite":
        validate_nmc_graphite,

    "nca_graphite":
        validate_nca_graphite,

}


# ==========================================================
# Public Entry Point
# ==========================================================

def validate(
    chemistry: str,
    params: dict[str, Any],
) -> bool:
    """
    Validate a parameter set.

    Parameters
    ----------
    chemistry
        Chemistry name.

    params
        Parameter dictionary.
    """

    chemistry = chemistry.lower()

    validate_common(params)

    validator = CHEMISTRY_VALIDATORS.get(chemistry)

    if validator is None:

        raise ParameterValidationError(
            f"Unsupported chemistry: {chemistry}"
        )

    validator(params)

    return True