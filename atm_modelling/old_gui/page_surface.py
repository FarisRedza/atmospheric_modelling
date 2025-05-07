import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

from atm_modelling.libRadtran import surface

class Surface(Adw.PreferencesPage):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = surface.Surface()

        # settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title(title='Settings')
        self.add(settings_group)

        ## altitude row
        altitude_row = Adw.ActionRow(title='Altitude')
        settings_group.add(child=altitude_row)

        ### altitude entry
        self.altitude_entry = Gtk.Entry(
            placeholder_text=surface.Surface.__dataclass_fields__['altitude'].default,
            valign=Gtk.Align.CENTER
        )
        self.altitude_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.altitude_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.altitude_entry.connect(
            'icon_press',
            self.on_altitude_clear
        )
        altitude_row.add_suffix(widget=self.altitude_entry)

        ## albedo row
        albedo_row = Adw.ActionRow(title='Albedo')
        settings_group.add(child=albedo_row)

        ### albedo entry
        self.albedo_entry = Gtk.Entry(
            placeholder_text=surface.Surface.__dataclass_fields__['albedo'].default,
            valign=Gtk.Align.CENTER
        )
        self.albedo_entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.SECONDARY,
            icon_name='edit-clear-symbolic'
        )
        self.albedo_entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            'Clear'
        )
        self.albedo_entry.connect(
            'icon_press',
            self.on_albedo_clear
        )
        albedo_row.add_suffix(widget=self.albedo_entry)

    def on_altitude_clear(self, entry: Gtk.Entry, _):
        self.altitude_entry.set_text(text='')

    def on_albedo_clear(self, entry: Gtk.Entry, _):
        self.albedo_entry.set_text(text='')