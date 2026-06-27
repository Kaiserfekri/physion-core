class BaseChemistry:
    """
    کلاس پایه برای همهٔ شیمی‌ها.
    """

    def U_anode(self, soc, T_K):
        raise NotImplementedError

    def U_cathode(self, soc, T_K):
        raise NotImplementedError

    def dUeq_dT(self, soc_a, soc_c):
        raise NotImplementedError

    def capacity_anode(self):
        raise NotImplementedError

    def capacity_cathode(self):
        raise NotImplementedError

    def diffusion_coeff_anode(self, soc, T_K):
        raise NotImplementedError

    def diffusion_coeff_cathode(self, soc, T_K):
        raise NotImplementedError

    def kinetics_params_anode(self):
        raise NotImplementedError

    def kinetics_params_cathode(self):
        raise NotImplementedError

    def electrolyte_params(self):
        raise NotImplementedError

    def mechanical_params(self):
        raise NotImplementedError

    def degradation_params(self):
        raise NotImplementedError
