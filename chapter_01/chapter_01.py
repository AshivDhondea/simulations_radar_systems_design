# -*- coding: utf-8 -*-
"""
Created on 26 January 2018

@author: Ashiv Dhondea
"""
import numpy as np
import math
import RadarBasics as RB
import RadarConstants as RC

# ------------------------------------------------------------------------- #
speed_light = RC.c; # [m/s]
# ------------------------------------------------------------------------- #
def fn_Calc_PulseWidth_RadarEq(P_Tx, G_Tx, G_Rx, rho_Rx, rho_Tx, wavelength, RCS, snr, T0, radar_loss):
    """
    Implements eqn 1.57 in Mahafza book.
    """
    k_B = RC.boltzmann_constant;
    numerator = (4*math.pi)**3 * (rho_Rx**2)*(rho_Tx**2)*snr* k_B*T0*radar_loss;
    denominator = P_Tx*G_Tx*G_Rx*RCS*(wavelength**2);
    pulse_width = numerator/denominator;
    return pulse_width

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