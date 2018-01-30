# -*- coding: utf-8 -*-
"""
Created on 21 October 2017

@author: Ashiv Dhondea
"""
import math
import numpy as np

import RadarBasics as RB
import RadarConstants as RC

# ------------------------------------------------------------------------- #
def fnCalculate_ReceivedPower(P_Tx,G_Tx,G_Rx,rho_Rx,rho_Tx,wavelength,RCS):
    """
    Calculate the received power at the bistatic radar receiver.
    
    equation 5 in " PERFORMANCE ASSESSMENT OF THE MULTIBEAM RADAR
    SENSOR BIRALES FOR SPACE SURVEILLANCE AND TRACKING"

    Note: ensure that the distances rho_Rx,rho_Tx,wavelength are converted to
    metres before passing into this function.
    
    Created on: 26 May 2017
    """
    denominator = (4*math.pi)**3 * (rho_Rx**2)*(rho_Tx**2);
    numerator = P_Tx*G_Tx*G_Rx*RCS*(wavelength**2);
    P_Rx = numerator/denominator;
    return P_Rx
    
def fnCalculate_ReceivedSNR(P_Rx,T0,bandwidth,radar_loss):
    """
    Calculate the SNR at the bistatic radar receiver.
    
    equation 7 in " PERFORMANCE ASSESSMENT OF THE MULTIBEAM RADAR
    SENSOR BIRALES FOR SPACE SURVEILLANCE AND TRACKING"
    
    Note: output is not in decibels.
    
    Created on: 26 May 2017
    Edited:
    21.10.17: included the term radar_loss, symbol L in eqn 1.56 in Mahafza radar book
    """
    k_B = RC.boltzmann_constant;
    snr = P_Rx/(k_B*bandwidth*T0*radar_loss);
    return snr
    

