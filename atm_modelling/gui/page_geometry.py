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
        sza_row = Adw.ActionRow(title='Solar Zenith Angle')
        settings_group.add(child=sza_row)

        ### sza entry
        self.sza_entry = Gtk.Entry(
            placeholder_text='sza',
            valign=Gtk.Align.CENTER
        )
        self.sza_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.sza_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.sza_entry.connect(
            'icon_press',
            self.on_sza_clear
        )
        sza_row.add_suffix(widget=self.sza_entry)

        ## phi0 row
        phi0_row = Adw.ActionRow(title='Phi0')
        settings_group.add(child=phi0_row)

        ### phi0 entry
        self.phi0_entry = Gtk.Entry(
            placeholder_text='phi0',
            valign=Gtk.Align.CENTER
        )
        self.phi0_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.phi0_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.phi0_entry.connect(
            'icon_press',
            self.on_phi0_clear
        )
        phi0_row.add_suffix(widget=self.phi0_entry)

        ## phi row
        phi_row = Adw.ActionRow(title='Phi')
        settings_group.add(child=phi_row)

        ### phi entry
        self.phi_entry = Gtk.Entry(
            placeholder_text='phi',
            valign=Gtk.Align.CENTER
        )
        self.phi_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.phi_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.phi_entry.connect(
            'icon_press',
            self.on_phi_clear
        )
        phi_row.add_suffix(widget=self.phi_entry)

        ## umu row
        umu_row = Adw.ActionRow(title='Umu')
        settings_group.add(child=umu_row)

        ### umu entry
        self.umu_entry = Gtk.Entry(
            placeholder_text='umu',
            valign=Gtk.Align.CENTER
        )
        self.umu_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.umu_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.umu_entry.connect(
            'icon_press',
            self.on_umu_clear
        )
        umu_row.add_suffix(widget=self.umu_entry)

        ## day_of_year row
        day_of_year_row = Adw.ActionRow(title='Day of Year')
        settings_group.add(child=day_of_year_row)

        ### day_of_year entry
        self.day_of_year_entry = Gtk.Entry(
            placeholder_text='day_of_year',
            valign=Gtk.Align.CENTER
        )
        self.day_of_year_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.day_of_year_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.day_of_year_entry.connect(
            'icon_press',
            self.on_day_of_year_clear
        )
        day_of_year_row.add_suffix(widget=self.day_of_year_entry)

        ## latitude row
        latitude_row = Adw.ActionRow(title='Latitude')
        settings_group.add(child=latitude_row)

        ### latitude entry
        self.latitude_entry = Gtk.Entry(
            placeholder_text='latitude',
            valign=Gtk.Align.CENTER
        )
        self.latitude_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.latitude_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.latitude_entry.connect(
            'icon_press',
            self.on_latitude_clear
        )
        latitude_row.add_suffix(widget=self.latitude_entry)

        ## longitude row
        longitude_row = Adw.ActionRow(title='Longitude')
        settings_group.add(child=longitude_row)

        ### longitude entry
        self.longitude_entry = Gtk.Entry(
            placeholder_text='longitude',
            valign=Gtk.Align.CENTER
        )
        self.longitude_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.longitude_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.longitude_entry.connect(
            'icon_press',
            self.on_longitude_clear
        )
        longitude_row.add_suffix(widget=self.longitude_entry)

        ## time row
        time_row = Adw.ActionRow(title='Time')
        settings_group.add(child=time_row)

        ### time entry
        self.time_entry = Gtk.Entry(
            placeholder_text='time',
            valign=Gtk.Align.CENTER
        )
        self.time_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.time_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.time_entry.connect(
            'icon_press',
            self.on_time_clear
        )
        time_row.add_suffix(widget=self.time_entry)

    def on_sza_clear(self, entry, _):
        self.sza_entry.set_text(text='')

    def on_phi0_clear(self, entry, _):
        self.phi0_entry.set_text(text='')

    def on_phi_clear(self, entry, _):
        self.phi_entry.set_text(text='')

    def on_umu_clear(self, entry, _):
        self.umu_entry.set_text(text='')

    def on_day_of_year_clear(self, entry, _):
        self.day_of_year_entry.set_text(text='')

    def on_latitude_clear(self, entry, _):
        self.latitude_entry.set_text(text='')

    def on_longitude_clear(self, entry, _):
        self.longitude_entry.set_text(text='')

    def on_time_clear(self, entry, _):
        self.time_entry.set_text(text='')