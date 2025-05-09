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
import libRadtranPy.output

class Output(Adw.PreferencesPage):
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
