from physion_core.chemistry import functions as f

FUNCTION_REGISTRY = {
    # Anode
    "U_anode_graphite": f.U_anode_graphite,
    "dU_anode_dT_graphite": f.dU_anode_dT_graphite,
    "D_anode_graphite": f.D_anode_graphite,

    # LFP
    "U_cathode_lfp_simple": f.U_cathode_lfp_simple,
    "U_cathode_lfp_user": f.U_cathode_lfp_user,
    "U_cathode_lfp_industrial": f.U_cathode_lfp_industrial,
    "dU_cathode_dT_lfp": f.dU_cathode_dT_lfp,
    "D_cathode_lfp": f.D_cathode_lfp,

    # NMC
    "U_cathode_nmc_simple": f.U_cathode_nmc_simple,
    "U_cathode_nmc_user": f.U_cathode_nmc_user,
    "U_cathode_nmc_industrial": f.U_cathode_nmc_industrial,
    "dU_cathode_dT_nmc": f.dU_cathode_dT_nmc,
    "D_cathode_nmc": f.D_cathode_nmc,

    # LCO
    "U_cathode_lco_simple": f.U_cathode_lco_simple,
    "U_cathode_lco_user": f.U_cathode_lco_user,
    "U_cathode_lco_industrial": f.U_cathode_lco_industrial,
    "dU_cathode_dT_lco": f.dU_cathode_dT_lco,
    "D_cathode_lco": f.D_cathode_lco,

    # NCA
    "U_cathode_nca_simple": f.U_cathode_nca_simple,
    "U_cathode_nca_user": f.U_cathode_nca_user,
    "U_cathode_nca_industrial": f.U_cathode_nca_industrial,
    "dU_cathode_dT_nca": f.dU_cathode_dT_nca,
    "D_cathode_nca": f.D_cathode_nca,
}
