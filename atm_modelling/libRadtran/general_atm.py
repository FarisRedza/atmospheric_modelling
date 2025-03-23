import dataclasses
import enum

@dataclasses.dataclass
class GeneralAtm:
    no_absorption: bool = False
    no_scattering: bool = False
    zout_interpolate: bool = False
    reverse_atmosphere: bool = False

    def __post_init__(self):
        if not isinstance(self.no_absorption, bool):
            raise ValueError(f'Invalid no_absorption: {self.no_absorption}')
        
        if not isinstance(self.no_scattering, bool):
            raise ValueError(f'Invalid no_scattering: {self.no_scattering}')
        
        if not isinstance(self.zout_interpolate, bool):
            raise ValueError(f'Invalid zout_interpolate: {self.zout_interpolate}')
        
        if not isinstance(self.reverse_atmosphere, bool):
            raise ValueError(f'Invalid reverse_atmosphere: {self.reverse_atmosphere}')
        
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

        add_parameter(self.no_absorption)
        add_parameter(self.no_scattering)
        add_parameter(self.zout_interpolate)
        add_parameter(self.reverse_atmosphere)

        return '\n'.join(parameters)