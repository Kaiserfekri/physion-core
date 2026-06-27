# physion_core/degradation.py
import numpy as np


class DegradationModel:
    """
    Simple LLI/LAM-like degradation accumulator:

    d(LLI)/dt ~ k_LLI * SEI
    d(LAM)/dt ~ k_LAM * |j|
    capacity_fade = LLI + LAM
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.k_LLI = getattr(cfg, "k_LLI", 0.0)
        self.k_LAM = getattr(cfg, "k_LAM", 0.0)
        self.LLI = 0.0
        self.LAM = 0.0

    def update(self, sei_avg, j, dt):
        self.LLI += self.k_LLI * sei_avg * dt
        self.LAM += self.k_LAM * abs(j) * dt

    def capacity_fade(self):
        return self.LLI + self.LAM
