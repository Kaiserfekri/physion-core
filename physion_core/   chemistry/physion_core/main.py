from physion_core.modelpack import ModelPackConfig, build_fullcell
from physion_core.chemistry.functions import set_user_ocv_lfp

class DummyCfg:
    def __init__(self, mp_cfg):
        self.model_pack = mp_cfg
        self.chemistry = None

if __name__ == "__main__":
    # Simple mode
    mp_simple = ModelPackConfig(
        chemistry_name="LFP_GRAPHITE_SIMPLE",
        params_path="physion_core/params/lfp_graphite_simple.json"
    )
    cfg_simple = DummyCfg(mp_simple)
    model_simple = build_fullcell(cfg_simple)
    print("Simple mode built:", model_simple is not None)

    # User mode (با دادهٔ فرضی)
    soc_data = [0.0, 0.5, 1.0]
    U_data = [3.2, 3.4, 3.6]
    set_user_ocv_lfp(soc_data, U_data)

    mp_user = ModelPackConfig(
        chemistry_name="LFP_GRAPHITE_USER",
        params_path="physion_core/params/lfp_graphite_user.json"
    )
    cfg_user = DummyCfg(mp_user)
    model_user = build_fullcell(cfg_user)
    print("User mode built:", model_user is not None)

    # Industrial mode
    mp_ind = ModelPackConfig(
        chemistry_name="LFP_GRAPHITE_INDUSTRIAL",
        params_path="physion_core/params/lfp_graphite_industrial.json"
    )
    cfg_ind = DummyCfg(mp_ind)
    model_ind = build_fullcell(cfg_ind)
    print("Industrial mode built:", model_ind is not None)
