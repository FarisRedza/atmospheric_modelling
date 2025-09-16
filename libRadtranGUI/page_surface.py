import sys
import pathlib
import typing

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import widgets

sys.path.append(str(pathlib.Path.cwd()))
import atm_modelling.libRadtranPy.libradtranpy as libradtranpy

class SurfacePage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()
        settings = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings)

        self.altitude = 0.0
        self.albedo = 0.0

        altitude_row = widgets.EntryRow(
            callable=self.set_altitude,
            title='Altitude',
            text=str(self.get_altitude()),
            placeholder_text='km'
        )
        settings.add(child=altitude_row)

        albedo_row = widgets.EntryRow(
            callable=self.set_albedo,
            title='Albedo',
            text=str(self.get_albedo())
        )
        settings.add(child=albedo_row)

    def set_altitude(self, altitude: float) -> None:
        self.altitude = altitude
    
    def get_altitude(self) -> float:
        return self.altitude

    def set_albedo(self, albedo: float) -> None:
        self.albedo = albedo
    
    def get_albedo(self) -> float:
        return self.albedo

    def surface_settings(self) -> libradtranpy.Surface:
        return libradtranpy.Surface(
            altitude=libradtranpy.km(self.altitude),
            albedo=self.albedo
        )
