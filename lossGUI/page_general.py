import sys
import pathlib
import typing

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

import matplotlib.backends.backend_gtk4agg
import matplotlib.figure
import matplotlib.cm
import matplotlib.image
import scipy.ndimage
import numpy as np

import widgets

class GeneralGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            wavelength: float,
            min_elevation: float
    ) -> None:
        super().__init__(title='Settings')

        self._wavelength = wavelength
        self._min_elevation = min_elevation

        wavelength_row = widgets.EntryRow(
            callable=self.set_wavelength,
            title='Wavelength',
            value=self.get_wavelength(),
            placeholder_text='m',
            signal='changed',
            sensitive=False
        )
        self.add(child=wavelength_row)

        min_elevation_row = widgets.EntryRow(
            callable=self.set_min_elevation,
            title='Minimum elevation',
            value=self.get_min_elevation(),
            placeholder_text='°',
            signal='changed',
            sensitive=False
        )
        self.add(child=min_elevation_row)
    
    def set_wavelength(self, wavelength: float | str) -> None:
        self._wavelength = float(wavelength)
    
    def get_wavelength(self) -> float:
        return self._wavelength

    def set_min_elevation(self, min_elevation: float | str) -> None:
        self._min_elevation = float(min_elevation)
    
    def get_min_elevation(self) -> float:
        return self._min_elevation
    
