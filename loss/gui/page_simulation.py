import sys
import os
import typing
import csv
import tempfile
import pathlib

import matplotlib.backends.backend_gtk4agg
import matplotlib.backends.backend_gtk4cairo
import matplotlib.pyplot

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GObject

sys.path.append(
    os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir
    ))
)
import libRadtranPy.libradtranpy

class PlotGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            set_show_grid_callback: typing.Callable,
            get_show_grid_callback: typing.Callable
    ) -> None:
        super().__init__(title='Plot')
        self.fig, self.ax = matplotlib.pyplot.subplots()
        self.ax.grid(visible=get_show_grid_callback())
        self.ax.set_xlim(0, 90)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel(xlabel='Elevation Angle (°)')
        self.ax.set_ylabel(ylabel='Transmittance')

        self.libradtran_plot = self.ax.plot([],[],label='libRadtran')[0]

        # satquma
        satquma_theta = []
        satquma_edir = []
        satquma_file = 'MODTRAN_wl_785.0-850.0-5.0nm_h1_500.0km_h0_0.0km_elevation_data.csv'
        satquma_fiile_path = pathlib.Path(
            pathlib.Path.cwd(),
            'SatQuMA',
            'channel',
            'atmosphere',
            satquma_file
        )
        with open(file=satquma_fiile_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                satquma_theta.append(float(row['# theta (deg)']))
                satquma_edir.append(float(row['785 nm']))

        self.satquma_plot = self.ax.plot(
            satquma_theta,
            satquma_edir,
            label='SatQuMA'
        )[0]

        # bourgoin
        bourgoin_theta = []
        bourgoin_edir = []
        bourgoin_file = 'bourgoin_figure.csv'
        bourgoin_fiile_path = pathlib.Path(
            pathlib.Path.cwd(),
            'tests',
            'libradtran',
            bourgoin_file
        )
        with open(file=bourgoin_fiile_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bourgoin_theta.append(float(row['x']))
                bourgoin_edir.append(float(row[' y']))

        self.bourgoin_plot = self.ax.plot(
            bourgoin_theta,
            bourgoin_edir,
            label='Bourgoin'
        )[0]
        self.ax.legend()

        # self.canvas = matplotlib.backends.backend_gtk4agg.FigureCanvasGTK4Agg(
        #     figure=self.fig
        # )
        self.canvas = matplotlib.backends.backend_gtk4cairo.FigureCanvasGTK4Cairo(
            figure=self.fig
        )

        self.style_manager = Adw.StyleManager.get_default()
        self.style_manager.connect(
            'notify::dark',
            self.dark_plot
        )

        self.add(child=Gtk.Frame(child=self.canvas))

    def update_plot(self, csvfile) -> None:
        csvfile.seek(0)
        reader = csv.DictReader(csvfile)
        libradtran_theta = []
        libradtran_edir = []
        for row in reader:
            libradtran_theta.append(float(row['# theta (deg)']))
            libradtran_edir.append(float(row['785 nm']))

        self.libradtran_plot.set_data(libradtran_theta, libradtran_edir)
        self.canvas.draw_idle()

    def dark_plot(
            self,
            style_manager: Adw.StyleManager,
            gparam: GObject.GParamSpec
    ) -> None:
        if self.style_manager.get_dark() == True:
            self.fig.set_facecolor('#353535')
            self.ax.set_facecolor('#353535')

            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')

            self.ax.tick_params(axis='x', colors='white')
            self.ax.tick_params(axis='y', colors='white')

            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['top'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.spines['right'].set_color('white')
        else:
            self.fig.set_facecolor('white')
            self.ax.set_facecolor('white')

            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')

            self.ax.tick_params(axis='x', colors='black')
            self.ax.tick_params(axis='y', colors='black')

            self.ax.spines['bottom'].set_color('black')
            self.ax.spines['top'].set_color('black')
            self.ax.spines['left'].set_color('black')
            self.ax.spines['right'].set_color('black')

        self.canvas.draw_idle()

class Simulation(Adw.PreferencesPage):
    def __init__(
            self,
            set_settings_callback: typing.Callable,
            get_settings_callback: typing.Callable
    ) -> None:
        super().__init__()
        self.set_settings_callback = set_settings_callback
        self.get_settings_callback = get_settings_callback

        self.show_grid = False

        settings_group = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings_group)

        run_row = Adw.ActionRow(title='Run simulation')
        settings_group.add(child=run_row)
        run_button = Gtk.Button(
            label='Run',
            valign=Gtk.Align.CENTER
        )
        run_button.connect(
            'clicked',
            self.on_run_simulation
        )
        run_row.add_suffix(widget=run_button)

        grid_row = Adw.ActionRow(title='Show grid')
        settings_group.add(child=grid_row)
        grid_switch = Gtk.Switch(
            active=self.show_grid,
            valign=Gtk.Align.CENTER
        )
        grid_switch.connect(
            'notify::active',
            self.set_show_grid
        )
        grid_row.set_activatable_widget(widget=grid_switch)
        grid_row.add_suffix(widget=grid_switch)

        self.plot_group = PlotGroup(
            set_show_grid_callback=self.set_show_grid,
            get_show_grid_callback=self.get_show_grid
        )
        self.add(group=self.plot_group)

    def on_run_simulation(self, button: Gtk.Button) -> None:
        simulation: libRadtranPy.libradtranpy.Simulation = self.get_settings_callback()
        print(simulation)
        elevation = range(0, 91, 1)
        with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False, suffix='.csv') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['# theta (deg)', '785 nm'])
            for angle in elevation:
                simulation.geometry.sza = 90 - angle
                result = simulation.run_uvscpec()
                wavelength, edir, *_ = map(float, result.split())
                writer.writerow([angle, edir])

            self.plot_group.update_plot(csvfile=csvfile)

    def set_show_grid(
            self,
            switch: Gtk.Switch,
            gparam: GObject.GParamSpec
    ) -> None:
        self.show_grid = not self.show_grid
        self.plot_group.ax.grid(visible=self.show_grid)
        self.plot_group.canvas.draw_idle()

    def get_show_grid(self) -> bool:
        return self.show_grid
            