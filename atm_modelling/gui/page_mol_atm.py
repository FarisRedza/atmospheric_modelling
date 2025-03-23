import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

from atm_modelling.libRadtran import mol_atm

class MolAtm(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = mol_atm.MolAtm()

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## atmosphere row
        atmosphere_row = Adw.ActionRow(title='Atmosphere')
        settings_group.add(child=atmosphere_row)

        ### select atmosphere dropdown
        dropdown_factory = Gtk.SignalListItemFactory.new()
        dropdown_factory.connect('setup', self.on_dropdown_setup)
        dropdown_factory.connect('bind', self.on_dropdown_bind)

        atmosphere_list = Gtk.StringList()
        for value in [atmosphere.value for atmosphere in mol_atm.Atmosphere]:
            atmosphere_list.append(str(value))

        select_atmosphere_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_atmosphere_dropdown.set_factory(factory=dropdown_factory)
        select_atmosphere_dropdown.connect('notify::selected', self.on_atmosphere_select)
        select_atmosphere_dropdown.props.model = atmosphere_list
        atmosphere_row.add_suffix(widget=select_atmosphere_dropdown)

        ## mol_abs_param row
        mol_abs_param_row = Adw.ActionRow(title='Mol Abs Parameter')
        settings_group.add(child=mol_abs_param_row)

        ### select ck_scheme dropdown
        # dropdown_factory = Gtk.SignalListItemFactory.new()
        # dropdown_factory.connect('setup', self.on_dropdown_setup)
        # dropdown_factory.connect('bind', self.on_dropdown_bind)

        ck_scheme_list = Gtk.StringList()
        for value in [ck_scheme.value for ck_scheme in mol_atm.CKScheme]:
            ck_scheme_list.append(str(value))

        select_ck_scheme_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_ck_scheme_dropdown.set_factory(factory=dropdown_factory)
        select_ck_scheme_dropdown.connect('notify::selected', self.on_ck_scheme_select)
        select_ck_scheme_dropdown.props.model = ck_scheme_list
        mol_abs_param_row.add_suffix(widget=select_ck_scheme_dropdown)

        ### mol_abs_param_str entry
        self.mol_abs_param_str_entry = Gtk.Entry(
            placeholder_text='mol_abs_param_str',
            valign=Gtk.Align.CENTER
        )
        self.mol_abs_param_str_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.mol_abs_param_str_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.mol_abs_param_str_entry.connect(
            'icon_press',
            self.on_mol_abs_param_str_clear
        )
        mol_abs_param_row.add_suffix(widget=self.mol_abs_param_str_entry)

        ## mol_modify row
        mol_modify_row = Adw.ActionRow(title='Mol Modify')
        settings_group.add(child=mol_modify_row)

        ### mol_modify entry
        self.mol_modify_entry = Gtk.Entry(
            placeholder_text='mol_modify',
            valign=Gtk.Align.CENTER
        )
        self.mol_modify_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.mol_modify_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.mol_modify_entry.connect(
            'icon_press',
            self.on_mol_modify_clear
        )
        mol_modify_row.add_suffix(widget=self.mol_modify_entry)

        ## crs_model row
        crs_model_row = Adw.ActionRow(title='CRS Model')
        settings_group.add(child=crs_model_row)

        ### select mol_id dropdown
        # dropdown_factory = Gtk.SignalListItemFactory.new()
        # dropdown_factory.connect('setup', self.on_dropdown_setup)
        # dropdown_factory.connect('bind', self.on_dropdown_bind)

        mol_id_list = Gtk.StringList()
        for value in [mol_id.value for mol_id in mol_atm.MolID]:
            mol_id_list.append(str(value))

        select_mol_id_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_mol_id_dropdown.set_factory(factory=dropdown_factory)
        select_mol_id_dropdown.connect('notify::selected', self.on_mol_id_select)
        select_mol_id_dropdown.props.model = mol_id_list
        crs_model_row.add_suffix(widget=select_mol_id_dropdown)

        ### select crs_model dropdown
        # dropdown_factory = Gtk.SignalListItemFactory.new()
        # dropdown_factory.connect('setup', self.on_dropdown_setup)
        # dropdown_factory.connect('bind', self.on_dropdown_bind)

        crs_model_list = Gtk.StringList()
        for value in [crs_model.value for crs_model in mol_atm.CRSModel]:
            crs_model_list.append(str(value))

        select_crs_model_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_crs_model_dropdown.set_factory(factory=dropdown_factory)
        select_crs_model_dropdown.connect('notify::selected', self.on_crs_model_select)
        select_crs_model_dropdown.props.model = crs_model_list
        crs_model_row.add_suffix(widget=select_crs_model_dropdown)

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

    def on_atmosphere_select(self, dropdown, _):
        self.selected_atmosphere = dropdown.get_selected()

    def on_ck_scheme_select(self, dropdown, _):
        self.selected_ck_scheme = dropdown.get_selected()

    def on_mol_abs_param_str_clear(self, entry, _):
        self.mol_abs_param_str_entry.set_text(text='')

    def on_mol_modify_clear(self, entry, _):
        self.mol_modify_entry.set_text(text='')

    def on_mol_id_select(self, dropdown, _):
        self.selected_mol_id = dropdown.get_selected()

    def on_crs_model_select(self, dropdown, _):
        self.selected_crs_model = dropdown.get_selected()