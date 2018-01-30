# -*- coding: utf-8 -*-
"""
Created on 26 January 2018

implements Listing 1.3. MATLAB Program “fig1_13.m” 
in Mahafza radar book


@author: Ashiv Dhondea
"""
import numpy as np
import math

import RadarBasics as RB
import RadarConstants as RC

# Importing what's needed for nice plots.
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Helvetica']})
rc('text', usetex=True)
params = {'text.latex.preamble' : [r'\usepackage{amsmath}', r'\usepackage{amssymb}']}
plt.rcParams.update(params)

# ------------------------------------------------------------------------- #
speed_light = RC.c; # [m/s]
# ------------------------------------------------------------------------- #
# Radar parameters
P_Tx = 1.e6; # [W]
centre_freq = 5.6e9; #[Hz]
G_Tx_dB = 40.; # [dB]
G_Tx = RB.fn_dB_to_Power(G_Tx_dB)
G_Rx = G_Tx;
RCS = 0.1 #[m^2]
te = 300.; # [K]
nf = 5.; #[dB]

T0 = RB.fn_dB_to_Power(nf)*te
radar_loss = RB.fn_dB_to_Power(6.0);
# ------------------------------------------------------------------------- #
rho_Tx = np.array([75e3,100e3,150e3],dtype=np.float64) # [m]
snr_db = np.linspace(5.,20.,200); # SNR values from 5 dB to 20 dB 200 points

snr = RB.fn_dB_to_Power(snr_db); #10.^(0.1.*snr_db); % convert snr into base 10


wavelength = RB.fnCalculate_Wavelength_or_Frequency(speed_light,centre_freq); # [m]

def fn_Calc_PulseWidth_RadarEq(P_Tx, G_Tx, G_Rx, rho_Rx, rho_Tx, wavelength, RCS, snr, T0, radar_loss):
    """
    Implements eqn 1.57 in Mahafza book.
    """
    k_B = RC.boltzmann_constant;
    numerator = (4*math.pi)**3 * (rho_Rx**2)*(rho_Tx**2)*snr* k_B*T0*radar_loss;
    denominator = P_Tx*G_Tx*G_Rx*RCS*(wavelength**2);
    pulse_width = numerator/denominator;
    return pulse_width

pulse_width_array = np.zeros([np.shape(rho_Tx)[0],np.shape(snr)[0]],dtype=np.float64);
for i in range(0,np.shape(rho_Tx)[0]):
    for j in range(0,np.shape(snr)[0]):
        pulse_width_array[i,j] = fn_Calc_PulseWidth_RadarEq(P_Tx,G_Tx,G_Tx,rho_Tx[i],rho_Tx[i],wavelength,RCS,snr[j],T0,radar_loss)

# ------------------------------------------------------------------------- #

fig = plt.figure(1);
ax = fig.gca()
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig.suptitle(r"\textbf{Pulse width versus required SNR for three different detection range values}" ,fontsize=12);
i = 0;
plt.semilogy(snr_db,1e6*pulse_width_array[i,:],label=r"$\rho = %0.1f~\mathrm{km}$" %(rho_Tx[i]/1e3));
i = 1;
plt.semilogy(snr_db,1e6*pulse_width_array[i,:],linestyle='-.',label=r"$\rho = %0.1f~\mathrm{km}$" %(rho_Tx[i]/1e3));
i = 2;
plt.semilogy(snr_db,1e6*pulse_width_array[i,:],linestyle='--',label=r"$\rho = %0.1f~\mathrm{km}$" %(rho_Tx[i]/1e3));
plt.xlim(5,20)

ax.set_ylabel(r"Pulse width $\tau~[\mathrm{\mu s}]$")
ax.set_xlabel(r'Minimum required SNR $[\mathrm{dB}]$');
plt.legend(loc='best')
plt.grid(True,which='both',linestyle=(0,[0.7,0.7]),lw=0.4,color='black')
fig.savefig('main_chapter01_01_13.pdf',bbox_inches='tight',pad_inches=0.11,dpi=10)