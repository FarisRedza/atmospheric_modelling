import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

from atm_modelling.libRadtran import monte_carlo

class MonteCarlo(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = monte_carlo.MonteCarlo()

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## mc_polarisation row
        mc_polarisation_row = Adw.ActionRow(title='Polarisation')
        settings_group.add(child=mc_polarisation_row)

        ### select mc_polarisation dropdown
        dropdown_factory = Gtk.SignalListItemFactory.new()
        dropdown_factory.connect('setup', self.on_dropdown_setup)
        dropdown_factory.connect('bind', self.on_dropdown_bind)

        mc_polarisation_list = Gtk.StringList()
        for value in [mc_polarisation.value for mc_polarisation in monte_carlo.MCPolarisation]:
            mc_polarisation_list.append(str(value))

        select_mc_polarisation_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_mc_polarisation_dropdown.set_factory(factory=dropdown_factory)
        select_mc_polarisation_dropdown.connect('notify::selected', self.on_mc_polarisation_select)
        select_mc_polarisation_dropdown.props.model = mc_polarisation_list
        mc_polarisation_row.add_suffix(widget=select_mc_polarisation_dropdown)

        ## mc_backward_output row
        mc_backward_output_row = Adw.ActionRow(title='Backward Output')
        settings_group.add(child=mc_backward_output_row)

        ### select mc_backward_output dropdown
        # dropdown_factory = Gtk.SignalListItemFactory.new()
        # dropdown_factory.connect('setup', self.on_dropdown_setup)
        # dropdown_factory.connect('bind', self.on_dropdown_bind)

        mc_backward_output_list = Gtk.StringList()
        for value in [mc_backward_output.value for mc_backward_output in monte_carlo.MCBackwardOutput]:
            mc_backward_output_list.append(str(value))

        select_mc_backward_output_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_mc_backward_output_dropdown.set_factory(factory=dropdown_factory)
        select_mc_backward_output_dropdown.connect('notify::selected', self.on_mc_backward_output_select)
        select_mc_backward_output_dropdown.props.model = mc_backward_output_list
        mc_backward_output_row.add_suffix(widget=select_mc_backward_output_dropdown)

        ## mc_forward_output row
        mc_forward_output_row = Adw.ActionRow(title='Forward Output')
        settings_group.add(child=mc_forward_output_row)

        ### select mc_forward_output dropdown
        # dropdown_factory = Gtk.SignalListItemFactory.new()
        # dropdown_factory.connect('setup', self.on_dropdown_setup)
        # dropdown_factory.connect('bind', self.on_dropdown_bind)

        mc_forward_output_list = Gtk.StringList()
        for value in [mc_forward_output.value for mc_forward_output in monte_carlo.MCForwardOutput]:
            mc_forward_output_list.append(str(value))

        select_mc_forward_output_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_mc_forward_output_dropdown.set_factory(factory=dropdown_factory)
        select_mc_forward_output_dropdown.connect('notify::selected', self.on_mc_forward_output_select)
        select_mc_forward_output_dropdown.props.model = mc_forward_output_list
        mc_forward_output_row.add_suffix(widget=select_mc_forward_output_dropdown)

        ## mc_output_unit row
        mc_output_unit_row = Adw.ActionRow(title='Output Unit')
        settings_group.add(child=mc_output_unit_row)

        ### select mc_output_unit dropdown
        # dropdown_factory = Gtk.SignalListItemFactory.new()
        # dropdown_factory.connect('setup', self.on_dropdown_setup)
        # dropdown_factory.connect('bind', self.on_dropdown_bind)

        mc_output_unit_list = Gtk.StringList()
        for value in [mc_output_unit.value for mc_output_unit in monte_carlo.MCOutputUnit]:
            mc_output_unit_list.append(str(value))

        select_mc_output_unit_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_mc_output_unit_dropdown.set_factory(factory=dropdown_factory)
        select_mc_output_unit_dropdown.connect('notify::selected', self.on_mc_output_unit_select)
        select_mc_output_unit_dropdown.props.model = mc_output_unit_list
        mc_output_unit_row.add_suffix(widget=select_mc_output_unit_dropdown)

    def on_dropdown_setup(self, factory: Gtk.SignalListItemFactory, list_item: Gtk.ListItem):
        label = Gtk.Label()
        label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        label.set_xalign(0)
        label.set_max_width_chars(20)
        label.set_hexpand(expand=True)
        list_item.set_child(label)

    def on_dropdown_bind(self, factory: Gtk.SignalListItemFactory, list_item: Gtk.ListItem):
        item = list_item.get_item()
        label = list_item.get_child()

        if isinstance(item, Gtk.StringObject):
            label.set_label(item.get_string())

    def on_mc_polarisation_select(self, dropdown: Gtk.DropDown, _):
        self.selected_device = dropdown.get_selected()

    def on_mc_backward_output_select(self, dropdown: Gtk.DropDown, _):
        self.selected_device = dropdown.get_selected()

    def on_mc_forward_output_select(self, dropdown: Gtk.DropDown, _):
        self.selected_device = dropdown.get_selected()

    def on_mc_output_unit_select(self, dropdown: Gtk.DropDown, _):
        self.selected_device = dropdown.get_selected()