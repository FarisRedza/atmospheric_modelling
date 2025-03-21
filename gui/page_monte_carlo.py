import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

class MonteCarlo(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## mc_polarisation row
        mc_polarisation_row = Adw.ActionRow(title='Polarisation')
        settings_group.add(child=mc_polarisation_row)

        ## mc_backward_output row
        mc_backward_output_row = Adw.ActionRow(title='Backward Output')
        settings_group.add(child=mc_backward_output_row)

        ## mc_forward_output row
        mc_forward_output_row = Adw.ActionRow(title='Forward Output')
        settings_group.add(child=mc_forward_output_row)

        ## mc_output_unit row
        mc_output_unit_row = Adw.ActionRow(title='Output Unit')
        settings_group.add(child=mc_output_unit_row)