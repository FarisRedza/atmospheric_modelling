import dataclasses
import enum
import typing

from .units import *

class Source(enum.Enum):
    SOLAR = 'solar'
    THERMAL = 'thermal'

@dataclasses.dataclass
class Spectral:
    wavelength: typing.List[nm] = None
    source: Source = Source.SOLAR

    def __post_init__(self):  
        if not isinstance(self.wavelength, typing.Union[list, None]):
            raise ValueError(f'Invalid wavelength: {self.wavelength}')
      
        if not isinstance(self.source, typing.Union[Source, None]):
            raise ValueError(f'Invalid source: {self.source}')

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
                    case list():
                        parameters.append(f'{field_name} {" ".join([str(i) for i in parameter])}')
                    case _:
                        raise Exception(f'Unknown type {type(parameter)}: {parameter}')

        add_parameter(self.wavelength)
        add_parameter(self.source)

        return '\n'.join(parameters)