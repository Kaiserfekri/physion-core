import numpy as np

from .electrode import ElectrodeSPM
from .tzim import TZIMModel
from .thermal import ThermalModel
from .resistance import ResistanceModel


class FullCellModel:
    """
    Full cell simulation engine for Physion Web Engine
    """

    def __init__(self, cfg):
        self.cfg = cfg

        # Sub‑models
        self.anode = ElectrodeSPM(cfg, is_anode=True)
        self.cathode = ElectrodeSPM(cfg, is_anode=False)
        self.tzim = TZIMModel(cfg)
        self.thermal = ThermalModel(cfg)
        self.resistance = ResistanceModel(cfg)

        # Time
        self.t = 0.0

        # Data storage
        self.history = {
            "t": [],
            "V": [],
            "T": [],
            "sei_avg": [],
            "R_total": [],
            "cs_anode": [],
            "cs_cathode": [],
        }

    def step(self, dt):
        """
        One simulation step
        """

        # Applied current
        j = self.cfg.I_app()

        # Surface concentrations
        cs_a = self.anode.surface_concentration()
        cs_c = self.cathode.surface_concentration()

        # Overpotentials
        eta_a = self.anode.overpotential(j)
        eta_c = self.cathode.overpotential(-j)

        # SEI growth
        sei_rate = abs(j) * 1e-9
        self.tzim.update_sei(j, dt)

        # Update SEI resistance
        sei_avg = float(np.mean(self.tzim.sei))
        self.resistance.update_sei_resistance(sei_avg)

        # Total resistance
        R_total = self.resistance.total()

        # Cell voltage
        V = (
            self.cfg.U_anode
            - self.cfg.U_anode
            + eta_c
            - eta_a
            - j * R_total
        )

        # Update diffusion
        self.anode.update_diffusion(j, dt)
        self.cathode.update_diffusion(-j, dt)

        # Update thermal model
        self.thermal.update(j, eta_a + eta_c, sei_rate, dt)

        # Time update
        self.t += dt

        # Save history
        self.history["t"].append(self.t)
        self.history["V"].append(float(V))
        self.history["T"].append(float(self.thermal.T))
        self.history["sei_avg"].append(sei_avg)
        self.history["R_total"].append(float(R_total))
        self.history["cs_anode"].append(float(cs_a))
        self.history["cs_cathode"].append(float(cs_c))

    def run(self):
        """
        Run full simulation
        """
        dt = self.cfg.dt_min
        steps = int(self.cfg.n_cycles * self.cfg.t_half_cycle / dt)

        for _ in range(steps):
            self.step(dt)

        return self.history
