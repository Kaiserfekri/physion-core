"""
function_registry.py
====================

Central registry for all callable chemistry functions.

The loader never imports chemistry functions directly.
Instead, every callable is resolved through this registry.

This design keeps the loader independent from the
internal organization of the chemistry package.
"""

from __future__ import annotations

from typing import Callable

from physion_core.chemistry import functions


# ==========================================================
# Function Registry
# ==========================================================

FUNCTION_REGISTRY = {

    name: obj

    for name, obj in vars(functions).items()

    if callable(obj)

}


# ==========================================================
# Public API
# ==========================================================

def get_function(
    name: str,
) -> Callable:
    """
    Return a callable chemistry function.

    Parameters
    ----------
    name
        Function name stored inside JSON.

    Returns
    -------
    Callable
    """

    try:

        return FUNCTION_REGISTRY[name]

    except KeyError as exc:

        raise KeyError(

            f"Unknown chemistry function '{name}'."

        ) from exc


def has_function(
    name: str,
) -> bool:
    """
    Return True if a function exists.
    """

    return name in FUNCTION_REGISTRY


def list_functions() -> list[str]:
    """
    Return all registered function names.
    """

    return sorted(

        FUNCTION_REGISTRY.keys()

    )