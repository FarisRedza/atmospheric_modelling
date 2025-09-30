import sys
import pathlib
import typing
import csv
import dataclasses
import enum

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio

import matplotlib.backends.backend_gtk4agg
import matplotlib.pyplot
import matplotlib.lines
import scipy.interpolate
import numpy as np

sys.path.append(str(pathlib.Path.cwd()))
import loss.libRadtranPy.libradtranpy as libradtranpy
import loss.diffraction as diffraction

import widgets

class PlotType(enum.Enum):
    LOSS_TIME = 1
    TRANSMISSION_TIME = 2
    TRANSMISSION_ANGLE = 3
    LOSS_ANGLE = 4

@dataclasses.dataclass
class Plot:
    name: str
    line: matplotlib.lines.Line2D
    colour: widgets.Colours
    dif_sim: typing.Optional[diffraction.DiffractionSim] = None
    dif_sim_result: typing.Optional[diffraction.DiffractionSimResult] = None
    atm_sim: typing.Optional[libradtranpy.Simulation] = None
    atm_sim_result: typing.Optional[libradtranpy.SimulationResult] = None

class SimulationGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            run_simulation_callback: typing.Callable
    ) -> None:
        super().__init__(title='Simulation')
        self._run_simulation = run_simulation_callback

        self._diffraction = True
        self._atmospheric = False
        self._plot_type = PlotType.LOSS_TIME

        diffraction_row = widgets.SwitchRow(
            title='Diffraction',
            callable=self.set_diffraction,
            active=self.get_diffraction()
        )
        self.add(child=diffraction_row)

        atmospheric_row = widgets.SwitchRow(
            title='Atmospheric',
            callable=self.set_atmospheric,
            active=self.get_atmospheric()
        )
        self.add(child=atmospheric_row)

        plot_type_row = widgets.DropdownRow(
            title='Plot type',
            callable=self.set_plot_type,
            enum_class=PlotType,
            selected_value=self.get_plot_type()
        )
        self.add(child=plot_type_row)

        run_row = widgets.ButtonRow(
            title='Run simulation',
            label='Run',
            callable=self.run_simulation
        )
        self.add(child=run_row)

    def set_diffraction(self, diffraction: bool) -> None:
        self._diffraction = diffraction
    
    def get_diffraction(self) -> bool:
        return self._diffraction
    
    def set_atmospheric(self, atmospheric: bool) -> None:
        self._atmospheric = atmospheric
    
    def get_atmospheric(self) -> bool:
        return self._atmospheric
    
    def set_plot_type(self, plot_type: PlotType) -> None:
        self._plot_type = plot_type
    
    def get_plot_type(self) -> PlotType:
        return self._plot_type

    def run_simulation(self) -> None:
        self._run_simulation(
            self.get_diffraction(),
            self.get_atmospheric(),
            self.get_plot_type()
        )

