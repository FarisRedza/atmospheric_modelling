import dataclasses
import enum

class RTESolver(enum.Enum):
    DISORT = 'disort'
    MYSTIC = 'MYSTIC'
    FDISORT1 = 'fdisort1'
    FDISORT2 = 'fdisort2'
    TWOSTR = 'twostr'
    RODENTS = 'rodents'
    SDISORT = 'sdisort'
    SPSDISORT = 'spsdisort'
    TZS = 'tzs'
    SSS = 'sss'
    SSLIDAR = 'sslidar'

@dataclasses.dataclass
class Solver:
    rte_solver: RTESolver = RTESolver.DISORT

    def __post_init__(self):
        if not isinstance(self.rte_solver, RTESolver):
            raise ValueError(f'Invalid rte_solver: {self.rte_solver}')
        
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

        add_parameter(self.rte_solver)

        return '\n'.join(parameters)