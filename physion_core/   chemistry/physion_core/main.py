from physion_core.modelpack import ModelPackConfig, build_fullcell
from physion_core.chemistry.functions import set_user_ocv_lfp

if __name__ == "__main__":
    mp_simple = ModelPackConfig(
        chemistry_name="LFP_GRAPHITE_SIMPLE",
        params_path="physion_core/params/lfp_graphite_simple.json"
    )
    model_simple = build_fullcell(mp_simple)
    model_simple.step(dt=1.0, current_density_A_m2=10.0)
    print("Simple mode:", model_simple.summary())
    assert model_simple.state.time_s == 1.0

    soc_data = [0.0, 0.5, 1.0]
    U_data = [3.2, 3.4, 3.6]
    set_user_ocv_lfp(soc_data, U_data)

    mp_user = ModelPackConfig(
        chemistry_name="LFP_GRAPHITE_USER",
        params_path="physion_core/params/lfp_graphite_user.json"
    )
    model_user = build_fullcell(mp_user)
    model_user.step(dt=1.0, current_density_A_m2=10.0)
    print("User mode:", model_user.summary())
    assert model_user.state.time_s == 1.0

    mp_ind = ModelPackConfig(
        chemistry_name="LFP_GRAPHITE_INDUSTRIAL",
        params_path="physion_core/params/lfp_graphite_industrial.json"
    )
    model_ind = build_fullcell(mp_ind)
    model_ind.step(dt=1.0, current_density_A_m2=10.0)
    print("Industrial mode:", model_ind.summary())
    assert model_ind.state.time_s == 1.0
