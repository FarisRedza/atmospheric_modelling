import os
import subprocess
import csv
import math

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from libradtran import *

matplotlib.use('GTK4Agg')

elevation = range(0,91,1)

with open(file='qrackling.csv', mode='w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['# theta (deg)', '785 nm'])
    for angle in elevation:
        sza = 90 -angle
        sim = Simulation(
            # Aerosol_Settings
            aerosol_default=True,
            aerosol_season=Aerosol_Season.SPRING_SUMMER,
            aerosol_visibility=50,
            # General_Atmosphere_Settings
            atmosphere_file=Atmosphere.MIDLATTITUDESUMMER,
            # Geometry_Settings
            phi=0,
            umu=-1,
            latitude='N 56.405',
            longitude='W 3.183',
            time='2025 3 18 13 5 37.8075',
            zout=1,
            # Molecule_Settings
            mol_abs_param_ck_scheme=Mol_Abs_Param_CK_Scheme.REPTRAN,
            mol_abs_param_ck_reptran_arg='coarse',
            mol_modify=['O3 200 DU', 'H2O 20 MM'],
            crs_model_mol_id=CRS_Model_Mol_ID.RAYLEIGH,
            crs_model_crs_model=CRS_Model_CRS_Model.BODHAINE,
            # Surface_Settings
            albedo=0.02,
            # Spectral_Settings
            source=Source.SOLAR,
            wavelength_min=785,
            wavelength_max=785,
            # Solver_Settings
            rte_solver=RTE_Solver.DISORT,
            # Output_Settings
            output_user='lambda edir edn',
            output_quantity=Output_Quantity.REFLECTIVITY,
            output_process=Output_Process.PER_NM,
            solar_zenith_angle=sza
        )
        print(sim.generate_uvspec_input())
        result = run_uvscpec(sim=sim)
        print(result)
        wavelength, edir, edn, *_ = map(float, result.split())
        writer.writerow([angle, edir])

radtran = pd.read_csv('qrackling.csv')
ax = radtran.plot(x='# theta (deg)', y='785 nm')

modtran = pd.read_csv('SatQuMA/channel/atmosphere/MODTRAN_wl_785.0-850.0-5.0nm_h1_500.0km_h0_0.0km_elevation_data.csv')
modtran.plot(x='# theta (deg)', y='785 nm', ax=ax)

plt.legend(['libRadtran', 'MODTRAN'])
plt.xlabel('Elevation Angle (°)')
plt.ylabel('Transmittance')
plt.title('Downlink')
plt.ylim([0, 1])
plt.xlim([0, 90])
plt.grid(True)
plt.show()
