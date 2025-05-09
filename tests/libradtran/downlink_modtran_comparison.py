import sys
import os
import pathlib
import csv

import matplotlib
import matplotlib.pyplot

sys.path.append(str(pathlib.Path.cwd()))
from atm_modelling.libRadtranPy.libradtranpy import *

try:
    os.environ['LIBRADTRANDIR']
except:
    os.environ['LIBRADTRANDIR'] = str(pathlib.Path(
        pathlib.Path.cwd(),
        'libRadtran-2.0.6'
    ))
else:
    print('Using system value for LIBRADTRANDIR')

headless = False
try:
    matplotlib.use('GTK4Agg')
except:
    headless = True
    fig = matplotlib.pyplot.figure()

matplotlib.use('GTK4Agg')

elevation = range(0, 91, 1)

downlink_sim = Simulation(
    aerosol=Aerosol(
        aerosol_default=True,
        # aerosol_season=AerosolSeason.SPRING_SUMMER,
        # aerosol_visibility=50,
        # aerosol_haze=AerosolHaze.RURAL,
        # aerosol_vulcan=AerosolVulcan.BACKGROUND_AEROSOLS,
        # aerosol_species_file=AerosolSpecies.CONTINENTAL_CLEAN,
        # aerosol_species_library=AerosolSpeciesLibrary.OPAC
    ),
    general_atm=GeneralAtm(
        # no_absorption=True,
        # no_scattering=True,
        # zout_interpolate=True,
        # reverse_atmosphere=True
    ),
    mol_atm=MolAtm(
        # atmosphere_file=Atmosphere.MIDLATTITUDESUMMER,
        # mol_abs_param=(CKScheme.REPTRAN, 'coarse'),
        # mol_modify=['O3 200 DU', 'H2O 20 MM'],
        # crs_model=(MolID.RAYLEIGH, CRSModel.BODHAINE)
    ),
    geometry=Geometry(
        # phi=0,
        # umu=-1,
        # latitude='N 56.405',
        # longitude='W 3.183',
        # time='2025 3 18 13, 5 37.8075'
    ),
    surface=Surface(
        # altitude=0,
        albedo=1,
    ),
    spectral=Spectral(
        wavelength=[785, 785]
    ),
    solver=Solver(
        rte_solver=RTESolver.DISORT
    ),
    output=Output(
        quiet=True,
        # verbose=True,
        output_user='lambda edir',
        output_quantity=OutputQuantity.REFLECTIVITY,
        # output_process=OutputProcess.PER_NM,
        # zout=ZOut.TOA
    )
)
libradtran_theta = []
libradtran_edir = []
for angle in elevation:
    sza = 90 - angle
    downlink_sim.geometry.sza = sza
    result = downlink_sim.run_uvscpec()
    wavelength, edir, *_ = map(float, result.split())
    libradtran_theta.append(float(angle))
    libradtran_edir.append(float(edir))
matplotlib.pyplot.plot(
    libradtran_theta,
    libradtran_edir,
    label='libRadtran'
)

# SatQuMA MODTRAN data
satquma_file = 'MODTRAN_wl_785.0-850.0-5.0nm_h1_500.0km_h0_0.0km_elevation_data.csv'
satquma_file_path = pathlib.Path(
    pathlib.Path.cwd(),
    'SatQuMA',
    'channel',
    'atmosphere',
    satquma_file
)
satquma_theta = []
satquma_edir = []
with open(file=satquma_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        satquma_theta.append(float(row['# theta (deg)']))
        satquma_edir.append(float(row['785 nm']))
matplotlib.pyplot.plot(
    satquma_theta,
    satquma_edir,
    label='SatQuMA'
)

matplotlib.pyplot.legend()
matplotlib.pyplot.xlabel('Elevation Angle (°)')
matplotlib.pyplot.ylabel('Transmittance')
matplotlib.pyplot.title('785 nm Downlink')
matplotlib.pyplot.ylim([0, 1])
matplotlib.pyplot.xlim([0, 90])
matplotlib.pyplot.grid(True)

if headless == True:
    fig.savefig(
        'bourgoin_reproduce.png',
        dpi='figure',
        bbox_inches='tight'
    )
else:
    matplotlib.pyplot.show()