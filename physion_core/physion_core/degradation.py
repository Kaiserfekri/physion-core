import numpy as np
from physion_core.fullcell.physics_state import PhysicsState


class DegradationModel:
    """
    Simple LLI/LAM-like degradation accumulator:
    نسخهٔ ترکیبی:
    - اسکلت قبلی update(state, dt)
    - پارامترهای k_LLI, k_LAM از cfg یا chemistry
    """

    def __init__(self, cfg_or_chemistry):
        self.src = cfg_or_chemistry
        self.k_LLI = getattr(self.src, "k_LLI", 0.0)
        self.k_LAM = getattr(self.src, "k_LAM", 0.0)
        self.LLI = 0.0
        self.LAM = 0.0

    def update(self, state: PhysicsState, dt: float):
        sei_avg = getattr(state, "sei_avg", 0.0)
        j = state.current_density_A_m2

        self.LLI += self.k_LLI * sei_avg * dt
        self.LAM += self.k_LAM * abs(j) * dt

    def capacity_fade(self):
        return self.LLI + self.LAM
