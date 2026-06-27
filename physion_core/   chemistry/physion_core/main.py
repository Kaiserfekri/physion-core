from physion_core.modelpack import ModelPackConfig, build_fullcell
from physion_core.config import PhysionConfig  # فرضی، همان cfg فعلی تو

def run_simulation():
    # تنظیمات اصلی
    cfg = PhysionConfig()

    # انتخاب شیمی و مدل‌ها
    cfg.model_pack = ModelPackConfig(
        chemistry_name="NMC_GRAPHITE_V1",
        params_path="params/nmc_graphite_v1.json"
    )

    # ساخت FullCellModel با شیمی انتخاب‌شده
    fullcell = build_fullcell(cfg)

    # اجرای شبیه‌سازی
    history = fullcell.run()
    return history
