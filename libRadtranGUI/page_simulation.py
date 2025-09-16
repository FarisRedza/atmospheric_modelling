import sys
import pathlib
import typing
import csv
import tempfile

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import matplotlib.backends.backend_gtk4agg
import matplotlib.pyplot

sys.path.append(str(pathlib.Path.cwd()))
import atm_modelling.libRadtranPy.libradtranpy as libradtranpy

import widgets

class SimulationGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            set_simulation_callback: typing.Callable,
            get_simulation_callback: typing.Callable,
            run_simulation_callback: typing.Callable
    ) -> None:
        super().__init__()
        self.set_simulation = set_simulation_callback
        self.get_simulation = get_simulation_callback
        
        run_row = widgets.ButtonRow(
            title='Run simulation',
            label='Run',
            callable=self.on_run_simulation,
            run_simulation_callback=run_simulation_callback
        )
        self.add(child=run_row)
    
    def on_run_simulation(self, run_simulation_callback: typing.Callable) -> None:
        self.set_simulation()
        run_simulation_callback()

class PlotGroup(Adw.PreferencesGroup):
    def __init__(self) -> None:
        super().__init__()
        plot_row = Adw.PreferencesRow(can_target=False)
        self.add(child=plot_row)

        self.xlim_min = 0
        self.xlim_max = 90
        self.ylim_min = 0
        self.ylim_max = 1
        self.grid = False

        self.figure, self.axes = matplotlib.pyplot.subplots()
        self.figure.tight_layout()
        self.axes.grid(visible=self.get_grid())

        self.plots = {}
        # self.plots['simulation'] = {
        #     'line': self.axes.plot([], [], label='simulation')[0]
        # }

        self.axes.legend(frameon=False)
        self.axes.set_xlim(self.xlim_min, self.xlim_max)
        self.axes.set_ylim(self.ylim_min, self.ylim_max)
        self.canvas = matplotlib.backends.backend_gtk4agg.FigureCanvasGTK4Agg(
            figure=self.figure
        )
        self.canvas.set_size_request(width=0, height=500)

        margin = 2
        plot_box = Gtk.Box(
            margin_top=margin,
            margin_bottom=margin,
            margin_start=margin,
            margin_end=margin
        )
        plot_row.set_child(child=plot_box)
        plot_box.append(child=self.canvas)

        grid_row = widgets.SwitchRow(
            title='Grid',
            callable=self.set_grid,
            active=self.get_grid()
        )
        self.add(child=grid_row)

    def set_grid(self, grid: bool) -> None:
        self.grid = grid
        
        self.axes.grid(visible=self.grid)
        self.canvas.draw_idle()
    
    def get_grid(self) -> bool:
        return self.grid

    def update_plot(self, csvfile) -> None:
        csvfile.seek(0)
        reader = csv.DictReader(csvfile)

        # Get all wavelength columns (skip the first one which is theta)
        fieldnames = reader.fieldnames
        if not fieldnames:
            return  # empty file
        wavelength_columns = [col for col in fieldnames if col != "# theta (deg)"]

        # Prepare storage
        libradtran_theta = []
        libradtran_edir = {wl: [] for wl in wavelength_columns}

        # Read rows
        for row in reader:
            libradtran_theta.append(float(row["# theta (deg)"]))
            for wl in wavelength_columns:
                libradtran_edir[wl].append(float(row[wl]))

        # Update each plot line
        for wl in wavelength_columns:
            if wl not in self.plots:
                # lazily create new line if needed
                line, = self.axes.plot([], [], label=wl)
                self.plots[wl] = {"line": line}

            self.plots[wl]["line"].set_data(libradtran_theta, libradtran_edir[wl])

        self.axes.relim()
        self.axes.autoscale_view()
        self.axes.legend()
        self.canvas.draw_idle()

class SimulationPage(Gtk.ScrolledWindow):
    def __init__(
            self,
            set_simulation_callback: typing.Callable,
            get_simulation_callback: typing.Callable
    ) -> None:
        super().__init__(
            hscrollbar_policy=Gtk.PolicyType.AUTOMATIC,
            vscrollbar_policy=Gtk.PolicyType.AUTOMATIC
        )
        self.set_simulation = set_simulation_callback
        self.get_simulation = get_simulation_callback

        margin = 16
        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_top=margin,
            margin_bottom=margin,
            margin_start=margin,
            margin_end=margin,
            spacing=margin
        )
        self.set_child(child=main_box)

        self.simulation_group = SimulationGroup(
            set_simulation_callback=self.set_simulation,
            get_simulation_callback=self.get_simulation,
            run_simulation_callback=self.run_simulation
        )
        main_box.append(child=self.simulation_group)

        self.plot_group = PlotGroup()
        main_box.append(child=self.plot_group)
    
    def run_simulation(self) -> None:
        simulation: libradtranpy.Simulation = self.get_simulation()
        simulation.solver = libradtranpy.Solver(rte_solver=libradtranpy.RTESolver.DISORT)
        simulation.geometry = libradtranpy.Geometry()
        simulation.output = libradtranpy.Output(
            quiet=True,
            output_user='lambda edir',
            output_quantity=libradtranpy.OutputQuantity.REFLECTIVITY
        )
        simulation.run_uvscpec()

        elevation = range(0, 91, 1)
        with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False, suffix='.csv') as csvfile:
            writer = csv.writer(csvfile)

            header = ['# theta (deg)']
            for wl in list(range(
                int(simulation.spectral.wavelength[0]),
                int(simulation.spectral.wavelength[-1])+1,
                1
            )):
                header.append(f'{int(wl)} nm')
            writer.writerow(header)

            for angle in elevation:
                simulation.geometry.sza = libradtranpy.degrees(90 - angle)
                result = simulation.run_uvscpec()
                lines = result.splitlines()
                values = []
                for line in lines:
                    wavelength, edir, *_ = map(float, line.split())
                    values.append(edir)

                row = [angle] + [val for val in values]
                writer.writerow(row)

            self.plot_group.update_plot(csvfile=csvfile)