class PlotInfoDialog(Adw.Dialog):
    def __init__(
            self,
            plot: Plot,
            content_height: int,
            content_width: int,
            update_plot_name_callback: typing.Callable[[str, str], None]
    ) -> None:
        super().__init__(
            content_height=content_height,
            content_width=content_width
        )
        self._plot = plot
        self._update_plot_name = update_plot_name_callback

        dialog_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(child=dialog_box)
        self._window_title = Adw.WindowTitle(title=self.get_plot_name())
        dialog_header_bar = Adw.HeaderBar(
            title_widget=self._window_title
        )
        dialog_box.append(child=dialog_header_bar)

        margin = 17
        info_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_top=margin,
            margin_bottom=margin,
            margin_start=margin,
            margin_end=margin,
            spacing=margin
        )
        dialog_box.append(child=info_box)

        general_group = Adw.PreferencesGroup(
            title='General'
        )
        info_box.append(child=general_group)

        name_row = widgets.EntryRow(
            title='Name',
            value=self.get_plot_name(),
            callable=self.set_plot_name
        )
        general_group.add(child=name_row)

        plot_colour_row = widgets.DropdownRow(
            title='Plot colour',
            enum_class=widgets.Colours,
            selected_value=self._plot.colour,
            callable=self.set_plot_colour
        )
        general_group.add(child=plot_colour_row)

        save_row = widgets.ButtonBarRow(
            label='Save',
            callable=self.on_save_plot,
            sensitive=False
        )
        general_group.add(child=save_row)

        diffraction_group = Adw.PreferencesGroup(
            title='Diffraction'
        )
        info_box.append(child=diffraction_group)
        diffraction_row = Adw.ActionRow()
        diffraction_group.add(child=diffraction_row)

        diffraction_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            hexpand=True
        )
        diffraction_row.set_child(child=diffraction_box)

        if self._plot.dif_sim is not None:
            attr_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            diffraction_box.append(child=attr_box)
            value_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            diffraction_box.append(child=value_box)
            for attr, value in self._plot.dif_sim.__dict__.items():
                attr_box.append(
                    child=Gtk.Label(label=attr, halign=Gtk.Align.START)
                )
                value_box.append(
                    child=Gtk.Label(label=value, halign=Gtk.Align.END, hexpand=True)
                )
        else:
            diffraction_box.append(
                child=Gtk.Label(label='None', hexpand=True)
            )

        atmosphere_group = Adw.PreferencesGroup(
            title='Atmosphere'
        )
        info_box.append(child=atmosphere_group)
        atmosphere_row = Adw.ActionRow()
        atmosphere_group.add(child=atmosphere_row)

        atmosphere_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            hexpand=True
        )
        atmosphere_row.set_child(child=atmosphere_box)

        if self._plot.atm_sim is not None:
            atmosphere_box.append(
                child=Gtk.Label(label=self._plot.atm_sim.generate_uvspec_input())
            )
        else:
            atmosphere_box.append(
                child=Gtk.Label(label='None', hexpand=True)
            )

    def set_plot_colour(self, colour: widgets.Colours) -> None:
        self._plot.colour = colour
        self._plot.line.set_color(color=colour.value)

    def set_plot_name(self, name: str) -> None:
        self._update_plot_name(self.get_plot_name(), name)
        self._plot.name = name
        self._plot.line.set_label(s=self.get_plot_name())
        self._window_title.set_title(title=self.get_plot_name())

    def get_plot_name(self) -> str:
        return self._plot.name
    
    def on_save_plot(self) -> None:
        file_dialog = Gtk.FileDialog(
            initial_name=f'{self._plot.name}.csv'
        )
        file_dialog.save(
            callback=self.save_file
        )

    def save_file(
            self,
            file_dialog: Gtk.FileDialog,
            task: Gio.Task
    ) -> None:
        file = file_dialog.save_finish(result=task)
        file_path = file.get_path()

