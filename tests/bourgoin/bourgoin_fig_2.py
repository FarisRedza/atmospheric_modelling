import sys
import pathlib
import csv
import re

import matplotlib.axes
import matplotlib.pyplot
import matplotlib.cm

sys.path.append(str(pathlib.Path.cwd()))
import loss.libRadtranPy.libradtranpy as libradtranpy

def atoi(text: str) -> int | str:
    return int(text) if text.isdigit() else text

def natural_keys(text: str) -> list:
    return [atoi(c) for c in re.split(r'(\d+)', text)]

data_dir = pathlib.Path(__file__).parent.parent.joinpath(
    'data',
    'bourgoin',
    'transmittance_elevation'
).resolve()
files_strings = sorted(
    [str(s) for s in data_dir.iterdir()],
    key=natural_keys
)
files = [pathlib.Path(f) for f in files_strings]

def fig_a(
        simulation: libradtranpy.Simulation,
        axis: matplotlib.axes.Axes
) -> None:
    wavelengths = [int(file.stem.split('_')[-1]) for file in files]
    simulation.spectral.wavelength = [350, 1700]
    result = simulation.run_uvscpec()
    result_wavelength = []
    result_edir = []
    for line in result.splitlines():
        result_w, result_e = map(float, line.strip().split())
        result_wavelength.append(result_w)
        result_edir.append(result_e)

    axis.plot(
        result_wavelength,
        result_edir,
        linewidth=1,
        color='blue',
        label='Transmittance'
    )
    axis.set_xlabel('Wavelength [nm]')
    axis.set_ylabel('Transmittance')
    axis.grid(True)
    axis.set_xlim(simulation.spectral.wavelength[0], simulation.spectral.wavelength[1])
    axis.set_ylim(0, 0.8)

    for i, wl in enumerate(wavelengths):
        axis.vlines(
            x=wl,
            ymin=0,
            ymax=0.8,
            colors=matplotlib.cm.tab10(i % 10),
            label=f'{wl} nm')
    axis.legend()

def fig_b(
        simulation: libradtranpy.Simulation,
        axis: matplotlib.axes.Axes
) -> None:
    min_elevation = 10
    max_elevation = 90

    wavelengths = []
    for i, file in enumerate(files):
        wavelength = int(file.stem.split('_')[-1])
        wavelengths.append(wavelength)
        with open(file=file, mode='r') as csvfile:
            csvreader = csv.DictReader(f=csvfile, delimiter=',')
            elevation = []
            transmittance = []
            for row in csvreader:
                elevation.append(float(row['x']))
                transmittance.append(float(row[' y']))
            axis.plot(
                elevation,
                transmittance,
                color=matplotlib.cm.tab10(i % 10),
                label=f'{wavelength} nm'
            )

        simulation.spectral.wavelength = [wavelength]
        atm_sim_result = simulation.run_transmission_against_elevation(
            min_elevation=min_elevation,
            max_elevation=max_elevation
        )
        axis.plot(
            atm_sim_result.elevations,
            atm_sim_result.transmissions,
            color=matplotlib.pyplot.cm.tab10(i % 10),
            linestyle='--',
            label=f'LRT - {wavelength} nm',
        )

    axis.set_xlabel('Angle from the horizon [degree]')
    axis.set_ylabel('Transmittance')
    axis.set_xlim(min_elevation, max_elevation)
    axis.set_ylim(0,0.8)
    axis.grid()
    axis.legend()

if __name__ == '__main__':
    simulation = libradtranpy.Simulation(
        spectral=libradtranpy.Spectral(
            wavelength=None,
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
    figure, (axis_a, axis_b) = matplotlib.pyplot.subplots(
        nrows=1,
        ncols=2,
        figsize=(12, 5)
    )
    fig_a(simulation=simulation, axis=axis_a)
    fig_b(simulation=simulation, axis=axis_b)
    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.show()