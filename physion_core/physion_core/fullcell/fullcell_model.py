import numpy as np

from physion_core.fullcell.physics_state import PhysicsState
from physion_core.physics.reaction_model import ReactionModel
from physion_core.physics.electrode_spm import ElectrodeSPM
from physion_core.mechanics import MechanicalModel
from physion_core.degradation import DegradationModel


class FullCellModel:
    """
    Physion V30 – Hybrid FullCellModel
    - SOC مینیمال مبتنی بر capacity از chemistry (نسخه قبلی)
    - SPM diffusion + SOC داخلی ذرات (نسخه جدید)
    - Butler–Volmer + OCV
    - مکانیک + تخریب
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.chemistry = cfg.chemistry
        self.state = PhysicsState()

        self.reaction = ReactionModel(cfg)
        self.anode = ElectrodeSPM(cfg, is_anode=True)
        self.cathode = ElectrodeSPM(cfg, is_anode=False)
        self.mechanics = MechanicalModel(self.chemistry)
        self.degradation = DegradationModel(self.chemistry)

    def _update_soc_capacity_based(self, dt: float):
        J = self.state.current_density_A_m2

        cap_an = self.chemistry.capacity_anode()
        cap_ca = self.chemistry.capacity_cathode()

        if cap_an > 0:
            d_soc_an = - J * dt / (3600.0 * cap_an)
            self.state.soc_anode += d_soc_an

        if cap_ca > 0:
            d_soc_ca = J * dt / (3600.0 * cap_ca)
            self.state.soc_cathode += d_soc_ca

    def _update_electrodes_spm(self, j, dt):
        self.anode.update_diffusion(j, dt)
        self.cathode.update_diffusion(j, dt)

        self.state.soc_anode = 0.5 * (self.state.soc_anode + self.anode.soc)
        self.state.soc_cathode = 0.5 * (self.state.soc_cathode + self.cathode.soc)

    def step(self, dt: float, current_density_A_m2: float):
        self.state.time_s += dt

        j = current_density_A_m2
        self.state.current_density_A_m2 = j

        # SOC مینیمال
        self._update_soc_capacity_based(dt)

        # SPM
        self._update_electrodes_spm(j, dt)

        # واکنش + BV
        eta_cell, V_eq = self.reaction.compute_overpotential_cell(self.state)
        j_bv = self.reaction.compute_flux_bv(self.state, eta_cell)
        self.state.reaction_rate_A_m2 = j_bv

        # گرما (نسخه جدید برناردی)
        q_dot = self.reaction.compute_heat_bernardi(self.state, V_eq)
        self.state.heat_source_W_m3 = q_dot

        # تنش
        self.state.stress_Pa = self.mechanics.compute_stress(self.state)

        # تخریب
        self.degradation.update(self.state, dt)

    def summary(self):
        return {
            "chemistry": type(self.chemistry).__name__,
            "capacity_anode": self.chemistry.capacity_anode(),
            "capacity_cathode": self.chemistry.capacity_cathode(),
            "time_s": self.state.time_s,
            "current_density_A_m2": self.state.current_density_A_m2,
            "soc_anode": self.state.soc_anode,
            "soc_cathode": self.state.soc_cathode,
            "equilibrium_voltage_V": getattr(self.state, "equilibrium_voltage_V", None),
            "overpotential_cell_V": getattr(self.state, "overpotential_cell_V", None),
            "reaction_rate_A_m2": self.state.reaction_rate_A_m2,
            "heat_source_W_m3": self.state.heat_source_W_m3,
            "stress_Pa": getattr(self.state, "stress_Pa", None),
        }

