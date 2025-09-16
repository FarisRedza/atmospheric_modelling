import sys
import pathlib
import typing

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import widgets

sys.path.append(str(pathlib.Path.cwd()))
import atm_modelling.libRadtranPy.geometry as geometry

class GeometryPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()
        settings = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings)

        self.sza = 0.0
        self.phi0 = 0.0
        self.phi = 0.0
        self.umu = 0.0
        self.day_of_year = 0.0
        self.latitude = ''
        self.longitude = ''
        self.time = ''

        sza_row = widgets.EntryRow(
            title='Solar zenith angle',
            subtitle='sza',
            text=str(self.get_sza()),
            placeholder_text='°'
        )
        settings.add(child=sza_row)

        phi0_row = widgets.EntryRow(
            title='Horizon angle of the sun',
            subtitle='phi0',
            text=str(self.get_phi0()),
            placeholder_text='°'
        )
        settings.add(child=phi0_row)

        phi_row = widgets.EntryRow(
            title='Viewing azimuthal angle',
            subtitle='phi',
            text=str(self.get_phi()),
            placeholder_text='°'
        )
        settings.add(child=phi_row)

        umu_row = widgets.EntryRow(
            title='Viewing zenith angle',
            subtitle='umu',
            text=str(self.get_umu()),
            placeholder_text='°'
        )
        settings.add(child=umu_row)

        day_of_year_row = widgets.EntryRow(
            title='Day of year',
            text=str(self.get_day_of_year())
        )
        settings.add(child=day_of_year_row)

        latitude_row = widgets.EntryRow(
            title='Latitude',
            text=str(self.get_latitude())
        )
        settings.add(child=latitude_row)

        longitude_row = widgets.EntryRow(
            title='Longitude',
            text=str(self.get_longitude())
        )
        settings.add(child=longitude_row)

        time_row = widgets.EntryRow(
            title='Time',
            text=str(self.get_time())
        )
        settings.add(child=time_row)

    def set_sza(self, sza: float) -> None:
        self.sza = sza
    
    def get_sza(self) -> float:
        return self.sza

    def set_phi0(self, phi0: float) -> None:
        self.phi0 = phi0
    
    def get_phi0(self) -> float:
        return self.phi0

    def set_phi(self, phi: float) -> None:
        self.phi = phi
    
    def get_phi(self) -> float:
        return self.phi

    def set_umu(self, umu: float) -> None:
        self.umu = umu

    def get_umu(self) -> float:
        return self.umu

    def set_day_of_year(self, day_of_year: float) -> None:
        self.day_of_year = day_of_year
    
    def get_day_of_year(self) -> float:
        return self.day_of_year

    def set_latitude(self, latitude: str) -> None:
        self.latitude = latitude

    def get_latitude(self) -> str:
        return self.latitude
    
    def set_longitude(self, longitude: str) -> None:
        self.longitude = longitude
    
    def get_longitude(self) -> str:
        return self.longitude

    def set_time(self, time: str) -> None:
        self.time = time
    
    def get_time(self) -> str:
        return self.time