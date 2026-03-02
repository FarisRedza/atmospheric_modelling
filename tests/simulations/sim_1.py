import sys
import pathlib

import numpy as np

sys.path.append(str(pathlib.Path.cwd()))
import loss.libRadtranPy.libradtranpy as libradtranpy
import loss.diffraction as diffraction
import loss.background_light as background_light

def main() -> None:
    sat_altitude = 550e3

    time_s = np.linspace(0, 600, 601)

    elevation_deg = 10 + 80 * np.sin(np.pi * time_s / time_s[-1])
    elevation_rad = np.deg2rad(elevation_deg)

    transmission_path_length = sat_altitude / np.sin(elevation_rad)

    atm_sim = libradtranpy.Simulation(
        spectral=libradtranpy.Spectral(
            wavelength=[785],
            source=libradtranpy.Source.SOLAR
        ),
        general_atm=libradtranpy.GeneralAtm(),
        mol_atm=libradtranpy.MolAtm(
            atmosphere_file=libradtranpy.Atmosphere.MIDLATITUDE_SUMMER
        ),
        aerosol=libradtranpy.Aerosol(
            aerosol_default=True
        ),
        solver=libradtranpy.Solver(
            rte_solver=libradtranpy.RTESolver.DISORT
        ),
        output=libradtranpy.Output(
            quiet=True,
            output_user='lambda edir',
            output_quantity=libradtranpy.OutputQuantity.TRANSMITTANCE,
            output_format=libradtranpy.OutputFormat.ASCII
        ),
        geometry=libradtranpy.Geometry(
            sza=90
        )
    )
    print(atm_sim.run_transmission_against_elevation())

if __name__ == '__main__':
    main()