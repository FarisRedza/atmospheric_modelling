# General satellite pass with Zenith offset xi
import os
import sys
import pathlib
import typing

import numpy as np
import scipy.interpolate
import scipy.special
import scipy.optimize
import scipy.integrate
import matplotlib.pyplot as plt

sys.path.append(str(pathlib.Path.cwd()))
import loss.libRadtranPy.libradtranpy as libradtranpy

try:
    os.environ['LIBRADTRANDIR']
except:
    os.environ['LIBRADTRANDIR'] = str(pathlib.Path(
        pathlib.Path.cwd(),
        'libRadtran-2.0.6'
    ))
else:
    print('Using system value for LIBRADTRANDIR')

G_CONST = 6.67408e-11
EARTH_MASS = 5.972e24
EARTH_RADIUS = 6371e3

def load_atm_interpolator(filename: str) -> scipy.interpolate.interp1d:
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    angles = data[:,0]
    values = -10*np.log10(data[:,1])
    return scipy.interpolate.interp1d(angles, values, kind='linear')

def atm_interpolator(angles, transmittance) -> scipy.interpolate.interp1d:
    return scipy.interpolate.interp1d(
        x=angles,
        y=-10*np.log10(transmittance),
        kind='linear'
    )

def equation_for_xi(zenith_offset, ogs_altitude, elevation_max):
    return np.arcsin(
        ((EARTH_RADIUS+sat_altitude)*np.cos(zenith_offset) - EARTH_RADIUS - ogs_altitude) / transmit_distance(
            time=0.0,
            zenith_offset=zenith_offset
        )
    ) - elevation_max

def elevation_zero(time, zenith_offset, sat_altitude):
    return elevation(
        sat_altitude=sat_altitude,
        time=time,
        zenith_offset=zenith_offset
    )

def calc_diffraction_loss(
        distance,
        zenith_offset,
        wavelength: int | float | None = None,
        beam_waist: typing.Callable | None = None
):
    if wavelength and beam_waist:
        return scipy.special.erf(
            (sat_telescope_diameter/2) / (np.sqrt(2) * np.sqrt(((distance*divergence_FWHM) / (2*np.sqrt(2*np.log(2))))**2 + beam_waist(wavelength, distance, zenith_offset)**2))
        )**2
    elif wavelength or beam_waist:
        raise RuntimeError('Must provide wavelength and beam_waist for turbulence')
    else:
        return scipy.special.erf(
            (sat_telescope_diameter/2) / (np.sqrt(2) * (distance*divergence_FWHM) / (2*np.sqrt(2*np.log(2))))
        )**2 

