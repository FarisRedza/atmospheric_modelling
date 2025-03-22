import dataclasses
import enum
import typing
import datetime

from .units import *

@dataclasses.dataclass
class Geometry:
    sza: degrees = None
    phi0: float = None
    phi: float = None
    umu: float = None
    day_of_year: float = None
    latitude: str = None
    longitude: str = None
    time: str = None

    @property
    def sza(self) -> degrees:
        return self._sza
    
    @sza.setter
    def sza(self, value: degrees):
        if isinstance(value, property):
            self._sza = None
        elif isinstance(value, typing.Union[float, int]):
            self._sza = value
        else:
            raise ValueError(f'Invalid sza: {value}')

    @property
    def phi0(self) -> float:
        return self._phi0
    
    @phi0.setter
    def phi0(self, value: float):
        if isinstance(value, property):
            self._phi0 = None
        elif isinstance(value, typing.Union[float, int]):
            self._phi0 = value
        else:
            raise ValueError(f'Invalid phi0: {value}')

    @property
    def phi(self) -> float:
        return self._phi
    
    @phi.setter
    def phi(self, value: float):
        if isinstance(value, property):
            self._phi = None
        elif isinstance(value, typing.Union[float, int]):
            self._phi = value
        else:
            raise ValueError(f'Invalid phi: {value}')

    @property
    def umu(self) -> float:
        return self._umu
    
    @umu.setter
    def umu(self, value: float):
        if isinstance(value, property):
            self._umu = None
        elif isinstance(value, typing.Union[float, int]):
            self._umu = value
        else:
            raise ValueError(f'Invalid umu: {value}')

    @property
    def day_of_year(self) -> float:
        return self._day_of_year
    
    @day_of_year.setter
    def day_of_year(self, value: float):
        if isinstance(value, property):
            self._day_of_year = None
        elif isinstance(value, typing.Union[float, int]):
            self._day_of_year = value
        else:
            raise ValueError(f'Invalid day_of_year: {value}')

    @property
    def latitude(self) -> str:
        return self._latitude
    
    @latitude.setter
    def latitude(self, value: str):
        if isinstance(value, property):
            self._latitude = None
        elif isinstance(value, str):
            self._latitude = value
        else:
            raise ValueError(f'Invalid latitude: {value}')

    @property
    def longitude(self) -> str:
        return self._longitude
    
    @longitude.setter
    def longitude(self, value: str):
        if isinstance(value, property):
            self._longitude = None
        elif isinstance(value, str):
            self._longitude = value
        else:
            raise ValueError(f'Invalid longitude: {value}')

    @property
    def time(self) -> datetime.datetime:
        return self._time
    
    @time.setter
    def time(self, value: str):
        if isinstance(value, property):
            self._time = None
        elif isinstance(value, str):
            self._time = value
        else:
            raise ValueError(f'Invalid time: {value}')
        
    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter: str, value: str):
            if getattr(self, parameter) is not None:
                value = value.strip('[]').replace(',','')
                parameters.append(f'{parameter} {value}')

        add_parameter('sza', f'{self.sza}')
        add_parameter('phi0', f'{self.phi0}')
        add_parameter('phi', f'{self.phi}')
        add_parameter('umu', f'{self.umu}')
        add_parameter('day_of_year', f'{self.day_of_year}')
        add_parameter('latitude', f'{self.latitude}')
        add_parameter('longitude', f'{self.longitude}')
        add_parameter('time', f'{self.time}')

        return '\n'.join(parameters)