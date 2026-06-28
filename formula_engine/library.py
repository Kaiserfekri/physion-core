class FormulaLibrary:
    def __init__(self):
        self.topics = {
            "li_metal_interface": [
                "i = i0 * (exp(alpha*F*eta/(R*T)) - exp(-(1-alpha)*F*eta/(R*T)))",
                "J = -D * grad_c + (sigma/(R*T)) * c * grad_phi",
            ],
            "sei_growth": [
                "dL_sei_dt = k_sei * i**n",
            ],
            "mechanical_coupling": [
                "sigma = E * epsilon + gamma * c",
            ],
        }

    def get_formulas(self, topic):
        return self.topics.get(topic, [])
