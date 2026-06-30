"""
base_state.py
=============

Industrial BaseState for Physion.

BaseState extends StateMixin with simulation-state
management capabilities.

Responsibilities
----------------
• State identity
• State lifecycle
• Lock management
• Update
• Validation hooks

Contains NO battery physics.
"""

# ==========================================================
# STATUS
#
# Physion Core Frozen Module
#
# Version : 1.0
# Status  : Frozen
#
# This file is part of the stable Physion Core.
# Modify only for bug fixes or architecture changes.
# ==========================================================

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
    fields,
    MISSING,
)

from datetime import datetime

from typing import Any

import copy
import uuid

from physion_core.state.state_mixin import StateMixin


@dataclass(slots=True, kw_only=True)
class BaseState(StateMixin):
    """
    Base class for every Physion simulation state.
    """

    # =====================================================
    # Framework Version
    # =====================================================

    VERSION: str = "2.0.0"

    # =====================================================
    # Internal Metadata
    # =====================================================

    state_id: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        init=False,
        repr=False,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.utcnow(),
        init=False,
        repr=False,
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.utcnow(),
        init=False,
        repr=False,
    )

    _locked: bool = field(
        default=False,
        init=False,
        repr=False,
    )

    # =====================================================
    # Construction
    # =====================================================

    def __post_init__(self) -> None:

        self.touch()

    # =====================================================
    # Timestamp
    # =====================================================

    def touch(self) -> None:
        """
        Update modification timestamp.
        """

        self.updated_at = datetime.utcnow()

    # =====================================================
    # Lock Management
    # =====================================================

    def lock(self) -> None:

        self._locked = True

    def unlock(self) -> None:

        self._locked = False

    @property
    def is_locked(self) -> bool:

        return self._locked

    # =====================================================
    # Hooks
    # =====================================================

    def before_update(self) -> None:
        """
        Override in child classes.
        """
        return

    def after_update(self) -> None:
        """
        Override in child classes.
        """
        return

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        **kwargs: Any,
    ) -> None:

        if self._locked:

            raise RuntimeError(

                f"{self.__class__.__name__} is locked."

            )

        self.before_update()

        valid_fields = {

            f.name

            for f in fields(self)

            if f.init

            and not f.name.startswith("_")

        }

        for key, value in kwargs.items():

            if key not in valid_fields:

                raise AttributeError(

                    f"Unknown field '{key}'."

                )

            setattr(

                self,

                key,

                value,

            )

        self.touch()

        self.after_update()
        
    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:
        """
        Restore all public dataclass fields to their
        declared default values.
        """

        if self._locked:

            raise RuntimeError(

                f"{self.__class__.__name__} is locked."

            )

        for f in fields(self):

            if f.name.startswith("_"):

                continue

            if not f.init:

                continue

            if f.default is not MISSING:

                value = copy.deepcopy(

                    f.default

                )

            elif f.default_factory is not MISSING:

                value = f.default_factory()

            else:

                raise RuntimeError(

                    f"Field '{f.name}' has no default value."
                                                                                                                
                )
            setattr(

                self,

                f.name,

                value,

            )

        self.touch()

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> None:
        """
        Validate current state.
        """

        self.before_validate()

        self.validate_impl()

        self.after_validate()

    # -----------------------------------------------------

    def before_validate(self) -> None:
        """
        Validation hook.
        """

        return

    # -----------------------------------------------------

    def validate_impl(self) -> None:
        """
        Override in child classes.
        """

        return

    # -----------------------------------------------------

    def after_validate(self) -> None:
        """
        Validation hook.
        """

        return
        
    # =====================================================
    # State Information
    # =====================================================

    @property
    def class_name(self) -> str:
        """
        Return state class name.
        """

        return self.__class__.__name__

    # -----------------------------------------------------

    @property
    def age_seconds(self) -> float:
        """
        Seconds since creation.
        """

        return (

            self.updated_at

            -

            self.created_at

        ).total_seconds()

    # =====================================================
    # Equality
    # =====================================================

    def __eq__(
        self,
        other: object,
    ) -> bool:

        if not isinstance(

            other,

            self.__class__,

        ):

            return False

        return (

            self.state_id

            ==

            other.state_id

        )

    # =====================================================
    # Hash
    # =====================================================

    def __hash__(self) -> int:

        return hash(

            self.state_id

        )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:

        return (

            f"{self.class_name}"

            "("

            f"id={self.state_id[:8]}, "

            f"locked={self.is_locked}"

            ")"

        )

    # =====================================================
    # Debug
    # =====================================================

    def summary(self) -> dict[str, Any]:
        """
        Lightweight state summary.
        """

        return {

            "class": self.class_name,

            "state_id": self.state_id,

            "locked": self.is_locked,

            "created_at": self.created_at,

            "updated_at": self.updated_at,

        }