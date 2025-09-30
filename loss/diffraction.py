import typing
import dataclasses

import numpy as np
import scipy.interpolate
import scipy.special
import scipy.optimize
import scipy.integrate

G_CONST = 6.67408e-11
EARTH_MASS = 5.972e24
EARTH_RADIUS = 6371e3

def equation_for_xi(zenith_offset, transmit_distance, sat_altitude, ogs_altitude, elevation_max):
    return np.arcsin(
        ((EARTH_RADIUS+sat_altitude)*np.cos(zenith_offset) - EARTH_RADIUS - ogs_altitude) / transmit_distance(
            time=0.0,
            zenith_offset=zenith_offset
        )
    ) - elevation_max

def elevation_zero(time, elevation, zenith_offset, sat_altitude):
    return elevation(
        sat_altitude=sat_altitude,
        time=time,
        zenith_offset=zenith_offset
    )

def calc_diffraction_loss(
        sat_telescope_diameter,
        divergence_FWHM,
        distance,
        zenith_offset,
        wavelength: typing.Optional[int | float] = None,
        beam_waist: typing.Optional[typing.Callable] = None,
) -> np.typing.NDArray[np.int64]:
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

@dataclasses.dataclass
class DiffractionSimResult:
    times: np.typing.NDArray[np.int64]
    transmissions: np.typing.NDArray[np.int64]
    zenith_offset: float
    elevations: np.typing.NDArray[np.int64]

@dataclasses.dataclass
class DiffractionSim:
    sat_altitude: float
    ogs_altitude: float
    wavelength: float
    divergence_FWHM: float
    sat_telescope_diameter: float
    turbulence: bool
    ground_level_turbulence_strength: float = 1.7e-14
    wind_speed: float = 21.0
    
    def run_sim(self) -> DiffractionSimResult:
        omega = np.sqrt((G_CONST * EARTH_MASS) / (EARTH_RADIUS + self.sat_altitude)**3)
        
        ogs_coords = np.array([0.0, 0.0, EARTH_RADIUS + self.ogs_altitude])

        sat_coords = lambda sat_altitude, time, zenith_offset: (EARTH_RADIUS+sat_altitude) * np.stack([
            np.sin(zenith_offset) * np.cos(omega * time),
            np.sin(omega * time),
            np.cos(zenith_offset) * np.cos(omega * time)
        ], axis=-1)

        transmit_distance = lambda time, zenith_offset: np.linalg.norm(
            sat_coords(
                sat_altitude=self.sat_altitude,
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
            args=(
                transmit_distance,
                self.sat_altitude,
                self.ogs_altitude,
                elevation_max
            )
        )

        t_root_tuple = scipy.optimize.bisect(
            f=elevation_zero,
            a=0,
            b=500,
            args=(elevation, zenith_offset, self.sat_altitude)
        )
        t_root = t_root_tuple[0] if isinstance(t_root_tuple, tuple) else t_root_tuple
        t_range = int(np.floor(t_root))

        times = np.linspace(-t_range, t_range, 500)

        if self.turbulence:
            refractive_index_structure_constant = lambda z, A, v: 0.00594 * (v/27)**2 * (z*1e-5)**10 * np.exp(-z/1000) + 2.7e-16 * np.exp(-z/1500) + A * np.exp(-z/100)
            def integrand(z, sat_altitude):
                return refractive_index_structure_constant(
                    z=z,
                    A=self.ground_level_turbulence_strength,
                    v=self.wind_speed
                ) * (1-z/sat_altitude)**(5/3)

            integral, _ = scipy.integrate.quad(
                func=integrand,
                a=self.ogs_altitude,
                b=self.sat_altitude,
                args=(self.sat_altitude,),
                limit=200,
                epsabs=1e-15,
                epsrel=1e-12
            )
            transverse_coherence_length = lambda wavelength, zenith_offset: (1.46/np.cos(zenith_offset) * (2*np.pi / wavelength)**2 * integral)**(-3/5)
            beam_waist = lambda wavelength, distance, zenith_offset: (2*np.sqrt(2) * distance * wavelength) / (np.pi * transverse_coherence_length(wavelength, zenith_offset))
            diffraction_loss = calc_diffraction_loss(
                sat_telescope_diameter=self.sat_telescope_diameter,
                divergence_FWHM=self.divergence_FWHM,
                distance=transmit_distance(time=times, zenith_offset=zenith_offset),
                zenith_offset=zenith_offset,
                wavelength=self.wavelength,
                beam_waist=beam_waist
            )
        else:
            diffraction_loss = calc_diffraction_loss(
                sat_telescope_diameter=self.sat_telescope_diameter,
                divergence_FWHM=self.divergence_FWHM,
                distance=transmit_distance(time=times, zenith_offset=zenith_offset),
                zenith_offset=zenith_offset
            )
        elevations: np.typing.NDArray[np.int64] = np.degrees(
            elevation(
                time=times,
                zenith_offset=zenith_offset,
                sat_altitude=self.sat_altitude
            )
        )

        # diffraction_dB = -10*np.log10(diffraction_loss)
        return DiffractionSimResult(
            times=times,
            transmissions=diffraction_loss,
            zenith_offset=zenith_offset,
            elevations=elevations
        )
