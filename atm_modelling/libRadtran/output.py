import dataclasses
import enum
import typing

class OutputQuantity(enum.Enum):
    BRIGHTNESS = "brightness"
    REFLECTIVITY = "reflectivity"
    TRANSMITTANCE = "transmittance"

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
    TOA = "TOA"

@dataclasses.dataclass
class Output:
    quiet: bool = False
    verbose: bool = False
    output_user: str = None
    output_quantity: OutputQuantity = None
    output_process: OutputProcess = None
    output_format: OutputFormat = OutputFormat.ASCII
    zout: ZOut = None

    def __post_init__(self):
        if not isinstance(self.quiet, bool):
            raise ValueError(f'Invalid quiet: {self.quiet}')

        if not isinstance(self.verbose, bool):
            raise ValueError(f'Invalid verbose: {self.verbose}')

        if not isinstance(self.output_user, typing.Union[str, None]):
            raise ValueError(f'Invalid output_user: {self.output_user}')
      
        if not isinstance(self.output_quantity, typing.Union[OutputQuantity, None]):
            raise ValueError(f'Invalid output_quantity: {self.output_quantity}')
        
        if not isinstance(self.output_process, typing.Union[OutputProcess, None]):
            raise ValueError(f'Invalid output_process: {self.output_process}')
        
        if not isinstance(self.output_format, typing.Union[OutputFormat, None]):
            raise ValueError(f'Invalid output_format: {self.output_format}')
        
        if not isinstance(self.zout, typing.Union[ZOut, None]):
            raise ValueError(f'Invalid zout: {self.zout}')

    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter, prefix: str = '', suffix: str = ''):
            for field in dataclasses.fields(self):
                if getattr(self, field.name) is parameter:
                    field_name = field.name
                    break

            if getattr(self, field_name) is not None:
                match parameter:
                    case str():
                        parameters.append(f'{field_name} {parameter}')
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
                        raise Exception(f'Unknown type {type(parameter)}')

        add_parameter(self.quiet)
        add_parameter(self.verbose)
        add_parameter(self.output_user)
        add_parameter(self.output_quantity)
        add_parameter(self.output_process)
        add_parameter(self.output_format)
        add_parameter(self.zout)

        return '\n'.join(parameters)