class OrbitGroup(Adw.PreferencesGroup):
    def __init__(self) -> None:
        super().__init__(title='Orbit')
        self._orbit_altitude = 550
        self._orbit_inclination = 97.6
        self._orbit_eccentricity = 0
        self._orbit_raan = 167.4

        mu = 398600
        self._earth_radius = 6371
        r = self._earth_radius + self._orbit_altitude
        self._orbit_period = 2*np.pi * np.sqrt(r**3 / mu)

        self._timescale = 100

        self._earth_angle = 0
        self._earth_rotation_speed = 0.5
        
        self._satellite_angle = 0
        self._orbit_theta = np.linspace(0, 2*np.pi, 100)

        self.figure = matplotlib.figure.Figure()
        self.figure.tight_layout()

        self.axes = self.figure.add_subplot(111, projection='3d')
        self.axes.axis('off')
        self.axes.set_box_aspect([1, 1, 1])
        size = 1
        self.axes.set_xlim([-size, size])
        self.axes.set_ylim([-size, size])
        self.axes.set_zlim([-size, size])
        
        self.canvas = matplotlib.backends.backend_gtk4agg.FigureCanvasGTK4Agg(
            figure=self.figure
        )
        self.canvas.set_size_request(
            width=0,
            height=500
        )

        self.draw_earth(image_file='lossGUI/earth_texture.jpg')

        self._orbit_line, = self.axes.plot3D(
            [], [], [],
            color='black',
            linewidth=1.5
        )

        self._satellite_point, = self.axes.plot3D(
            [], [], [],
            marker='o',
            color=widgets.Colours.TEAL.value,
            markersize=6, zorder=20
        )

        self.update_orbit()

        plot_row = Adw.PreferencesRow()
        self.add(child=plot_row)
        margin = 2
        plot_box = Gtk.Box(
            margin_top=margin,
            margin_bottom=margin,
            margin_start=margin,
            margin_end=margin
        )
        plot_box.append(child=self.canvas)
        plot_row.set_child(child=plot_box)

        orbit_altitude_row = widgets.EntryRow(
            title='Orbit altitude',
            callable=self.set_orbit_altitude,
            value=self.get_orbit_altitude()
        )
        self.add(child=orbit_altitude_row)

        orbit_inclination_row = widgets.EntryRow(
            title='Orbit inclination',
            callable=self.set_orbit_inclination,
            value=self.get_orbit_inclination()
        )
        self.add(child=orbit_inclination_row)

        orbit_eccentricity_row = widgets.EntryRow(
            title='Orbit eccentricity',
            callable=self.set_orbit_eccentricity,
            value=self.get_orbit_eccentricity()
        )
        self.add(child=orbit_eccentricity_row)

        orbit_raan_row = widgets.EntryRow(
            title='Orbit RAAN',
            callable=self.set_orbit_raan,
            value=self.get_orbit_raan()
        )
        self.add(child=orbit_raan_row)

        orbit_period_row = widgets.EntryRow(
            title='Orbit period',
            callable=self.set_orbit_period,
            value=self.get_orbit_period(),
            sensitive=False
        )
        self.add(child=orbit_period_row)

        timescale_row = widgets.EntryRow(
            title='Timescale',
            callable=self.set_timescale,
            value=self.get_timescale()
        )
        self.add(child=timescale_row)

        self.start_animated_plot()
    
    def draw_earth(
        self,
        image_file: str,
        mesh_resolution: int = 25,
        texture_scale: float = 0.5
    ) -> None:
        texture = matplotlib.image.imread(image_file)
        texture_scaled = scipy.ndimage.zoom(
            texture,
            (texture_scale, texture_scale, 1)
        )

        theta = np.linspace(0, np.pi, mesh_resolution)
        phi = np.linspace(0, 2*np.pi, mesh_resolution*2)
        theta, phi = np.meshgrid(theta, phi)

        R = 1
        self._earth_x = R * np.sin(theta) * np.cos(phi)
        self._earth_y = R * np.sin(theta) * np.sin(phi)
        self._earth_z = R * np.cos(theta)

        i = (theta / np.pi * (texture_scaled.shape[0]-1)).astype(int)
        j = (phi / (2*np.pi) * (texture_scaled.shape[1]-1)).astype(int)
        self._earth_facecolors = texture_scaled[i, j] / 255.0

        self._earth_wireframe = self.axes.plot_wireframe(
            self._earth_x, self._earth_y, self._earth_z,
            rstride=2,
            cstride=2,
            color='k',
            linewidth=0.5,
            alpha=0.5
        )

        self._earth_surface = self.axes.plot_surface(
            self._earth_x, self._earth_y, self._earth_z,
            facecolors=self._earth_facecolors,
            rstride=1,
            cstride=1,
            antialiased=False
        )

    def rotate_earth(self, angle: float) -> None:
        angle_rad = np.radians(angle)

        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        x0, y0, z0 = self._earth_x, self._earth_y, self._earth_z

        x_rot = cos_a * x0 - sin_a * y0
        y_rot = sin_a * x0 + cos_a * y0
        z_rot = z0

        self._earth_surface.remove()
        self._earth_wireframe.remove()

        self._earth_wireframe = self.axes.plot_wireframe(
            x_rot, y_rot, z_rot,
            rstride=2,
            cstride=2,
            color='k',
            linewidth=0.5,
            alpha=0.5
        )

        self._earth_surface = self.axes.plot_surface(
            x_rot, y_rot, z_rot,
            facecolors=self._earth_facecolors,
            rstride=1,
            cstride=1,
            antialiased=False
        )

        self.canvas.draw_idle()

    def start_animated_plot(self) -> None:
        earth_deg_per_sec = 360/(24*3600)

        sat_deg_per_sec = 360 / self._orbit_period

        def update() -> bool:
            self._earth_angle += earth_deg_per_sec * self._timescale * 0.05
            self._satellite_angle += np.radians(sat_deg_per_sec * self._timescale * 0.05)
            self.rotate_earth(self._earth_angle)
            self.update_satellite()
            return True

        GLib.timeout_add(50, update)

    def update_orbit(self) -> None:
        orbit_radius = (self._earth_radius + self._orbit_altitude) / self._earth_radius
        self._orbit_inclination_rad = np.radians(self._orbit_inclination)

        self._orbit_x = orbit_radius * np.cos(self._orbit_theta)
        self._orbit_y = orbit_radius * np.sin(self._orbit_theta) * np.cos(self._orbit_inclination_rad)
        self._orbit_z = orbit_radius * np.sin(self._orbit_theta) * np.sin(self._orbit_inclination_rad)

        self._orbit_line.set_data(
            self._orbit_x,
            self._orbit_y
        )
        self._orbit_line.set_3d_properties(self._orbit_z)
        self._orbit_line.set_zorder(10)
        self.canvas.draw_idle()

    def update_satellite(self) -> None:
        orbit_radius = (self._earth_radius + self._orbit_altitude) / self._earth_radius
        inclination_rad = np.radians(self._orbit_inclination)

        x = orbit_radius * np.cos(self._satellite_angle)
        y = orbit_radius * np.sin(self._satellite_angle) * np.cos(inclination_rad)
        z = orbit_radius * np.sin(self._satellite_angle) * np.sin(inclination_rad)

        self._satellite_point.set_data([x], [y])
        self._satellite_point.set_3d_properties([z])


    def set_orbit_altitude(self, altitude: float | str) -> None:
        self._orbit_altitude = float(altitude)
        self.update_orbit()
    
    def get_orbit_altitude(self) -> float:
        return self._orbit_altitude
    
    def set_orbit_inclination(self, inclination: float | str) -> None:
        self._orbit_inclination = float(inclination)
        self.update_orbit()
    
    def get_orbit_inclination(self) -> float:
        return self._orbit_inclination
    
    def set_orbit_eccentricity(self, eccentricity: float | str) -> None:
        self._orbit_eccentricity = float(eccentricity)
        self.update_orbit()
    
    def get_orbit_eccentricity(self) -> float:
        return self._orbit_eccentricity
    
    def set_orbit_raan(self, raan: float | str) -> None:
        self._orbit_raan = float(raan)
        self.update_orbit()
    
    def get_orbit_raan(self) -> float:
        return self._orbit_raan
    
    def set_orbit_period(self, period: float | str) -> None:
        self._orbit_period = float(period)
        self.update_orbit()
    
    def get_orbit_period(self) -> float:
        return self._orbit_period
    
    def set_timescale(self, timescale: float | str) -> None:
        self._timescale = float(timescale)
    
    def get_timescale(self) -> float:
        return self._timescale

class GeneralPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()

        diffraction_group = GeneralGroup(
            wavelength=785e-9,
            min_elevation=30.0
        )
        self.add(group=diffraction_group)

        orbit_group = OrbitGroup()
        self.add(group=orbit_group)