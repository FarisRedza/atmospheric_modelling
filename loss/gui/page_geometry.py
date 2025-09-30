import sys
import os
import typing

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GObject

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
import libRadtranPy.geometry

class Geometry(Adw.PreferencesPage):
    def __init__(
            self,
            set_settings_callback: typing.Callable,
            get_settings_callback: typing.Callable
    ) -> None:
        super().__init__()
        self.set_settings_callback = set_settings_callback
        self.get_settings_callback = get_settings_callback

        settings_group = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings_group)

        # sza row
        sza_row = Adw.ActionRow(title='Solar zenith angle')
        settings_group.add(child=sza_row)

        sza_entry = Gtk.Entry(
            valign=Gtk.Align.CENTER
        )
        sza_entry.connect(
            'activate',
            self.on_set_sza,
        )
        sza_row.add_suffix(widget=sza_entry)

        # phi0 row
        phi0_row = Adw.ActionRow(title='Phi0')
        settings_group.add(child=phi0_row)

        phi0_entry = Gtk.Entry(
            valign=Gtk.Align.CENTER
        )
        phi0_entry.connect(
            'activate',
            self.on_set_phi0,
        )
        phi0_row.add_suffix(widget=phi0_entry)

        # phi row
        phi_row = Adw.ActionRow(title='Phi')
        settings_group.add(child=phi_row)

        phi_entry = Gtk.Entry(
            valign=Gtk.Align.CENTER
        )
        phi_entry.connect(
            'activate',
            self.on_set_phi,
        )
        phi_row.add_suffix(widget=phi_entry)

        # umu row
        umu_row = Adw.ActionRow(title='Umu')
        settings_group.add(child=umu_row)

        umu_entry = Gtk.Entry(
            valign=Gtk.Align.CENTER
        )
        umu_entry.connect(
            'activate',
            self.on_set_umu,
        )
        umu_row.add_suffix(widget=umu_entry)

        # day of year row
        day_of_year_row = Adw.ActionRow(title='Day of year')
        settings_group.add(child=day_of_year_row)

        day_of_year_entry = Gtk.Entry(
            valign=Gtk.Align.CENTER
        )
        day_of_year_entry.connect(
            'activate',
            self.on_set_day_of_year,
        )
        day_of_year_row.add_suffix(widget=day_of_year_entry)

        # latitude row
        latitude_row = Adw.ActionRow(title='Latitude')
        settings_group.add(child=latitude_row)

        latitude_entry = Gtk.Entry(
            valign=Gtk.Align.CENTER
        )
        latitude_entry.connect(
            'activate',
            self.on_set_latitude,
        )
        latitude_row.add_suffix(widget=latitude_entry)

        # longitude row
        longitude_row = Adw.ActionRow(title='Longitude')
        settings_group.add(child=longitude_row)

        longitude_entry = Gtk.Entry(
            valign=Gtk.Align.CENTER
        )
        longitude_entry.connect(
            'activate',
            self.on_set_longitude,
        )
        longitude_row.add_suffix(widget=longitude_entry)

        # time row
        time_row = Adw.ActionRow(title='Time')
        settings_group.add(child=time_row)

        time_entry = Gtk.Entry(
            valign=Gtk.Align.CENTER
        )
        time_entry.connect(
            'activate',
            self.on_set_time,
        )
        time_row.add_suffix(widget=time_entry)

    def on_set_sza(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtranPy.geometry.Geometry = self.get_settings_callback()
        settings.sza = float(entry.get_text())
        self.set_settings_callback(settings=settings)

    def on_set_phi0(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtranPy.geometry.Geometry = self.get_settings_callback()
        settings.phi0 = float(entry.get_text())
        self.set_settings_callback(settings=settings)

    def on_set_phi(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtranPy.geometry.Geometry = self.get_settings_callback()
        settings.phi = float(entry.get_text())
        self.set_settings_callback(settings=settings)

    def on_set_umu(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtranPy.geometry.Geometry = self.get_settings_callback()
        settings.umu = float(entry.get_text())
        self.set_settings_callback(settings=settings)

    def on_set_day_of_year(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtranPy.geometry.Geometry = self.get_settings_callback()
        settings.day_of_year = float(entry.get_text())
        self.set_settings_callback(settings=settings)

    def on_set_latitude(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtranPy.geometry.Geometry = self.get_settings_callback()
        settings.latitude = float(entry.get_text())
        self.set_settings_callback(settings=settings)

    def on_set_longitude(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtranPy.geometry.Geometry = self.get_settings_callback()
        settings.longitude = float(entry.get_text())
        self.set_settings_callback(settings=settings)

    def on_set_time(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtranPy.geometry.Geometry = self.get_settings_callback()
        settings.time = float(entry.get_text())
        self.set_settings_callback(settings=settings)