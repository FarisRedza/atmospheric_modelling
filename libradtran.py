import dataclasses

from modules.spectral import *
from modules.general_atm import *
from modules.mol_atm import *
from modules.aerosol import *
from modules.profile import *
from modules.clouds import *
from modules.surface import *
from modules.solver import *
from modules.monte_carlo import *
from modules.geometry import *
from modules.output import *

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

sim = Simulation(
    aerosol=Aerosol(
        aerosol_default=True,
        aerosol_season=AerosolSeason.SPRING_SUMMER,
        aerosol_visibility=50
    ),
    mol_atm=MolAtm(
        atmosphere=Atmosphere.MIDLATTITUDESUMMER,
        mol_abs_param=(CKScheme.REPTRAN, 'coarse'),
        mol_modify=['O3 200 DU', 'H2O 20 MM'],
        crs_model=(MolID.RAYLEIGH, CRSModel.BODHAINE)
    ),
    geometry=Geometry(
        sza=90,
        phi=0,
        umu=-1,
        latitude='N 56.405',
        longitude='W 3.183',
        time='2025 3 18 13, 5 37.8075'
    ),
    surface=Surface(
        albedo=0.02,
    ),
    spectral=Spectral(
        wavelength=[785, 785]
    ),
    solver=Solver(
        rte_solver=RTESolver.DISORT
    ),
    output=Output(
        output_user='lambda edir edn',
        output_quantity=OutputQuantity.REFLECTIVITY,
        output_process=OutputProcess.PER_NM,
        z_out='1'
    )
)
print(sim.generate_uvspec_input())