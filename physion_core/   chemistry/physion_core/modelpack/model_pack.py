from physion_core.chemistry.nmc_graphite import NMCGraphiteChemistry
from physion_core.chemistry.lfp_graphite import LFPGraphiteChemistry
from physion_core.chemistry.lco_graphite import LCOGraphiteChemistry
from physion_core.chemistry.nca_graphite import NCAGraphiteChemistry

from physion_core.chemistry.parameter_loader import (
    load_nmc_graphite_params,
    load_lfp_graphite_params,
    load_lco_graphite_params,
    load_nca_graphite_params,
)

from physion_core.fullcell.fullcell_model import FullCellModel


class ModelPackConfig:
    """
    تنظیمات انتخاب شیمی و مسیر JSON.
    """

    def __init__(self,
                 chemistry_name: str = "LFP_GRAPHITE_SIMPLE",
                 params_path: str = "physion_core/params/lfp_graphite_simple.json"):
        self.chemistry_name = chemistry_name
        self.params_path = params_path


def build_chemistry(cfg_pack: ModelPackConfig):
    """
    ساخت آبجکت شیمی بر اساس نام و JSON.
    """
    name = cfg_pack.chemistry_name.upper()

    if name.startswith("LFP_GRAPHITE"):
        return LFPGraphiteChemistry(load_lfp_graphite_params(cfg_pack.params_path))

    if name.startswith("NMC_GRAPHITE"):
        return NMCGraphiteChemistry(load_nmc_graphite_params(cfg_pack.params_path))

    if name.startswith("LCO_GRAPHITE"):
        return LCOGraphiteChemistry(load_lco_graphite_params(cfg_pack.params_path))

    if name.startswith("NCA_GRAPHITE"):
        return NCAGraphiteChemistry(load_nca_graphite_params(cfg_pack.params_path))

    raise ValueError(f"Unknown chemistry: {cfg_pack.chemistry_name}")


def build_fullcell(cfg):
    """
    اتصال شیمی به cfg و ساخت FullCellModel.
    """
    cfg.chemistry = build_chemistry(cfg.model_pack)
    return FullCellModel(cfg)
