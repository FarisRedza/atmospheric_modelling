import dataclasses
import enum

class RTESolver(enum.Enum):
    DISORT = "disort"
    MYSTIC = "MYSTIC"
    FDISORT1 = "fdisort1"
    FDISORT2 = "fdisort2"
    TWOSTR = "twostr"
    RODENTS = "rodents"
    SDISORT = "sdisort"
    SPSDISORT = "spsdisort"
    TZS = "tzs"
    SSS = "sss"
    SSLIDAR = "sslidar"

rte_solver: RTESolver = None

@dataclasses.dataclass
class Solver:
    rte_solver: RTESolver = None

    @property
    def rte_solver(self) -> str:
        if getattr(self._rte_solver, 'value', None):
            return self._rte_solver.value
        return self._rte_solver
    
    @rte_solver.setter
    def rte_solver(self, value: RTESolver):
        if isinstance(value, property):
            self._rte_solver = None
        elif isinstance(value, RTESolver):
            self._rte_solver = value
        else:
            raise ValueError(f'Invalid rte_solver: {value}')
        
    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter: str, value: str):
            if getattr(self, parameter) is not None:
                value = value.strip('[]').replace(',','')
                parameters.append(f'{parameter} {value}')

        add_parameter('rte_solver', f'{self.rte_solver}')

        return '\n'.join(parameters)