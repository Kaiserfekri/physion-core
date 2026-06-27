from .base import BaseChemistry

class NMCGraphiteChemistry(BaseChemistry):
    def __init__(self, params):
        self.p = params

    def U_anode(self, soc, T_K):
        return self.p["U_anode"](soc, T_K)

    def U_cathode(self, soc, T_K):
        return self.p["U_cathode"](soc, T_K)

    def dUeq_dT(self, soc_a, soc_c):
        return self.p["dU_cathode_dT"](soc_c) - self.p["dU_anode_dT"](soc_a)

    def capacity_anode(self):
        return self.p["capacity_anode"]

    def capacity_cathode(self):
        return self.p["capacity_cathode"]

    def diffusion_coeff_anode(self, soc, T_K):
        return self.p["D_anode"](soc, T_K)

    def diffusion_coeff_cathode(self, soc, T_K):
        return self.p["D_cathode"](soc, T_K)

    def kinetics_params_anode(self):
        return self.p["kinetics_anode"]

    def kinetics_params_cathode(self):
        return self.p["kinetics_cathode"]

    def electrolyte_params(self):
        return self.p["electrolyte"]

    def mechanical_params(self):
        return self.p["mechanical"]

    def degradation_params(self):
        return self.p["degradation"]