import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

from atm_modelling.libRadtranPy import general_atm

class GeneralAtm(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = general_atm.GeneralAtm()

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## absorption row
        absorption_row = Adw.ActionRow(title='Absorption')
        settings_group.add(child=absorption_row)

        ### absorption switch
        absorption_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        absorption_switch.set_active(not self.settings.no_absorption)
        absorption_switch.connect('activate', self.on_toggle_absorption)
        absorption_row.add_suffix(widget=absorption_switch)
        absorption_row.set_activatable_widget(widget=absorption_switch)

        ## scattering row
        scattering_row = Adw.ActionRow(title='Scattering')
        settings_group.add(child=scattering_row)

        ### scattering switch
        scattering_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        scattering_switch.set_active(not self.settings.no_scattering)
        scattering_switch.connect('activate', self.on_toggle_scattering)
        scattering_row.add_suffix(widget=scattering_switch)
        scattering_row.set_activatable_widget(widget=scattering_switch)

        ## zout_interpolate row
        zout_interpolate_row = Adw.ActionRow(title='Zout Interpolate')
        settings_group.add(child=zout_interpolate_row)

        ### zout_interpolate switch
        zout_interpolate_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        zout_interpolate_switch.set_active(self.settings.zout_interpolate)
        zout_interpolate_switch.connect('activate', self.on_toggle_zout_interpolate)
        zout_interpolate_row.add_suffix(widget=zout_interpolate_switch)
        zout_interpolate_row.set_activatable_widget(widget=zout_interpolate_switch)

        ## reverse_atmosphere row
        reverse_atmosphere_row = Adw.ActionRow(title='Reverse Atmosphere')
        settings_group.add(child=reverse_atmosphere_row)

        ### reverse_atmosphere switch
        reverse_atmosphere_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        reverse_atmosphere_switch.set_active(self.settings.reverse_atmosphere)
        reverse_atmosphere_switch.connect('activate', self.on_toggle_reverse_atmosphere)
        reverse_atmosphere_row.add_suffix(widget=reverse_atmosphere_switch)
        reverse_atmosphere_row.set_activatable_widget(widget=reverse_atmosphere_switch)

    def on_toggle_absorption(self, switch: Gtk.Switch):
        self.settings.no_absorption = not self.settings.no_absorption

    def on_toggle_scattering(self, switch: Gtk.Switch):
        self.settings.no_scattering = not self.settings.no_scattering

    def on_toggle_zout_interpolate(self, switch: Gtk.Switch):
        self.settings.zout_interpolate = not self.settings.zout_interpolate

    def on_toggle_reverse_atmosphere(self, switch: Gtk.Switch):
        self.settings.reverse_atmosphere = not self.settings.reverse_atmosphere