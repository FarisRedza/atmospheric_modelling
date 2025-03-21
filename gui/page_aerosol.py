import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

class Aerosol(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## default row
        default_row = Adw.ActionRow(title='Default')
        settings_group.add(child=default_row)

        ## season row
        season_row = Adw.ActionRow(title='Season')
        settings_group.add(child=season_row)

        ## visibility row
        visibility_row = Adw.ActionRow(title='Visibility')
        settings_group.add(child=visibility_row)

        ## species row
        species_row = Adw.ActionRow(title='Species')
        settings_group.add(child=species_row)

        ## season row
        species_library_row = Adw.ActionRow(title='Species Library')
        settings_group.add(child=species_library_row)
