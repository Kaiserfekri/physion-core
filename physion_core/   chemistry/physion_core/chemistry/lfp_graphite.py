from .base import BaseChemistry

class LFPGraphiteChemistry(BaseChemistry):
    def __init__(self, params):
        self.p = params

    def U_anode(self, soc, T_K):
        return self.p["U_anode"](soc, T_K)

    def U_cathode(self, soc, T_K):
        return self.p["U_cathode"](soc, T_K)

    def dUeq_dT(self, soc_a, soc_c):
        return self.p["dU_cathode_dT"](soc_c) - self.p["dU_anode_dT"](soc_a)

    # بقیه مثل NMC
