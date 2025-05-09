import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

from atm_modelling.libRadtranPy import aerosol

class Aerosol(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = aerosol.Aerosol()

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## default row
        default_row = Adw.ActionRow(title='Default')
        settings_group.add(child=default_row)

        ### default switch
        default_switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        default_switch.set_active(self.settings.aerosol_default)
        default_switch.connect('activate', self.on_toggle_default)
        default_row.add_suffix(widget=default_switch)
        default_row.set_activatable_widget(widget=default_switch)

        ## season row
        season_row = Adw.ActionRow(title='Season')
        settings_group.add(child=season_row)

        ### select season dropdown
        dropdown_factory = Gtk.SignalListItemFactory.new()
        dropdown_factory.connect('setup', self.on_dropdown_setup)
        dropdown_factory.connect('bind', self.on_dropdown_bind)

        self.season_list = [season.value for season in aerosol.AerosolSeason]
        season_string_list = Gtk.StringList()
        for value in self.season_list:
            season_string_list.append(str(value))

        select_season_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_season_dropdown.set_factory(factory=dropdown_factory)
        select_season_dropdown.connect('notify::selected', self.on_season_select)
        select_season_dropdown.props.model = season_string_list
        season_row.add_suffix(widget=select_season_dropdown)

        ## visibility row
        visibility_row = Adw.ActionRow(title='Visibility')
        settings_group.add(child=visibility_row)

        ### visibility entry
        self.visibility_entry = Gtk.Entry(
            # placeholder_text=aerosol.Aerosol.__dataclass_fields__['aerosol_visibility'].default,
            valign=Gtk.Align.CENTER
        )
        self.visibility_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.visibility_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.visibility_entry.connect(
            'icon_press',
            self.on_visibility_clear
        )
        visibility_row.add_suffix(widget=self.visibility_entry)

        ## haze row
        haze_row = Adw.ActionRow(title='Haze')
        settings_group.add(child=haze_row)

        ### select haze_row dropdown
        self.haze_list = [haze.value for haze in aerosol.AerosolHaze]
        haze_string_list = Gtk.StringList()
        for value in self.haze_list:
            haze_string_list.append(str(value))

        select_haze_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_haze_dropdown.set_factory(factory=dropdown_factory)
        select_haze_dropdown.connect('notify::selected', self.on_haze_select)
        select_haze_dropdown.props.model = haze_string_list
        haze_row.add_suffix(widget=select_haze_dropdown)

        ## vulcan row
        vulcan_row = Adw.ActionRow(title='Vulcan')
        settings_group.add(child=vulcan_row)

        ### select vulcan dropdown
        self.vulcan_list = [vulcan.value for vulcan in aerosol.AerosolVulcan]
        vulcan_string_list = Gtk.StringList()
        for value in self.vulcan_list:
            vulcan_string_list.append(str(value))

        select_vulcan_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_vulcan_dropdown.set_factory(factory=dropdown_factory)
        select_vulcan_dropdown.connect('notify::selected', self.on_vulcan_select)
        select_vulcan_dropdown.props.model = vulcan_string_list
        vulcan_row.add_suffix(widget=select_vulcan_dropdown)

        ## species row
        species_row = Adw.ActionRow(title='Species')
        settings_group.add(child=species_row)

        ### select species dropdown
        self.species_list = [species.value for species in aerosol.AerosolSpecies]
        species_string_list = Gtk.StringList()
        for value in self.species_list:
            species_string_list.append(value)

        select_species_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_species_dropdown.set_factory(factory=dropdown_factory)
        select_species_dropdown.connect('notify::selected', self.on_species_select)
        select_species_dropdown.props.model = species_string_list
        species_row.add_suffix(widget=select_species_dropdown)

        ## species_library row
        species_library_row = Adw.ActionRow(title='Species Library')
        settings_group.add(child=species_library_row)

        ### select species_library dropdown
        self.species_library_list = [species_library.value for species_library in aerosol.AerosolSpeciesLibrary]
        species_library_string_list = Gtk.StringList()
        for value in self.species_library_list :
            species_library_string_list.append(value)

        select_species_library_dropdown = Gtk.DropDown(valign=Gtk.Align.CENTER)
        select_species_library_dropdown.set_factory(factory=dropdown_factory)
        select_species_library_dropdown.connect('notify::selected', self.on_species_library_select)
        select_species_library_dropdown.props.model = species_library_string_list
        species_library_row.add_suffix(widget=select_species_library_dropdown)

    def on_toggle_default(self, switch: Gtk.Switch):
        self.settings.aerosol_default = not self.settings.aerosol_default

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

    def on_season_select(self, dropdown: Gtk.DropDown, _):
        self.settings.aerosol_season = self.season_list[dropdown.get_selected()]

    def on_visibility_clear(self, entry: Gtk.Entry, _):
        self.visibility_entry.set_text(text='')

    def on_haze_select(self, dropdown: Gtk.DropDown, _):
        self.settings.aerosol_haze = self.haze_list[dropdown.get_selected()]

    def on_vulcan_select(self, dropdown: Gtk.DropDown, _):
        self.settings.aerosol_vulcan = self.vulcan_list[dropdown.get_selected()]

    def on_species_select(self, dropdown: Gtk.DropDown, _):
        self.settings.aerosol_species_file = self.species_list[dropdown.get_selected()]

    def on_species_library_select(self, dropdown: Gtk.DropDown, _):
        self.settings.aerosol_species_library = self.species_library_list[dropdown.get_selected()]