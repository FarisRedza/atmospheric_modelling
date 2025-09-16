import sys
import pathlib

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import widgets

sys.path.append(str(pathlib.Path.cwd()))
import atm_modelling.libRadtranPy.libradtranpy as libradtranpy

class SolverPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()
        settings = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings)

        self.rte_solver = libradtranpy.RTESolver.DISORT

        solver_string_list = Gtk.StringList()
        for i in libradtranpy.RTESolver:
            solver_string_list.append(i.name)
        solver_row = widgets.DropdownRow(
            callable=self.set_rte_solver,
            title='Solver',
            string_list=solver_string_list,
            selected=list(libradtranpy.RTESolver).index(
                self.get_rte_solver()
            )
        )
        settings.add(child=solver_row)

    def set_rte_solver(
            self,
            rte_solver: libradtranpy.RTESolver | None = None,
            index: int | None = None
    ) -> None:
        if rte_solver:
            self.rte_solver = rte_solver
        elif index is not None:
            self.rte_solver = libradtranpy.RTESolver.from_index(
                index=index
            )
    
    def get_rte_solver(self) -> libradtranpy.RTESolver:
        return self.rte_solver

    def solver_settings(self) -> libradtranpy.Solver:
        settings = libradtranpy.Solver(
            rte_solver=self.rte_solver
        )
        return settings