# -*- coding: utf-8 -*-
"""
Created on 21 October 2017

Python functions implementing basic radar calculations

Makes extensive use of numpy arrays to ensure that scalar and array inputs
are both handled fine.

Ref:
1. Principles of Modern Radar, vol 1. aka POMR

@author: Ashiv Dhondea
"""
import math
import numpy as np

import RadarConstants as RC
# ------------------------------------------------------------------------- #
# The following functions are compatible with numpy array inputs.
# e.g allow you to convert an array of power values to decibels easily.
def fn_Power_to_dB(p):
    """
    Convert power from watts to decibels
    """
    return 10*np.log10(p); 

def fn_dB_to_Power(dB):
    """
    Convert decibels to watts
    """
    vec10 = 10.*np.ones_like(dB);
    exponents = 0.1*dB;
    return np.power(vec10,exponents)
# ------------------------------------------------------------------------- #
# Use numpy arrays for maximum flexibility wrt inputs
def fnCalculate_Wavelength_or_Frequency(speed_light,freq):
    """
    # wavelength in metres if speed_light in m/s and freq in hertz
    # frequency in hertz if speed_light in m/s and wavelenght in metres
    """
    return np.divide(speed_light,freq )
# ------------------------------------------------------------------------- #
def fnCalculate_Monostatic_RangeResolution(speed_light,bandwidth):
    """
    Calculate the monostatic range resolution
    speed_light in [m/s]
    bandwidth in [Hz]
    """
    return np.divide(speed_light,2*bandwidth)
    
def fnCalculate_Monostatic_VelocityResolution(wavelength,pulse_width):
    """
    Calculate the monostatic velocity resolution
    wavelength in [m]
    pulse_width in [s]
    """
    return np.divide(wavelength,2*pulse_width)
# ------------------------------------------------------------------------- #
def fnCalculate_TimeBandwidthProduct(pulse_width,bandwidth):
    return np.multiply(pulse_width,bandwidth)