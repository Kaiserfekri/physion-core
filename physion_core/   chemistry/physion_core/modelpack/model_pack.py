from physion_core.chemistry.nmc_graphite import NMCGraphiteChemistry
from physion_core.chemistry.lfp_graphite import LFPGraphiteChemistry
from physion_core.chemistry.lco_graphite import LCOGraphiteChemistry
from physion_core.chemistry.nca_graphite import NCAGraphiteChemistry

from physion_core.chemistry.parameter_loader import load_params
from physion_core.fullcell.fullcell_model import FullCellModel

class ModelPackConfig:
    def __init__(self,
                 chemistry_name: str = "LFP_GRAPHITE_SIMPLE",
                 params_path: str = "physion_core/params/lfp_graphite_simple.json"):
        self.chemistry_name = chemistry_name
        self.params_path = params_path

def build_chemistry(mp_cfg: ModelPackConfig):
    name = mp_cfg.chemistry_name.upper()
    params = load_params(mp_cfg.params_path)

    if name.startswith("LFP_GRAPHITE"):
        return LFPGraphiteChemistry(params)

    if name.startswith("NMC_GRAPHITE"):
        return NMCGraphiteChemistry(params)

    if name.startswith("LCO_GRAPHITE"):
        return LCOGraphiteChemistry(params)

    if name.startswith("NCA_GRAPHITE"):
        return NCAGraphiteChemistry(params)

    raise ValueError(f"Unknown chemistry: {mp_cfg.chemistry_name}")

def build_fullcell(mp_cfg: ModelPackConfig):
    chemistry = build_chemistry(mp_cfg)

    class Cfg:
        pass

    cfg = Cfg()
    cfg.chemistry = chemistry
    cfg.model_pack = mp_cfg

    return FullCellModel(cfg)
