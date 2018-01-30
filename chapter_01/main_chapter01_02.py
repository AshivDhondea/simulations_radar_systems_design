# -*- coding: utf-8 -*-
"""
Created on 26 January 2018

Listing 1.4. MATLAB Program ref_snr.m
in Mahafza radar book

@author: Ashiv Dhondea
"""

import RadarBasics as RB

# ------------------------------------------------------------------------- #
Rref = 86e3; # reference range
tau_ref = 0.1e-6; # reference pulse width
SNRref = 20.; # Ref SNR in dB
snrref = RB.fn_dB_to_Power(SNRref)

Sigmaref = 0.1; # ref RCS in m^2
Lossp_dB = 2; # processing loss in dB
lossp = RB.fn_dB_to_Power(Lossp_dB);
# Enter desired value
tau = tau_ref;
R = 120e3;
rangeratio = (Rref / R)**4;
Sigma = 0.2;
# Implement Eq. (1.60)
snr = snrref * (tau / tau_ref) * (1. / lossp) * (Sigma / Sigmaref) * rangeratio;
snr = RB.fn_Power_to_dB(snr)
print('SNR at 120 km =  %.1f dB' %snr)