"""
validators.py
==============

Validation utilities for Physion parameter sets.

This module validates:
    - Common parameters
    - Chemistry-specific parameters
    - Future industrial extensions
"""

from typing import Dict


class ParameterValidationError(ValueError):
    """Raised when a parameter set is invalid."""
    pass


# ============================================================
# Generic Validators
# ============================================================

def require_keys(params: Dict, required):
    """Ensure required keys exist."""

    missing = [k for k in required if k not in params]

    if missing:
        raise ParameterValidationError(
            f"Missing required parameters: {missing}"
        )


def positive(params: Dict, keys):
    """Ensure parameters are strictly positive."""

    for key in keys:

        if params[key] <= 0:
            raise ParameterValidationError(
                f"{key} must be > 0"
            )


def bounded(params: Dict, key, low, high):
    """Ensure parameter lies inside a range."""

    value = params[key]

    if not (low <= value <= high):

        raise ParameterValidationError(
            f"{key} must be between {low} and {high}"
        )


# ============================================================
# Common Validation
# ============================================================

def validate_common(params: Dict):
    """
    Validation required for every chemistry.
    """

    require_keys(
        params,
        [
            "temperature",
            "c_rate",
            "porosity",
        ],
    )

    positive(
        params,
        [
            "temperature",
            "c_rate",
        ],
    )

    bounded(
        params,
        "porosity",
        0.0,
        1.0,
    )


# ============================================================
# Chemistry Specific Validators
# ============================================================

def validate_lithium_metal(params: Dict):
    """
    Lithium Metal specific validation.
    """

    if "exchange_current_density" in params:

        positive(
            params,
            [
                "exchange_current_density",
            ],
        )


def validate_lfp(params: Dict):
    """
    LFP validation.
    """
    return


def validate_nmc(params: Dict):
    """
    NMC validation.
    """
    return


def validate_lithium_sulfur(params: Dict):
    """
    Lithium Sulfur validation.
    """
    return


# ============================================================
# Main Dispatcher
# ============================================================

def validate(
    chemistry: str,
    params: Dict,
):
    """
    Main validation entry point.

    Example
    -------
    validate(
        chemistry="lithium_metal",
        params=data,
    )
    """

    validate_common(params)

    chemistry = chemistry.lower()

    if chemistry == "lithium_metal":
        validate_lithium_metal(params)

    elif chemistry == "lfp":
        validate_lfp(params)

    elif chemistry == "nmc":
        validate_nmc(params)

    elif chemistry == "lithium_sulfur":
        validate_lithium_sulfur(params)

    else:
        raise ParameterValidationError(
            f"Unknown chemistry: {chemistry}"
        )

    return True