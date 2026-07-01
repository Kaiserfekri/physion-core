"""
base_update.py
==============

Industrial Base Update Object for Physion Framework.

Purpose
-------
Defines the immutable contract for every Physion
Update Object.

Architecture
------------
Solver
    ↓
Update Object
    ↓
Commit Manager
    ↓
State

Responsibilities
----------------
• Immutable update container
• Metadata
• Generic validation
• Lightweight diagnostics

Contains
--------
• NO physics
• NO numerical methods
• NO state ownership
• NO commit logic
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from math import isfinite
import uuid


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseUpdate(ABC):
    """
    Base class for every Physion Update Object.
    """

    # =====================================================
    # Framework
    # =====================================================

    VERSION: str = "2.0.0"

    # =====================================================
    # Metadata
    # =====================================================

    update_id: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        init=False,
        repr=False,
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow,
        init=False,
        repr=False,
    )

    valid: bool = True

    # =====================================================
    # Information
    # =====================================================

    @property
    def class_name(self) -> str:

        return self.__class__.__name__

    # =====================================================
    # Generic Validation
    # =====================================================

    def validate(self) -> bool:
        """
        Generic validation shared by every Update.

        Checks

        • finite floating values

        Child classes may extend this method.
        """

        for value in self.__dict__.values():

            if isinstance(value, float):

                if not isfinite(value):

                    return False

        return self.valid

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:

        return (

            f"{self.class_name}"

            "("

            f"id={self.update_id[:8]}"

            ")"

        )