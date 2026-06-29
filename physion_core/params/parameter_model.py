"""
parameter_model.py
==================

Abstract base class for all Physion parameter models.

Every chemistry parameter model must inherit from
ParameterModel.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ParameterModel(ABC):
    """
    Base class for every Physion parameter model.

    A parameter model is responsible for loading and
    returning a complete parameter dictionary for one
    chemistry and one simulation level.

    Parameters may originate from JSON files,
    Python objects, databases or any future source.
    """

    # ======================================================
    # Model information
    # ======================================================

    chemistry: str = ""

    level: str = ""

    version: str = "1.0.0"

    description: str = ""

    enabled: bool = True

    # JSON filename used by the loader
    json_file: str = ""

    # ======================================================
    # Required Interface
    # ======================================================

    @classmethod
    @abstractmethod
    def parameters(cls) -> dict[str, Any]:
        """
        Return the complete parameter dictionary.

        Child classes decide how the parameters are
        obtained (JSON, database, etc.).
        """
        raise NotImplementedError

    # ======================================================
    # Optional Interface
    # ======================================================

    @classmethod
    def resolve_references(
        cls,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Resolve function references if necessary.

        The default implementation simply returns
        the dictionary unchanged.

        loader.py may override or extend this step.
        """

        return parameters

    # ======================================================
    # Metadata
    # ======================================================

    @classmethod
    def metadata(cls) -> dict[str, Any]:

        return {

            "chemistry": cls.chemistry,

            "level": cls.level,

            "version": cls.version,

            "description": cls.description,

            "enabled": cls.enabled,

            "json_file": cls.json_file,

        }

    # ======================================================
    # Convenience Methods
    # ======================================================

    @classmethod
    def identifier(cls) -> str:
        """
        Unique identifier.

        Example
        -------
        lfp_basic
        """

        return f"{cls.chemistry}_{cls.level}"

    @classmethod
    def chemistry_name(cls) -> str:

        return cls.chemistry

    @classmethod
    def simulation_level(cls) -> str:

        return cls.level

    @classmethod
    def is_enabled(cls) -> bool:

        return cls.enabled

    @classmethod
    def json_filename(cls) -> str:

        return cls.json_file

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(chemistry='{self.chemistry}', "
            f"level='{self.level}')"
        )