# General satellite pass with Zenith offset xi

import numpy as np
from scipy import interpolate, special, integrate
from scipy.optimize import bisect
import matplotlib.pyplot as plt

G = 6.67408e-11
M = 5.972e24
R = 6371e3
s = 550e3

divFW0 = 25.7e-6 / 2  # divergence FWHM (rad)
# divFW0 = 25.7e-6  # divergence FWHM (rad)
dSAT = 0.25 # OGS telescope diameter (m)

omega = np.sqrt((G*M)/(R+s)**3)

OGScoords = np.array([0.0, 0.0, R])

Satcoords = lambda t, xi: (R+s) * np.stack([
    np.sin(xi) * np.cos(omega * t),
    np.sin(omega * t),
    np.cos(xi) * np.cos(omega * t)
], axis=-1)

L = lambda t, xi: np.linalg.norm(Satcoords(t, xi) - OGScoords, axis=-1)

Phi = lambda t, xi: np.arcsin((Satcoords(t, xi)[...,2] - OGScoords[2]) / L(t, xi))

def load_atm_interpolator(filename: str) -> interpolate.interp1d:
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    angles = data[:,0]
    values = -10*np.log10(data[:,1])
    return interpolate.interp1d(angles, values, kind='linear')

atmInterpolated = load_atm_interpolator(filename='loss/bourgoin_reproduce.csv')

# without turbulence
PhiMax = np.deg2rad(90)

def equation_for_xi(xi):
    return np.arcsin(((R+s)*np.cos(xi) - R) / L(0.0, xi)) - PhiMax

xi = bisect(equation_for_xi, 0, np.pi/2)

def elevation_zero(t):
    return Phi(t, xi)

tRange = int(np.floor(bisect(elevation_zero, 0, 500)))

divLoss = lambda R: special.erf(
    (dSAT/2) / (np.sqrt(2) * (R*divFW0) / (2*np.sqrt(2*np.log(2))))
)**2

times = np.linspace(-tRange, tRange, 500)

diffraction_dB = -10*np.log10(divLoss(L(times, xi)))
atm_dB = atmInterpolated(np.degrees(Phi(times, xi)))
total_loss_dB = diffraction_dB + atm_dB
print(np.nanmin(total_loss_dB))

plt.figure(figsize=(8,5))
plt.plot(times, total_loss_dB, label='No turbulence')
plt.xlabel('Time (s)')
plt.ylabel('Loss (dB)')
plt.ylim(30, 100)
plt.grid(True)
plt.legend()
# plt.show()

# with turbulence
Cint = lambda z: 0.00594 * (21/27)**2 * (z*1e-5)**10 * np.exp(-z/1000) + 2.7e-16 * np.exp(-z/1500) + 1.7e-14 * np.exp(-z/100)

def integrand(z):
    return Cint(z) * (1-z/s)**(5/3)

integral, _ = integrate.quad(
    func=integrand,
    a=0,
    b=s,
    limit=200,
    epsabs=1e-15,
    epsrel=1e-12
)
print(integral)

rn = lambda zeta: (1.46/np.cos(zeta) * (2*np.pi / 785e-9)**2 * integral)**(-3/5)

w = lambda R, xi: (2*np.sqrt(2) * R * 785e-9) / (np.pi * rn(xi)) / 2

divLoss = lambda R, xi: special.erf(
    (dSAT/2) / (np.sqrt(2) * np.sqrt((R*divFW0) / (2*np.sqrt(2*np.log(2)))**2 + w(R, xi)**2))
)**2

PhiMax = np.deg2rad(90)

def equation_for_xi(xi):
    return np.arcsin(((R+s)*np.cos(xi) - R) / L(0.0, xi)) - PhiMax

xi = bisect(equation_for_xi, 0, np.pi/2)

tRange = int(np.floor(bisect(elevation_zero, 0, 500)))

times = np.linspace(-tRange, tRange, 500)

diffraction_dB = -10*np.log10(divLoss(L(times, xi), xi))
atm_dB = atmInterpolated(np.degrees(Phi(times, xi)))
total_loss_dB = diffraction_dB + atm_dB
print(np.nanmin(total_loss_dB))

# plt.figure(figsize=(8,5))
plt.plot(times, total_loss_dB, label='Turbulence')
plt.legend()
plt.show()