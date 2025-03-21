import dataclasses
import enum

@dataclasses.dataclass
class GeneralAtm:
    absorption: bool = None
    scattering: bool = None
    zout_interpolate: bool = None
    reverse_atmosphere: bool = None

    @property
    def absorption(self) -> bool:
        return self._absorption
    
    @absorption.setter
    def absorption(self, value: bool):
        if isinstance(value, property):
            self._absorption = None
        elif isinstance(value, bool):
            self._absorption = value
        else:
            raise ValueError(f'Invalid absorption: {value}')

    @property
    def scattering(self) -> bool:
        return self._scattering
    
    @scattering.setter
    def scattering(self, value: bool):
        if isinstance(value, property):
            self._scattering = None
        elif isinstance(value, bool):
            self._scattering = value
        else:
            raise ValueError(f'Invalid scattering: {value}')

    @property
    def zout_interpolate(self) -> bool:
        return self._zout_interpolate
    
    @zout_interpolate.setter
    def zout_interpolate(self, value: bool):
        if isinstance(value, property):
            self._zout_interpolate = None
        elif isinstance(value, bool):
            self._zout_interpolate = value
        else:
            raise ValueError(f'Invalid zout_interpolate: {value}')

    @property
    def reverse_atmosphere(self) -> bool:
        return self._reverse_atmosphere
    
    @reverse_atmosphere.setter
    def reverse_atmosphere(self, value: bool):
        if isinstance(value, property):
            self._reverse_atmosphere = None
        elif isinstance(value, bool):
            self._reverse_atmosphere = value
        else:
            raise ValueError(f'Invalid reverse_atmosphere: {value}')

    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter: str, value: str = None):
            if getattr(self, parameter) is not None:
                if value == None:
                    parameters.append(parameter)
                else:
                    value = value.strip('[]').replace(',','')
                    parameters.append(f'{parameter} {value}')

        add_parameter('absorption')
        add_parameter('scattering')
        add_parameter('zout_interpolate')
        add_parameter('reverse_atmosphere')

        return '\n'.join(parameters)