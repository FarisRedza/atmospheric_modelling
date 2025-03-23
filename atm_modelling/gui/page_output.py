import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

from atm_modelling.libRadtran import output

class Output(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = output.Output()

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## quiet row
        quiet_row = Adw.ActionRow(title='Quiet')
        settings_group.add(child=quiet_row)

        ### quiet switch
        quiet_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        quiet_switch.set_active(self.settings.quiet)
        quiet_switch.connect('activate', self.on_toggle_quiet)
        quiet_row.add_suffix(widget=quiet_switch)
        quiet_row.set_activatable_widget(widget=quiet_switch)

        ## verbose row
        verbose_row = Adw.ActionRow(title='Verbose')
        settings_group.add(child=verbose_row)

        ### verbose switch
        verbose_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        verbose_switch.set_active(self.settings.verbose)
        verbose_switch.connect('activate', self.on_toggle_verbose)
        verbose_row.add_suffix(widget=verbose_switch)
        verbose_row.set_activatable_widget(widget=verbose_switch)

        ## output_user row
        output_user_row = Adw.ActionRow(title='Output User')
        settings_group.add(child=output_user_row)

        ### output_user entry
        self.output_user_entry = Gtk.Entry(
            placeholder_text='output_user',
            valign=Gtk.Align.CENTER
        )
        self.output_user_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.output_user_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.output_user_entry.connect(
            'icon_press',
            self.on_output_user_clear
        )
        output_user_row.add_suffix(widget=self.output_user_entry)

        ## output_quantity row
        output_quantity_row = Adw.ActionRow(title='Output Quantity')
        settings_group.add(child=output_quantity_row)

        ### select output_quantity dropdown
        dropdown_factory = Gtk.SignalListItemFactory.new()
        dropdown_factory.connect('setup', self.on_dropdown_setup)
        dropdown_factory.connect('bind', self.on_dropdown_bind)

        output_quantity_list = Gtk.StringList()
        for value in [output_quantity.value for output_quantity in output.OutputQuantity]:
            output_quantity_list.append(str(value))

        select_output_quantity_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_output_quantity_dropdown.set_factory(factory=dropdown_factory)
        select_output_quantity_dropdown.connect('notify::selected', self.on_output_quantity_select)
        select_output_quantity_dropdown.props.model = output_quantity_list
        output_quantity_row.add_suffix(widget=select_output_quantity_dropdown)

        ## output_process row
        output_process_row = Adw.ActionRow(title='Output Process')
        settings_group.add(child=output_process_row)

        ### select output_process dropdown
        # dropdown_factory = Gtk.SignalListItemFactory.new()
        # dropdown_factory.connect('setup', self.on_dropdown_setup)
        # dropdown_factory.connect('bind', self.on_dropdown_bind)

        output_process_list = Gtk.StringList()
        for value in [output_process.value for output_process in output.OutputProcess]:
            output_process_list.append(str(value))

        select_output_process_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_output_process_dropdown.set_factory(factory=dropdown_factory)
        select_output_process_dropdown.connect('notify::selected', self.on_output_process_select)
        select_output_process_dropdown.props.model = output_process_list
        output_process_row.add_suffix(widget=select_output_process_dropdown)

        ## output_format row
        output_format_row = Adw.ActionRow(title='Output Format')
        settings_group.add(child=output_format_row)

        ### select output_format dropdown
        # dropdown_factory = Gtk.SignalListItemFactory.new()
        # dropdown_factory.connect('setup', self.on_dropdown_setup)
        # dropdown_factory.connect('bind', self.on_dropdown_bind)

        output_format_list = Gtk.StringList()
        for value in [output_format.value for output_format in output.OutputFormat]:
            output_format_list.append(str(value))

        select_output_format_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_output_format_dropdown.set_factory(factory=dropdown_factory)
        select_output_format_dropdown.connect('notify::selected', self.on_output_format_select)
        select_output_format_dropdown.props.model = output_format_list
        output_format_row.add_suffix(widget=select_output_format_dropdown)

        ## zout row
        zout_row = Adw.ActionRow(title='ZOut')
        settings_group.add(child=zout_row)

        ### zout entry
        self.zout_entry = Gtk.Entry(
            placeholder_text='zout',
            valign=Gtk.Align.CENTER
        )
        self.zout_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.zout_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.zout_entry.connect(
            'icon_press',
            self.on_zout_clear
        )
        zout_row.add_suffix(widget=self.zout_entry)

    def on_toggle_quiet(self, switch):
        self.settings.quiet = not self.settings.quiet

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

    def on_toggle_verbose(self, switch):
        self.settings.verbose = not self.settings.verbose

    def on_output_user_clear(self, entry, _):
        self.output_user_entry.set_text(text='')

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

    def on_output_quantity_select(self, dropdown, _):
        self.selected_device = dropdown.get_selected()

    def on_output_process_select(self, dropdown, _):
        self.selected_device = dropdown.get_selected()

    def on_output_format_select(self, dropdown, _):
        self.selected_device = dropdown.get_selected()

    def on_zout_clear(self, entry, _):
        self.zout_entry.set_text(text='')