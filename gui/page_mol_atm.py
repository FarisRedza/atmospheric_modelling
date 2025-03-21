import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

class MolAtm(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## atmosphere row
        atmosphere_row = Adw.ActionRow(title='Atmosphere')
        settings_group.add(child=atmosphere_row)

        ## mol_abs_param row
        mol_abs_param_row = Adw.ActionRow(title='Mol Abs Parameter')
        settings_group.add(child=mol_abs_param_row)

        ## mol_modify row
        mol_modify_row = Adw.ActionRow(title='Mol Modify')
        settings_group.add(child=mol_modify_row)

        ## crs_model row
        crs_model_row = Adw.ActionRow(title='CRS Model')
        settings_group.add(child=crs_model_row)
