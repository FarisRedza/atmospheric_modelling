import sys
import os
import pathlib
import csv

import matplotlib
import matplotlib.pyplot

sys.path.append(str(pathlib.Path.cwd()))
from atm_modelling.libRadtran.libradtran import *

try:
    os.environ['LIBRADTRANDIR']
except:
    os.environ['LIBRADTRANDIR'] = str(pathlib.Path(
        pathlib.Path.cwd(),
        'libRadtran-2.0.6'
    ))
else:
    print('Using system value for LIBRADTRANDIR')

matplotlib.use('GTK4Agg')
fig = matplotlib.pyplot.figure()

elevation = range(0,91,1)

bourgoin_settings = Simulation(
    aerosol=Aerosol(
        aerosol_default=True,
        aerosol_visibility=5,
        aerosol_haze=AerosolHaze.RURAL,
    ),
    general_atm=GeneralAtm(),
    mol_atm=MolAtm(),
    geometry=Geometry(),
    surface=Surface(
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
        output_user='lambda edir',
        output_quantity=OutputQuantity.REFLECTIVITY,
    )
)
bourgoin_settings_theta = []
bourgoin_settings_edir = []
for angle in elevation:
    bourgoin_settings.geometry.sza = 90 - angle
    result = bourgoin_settings.run_uvscpec()
    wavelength, edir, *_ = map(float, result.split())
    bourgoin_settings_theta.append(float(angle))
    bourgoin_settings_edir.append(float(edir))

matplotlib.pyplot.plot(
    bourgoin_settings_theta,
    bourgoin_settings_edir,
    label='BourgoinSettings'
)

custom_settings = Simulation(
    aerosol=Aerosol(
        aerosol_default=True,
        aerosol_season=AerosolSeason.AUTUMN_WINTER,
        aerosol_visibility=5,
        aerosol_haze=AerosolHaze.TROPOSPHERIC,
    ),
    general_atm=GeneralAtm(
        no_absorption=True,
        no_scattering=True,
    ),
    mol_atm=MolAtm(
        atmosphere_file=Atmosphere.USSTANDARD,
    ),
    geometry=Geometry(),
    surface=Surface(
        altitude=0,
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
        output_user='lambda edir',
        output_quantity=OutputQuantity.REFLECTIVITY,
    )
)
custom_settings_theta = []
custom_settings_edir = []
for angle in elevation:
    custom_settings.geometry.sza = 90 - angle
    result = custom_settings.run_uvscpec()
    wavelength, edir, *_ = map(float, result.split())
    custom_settings_theta.append(float(angle))
    custom_settings_edir.append(float(edir))
matplotlib.pyplot.plot(
    custom_settings_theta,
    custom_settings_edir,
    label='CustomSettings'
)

custom_settings_csv_file = 'bourgoin_reproduce.csv'
custom_settings_csv_file_path = pathlib.Path(
    pathlib.Path.cwd(),
    custom_settings_csv_file
)
with open(file=custom_settings_csv_file_path, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Elevation (°)','Transmittance'])
    for angle, transmission in zip(custom_settings_theta, custom_settings_edir):
        writer.writerow([angle, transmission])

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

bourgoin_figure_file = 'bourgoin_figure.csv'
bourgoin_figure_file_path = pathlib.Path(
    pathlib.Path.cwd(),
    'tests',
    'libradtran',
    bourgoin_figure_file
)
bourgoin_figure_theta = []
bourgoin_figure_edir = []
with open(file=bourgoin_figure_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        bourgoin_figure_theta.append(float(row['x']))
        bourgoin_figure_edir.append(float(row[' y']))
matplotlib.pyplot.plot(
    bourgoin_figure_theta,
    bourgoin_figure_edir,
    label='BourgoinFigure'
)


matplotlib.pyplot.legend()
matplotlib.pyplot.xlabel('Elevation Angle (°)')
matplotlib.pyplot.ylabel('Transmittance')
matplotlib.pyplot.title('785 nm Downlink')
matplotlib.pyplot.ylim([0, 1])
matplotlib.pyplot.xlim([0, 90])
matplotlib.pyplot.grid(True)
matplotlib.pyplot.show()

fig.savefig(
    'bourgoin_reproduce.png',
    dpi='figure',
    bbox_inches='tight'
)
