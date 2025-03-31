import csv
import pprint
import math

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from atm_modelling.libRadtran.libradtran import *

matplotlib.use('GTK4Agg')

elevation = range(0,-91,1)
with open(file='uplink.csv', mode='w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['# theta (deg)', '785 nm'])
    uplink_sim = Simulation(
        aerosol=Aerosol(
            aerosol_default=True,
        ),
        general_atm=GeneralAtm(),
        mol_atm=MolAtm(),
        geometry=Geometry(
            umu=1,
        ),
        surface=Surface(
            altitude=0,
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
            # zout=ZOut.TOA
        )
    )
    for angle in elevation:
        sza = -90 + angle
        uplink_sim.geometry.sza=sza
        result = run_uvscpec(sim=uplink_sim)
        wavelength, edir, *_ = map(float, result.split())
        writer.writerow([angle, edir])

uplink = pd.read_csv('uplink.csv')
ax = uplink.plot(x='# theta (deg)', y='785 nm')

downlink = pd.read_csv('./downlink.csv')
downlink.plot(x='# theta (deg)', y='785 nm', ax=ax)

plt.legend(['uplink', 'downlink'])
plt.xlabel('Elevation Angle (°)')
plt.ylabel('Transmittance')
plt.title('785 nm')
# plt.ylim([0, 1])
# plt.xlim([0, 90])
plt.grid(True)
plt.show()


# sim = Simulation(
#     spectral=Spectral(
#         wavelength=[785, 785]
#     ),
#     general_atm=GeneralAtm(),
#     mol_atm=MolAtm(),
#     aerosol=Aerosol(
#         aerosol_default=True
#     ),
#     profile=Profile(),
#     clouds=Clouds(),
#     surface=Surface(),
#     solver=Solver(),
#     monte_carlo=MonteCarlo(),
#     geometry=Geometry(
#         umu=math.cos(math.radians(90))
#     ),
#     output=Output(
#         output_user='lambda edir'
#     )
# )
# run_uvscpec(sim=sim)
