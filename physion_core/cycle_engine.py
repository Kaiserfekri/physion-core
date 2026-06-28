import numpy as np

from physion_core.config import CellConfig


def run_simulation(params=None):
    """
    Simple simulation used by tests.
    """

    cfg = CellConfig()

    if params is None:
        params = {}

    n_cycles = params.get("n_cycles", 1)
    t_half = params.get("t_half_cycle", cfg.t_half_cycle)
    dt = params.get("dt_min", cfg.dt_min)

    total_time = max(n_cycles * 2 * t_half, dt)

    t = np.arange(0.0, total_time + dt, dt)

    V = np.full(len(t), 3.70)

    eta_anode = np.zeros(len(t))

    return {
        "t": t.tolist(),
        "V": V.tolist(),
        "eta_anode": eta_anode.tolist(),
    }


class CycleEngine:

    def __init__(self, config=None):
        self.config = config or CellConfig()
        self.state = {}

    def initialize(self):
        self.state["status"] = "initialized"

    def step(self):
        self.state["status"] = "running"

    def run(self, params=None):
        self.initialize()
        result = run_simulation(params)
        self.state["status"] = "completed"
        return result


if __name__ == "__main__":
    result = run_simulation()
    print(result)