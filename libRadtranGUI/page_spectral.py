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

class SpectralPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()
        settings = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings)

        self.wavelength_min = 785.0
        self.wavelength_max = 785.0
        self.source = libradtranpy.Source.SOLAR

        wavelength_row = widgets.DoubleEntryRow(
            title='Wavelength',
            callable_1=self.set_wavelength_min,
            callable_2=self.set_wavelength_max,
            text_1=str(self.get_wavelength_min()),
            text_2=str(self.get_wavelength_max()),
            placeholder_text_1='Min nm',
            placeholder_text_2='Max nm'
        )
        settings.add(child=wavelength_row)

        source_string_list = Gtk.StringList()
        for i in libradtranpy.Source:
            source_string_list.append(i.name)
        source_row = widgets.DropdownRow(
            callable=self.set_source,
            title='Source',
            string_list=source_string_list,
            selected=list(libradtranpy.Source).index(self.get_source())
        )
        settings.add(child=source_row)

    def set_wavelength_min(self, wavelength: float) -> None:
        self.wavelength_min = wavelength
    
    def get_wavelength_min(self) -> float:
        return self.wavelength_min

    def set_wavelength_max(self, wavelength: float) -> None:
        self.wavelength_max = wavelength
    
    def get_wavelength_max(self) -> float:
        return self.wavelength_max

    def set_source(self, source: libradtranpy.Source) -> None:
        self.source = source
    
    def get_source(self) -> libradtranpy.Source:
        return self.source

    def spectral_settings(self) -> libradtranpy.Spectral:
        settings = libradtranpy.Spectral(
            wavelength=[
                libradtranpy.nm(int(self.get_wavelength_min())),
                libradtranpy.nm(int(self.get_wavelength_max()))
            ] if self.get_wavelength_min() != self.get_wavelength_max() else [
                libradtranpy.nm(self.get_wavelength_min())
            ],
            source=self.source
        )
        return settings