class PlotDisplayGroup(Adw.PreferencesGroup):
    def __init__(self) -> None:
        super().__init__()

        self.xlim_min = -300
        self.xlim_max = 300
        self.ylim_min = 0
        self.ylim_max = 70
        self.grid = False

        self.figure, self.axes = matplotlib.pyplot.subplots()
        self.figure.tight_layout()
        self.axes.set_xlim(self.xlim_min, self.xlim_max)
        self.axes.set_ylim(self.ylim_min, self.ylim_max)
        
        self.canvas = matplotlib.backends.backend_gtk4agg.FigureCanvasGTK4Agg(
            figure=self.figure
        )
        self.canvas.set_size_request(
            width=0,
            height=500
        )

        plot_row = Adw.PreferencesRow(can_target=False)
        self.add(child=plot_row)
        margin = 2
        plot_box = Gtk.Box(
            margin_top=margin,
            margin_bottom=margin,
            margin_start=margin,
            margin_end=margin
        )
        plot_box.append(child=self.canvas)
        plot_row.set_child(child=plot_box)

        xlim_row = widgets.DoubleEntryRow(
            callable_1=self.set_xlim_min,
            callable_2=self.set_xlim_max,
            title='X limits',
            value_1=str(self.get_xlim_min()),
            value_2=str(self.get_xlim_max())
        )
        self.add(child=xlim_row)

        ylim_row = widgets.DoubleEntryRow(
            callable_1=self.set_ylim_min,
            callable_2=self.set_ylim_max,
            title='Y limits',
            value_1=str(self.get_ylim_min()),
            value_2=str(self.get_ylim_max())
        )
        self.add(child=ylim_row)

        grid_row = widgets.SwitchRow(
            title='Grid',
            callable=self.set_grid,
            active=self.get_grid()
        )
        self.add(child=grid_row)

    def set_xlim_min(self, value: int | str) -> None:
        self.xlim_min = int(value)
        self.axes.set_xlim(self.get_xlim_min(), self.get_xlim_max())
        self.update_plot()

    def get_xlim_min(self) -> int:
        return self.xlim_min

    def set_xlim_max(self, value: int | str) -> None:
        self.xlim_max = int(value)
        self.axes.set_xlim(self.get_xlim_min(), self.get_xlim_max())
        self.update_plot()

    def get_xlim_max(self) -> int:
        return self.xlim_max

    def set_ylim_min(self, value: int | str) -> None:
        self.ylim_min = int(value)
        self.axes.set_ylim(self.get_ylim_min(), self.get_ylim_max())
        self.update_plot()

    def get_ylim_min(self) -> int:
        return self.ylim_min

    def set_ylim_max(self, value: int | str) -> None:
        self.ylim_max = int(value)
        self.axes.set_ylim(self.get_ylim_min(), self.get_ylim_max())
        self.update_plot()

    def get_ylim_max(self) -> int:
        return self.ylim_max

    def set_grid(self, grid: bool) -> None:
        self.grid = grid
        self.axes.grid(visible=self.grid)
        self.update_plot()

    def get_grid(self) -> bool:
        return self.grid

    def add_plot(self, plot: Plot) -> None:
        self.axes.add_line(line=plot.line)
        self.update_plot()

    def remove_plot(self, plot: Plot) -> None:
        plot.line.remove()
        self.update_plot()
    
    def update_plot(self) -> None:
        self.axes.legend(frameon=False)
        self.canvas.draw_idle()

class PlotsGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            get_plots_callback: typing.Callable[[], list[Plot]],
            set_plots_callback: typing.Callable[[list[Plot]], None],
            remove_plot: typing.Callable[[Plot], None],
            update_plot_callback: typing.Callable,
            load_plot_from_file_callback: typing.Callable
    ) -> None:
        super().__init__(title='Plots')
        self._get_plots = get_plots_callback
        self._set_plots = set_plots_callback
        self._remove_plot = remove_plot
        self._update_plot = update_plot_callback
        self._load_plot_from_file = load_plot_from_file_callback

        self.plot_rows: list[Adw.ActionRow] = []

        load_plot_row = widgets.ButtonBarRow(
            label='Load plot',
            callable=self.on_load_plot
        )
        self.add(child=load_plot_row)

    def add_plot(self, plot: Plot) -> None:
        row = widgets.DoubleButtonRow(
            title=plot.name,
            subtitle=str(plot.line.get_color()),
            label_1='Info',
            label_2='Remove',
            icon_name_1='dialog-information-symbolic',
            icon_name_2='list-remove-symbolic',
            callable_1=self.plot_info,
            callable_2=self.remove_plot,
            plot=plot
        )
        self.plot_rows.append(row)
        self.add(child=row)

    def remove_plot(self, plot: Plot) -> None:
        self._remove_plot(plot=plot)
        row = next(
            (r for r in self.plot_rows if r.get_title() == plot.name),
            None
        )
        if row is None:
            raise RuntimeError(f'Row {plot.name} not found')
        
        self.remove(child=row)
        self.plot_rows.remove(row)
    
    def plot_info(self, plot: Plot) -> None:
        self.plot_info_dialog = PlotInfoDialog(
            plot=plot,
            content_height=500,
            content_width=400,
            update_plot_name_callback=self.update_plot_name
        )
        self.plot_info_dialog.present()

    def get_plot_name(self, plot: Plot) -> str:
        return plot.name

    def update_plot_name(self, old_name: str, new_name: str) -> None:
        row = next((r for r in self.plot_rows if r.get_title() == old_name), None)
        if row is None:
            raise RuntimeError(f'Row {old_name} not found')
        row.set_title(title=new_name)
        self._update_plot()

    def on_load_plot(self) -> None:
        file_dialog = Gtk.FileDialog()
        file_dialog.open(
            callback=self.open_file
        )

    def open_file(
            self,
            file_dialog: Gtk.FileDialog,
            task: Gio.Task
    ) -> None:
        file = file_dialog.open_finish(result=task)
        file_path = file.get_path()
        if file_path:
            self._load_plot_from_file(pathlib.Path(file_path))


