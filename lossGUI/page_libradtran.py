import sys
import pathlib
import typing

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import widgets

sys.path.append(str(pathlib.Path.cwd()))
import loss.libRadtranPy.libradtranpy as libradtranpy

class LibRadtranGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            get_simulation_callback: typing.Callable,
            update_simulation_callback: typing.Callable
    ) -> None:
        super().__init__(title='libRadtran')
        show_input_row = widgets.ButtonRow(
            title='Show input file',
            label='Show',
            callable=self.show_input,
            get_simulation_cb=get_simulation_callback
        )
        self.add(child=show_input_row)

        apply_changes_row = widgets.ButtonRow(
            title='Apply changes',
            label='Apply',
            callable=self.apply_changes,
            update_simulation_cb=update_simulation_callback
        )
        self.add(child=apply_changes_row)

    def show_input(self, get_simulation_cb: typing.Callable) -> None:
        simulation: libradtranpy.Simulation = get_simulation_cb()

        text_view = Gtk.TextView(
            buffer=Gtk.TextBuffer(
                text=simulation.generate_uvspec_input()
            ),
            editable=False
        )
        margin = 6
        input_file_dialog = Adw.Dialog(
            child=text_view,
            content_height=600,
            content_width=400,
            margin_top=margin,
            margin_bottom=margin,
            margin_start=margin,
            margin_end=margin,
            can_close=True
        )
        input_file_dialog.present()

    def apply_changes(self, update_simulation_cb: typing.Callable) -> None:
        update_simulation_cb()

class AerosolGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            default: bool,
            season: libradtranpy.AerosolSeason | None,
            visibility: float | None,
            haze: libradtranpy.AerosolHaze | None,
            vulcan: libradtranpy.AerosolVulcan | None,
            species: libradtranpy.AerosolSpecies | None,
            species_library: libradtranpy.AerosolSpeciesLibrary | None
    ) -> None:
        super().__init__(title='Aerosol')
        self._default = default
        self._season = season
        self._visibility = visibility
        self._haze = haze
        self._vulcan = vulcan
        self._species = species
        self._species_library = species_library

        default_row = widgets.SwitchRow(
            title='Default aerosol',
            callable=self.set_default,
            active=self.get_default()
        )
        self.add(child=default_row)

        season_row = widgets.DropdownRow(
            callable=self.set_season,
            title='Season',
            enum_class=libradtranpy.AerosolSeason,
            selected_value=self.get_season(),
            allow_none=True,
        )
        self.add(child=season_row)

        visibility_row = widgets.EntryRow(
            callable=self.set_visibility,
            title='Visibility',
            value=self.get_visibility(),
            placeholder_text='km',
        )
        self.add(child=visibility_row)

        haze_row = widgets.DropdownRow(
            callable=self.set_haze,
            title='Haze',
            enum_class=libradtranpy.AerosolHaze,
            selected_value=self.get_haze(),
            allow_none=True,
        )
        self.add(child=haze_row)

        vulcan_row = widgets.DropdownRow(
            callable=self.set_vulcan,
            title='Vulcan',
            enum_class=libradtranpy.AerosolVulcan,
            selected_value=self.get_vulcan(),
            allow_none=True,
        )
        self.add(child=vulcan_row)

        species_row = widgets.DropdownRow(
            callable=self.set_species,
            title='Species',
            enum_class=libradtranpy.AerosolSpecies,
            selected_value=self.get_species(),
            allow_none=True,
        )
        self.add(child=species_row)

        species_library_row = widgets.DropdownRow(
            callable=self.set_species_library,
            title='Species library',
            enum_class=libradtranpy.AerosolSpeciesLibrary,
            selected_value=self.get_species_library(),
            allow_none=True,
        )
        self.add(child=species_library_row)

    def set_default(self, default: bool) -> None:
        self._default = default

    def get_default(self) -> bool:
        return self._default

    def set_season(self, season: libradtranpy.AerosolSeason | None) -> None:
        self._season = season
    
    def get_season(self) -> libradtranpy.AerosolSeason | None:
        return self._season

    def set_visibility(self, visibility: typing.Optional[float | str]) -> None:
        self._visibility = float(visibility) if visibility is not None else visibility
    
    def get_visibility(self) -> float | None:
        return self._visibility

    def set_haze(self, haze: libradtranpy.AerosolHaze | None) -> None:
        self._haze = haze
    
    def get_haze(self) -> libradtranpy.AerosolHaze | None:
        return self._haze

    def set_vulcan(self, vulcan: libradtranpy.AerosolVulcan | None) -> None:
        self._vulcan = vulcan
    
    def get_vulcan(self) -> libradtranpy.AerosolVulcan | None:
        return self._vulcan

    def set_species(self, species: libradtranpy.AerosolSpecies | None) -> None:
        self._species = species
    
    def get_species(self) -> libradtranpy.AerosolSpecies | None:
        return self._species

    def set_species_library(self, species_library: libradtranpy.AerosolSpeciesLibrary | None) -> None:
        self._species_library = species_library
    
    def get_species_library(self) -> libradtranpy.AerosolSpeciesLibrary | None:
        return self._species_library

    def aerosol_settings(self) -> libradtranpy.Aerosol:
        settings = libradtranpy.Aerosol(
            aerosol_default=self.get_default(),
            aerosol_season=self.get_season(),
            aerosol_visibility=self.get_visibility(),
            aerosol_haze=self.get_haze(),
            aerosol_vulcan=self.get_vulcan(),
            aerosol_species_file=self.get_species(),
            aerosol_species_library=self.get_species_library()
        )
        return settings

class GeneralAtmGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            absorption: bool,
            scattering: bool,
            zout_interpolate: bool,
            reverse_atmosphere: bool
    ) -> None:
        super().__init__(title='General Atmosphere')
        self._absorption = absorption
        self._scattering = scattering
        self._zout_interpolate = zout_interpolate
        self._reverse_atmosphere = reverse_atmosphere

        absorption_row = widgets.SwitchRow(
            title='Absorption',
            callable=self.set_absorption,
            active=self.get_absorption()
        )
        self.add(child=absorption_row)

        scattering_row = widgets.SwitchRow(
            title='Scattering',
            callable=self.set_scattering,
            active=self.get_scattering()
        )
        self.add(child=scattering_row)

        zout_interpolate_row = widgets.SwitchRow(
            title='Zout interpolate',
            callable=self.set_zout_interpolate,
            active=self.get_zout_interpolate()
        )
        self.add(child=zout_interpolate_row)

        reverse_atmosphere_row = widgets.SwitchRow(
            title='Reverse Atmosphere',
            callable=self.set_reverse_atmosphere,
            active=self.get_reverse_atmosphere()
        )
        self.add(child=reverse_atmosphere_row)
    
    def set_absorption(self, absorption: bool) -> None:
        self._absorption = absorption
    
    def get_absorption(self) -> bool:
        return self._absorption

    def set_scattering(self, scattering: bool) -> None:
        self._scattering = scattering
    
    def get_scattering(self) -> bool:
        return self._scattering

    def set_zout_interpolate(self, zout_interpolate: bool) -> None:
        self._zout_interpolate = zout_interpolate
    
    def get_zout_interpolate(self) -> bool:
        return self._zout_interpolate

    def set_reverse_atmosphere(self, reverse_atmosphere: bool) -> None:
        self._reverse_atmosphere = reverse_atmosphere
    
    def get_reverse_atmosphere(self) -> bool:
        return self._reverse_atmosphere
    
    def general_atm_settings(self) -> libradtranpy.GeneralAtm:
        settings = libradtranpy.GeneralAtm(
            no_absorption=not self._absorption,
            no_scattering=not self._scattering,
            zout_interpolate=self._zout_interpolate,
            reverse_atmosphere=self._reverse_atmosphere
        )
        return settings

class MolAtmGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            atmosphere: libradtranpy.Atmosphere
    ) -> None:
        super().__init__(title='Molecular Atmosphere')

        self._atmosphere = atmosphere

        source_row = widgets.DropdownRow(
            callable=self.set_atmosphere,
            title='Atmosphere',
            enum_class=libradtranpy.Atmosphere,
            selected_value=self.get_atmosphere()
        )
        self.add(child=source_row)

    def set_atmosphere(self, atmosphere: libradtranpy.Atmosphere) -> None:
        self._atmosphere = atmosphere
    
    def get_atmosphere(self) -> libradtranpy.Atmosphere:
        return self._atmosphere
    
    def mol_atm_settings(self) -> libradtranpy.MolAtm:
        settings = libradtranpy.MolAtm(
            atmosphere_file=self.get_atmosphere(),
            # mol_abs_param=sel,
            # zout_interpolate=self.zout_interpolate,
            # reverse_atmosphere=self.reverse_atmosphere
        )
        return settings

class GeometryGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            sza: float | None,
            phi0: float | None,
            phi: float | None,
            umu: float | None,
            day_of_year: float | None,
            latitude: str | None,
            longitude: str | None,
            time: str | None,
    ) -> None:
        super().__init__(title='Geometry')

        self._sza = sza
        self._phi0 = phi0
        self._phi = phi
        self._umu = umu
        self._day_of_year = day_of_year
        self._latitude = latitude
        self._longitude = longitude
        self._time = time

        sza_row = widgets.EntryRow(
            callable=self.set_sza,
            title='Solar zenith angle',
            subtitle='sza',
            value=self.get_sza(),
            placeholder_text='°',
            sensitive=False
        )
        self.add(child=sza_row)

        phi0_row = widgets.EntryRow(
            callable=self.set_phi0,
            title='Horizon angle of the sun',
            subtitle='phi0',
            value=self.get_phi0(),
            placeholder_text='°',
            sensitive=False
        )
        self.add(child=phi0_row)

        phi_row = widgets.EntryRow(
            callable=self.set_phi,
            title='Viewing azimuthal angle',
            subtitle='phi',
            value=self.get_phi(),
            placeholder_text='°',
            sensitive=False
        )
        self.add(child=phi_row)

        umu_row = widgets.EntryRow(
            callable=self.set_umu,
            title='Viewing zenith angle',
            subtitle='umu',
            value=self.get_umu(),
            placeholder_text='°',
            sensitive=False
        )
        self.add(child=umu_row)

        day_of_year_row = widgets.EntryRow(
            callable=self.set_day_of_year,
            title='Day of year',
            value=self.get_day_of_year(),
            sensitive=False
        )
        self.add(child=day_of_year_row)

        latitude_row = widgets.EntryRow(
            callable=self.set_latitude,
            title='Latitude',
            value=self.get_latitude(),
            sensitive=False
        )
        self.add(child=latitude_row)

        longitude_row = widgets.EntryRow(
            callable=self.set_longitude,
            title='Longitude',
            value=self.get_longitude(),
            sensitive=False
        )
        self.add(child=longitude_row)

        time_row = widgets.EntryRow(
            callable=self.set_time,
            title='Time',
            value=self.get_time(),
            sensitive=False
        )
        self.add(child=time_row)

    def set_sza(self, sza: typing.Optional[float | str]) -> None:
        self._sza = float(sza) if sza is not None else sza
    
    def get_sza(self) -> float | None:
        return self._sza

    def set_phi0(self, phi0: typing.Optional[float | str]) -> None:
        self._phi0 = float(phi0) if phi0 is not None else phi0
    
    def get_phi0(self) -> float | None:
        return self._phi0

    def set_phi(self, phi: typing.Optional[float | str]) -> None:
        self._phi = float(phi) if phi is not None else phi
    
    def get_phi(self) -> float | None:
        return self._phi

    def set_umu(self, umu: typing.Optional[float | str]) -> None:
        self._umu = float(umu) if umu is not None else umu

    def get_umu(self) -> float | None:
        return self._umu

    def set_day_of_year(self, day_of_year: typing.Optional[float | str]) -> None:
        self._day_of_year = float(day_of_year) if day_of_year is not None else day_of_year
    
    def get_day_of_year(self) -> float | None:
        return self._day_of_year

    def set_latitude(self, latitude: typing.Optional[str]) -> None:
        self._latitude = latitude

    def get_latitude(self) -> str | None:
        return self._latitude
    
    def set_longitude(self, longitude: typing.Optional[str]) -> None:
        self._longitude = longitude
    
    def get_longitude(self) -> str | None:
        return self._longitude

    def set_time(self, time: typing.Optional[str]) -> None:
        self._time = time
    
    def get_time(self) -> str | None:
        return self._time

    def geometry_settings(self) -> libradtranpy.Geometry:
        settings = libradtranpy.Geometry(
            sza=self.get_sza(),
            phi0=self.get_phi0(),
            phi=self.get_phi(),
            umu=self.get_umu(),
            day_of_year=self.get_day_of_year(),
            latitude=self.get_latitude(),
            longitude=self.get_longitude(),
            time=self.get_time()
        )
        return settings

class SolverGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            rte_solver: libradtranpy.RTESolver
    ) -> None:
        super().__init__(title='Solver')

        self._rte_solver = rte_solver

        solver_row = widgets.DropdownRow(
            callable=self.set_rte_solver,
            title='Solver',
            enum_class=libradtranpy.RTESolver,
            selected_value=self.get_rte_solver()
        )
        self.add(child=solver_row)

    def set_rte_solver(self, rte_solver: libradtranpy.RTESolver) -> None:
        self._rte_solver = rte_solver
    
    def get_rte_solver(self) -> libradtranpy.RTESolver:
        return self._rte_solver

    def solver_settings(self) -> libradtranpy.Solver:
        settings = libradtranpy.Solver(
            rte_solver=self.get_rte_solver()
        )
        return settings

class SpectralGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            wavelength_min: float,
            wavelength_max: float,
            source: libradtranpy.Source
    ) -> None:
        super().__init__(title='Spectral')

        self._wavelength_min = wavelength_min
        self._wavelength_max = wavelength_max
        self._source = source

        wavelength_row = widgets.DoubleEntryRow(
            title='Wavelength',
            callable_1=self.set_wavelength_min,
            callable_2=self.set_wavelength_max,
            value_1=self.get_wavelength_min(),
            value_2=self.get_wavelength_max(),
            placeholder_text_1='Min nm',
            placeholder_text_2='Max nm'
        )
        self.add(child=wavelength_row)

        source_row = widgets.DropdownRow(
            callable=self.set_source,
            title='Source',
            enum_class=libradtranpy.Source,
            selected_value=self.get_source()
        )
        self.add(child=source_row)

    def set_wavelength_min(self, wavelength: float | str) -> None:
        self._wavelength_min = float(wavelength)
    
    def get_wavelength_min(self) -> float:
        return self._wavelength_min

    def set_wavelength_max(self, wavelength: float | str) -> None:
        self._wavelength_max = float(wavelength)
    
    def get_wavelength_max(self) -> float:
        return self._wavelength_max

    def set_source(self, source: libradtranpy.Source) -> None:
        self._source = source
    
    def get_source(self) -> libradtranpy.Source:
        return self._source

    def spectral_settings(self) -> libradtranpy.Spectral:
        settings = libradtranpy.Spectral(
            wavelength=[
                int(self.get_wavelength_min()),
                int(self.get_wavelength_max())
            ] if self.get_wavelength_min() != self.get_wavelength_max() else [
                self.get_wavelength_min()
            ],
            source=self.get_source()
        )
        return settings

class SurfaceGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            altitude: float | None,
            albedo: float | None
    ) -> None:
        super().__init__(title='Surface')

        self._altitude = altitude
        self._albedo = albedo

        altitude_row = widgets.EntryRow(
            callable=self.set_altitude,
            title='Altitude',
            value=self.get_altitude(),
            placeholder_text='km'
        )
        self.add(child=altitude_row)

        albedo_row = widgets.EntryRow(
            callable=self.set_albedo,
            title='Albedo',
            value=self.get_albedo()
        )
        self.add(child=albedo_row)

    def set_altitude(self, altitude: typing.Optional[float | str]) -> None:
        self._altitude = float(altitude) if altitude is not None else altitude
    
    def get_altitude(self) -> float | None:
        return self._altitude

    def set_albedo(self, albedo: typing.Optional[float | str]) -> None:
        self._albedo = float(albedo) if albedo is not None else albedo
    
    def get_albedo(self) -> float | None:
        return self._albedo

    def surface_settings(self) -> libradtranpy.Surface:
        return libradtranpy.Surface(
            altitude=self.get_altitude(),
            albedo=self.get_albedo()
        )

class OutputGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            quiet: bool,
            verbose: bool,
            output_user: str | None,
            output_quantity: libradtranpy.OutputQuantity | None
    ) -> None:
        super().__init__(title='Output')

        self._quiet = quiet
        self._verbose = verbose
        self._output_user = output_user
        self._output_quantity = output_quantity

        quiet_row = widgets.SwitchRow(
            title='Quiet',
            callable=self.set_quiet,
            active=self.get_quiet()
        )
        self.add(child=quiet_row)

        verbose_row = widgets.SwitchRow(
            title='Verbose',
            callable=self.set_verbose,
            active=self.get_verbose()
        )
        self.add(child=verbose_row)

        output_user_row = widgets.EntryRow(
            callable=self.set_output_user,
            title='Output user',
            value=self.get_output_user(),
            sensitive=False
        )
        self.add(child=output_user_row)

        output_quantity_row = widgets.DropdownRow(
            callable=self.set_output_quantity,
            title='Output quantity',
            enum_class=libradtranpy.OutputQuantity,
            selected_value=self.get_output_quantity(),
            allow_none=True
        )
        self.add(child=output_quantity_row)

    def set_quiet(self, quiet: bool) -> None:
        self._quiet = quiet

    def get_quiet(self) -> bool:
        return self._quiet

    def set_verbose(self, verbose: bool) -> None:
        self._verbose = verbose

    def get_verbose(self) -> bool:
        return self._verbose

    def set_output_user(self, output_user: typing.Optional[str]) -> None:
        self._output_user = output_user

    def get_output_user(self) -> str | None:
        return self._output_user

    def set_output_quantity(self, output_quantity: typing.Optional[libradtranpy.OutputQuantity]) -> None:
        self._output_quantity = output_quantity

    def get_output_quantity(self) -> libradtranpy.OutputQuantity | None:
        return self._output_quantity

    def output_settings(self) -> libradtranpy.Output:
        return libradtranpy.Output(
            quiet=self.get_quiet(),
            verbose=self.get_verbose(),
            output_user=self.get_output_user(),
            output_quantity=self.get_output_quantity()
        )

class LibRadtranPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()
        libRadtran_group = LibRadtranGroup(
            get_simulation_callback=self.get_simulation,
            update_simulation_callback=self.update_simulation
        )
        self.add(group=libRadtran_group)

        self.aerosol_group = AerosolGroup(
            default=True,
            season=None,
            visibility=None,
            haze=None,
            vulcan=None,
            species=None,
            species_library=None
        )
        self.add(group=self.aerosol_group)

        self.general_atm_group = GeneralAtmGroup(
            absorption=True,
            scattering=True,
            zout_interpolate=False,
            reverse_atmosphere=False
        )
        self.add(group=self.general_atm_group)

        self.mol_atm_group = MolAtmGroup(
            atmosphere=libradtranpy.Atmosphere.USSTANDARD
        )
        self.add(group=self.mol_atm_group)

        self.geometry_group = GeometryGroup(
            sza=None,
            phi0=None,
            phi=None,
            umu=None,
            day_of_year=None,
            latitude=None,
            longitude=None,
            time=None
        )
        self.add(group=self.geometry_group)

        self.solver_group = SolverGroup(
            rte_solver=libradtranpy.RTESolver.DISORT
        )
        self.add(group=self.solver_group)

        self.spectral_group = SpectralGroup(
            wavelength_min=785,
            wavelength_max=785,
            source=libradtranpy.Source.SOLAR
        )
        self.add(group=self.spectral_group)

        self.surface_group = SurfaceGroup(
            altitude=None,
            albedo=None
        )
        self.add(group=self.surface_group)

        self.output_group = OutputGroup(
            quiet=True,
            verbose=False,
            output_user='lambda edir',
            output_quantity=libradtranpy.OutputQuantity.TRANSMITTANCE
        )
        self.add(group=self.output_group)

        self.update_simulation()

    def update_simulation(self) -> None:
        simulation = libradtranpy.Simulation(
            aerosol=self.aerosol_group.aerosol_settings(),
            general_atm=self.general_atm_group.general_atm_settings(),
            mol_atm=self.mol_atm_group.mol_atm_settings(),
            geometry=self.geometry_group.geometry_settings(),
            solver=self.solver_group.solver_settings(),
            spectral=self.spectral_group.spectral_settings(),
            surface=self.surface_group.surface_settings(),
            output=self.output_group.output_settings(),
        )
        self.set_simulation(simulation=simulation)   

    def set_simulation(self, simulation: libradtranpy.Simulation) -> None:
        self._simulation = simulation
    
    def get_simulation(self) -> libradtranpy.Simulation:
        return self._simulation