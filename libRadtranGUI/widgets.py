import typing
import enum

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GObject

class ButtonRow(Adw.ActionRow):
    def __init__(
            self,
            title: str,
            label: str,
            callable: typing.Callable,
            sensitive: bool = True,
            *args: typing.Any,
            **kwargs: typing.Any
    ) -> None:
        super().__init__(
            title=title,
            sensitive=sensitive
        )

        button = Gtk.Button(
            valign=Gtk.Align.CENTER,
            label=label
        )
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
            text: str = '',
            placeholder_text: str = '',
            sensitive: bool = True
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            sensitive=sensitive
        )

        entry = Gtk.Entry(
            valign=Gtk.Align.CENTER,
            text=text,
            placeholder_text=placeholder_text
        )
        entry.connect(
            'activate',
            self.on_entry,
            callable
        )
        self.add_suffix(widget=entry)
    
    def on_entry(
            self,
            entry: Gtk.Entry,
            callable: typing.Callable
    ) -> None:
        callable(float(entry.get_text()))

class DoubleEntryRow(Adw.ActionRow):
    def __init__(
            self,
            callable_1: typing.Callable,
            callable_2: typing.Callable,
            title: str,
            subtitle: str = '',
            text_1: str = '',
            text_2: str = '',
            placeholder_text_1: str = '',
            placeholder_text_2: str = '',
            sensitive: bool = True
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            sensitive=sensitive
        )

        entry_1 = Gtk.Entry(
            valign=Gtk.Align.CENTER,
            text=text_1,
            placeholder_text=placeholder_text_1
        )
        entry_1.connect(
            'activate',
            self.on_entry_1,
            callable_1
        )
        self.add_suffix(widget=entry_1)

        entry_2 = Gtk.Entry(
            valign=Gtk.Align.CENTER,
            text=text_2,
            placeholder_text=placeholder_text_2
        )
        entry_2.connect(
            'activate',
            self.on_entry_2,
            callable_2
        )
        self.add_suffix(widget=entry_2)
    
    def on_entry_1(
            self,
            entry: Gtk.Entry,
            callable: typing.Callable
    ) -> None:
        callable(float(entry.get_text()))

    def on_entry_2(
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
            string_list: Gtk.StringList,
            selected: int = 0,
            sensitive: bool = True
    ) -> None:
        super().__init__(
            title=title,
            sensitive=sensitive
        )

        dropdown = Gtk.DropDown(
            valign=Gtk.Align.CENTER,
            model=string_list,
            selected=selected
        )
        dropdown.connect(
            'notify::selected',
            self.on_dropdown,
            callable,
        )
        self.add_suffix(widget=dropdown)
    
    def on_dropdown(
            self,
            dropdown: Gtk.DropDown,
            gobject_param_spec_uint: GObject.ParamSpecUInt,
            callable: typing.Callable,
    ) -> None:
        callable(index=dropdown.get_selected())