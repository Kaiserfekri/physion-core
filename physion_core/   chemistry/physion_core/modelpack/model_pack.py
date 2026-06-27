from physion_core.chemistry.nmc_graphite import NMCGraphiteChemistry
from physion_core.chemistry.lfp_graphite import LFPGraphiteChemistry
from physion_core.chemistry.lco_graphite import LCOGraphiteChemistry
from physion_core.chemistry.nca_graphite import NCAGraphiteChemistry
from physion_core.chemistry.custom_user_defined import CustomUserChemistry

from physion_core.chemistry.parameter_loader import load_nmc_graphite_params
# بعداً: load_lfp_graphite_params, load_lco_graphite_params, ...

from physion_core.fullcell.fullcell_model import FullCellModel


class ModelPackConfig:
    """
    High-level configuration for selecting chemistry and sub-models.
    """

    def __init__(self,
                 chemistry_name: str = "NMC_GRAPHITE_V1",
                 params_path: str = "params/nmc_graphite_v1.json"):
        self.chemistry_name = chemistry_name
        self.params_path = params_path

        # مدل‌ها (فعلاً ثابت، بعداً قابل انتخاب می‌شوند)
        self.use_electrolyte_1d = True
        self.use_tzim = True
        self.use_thermal = True


def build_chemistry(cfg_pack: ModelPackConfig):
    """
    Build chemistry object from config.
    """
    name = cfg_pack.chemistry_name.upper()

    if name == "NMC_GRAPHITE_V1":
        params = load_nmc_graphite_params(cfg_pack.params_path)
        return NMCGraphiteChemistry(params)

    # TODO: LFP / LCO / NCA / Custom
    # elif name == "LFP_GRAPHITE_V1": ...
    # elif name == "LCO_GRAPHITE_V1": ...
    # elif name == "NCA_GRAPHITE_V1": ...
    # elif name == "CUSTOM_USER": ...

    raise ValueError(f"Unknown chemistry_name: {cfg_pack.chemistry_name}")


def build_fullcell(cfg):
    """
    High-level builder: attach chemistry to cfg and return FullCellModel.
    """
    # cfg باید یک آبجکت تنظیمات اصلی باشد (همان که الان داری)
    # و ما فقط به آن یک فیلد chemistry اضافه می‌کنیم.
    chem = build_chemistry(cfg.model_pack)

    cfg.chemistry = chem

    fc = FullCellModel(cfg)
    return fc
