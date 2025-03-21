import sys
import dataclasses

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Adw, GObject

from page_spectral import Spectral
from page_general_atm import GeneralAtm
from page_mol_atm import MolAtm
from page_aerosol import Aerosol
from page_profile import Profile
from page_clouds import Clouds
from page_surface import Surface
from page_solver import Solver
from page_monte_carlo import MonteCarlo
from page_geometry import Geometry
from page_output import Output

@dataclasses.dataclass
class Settings():
    manually_shown: bool = False
    manually_hidden: bool = False

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title(title='libRadtran')
        self.set_default_size(width=580, height=550)
        self.set_size_request(width=430, height=130)

        self.connect("notify::default-width", self.on_window_resize)
        self.connect("notify::default-height", self.on_window_resize)

        self.settings = Settings()

        # content box
        content_box = Gtk.Box()
        self.set_content(content=content_box)

        ## sidebar
        self.revealer = Gtk.Revealer(
            transition_type=Gtk.RevealerTransitionType.SLIDE_LEFT,
            reveal_child=True
        )
        content_box.append(child=self.revealer)

        ### sidebar toolbar view
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.add_css_class("sidebar")
        self.revealer.set_child(child=sidebar_box)

        #### sidebar header bar
        sidebar_header_bar = Adw.HeaderBar(show_end_title_buttons=False)
        sidebar_header_bar.set_css_classes(['headerbar-bg-color'])
        sidebar_box.append(child=sidebar_header_bar)

        ##### menu button
        menu_button = Gtk.MenuButton(
            icon_name='open-menu-symbolic',
            tooltip_text='Main Menu'
        )
        sidebar_header_bar.pack_end(child=menu_button)

        ###### menuadd_css_class
        menu = Gio.Menu.new()
        menu_button.set_menu_model(menu)

        ###### menu items
        menu.append(label='New Window', detailed_action='app.new_window')
        menu.append(label='Full Screen', detailed_action='app.full_screen')
        menu.append(label='Help', detailed_action='app.help')
        menu.append(label='About libRadtran', detailed_action='app.about')
        menu.append(label='Quit', detailed_action='app.quit')

        ### sidebar scrolled window
        sidebar_scrolled_window = Gtk.ScrolledWindow()
        sidebar_box.append(child=sidebar_scrolled_window)

        #### stack sidebar
        stack_sidebar = Gtk.StackSidebar(vexpand=True)
        stack_sidebar.set_css_classes([])
        sidebar_scrolled_window.set_child(child=stack_sidebar)

        ## main view
        # toolbar_view = Adw.ToolbarView()
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content_box.append(child=main_box)

        ### header bar
        header_bar = Adw.HeaderBar()
        main_box.append(child=header_bar)

        #### header bar title
        self.header_bar_title = Adw.WindowTitle()
        header_bar.set_title_widget(self.header_bar_title)

        #### sidebar button
        sidebar_button = Gtk.Button(
            icon_name='sidebar-show-symbolic',
            tooltip_text='Toggle sidebar'
        )
        sidebar_button.connect('clicked', self.on_toggle_sidebar)
        header_bar.pack_start(child=sidebar_button)

        ### stack
        stack = Gtk.Stack()
        stack.set_transition_type(
            transition=Gtk.StackTransitionType.CROSSFADE
        )
        stack.connect('notify::visible-child-name', self.on_page_changed)
        stack_sidebar.set_stack(stack)
        main_box.append(child=stack)

        #### stack pages
        stack.add_titled(
            child=Spectral(self),
            name='Spectral',
            title='Spectral'
        )
        stack.add_titled(
            child=GeneralAtm(self),
            name='General Atmosphere',
            title='General Atmosphere'
        )
        stack.add_titled(
            child=MolAtm(self),
            name='Molecular Atmosphere',
            title='Molecular Atmosphere'
        )
        stack.add_titled(
            child=Aerosol(self),
            name='Aerosol',
            title='Aerosol'
        )
        stack.add_titled(
            child=Profile(self),
            name='Profile',
            title='Profile'
        )
        stack.add_titled(
            child=Clouds(self),
            name='Clouds',
            title='Clouds'
        )
        stack.add_titled(
            child=Surface(self),
            name='Surface',
            title='Surface'
        )
        stack.add_titled(
            child=Solver(self),
            name='Solver',
            title='Solver'
        )
        stack.add_titled(
            child=MonteCarlo(self),
            name='Monte Carlo',
            title='Monte Carlo'
        )
        stack.add_titled(
            child=Geometry(self),
            name='Geometry',
            title='Geometry'
        )
        stack.add_titled(
            child=Output(self),
            name='Output',
            title='Output'
        )

    def on_toggle_sidebar(self, button):
        if self.revealer.get_reveal_child() == True:
            self.settings.manually_hidden= True
        else:
            self.settings.manually_shown= True

        self.revealer.set_reveal_child(
            not self.revealer.get_reveal_child()
        )

    def on_window_resize(self, widget, _):
        width = self.get_default_size().width
        if width < 550:
            if not self.settings.manually_shown:
                self.revealer.set_reveal_child(False)
        else:
            if not self.settings.manually_hidden:
                self.revealer.set_reveal_child(True)

        if width >= 550:
            self.settings.manually_shown= False
        elif width < 550:
            self.settings.manually_hidden= False

    def on_page_changed(self, stack, _):
        self.header_bar_title.set_title(stack.get_visible_child_name())


class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

        # menu actions
        new_window_action = Gio.SimpleAction.new(
            name='new_window',
            parameter_type=None
        )
        new_window_action.connect('activate', self.on_new_window)
        self.add_action(new_window_action)

        full_screen_action = Gio.SimpleAction.new(
            name='full_screen',
            parameter_type=None
        )
        full_screen_action.connect('activate', self.on_full_screen)
        self.add_action(full_screen_action)

        help_action = Gio.SimpleAction.new(
            name='help',
            parameter_type=None
        )
        help_action.connect('activate', self.on_help)
        self.add_action(help_action)

        about_action = Gio.SimpleAction.new(
            name='about',
            parameter_type=None
        )
        about_action.connect('activate', self.on_about)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new(
            name='quit',
            parameter_type=None
        )
        quit_action.connect('activate', self.on_quit)
        self.add_action(quit_action)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

    def on_new_window(self, action, param):
        new_win = MainWindow(application=self)
        new_win.present()

    def on_full_screen(self, action, param):
        active_window = self.get_active_window()
        if active_window:
            if active_window.is_fullscreen():
                active_window.unfullscreen()
            else:
                active_window.fullscreen()

    def on_help(self, action, _):
        help_dialog = Gtk.MessageDialog(
            transient_for=self.get_active_window(),
            modal=True,
            buttons=Gtk.ButtonsType.OK,
            text='Help',
            secondary_text=''
        )
        help_dialog.connect('response', lambda dialog, response: dialog.destroy())
        help_dialog.present()

    def on_about(self, action, _):
        about_dialog = Gtk.AboutDialog(
            transient_for=self.win,
            modal=True
        )
        about_dialog.set_logo_icon_name(icon_name='tag-symbolic')
        about_dialog.set_program_name(name='libRadtran')
        about_dialog.set_version(version='0.1')
        about_dialog.set_authors(
            authors=['Faris Redza']
        )
        about_dialog.set_website(
            website='https://github.com/FarisRedza/atmospheric_modelling'
        )
        about_dialog.present()

    def on_quit(self, action, _):
        self.quit()


if __name__ == '__main__':
    app = App(application_id='com.github.FarisRedza.libRadtran')
    app.run(sys.argv)
