import dataclasses
import enum

class Source(enum.Enum):
    SOLAR = 'solar'
    THERMAL = 'thermal'

@dataclasses.dataclass
class Spectral:
    wavelength: list = None
    source: Source = None

    @property
    def wavelength(self) -> list:
        return self._wavelength
    
    @wavelength.setter
    def wavelength(self, value: list):
        if isinstance(value, property):
            self._wavelength = None
        elif isinstance(value, list):
            self._wavelength = value
        else:
            raise ValueError(f'Invalid wavelength: {value}')

    @property
    def source(self) -> str:
        if getattr(self._source, 'value', None):
            return self._source.value
        return self._source
    
    @source.setter
    def source(self, value: Source):
        if isinstance(value, property):
            self._source = None
        elif not isinstance(value, Source):
            raise ValueError(f'Invalid source: {value}')
        else:
            self._source = value

    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter: str, value: str):
            if getattr(self, parameter) is not None:
                value = value.strip('[]').replace(',','')
                parameters.append(f'{parameter} {value}')

        add_parameter('wavelength', f'{self.wavelength}')
        add_parameter('source', f'{self.source}')

        return '\n'.join(parameters)