import numpy as np

from .electrode import ElectrodeSPM
from .tzim import TZIMModel
from .thermal import ThermalModel
from .resistance import ResistanceModel


class FullCellModel:
    """
    Full cell simulation engine for Physion Web Engine
    (revised: SOC + OCV(SOC) + full history)
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
        }

    def step(self, dt):
        """
        One simulation step
        """

        # Applied current density (A/m^2 or normalized)
        j = self.cfg.I_app()

        # Surface concentrations
        cs_a = self.anode.surface_concentration()
        cs_c = self.cathode.surface_concentration()

        # Overpotentials (from ElectrodeSPM / Butler–Volmer)
        eta_a = self.anode.overpotential(j)
        eta_c = self.cathode.overpotential(-j)

        # --- SEI update (only via TZIM, no fake sei_rate model) ---
        self.tzim.update_sei(j, dt)
        sei_avg = float(np.mean(self.tzim.sei))

        # Update SEI resistance from SEI thickness
        self.resistance.update_sei_resistance(sei_avg)

        # Total resistance (ohmic + SEI + others)
        R_total = self.resistance.total()

        # --- Cell voltage ---
        # V_cell = (phi_c - phi_a) ≈ (U_c(SOC_c) - U_a(SOC_a)) + (eta_c - eta_a) - j * R_total
        if hasattr(self.cfg, "U_cathode") and hasattr(self.cfg, "U_anode"):
            U_a = self.cfg.U_anode(self.anode.soc)
            U_c = self.cfg.U_cathode(self.cathode.soc)
            V_eq = U_c - U_a
        else:
            V_eq = 0.0

        V = V_eq + (eta_c - eta_a) - j * R_total

        # Update diffusion in electrodes (includes SOC update inside electrode)
        self.anode.update_diffusion(j, dt)
        self.cathode.update_diffusion(-j, dt)

        # Update thermal model
        # منبع گرما ~ j * (eta_a + eta_c) + losses
        self.thermal.update(j, eta_a + eta_c, sei_avg, dt)

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
        self.history["eta_anode"].append(float(eta_a))
        self.history["eta_cathode"].append(float(eta_c))
        self.history["soc_anode"].append(float(self.anode.soc))
        self.history["soc_cathode"].append(float(self.cathode.soc))

    def run(self):
        """
        Run full simulation
        """
        dt = self.cfg.dt_min
        steps = int(self.cfg.n_cycles * self.cfg.t_half_cycle / dt)

        for _ in range(steps):
            self.step(dt)

        return self.history
