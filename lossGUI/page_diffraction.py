import sys
import pathlib
import typing

import numpy as np

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import widgets
import loss.diffraction as diffraction

class DiffractionGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            set_simulation_callback: typing.Callable,
            get_simulation_callback: typing.Callable
    ) -> None:
        super().__init__(title='Settings')
        simulation: diffraction.DiffractionSim = get_simulation_callback()

        self._sat_altitude = simulation.sat_altitude
        self._ogs_altitude = simulation.ogs_altitude
        self._wavelength = simulation.wavelength
        self._sat_telescope_diameter = simulation.sat_telescope_diameter
        self._divergence_FWHM = simulation.divergence_FWHM
        self._turbulence = simulation.turbulence
        self._ground_level_turbulence_strength = simulation.ground_level_turbulence_strength
        self._wind_speed = simulation.wind_speed

        self.simulation = diffraction.DiffractionSim(
            sat_altitude=self.get_sat_altitude(),
            ogs_altitude=self.get_ogs_altitude(),
            wavelength=self.get_wavelength(),
            sat_telescope_diameter=self.get_sat_telescope_diameter(),
            divergence_FWHM=self.get_divergence_FWHM(),
            turbulence=self.get_turbulence()
        )

        sat_altitude_row = widgets.EntryRow(
            callable=self.set_sat_altitude,
            title='Satellite altitude',
            value=self.get_sat_altitude(),
            placeholder_text='m',
            signal='changed'
        )
        self.add(child=sat_altitude_row)

        ogs_altitude_row = widgets.EntryRow(
            callable=self.set_ogs_altitude,
            title='OGS altitude',
            value=self.get_ogs_altitude(),
            placeholder_text='m',
            signal='changed'
        )
        self.add(child=ogs_altitude_row)

        wavelength_row = widgets.EntryRow(
            callable=self.set_wavelength,
            title='Wavelength',
            value=self.get_wavelength(),
            placeholder_text='m',
            signal='changed',
            sensitive=False
        )
        self.add(child=wavelength_row)

        divergence_FWHM_row = widgets.EntryRow(
            callable=self.set_divergence_FWHM,
            title='Divergence FWHM',
            value=self.get_divergence_FWHM(),
            signal='changed'
        )
        self.add(child=divergence_FWHM_row)

        sat_telescope_diameter_row = widgets.EntryRow(
            callable=self.set_sat_telescope_diameter,
            title='Satellite telescope diameter',
            placeholder_text='m',
            value=self.get_sat_telescope_diameter(),
            signal='changed'
        )
        self.add(child=sat_telescope_diameter_row)

        turbulence_row = widgets.SwitchRow(
            callable=self.set_turbulence,
            title='Turbulence',
            active=self.get_turbulence()
        )
        self.add(child=turbulence_row)

        ground_level_turbulence_strength_row = widgets.EntryRow(
            callable=self.set_ground_level_turbulence_strength,
            title='Ground level turbulence strength',
            subtitle='A',
            placeholder_text='m^(-2/3)',
            value=self.get_ground_level_turbulence_strength(),
            signal='changed',
            sensitive=self.get_turbulence()
        )
        self.add(child=ground_level_turbulence_strength_row)

        wind_speed_row = widgets.EntryRow(
            callable=self.set_wind_speed,
            title='Wind speed',
            subtitle='v',
            placeholder_text='m/s',
            value=str(self.get_wind_speed()),
            signal='changed',
            sensitive=self.get_turbulence()
        )
        self.add(child=wind_speed_row)

        apply_changes_row = widgets.ButtonRow(
            title='Apply changes',
            label='Apply',
            callable=self.set_simulation,
            set_simulation_cb=set_simulation_callback
        )
        self.add(child=apply_changes_row)

        self._disable_when_no_turbulence: typing.List[Adw.ActionRow] = [
            ground_level_turbulence_strength_row,
            wind_speed_row
        ]
    
    def set_simulation(self, set_simulation_cb: typing.Callable) -> None:
        set_simulation_cb(
            simulation=diffraction.DiffractionSim(
                sat_altitude=self.get_sat_altitude(),
                ogs_altitude=self.get_ogs_altitude(),
                wavelength=self.get_wavelength(),
                divergence_FWHM=self.get_divergence_FWHM(),
                sat_telescope_diameter=self.get_sat_telescope_diameter(),
                turbulence=self.get_turbulence(),
                ground_level_turbulence_strength=self.get_ground_level_turbulence_strength(),
                wind_speed=self.get_wind_speed()
            )
        )

    def set_sat_altitude(self, altitude: float | str) -> None:
        self._sat_altitude = float(altitude)

    def get_sat_altitude(self) -> float:
        return self._sat_altitude

    def set_ogs_coords(self, coords: np.ndarray) -> None:
        self.ogs_coords = coords
    
    def get_ogs_coords(self) -> np.ndarray:
        return self.ogs_coords

    def set_ogs_altitude(self, altitude: float | str) -> None:
        self._ogs_altitude = float(altitude)
    
    def get_ogs_altitude(self) -> float:
        return self._ogs_altitude
    
    def set_wavelength(self, wavelength: float | str) -> None:
        self._wavelength = float(wavelength)
    
    def get_wavelength(self) -> float:
        return self._wavelength

    def set_divergence_FWHM(self, divergence: float | str) -> None:
        self._divergence_FWHM = float(divergence)
    
    def get_divergence_FWHM(self) -> float:
        return self._divergence_FWHM

    def set_sat_telescope_diameter(self, diameter: float | str) -> None:
        self._sat_telescope_diameter = float(diameter)
    
    def get_sat_telescope_diameter(self) -> float:
        return self._sat_telescope_diameter

    def set_turbulence(self, turbulence: bool) -> None:
        self._turbulence = turbulence
        for row in self._disable_when_no_turbulence:
            row.set_sensitive(sensitive=self.get_turbulence())
    
    def get_turbulence(self) -> bool:
        return self._turbulence
    
    def set_ground_level_turbulence_strength(self, A: float | str) -> None:
        self._ground_level_turbulence_strength = float(A)
    
    def get_ground_level_turbulence_strength(self) -> float:
        return self._ground_level_turbulence_strength
    
    def set_wind_speed(self, wind_speed: float | str) -> None:
        self._wind_speed = float(wind_speed)
    
    def get_wind_speed(self) -> float:
        return self._wind_speed

class DiffractionPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()

        self.simulation = diffraction.DiffractionSim(
            sat_altitude = 550e3,
            ogs_altitude = 0,
            wavelength = 785e-9,
            sat_telescope_diameter = 0.25,
            divergence_FWHM = 25.7e-6,
            turbulence = False,
        )

        diffraction_group = DiffractionGroup(
            set_simulation_callback=self.set_simulation,
            get_simulation_callback=self.get_simulation
        )
        self.add(group=diffraction_group)

    def set_simulation(self, simulation: diffraction.DiffractionSim) -> None:
        self.simulation = simulation
    
    def get_simulation(self) -> diffraction.DiffractionSim:
        return self.simulation