class SimulationPage(Gtk.ScrolledWindow):
    def __init__(
            self,
            set_dif_simulation_callback: typing.Callable,
            get_dif_simulation_callback: typing.Callable,
            set_atm_simulation_callback: typing.Callable,
            get_atm_simulation_callback: typing.Callable
    ) -> None:
        super().__init__(
            hscrollbar_policy=Gtk.PolicyType.AUTOMATIC,
            vscrollbar_policy=Gtk.PolicyType.AUTOMATIC
        )
        self.set_dif_simulation = set_dif_simulation_callback
        self.get_dif_simulation = get_dif_simulation_callback
        self.set_atm_simulation = set_atm_simulation_callback
        self.get_atm_simulation = get_atm_simulation_callback

        self._plots: list[Plot] = []

        margin = 17
        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_top=margin+6,
            margin_bottom=margin+6,
            margin_start=margin,
            margin_end=margin,
            spacing=margin+12
        )
        self.set_child(child=main_box)

        simulation_group = SimulationGroup(
            run_simulation_callback=self.run_simulation
        )
        main_box.append(child=simulation_group)

        self.plot_display_group = PlotDisplayGroup()
        main_box.append(child=self.plot_display_group)

        self.plots_group = PlotsGroup(
            get_plots_callback=self.get_plots,
            set_plots_callback=self.set_plots,
            remove_plot=self.remove_plot,
            update_plot_callback=self.update_plot,
            load_plot_from_file_callback=self.load_plot_from_file
        )
        main_box.append(child=self.plots_group)

    def get_plots(self) -> list[Plot]:
        return self._plots

    def set_plots(self, plots: list[Plot]) -> None:
        self._plots = plots

    def add_plot(
            self,
            x,
            y,
            name: typing.Optional[str] = None,
            dif_sim: typing.Optional[diffraction.DiffractionSim] = None,
            dif_sim_result: typing.Optional[diffraction.DiffractionSimResult] = None,
            atm_sim: typing.Optional[libradtranpy.Simulation] = None,
            atm_sim_result: typing.Optional[libradtranpy.SimulationResult] = None
    ) -> None:
        plot_count = len(self.get_plots())
        if not name:
            name = f'Plot {plot_count+1}'

        plot = Plot(
            name=name,
            line=matplotlib.lines.Line2D(
                xdata=x,
                ydata=y,
                label=name,
                color=list(widgets.Colours)[plot_count].value
            ),
            colour=list(widgets.Colours)[plot_count],
            dif_sim=dif_sim,
            atm_sim=atm_sim
        )
        self._plots.append(plot)
        self.plot_display_group.add_plot(plot=plot)
        self.plots_group.add_plot(plot=plot)
    
    def remove_plot(self, plot: Plot) -> None:
        self.plot_display_group.remove_plot(plot=plot)
        self._plots.remove(plot)

    def rename_plot(self, name: str) -> None:
        plot = next(
            (p for p in self.get_plots() if p.name == name),
            None
        )
        if plot is None:
            raise RuntimeError(f'Plot {name} not found')

        print(self._plots.index(plot))
    
    def update_plot(self) -> None:
        self.plot_display_group.update_plot()

    def load_plot_from_file(self, file_path: pathlib.Path) -> None:
        line_count = 0
        with open(file=file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            atm_transmission: list[float] = []
            atm_elevation: list[float] = []
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    atm_elevation.append(float(row[0]))
                    atm_transmission.append(float(row[1]))
        
        atm_data = libradtranpy.SimulationResult(
            elevations=atm_elevation,
            transmissions=atm_transmission
        )

        self.add_plot(
            x=atm_data.elevations,
            y=atm_data.transmissions
        )

    def run_simulation(
            self,
            enable_diffraction: bool,
            enable_atmospheric: bool,
            plot_type: PlotType,
    ) -> None:
        dif_sim: diffraction.DiffractionSim = self.get_dif_simulation()
        dif_sim_result = dif_sim.run_sim()

        times = dif_sim_result.times

        if not enable_diffraction:
            dif_sim = None

        if enable_atmospheric:
            atm_sim: libradtranpy.Simulation = self.get_atm_simulation()
            atm_sim_result = atm_sim.run_transmission_against_elevation()
        else:
            atm_sim = None

        match plot_type:
            case PlotType.LOSS_TIME:
                x=times
                y = np.zeros(len(dif_sim_result.times))

                if enable_diffraction:
                    y += -10*np.log10(dif_sim_result.transmissions)
                if enable_atmospheric:
                    atm_interpolated = scipy.interpolate.interp1d(
                        x=atm_sim_result.elevations,
                        y=atm_sim_result.transmission_as_dB(),
                        kind='linear'
                    )
                    atm_interpolated_dB = atm_interpolated(dif_sim_result.elevations)
                    y += atm_interpolated_dB
            
            case PlotType.TRANSMISSION_TIME:
                x=times
                y = np.zeros(len(dif_sim_result.times))

                if enable_diffraction:
                    y += dif_sim_result.transmissions
                if enable_atmospheric:
                    atm_interpolated = scipy.interpolate.interp1d(
                        x=atm_sim_result.elevations,
                        y=atm_sim_result.transmissions,
                        kind='linear'
                    )
                    atm_interpolated_loss = atm_interpolated(dif_sim_result.elevations)
                    y += atm_interpolated_loss

            case PlotType.LOSS_ANGLE:
                x=dif_sim_result.elevations
                y = np.zeros(len(dif_sim_result.elevations))
                
                if enable_diffraction:
                    y += -10*np.log10(dif_sim_result.transmissions)
                if enable_atmospheric:
                    atm_interpolated = scipy.interpolate.interp1d(
                        x=atm_sim_result.elevations,
                        y=atm_sim_result.transmission_as_dB(),
                        kind='linear'
                    )
                    atm_interpolated_loss = atm_interpolated(dif_sim_result.elevations)
                    y += atm_interpolated_loss

            case PlotType.TRANSMISSION_ANGLE:
                x=dif_sim_result.elevations
                y = np.zeros(len(dif_sim_result.elevations))
                
                if enable_diffraction:
                    y += dif_sim_result.transmissions
                if enable_atmospheric:
                    atm_interpolated = scipy.interpolate.interp1d(
                        x=atm_sim_result.elevations,
                        y=atm_sim_result.transmissions,
                        kind='linear'
                    )
                    atm_interpolated_loss = atm_interpolated(dif_sim_result.elevations)
                    y += atm_interpolated_loss

            case _:
                raise RuntimeError(f'Unsupported plot: {plot_type}')

        self.add_plot(
            x=x,
            y=y,
            dif_sim=dif_sim,
            atm_sim=atm_sim
        )