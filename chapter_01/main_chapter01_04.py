# -*- coding: utf-8 -*-
"""
Created on 26 January 2018

Chapter 1 example on power aperture product
Mahafza book

@author: Ashiv Dhondea
"""
import math
import numpy as np

import RadarBasics as RB
import RadarConstants as RC

# ------------------------------------------------------------------------- #
def fn_Calc_SearchVolume(az,el):
    """
    az,el in deg
    eqn 1.61 in Mahafza book
    """
    return az*el/(57.296**2) # steradians
    
def fn_power_aperture(snr,tsc,rcs,rho,te,nf,loss,az_angle,el_angle):
    """
    implements Listing 1.5. MATLAB Function power_aperture.m
    % This program implements Eq. (1.67)

    """
    Tsc = RB.fn_Power_to_dB(tsc); # convert Tsc into dB
    Sigma = RB.fn_Power_to_dB(rcs);# convert sigma to dB
    four_pi = RB.fn_Power_to_dB(4.0 * math.pi); # (4pi) in dB
    k_B = RC.boltzmann_constant;
    k_db = RB.fn_Power_to_dB(k_B); # Boltzman’s constant in dB
    Te = RB.fn_Power_to_dB(te) #noise temp. in dB
    range_pwr4_db = RB.fn_Power_to_dB(rho**4); # target range^4 in dB
    omega = fn_Calc_SearchVolume(az_angle,el_angle) # compute search volume in steradians
    Omega = RB.fn_Power_to_dB(omega)# search volume in dB
    # implement Eq. (1.67)
    PAP = snr + four_pi + k_db + Te + nf + loss + range_pwr4_db + Omega - Sigma - Tsc;
    return PAP
    
    

# ------------------------------------------------------------------------- #
T_sc = 2.; # [s]
noise_fig_dB = 8. ;# [dB]

losses_dB = 6.;
rho=75e3; # [m]
snr_req_dB = 20.; # [dB]

T_e = 290; # [K]
rcs = 3.162; # [m^2]

az = 180.;
el = 135.;
PAP = fn_power_aperture(snr_req_dB,T_sc,rcs,rho,T_e,noise_fig_dB,losses_dB,az,el)
print('power aperture product = %.1f dB' %PAP)