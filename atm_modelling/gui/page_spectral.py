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
import libRadtranPy.spectral

class Spectral(Adw.PreferencesPage):
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

        ## wavelength row
        wavelength_row = Adw.ActionRow(title='Wavelength')
        settings_group.add(child=wavelength_row)

        wavelength_entry = Gtk.Entry(
            placeholder_text='nm',
            valign=Gtk.Align.CENTER
        )
        wavelength_entry.connect(
            'activate',
            self.on_set_wavelength,
        )
        wavelength_row.add_suffix(widget=wavelength_entry)

        # source dropdown
        source_row = Adw.ActionRow(title='Source')
        settings_group.add(child=source_row)

        source_dropdown = Gtk.DropDown().new_from_strings(
            strings=[i.name for i in libRadtranPy.spectral.Source]
        )
        source_dropdown.connect(
            'notify::selected',
            self.on_source_select
        )
        source_dropdown.set_selected(
            position=list(
                libRadtranPy.spectral.Source
            ).index(
                self.get_settings_callback().source
            )
        )
        source_dropdown.set_valign(align=Gtk.Align.CENTER)
        source_row.set_activatable_widget(widget=source_dropdown)
        source_row.add_suffix(widget=source_dropdown)

    def on_set_wavelength(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtranPy.spectral.Spectral = self.get_settings_callback()
        settings.wavelength = [float(entry.get_text()), float(entry.get_text())]
        self.set_settings_callback(settings=settings)

    def on_source_select(
            self,
            dropdown: Gtk.DropDown,
            gparam: GObject.GParamSpec
        ) -> None:
        settings: libRadtranPy.spectral.Spectral = self.get_settings_callback()
        settings.source = list(
            libRadtranPy.spectral.Source
        )[dropdown.get_selected()]
        self.set_settings_callback(settings=settings)