"""
base_update.py
==============

Industrial Base Update Object for Physion Framework.

Purpose
-------
Defines the immutable contract shared by every
Physion Update Object.

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
• NO solver logic
• NO commit logic
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from datetime import datetime
from math import isfinite
from typing import ClassVar

import uuid


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BaseUpdate(ABC):
    """
    Base class for every Physion Update Object.
    """

    # =====================================================
    # Framework
    # =====================================================

    VERSION: ClassVar[str] = "2.0.0"

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
        Perform generic validation shared by
        every Update Object.

        Checks
        ------
        • every floating-point value is finite.
        """

        for item in fields(self):

            value = getattr(self, item.name)

            if isinstance(value, float):

                if not isfinite(value):

                    return False

        return True

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