"""
cell_enums.py
=============

Industrial Cell Enumerations
for Physion Framework.

Purpose
-------
Defines every enumeration describing
cell identity, chemistry, operating mode
and lifecycle.

Notes
-----
Contains NO physics.

Contains NO solver logic.

Contains NO state.

Used throughout the framework.
"""

from __future__ import annotations

from enum import Enum


# ==========================================================
# Cell Format
# ==========================================================

class CellFormat(str, Enum):

    CYLINDRICAL = "CYLINDRICAL"

    PRISMATIC = "PRISMATIC"

    POUCH = "POUCH"

    COIN = "COIN"

    BUTTON = "BUTTON"

    CUSTOM = "CUSTOM"


# ==========================================================
# Chemistry
# ==========================================================

class CellChemistry(str, Enum):

    LFP = "LFP"

    NMC = "NMC"

    NCA = "NCA"

    LCO = "LCO"

    LMO = "LMO"

    LTO = "LTO"

    LMFP = "LMFP"

    SODIUM_ION = "SODIUM_ION"

    LITHIUM_SULFUR = "LITHIUM_SULFUR"

    SOLID_STATE = "SOLID_STATE"

    CUSTOM = "CUSTOM"
    
# ==========================================================
# Operating Mode
# ==========================================================

class CellOperatingMode(str, Enum):

    # ----------------------------------------------
    # General
    # ----------------------------------------------

    INITIALIZATION = "INITIALIZATION"

    IDLE = "IDLE"

    REST = "REST"

    STANDBY = "STANDBY"

    # ----------------------------------------------
    # Charging
    # ----------------------------------------------

    PRECHARGE = "PRECHARGE"

    CC_CHARGE = "CC_CHARGE"

    CV_CHARGE = "CV_CHARGE"

    CCCV_CHARGE = "CCCV_CHARGE"

    TRICKLE_CHARGE = "TRICKLE_CHARGE"

    PULSE_CHARGE = "PULSE_CHARGE"

    FAST_CHARGE = "FAST_CHARGE"

    # ----------------------------------------------
    # Discharging
    # ----------------------------------------------

    DISCHARGE = "DISCHARGE"

    CONSTANT_POWER_DISCHARGE = (
        "CONSTANT_POWER_DISCHARGE"
    )

    CONSTANT_RESISTANCE_DISCHARGE = (
        "CONSTANT_RESISTANCE_DISCHARGE"
    )

    PULSE_DISCHARGE = "PULSE_DISCHARGE"

    REGENERATIVE_DISCHARGE = (
        "REGENERATIVE_DISCHARGE"
    )

    # ----------------------------------------------
    # Balancing
    # ----------------------------------------------

    PASSIVE_BALANCING = "PASSIVE_BALANCING"

    ACTIVE_BALANCING = "ACTIVE_BALANCING"

    # ----------------------------------------------
    # Laboratory Tests
    # ----------------------------------------------

    FORMATION = "FORMATION"

    HPPC = "HPPC"

    EIS = "EIS"

    GITT = "GITT"

    PITT = "PITT"

    RATE_CAPABILITY = "RATE_CAPABILITY"

    CALENDAR_AGING = "CALENDAR_AGING"

    CYCLE_AGING = "CYCLE_AGING"

    STORAGE = "STORAGE"

    SHIPPING = "SHIPPING"

    CHARACTERIZATION = "CHARACTERIZATION"

    # ----------------------------------------------
    # Safety
    # ----------------------------------------------

    DIAGNOSTIC = "DIAGNOSTIC"

    RECOVERY = "RECOVERY"

    FAULT = "FAULT"

    SHUTDOWN = "SHUTDOWN"

    EMERGENCY = "EMERGENCY"
    
# ==========================================================
# Lifecycle Status
# ==========================================================

class CellLifecycleStatus(str, Enum):

    MANUFACTURED = "MANUFACTURED"

    FORMATION = "FORMATION"

    QUALIFIED = "QUALIFIED"

    STORED = "STORED"

    SHIPPED = "SHIPPED"

    INSTALLED = "INSTALLED"

    ACTIVE = "ACTIVE"

    MAINTENANCE = "MAINTENANCE"

    AGING = "AGING"

    RETIRED = "RETIRED"

    RECYCLED = "RECYCLED"

    FAILED = "FAILED"


# ==========================================================
# Health Status
# ==========================================================

class CellHealthStatus(str, Enum):

    EXCELLENT = "EXCELLENT"

    GOOD = "GOOD"

    FAIR = "FAIR"

    DEGRADED = "DEGRADED"

    CRITICAL = "CRITICAL"

    FAILED = "FAILED"


# ==========================================================
# Diagnostic Status
# ==========================================================

class DiagnosticStatus(str, Enum):

    NORMAL = "NORMAL"

    WARNING = "WARNING"

    FAULT = "FAULT"

    CRITICAL = "CRITICAL"

    UNKNOWN = "UNKNOWN"