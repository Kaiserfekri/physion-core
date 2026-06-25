import numpy as np

from .electrode import ElectrodeSPM
from .tzim import TZIMModel
from .thermal import ThermalModel
from .resistance import ResistanceModel


class FullCellModel:
    """
    Full cell simulation engine for Physion Web Engine
    (SOC + OCV(SOC) + j_lim + full history)
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
            "eta_anode": [],
            "eta_cathode": [],
            "soc_anode": [],
            "soc_cathode": [],
            "j_lim_anode": [],
            "j_lim_cathode": [],
        }

    def step(self, dt):
        """
        One simulation step
        """

        # Applied current density
        j = self.cfg.I_app()

        # Surface concentrations
        cs_a = self.anode.surface_concentration()
        cs_c = self.cathode.surface_concentration()

        # Overpotentials
        eta_a = self.anode.overpotential(j)
        eta_c = self.cathode.overpotential(-j)

        # SEI update
        self.tzim.update_sei(j, dt)
        sei_avg = float(np.mean(self.tzim.sei))

        # Resistance update
        self.resistance.update_sei_resistance(sei_avg)
        R_total = self.resistance.total()

        # OCV(SOC)
        if hasattr(self.cfg, "U_cathode") and hasattr(self.cfg, "U_anode"):
            U_a = self.cfg.U_anode(self.anode.soc)
            U_c = self.cfg.U_cathode(self.cathode.soc)
            V_eq = U_c - U_a
        else:
            V_eq = 0.0

        # Total voltage
        V = V_eq + (eta_c - eta_a) - j * R_total

        # Diffusion + SOC update
        self.anode.update_diffusion(j, dt)
        self.cathode.update_diffusion(-j, dt)

        # Thermal update
        self.thermal.update(j, eta_a + eta_c, sei_avg, dt)

        # Time update
        self.t += dt

        # ===== NEW: j_lim =====
        j_lim_a = self.anode.j_lim()
        j_lim_c = self.cathode.j_lim()

        # Save history
        self.history["t"].append(self.t)
        self.history["V"].append(float(V))
        self.history["T"].append(float(self.thermal.T))
        self.history["sei_avg"].append(sei_avg)
        self.history["R_total"].append(float(R_total))
        self.history["cs_anode"].append(float(cs_a))
        self.history["cs_cathode"].append(float(cs_c))
        self.history["eta_anode"].append(float(eta_a))
        self.history["eta_cathode"].append(float(eta_c))
        self.history["soc_anode"].append(float(self.anode.soc))
        self.history["soc_cathode"].append(float(self.cathode.soc))
        self.history["j_lim_anode"].append(float(j_lim_a))
        self.history["j_lim_cathode"].append(float(j_lim_c))

    def run(self):
        """
        Run full simulation
        """
        dt = self.cfg.dt_min
        steps = int(self.cfg.n_cycles * self.cfg.t_half_cycle / dt)

        for _ in range(steps):
            self.step(dt)

        return self.history
