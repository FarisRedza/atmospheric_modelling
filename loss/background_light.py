import math
import dataclasses

@dataclasses.dataclass
class BackgroundLightSim:
    wavelength: float
    sat_altitude: float
    sat_fov: float
    sat_telescope_diameter: float
    earth_albedo: float
    moon_albedo: float

    # def run_sim(self):
    #     # uplink night-time
    #     # bonato 2009
    #     h = 6.62607015e-34
    #     k = 1.380649e-23
    #     c = 2.998e8
    #     T = 293
    #     H_sun = 4.61e18 # solar spectral irradiance
    #     R_Earth = 6371e3
    #     R_Moon = 1737.4e3 # Moon radius
    #     a_Moon = 0.12 # Moon albedo
    #     d_EM = 384400e3 # Earth-Moon distance
    #     a_Earth = 0.3 # Earth albedo

    #     wavelength = 800e-9
    #     IFOV = 1 # instantaneous FOV
    #     L = 500e3 # sat altitud
    #     telescope_r = 1.5e-2 # sat telescope aperature radius
    #     Delta_wavelength = 1

    #     Sigma = IFOV**2 * L**2
    #     Omega = math.pi * telescope_r**2 / L**2

    #     N_day = a_Earth * telescope_r**2 * IFOV**2 * H_sun

    #     a = a_Moon * (R_Moon/d_EM)**2
    #     N_night = a * N_day

    #     N_0 = lambda wavelength: 2*c / (wavelength**4 * math.exp((h*c)/(wavelength*k*T))-1)

    #     N_planck = N_0(wavelength=wavelength) * Sigma * Omega * Delta_wavelength
    #     return N_day, N_night, N_planck

    # def run_sim(self):
    #     # uplink night-time
    #     # bourgoin 2013
    #     h = 6.62607015e-34
    #     k = 1.380649e-23
    #     c = 2.998e8
    #     sun_surface_temperature = 5778
    #     moon_radius = 1737.4e3
    #     earth_moon_distance = 384400e3

    #     # placeholder values
    #     atm_extinction_coeff = 0.5
    #     atm_extinction_coeff_light = 0.7
    #     average_radiance = 1e-3

    #     I = lambda v, T: (2*h*v**3) / (c**2 * math.exp((h*v)/(k*T)) - 1)

    #     frequency = c/self.wavelength
    #     photon_energy = h*frequency

    #     N_Moon = self.moon_albedo * (I(frequency, sun_surface_temperature)) / photon_energy * math.pi * moon_radius**2

    #     radius_on_earth = self.sat_altitude * math.sin(self.sat_fov/2)
    #     area_on_earth = math.pi * radius_on_earth**2
    #     satellite_earth_solid_angle = math.pi * (self.sat_telescope_diameter/2)**2 / self.sat_altitude**2
    #     N_Sun = atm_extinction_coeff * self.earth_albedo * N_Moon * (area_on_earth / earth_moon_distance**2) * satellite_earth_solid_angle

    #     N_night = atm_extinction_coeff_light * average_radiance / photon_energy * area_on_earth * satellite_earth_solid_angle

    #     N_background = N_Sun + N_night
    #     return N_background

    def run_sim(self):
        h = 6.62607015e-34
        k = 1.380649e-23
        c = 2.998e8

        a_Moon = 0.12
        R_Moon = 1737.4e3
        a_Earth = 6371e3
        d_EM = 384400e3
        v = 800e-9/c
        E_v0 = h*v
        T_Sun = 5778

        I = lambda v, T: (2*h*v**3) / (c**2 * math.exp((h*v)/(k*T)) - 1)

        N_Moon = a_Moon * I(v=v,T=T_Sun) / E_v0 * math.pi * R_Moon**2

        e = 1
        Lamda = self.sat_fov**2 * self.sat_altitude**2
        # Sigma = 
        N_Sun = e * a_Earth * N_Sun * (Lamda/d_EM**2) * Sigma

if __name__ == '__main__':
    sim = BackgroundLightSim(
        wavelength=785e-9,
        sat_altitude=550e3,
        sat_fov=0.3,
        sat_telescope_diameter=0.3,
        earth_albedo=0.3,
        moon_albedo=0.12
    )
    print(sim.run_sim())