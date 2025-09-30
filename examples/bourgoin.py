import sys
import os
import pathlib
import csv
import platform

import matplotlib
import matplotlib.pyplot

sys.path.append(str(pathlib.Path.cwd()))
from loss.libRadtranPy.libradtranpy import *

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
if platform.system() == 'Linux':
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
        aerosol_visibility=5,
        aerosol_haze=AerosolHaze.RURAL,
        aerosol_vulcan=AerosolVulcan.BACKGROUND_AEROSOLS,
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
        atmosphere_file=Atmosphere.MIDLATTITUDESUMMER,
        # mol_abs_param=(CKScheme.REPTRAN, 'coarse'),
        mol_modify=['CO2 7.84e21 CM_2'],
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
        altitude=0,
        albedo=0.3,
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
        output_quantity=OutputQuantity.TRANSMITTANCE,
        # output_process=OutputProcess.PER_NM,
        # zout=ZOut.TOA
    )
)
print(downlink_sim.generate_uvspec_input())
libradtran_theta = []
libradtran_edir = []
for angle in elevation:
    sza = 90 - angle
    downlink_sim.geometry.sza = sza
    result = downlink_sim.run_uvscpec()
    wavelength, edir, *_ = map(float, result.split())
    libradtran_theta.append(angle)
    libradtran_edir.append(edir)
matplotlib.pyplot.plot(
    libradtran_theta,
    libradtran_edir,
    label='libRadtran'
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
        fname='785nm_loss.png',
        dpi='figure',
        bbox_inches='tight'
    )
else:
    matplotlib.pyplot.show()