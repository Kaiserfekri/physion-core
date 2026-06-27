import numpy as np

def U_anode_graphite(soc, T_K):
    # OCV واقعی گرافیت باید از داده بارگذاری شود
    raise NotImplementedError

def U_cathode_nmc(soc, T_K):
    # OCV واقعی NMC باید از داده بارگذاری شود
    raise NotImplementedError

def dU_anode_dT_graphite(soc):
    # dU/dT گرافیت از مقاله/داده
    raise NotImplementedError

def dU_cathode_dT_nmc(soc):
    # dU/dT NMC از مقاله/داده
    raise NotImplementedError

def D_anode_graphite(soc, T_K):
    # D(soc,T) گرافیت
    raise NotImplementedError

def D_cathode_nmc(soc, T_K):
    # D(soc,T) NMC
    raise NotImplementedError
