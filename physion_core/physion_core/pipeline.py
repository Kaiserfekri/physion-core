import numpy as np
from .calibration import CalibrationEngine
from .uncertainty import UncertaintyEngine
from .trust import TrustEngine


def run_pipeline(model_class, cfg, exp_data, param_names, n_mcmc=400, n_uncertainty=80):
    """
    اجرای کامل سه لایه:
    1) Calibration
    2) Uncertainty propagation
    3) Trust evaluation

    ورودی‌ها:
        model_class: کلاس مدل (FullCellModel)
        cfg: پیکربندی سلول
        exp_data: دادهٔ واقعی
        param_names: لیست پارامترهایی که باید کالیبره شوند
        n_mcmc: تعداد نمونه‌های MCMC
        n_uncertainty: تعداد نمونه‌های propagation

    خروجی:
        dict شامل:
            - best_params
            - posterior_samples
            - uncertainty
            - trust
    """

    # -----------------------------
    # 1) Calibration
    # -----------------------------
    cal = CalibrationEngine(model_class, cfg)

    # مرحلهٔ اول: تخمین اولیه با likelihood
    best_params, best_cost = cal.fit_via_likelihood(exp_data, param_names)

    # مرحلهٔ دوم: MCMC برای posterior واقعی
    posterior_samples = cal.adaptive_mcmc(exp_data, param_names, n_samples=n_mcmc)

    # -----------------------------
    # 2) Uncertainty propagation
    # -----------------------------
    unc = UncertaintyEngine(model_class, cfg, posterior_samples)
    uncertainty_output = unc.propagate(n=n_uncertainty)

    # -----------------------------
    # 3) Trust evaluation
    # -----------------------------
    trust = TrustEngine()
    trust_output = {
        "predictive_interval": trust.predictive_interval(uncertainty_output),
        "coverage_probability": trust.coverage_probability(uncertainty_output, exp_data),
    }

    # اگر دیتاست اعتبارسنجی جداگانه داری:
    if "validation" in exp_data:
        sim0 = model_class(cfg).run()
        trust_output["validation_score"] = trust.validation_score(sim0, exp_data["validation"])

    # -----------------------------
    # خروجی نهایی
    # -----------------------------
    return {
        "best_params": best_params,
        "posterior_samples": posterior_samples,
        "uncertainty": uncertainty_output,
        "trust": trust_output
    }
