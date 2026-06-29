"""
validators.py
=============

Validation utilities for Physion parameter sets.
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

    if key not in params:

        return

    value = params[key]

    if not (low <= value <= high):

        raise ParameterValidationError(

            f"{key} must be between {low} and {high}"

        )


# ==========================================================
# Protocol Validation
# ==========================================================

def validate_protocol(
    protocol: dict[str, Any],
) -> None:

    require_keys(

        protocol,

        [

            "type",

            "V_charge",

            "V_discharge",

            "I_1C",

            "C_rate",

            "V_cv_cutoff",

            "I_cv_cutoff",

            "n_cycles",

            "t_half_cycle",

            "Q_initial",

            "capacity_cutoff",

        ],

    )

    positive(

        protocol,

        [

            "V_charge",

            "V_discharge",

            "I_1C",

            "C_rate",

            "n_cycles",

            "t_half_cycle",

            "Q_initial",

        ],

    )

    bounded(

        protocol,

        "capacity_cutoff",

        0.0,

        1.0,

    )


# ==========================================================
# Common Validation
# ==========================================================

def validate_common(
    params: dict[str, Any],
) -> None:

    require_keys(

        params,

        [

            "capacity_anode",

            "capacity_cathode",

            "electrolyte",

            "mechanical",

            "degradation",

            "protocol",

        ],

    )

    positive(

        params,

        [

            "capacity_anode",

            "capacity_cathode",

        ],

    )

    validate_protocol(

        params["protocol"]

    )


# ==========================================================
# Chemistry Validators
# ==========================================================

def validate_lco_graphite(
    params: dict[str, Any],
) -> None:
    return


def validate_lfp_graphite(
    params: dict[str, Any],
) -> None:
    return


def validate_nmc_graphite(
    params: dict[str, Any],
) -> None:
    return


def validate_nca_graphite(
    params: dict[str, Any],
) -> None:
    return


# ==========================================================
# Registry
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
# Public API
# ==========================================================

def validate(
    chemistry: str,
    params: dict[str, Any],
) -> bool:

    chemistry = chemistry.lower()

    validate_common(

        params,

    )

    validator = CHEMISTRY_VALIDATORS.get(

        chemistry,

    )

    if validator is None:

        raise ParameterValidationError(

            f"Unsupported chemistry: {chemistry}"

        )

    validator(

        params,

    )

    return True