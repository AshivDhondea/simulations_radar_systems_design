# -*- coding: utf-8 -*-
"""
Created on 21 October 2017

implements Listing 1.2. MATLAB Program “fig1_12.m” 
in Mahafza radar book

@author: Ashiv Dhondea
"""

import numpy as np

import RadarBasics as RB
import RadarConstants as RC
import RadarEquations as RE

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
P_Tx = 1.5e6; # [W]
centre_freq = 5.6e9; #[Hz]
G_Tx_dB = 45.; # [dB]
G_Tx = RB.fn_dB_to_Power(G_Tx_dB)
G_Rx = G_Tx;
RCS = 0.1 #[m^2]
bandwidth = 5e6; # [Hz]
te = 290.; # [K]
nf = 3; #[dB]
T0 = RB.fn_dB_to_Power(nf)*te
radar_loss = RB.fn_dB_to_Power(6.0);

wavelength = RB.fnCalculate_Wavelength_or_Frequency(speed_light,centre_freq);

rho_Tx = np.linspace(25e3,165e3,1000); # target range 25 -165 km, 1000 points

P_Rx1 = np.zeros([np.shape(rho_Tx)[0]],dtype=np.float64);
P_Rx2 = np.zeros([np.shape(rho_Tx)[0]],dtype=np.float64);
P_Rx3 = np.zeros([np.shape(rho_Tx)[0]],dtype=np.float64);
snr_Rx_1 = np.zeros([np.shape(rho_Tx)[0]],dtype=np.float64);
snr_Rx_2 = np.zeros([np.shape(rho_Tx)[0]],dtype=np.float64);
snr_Rx_3 = np.zeros([np.shape(rho_Tx)[0]],dtype=np.float64);


snr_Rx_2_04 = np.zeros([np.shape(rho_Tx)[0]],dtype=np.float64);
snr_Rx_3_18 = np.zeros([np.shape(rho_Tx)[0]],dtype=np.float64);

for index in range(len(rho_Tx)):
    P_Rx1[index] = RE.fnCalculate_ReceivedPower(P_Tx,G_Tx,G_Rx,rho_Tx[index],rho_Tx[index],wavelength,RCS);
    P_Rx2[index] = RE.fnCalculate_ReceivedPower(P_Tx,G_Tx,G_Rx,rho_Tx[index],rho_Tx[index],wavelength,RCS/10.);
    P_Rx3[index] = RE.fnCalculate_ReceivedPower(P_Tx,G_Tx,G_Rx,rho_Tx[index],rho_Tx[index],wavelength,RCS*10.);
    snr_Rx_1[index] = RE.fnCalculate_ReceivedSNR(P_Rx1[index],T0,bandwidth,radar_loss);
    snr_Rx_2[index] = RE.fnCalculate_ReceivedSNR(P_Rx2[index],T0,bandwidth,radar_loss)
    snr_Rx_3[index] = RE.fnCalculate_ReceivedSNR(P_Rx3[index],T0,bandwidth,radar_loss)
    
    snr_Rx_2_04[index] = RE.fnCalculate_ReceivedSNR(P_Rx1[index]*0.4,T0,bandwidth,radar_loss)
    snr_Rx_3_18[index] = RE.fnCalculate_ReceivedSNR(P_Rx1[index]*1.8,T0,bandwidth,radar_loss)

snr_Rx_1_dB = RB.fn_Power_to_dB(snr_Rx_1);
snr_Rx_2_dB = RB.fn_Power_to_dB(snr_Rx_2);
snr_Rx_3_dB = RB.fn_Power_to_dB(snr_Rx_3);

rcs1 = RB.fn_Power_to_dB(RCS);
rcs2 = RB.fn_Power_to_dB(RCS/10.)
rcs3 = RB.fn_Power_to_dB(RCS*10.)

snr_Rx_2_04_dB = RB.fn_Power_to_dB(snr_Rx_2_04);
snr_Rx_3_18_dB = RB.fn_Power_to_dB(snr_Rx_3_18);

# ------------------------------------------------------------------------- #

fig = plt.figure(1);
ax = fig.gca()
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig.suptitle(r"\textbf{SNR versus detection range for three different values of RCS}" ,fontsize=12);
plt.plot(rho_Tx/1000.,snr_Rx_3_dB,label=r"$\sigma = %f~\mathrm{dBsm}$" %rcs3)
plt.plot(rho_Tx/1000.,snr_Rx_1_dB,linestyle='-.',label=r"$\sigma = %f~\mathrm{dBsm}$" %rcs1)
plt.plot(rho_Tx/1000.,snr_Rx_2_dB,linestyle='--',label=r"$\sigma = %f~\mathrm{dBsm}$" %rcs2)
ax.set_ylabel(r"SNR $[\mathrm{dB}]$")
ax.set_xlabel(r'Detection range $[\mathrm{km}]$');
plt.legend(loc='best')
plt.grid(True,which='both',linestyle=(0,[0.7,0.7]),lw=0.4,color='black')
fig.savefig('main_chapter01_00_12a.pdf',bbox_inches='tight',pad_inches=0.11,dpi=10)

fig = plt.figure(2);
ax = fig.gca()
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig.suptitle(r"\textbf{SNR versus detection range for three different values of radar peak power}" ,fontsize=12);
plt.plot(rho_Tx/1000.,snr_Rx_3_18_dB,label=r"$P_\text{Tx} = 2.16~\mathrm{MW}$")
plt.plot(rho_Tx/1000.,snr_Rx_1_dB,linestyle='-.',label=r"$P_\text{Tx} = 1.5~\mathrm{MW}$")
plt.plot(rho_Tx/1000.,snr_Rx_2_04_dB,linestyle='--',label=r"$P_\text{Tx} = 0.6~\mathrm{MW}$" )
ax.set_ylabel(r"SNR $[\mathrm{dB}]$")
ax.set_xlabel(r'Detection range $[\mathrm{km}]$');
plt.legend(loc='best')
plt.grid(True,which='both',linestyle=(0,[0.7,0.7]),lw=0.4,color='black')
fig.savefig('main_chapter01_00_12b.pdf',bbox_inches='tight',pad_inches=0.11,dpi=10)
