import sys
import os
import pathlib
import typing
import os
import signal

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
# gi.require_version('GioUnix', '2.0')
from gi.repository import Gtk, Gdk, Adw, GObject

sys.path.append(str(pathlib.Path.cwd()))
import atm_modelling.libRadtranPy.libradtranpy as libradtranpy

import page_spectral
import page_general_atm
import page_mol_atm
import page_aerosol
import page_surface
import page_geometry
import page_solver
import libRadtranGUI.page_simulation as page_simulation

try:
    os.environ['LIBRADTRANDIR']
except:
    os.environ['LIBRADTRANDIR'] = str(pathlib.Path(
        pathlib.Path.cwd(),
        'libRadtran-2.0.6'
    ))
else:
    print('Using system value for LIBRADTRANDIR')

class SideBar(Gtk.Revealer):
    def __init__(self) -> None:
        super().__init__(
            transition_type=Gtk.RevealerTransitionType.SLIDE_LEFT,
            reveal_child=True
        )
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b'''
            .custom-sidebar {
                background-color: @headerbar_bg_color;
            }
        ''')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.add_css_class('custom-sidebar')

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(child=main_box)

        header_bar = Adw.HeaderBar(show_end_title_buttons=False)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b'''
            .custom-sidebar-headerbar {
                background-color: @headerbar_bg_color;
                border-bottom: none;
                box-shadow: inset 0 -1px 0 transparent;
            }
        ''')
        header_bar.add_css_class('custom-sidebar-headerbar')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        main_box.append(child=header_bar)

        menu_button = Gtk.MenuButton(
            icon_name='open-menu-symbolic',
            tooltip_text='Main Menu'
        )
        header_bar.pack_end(child=menu_button)

        self.stack_sidebar = Gtk.StackSidebar(vexpand=True)
        main_box.append(child=self.stack_sidebar)

    def set_stack(self, stack: Gtk.Stack) -> None:
        self.stack_sidebar.set_stack(stack=stack)

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            title='libRadtran',
            default_width=650,
            default_height=575,
            width_request=350,
            height_request=125
    )
        window_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_content(content=window_box)

        sidebar = SideBar()
        window_box.append(child=sidebar)

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True
        )
        window_box.append(child=main_box)

        window_title = Adw.WindowTitle()
        header_bar = Gtk.HeaderBar(title_widget=window_title)
        if Gtk.HeaderBar().find_property(
            property_name='use_native_controls'
        ) is not None:
            header_bar.set_use_native_controls(True)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b'''
            .custom-headerbar {
                background-color: @window_bg_color;
            }
        ''')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        header_bar.add_css_class('custom-headerbar')
        main_box.append(child=header_bar)

        toggle_sidebar_button = Gtk.Button(
            icon_name='sidebar-show-symbolic',
            tooltip_text='Toggle sidebar'
        )
        toggle_sidebar_button.connect(
            'clicked',
            self.on_toggle_sidebar,
            sidebar
        )
        header_bar.pack_start(child=toggle_sidebar_button)

        stack = Gtk.Stack(vexpand=True)
        stack.set_transition_type(
            transition=Gtk.StackTransitionType.CROSSFADE
        )
        stack.connect(
            'notify::visible-child-name',
            self.on_page_changed,
            window_title
        )
        sidebar.set_stack(stack=stack)
        main_box.append(child=stack)

        # pages
        spectral_page_name = 'Spectral'
        self.spectral_page = page_spectral.SpectralPage()
        stack.add_titled(
            child=self.spectral_page,
            name=spectral_page_name,
            title=spectral_page_name
        )

        general_atm_page_name = 'General Atmosphere'
        self.general_atm_page = page_general_atm.GeneralAtmPage()
        stack.add_titled(
            child=self.general_atm_page,
            name=general_atm_page_name,
            title=general_atm_page_name
        )

        # mol_atm_page_name = 'Molecular Atmosphere'
        # self.mol_atm_page = page_mol_atm.MolAtmPage()
        # stack.add_titled(
        #     child=self.mol_atm_page,
        #     name=mol_atm_page_name,
        #     title=mol_atm_page_name
        # )

        aerosol_page_name = 'Aerosol'
        self.aerosol_page = page_aerosol.AerosolPage()
        stack.add_titled(
            child=self.aerosol_page,
            name=aerosol_page_name,
            title=aerosol_page_name
        )

        surface_page_name = 'Surface'
        self.surface_page = page_surface.SurfacePage()
        stack.add_titled(
            child=self.surface_page,
            name=surface_page_name,
            title=surface_page_name
        )

        # geometry_page_name = 'Geometry'
        # self.geometry_page = page_geometry.GeometryPage()
        # stack.add_titled(
        #     child=self.geometry_page,
        #     name=geometry_page_name,
        #     title=geometry_page_name
        # )

        solver_page_name = 'Solver'
        self.solver_page = page_solver.SolverPage()
        stack.add_titled(
            child=self.solver_page,
            name=solver_page_name,
            title=solver_page_name
        )

        simulation_page_name = 'Simulation'
        self.simulation_page = page_simulation.SimulationPage(
            set_simulation_callback=self.set_simulation,
            get_simulation_callback=self.get_simulation
        )
        stack.add_titled(
            child=self.simulation_page,
            name=simulation_page_name,
            title=simulation_page_name
        )

    def set_simulation(self) -> None:
        simulation = libradtranpy.Simulation()
        if hasattr(self, 'spectral_page'):
            simulation.spectral = self.spectral_page.spectral_settings()
        
        if hasattr(self, 'general_atm_page'):
            simulation.general_atm = self.general_atm_page.general_atm_settings()

        if hasattr(self, 'aerosol_page'):
            simulation.aerosol = self.aerosol_page.aerosol_settings()

        if hasattr(self, 'surface_page'):
            simulation.surface = self.surface_page.surface_settings()

        if hasattr(self, 'solver_page'):
            simulation.solver = self.solver_page.solver_settings()

        self.simulation = simulation
    
    def get_simulation(self) -> libradtranpy.Simulation:
        return self.simulation

    def on_toggle_sidebar(
            self,
            button: Gtk.Button,
            revealer: Gtk.Revealer
    ) -> None:
        revealer.set_reveal_child(
            reveal_child=not revealer.get_reveal_child()
        )

    def on_page_changed(
            self,
            stack: Gtk.Stack,
            param_spec_string: GObject.ParamSpecString,
            window_title: Adw.WindowTitle
    ) -> None:
        window_title.set_title(title=stack.get_visible_child_name() or '')

class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app: Adw.Application) -> None:
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == '__main__':
    app = App(application_id='com.github.FarisRedza.libRadtran')
    app.run(argv=sys.argv)
