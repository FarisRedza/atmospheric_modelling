import dataclasses
import enum

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
        if getattr(self._mc_polarisation, 'value', None):
            return self._mc_polarisation.value
        return self._mc_polarisation
    
    @mc_polarisation.setter
    def mc_polarisation(self, value: MCPolarisation):
        if isinstance(value, property):
            self._mc_polarisation = None
        elif isinstance(value, MCPolarisation):
            self._mc_polarisation = value
        else:
            raise ValueError(f'Invalid mc_polarisation: {value}')

    @property
    def mc_backward_output(self) -> str:
        if getattr(self._mc_backward_output, 'value', None):
            return self._mc_backward_output.value
        return self._mc_backward_output
    
    @mc_backward_output.setter
    def mc_backward_output(self, value: MCBackwardOutput):
        if isinstance(value, property):
            self._mc_backward_output = None
        elif isinstance(value, MCBackwardOutput):
            self._mc_backward_output = value
        else:
            raise ValueError(f'Invalid mc_backward_output: {value}')

    @property
    def mc_forward_output(self) -> str:
        if getattr(self._mc_forward_output, 'value', None):
            return self._mc_forward_output.value
        return self._mc_forward_output
    
    @mc_forward_output.setter
    def mc_forward_output(self, value: MCForwardOutput):
        if isinstance(value, property):
            self._mc_forward_output = None
        elif isinstance(value, MCForwardOutput):
            self._mc_forward_output = value
        else:
            raise ValueError(f'Invalid mc_forward_output: {value}')

    @property
    def mc_output_unit(self) -> str:
        if getattr(self._mc_output_unit, 'value', None):
            return self._mc_output_unit.value
        return self._mc_output_unit
    
    @mc_output_unit.setter
    def mc_output_unit(self, value: MCOutputUnit):
        if isinstance(value, property):
            self._mc_output_unit = None
        elif isinstance(value, MCOutputUnit):
            self._mc_output_unit = value
        else:
            raise ValueError(f'Invalid mc_output_unit: {value}')
        
    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter: str, value: str):
            if getattr(self, parameter) is not None:
                value = value.strip('[]').replace(',','')
                parameters.append(f'{parameter} {value}')

        add_parameter('mc_polarisation', f'{self.mc_polarisation}')
        add_parameter('mc_backward_output', f'{self.mc_backward_output}')
        add_parameter('mc_forward_output', f'{self.mc_forward_output}')
        add_parameter('mc_output_unit', f'{self.mc_output_unit}')

        return '\n'.join(parameters)