import sys
import pathlib
import typing

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import widgets

sys.path.append(str(pathlib.Path.cwd()))
import atm_modelling.libRadtranPy.libradtranpy as libradtranpy

class AerosolPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()
        settings = Adw.PreferencesGroup(title='Settings')
        self.add(group=settings)

        self.default = True
        self.season = libradtranpy.AerosolSeason.SPRING_SUMMER
        self.visibility = 0.0
        self.haze = libradtranpy.AerosolHaze.RURAL
        self.vulcan = libradtranpy.AerosolVulcan.BACKGROUND_AEROSOLS
        self.species = libradtranpy.AerosolSpecies.CONTINENTAL_CLEAN
        self.species_library = libradtranpy.AerosolSpeciesLibrary.OPAC

        default_row = widgets.SwitchRow(
            title='Default aerosol',
            callable=self.set_default,
            active=self.get_default()
        )
        settings.add(child=default_row)

        season_string_list = Gtk.StringList(
            strings=[i.name for i in libradtranpy.AerosolSeason]
        )
        season_row = widgets.DropdownRow(
            callable=self.get_season,
            title='Season',
            string_list=season_string_list,
            selected=list(libradtranpy.AerosolSeason).index(self.get_season()),
            sensitive=not self.get_default()
        )
        settings.add(child=season_row)

        visibility_row = widgets.EntryRow(
            callable=self.get_visibility,
            title='Visibility',
            text=str(self.get_visibility()),
            placeholder_text='km',
            sensitive=not self.get_default()
        )
        settings.add(child=visibility_row)

        haze_string_list = Gtk.StringList(
            strings=[i.name for i in libradtranpy.AerosolHaze]
        )
        haze_row = widgets.DropdownRow(
            callable=self.get_haze,
            title='Haze',
            string_list=haze_string_list,
            sensitive=not self.get_default()
        )
        settings.add(child=haze_row)

        vulcan_string_list = Gtk.StringList(
            strings=[i.name for i in libradtranpy.AerosolVulcan]
        )
        vulcan_row = widgets.DropdownRow(
            callable=self.get_vulcan,
            title='Vulcan',
            string_list=vulcan_string_list,
            selected=list(libradtranpy.AerosolVulcan).index(self.get_vulcan()),
            sensitive=not self.get_default()
        )
        settings.add(child=vulcan_row)

        species_string_list = Gtk.StringList(
            strings=[i.name for i in libradtranpy.AerosolSpecies]
        )
        species_row = widgets.DropdownRow(
            callable=self.get_species,
            title='Species',
            string_list=species_string_list,
            selected=list(libradtranpy.AerosolSpecies).index(self.get_species()),
            sensitive=not self.get_default()
        )
        settings.add(child=species_row)

        species_library_string_list = Gtk.StringList(
            strings=[i.name for i in libradtranpy.AerosolSpeciesLibrary]
        )
        species_library_row = widgets.DropdownRow(
            callable=self.get_species_library,
            title='Species library',
            string_list=species_library_string_list,
            selected=list(libradtranpy.AerosolSpeciesLibrary).index(self.get_species_library()),
            sensitive=not self.get_default()
        )
        settings.add(child=species_library_row)

        self._disable_when_default: typing.List[Adw.ActionRow] = [
            season_row,
            visibility_row,
            haze_row,
            vulcan_row,
            species_row,
            species_library_row
        ]

    def set_default(self, default: bool) -> None:
        self.default = default
        for row in self._disable_when_default:
            row.set_sensitive(sensitive=not self.default)

    def get_default(self) -> bool:
        return self.default

    def set_season(self, season: libradtranpy.AerosolSeason) -> None:
        self.season = season
    
    def get_season(self) -> libradtranpy.AerosolSeason:
        return self.season

    def set_visibility(self, visibility: float) -> None:
        self.visibility = visibility
    
    def get_visibility(self) -> float:
        return self.visibility

    def set_haze(self, haze: libradtranpy.AerosolHaze) -> None:
        self.haze = haze
    
    def get_haze(self) -> libradtranpy.AerosolHaze:
        return self.haze

    def set_vulcan(self, vulcan: libradtranpy.AerosolVulcan) -> None:
        self.vulcan = vulcan
    
    def get_vulcan(self) -> libradtranpy.AerosolVulcan:
        return self.vulcan

    def set_species(self, species: libradtranpy.AerosolSpecies) -> None:
        self.species = species
    
    def get_species(self) -> libradtranpy.AerosolSpecies:
        return self.species

    def set_species_library(self, species_library: libradtranpy.AerosolSpeciesLibrary) -> None:
        self.species_library = species_library
    
    def get_species_library(self) -> libradtranpy.AerosolSpeciesLibrary:
        return self.species_library

    def aerosol_settings(self) -> libradtranpy.Aerosol:
        if self.get_default():
            settings = libradtranpy.Aerosol(
                aerosol_default=self.get_default()
            )
        else:
            settings = libradtranpy.Aerosol(
                aerosol_season=self.get_season(),
                aerosol_visibility=libradtranpy.km(self.get_visibility()),
                aerosol_haze=self.get_haze(),
                aerosol_vulcan=self.get_vulcan(),
                aerosol_species_file=self.get_species(),
                aerosol_species_library=self.get_species_library()
            )
        return settings