import sys
import pathlib
import csv

import numpy
import scipy.interpolate
import matplotlib.axes
import matplotlib.pyplot
import matplotlib.cm

sys.path.append(str(pathlib.Path.cwd()))
import loss.diffraction as diffraction
import loss.libRadtranPy.libradtranpy as libradtranpy

data_dir = pathlib.Path(__file__).parent.parent.joinpath(
    'data',
    'bourgoin'
).resolve()
data_file = 'bourgoin_loss_profile_best.csv'

with open(file=data_dir.joinpath(data_file), mode='r') as csvfile:
    csvreader = csv.DictReader(f=csvfile, delimiter=',')
    time = []
    loss = []
    for row in csvreader:
        time.append(float(row['x']))
        loss.append(float(row[' y']))

figure, axis = matplotlib.pyplot.subplots()
axis.plot(
    time,
    loss,
    label='Bourgoin best pass'
)

dif_simulation = diffraction.DiffractionSim(
    sat_altitude=600e3,
    ogs_altitude=0,
    wavelength=785e-9,
    divergence_FWHM=2.57e-5,
    sat_telescope_diameter=0.3,
    turbulence=True,
    minimum_elevation=10
)

atm_simulation = libradtranpy.Simulation(
    spectral=libradtranpy.Spectral(
        wavelength=[785],
        source=libradtranpy.Source.SOLAR
    ),
    aerosol=libradtranpy.Aerosol(
        aerosol_default=True,
        # aerosol_set_tau_at_wvl=('550.0', '0.05'),
        aerosol_visibility=6,
        aerosol_haze=libradtranpy.AerosolHaze.RURAL,
        aerosol_season=libradtranpy.AerosolSeason.SPRING_SUMMER,
        aerosol_vulcan=libradtranpy.AerosolVulcan.BACKGROUND_AEROSOLS
    ),
    mol_atm=libradtranpy.MolAtm(
        atmosphere_file=libradtranpy.Atmosphere.MIDLATITUDE_SUMMER,
        # atmosphere_file='/home/faris/Projects/atmospheric_modelling/libRadtran-2.0.6/examples/AFGLMS50.DAT',
        mixing_ratio=(libradtranpy.Species.CO2, '365.0')
    ),
    geometry=libradtranpy.Geometry(
        sza=0,
    ),
    surface=libradtranpy.Surface(
        # altitude=5,
        albedo=0.3
    ),
    solver=libradtranpy.Solver(
        rte_solver=libradtranpy.RTESolver.DISORT,
        number_of_streams=8
    ),
    output=libradtranpy.Output(
        quiet=True,
        output_user='lambda edir',
        output_quantity=libradtranpy.OutputQuantity.REFLECTIVITY,
        # zout=libradtranpy.ZOut.TOA
    )
)

dif_sim_result = dif_simulation.run_sim()

x = dif_sim_result.times
y = numpy.zeros(len(dif_sim_result.transmissions))

y += -10*numpy.log10(dif_sim_result.transmissions)

atm_sim_result = atm_simulation.run_transmission_against_elevation()
atm_sim_interpolated = scipy.interpolate.interp1d(
    x=atm_sim_result.elevations,
    y=atm_sim_result.transmission_as_dB(),
    kind='linear'
)
atm_sim_interpolated_dB = atm_sim_interpolated(dif_sim_result.elevations)
y += atm_sim_interpolated_dB

axis.plot(
    x,
    y,
    label='Simulation'
)

axis.set_xlabel(xlabel='Time [s]')
axis.set_ylabel(ylabel='Loss [dB]')
axis.legend()
axis.grid(visible=True)
matplotlib.pyplot.show()

print(atm_simulation.generate_uvspec_input())