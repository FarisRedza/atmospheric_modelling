import sys
import pathlib

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import widgets

sys.path.append(str(pathlib.Path.cwd()))
import atm_modelling.libRadtranPy.general_atm as general_atm

class GeneralAtmPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()
        settings = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings)

        self.absorption = True
        self.scattering = True
        self.zout_interpolate = False
        self.reverse_atmosphere = False

        absorption_row = widgets.SwitchRow(
            title='Absorption',
            callable=self.set_absorption,
            active=self.get_absorption()
        )
        settings.add(child=absorption_row)

        scattering_row = widgets.SwitchRow(
            title='Scattering',
            callable=self.set_scattering,
            active=self.get_scattering()
        )
        settings.add(child=scattering_row)

        zout_interpolate_row = widgets.SwitchRow(
            title='Zout interpolate',
            callable=self.set_zout_interpolate,
            active=self.get_zout_interpolate()
        )
        settings.add(child=zout_interpolate_row)

        reverse_atmosphere_row = widgets.SwitchRow(
            title='Reverse Atmosphere',
            callable=self.set_reverse_atmosphere,
            active=self.get_reverse_atmosphere()
        )
        settings.add(child=reverse_atmosphere_row)
    
    def set_absorption(self, absorption: bool) -> None:
        self.absorption = absorption
    
    def get_absorption(self) -> bool:
        return self.absorption

    def set_scattering(self, scattering: bool) -> None:
        self.scattering = scattering
    
    def get_scattering(self) -> bool:
        return self.scattering

    def set_zout_interpolate(self, zout_interpolate: bool) -> None:
        self.zout_interpolate = zout_interpolate
    
    def get_zout_interpolate(self) -> bool:
        return self.zout_interpolate

    def set_reverse_atmosphere(self, reverse_atmosphere: bool) -> None:
        self.reverse_atmosphere = reverse_atmosphere
    
    def get_reverse_atmosphere(self) -> bool:
        return self.reverse_atmosphere
    
    def general_atm_settings(self) -> general_atm.GeneralAtm:
        settings = general_atm.GeneralAtm(
            no_absorption=not self.absorption,
            no_scattering=not self.scattering,
            zout_interpolate=self.zout_interpolate,
            reverse_atmosphere=self.reverse_atmosphere
        )
        return settings