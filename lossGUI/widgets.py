import typing
import enum
import platform

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GObject, Gdk

def rgba_to_tuple(rgba: Gdk.RGBA) -> tuple[float, float, float, float]:
    return (rgba.red, rgba.green, rgba.blue, rgba.alpha)

class Colours(enum.Enum):
    BLUE = (0.207843, 0.517647, 0.894118, 1.000000)
    TEAL = (0.129412, 0.564706, 0.643137, 1.000000)
    GREEN = (0.227451, 0.580392, 0.290196, 1.000000)
    YELLOW = (0.784314, 0.533333, 0.000000, 1.000000)
    ORANGE = (0.929412, 0.356863, 0.000000, 1.000000)
    RED = (0.901961, 0.176471, 0.258824, 1.000000)
    PINK = (0.835294, 0.380392, 0.600000, 1.000000)
    PURPLE = (0.568627, 0.254902, 0.674510, 1.000000)
    SLATE = (0.435294, 0.513726, 0.588235, 1.000000)
    BROWN = (0.701961, 0.568627, 0.411765, 1.000000)
    LIGHT = (1, 1, 1, 1)
    DARK = (53/255, 53/255, 53/255, 1)

    @staticmethod
    def system_colours() -> dict[str, tuple[float, float, float, float]]:
        """Return a dict of system colours if available, else fallback to enum defaults."""
        if Adw.get_minor_version() >= 6 and platform.system() == "Linux":
            colours = {
                colour.name: rgba_to_tuple(colour.to_rgba())
                for colour in Adw.AccentColor
            }
            colours["LIGHT"] = (1, 1, 1, 1)
            colours["DARK"] = (61/255, 61/255, 61/255, 1)
            return colours
        else:
            # fallback to the enum values
            return {c.name: c.value for c in Colours}

class ButtonRow(Adw.ActionRow):
    def __init__(
            self,
            title: str,
            label: str,
            callable: typing.Callable,
            subtitle: str = '',
            icon_name: typing.Optional[str] = None,
            sensitive: bool = True,
            *args: typing.Any,
            **kwargs: typing.Any
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            sensitive=sensitive
        )

        button = Gtk.Button(
            valign=Gtk.Align.CENTER,
            label=label,
        )
        if icon_name:
            button.set_icon_name(icon_name=icon_name)

        button.connect(
            'clicked',
            self.on_button,
            callable,
            args,
            kwargs
        )
        self.add_suffix(widget=button)
    
    def on_button(
            self,
            button: Gtk.Button,
            callable: typing.Callable,
            args: tuple,
            kwargs: dict
    ) -> None:
        callable(*args, **kwargs)

class DoubleButtonRow(Adw.ActionRow):
    def __init__(
            self,
            title: str,
            label_1: str,
            label_2: str,
            callable_1: typing.Callable,
            callable_2: typing.Callable,
            subtitle: str = '',
            icon_name_1: typing.Optional[str] = None,
            icon_name_2: typing.Optional[str] = None,
            sensitive: bool = True,
            *args: typing.Any,
            **kwargs: typing.Any
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            sensitive=sensitive
        )

        button_1 = Gtk.Button(
            valign=Gtk.Align.CENTER,
            label=label_1,
        )
        if icon_name_1:
            button_1.set_icon_name(icon_name=icon_name_1)

        button_1.connect(
            'clicked',
            self.on_button,
            callable_1,
            args,
            kwargs
        )
        self.add_suffix(widget=button_1)

        button_2 = Gtk.Button(
            valign=Gtk.Align.CENTER,
            label=label_2,
        )
        if icon_name_2:
            button_2.set_icon_name(icon_name=icon_name_2)

        button_2.connect(
            'clicked',
            self.on_button,
            callable_2,
            args,
            kwargs
        )
        self.add_suffix(widget=button_2)
    
    def on_button(
            self,
            button: Gtk.Button,
            callable: typing.Callable,
            args: tuple,
            kwargs: dict
    ) -> None:
        callable(*args, **kwargs)

class ButtonBarRow(Adw.ActionRow):
    def __init__(
            self,
            label: str,
            callable: typing.Callable,
            sensitive: bool = True,
            *args: typing.Any,
            **kwargs: typing.Any
    ) -> None:
        super().__init__(sensitive=sensitive)

        button = Gtk.Button(
            valign=Gtk.Align.CENTER,
            label=label,
            css_classes=['flat']
        )

        button.connect(
            'clicked',
            self.on_button,
            callable,
            args,
            kwargs
        )
        self.set_child(child=button)

    def on_button(
            self,
            button: Gtk.Button,
            callable: typing.Callable,
            args: tuple,
            kwargs: dict
    ) -> None:
        callable(*args, **kwargs)


