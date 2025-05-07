import sys
import os
import typing

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GObject

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
import libRadtran.mol_atm

class MolAtm(Adw.PreferencesPage):
    def __init__(
            self,
            set_settings_callback: typing.Callable,
            get_settings_callback: typing.Callable
    ) -> None:
        super().__init__()
        self.set_settings_callback = set_settings_callback
        self.get_settings_callback = get_settings_callback

        settings_group = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings_group)

        # atmosphere dropdown
        atmosphere_row = Adw.ActionRow(title='Atmosphere')
        settings_group.add(child=atmosphere_row)

        atmosphere_dropdown = Gtk.DropDown().new_from_strings(
            strings=[i.name for i in libRadtran.mol_atm.Atmosphere]
        )
        atmosphere_dropdown.connect(
            'notify::selected',
            self.on_atmosphere_select
        )
        print(self.get_settings_callback())
        atmosphere_dropdown.set_selected(
            position=list(
                libRadtran.mol_atm.Atmosphere
            ).index(
                self.get_settings_callback().atmosphere_file
            )
        )
        atmosphere_dropdown.set_valign(align=Gtk.Align.CENTER)
        atmosphere_row.set_activatable_widget(widget=atmosphere_dropdown)
        atmosphere_row.add_suffix(widget=atmosphere_dropdown)

    def on_atmosphere_select(
            self,
            dropdown: Gtk.DropDown,
            gparam: GObject.GParamSpec
        ) -> None:
        settings: libRadtran.mol_atm.MolAtm = self.get_settings_callback()
        settings.atmosphere_file = list(
            libRadtran.mol_atm.Atmosphere
        )[dropdown.get_selected()]
        self.set_settings_callback(settings=settings)