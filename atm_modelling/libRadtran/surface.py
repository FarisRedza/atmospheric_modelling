import dataclasses
import enum
import typing

from .units import *

@dataclasses.dataclass
class Surface:
    altitude: km = None
    albedo: float = None

    @property
    def altitude(self) -> km:
        return self._altitude
    
    @altitude.setter
    def altitude(self, value: km):
        if isinstance(value, property):
            self._altitude = None
        elif isinstance(value, typing.Union[float, int]):
            self._altitude = value
        else:
            raise ValueError(f'Invalid altitude: {value}')

    @property
    def albedo(self) -> float:
        return self._albedo
    
    @albedo.setter
    def albedo(self, value: float):
        if isinstance(value, property):
            self._albedo = None
        elif isinstance(value, typing.Union[float, int]):
            self._albedo = value
        else:
            raise ValueError(f'Invalid albedo: {value}')
        
    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter: str, value: str):
            if getattr(self, parameter) is not None:
                value = value.strip('[]').replace(',','')
                parameters.append(f'{parameter} {value}')

        add_parameter('altitude', f'{self.altitude}')
        add_parameter('albedo', f'{self.albedo}')

        return '\n'.join(parameters)