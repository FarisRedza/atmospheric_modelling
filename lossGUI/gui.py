import sys
import os
import pathlib
import os
import signal

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, GObject

sys.path.append(str(pathlib.Path.cwd()))
import loss.libRadtranPy.libradtranpy as libradtranpy
import loss.diffraction as diffraction

import page_general
import page_diffraction
import page_libradtran
import page_background_light
import page_simulation

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
            title='lossGUI',
            default_width=650,
            default_height=575,
            width_request=350,
            height_request=125
    )
        self.connect('close-request', self.on_close_request)

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
        header_bar = Adw.HeaderBar(title_widget=window_title)
        if Adw.HeaderBar().find_property(
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
        general_page_name = 'General'
        self.general_page = page_general.GeneralPage()
        stack.add_titled(
            child=self.general_page,
            name=general_page_name,
            title=general_page_name
        )

        diffraction_page_name = 'Diffraction'
        self.diffraction_page = page_diffraction.DiffractionPage()
        stack.add_titled(
            child=self.diffraction_page,
            name=diffraction_page_name,
            title=diffraction_page_name
        )

        libradtran_page_name = 'Atmospheric'
        self.libradtran_page = page_libradtran.LibRadtranPage()
        stack.add_titled(
            child=self.libradtran_page,
            name=libradtran_page_name,
            title=libradtran_page_name
        )

        background_light_page_name = 'Background light'
        self.background_light_page = page_background_light.BackgroundLightPage()
        stack.add_titled(
            child=self.background_light_page,
            name=background_light_page_name,
            title=background_light_page_name
        )

        simulation_page_name = 'Simulation'
        self.simulation_page = page_simulation.SimulationPage(
            set_dif_simulation_callback=self.set_dif_simulation,
            get_dif_simulation_callback=self.get_dif_simulation,
            set_atm_simulation_callback=self.set_atm_simulation,
            get_atm_simulation_callback=self.get_atm_simulation
        )
        stack.add_titled(
            child=self.simulation_page,
            name=simulation_page_name,
            title=simulation_page_name
        )

    def set_dif_simulation(self, simulation: diffraction.DiffractionSim) -> None:
        self.diffraction_page.set_simulation(simulation=simulation)
    
    def get_dif_simulation(self) -> diffraction.DiffractionSim:
        return self.diffraction_page.get_simulation()

    def set_atm_simulation(self, simulation: libradtranpy.Simulation) -> None:
        self.libradtran_page.set_simulation(simulation=simulation)
    
    def get_atm_simulation(self) -> libradtranpy.Simulation:
        return self.libradtran_page.get_simulation()

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

    def on_close_request(self, window: Adw.ApplicationWindow) -> bool:
        os.kill(os.getpid(), signal.SIGINT)
        return False

class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app: Adw.Application) -> None:
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == '__main__':
    app = App(application_id='com.github.FarisRedza.lossGUI')
    app.run(argv=sys.argv)
