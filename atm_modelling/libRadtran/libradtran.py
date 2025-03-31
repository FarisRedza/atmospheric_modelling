import dataclasses
import subprocess
import os

from .spectral import *
from .general_atm import *
from .mol_atm import *
from .aerosol import *
from .profile import *
from .clouds import *
from .surface import *
from .solver import *
from .monte_carlo import *
from .geometry import *
from .output import *

@dataclasses.dataclass
class Simulation:
    spectral: Spectral = None
    general_atm: GeneralAtm = None
    mol_atm: MolAtm = None
    aerosol: Aerosol = None
    profile: Profile = None
    clouds: Clouds = None
    surface: Surface = None
    solver: Solver = None
    monte_carlo: MonteCarlo = None
    geometry: Geometry = None
    output: Output = None

    def generate_uvspec_input(self) -> str:
        parameters = []
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
        cwd = os.getcwd()
        os.chdir(os.path.join(os.environ['LIBRADTRANDIR'],'examples'))
        result = subprocess.run(
            ['../bin/uvspec'],
            input=self.generate_uvspec_input(),
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        os.chdir(cwd)
        return result.stdout