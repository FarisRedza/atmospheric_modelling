import dataclasses
import enum
import typing

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
    atmosphere_file: Atmosphere = Atmosphere.USSTANDARD
    mol_abs_param: tuple[CKScheme, str] | None = None
    mol_modify: list | None = None
    crs_model: tuple[MolID, CRSModel] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.atmosphere_file, typing.Union[Atmosphere, None]):
            raise ValueError(f'Invalid atmosphere_file: {self.atmosphere_file}')
      
        if not isinstance(self.mol_abs_param, typing.Union[tuple, None]):
            raise ValueError(f'Invalid mol_abs_param: {self.mol_abs_param}')
        
        if not isinstance(self.mol_modify, typing.Union[list, None]):
            raise ValueError(f'Invalid mol_modify: {self.mol_modify}')
        
        if not isinstance(self.crs_model, typing.Union[tuple, None]):
            raise ValueError(f'Invalid crs_model: {self.crs_model}')

    def generate_uvspec_input(self) -> str:
        parameters = []
        def add_parameter(parameter, prefix: str = '', suffix: str = '') -> None:
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
                    case list():
                        parameters.append(f'{field_name} {" ".join([str(i) for i in parameter])}')
                    case _:
                        raise Exception(f'Unknown type {type(parameter)}: {parameter}')

        add_parameter(
            parameter=self.atmosphere_file,
            prefix='../data/atmmod/',
            suffix='.dat'
        )
        add_parameter(self.mol_abs_param)
        add_parameter(self.mol_modify)
        add_parameter(self.crs_model)

        return '\n'.join(parameters)

def ppmv_to_cm_2(ppmv: float):
    pass