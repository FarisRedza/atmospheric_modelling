import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

class Output(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## output_user row
        output_user_row = Adw.ActionRow(title='Output User')
        settings_group.add(child=output_user_row)

        ## output_quantity row
        output_quantity_row = Adw.ActionRow(title='Output Quantity')
        settings_group.add(child=output_quantity_row)

        ## output_process row
        output_process_row = Adw.ActionRow(title='Output Process')
        settings_group.add(child=output_process_row)

        ## output_format row
        output_format_row = Adw.ActionRow(title='Output Format')
        settings_group.add(child=output_format_row)

        ## zout row
        zout_row = Adw.ActionRow(title='ZOut')
        settings_group.add(child=zout_row)
