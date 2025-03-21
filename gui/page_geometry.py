import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

class Geometry(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## sza row
        sza = Adw.ActionRow(title='Solar Zenith Angle')
        settings_group.add(child=sza)

        ## phi0 row
        phi0_row = Adw.ActionRow(title='Phi0')
        settings_group.add(child=phi0_row)

        ## phi row
        phi_row = Adw.ActionRow(title='Phi')
        settings_group.add(child=phi_row)

        ## umu row
        umu_row = Adw.ActionRow(title='Umu')
        settings_group.add(child=umu_row)

        ## day_of_year row
        day_of_year = Adw.ActionRow(title='Day of Year')
        settings_group.add(child=day_of_year)

        ## latitude row
        latitude_row = Adw.ActionRow(title='Latitude')
        settings_group.add(child=latitude_row)

        ## longitude row
        longitude_row = Adw.ActionRow(title='Longitude')
        settings_group.add(child=longitude_row)

        ## time row
        time_row = Adw.ActionRow(title='Time')
        settings_group.add(child=time_row)