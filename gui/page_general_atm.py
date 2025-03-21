import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

class GeneralAtm(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## absorption row
        absorption_row = Adw.ActionRow(title='Absorption')
        settings_group.add(child=absorption_row)

        ## scattering row
        scattering_row = Adw.ActionRow(title='Scattering')
        settings_group.add(child=scattering_row)

        ## zout_interpolate row
        zout_interpolate_row = Adw.ActionRow(title='Zout Interpolate')
        settings_group.add(child=zout_interpolate_row)

        ## reverse_atmosphere row
        reverse_atmosphere_row = Adw.ActionRow(title='Reverse Atmosphere')
        settings_group.add(child=reverse_atmosphere_row)
