# physion_core/reaction.py
import numpy as np

FARADAY = 96485.3329  # C/mol


class ReactionModel:
    """
    Reaction and Li-plating model.

    - Reaction flux: j/F  (mol/(m^2·s))
    - Li-plating: kinetic rate based on negative anode overpotential.
    """

    def __init__(self, cfg):
        self.cfg = cfg
        # پارامترهای سینتیکی Li-plating
        self.eta_crit = getattr(cfg, "eta_plating_crit", -0.03)  # V
        self.k_pl = getattr(cfg, "k_plating", 0.0)               # mol/(C·s) یا مشابه

    def reaction_flux(self, j):
        """
        j [A/m^2] → mol/(m^2·s)
        """
        return j / FARADAY

    def li_plating_rate(self, j, eta_a):
        """
        Li-plating rate based on overpotential of anode.

        Only active when eta_a < eta_crit.
        """
        if eta_a < self.eta_crit and self.k_pl > 0.0:
            return self.k_pl * abs(j) * abs(self.eta_crit - eta_a) / FARADAY
        return 0.0
