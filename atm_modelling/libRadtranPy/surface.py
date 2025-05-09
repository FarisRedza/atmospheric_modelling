import dataclasses
import enum
import typing

from .units import *

@dataclasses.dataclass
class Surface:
    altitude: km = 0
    albedo: float = 0

    def __post_init__(self):
        if not isinstance(self.altitude, typing.Union[float, int, None]):
            raise ValueError(f'Invalid altitude: {self.altitude}')

        if not isinstance(self.albedo, typing.Union[float, int, None]) or self.albedo < 0 or self.albedo > 1:
            raise ValueError(f'Invalid albedo: {self.albedo}')
        
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
                        raise Exception(f'Unknown type {type(parameter)}: {parameter}')


        add_parameter(self.altitude)
        add_parameter(self.albedo)

        return '\n'.join(parameters)