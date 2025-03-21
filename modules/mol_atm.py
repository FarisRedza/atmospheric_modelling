import dataclasses
import enum

class Atmosphere(enum.Enum):
    MIDLATTITUDESUMMER = "afglms"
    MIDLATTITUDEWINTER = "afglmw"
    SUBARCTICSUMMER = "afglss"
    SUBARCTICWINTER = "afglsw"
    TROPICAL = "afglt"
    USSTANDARD = "afglus"

class CKScheme(enum.Enum):
    KATO = 'kato'
    KATO2 = 'kato2'
    KATO2_96 = 'kato2.96'
    KATO2ANDWANDJI = 'kato2andwandji'
    FU = 'fu'
    AVHRR_KRATZ = 'avhrr_kratz'
    SPDART = 'spdart'
    LOWTRAN = 'lowtran'
    REPTRAN = 'reptran'
    REPTRAN_CHANNEL = 'reptran_channel'
    CRS = 'crs'
    USER_DEFINED = 'user_defined'

class MolID(enum.Enum):
    NO2 = 'no2'
    O3 = 'o3'
    O4 = 'o4'
    RAYLEIGH = 'rayleigh'

class CRSModel(enum.Enum):
    BASS_AND_PAUR = 'bass_and_paur'
    MOLINA = 'molina'
    DAUMONT = 'daumont'
    SERDYUCHENKO = 'serdyuchenko'
    BOGUMIL = 'bogumil'
    BODHAINE = 'bodhaine'
    BODHAINE29 = 'bodhain29'
    NICOLET = 'nicolet'
    PENNDORF = 'penndorf'
    BURROWS = 'burrows'
    VANDAELE = 'vandale'
    GREENBLATT = 'greenblatt'
    THALMAN = 'thalman'

@dataclasses.dataclass
class MolAtm:
    atmosphere: Atmosphere = None
    mol_abs_param: tuple[CKScheme, str] = None
    mol_modify: list = None
    crs_model: tuple[MolID, CRSModel] = None

    @property
    def atmosphere(self) -> str:
        if getattr(self._atmosphere, 'value', None):
            return self._atmosphere.value
        return self._atmosphere

    @atmosphere.setter
    def atmosphere(self, value: Atmosphere):
        if isinstance(value, property):
            self._atmosphere = None
        elif isinstance(value, Atmosphere):
            self._atmosphere = value
        else:
            raise ValueError(f'Invalid atmosphere: {value}')

    @property
    def mol_abs_param(self) -> tuple:
        return self._mol_abs_param
    
    @mol_abs_param.setter
    def mol_abs_param(self, value: tuple):
        if isinstance(value, property):
            self._mol_abs_param = None
        elif isinstance(value, tuple):
            self._mol_abs_param = value
        else:
            raise ValueError(f'Invalid mol_abs_param: {value}')

    @property
    def mol_modify(self) -> list:
        return self._mol_modify
    
    @mol_modify.setter
    def mol_modify(self, value: list):
        if isinstance(value, property):
            self._mol_modify = None
        elif isinstance(value, list):
            self._mol_modify = value
        else:
            raise ValueError(f'Invalid mol_modify: {value}')

    @property
    def crs_model(self) -> tuple:
        return self._crs_model
    
    @crs_model.setter
    def crs_model(self, value: tuple):
        if isinstance(value, property):
            self._crs_model = None
        elif isinstance(value, tuple):
            self._crs_model = value
        else:
            raise ValueError(f'Invalid crs_model: {value}')

    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter: str, value):
            if getattr(self, parameter) is not None:
                if isinstance(value, tuple):
                    if isinstance(value[1], str):
                        value_str = f'{value[0].value} {value[1]}'
                    else:
                        value_str = f'{value[0].value} {value[1].value}'
                else:
                    value_str = str(value).strip('[]').replace(',','')
                parameters.append(f'{parameter} {value_str}')

        add_parameter('atmosphere', self.atmosphere)
        add_parameter('mol_abs_param', self.mol_abs_param)
        if self.mol_modify is not None:
                for i in self.mol_modify:
                    add_parameter('mol_modify', i)
        add_parameter('crs_model', self.crs_model)

        return '\n'.join(parameters)