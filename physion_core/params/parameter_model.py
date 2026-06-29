"""
parameter_model.py
==================

Base parameter model for Physion.

Every chemistry parameter model must inherit
from ParameterModel.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ParameterModel(ABC):
    """
    Abstract base class for all Physion
    parameter models.
    """

    chemistry: str = ""

    level: str = ""

    version: str = "1.0.0"

    description: str = ""

    enabled: bool = True

    @classmethod
    @abstractmethod
    def parameters(cls) -> dict[str, Any]:
        """
        Return the parameter dictionary.
        """
        raise NotImplementedError

    @classmethod
    def metadata(cls) -> dict[str, Any]:
        """
        Return metadata describing this
        parameter model.
        """

        return {
            "chemistry": cls.chemistry,
            "level": cls.level,
            "version": cls.version,
            "description": cls.description,
            "enabled": cls.enabled,
        }

    @classmethod
    def chemistry_name(cls) -> str:
        """
        Return chemistry name.
        """

        return cls.chemistry

    @classmethod
    def simulation_level(cls) -> str:
        """
        Return simulation level.
        """

        return cls.level

    @classmethod
    def identifier(cls) -> str:
        """
        Return a unique identifier.

        Example
        -------
        lfp_basic
        """

        return f"{cls.chemistry}_{cls.level}"

    @classmethod
    def is_enabled(cls) -> bool:
        """
        Return whether this parameter model
        is enabled.
        """

        return cls.enabled

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"chemistry='{self.chemistry}', "
            f"level='{self.level}')"
        )