class SwitchRow(Adw.ActionRow):
    def __init__(
            self,
            title: str,
            callable: typing.Callable,
            active: bool = False,
            sensitive: bool = True
    ) -> None:
        super().__init__(
            title=title,
            sensitive=sensitive
        )

        switch = Gtk.Switch(
            valign=Gtk.Align.CENTER,
            active=active
        )
        switch.connect(
            'notify::active',
            self.on_switch,
            callable
        )
        self.set_activatable_widget(widget=switch)
        self.add_suffix(widget=switch)

    def on_switch(
            self,
            switch: Gtk.Switch,
            g_param_spec: GObject.GParamSpec,
            callable: typing.Callable
    ) -> None:
        callable(switch.get_active())

class EntryRow(Adw.ActionRow):
    def __init__(
            self,
            callable: typing.Callable,
            title: str,
            subtitle: str = '',
            value: typing.Any = '',
            placeholder_text: str = '',
            signal: str = 'activate',
            sensitive: bool = True
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            sensitive=sensitive
        )
        if value == None:
            text = ''
        else:
            text = str(value)

        entry = Gtk.Entry(
            valign=Gtk.Align.CENTER,
            text=text,
            placeholder_text=placeholder_text
        )
        entry.connect(
            signal,
            self.on_entry,
            callable
        )
        self.add_suffix(widget=entry)
    
    def on_entry(
            self,
            entry: Gtk.Entry,
            callable: typing.Callable
    ) -> None:
        callable(entry.get_text())

class DoubleEntryRow(Adw.ActionRow):
    def __init__(
            self,
            callable_1: typing.Callable,
            callable_2: typing.Callable,
            title: str,
            subtitle: str = '',
            value_1: typing.Any = '',
            value_2: typing.Any = '',
            placeholder_text_1: str = '',
            placeholder_text_2: str = '',
            signal: str = 'activate',
            sensitive: bool = True
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            sensitive=sensitive
        )
        if value_1 == None:
            text_1 = ''
        else:
            text_1 = str(value_1)

        entry_1 = Gtk.Entry(
            valign=Gtk.Align.CENTER,
            text=text_1,
            placeholder_text=placeholder_text_1
        )
        entry_1.connect(
            signal,
            self.on_entry,
            callable_1
        )
        self.add_suffix(widget=entry_1)

        if value_2 == None:
            text_2 = ''
        else:
            text_2 = str(value_2)

        entry_2 = Gtk.Entry(
            valign=Gtk.Align.CENTER,
            text=text_2,
            placeholder_text=placeholder_text_2
        )
        entry_2.connect(
            signal,
            self.on_entry,
            callable_2
        )
        self.add_suffix(widget=entry_2)
    
    def on_entry(
            self,
            entry: Gtk.Entry,
            callable: typing.Callable
    ) -> None:
        callable(float(entry.get_text()))

class DropdownRow(Adw.ActionRow):
    def __init__(
            self,
            callable: typing.Callable,
            title: str,
            enum_class: typing.Type[enum.Enum],
            selected_value: typing.Optional[enum.Enum] = None,
            allow_none: bool = False,
            sensitive: bool = True
    ) -> None:
        super().__init__(
            title=title,
            sensitive=sensitive
        )
        self._callable = callable
        self._enum_class = enum_class
        self._allow_none = allow_none

        string_list = Gtk.StringList.new()
        if allow_none:
            string_list.append(string='None')

        for i in enum_class:
            string_list.append(
                string=i.name.replace('_', ' ')
            )
            
        if selected_value is None:
            selected_index = 0
        else:
            idx = list(enum_class).index(selected_value)
            selected_index = idx + (1 if allow_none else 0)

        dropdown = Gtk.DropDown(
            valign=Gtk.Align.CENTER,
            model=string_list,
            selected=selected_index
        )
        dropdown.connect(
            'notify::selected',
            self.on_dropdown
        )
        self.add_suffix(widget=dropdown)
    
    def on_dropdown(
            self,
            dropdown: Gtk.DropDown,
            gobject_param_spec_uint: GObject.ParamSpecUInt
    ) -> None:
        self._callable(
            list(self._enum_class)[
                dropdown.get_selected()-1 if self._allow_none
                else dropdown.get_selected()
            ]
        )
