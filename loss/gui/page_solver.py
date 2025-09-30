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
import libRadtranPy.solver

class Solver(Adw.PreferencesPage):
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

        # solver
        solver_row = Adw.ActionRow(title='Solver')
        settings_group.add(child=solver_row)

        solver_dropdown = Gtk.DropDown().new_from_strings(
            strings=[i.name for i in libRadtranPy.solver.RTESolver]
        )
        solver_dropdown.connect(
            'notify::selected',
            self.on_solver_select
        )
        solver_dropdown.set_selected(
            position=list(
                libRadtranPy.solver.RTESolver
            ).index(
                self.get_settings_callback().rte_solver
            )
        )
        solver_dropdown.set_valign(align=Gtk.Align.CENTER)
        solver_row.set_activatable_widget(widget=solver_dropdown)
        solver_row.add_suffix(widget=solver_dropdown)

    def on_solver_select(
            self,
            dropdown: Gtk.DropDown,
            gparam: GObject.GParamSpec
        ) -> None:
        settings: libRadtranPy.solver.Solver = self.get_settings_callback()
        settings.rte_solver = list(
            libRadtranPy.solver.RTESolver
        )[dropdown.get_selected()]
        self.set_settings_callback(settings=settings)