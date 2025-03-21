import dataclasses
import enum
import typing

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
    aerosol_visibility: float = None
    aerosol_species: AerosolSpecies = None
    aerosol_species_library: AerosolSpeciesLibrary = None

    @property
    def aerosol_default(self) -> bool:
        return self._aerosol_default
    
    @aerosol_default.setter
    def aerosol_default(self, value: bool):
        if isinstance(value, property):
            self._aerosol_default = None
        elif isinstance(value, bool):
            self._aerosol_default = value
        else:
            raise ValueError(f'Invalid aerosol_default: {value}')

    @property
    def aerosol_season(self) -> str:
        if getattr(self._aerosol_season, 'value', None):
            return self._aerosol_season.value
        return self._aerosol_season
    
    @property
    def aerosol_visibility(self) -> float:
        return self._aerosol_visibility
    
    @aerosol_visibility.setter
    def aerosol_visibility(self, value: float):
        if isinstance(value, property):
            self._aerosol_visibility = None
        elif isinstance(value, typing.Union[float, int]):
            self._aerosol_visibility = value
        else:
            raise ValueError(f'Invalid aerosol_visibility: {value}')

    @aerosol_season.setter
    def aerosol_season(self, value: AerosolSeason):
        if isinstance(value, property):
            self._aerosol_season = None
        elif isinstance(value, AerosolSeason):
            self._aerosol_season = value
        else:
            raise ValueError(f'Invalid aerosol_season: {value}')

    @property
    def aerosol_species(self) -> str:
        if getattr(self._aerosol_species, 'value', None):
            return self._aerosol_species.value
        return self._aerosol_species
    
    @aerosol_species.setter
    def aerosol_species(self, value: AerosolSpecies):
        if isinstance(value, property):
            self._aerosol_species = None
        elif isinstance(value, AerosolSpecies):
            self._aerosol_species = value
        else:
            raise ValueError(f'Invalid aerosol_species: {value}')

    @property
    def aerosol_species_library(self) -> str:
        if getattr(self._aerosol_species_library, 'value', None):
            return self._aerosol_species_library.value
        return self._aerosol_species_library
    
    @aerosol_species_library.setter
    def aerosol_species_library(self, value: AerosolSpeciesLibrary):
        if isinstance(value, property):
            self._aerosol_species_library = None
        elif isinstance(value, AerosolSpeciesLibrary):
            self._aerosol_species_library = value
        else:
            raise ValueError(f'Invalid aerosol_species_library: {value}')
        
    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter: str, value: str):
            if getattr(self, parameter) is not None:
                value = value.strip('[]').replace(',','')
                parameters.append(f'{parameter} {value}')

        add_parameter('aerosol_default', f'{self.aerosol_default}')
        add_parameter('aerosol_season', f'{self.aerosol_season}')
        add_parameter('aerosol_visibility', f'{self.aerosol_visibility}')
        add_parameter('aerosol_species', f'{self.aerosol_species}')
        add_parameter('aerosol_species_library', f'{self.aerosol_species_library}')

        return '\n'.join(parameters)