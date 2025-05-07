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
import libRadtran.surface

class Surface(Adw.PreferencesPage):
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

        # altitude row
        altitude_row = Adw.ActionRow(title='Altitude')
        settings_group.add(child=altitude_row)

        altitude_entry = Gtk.Entry(
            placeholder_text='km',
            valign=Gtk.Align.CENTER
        )
        altitude_entry.connect(
            'activate',
            self.on_set_altitude,
        )
        altitude_row.add_suffix(widget=altitude_entry)

        # albedo row
        albedo_row = Adw.ActionRow(title='Albedo')
        settings_group.add(child=albedo_row)

        albedo_entry = Gtk.Entry(
            valign=Gtk.Align.CENTER
        )
        albedo_entry.connect(
            'activate',
            self.on_set_albedo,
        )
        albedo_row.add_suffix(widget=albedo_entry)

    def on_set_altitude(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtran.surface.Surface = self.get_settings_callback()
        settings.altitude = float(entry.get_text())
        self.set_settings_callback(settings=settings)

    def on_set_albedo(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtran.surface.Surface = self.get_settings_callback()
        settings.albedo = float(entry.get_text())
        self.set_settings_callback(settings=settings)
