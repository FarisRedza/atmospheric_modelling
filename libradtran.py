import dataclasses
import enum

# Spectral
class Source(enum.Enum):
    SOLAR = 'solar'
    THERMAL = 'thermal'

@dataclasses.dataclass
class Spectral:
    wavelength: list
    source: Source

    @property
    def wavelength(self) -> list:
        return self._wavelength
    
    @wavelength.setter
    def wavelength(self, value: list):
        if not isinstance(value, list):
            raise ValueError(f'Invalid wavelength: {value}')
        self._wavelength = value

    @property
    def source(self) -> str:
        return self._source.value
    
    @source.setter
    def source(self, value: Source):
        if not isinstance(value, Source):
            raise ValueError(f'Invalid source: {value}')
        self._source = value

# General Atm
@dataclasses.dataclass
class GeneralAtm:
    absorption: bool = None
    scattering: bool = None
    zout_interpolate: bool = None
    reverse_atmosphere: bool = None

    @property
    def absorption(self) -> bool:
        return self.absorption
    
    @absorption.setter
    def absorption(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(f'Invalid absorption: {value}')
        self._absorption = value

    @property
    def scattering(self) -> bool:
        return self.scattering
    
    @scattering.setter
    def scattering(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(f'Invalid scattering: {value}')
        self._scattering = value

    @property
    def zout_interpolate(self) -> bool:
        return self.zout_interpolate
    
    @zout_interpolate.setter
    def zout_interpolate(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(f'Invalid zout_interpolate: {value}')
        self._zout_interpolate = value

    @property
    def reverse_atmosphere(self) -> bool:
        return self.reverse_atmosphere
    
    @reverse_atmosphere.setter
    def reverse_atmosphere(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(f'Invalid reverse_atmosphere: {value}')
        self._reverse_atmosphere = value

# Mol Atm
class Atmosphere(enum.Enum):
    MIDLATTITUDESUMMER = "afglms"
    MIDLATTITUDEWINTER = "afglmw"
    SUBARCTICSUMMER = "afglss"
    SUBARCTICWINTER = "afglsw"
    TROPICAL = "afglt"
    USSTANDARD = "afglus"

class CKScheme(enum.Enum):
    KATO = 'kato'
    KATO2 = 'kato2'
    KATO2_96 = 'kato2.96'
    KATO2ANDWANDJI = 'kato2andwandji'
    FU = 'fu'
    AVHRR_KRATZ = 'avhrr_kratz'
    SPDART = 'spdart'
    LOWTRAN = 'lowtran'
    REPTRAN = 'reptran'
    REPTRAN_CHANNEL = 'reptran_channel'
    CRS = 'crs'
    USER_DEFINED = 'user_defined'

class MolID(enum.Enum):
    NO2 = 'no2'
    O3 = 'o3'
    O4 = 'o4'
    RAYLEIGH = 'rayleigh'

class CRSModel(enum.Enum):
    BASS_AND_PAUR = 'bass_and_paur'
    MOLINA = 'molina'
    DAUMONT = 'daumont'
    SERDYUCHENKO = 'serdyuchenko'
    BOGUMIL = 'bogumil'
    BODHAINE = 'bodhaine'
    BODHAINE29 = 'bodhain29'
    NICOLET = 'nicolet'
    PENNDORF = 'penndorf'
    BURROWS = 'burrows'
    VANDAELE = 'vandale'
    GREENBLATT = 'greenblatt'
    THALMAN = 'thalman'

@dataclasses.dataclass
class MolAtm:
    atmosphere: Atmosphere = Atmosphere.MIDLATTITUDESUMMER
    mol_abs_param: tuple[CKScheme, str] = None
    crs_model: tuple[MolID, CRSModel] = None

    @property
    def atmosphere(self) -> str:
        return self._atmosphere.value
    
    @atmosphere.setter
    def atmosphere(self, value: Atmosphere):
        if not isinstance(value, Atmosphere):
            raise ValueError(f'Invalid atmosphere: {value}')
        self._atmosphere = value

    @property
    def mol_abs_param(self) -> tuple:
        return self._mol_abs_param
    
    @mol_abs_param.setter
    def mol_abs_param(self, value: tuple):
        if not isinstance(value, tuple):
            raise ValueError(f'Invalid mol_abs_param: {value}')
        self._mol_abs_param = value

    @property
    def crs_model(self) -> tuple:
        return self._crs_model
    
    @crs_model.setter
    def crs_model(self, value: tuple):
        if not isinstance(value, tuple):
            raise ValueError(f'Invalid crs_model: {value}')
        self._crs_model = value

# Aerosol
class AerosolSeason(enum.Enum):
    SPRING_SUMMER = 1
    AUTUMN_WINTER = 2

class AerosolSpecies(enum.Enum):
    CONTINENTAL_CLEAN = 'continental_clean'
    CONTINENTAL_AVERAGE = 'continental_average'
    CONTINENTAL_POLLUTED = 'continental_polluted'
    URBAN = 'urban'
    MARITIME_CLEAN = 'maritime_clean'
    MARITIME_POLLUTED = 'maritime_polluted'
    MARITIME_TROPICAL = 'maritime_tropical'
    DESERT = 'desert'
    ANTARCTIC = 'antarctic'

class AerosolSpeciesLibrary(enum.Enum):
    OPAC = 'opac'
    USER_DEFINED = 'user_defined'

@dataclasses.dataclass
class Aerosol:
    aerosol_default: bool = None
    aerosol_season: AerosolSeason = None
    aerosol_species: AerosolSpecies = None
    aerosol_species_library: AerosolSpeciesLibrary = None

    @property
    def aerosol_default(self) -> bool:
        return self._aerosol_default
    
    @aerosol_default.setter
    def aerosol_default(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(f'Invalid aerosol_default: {value}')
        self._aerosol_default = value

    @property
    def aerosol_season(self) -> str:
        return self._aerosol_season.value
    
    @aerosol_season.setter
    def aerosol_season(self, value: AerosolSeason):
        if not isinstance(value, AerosolSeason):
            raise ValueError(f'Invalid aerosol_season: {value}')
        self._aerosol_season = value

    @property
    def aerosol_species(self) -> str:
        return self._aerosol_species.value
    
    @aerosol_species.setter
    def aerosol_species(self, value: AerosolSpecies):
        if not isinstance(value, AerosolSpecies):
            raise ValueError(f'Invalid aerosol_species: {value}')
        self._aerosol_species = value

    @property
    def aerosol_species_library(self) -> str:
        return self._aerosol_species_library.value
    
    @aerosol_species_library.setter
    def aerosol_species_library(self, value: AerosolSpeciesLibrary):
        if not isinstance(value, AerosolSpeciesLibrary):
            raise ValueError(f'Invalid aerosol_species_library: {value}')
        self._aerosol_species_library = value

@dataclasses.dataclass
class Profile:
    pass

@dataclasses.dataclass
class Clouds:
    pass

@dataclasses.dataclass
class Clouds:
    pass

@dataclasses.dataclass
class Surface:
    pass

# Solver
class RTESolver(enum.Enum):
    DISORT = "disort"
    MYSTIC = "MYSTIC"
    FDISORT1 = "fdisort1"
    FDISORT2 = "fdisort2"
    TWOSTR = "twostr"
    RODENTS = "rodents"
    SDISORT = "sdisort"
    SPSDISORT = "spsdisort"
    TZS = "tzs"
    SSS = "sss"
    SSLIDAR = "sslidar"

rte_solver: RTESolver = None

@dataclasses.dataclass
class Solver:
    rte_solver: RTESolver = None

    @property
    def rte_solver(self) -> str:
        return self._rte_solver.value
    
    @rte_solver.setter
    def rte_solver(self, value: RTESolver):
        if not isinstance(value, RTESolver):
            raise ValueError(f'Invalid rte_solver: {value}')
        self._rte_solver = value

# Monte Carlo
class MCPolarisation(enum.Enum):
    ZERO = {0: '(1,0,0,0) (default)'}
    ONE = {1: '(1,1,0,0)'}
    TWO = {2: '(1,0,1,0)'}
    THREE = {3: '(1,0,0,1)'}
    MINUS_ONE = {-1: '(1,-1,0,0)'}
    MINUS_TWO = {-2: '(1,0,-1,0)'}
    MINUS_THREE = {-3: '(1,0,0,-1)'}
    FOUR = {4: 'Random'}

class MCBackwardOutput(enum.Enum):
    EDIR = 'edir'
    EDN = 'edn'
    EUP = 'eup'
    EXP = 'exp'
    EYP = 'eyp'
    EYN = 'eyn'
    ACT = 'act'

class MCForwardOutput(enum.Enum):
    ABSORPTION = 'absorption'
    EMISSION = 'emission'
    HEATING = 'heating'

class MCOutputUnit(enum.Enum):
    W_PER_M2_AND_DZ = 'W_per_m2_and_dz'
    W_PER_M3 = 'W_per_m3'
    K_PER_DAY = 'K_per_day'

@dataclasses.dataclass
class MonteCarlo:
    mc_polarisation: MCPolarisation = None
    mc_backward_output: MCBackwardOutput = None
    mc_forward_output: MCForwardOutput = None
    mc_output_unit: MCOutputUnit = None

    @property
    def mc_polarisation(self) -> str:
        return self._mc_polarisation.value
    
    @mc_polarisation.setter
    def mc_polarisation(self, value: MCPolarisation):
        if not isinstance(value, MCPolarisation):
            raise ValueError(f'Invalid mc_polarisation: {value}')
        self._mc_polarisation = value

    @property
    def mc_backward_output(self) -> str:
        return self._mc_backward_output.value
    
    @mc_backward_output.setter
    def mc_backward_output(self, value: MCBackwardOutput):
        if not isinstance(value, MCBackwardOutput):
            raise ValueError(f'Invalid mc_backward_output: {value}')
        self._mc_backward_output = value

    @property
    def mc_forward_output(self) -> str:
        return self._mc_forward_output.value
    
    @mc_forward_output.setter
    def mc_forward_output(self, value: MCForwardOutput):
        if not isinstance(value, MCForwardOutput):
            raise ValueError(f'Invalid mc_forward_output: {value}')
        self._mc_forward_output = value

    @property
    def mc_output_unit(self) -> str:
        return self._mc_output_unit.value
    
    @mc_output_unit.setter
    def mc_output_unit(self, value: MCOutputUnit):
        if not isinstance(value, MCOutputUnit):
            raise ValueError(f'Invalid mc_output_unit: {value}')
        self._mc_output_unit = value

@dataclasses.dataclass
class Geometry:
    pass

# Output
class OutputQuantity(enum.Enum):
    TRANSMITTANCE = "transmittance"
    REFLECTIVITY = "reflectivity"

class OutputProcess(enum.Enum):
    INTEGRATE = 'integrate'
    SUM = 'sum'
    RGBNORM = 'rgbnorm'
    RGB_NORM = 'rgb_norm'
    RGB = 'rgb'
    PER_NM = 'per_nm'
    PER_CM_1 = 'per_cm-1'
    PER_BAND = 'per_band'

class OutputFormat(enum.Enum):
    ASCII = 'ascii'
    FLEXSTOR = 'flexstor'

class ZOut(enum.Enum):
    TOP = "TOP"

@dataclasses.dataclass
class Output:
    output_quantity: OutputQuantity = None
    output_process: OutputProcess = None
    output_format: OutputFormat = None
    z_out: ZOut = None

    @property
    def output_quantity(self) -> str:
        return self._output_quantity.value
    
    @output_quantity.setter
    def output_quantity(self, value: OutputQuantity):
        if not isinstance(value, OutputQuantity):
            raise ValueError(f'Invalid output_quantity: {value}')
        self._output_quantity = value

    @property
    def output_process(self) -> str:
        return self._output_process.value
    
    @output_process.setter
    def output_process(self, value: OutputProcess):
        if not isinstance(value, OutputProcess):
            raise ValueError(f'Invalid output_process: {value}')
        self._output_process = value

    @property
    def output_format(self) -> str:
        return self._output_format.value
    
    @output_format.setter
    def output_format(self, value: OutputFormat):
        if not isinstance(value, OutputFormat):
            raise ValueError(f'Invalid output_format: {value}')
        self._output_format = value

    @property
    def z_out(self) -> str:
        return self._z_out.value
    
    @z_out.setter
    def z_out(self, value: ZOut):
        if not isinstance(value, ZOut):
            raise ValueError(f'Invalid z_out: {value}')
        self._z_out = value

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