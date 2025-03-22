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
        parameters = [
            self.spectral.generate_uvspec_input(),
            # self.general_atm.generate_uvspec_input()
            self.mol_atm.generate_uvspec_input(),
            self.aerosol.generate_uvspec_input(),
            # self.profile.generate_uvspec_input(),
            # self.clouds.generate_uvspec_input(),
            self.surface.generate_uvspec_input(),
            self.solver.generate_uvspec_input(),
            # self.monte_carlo.generate_uvspec_input(),
            self.geometry.generate_uvspec_input(),
            self.output.generate_uvspec_input()
        ]
        return '\n'.join(parameters)

def run_uvscpec(sim: Simulation) -> str:
    cwd = os.getcwd()
    os.chdir(os.path.join(os.environ['LIBRADTRANDIR'],'examples'))
    result = subprocess.run(
        ['../bin/uvspec'],
        input=sim.generate_uvspec_input(),
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )
    os.chdir(cwd)
    return result.stdout