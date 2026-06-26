# calibration.py

import numpy as np
from copy import deepcopy
from scipy.optimize import minimize


class CalibrationEngine:
    """
    Realistic calibration layer for Physion Web Engine.
    بدون تغییر در هسته.
    - multi-observable likelihood
    - state-dependent noise (physics-informed)
    - adaptive, covariance-aware MCMC
    """

    def __init__(self, model_class, cfg):
        self.model_class = model_class
        self.cfg = cfg

    def _simulate(self, params: dict):
        cfg = deepcopy(self.cfg)
        for k, v in params.items():
            setattr(cfg, k, v)
        model = self.model_class(cfg)
        return model.run()

    def _sigma_state(self, sim: dict):
        """
        نویز وابسته به state:
        sigma_V, sigma_T, sigma_R بر اساس SOC و جریان و دما
        """
        soc = np.array(sim["soc_anode"])
        T = np.array(sim["T"])
        R = np.array(sim["R_total"])
        j = self.cfg.I_app()

        # physics-informed noise:
        sigma_V = 0.003 + 0.004 * np.abs(j) + 0.006 * (1 - soc)
        sigma_T = 0.3 + 0.002 * np.clip(T - 298.0, 0, None)
        sigma_R = 0.0005 + 0.02 * np.abs(j)

        return sigma_V, sigma_T, sigma_R

    def mixed_likelihood(self, diff: np.ndarray, sigma: np.ndarray):
        """
        Gaussian + Laplace mixture likelihood
        """
        gauss = -0.5 * (diff / sigma) ** 2
        laplace = -np.abs(diff) / (sigma * 0.8)
        return np.logaddexp(gauss, laplace)

    def multi_observable_likelihood(self, sim: dict, exp: dict):
        """
        likelihood روی چند observable:
        V, T, R_total, SOC_end
        """
        n = min(len(sim["V"]), len(exp["V"]))

        V_sim = np.array(sim["V"][:n])
        V_exp = np.array(exp["V"][:n])

        T_sim = np.array(sim["T"][:n])
        T_exp = np.array(exp["T"][:n])

        R_sim = np.array(sim["R_total"][:n])
        R_exp = np.array(exp.get("R_total", R_sim)[:n])

        sigma_V, sigma_T, sigma_R = self._sigma_state(sim)
        sigma_V = sigma_V[:n]
        sigma_T = sigma_T[:n]
        sigma_R = sigma_R[:n]

        ll_V = np.sum(self.mixed_likelihood(V_sim - V_exp, sigma_V))
        ll_T = np.sum(self.mixed_likelihood(T_sim - T_exp, sigma_T))
        ll_R = np.sum(self.mixed_likelihood(R_sim - R_exp, sigma_R))

        soc_sim = float(sim["soc_anode"][-1])
        soc_exp = float(exp.get("soc_end", soc_sim))
        sigma_soc = 0.02
        ll_soc = -0.5 * ((soc_sim - soc_exp) / sigma_soc) ** 2

        return float(ll_V + ll_T + ll_R + ll_soc)

    def fit_via_likelihood(self, exp_data: dict, param_names: list[str]):
        """
        حداکثرسازی likelihood چند observable
        """
        p0 = np.array([getattr(self.cfg, p) for p in param_names])

        def objective(p):
            params = {name: val for name, val in zip(param_names, p)}
            sim = self._simulate(params)
            ll = self.multi_observable_likelihood(sim, exp_data)
            return -ll

        sol = minimize(objective, p0, method="L-BFGS-B")
        best_params = {name: val for name, val in zip(param_names, sol.x)}
        return best_params, float(sol.fun)

    def adaptive_mcmc(self, exp_data: dict, param_names: list[str], n_samples: int = 400):
        """
        MCMC تطبیقی با proposal کوواریانس‌محور
        """
        current = {p: getattr(self.cfg, p) for p in param_names}
        current_sim = self._simulate(current)
        current_ll = self.multi_observable_likelihood(current_sim, exp_data)

        samples: list[tuple[dict, float]] = []
        dim = len(param_names)
        cov = np.eye(dim) * 1e-4

        for i in range(n_samples):
            if i > 30 and i % 20 == 0 and len(samples) > 10:
                data = np.array([[s[0][p] for p in param_names] for s in samples])
                cov = np.cov(data.T) + 1e-6 * np.eye(dim)

            proposal_vec = np.random.multivariate_normal(
                np.array([current[p] for p in param_names]),
                cov
            )
            proposal = {p: v for p, v in zip(param_names, proposal_vec)}

            sim_prop = self._simulate(proposal)
            ll_prop = self.multi_observable_likelihood(sim_prop, exp_data)

            alpha = np.exp(ll_prop - current_ll)
            if np.random.rand() < min(1.0, alpha):
                current = proposal
                current_ll = ll_prop

            samples.append((current.copy(), current_ll))

        samples.sort(key=lambda x: -x[1])
        return samples
