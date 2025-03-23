import dataclasses
import enum
import typing

from .units import *

class AerosolSeason(enum.Enum):
    SPRING_SUMMER = 1
    AUTUMN_WINTER = 2

class AerosolHaze(enum.Enum):
    RURAL = 1
    MARITIME = 4
    URBAN = 5
    TROPOSPHERIC = 6

class AerosolVulcan(enum.Enum):
    BACKGROUND_AEROSOLS = 1
    MODERATE_VOLCANIC_AEROSOLS = 2
    HIGH_VOLCANIC_AEROSOLS = 3
    EXTREME_VOLCANIC_AEROSOLS = 4

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
    aerosol_default: bool = False
    aerosol_season: AerosolSeason = None
    aerosol_visibility: km = None
    aerosol_haze: AerosolHaze = None
    aerosol_vulcan: AerosolVulcan = None
    aerosol_species_file: AerosolSpecies = None
    aerosol_species_library: AerosolSpeciesLibrary = None

    def __post_init__(self):
        if not isinstance(self.aerosol_default, bool):
            raise ValueError(f'Invalid aerosol_default: {self.aerosol_default}')
        
        if not isinstance(self.aerosol_season, typing.Union[AerosolSeason, None]):
            raise ValueError(f'Invalid aerosol_season: {self.aerosol_season}')
        
        if not isinstance(self.aerosol_visibility, typing.Union[float, int, None]):
            raise ValueError(f'Invalid aerosol_visibility: {self.aerosol_visibility}')
        
        if not isinstance(self.aerosol_haze, typing.Union[AerosolHaze, None]):
            raise ValueError(f'Invalid aerosol_haze: {self.aerosol_haze}')
        
        if not isinstance(self.aerosol_vulcan, typing.Union[AerosolVulcan, None]):
            raise ValueError(f'Invalid aerosol_vulcan: {self.aerosol_vulcan}')
        
        if not isinstance(self.aerosol_species_file, typing.Union[AerosolSpecies, None]):
            raise ValueError(f'Invalid aerosol_species: {self.aerosol_species_file}')
        
        if not isinstance(self.aerosol_season, typing.Union[AerosolSeason, None]):
            raise ValueError(f'Invalid aerosol_default: {self.aerosol_season}')
        
    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter, prefix: str = '', suffix: str = ''):
            for field in dataclasses.fields(self):
                if getattr(self, field.name) is parameter:
                    field_name = field.name
                    break

            if getattr(self, field_name) is not None:
                match parameter:
                    case bool():
                        if parameter == True:
                            parameters.append(field_name)
                    case enum.Enum():
                        parameters.append(f'{field_name} {prefix}{parameter.value}{suffix}')
                    case float() | int():
                        parameters.append(f'{field_name} {parameter}')
                    case _:
                        raise Exception(f'Unknown type {type(parameter)}')

        add_parameter(self.aerosol_default)
        add_parameter(self.aerosol_season)
        add_parameter(self.aerosol_visibility)
        add_parameter(self.aerosol_haze)
        add_parameter(self.aerosol_vulcan)
        add_parameter(
            parameter=self.aerosol_species_file,
            prefix='../data/aerosol/OPAC/standard_aerosol_files/',
            suffix='.dat'
        )
        add_parameter(self.aerosol_species_library)

        return '\n'.join(parameters)