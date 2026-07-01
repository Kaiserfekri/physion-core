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
• Atomic update
• Atomic reset
• Validation hooks

Contains NO battery physics.
"""

# ==========================================================
# STATUS
#
# Physion Core Frozen Module
#
# Version : 2.1
# Status  : Frozen
#
# ==========================================================

from __future__ import annotations

import copy
import uuid

from datetime import datetime

from dataclasses import (
    MISSING,
    dataclass,
    field,
    fields,
)

from typing import (
    Any,
    ClassVar,
)

from physion_core.state.state_mixin import StateMixin


@dataclass(slots=True, kw_only=True)
class BaseState(StateMixin):
    """
    Industrial base class for every Physion State.

    Responsibilities
    ----------------
    • Identity
    • Locking
    • Atomic update
    • Atomic reset
    • Validation lifecycle

    Contains
    --------
    • NO battery physics
    • NO numerical methods
    """

    # =====================================================
    # Framework
    # =====================================================

    VERSION: ClassVar[str] = "2.1.0"

    # =====================================================
    # Metadata
    # =====================================================

    state_id: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        init=False,
        repr=False,
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow,
        init=False,
        repr=False,
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow,
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
        """
        Initialize timestamps.
        """
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
        """
        Lock state against modification.
        """
        self._locked = True

    def unlock(self) -> None:
        """
        Unlock state.
        """
        self._locked = False

    @property
    def is_locked(self) -> bool:
        """
        Lock status.
        """
        return self._locked

    # =====================================================
    # Update Hooks
    # =====================================================

    def before_update(self) -> None:
        """
        Override when needed.
        """
        return

    def after_update(self) -> None:
        """
        Override when needed.
        """
        return

    # =====================================================
    # Validation Hooks
    # =====================================================

    def before_validate(self) -> None:
        """
        Override when needed.
        """
        return

    def validate_impl(self) -> None:
        """
        Override in derived State classes.
        """
        return

    def after_validate(self) -> None:
        """
        Override when needed.
        """
        return
            # =====================================================
    # Atomic Update
    # =====================================================

    def update(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Atomically update state.

        The update is committed only if validation succeeds.
        """

        if self._locked:
            raise RuntimeError(
                f"{self.class_name} is locked."
            )

        self.before_update()

        valid_fields = {
            f.name
            for f in fields(self)
            if f.init and not f.name.startswith("_")
        }

        unknown = set(kwargs) - valid_fields

        if unknown:
            raise AttributeError(
                f"Unknown field(s): {', '.join(sorted(unknown))}"
            )

        # ---------------------------------------------
        # Transaction Snapshot
        # ---------------------------------------------

        snapshot = {
            name: copy.deepcopy(
                getattr(self, name)
            )
            for name in valid_fields
        }

        try:

            # -----------------------------------------
            # Apply New Values
            # -----------------------------------------

            for key, value in kwargs.items():

                setattr(
                    self,
                    key,
                    value,
                )

            # -----------------------------------------
            # Validate New State
            # -----------------------------------------

            self.validate()

        except Exception:

            # -----------------------------------------
            # Rollback
            # -----------------------------------------

            for key, value in snapshot.items():

                setattr(
                    self,
                    key,
                    value,
                )

            raise

        # ---------------------------------------------
        # Commit
        # ---------------------------------------------

        self.touch()

        self.after_update()
            # =====================================================
    # Atomic Reset
    # =====================================================

    def reset(self) -> None:
        """
        Atomically restore all public fields to their
        declared default values.
        """

        if self._locked:
            raise RuntimeError(
                f"{self.class_name} is locked."
            )

        valid_fields = [
            f
            for f in fields(self)
            if f.init and not f.name.startswith("_")
        ]

        # ---------------------------------------------
        # Transaction Snapshot
        # ---------------------------------------------

        snapshot = {
            f.name: copy.deepcopy(
                getattr(self, f.name)
            )
            for f in valid_fields
        }

        try:

            # -----------------------------------------
            # Apply Defaults
            # -----------------------------------------

            for f in valid_fields:

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

            # -----------------------------------------
            # Validate
            # -----------------------------------------

            self.validate()

        except Exception:

            # -----------------------------------------
            # Rollback
            # -----------------------------------------

            for key, value in snapshot.items():

                setattr(
                    self,
                    key,
                    value,
                )

            raise

        # ---------------------------------------------
        # Commit
        # ---------------------------------------------

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

    # =====================================================
    # Information
    # =====================================================

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def age_seconds(self) -> float:
        return (
            self.updated_at -
            self.created_at
        ).total_seconds()

    # =====================================================
    # Equality / Hash
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
            self.state_id ==
            other.state_id
        )

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
        