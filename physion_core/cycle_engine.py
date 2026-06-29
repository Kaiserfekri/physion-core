"""
cycle_engine.py
===============

Main simulation engine for Physion.

CycleEngine is responsible for

- loading chemistry parameters
- initializing simulation state
- executing cycle simulations
"""

from __future__ import annotations

import numpy as np

from physion_core.config import CellConfig

from physion_core.params.parameter_set import ParameterSet


# ==========================================================
# Simulation
# ==========================================================

def run_simulation(
    parameter_set: ParameterSet,
):
    """
    Temporary simulation kernel.

    Future versions will call the electrochemical,
    thermal and degradation solvers.
    """

    cfg = CellConfig()

    n_cycles = parameter_set.get(
        "n_cycles",
        1,
    )

    t_half = parameter_set.get(
        "t_half_cycle",
        cfg.t_half_cycle,
    )

    dt = parameter_set.get(
        "dt_min",
        cfg.dt_min,
    )

    total_time = max(

        n_cycles * 2 * t_half,

        dt,

    )

    t = np.arange(

        0.0,

        total_time + dt,

        dt,

    )

    V = np.full(

        len(t),

        3.70,

    )

    eta_anode = np.zeros(

        len(t),

    )

    return {

        "t": t.tolist(),

        "V": V.tolist(),

        "eta_anode": eta_anode.tolist(),

    }


# ==========================================================
# Cycle Engine
# ==========================================================

class CycleEngine:

    """
    Main Physion simulation engine.
    """

    def __init__(

        self,

        chemistry: str = "lfp_graphite",

        level: str = "basic",

        config=None,

    ):

        self.config = config or CellConfig()

        self.parameter_set = ParameterSet(

            chemistry=chemistry,

            level=level,

        )

        self.state = {}

    # ------------------------------------------------------

    def initialize(self):

        self.state["status"] = "initialized"

    # ------------------------------------------------------

    def step(self):

        self.state["status"] = "running"

    # ------------------------------------------------------

    def run(self):

        self.initialize()

        result = run_simulation(

            self.parameter_set,

        )

        self.state["status"] = "completed"

        return result


# ==========================================================
# Demo
# ==========================================================

if __name__ == "__main__":

    engine = CycleEngine(

        chemistry="lfp_graphite",

        level="basic",

    )

    result = engine.run()

    print(result)