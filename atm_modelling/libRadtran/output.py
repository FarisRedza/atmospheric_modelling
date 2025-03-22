import dataclasses
import enum

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
    output_user: str = None
    output_quantity: OutputQuantity = None
    output_process: OutputProcess = None
    output_format: OutputFormat = None
    zout: ZOut = None

    @property
    def output_user(self) -> str:
        return self._output_user
    
    @output_user.setter
    def output_user(self, value: str):
        if isinstance(value, property):
            self._output_user = None
        elif isinstance(value, str):
            self._output_user = value
        else:
            raise ValueError(f'Invalid output_user: {value}')

    @property
    def output_quantity(self) -> str:
        if getattr(self._output_quantity, 'value', None):
            return self._output_quantity.value
        return self._output_quantity
    
    @output_quantity.setter
    def output_quantity(self, value: OutputQuantity):
        if isinstance(value, property):
            self._output_quantity = None
        elif isinstance(value, OutputQuantity):
            self._output_quantity = value
        else:
            raise ValueError(f'Invalid output_quantity: {value}')

    @property
    def output_process(self) -> str:
        if getattr(self._output_process, 'value', None):
            return self._output_process.value
        return self._output_process
    
    @output_process.setter
    def output_process(self, value: OutputProcess):
        if isinstance(value, property):
            self._output_process = None
        elif isinstance(value, OutputProcess):
            self._output_process = value
        else:
            raise ValueError(f'Invalid output_process: {value}')

    @property
    def output_format(self) -> str:
        if getattr(self._output_format, 'value', None):
            return self._output_format.value
        return self._output_format
    
    @output_format.setter
    def output_format(self, value: OutputFormat):
        if isinstance(value, property):
            self._output_format = None
        elif isinstance(value, OutputFormat):
            self._output_format = value
        else:
            raise ValueError(f'Invalid output_format: {value}')

    @property
    def zout(self) -> str:
        if getattr(self._zout, 'value', None):
            return self._zout.value
        return self._zout

    @zout.setter
    def zout(self, value: str):
        if isinstance(value, property):
            self._zout = None
        elif isinstance(value, str):
            self._zout = value
        else:
            raise ValueError(f'Invalid z_out: {value}')

    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter: str, value: str):
            if getattr(self, parameter) is not None:
                value = value.strip('[]').replace(',','')
                parameters.append(f'{parameter} {value}')

        add_parameter('output_user', f'{self.output_user}')
        add_parameter('output_quantity', f'{self.output_quantity}')
        add_parameter('output_process', f'{self.output_process}')
        add_parameter('output_format', f'{self.output_format}')
        add_parameter('zout', f'{self.zout}')

        return '\n'.join(parameters)