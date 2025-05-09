import sys
import os
import pathlib
import tempfile

import numpy as np
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

matplotlib.pyplot.figure(figsize=(8, 4))
matplotlib.pyplot.plot(wavelength, transmittance, color='blue', linewidth=1)
matplotlib.pyplot.xlabel('Wavelength (nm)')
matplotlib.pyplot.ylabel('Transmittance (%)')
matplotlib.pyplot.title('Atmospheric Transmittance Spectrum')
matplotlib.pyplot.grid(True)
matplotlib.pyplot.xlim(sim.spectral.wavelength[0], sim.spectral.wavelength[1])
matplotlib.pyplot.ylim(0, 100)

if headless == True:
    fig.savefig(
        'bourgoin_reproduce.png',
        dpi='figure',
        bbox_inches='tight'
    )
else:
    matplotlib.pyplot.show()