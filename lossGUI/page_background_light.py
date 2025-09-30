import sys
import pathlib
import typing

import numpy as np

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import widgets

class BackgroundLightGroup(Adw.PreferencesGroup):
    def __init__(
            self
    ) -> None:
        super().__init__(title='Settings')
        self._wavelength = 785e-9
        self._satellite_alt = 500e3
        self._satellite_fov = 0.3
        self._earth_albedo = 0.3
        self._moon_albedo = 0.12

        wavelength_alt_row = widgets.EntryRow(
            title='Wavelength',
            callable=self.set_wavelength,
            value=self.get_wavelength()
        )
        self.add(child=wavelength_alt_row)

        satellite_alt_row = widgets.EntryRow(
            title='Satellite altitude',
            callable=self.set_satellite_alt,
            value=self.get_satellite_alt()
        )
        self.add(child=satellite_alt_row)

        satellite_fov_row = widgets.EntryRow(
            title='Satellite FOV',
            callable=self.set_satellite_fov,
            value=self.get_satellite_fov()
        )
        self.add(child=satellite_fov_row)

        earth_albedo_row = widgets.EntryRow(
            title='Earth albedo',
            callable=self.set_earth_albedo,
            value=self.get_earth_albedo()
        )
        self.add(child=earth_albedo_row)

        moon_albedo_row = widgets.EntryRow(
            title='Moon albedo',
            callable=self.set_moon_albedo,
            value=self.get_moon_albedo()
        )
        self.add(child=moon_albedo_row)

    def set_wavelength(self, wavelength: float) -> None:
        self._wavelength = wavelength
    
    def get_wavelength(self) -> float:
        return self._wavelength

    def set_satellite_alt(self, altitude: float) -> None:
        self._satellite_alt = altitude
    
    def get_satellite_alt(self) -> float:
        return self._satellite_alt

    def set_satellite_fov(self, fov: float) -> None:
        self._satellite_fov = fov
    
    def get_satellite_fov(self) -> float:
        return self._satellite_fov

    def set_earth_albedo(self, albedo: float) -> None:
        self._earth_albedo = albedo
    
    def get_earth_albedo(self) -> float:
        return self._earth_albedo

    def set_moon_albedo(self, albedo: float) -> None:
        self._moon_albedo = albedo
    
    def get_moon_albedo(self) -> float:
        return self._moon_albedo


class BackgroundLightPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()

        backgroun_light_group = BackgroundLightGroup()
        self.add(group=backgroun_light_group)
