import csv
import tempfile

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from atm_modelling.libRadtran.libradtran import *

matplotlib.use('GTK4Agg')

sim = Simulation(
    mol_atm=MolAtm(
        atmosphere_file=Atmosphere.MIDLATTITUDESUMMER,
    ),
    geometry=Geometry(
        sza=0,
        phi0=0,
        umu=-1,
        phi=0
    ),
    spectral=Spectral(
        source=Source.SOLAR,
        wavelength=[200, 2000]
    ),
    solver=Solver(
        rte_solver=RTESolver.DISORT
    ),
    output=Output(
        output_user='lambda edir',
        output_quantity=OutputQuantity.TRANSMITTANCE,
    ),
)

result = sim.run_uvscpec()

temp = tempfile.TemporaryFile()
try:
    print(temp.name)
    temp.write(result.encode(encoding='utf-8'))
    temp.seek(0)
    data = np.loadtxt(temp)
finally:
    temp.close()

wavelength = data[:, 0]
transmittance = data[:, 1] * 100

plt.figure(figsize=(8, 4))
plt.plot(wavelength, transmittance, color='blue', linewidth=1)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Transmittance (%)')
plt.title('Atmospheric Transmittance Spectrum')
plt.grid(True)
plt.xlim(sim.spectral.wavelength[0], sim.spectral.wavelength[1])
plt.ylim(0, 100)
plt.show()