if __name__ == '__main__':
    A = 1.7e-13
    wind_speed = 21
    # qeyssat_hogs
    sat_altitude = 550e3
    ogs_altitude = 0
    wavelength = 785e-9

    divergence_FWHM = 25.7e-6 / 2  # divergence FWHM (rad)
    sat_telescope_diameter = 0.25
    
    # # micius_ngari
    # sat_altitude = 500e3
    # ogs_altitude = 5e3
    # wavelength = 780e-9

    # divergence_FWHM = 34e-6  # divergence FWHM (rad)
    # sat_telescope_diameter = 0.3

    omega = np.sqrt((G_CONST*EARTH_MASS)/(EARTH_RADIUS+sat_altitude)**3)

    ogs_coords = np.array([0.0, 0.0, EARTH_RADIUS + ogs_altitude])

    sat_coords = lambda sat_altitude, time, zenith_offset: (EARTH_RADIUS+sat_altitude) * np.stack([
        np.sin(zenith_offset) * np.cos(omega * time),
        np.sin(omega * time),
        np.cos(zenith_offset) * np.cos(omega * time)
    ], axis=-1)

    transmit_distance = lambda time, zenith_offset: np.linalg.norm(
        sat_coords(
            sat_altitude=sat_altitude,
            time=time,
            zenith_offset=zenith_offset
        ) - ogs_coords,
        axis=-1
    )

    elevation = lambda sat_altitude, time, zenith_offset: np.arcsin(
        (sat_coords(
            sat_altitude=sat_altitude,
            time=time,
            zenith_offset=zenith_offset
        )[...,2] - ogs_coords[2]) / transmit_distance(
            time=time,
            zenith_offset=zenith_offset
        )
    )

    elevation_max = np.deg2rad(90)

    zenith_offset = scipy.optimize.bisect(
        f=equation_for_xi,
        a=0,
        b=np.pi/2,
        args=(ogs_altitude, elevation_max,)
    )

    t_root_tuple = scipy.optimize.bisect(
        f=elevation_zero,
        a=0,
        b=500,
        args=(zenith_offset,sat_altitude)
    )
    t_root = t_root_tuple[0] if isinstance(t_root_tuple, tuple) else t_root_tuple
    t_range = int(np.floor(t_root))

    times = np.linspace(-t_range, t_range, 500)

    diffraction_loss = calc_diffraction_loss(
        distance=transmit_distance(time=times, zenith_offset=zenith_offset),
        zenith_offset=zenith_offset
    )

    diffraction_dB = -10*np.log10(diffraction_loss)

    # atm_interpolated = load_atm_interpolator(filename='loss/bourgoin_reproduce.csv')
    # atm_dB = atm_interpolated(np.degrees(elevation(
    #     sat_altitude=sat_altitude,
    #     time=times,
    #     zenith_offset=zenith_offset
    # )))
    atm_sim = libradtranpy.Simulation(
        aerosol=libradtranpy.Aerosol(
            aerosol_default=True,
            # aerosol_season=libradtranpy.AerosolSeason.SPRING_SUMMER,
            aerosol_visibility=5,
            aerosol_haze=libradtranpy.AerosolHaze.RURAL,
            aerosol_vulcan=libradtranpy.AerosolVulcan.BACKGROUND_AEROSOLS,
            aerosol_species_file=libradtranpy.AerosolSpecies.CONTINENTAL_CLEAN,
            # aerosol_species_library=libradtranpy.AerosolSpeciesLibrary.OPAC
        ),
        general_atm=libradtranpy.GeneralAtm(
            # no_absorption=True,
            # no_scattering=True,
            # zout_interpolate=True,
            # reverse_atmosphere=True
        ),
        mol_atm=libradtranpy.MolAtm(
            atmosphere_file=libradtranpy.Atmosphere.MIDLATTITUDESUMMER,
            # mol_abs_param=(libradtranpy.CKScheme.REPTRAN, 'coarse'),
            mol_modify=['CO2 7.84e21 CM_2'],
            # crs_model=(libradtranpy.MolID.RAYLEIGH, libradtranpy.CRSModel.BODHAINE)
        ),
        geometry=libradtranpy.Geometry(
            # phi=0,
            # umu=-1,
            # latitude='N 56.405',
            # longitude='W 3.183',
            # time='2025 3 18 13, 5 37.8075'
        ),
        surface=libradtranpy.Surface(
            altitude=0,
            albedo=0.3,
        ),
        spectral=libradtranpy.Spectral(
            wavelength=[785, 785]
        ),
        solver=libradtranpy.Solver(
            rte_solver=libradtranpy.RTESolver.DISORT
        ),
        output=libradtranpy.Output(
            quiet=True,
            # verbose=True,
            output_user='lambda edir',
            output_quantity=libradtranpy.OutputQuantity.TRANSMITTANCE,
            # output_process=libradtranpy.OutputProcess.PER_NM,
            # zout=ZOut.TOA
        )
    )
    atm_theta = []
    atm_edir = []
    for angle in range(0, 91, 1):
        atm_sim.geometry.sza = 90 - angle
        result = atm_sim.run_uvscpec()
        result_wavelength, result_edir, *_ = map(float, result.split())
        atm_theta.append(angle)
        atm_edir.append(result_edir)
    
    atm_interpolated = atm_interpolator(
        angles=atm_theta,
        transmittance=atm_edir
    )
    atm_dB = atm_interpolated(
        np.degrees(elevation(
            time=times,
            zenith_offset=zenith_offset,
            sat_altitude=sat_altitude
        ))
    )
    print(atm_dB)
    print(atm_sim.generate_uvspec_input())

    total_loss_dB = diffraction_dB + atm_dB

    plt.figure(figsize=(8,5))
    plt.plot(times, total_loss_dB, label='No turbulence')
    plt.plot(times, atm_dB, label='No turbulence - atm')
    plt.xlabel('Time (s)')
    plt.ylabel('Loss (dB)')
    plt.xlim(-300, 300)
    plt.ylim(0, 100)
    plt.grid(True)
    plt.legend()
    # plt.show()

    # with turbulence
    refractive_index_structure_constant = lambda z, A, v: 0.00594 * (v/27)**2 * (z*1e-5)**10 * np.exp(-z/1000) + 2.7e-16 * np.exp(-z/1500) + A * np.exp(-z/100)

    def integrand(z, sat_altitude):
        return refractive_index_structure_constant(z=z, A=A, v=wind_speed) * (1-z/sat_altitude)**(5/3)

    integral, _ = scipy.integrate.quad(
        func=integrand,
        a=ogs_altitude,
        b=sat_altitude,
        args=(sat_altitude,),
        limit=200,
        epsabs=1e-15,
        epsrel=1e-12
    )

    transverse_coherence_length = lambda wavelength, zenith_offset: (1.46/np.cos(zenith_offset) * (2*np.pi / wavelength)**2 * integral)**(-3/5)

    beam_waist = lambda wavelength, distance, zenith_offset: (2*np.sqrt(2) * distance * wavelength) / (np.pi * transverse_coherence_length(wavelength, zenith_offset))
    diffraction_loss = calc_diffraction_loss(
        distance=transmit_distance(time=times, zenith_offset=zenith_offset),
        zenith_offset=zenith_offset,
        wavelength=wavelength,
        beam_waist=beam_waist
    )
    diffraction_dB = -10*np.log10(diffraction_loss)
    total_loss_dB = diffraction_dB + atm_dB

    plt.plot(times, total_loss_dB, label='Turbulence')
    plt.xlabel('Time (s)')
    plt.ylabel('Loss (dB)')
    plt.ylim(30, 100)
    plt.grid(True)
    plt.legend()
    plt.show()