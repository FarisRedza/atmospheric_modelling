import dataclasses
import enum
import typing
import pathlib

class Atmosphere(enum.Enum):
    MIDLATITUDE_SUMMER = "afglms"
    MIDLATITUDE_WINTER = "afglmw"
    SUBARCTIC_SUMMER = "afglss"
    SUBARCTIC_WINTER = "afglsw"
    TROPICAL = "afglt"
    US_STANDARD = "afglus"

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

class Species(enum.Enum):
    O2 = 'O2'
    H2O = 'H2O'
    CO2 = 'CO2'
    NO2 = 'NO2'
    CH4 = 'CH4'
    N2O = 'N2O'
    F11 = 'F11'
    F12 = 'F12'
    F22 = 'F22'

@dataclasses.dataclass
class MolAtm:
    atmosphere_file: Atmosphere | str = Atmosphere.US_STANDARD
    mixing_ratio: tuple[Species, str] | None = None
    mol_abs_param: tuple[CKScheme, str] | None = None
    mol_modify: list | None = None
    crs_model: tuple[MolID, CRSModel] | None = None
    _libRadtran_version = '2.0.6'
    _libRadtran_dir = pathlib.Path(__file__).parent.parent.parent.joinpath(
        f'libRadtran-{_libRadtran_version}',
    )

    def __post_init__(self) -> None:
        if not isinstance(self.atmosphere_file, typing.Union[Atmosphere, str, None]):
            raise ValueError(f'Invalid atmosphere_file: {self.atmosphere_file}')

        if not isinstance(self.mixing_ratio, typing.Union[tuple, None]):
            raise ValueError(f'Invalid mixing_ratio: {self.mixing_ratio}')

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
                    
                    case tuple():
                        parameters.append(f'{field_name} {" ".join([(i.name if isinstance(i, Species) else i) for i in parameter])}')

                    case str():
                        parameters.append(f'{field_name} {parameter}')
                    case _:
                        raise Exception(f'Unknown type {type(parameter)}: {parameter}')

        add_parameter(
            parameter=self.atmosphere_file,
            prefix=f'{self._libRadtran_dir.joinpath(
                'data',
                'atmmod'
            )}/',
            suffix='.dat'
        )
        add_parameter(self.mixing_ratio)
        add_parameter(self.mol_abs_param)
        add_parameter(self.mol_modify)
        add_parameter(self.crs_model)

        return '\n'.join(parameters)

if __name__ == '__main__':
    mol_atm = MolAtm(
        atmosphere_file=Atmosphere.MIDLATITUDE_SUMMER,
        mixing_ratio=(Species.CO2, '365.0')
    )
    print(type(mol_atm.mixing_ratio))
    print(mol_atm.generate_uvspec_input())