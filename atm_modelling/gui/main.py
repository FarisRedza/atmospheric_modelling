import sys
import os
import pathlib
import typing

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw

from page_aerosol import Aerosol
from page_spectral import Spectral
from page_general_atm import GeneralAtm
from page_mol_atm import MolAtm
from page_surface import Surface
from page_solver import Solver
from page_simulation import Simulation

sys.path.append(
    os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir
    ))
)
import libRadtran.libradtran
import libRadtran.aerosol
import libRadtran.general_atm
import libRadtran.mol_atm
import libRadtran.geometry
import libRadtran.surface
import libRadtran.spectral
import libRadtran.solver
import libRadtran.output

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
    def __init__(
            self,
            get_show_sidebar_callback: typing.Callable
    ) -> None:
        super().__init__(
            transition_type=Gtk.RevealerTransitionType.SLIDE_LEFT,
            reveal_child=get_show_sidebar_callback()
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

        self.side_bar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.side_bar_box.add_css_class('sidebar')
        self.set_child(child=self.side_bar_box)

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
        header_bar
        self.side_bar_box.append(child=header_bar)

        menu_button = Gtk.MenuButton(
            icon_name='open-menu-symbolic',
            tooltip_text='Main Menu'
        )
        header_bar.pack_end(child=menu_button)


    def add_stack_sidebar(self, stack_sidebar: Gtk.StackSidebar) -> None:
        self.side_bar_box.append(child=stack_sidebar)

class MainBox(Gtk.Box):
    def __init__(
            self,
            set_show_sidebar_callback: typing.Callable
    ):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            vexpand=True
        )
        self.header_bar_title = Adw.WindowTitle()
        header_bar = Adw.HeaderBar(
            title_widget=self.header_bar_title,
        )
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
        self.append(child=header_bar)

        sidebar_button = Gtk.Button(
            icon_name='sidebar-show-symbolic',
            tooltip_text='Toggle sidebar'
        )
        sidebar_button.connect('clicked', set_show_sidebar_callback)
        header_bar.pack_start(child=sidebar_button)

        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append(child=self.content_box)

    def add_stack(self, stack: Gtk.Stack) -> None:
        self.content_box.append(child=stack)

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title(title='libRadtran')
        self.set_default_size(width=750, height=720)
        self.set_size_request(width=430, height=130)

        self.show_sidebar = True
        self.settings = libRadtran.libradtran.Simulation(
            aerosol=libRadtran.aerosol.Aerosol(),
            general_atm=libRadtran.general_atm.GeneralAtm(),
            mol_atm=libRadtran.mol_atm.MolAtm(),
            geometry=libRadtran.geometry.Geometry(),
            surface=libRadtran.surface.Surface(),
            spectral=libRadtran.spectral.Spectral(),
            solver=libRadtran.solver.Solver(),
            output=libRadtran.output.Output(
                quiet=True,
                output_user='lambda edir',
                output_quantity=libRadtran.output.OutputQuantity.REFLECTIVITY
            )
        )

        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_content(content=content_box)

        self.sidebar = SideBar(
            get_show_sidebar_callback=self.get_show_sidebar
        )
        content_box.append(child=self.sidebar)

        main_box = MainBox(
            set_show_sidebar_callback=self.set_show_sidebar
        )
        content_box.append(child=main_box)

        stack = Gtk.Stack(transition_type=Gtk.StackTransitionType.CROSSFADE)
        main_box.add_stack(stack=stack)

        stack.add_titled(
            child=Spectral(
                set_settings_callback=self.set_settings_spectral,
                get_settings_callback=self.get_settings_spectral
            ),
            name='Spectral',
            title='Spectral'
        )
        stack.add_titled(
            child=GeneralAtm(
                set_settings_callback=self.set_settings_general_atm,
                get_settings_callback=self.get_settings_general_atm
            ),
            name='General Atmosphere',
            title='General Atmosphere'
        )
        stack.add_titled(
            child=MolAtm(
                set_settings_callback=self.set_settings_mol_atm,
                get_settings_callback=self.get_settings_mol_atm
            ),
            name='Molecular Atmosphere',
            title='Molecular Atmosphere'
        )
        stack.add_titled(
            child=Aerosol(
                set_settings_callback=self.set_settings_aerosol,
                get_settings_callback=self.get_settings_aerosol
            ),
            name='Aerosol',
            title='Aerosol'
        )
        stack.add_titled(
            child=Surface(
                set_settings_callback=self.set_settings_surface,
                get_settings_callback=self.get_settings_surface
            ),
            name='Surface',
            title='Surface'
        )
        stack.add_titled(
            child=Solver(
                set_settings_callback=self.set_settings_solver,
                get_settings_callback=self.get_settings_solver
            ),
            name='Solver',
            title='Solver'
        )
        stack.add_titled(
            child=Simulation(
                set_settings_callback=self.set_settings,
                get_settings_callback=self.get_settings
            ),
            name='Simulation',
            title='Simulation'
        )
        stack.connect(
            'notify::visible-child-name',
            lambda st, _: main_box.header_bar_title.set_title(st.get_visible_child_name())
        )

        main_box.header_bar_title.set_title(stack.get_visible_child_name())

        stack_sidebar = Gtk.StackSidebar(vexpand=True)
        stack_sidebar.set_css_classes([])
        stack_sidebar.set_stack(stack=stack)
        self.sidebar.add_stack_sidebar(stack_sidebar=stack_sidebar)

    def set_show_sidebar(self, button: Gtk.Button):
        self.show_sidebar = not self.show_sidebar
        self.sidebar.set_reveal_child(self.show_sidebar)

    def get_show_sidebar(self) -> bool:
        return self.show_sidebar
    
    def set_settings(self, settings: libRadtran.libradtran.Simulation) -> None:
        self.settings = settings
        print(self.settings)

    def get_settings(self) -> libRadtran.libradtran.Simulation:
        return self.settings

    def set_settings_spectral(self, settings: libRadtran.spectral.Spectral) -> None:
        self.settings.spectral = settings
        print(self.settings.spectral)

    def get_settings_spectral(self) -> libRadtran.spectral.Spectral:
        return self.settings.spectral
    
    def set_settings_general_atm(self, settings: libRadtran.general_atm.GeneralAtm) -> None:
        self.settings.general_atm = settings
        print(self.settings.general_atm)

    def get_settings_general_atm(self) -> libRadtran.general_atm.GeneralAtm:
        return self.settings.general_atm
    
    def set_settings_mol_atm(self, settings: libRadtran.mol_atm.MolAtm) -> None:
        self.settings.mol_atm = settings
        print(self.settings.mol_atm)

    def get_settings_mol_atm(self) -> libRadtran.mol_atm.MolAtm:
        return self.settings.mol_atm
    
    def set_settings_aerosol(self, settings: libRadtran.aerosol.Aerosol) -> None:
        self.settings.aerosol = settings
        print(self.settings.aerosol)

    def get_settings_aerosol(self) -> libRadtran.aerosol.Aerosol:
        return self.settings.aerosol
    
    def set_settings_surface(self, settings: libRadtran.surface.Surface) -> None:
        self.settings.surface = settings
        print(self.settings.surface)

    def get_settings_surface(self) -> libRadtran.surface.Surface:
        return self.settings.surface
    
    def set_settings_solver(self, settings: libRadtran.solver.Solver) -> None:
        self.settings.solver = settings
        print(self.settings.solver)

    def get_settings_solver(self) -> libRadtran.solver.Solver:
        return self.settings.solver

class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == '__main__':
    app = App(application_id='com.github.FarisRedza.libRadtran')
    app.run(sys.argv)
