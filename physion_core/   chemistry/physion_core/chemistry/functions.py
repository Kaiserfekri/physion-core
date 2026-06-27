import numpy as np

# -----------------------------
# Graphite (Anode)
# -----------------------------
def U_anode_graphite(soc, T_K):
    raise NotImplementedError

def dU_anode_dT_graphite(soc):
    raise NotImplementedError

def D_anode_graphite(soc, T_K):
    raise NotImplementedError


# -----------------------------
# NMC (Cathode)
# -----------------------------
def U_cathode_nmc(soc, T_K):
    raise NotImplementedError

def dU_cathode_dT_nmc(soc):
    raise NotImplementedError

def D_cathode_nmc(soc, T_K):
    raise NotImplementedError


# -----------------------------
# LFP (Cathode)
# -----------------------------
def U_cathode_lfp(soc, T_K):
    raise NotImplementedError

def dU_cathode_dT_lfp(soc):
    raise NotImplementedError

def D_cathode_lfp(soc, T_K):
    raise NotImplementedError


# -----------------------------
# LCO (Cathode)
# -----------------------------
def U_cathode_lco(soc, T_K):
    raise NotImplementedError

def dU_cathode_dT_lco(soc):
    raise NotImplementedError

def D_cathode_lco(soc, T_K):
    raise NotImplementedError


# -----------------------------
# NCA (Cathode)
# -----------------------------
def U_cathode_nca(soc, T_K):
    raise NotImplementedError

def dU_cathode_dT_nca(soc):
    raise NotImplementedError

def D_cathode_nca(soc, T_K):
    raise NotImplementedError
