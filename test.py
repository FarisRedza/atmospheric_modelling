import csv

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from atm_modelling.libRadtran.libradtran import *

matplotlib.use('GTK4Agg')

elevation = range(0,91,1)
with open(file='test.csv', mode='w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['# theta (deg)', '785 nm'])
    for angle in elevation:
        sza = 90 -angle
        sim = Simulation(
            aerosol=Aerosol(
                aerosol_default=False,
                # aerosol_season=AerosolSeason.SPRING_SUMMER,
                # aerosol_visibility=50
            ),
            mol_atm=MolAtm(
                # atmosphere_file=Atmosphere.MIDLATTITUDESUMMER,
                # mol_abs_param=(CKScheme.REPTRAN, 'coarse'),
                # mol_modify=['O3 200 DU', 'H2O 20 MM'],
                # crs_model=(MolID.RAYLEIGH, CRSModel.BODHAINE)
            ),
            geometry=Geometry(
                sza=sza,
                # phi=0,
                # umu=-1,
                # latitude='N 56.405',
                # longitude='W 3.183',
                # time='2025 3 18 13, 5 37.8075'
            ),
            surface=Surface(
                # albedo=0.02,
            ),
            spectral=Spectral(
                wavelength=[785, 785]
            ),
            solver=Solver(
                # rte_solver=RTESolver.DISORT
            ),
            output=Output(
                output_user='lambda edir edn',
                output_quantity=OutputQuantity.REFLECTIVITY,
                # output_process=OutputProcess.PER_NM,
                # zout='0'
            )
        )
        result = run_uvscpec(sim=sim)
        print(result)
        wavelength, edir, edn, *_ = map(float, result.split())
        writer.writerow([angle, edir])

print(sim.generate_uvspec_input())

radtran = pd.read_csv('test.csv')
ax = radtran.plot(x='# theta (deg)', y='785 nm')

modtran = pd.read_csv('./SatQuMA/channel/atmosphere/MODTRAN_wl_785.0-850.0-5.0nm_h1_500.0km_h0_0.0km_elevation_data.csv')
modtran.plot(x='# theta (deg)', y='785 nm', ax=ax)

plt.legend(['libRadtran', 'MODTRAN'])
plt.xlabel('Elevation Angle (°)')
plt.ylabel('Transmittance')
plt.title('785 nm Downlink')
plt.ylim([0, 1])
plt.xlim([0, 90])
plt.grid(True)
plt.show()
