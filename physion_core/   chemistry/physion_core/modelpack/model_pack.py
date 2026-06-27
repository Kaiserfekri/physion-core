from physion_core.chemistry.nmc_graphite import NMCGraphiteChemistry
from physion_core.chemistry.lfp_graphite import LFPGraphiteChemistry
from physion_core.chemistry.lco_graphite import LCOGraphiteChemistry
from physion_core.chemistry.nca_graphite import NCAGraphiteChemistry

from physion_core.chemistry.parameter_loader import (
    load_nmc_graphite_params,
    load_lfp_graphite_params,
    load_lco_graphite_params,
    load_nca_graphite_params
)

from physion_core.fullcell.fullcell_model import FullCellModel


class ModelPackConfig:
    def __init__(self, chemistry_name, params_path):
        self.chemistry_name = chemistry_name
        self.params_path = params_path


def build_chemistry(cfg_pack):
    name = cfg_pack.chemistry_name.upper()

    if name == "NMC_GRAPHITE_V1":
        return NMCGraphiteChemistry(load_nmc_graphite_params(cfg_pack.params_path))

    if name == "LFP_GRAPHITE_V1":
        return LFPGraphiteChemistry(load_lfp_graphite_params(cfg_pack.params_path))

    if name == "LCO_GRAPHITE_V1":
        return LCOGraphiteChemistry(load_lco_graphite_params(cfg_pack.params_path))

    if name == "NCA_GRAPHITE_V1":
        return NCAGraphiteChemistry(load_nca_graphite_params(cfg_pack.params_path))

    raise ValueError(f"Unknown chemistry: {cfg_pack.chemistry_name}")


def build_fullcell(cfg):
    cfg.chemistry = build_chemistry(cfg.model_pack)
    return FullCellModel(cfg)
