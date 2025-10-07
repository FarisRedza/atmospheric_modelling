import os
import sys
import pathlib

import numpy as np
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

atm_sim = libradtranpy.Simulation(
    spectral=libradtranpy.Spectral(
        wavelength=[405],
        source=libradtranpy.Source.SOLAR
    ),
    aerosol=libradtranpy.Aerosol(
        aerosol_default=True,
        aerosol_season=libradtranpy.AerosolSeason.SPRING_SUMMER,
        aerosol_visibility=6,
        aerosol_haze=libradtranpy.AerosolHaze.RURAL,
        aerosol_vulcan=libradtranpy.AerosolVulcan.BACKGROUND_AEROSOLS
    ),
    mol_atm=libradtranpy.MolAtm(
        atmosphere_file=libradtranpy.Atmosphere.MIDLATITUDE_SUMMER
    ),
    geometry=libradtranpy.Geometry(
        sza=0
    ),
    surface=libradtranpy.Surface(
        altitude=0
    ),
    output=libradtranpy.Output(
        output_user='lambda edir',
        output_quantity=libradtranpy.OutputQuantity.REFLECTIVITY
    )
)


min_elevation = 30
max_elevation = 90
angles = list(range(min_elevation, max_elevation, 5))

ogs_altitude = 5

atm_sim_result = atm_sim.run_transmission_against_elevation()
atm_loss = atm_sim_result.transmission_as_dB()
horizon_angle = [float(np.deg2rad(angle)) for angle in atm_sim_result.elevations]

plt.plot(atm_sim_result.elevations, atm_sim_result.transmissions)
plt.grid()
plt.show()