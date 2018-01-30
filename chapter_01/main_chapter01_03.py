# -*- coding: utf-8 -*-
"""
Created on 26 January 2018

Listing 1.5 and 1.6
in Mahafza radar book
creates fig 1-16

@author: Ashiv Dhondea
"""
import math
import numpy as np

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
tsc = 2.5; # Scan time is 2.5 seconds
rcs = 0.1; # radar cross section in m squared
te = 900.0; # effective noise temperature in Kelvins
snr = 15; # desired SNR in dB
nf = 6.0; #noise figure in dB
loss = 7.0; # radar losses in dB

az_angle = 2.; # search volume azimuth extent in degrees
el_angle = 2.; # search volume elevation extent in degrees
rho_Tx = np.linspace(20e3,250e3,1000); # range to target 20 Km 250 Km, 1000 points


rcs_array = np.array([rcs/10,rcs,rcs*10.],dtype=np.float64);
rcs_array_db = RB.fn_Power_to_dB(rcs_array)
power_aperture = np.zeros([np.shape(rcs_array)[0],np.shape(rho_Tx)[0]],dtype=np.float64);
for i_rho in range(0,np.shape(rho_Tx)[0]):
    for i_rcs in range(0,np.shape(rcs_array)[0]):
        power_aperture[i_rcs,i_rho] = fn_power_aperture(snr,tsc,rcs_array[i_rcs],rho_Tx[i_rho],te,nf,loss,az_angle,el_angle);
    

# ------------------------------------------------------------------------- #
fig = plt.figure(1);
ax = fig.gca()
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig.suptitle(r"\textbf{Power aperture product versus detection range}" ,fontsize=12);
i = 0;
plt.plot(rho_Tx/1e3,power_aperture[i,:],label=r"$\sigma = %0.1f~\mathrm{dBsm}$" %rcs_array_db[i]);
i = 1;
plt.plot(rho_Tx/1e3,power_aperture[i,:],linestyle='-.',label=r"$\sigma = %0.1f~\mathrm{dBsm}$" %rcs_array_db[i]);
i = 2;
plt.plot(rho_Tx/1e3,power_aperture[i,:],linestyle='--',label=r"$\sigma = %0.1f~\mathrm{dBsm}$" %rcs_array_db[i]);

ax.set_ylabel(r"Power aperture product $[\mathrm{dB}]$")
ax.set_xlabel(r'Detection range $[\mathrm{km}]$');
plt.legend(loc='best')
plt.grid(True,which='both',linestyle=(0,[0.7,0.7]),lw=0.4,color='black')
fig.savefig('main_chapter01_03_16a.pdf',bbox_inches='tight',pad_inches=0.11,dpi=10)
# ------------------------------------------------------------------------- #

wavelength = 0.03; # wavelength in meters
G = 45; # antenna gain in dB
ae = np.linspace(1.,25.,1000);# aperture size 1 to 25 meter squared, 1000 points
Ae = RB.fn_Power_to_dB(ae)
rho = 250e3; # range of interest is 250 Km
pap = np.zeros([np.shape(rcs_array)[0]],dtype=np.float64);
Pave = np.zeros([np.shape(rcs_array)[0],np.shape(Ae)[0]],dtype=np.float64);

for i in range(0,np.shape(pap)[0]):
    pap[i] = fn_power_aperture(snr,tsc,rcs_array[i],rho,te,nf,loss,az_angle,el_angle);
    for j in range(0,np.shape(Ae)[0]):
        Pave[i,j] = pap[i] - Ae[j];
# ------------------------------------------------------------------------- #
fig = plt.figure(2);
ax = fig.gca()
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig.suptitle(r"\textbf{Radar average power versus power aperture product}" ,fontsize=12);
i = 0;
plt.plot(ae,Pave[i,:],label=r"$\sigma = %0.1f~\mathrm{dBsm}$" %rcs_array_db[i]);
i = 1;
plt.plot(ae,Pave[i,:],linestyle='-.',label=r"$\sigma = %0.1f~\mathrm{dBsm}$" %rcs_array_db[i]);
i = 2;
plt.plot(ae,Pave[i,:],linestyle='--',label=r"$\sigma = %0.1f~\mathrm{dBsm}$" %rcs_array_db[i]);

ax.set_ylabel(r"$P_{\text{av}}~[\mathrm{dB}]$")
ax.set_xlabel(r'Aperture size $[\mathrm{m^2}]$');
plt.legend(loc='best')
plt.grid(True,which='both',linestyle=(0,[0.7,0.7]),lw=0.4,color='black')
fig.savefig('main_chapter01_03_16b.pdf',bbox_inches='tight',pad_inches=0.11,dpi=10)


