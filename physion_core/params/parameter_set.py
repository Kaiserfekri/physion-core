"""
parameter_set.py
================

High-level parameter container used throughout Physion.

ParameterSet is the public API for accessing simulation
parameters.

All parameter loading is delegated to loader.py.
"""

from __future__ import annotations

from typing import Any
from collections.abc import Iterator

from physion_core.params.loader import load


class ParameterSet:
    """
    High-level container for simulation parameters.

    Examples
    --------
    >>> params = ParameterSet(
    ...     chemistry="nmc_graphite",
    ...     level="industrial",
    ... )

    >>> params["capacity_anode"]

    >>> params.get("electrolyte")

    >>> params.metadata()

    >>> "capacity_anode" in params
    """

    # ======================================================
    # Construction
    # ======================================================

    def __init__(
        self,
        chemistry: str,
        level: str,
    ) -> None:

        self.chemistry = chemistry

        self.level = level

        self._parameters = load(
            chemistry=chemistry,
            level=level,
        )

    # ======================================================
    # Dictionary Interface
    # ======================================================

    def __getitem__(
        self,
        key: str,
    ) -> Any:

        return self._parameters[key]

    def __contains__(
        self,
        key: str,
    ) -> bool:

        return key in self._parameters

    def __len__(
        self,
    ) -> int:

        return len(self._parameters)

    def __iter__(
        self,
    ) -> Iterator[str]:

        return iter(self._parameters)

    # ======================================================
    # Convenience Methods
    # ======================================================

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self._parameters.get(
            key,
            default,
        )

    def keys(
        self,
    ):

        return self._parameters.keys()

    def values(
        self,
    ):

        return self._parameters.values()

    def items(
        self,
    ):

        return self._parameters.items()

    # ======================================================
    # Metadata
    # ======================================================

    def metadata(
        self,
    ) -> dict[str, str]:

        return {

            "chemistry": self.chemistry,

            "level": self.level,

        }

    # ======================================================
    # Export
    # ======================================================

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return dict(self._parameters)

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(
        self,
    ) -> str:

        return (

            f"ParameterSet("

            f"chemistry='{self.chemistry}', "

            f"level='{self.level}', "

            f"parameters={len(self._parameters)})"

        )