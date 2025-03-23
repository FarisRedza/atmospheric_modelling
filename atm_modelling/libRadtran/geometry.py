import dataclasses
import enum
import typing
import datetime

from .units import *

@dataclasses.dataclass
class Geometry:
    sza: degrees = None
    phi0: float = None
    phi: float = None
    umu: float = None
    day_of_year: float = None
    latitude: str = None
    longitude: str = None
    time: str = None

    def __post_init__(self):
        if not isinstance(self.sza, typing.Union[float, int, None]):
            raise ValueError(f'Invalid sza: {self.sza}')
        
        if not isinstance(self.phi0, typing.Union[float, int, None]):
            raise ValueError(f'Invalid phi0: {self.phi0}')
        
        if not isinstance(self.phi, typing.Union[float, int, None]):
            raise ValueError(f'Invalid phi: {self.phi}')
        
        if not isinstance(self.umu, typing.Union[float, int, None]):
            raise ValueError(f'Invalid umu: {self.umu}')
        
        if not isinstance(self.day_of_year, typing.Union[float, int, None]):
            raise ValueError(f'Invalid day_of_year: {self.day_of_year}')
        
        if not isinstance(self.latitude, typing.Union[str, None]):
            raise ValueError(f'Invalid latitude: {self.latitude}')
        
        if not isinstance(self.longitude, typing.Union[str, None]):
            raise ValueError(f'Invalid longitude: {self.longitude}')
        
        if not isinstance(self.time, typing.Union[str, None]):
            raise ValueError(f'Invalid time: {self.time}')
        
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

        add_parameter(self.sza)
        add_parameter(self.phi0)
        add_parameter(self.phi)
        add_parameter(self.umu)
        add_parameter(self.day_of_year)
        add_parameter(self.latitude)
        add_parameter(self.longitude)
        add_parameter(self.time)

        return '\n'.join(parameters)