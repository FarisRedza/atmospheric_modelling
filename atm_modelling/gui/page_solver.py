import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

from atm_modelling.libRadtran import solver

class Solver(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = solver.Solver()

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## rte_solver row
        rte_solver_row = Adw.ActionRow(title='RTE Solver')
        settings_group.add(child=rte_solver_row)

        ### select rte_solver dropdown
        dropdown_factory = Gtk.SignalListItemFactory.new()
        dropdown_factory.connect('setup', self.on_dropdown_setup)
        dropdown_factory.connect('bind', self.on_dropdown_bind)

        rte_solver_list = Gtk.StringList()
        for value in [rte_solver.value for rte_solver in solver.RTESolver]:
            rte_solver_list.append(str(value))

        select_rte_solver_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_rte_solver_dropdown.set_factory(factory=dropdown_factory)
        select_rte_solver_dropdown.connect('notify::selected', self.on_rte_solver_select)
        select_rte_solver_dropdown.props.model = rte_solver_list
        rte_solver_row.add_suffix(widget=select_rte_solver_dropdown)

    def on_dropdown_setup(self, factory, list_item):
        label = Gtk.Label()
        label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        label.set_xalign(0)
        label.set_max_width_chars(20)
        label.set_hexpand(expand=True)
        list_item.set_child(label)

    def on_dropdown_bind(self, factory, list_item):
        item = list_item.get_item()
        label = list_item.get_child()

        if isinstance(item, Gtk.StringObject):
            label.set_label(item.get_string())

    def on_rte_solver_select(self, dropdown, _):
        self.selected_rte_solver = dropdown.get_selected()
        print(self.selected_rte_solver)