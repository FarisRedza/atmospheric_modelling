import sys
import dataclasses
import subprocess
import pathlib
import math
import shutil

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from loss.libRadtranPy.spectral import *
from loss.libRadtranPy.general_atm import *
from loss.libRadtranPy.mol_atm import *
from loss.libRadtranPy.aerosol import *
from loss.libRadtranPy.profile import *
from loss.libRadtranPy.clouds import *
from loss.libRadtranPy.surface import *
from loss.libRadtranPy.solver import *
from loss.libRadtranPy.monte_carlo import *
from loss.libRadtranPy.geometry import *
from loss.libRadtranPy.output import *

@dataclasses.dataclass
class SimulationResult:
    elevations: list[float]
    transmissions: list[float]

    def transmission_as_dB(self) -> list[float]:
        return [
            -10 * math.log10(t)if t > 0 else float('inf')
            for t in self.transmissions
        ]

@dataclasses.dataclass
class Simulation:
    spectral: Spectral | None = None
    general_atm: GeneralAtm | None = None
    mol_atm: MolAtm | None = None
    aerosol: Aerosol | None = None
    profile: Profile | None = None
    clouds: Clouds | None = None
    surface: Surface | None = None
    solver: Solver | None = None
    monte_carlo: MonteCarlo | None = None
    geometry: Geometry | None = None
    output: Output | None = None
    _libRadtran_version = '2.0.6'
    _libRadtran_dir = pathlib.Path(__file__).parent.parent.parent.joinpath(
        f'libRadtran-{_libRadtran_version}',
    )

    def generate_uvspec_input(self) -> str:
        parameters = []
        data_dir = self._libRadtran_dir.joinpath('data')
        parameters.append(f'data_files_path {data_dir}')
        def add_parameter(parameter):
            if parameter is not None:
                parameters.append(parameter.generate_uvspec_input())

        add_parameter(self.spectral)
        add_parameter(self.general_atm)
        add_parameter(self.mol_atm)
        add_parameter(self.aerosol)
        add_parameter(self.profile)
        add_parameter(self.clouds)
        add_parameter(self.surface)
        add_parameter(self.solver)
        add_parameter(self.monte_carlo)
        add_parameter(self.geometry)
        add_parameter(self.output)
        return '\n'.join(parameters)

    def run_uvscpec(self) -> str:
        if shutil.which('uvspec'):
            uvspec = str(shutil.which('uvspec'))
        else:
            uvspec = [str(self._libRadtran_dir.joinpath(
                'bin',
                'uvspec'
            ))]
        result = subprocess.run(
            uvspec,
            input=self.generate_uvspec_input(),
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout

    def run_transmission_against_elevation(
            self,
            min_elevation: int = 0,
            max_elevation: int = 90,
            elevation_step: int = 1
    ) -> SimulationResult:
        atm_theta = []
        atm_edir = []
        for angle in range(min_elevation, max_elevation+elevation_step, elevation_step):
            self.geometry.sza = 90 - angle
            result = self.run_uvscpec()
            result_wavelength, result_edir, *_ = map(float, result.split())
            atm_theta.append(angle)
            atm_edir.append(result_edir)
        
        return SimulationResult(
            elevations=atm_theta,
            transmissions=atm_edir
        )