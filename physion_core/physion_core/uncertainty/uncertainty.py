# uncertainty.py

import numpy as np
from copy import deepcopy


class UncertaintyEngine:
    """
    Uncertainty layer با استفاده از posterior پارامترها،
    covariance و propagation از طریق مدل.
    بدون تغییر در هسته.
    """

    def __init__(self, model_class, cfg, posterior_samples: list[tuple[dict, float]]):
        self.model_class = model_class
        self.cfg = cfg
        self.posterior_samples = posterior_samples

    def parameter_posterior(self):
        if not self.posterior_samples:
            return {}

        keys = list(self.posterior_samples[0][0].keys())
        vals = {k: [] for k in keys}

        for params, _ in self.posterior_samples:
            for k in keys:
                vals[k].append(params[k])

        stats = {}
        for k in keys:
            arr = np.array(vals[k])
            stats[k] = {
                "mean": float(np.mean(arr)),
                "var": float(np.var(arr))
            }
        return stats

    def covariance_structure(self):
        if not self.posterior_samples:
            return None

        keys = list(self.posterior_samples[0][0].keys())
        data = np.array([[params[k] for k in keys] for params, _ in self.posterior_samples])
        cov = np.cov(data.T)
        return {
            "params": keys,
            "covariance": cov.tolist()
        }

    def propagate(self, n: int = 80):
        """
        انتشار عدم قطعیت پارامترها از طریق مدل
        با استفاده از میانگین و کوواریانس posterior
        """
        if not self.posterior_samples:
            return {
                "V_lower": [],
                "V_upper": [],
                "V_mean": [],
                "sims": []
            }

        keys = list(self.posterior_samples[0][0].keys())
        data = np.array([[p[k] for k in keys] for p, _ in self.posterior_samples])
        mean = np.mean(data, axis=0)
        cov = np.cov(data.T) + 1e-6 * np.eye(len(keys))

        sims = []
        for _ in range(n):
            sample = np.random.multivariate_normal(mean, cov)
            cfg = deepcopy(self.cfg)
            for k, v in zip(keys, sample):
                setattr(cfg, k, v)
            sim = self.model_class(cfg).run()
            sims.append(sim)

        V_all = np.array([s["V"] for s in sims])
        V_lower = np.percentile(V_all, 5, axis=0)
        V_upper = np.percentile(V_all, 95, axis=0)
        V_mean = np.mean(V_all, axis=0)

        return {
            "V_lower": V_lower.tolist(),
            "V_upper": V_upper.tolist(),
            "V_mean": V_mean.tolist(),
            "sims": sims
        }
