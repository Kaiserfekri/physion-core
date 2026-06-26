import numpy as np
import logging

from .electrode import ElectrodeSPM
from .tzim import TZIMModel
from .thermal import ThermalModel
from .resistance import ResistanceModel
from .electrolyte import Electrolyte1DModel  # مدل الکترولیت

logger = logging.getLogger("fullcell")


class FullCellModel:
    """
    Full cell simulation engine for Physion Web Engine
    (SOC + OCV(SOC) + j_lim + TZIM + Electrolyte1D + full history
     با کوپل واقعی الکترولیت روی j0 و R_electrolyte)
    """

    def __init__(self, cfg):
        self.cfg = cfg

        # Sub‑models
        self.anode = ElectrodeSPM(cfg, is_anode=True)
        self.cathode = ElectrodeSPM(cfg, is_anode=False)
        self.tzim = TZIMModel(cfg)
        self.thermal = ThermalModel(cfg)
        self.resistance = ResistanceModel(cfg)
        self.electrolyte = Electrolyte1DModel(cfg)

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
            "C_e_surface": [],
            "hotspot_z_um": [],
            "hotspot_j": [],
            "DGI_max": [],
            "CCD": [],
        }

        logger.info("FullCellModel initialized with Electrolyte coupling.")

    def step(self, dt):
        """
        One simulation step
        """

        # Applied current density
        j = self.cfg.I_app()

        # SEI update (TZIM)
        self.tzim.update_sei(j, dt)
        sei_avg = float(np.mean(self.tzim.sei))

        # الکترولیت: یک گام ساده با ولتاژ قبلی تخمینی
        # ابتدا ولتاژ تخمینی بدون کوپل الکترولیت:
        V_guess = 0.0
        if hasattr(self.cfg, "U_cathode") and hasattr(self.cfg, "U_anode"):
            U_a_guess = self.cfg.U_anode(self.anode.soc)
            U_c_guess = self.cfg.U_cathode(self.cathode.soc)
            V_guess = U_c_guess - U_a_guess
        self.electrolyte.step(j_app=j, dt=dt, V_app=V_guess)

        # سطح الکترولیت در سمت آند
        C_e_surface = float(self.electrolyte.C[0])

        # Surface concentrations
        cs_a = self.anode.surface_concentration()
        cs_c = self.cathode.surface_concentration()

        # Overpotentials با کوپل الکترولیت
        eta_a = self.anode.overpotential(j, C_e_surface)
        eta_c = self.cathode.overpotential(-j, C_e_surface)

        # Resistance update (SEI)
        self.resistance.update_sei_resistance(sei_avg)
        R_total = self.resistance.total(C_e_surface)

        # OCV(SOC)
        if hasattr(self.cfg, "U_cathode") and hasattr(self.cfg, "U_anode"):
            U_a = self.cfg.U_anode(self.anode.soc)
            U_c = self.cfg.U_cathode(self.cathode.soc)
            V_eq = U_c - U_a
        else:
            V_eq = 0.0

        # Total voltage با در نظر گرفتن R_total و اورپتانسیل‌ها
        V = V_eq + (eta_c - eta_a) - j * R_total

        # Diffusion + SOC update
        self.anode.update_diffusion(j, dt)
        self.cathode.update_diffusion(-j, dt)

        # Thermal update
        self.thermal.update(j, eta_a + eta_c, sei_avg, dt)

        # Time update
        self.t += dt

        # j_lim
        j_lim_a = self.anode.j_lim()
        j_lim_c = self.cathode.j_lim()

        # Electrolyte analytics
        hotspot_z_um, hotspot_j = self.electrolyte.hotspot()
        DGI = self.electrolyte.DGI_profile()
        DGI_max = float(np.max(DGI))
        CCD_now = float(self.electrolyte.CCD())

        logger.debug(
            f"t={self.t:.2f}, V={V:.3f}, eta_a={eta_a:.4f}, eta_c={eta_c:.4f}, "
            f"j_lim_a={j_lim_a:.4f}, j_lim_c={j_lim_c:.4f}, "
            f"C_e_surf={C_e_surface:.2f}, DGI_max={DGI_max:.3f}, CCD={CCD_now:.2f}"
        )

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

        # Electrolyte + multiphysics
        self.history["C_e_surface"].append(C_e_surface)
        self.history["hotspot_z_um"].append(hotspot_z_um)
        self.history["hotspot_j"].append(hotspot_j)
        self.history["DGI_max"].append(DGI_max)
        self.history["CCD"].append(CCD_now)

    def run(self):
        """
        Run full simulation
        """
        dt = self.cfg.dt_min
        steps = int(self.cfg.n_cycles * self.cfg.t_half_cycle / dt)

        logger.info("FullCellModel: Simulation started. Steps=%d", steps)

        for _ in range(steps):
            self.step(dt)

        logger.info("FullCellModel: Simulation finished.")
        return self.history
