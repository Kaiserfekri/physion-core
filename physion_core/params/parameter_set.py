"""
parameter_set.py
================

High-level parameter container for Physion.

ParameterSet is the public interface used by every
simulation module to access chemistry parameters.

Parameter loading is delegated to loader.py.
"""

from __future__ import annotations

from typing import Any
from collections.abc import Iterator

from physion_core.params.loader import load_parameters


class ParameterSet:
    """
    High-level parameter container.

    Examples
    --------
    >>> params = ParameterSet(
    ...     chemistry="nmc_graphite",
    ...     level="industrial",
    ... )

    >>> params["capacity_anode"]

    >>> params.capacity_anode

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

        self._chemistry = chemistry

        self._level = level

        self._parameters = load(

            chemistry=chemistry,

            level=level,

        )

    # ======================================================
    # Properties
    # ======================================================

    @property
    def chemistry(self) -> str:

        return self._chemistry

    @property
    def level(self) -> str:

        return self._level

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
    # Attribute Interface
    # ======================================================

    def __getattr__(
        self,
        name: str,
    ) -> Any:
        """
        Allow attribute-style access.

        Example
        -------
        params.capacity_anode
        """

        try:

            return self._parameters[name]

        except KeyError as exc:

            raise AttributeError(

                f"No parameter named '{name}'."

            ) from exc

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

    def keys(self):

        return self._parameters.keys()

    def values(self):

        return self._parameters.values()

    def items(self):

        return self._parameters.items()

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Return a copy of the parameter dictionary.
        """

        return dict(self._parameters)

    # ======================================================
    # Metadata
    # ======================================================

    def metadata(
        self,
    ) -> dict[str, str]:
        """
        Return ParameterSet metadata.
        """

        return {

            "chemistry": self._chemistry,

            "level": self._level,

        }

    # ======================================================
    # Utilities
    # ======================================================

    def copy(
        self,
    ) -> "ParameterSet":
        """
        Return a new ParameterSet using the same
        chemistry and simulation level.
        """

        return ParameterSet(

            chemistry=self._chemistry,

            level=self._level,

        )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"chemistry='{self._chemistry}', "

            f"level='{self._level}', "

            f"parameters={len(self._parameters)})"

        )