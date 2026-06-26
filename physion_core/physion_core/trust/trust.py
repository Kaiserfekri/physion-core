# trust.py

import numpy as np


class TrustEngine:
    """
    Trust layer با:
      - predictive interval
      - coverage probability
      - validation scoring (CRPS + MSE + MAE)
    بدون تغییر در هسته.
    """

    def __init__(self):
        pass

    def predictive_interval(self, propagated: dict):
        """
        بازهٔ پیش‌بینی ولتاژ
        """
        return {
            "V_lower": propagated["V_lower"],
            "V_upper": propagated["V_upper"],
            "V_mean": propagated["V_mean"]
        }

    def coverage_probability(self, propagated: dict, exp_data: dict):
        """
        احتمال اینکه دادهٔ واقعی داخل بازهٔ پیش‌بینی باشد
        """
        V_lower = np.array(propagated["V_lower"])
        V_upper = np.array(propagated["V_upper"])
        V_exp = np.array(exp_data["V"][:len(V_lower)])

        inside = (V_exp >= V_lower) & (V_exp <= V_upper)
        coverage = float(np.mean(inside))
        return {
            "coverage_probability": coverage
        }

    def crps(self, V_lower: np.ndarray, V_upper: np.ndarray, V_exp: np.ndarray):
        """
        Continuous Ranked Probability Score (نسخهٔ ساده)
        """
        mid = 0.5 * (V_lower + V_upper)
        width = V_upper - V_lower
        return float(np.mean(np.abs(mid - V_exp) + 0.5 * width))

    def validation_score(self, sim: dict, dataset: dict):
        """
        ارزیابی مدل روی دیتاست اعتبارسنجی
        """
        n = min(len(sim["V"]), len(dataset["V"]))
        V_sim = np.array(sim["V"][:n])
        V_exp = np.array(dataset["V"][:n])

        mse = float(np.mean((V_sim - V_exp) ** 2))
        mae = float(np.mean(np.abs(V_sim - V_exp)))

        # برای CRPS، از یک بازهٔ ساده حول V_sim استفاده می‌کنیم
        V_lower = V_sim * 0.95
        V_upper = V_sim * 1.05
        crps_val = self.crps(V_lower, V_upper, V_exp)

        return {
            "mse": mse,
            "mae": mae,
            "crps": crps_val
        }
