import sys
import pathlib
import typing

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import widgets

sys.path.append(str(pathlib.Path.cwd()))
import atm_modelling.libRadtranPy.mol_atm as mol_atm

class MolAtmPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()
        settings = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings)

        self.atmosphere = mol_atm.Atmosphere.MIDLATTITUDESUMMER

        atmosphere_string_list = Gtk.StringList(
            strings=[i.name for i in mol_atm.Atmosphere]
        )     
        source_row = widgets.DropdownRow(
            title='Solver',
            string_list=atmosphere_string_list,
            selected=list(mol_atm.Atmosphere).index(self.get_atmosphere())
        )
        settings.add(child=source_row)

    def set_atmosphere(self, atmosphere: mol_atm.Atmosphere) -> None:
        self.atmosphere = atmosphere
    
    def get_atmosphere(self) -> mol_atm.Atmosphere:
        return self.atmosphere