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
import libRadtran.general_atm


class GeneralAtm(Adw.PreferencesPage):
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

        # absorption switch
        absorption_row = Adw.ActionRow(title='Absorption')
        absorption_switch = Gtk.Switch(
            active=not self.get_settings_callback().no_absorption,
            valign=Gtk.Align.CENTER
        )
        absorption_switch.connect('notify::active', self.on_set_absorption)
        absorption_row.add_suffix(widget=absorption_switch)
        absorption_row.set_activatable_widget(
            widget=absorption_switch
        )
        settings_group.add(absorption_row)

        # scattering switch
        scattering_row = Adw.ActionRow(title='Scattering')
        scattering_switch = Gtk.Switch(
            active=not self.get_settings_callback().no_scattering,
            valign=Gtk.Align.CENTER
        )
        scattering_switch.connect('notify::active', self.on_set_scattering)
        scattering_row.add_suffix(widget=scattering_switch)
        scattering_row.set_activatable_widget(
            widget=scattering_switch
        )
        settings_group.add(scattering_row)

        # zout interpolate switch
        zout_interpolate_row = Adw.ActionRow(title='Zout interpolate')
        zout_interpolate_switch = Gtk.Switch(
            active=self.get_settings_callback().zout_interpolate,
            valign=Gtk.Align.CENTER
        )
        zout_interpolate_switch.connect('notify::active', self.on_set_zout_interpolate)
        zout_interpolate_row.add_suffix(widget=zout_interpolate_switch)
        zout_interpolate_row.set_activatable_widget(
            widget=zout_interpolate_switch
        )
        settings_group.add(zout_interpolate_row)

        # reverse atmosphere switch
        reverse_atmosphere_row = Adw.ActionRow(title='Reverse atmosphere')
        reverse_atmosphere_switch = Gtk.Switch(
            active=self.get_settings_callback().reverse_atmosphere,
            valign=Gtk.Align.CENTER
        )
        reverse_atmosphere_switch.connect('notify::active', self.on_set_reverse_atmosphere)
        reverse_atmosphere_row.add_suffix(widget=reverse_atmosphere_switch)
        reverse_atmosphere_row.set_activatable_widget(
            widget=reverse_atmosphere_switch
        )
        settings_group.add(reverse_atmosphere_row)

    def on_set_absorption(
            self,
            switch: Gtk.Switch,
            gparam: GObject.GParamSpec
    ) -> None:
        settings: libRadtran.general_atm.GeneralAtm = self.get_settings_callback()
        settings.no_absorption = not switch.get_active()
        self.set_settings_callback(settings=settings)

    def on_set_scattering(
            self,
            switch: Gtk.Switch,
            gparam: GObject.GParamSpec
    ) -> None:
        settings: libRadtran.general_atm.GeneralAtm = self.get_settings_callback()
        settings.no_scattering = not switch.get_active()
        self.set_settings_callback(settings=settings)

    def on_set_zout_interpolate(
            self,
            switch: Gtk.Switch,
            gparam: GObject.GParamSpec
    ) -> None:
        settings: libRadtran.general_atm.GeneralAtm = self.get_settings_callback()
        settings.zout_interpolate = switch.get_active()
        self.set_settings_callback(settings=settings)

    def on_set_reverse_atmosphere(
            self,
            switch: Gtk.Switch,
            gparam: GObject.GParamSpec
    ) -> None:
        settings: libRadtran.general_atm.GeneralAtm = self.get_settings_callback()
        settings.reverse_atmosphere = switch.get_active()
        self.set_settings_callback(settings=settings)