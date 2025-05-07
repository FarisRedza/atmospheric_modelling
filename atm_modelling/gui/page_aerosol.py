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
import libRadtran.aerosol


class Aerosol(Adw.PreferencesPage):
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

        # default switch
        default_row = Adw.ActionRow(title='Default')
        default_switch = Gtk.Switch(
            active=self.get_settings_callback().aerosol_default,
            valign=Gtk.Align.CENTER
        )
        default_switch.connect("notify::active", self.on_set_default)
        default_row.add_suffix(widget=default_switch)
        default_row.set_activatable_widget(
            widget=default_switch
        )
        settings_group.add(default_row)

        # season dropdown
        season_row = Adw.ActionRow(title='Season')
        settings_group.add(child=season_row)

        season_dropdown = Gtk.DropDown().new_from_strings(
            strings=[i.name for i in libRadtran.aerosol.AerosolSeason]
        )
        season_dropdown.connect(
            'notify::selected',
            self.on_season_select
        )
        season_dropdown.set_valign(align=Gtk.Align.CENTER)
        season_row.set_activatable_widget(widget=season_dropdown)
        season_row.add_suffix(widget=season_dropdown)

        ## visiblity dropdown
        visibility_row = Adw.ActionRow(title='Visibility')
        settings_group.add(child=visibility_row)

        visibility_entry = Gtk.Entry(
            placeholder_text='km',
            valign=Gtk.Align.CENTER
        )
        visibility_entry.connect(
            'activate',
            self.on_set_visiblity,
        )
        visibility_row.add_suffix(widget=visibility_entry)

        # haze dropdown
        haze_row = Adw.ActionRow(title='Haze')
        settings_group.add(child=haze_row)

        haze_dropdown = Gtk.DropDown().new_from_strings(
            strings=[i.name for i in libRadtran.aerosol.AerosolHaze]
        )
        haze_dropdown.connect(
            'notify::selected',
            self.on_haze_select
        )
        haze_dropdown.set_valign(align=Gtk.Align.CENTER)
        haze_row.set_activatable_widget(widget=haze_dropdown)
        haze_row.add_suffix(widget=haze_dropdown)

        # vulcan dropdown
        vulcan_row = Adw.ActionRow(title='Vulcan')
        settings_group.add(child=vulcan_row)

        vulcan_dropdown = Gtk.DropDown().new_from_strings(
            strings=[i.name for i in libRadtran.aerosol.AerosolVulcan]
        )
        vulcan_dropdown.connect(
            'notify::selected',
            self.on_vulcan_select
        )
        vulcan_dropdown.set_valign(align=Gtk.Align.CENTER)
        vulcan_row.set_activatable_widget(widget=vulcan_dropdown)
        vulcan_row.add_suffix(widget=vulcan_dropdown)

        # species dropdown
        species_row = Adw.ActionRow(title='Species')
        settings_group.add(child=species_row)

        species_dropdown = Gtk.DropDown().new_from_strings(
            strings=[i.name for i in libRadtran.aerosol.AerosolSpecies]
        )
        species_dropdown.connect(
            'notify::selected',
            self.on_species_select
        )
        species_dropdown.set_valign(align=Gtk.Align.CENTER)
        species_row.set_activatable_widget(widget=species_dropdown)
        species_row.add_suffix(widget=species_dropdown)

        # species library dropdown
        species_library_row = Adw.ActionRow(title='Species Library')
        settings_group.add(child=species_library_row)

        species_library_dropdown = Gtk.DropDown().new_from_strings(
            strings=[i.name for i in libRadtran.aerosol.AerosolSpeciesLibrary]
        )
        species_library_dropdown.connect(
            'notify::selected',
            self.on_species_library_select
        )
        species_library_dropdown.set_valign(align=Gtk.Align.CENTER)
        species_library_row.set_activatable_widget(widget=species_library_dropdown)
        species_library_row.add_suffix(widget=species_library_dropdown)

    def on_set_default(
            self,
            switch: Gtk.Switch,
            gparam: GObject.GParamSpec
    ) -> None:
        settings: libRadtran.aerosol.Aerosol = self.get_settings_callback()
        settings.aerosol_default = switch.get_active()
        self.set_settings_callback(settings=settings)

    def on_season_select(
            self,
            dropdown: Gtk.DropDown,
            gparam: GObject.GParamSpec
        ) -> None:
        settings: libRadtran.aerosol.Aerosol = self.get_settings_callback()
        settings.aerosol_season = list(
            libRadtran.aerosol.AerosolSeason
        )[dropdown.get_selected()]
        self.set_settings_callback(settings=settings)

    def on_set_visiblity(
            self,
            entry: Gtk.Entry
    ) -> None:
        settings: libRadtran.aerosol.Aerosol = self.get_settings_callback()
        settings.aerosol_visibility = float(entry.get_text())
        self.set_settings_callback(settings=settings)

    def on_haze_select(
            self,
            dropdown: Gtk.DropDown,
            gparam: GObject.GParamSpec
        ) -> None:
        settings: libRadtran.aerosol.Aerosol = self.get_settings_callback()
        settings.aerosol_haze = list(
            libRadtran.aerosol.AerosolHaze
        )[dropdown.get_selected()]
        self.set_settings_callback(settings=settings)

    def on_vulcan_select(
            self,
            dropdown: Gtk.DropDown,
            gparam: GObject.GParamSpec
        ) -> None:
        settings: libRadtran.aerosol.Aerosol = self.get_settings_callback()
        settings.aerosol_vulcan = list(
            libRadtran.aerosol.AerosolVulcan
        )[dropdown.get_selected()]
        self.set_settings_callback(settings=settings)

    def on_species_select(
            self,
            dropdown: Gtk.DropDown,
            gparam: GObject.GParamSpec
        ) -> None:
        settings: libRadtran.aerosol.Aerosol = self.get_settings_callback()
        settings.aerosol_species_file = list(
            libRadtran.aerosol.AerosolSpecies
        )[dropdown.get_selected()]
        self.set_settings_callback(settings=settings)

    def on_species_library_select(
            self,
            dropdown: Gtk.DropDown,
            gparam: GObject.GParamSpec
        ) -> None:
        settings: libRadtran.aerosol.Aerosol = self.get_settings_callback()
        settings.aerosol_species_library = list(
            libRadtran.aerosol.AerosolSpecies
        )[dropdown.get_selected()]
        self.set_settings_callback(settings=settings)