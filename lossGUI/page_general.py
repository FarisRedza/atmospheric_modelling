import sys
import pathlib
import typing
import time
import dataclasses

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

import matplotlib.backends.backend_gtk4agg
import matplotlib.figure
import matplotlib.image
import matplotlib.lines
import mpl_toolkits.mplot3d.art3d
import numpy as np

import widgets

EARTH_RADIUS = 6371

@dataclasses.dataclass
class Satellite:
    name: str
    altitude: float
    inclination: float
    eccentricity: float
    raan: float
    period: float
    _angle: typing.Optional[float] = None
    _theta: typing.Optional[np.ndarray] = None
    _orbit: typing.Optional[matplotlib.lines.Line2D] = None
    _point: typing.Optional[matplotlib.lines.Line2D] = None

@dataclasses.dataclass
class GroundStation:
    name: str
    latitude: float
    longitude: float
    min_elevation: typing.Optional[float]
    _vec: typing.Optional[np.ndarray] = None
    _point: typing.Optional[matplotlib.lines.Line2D] = None

@dataclasses.dataclass
class FOVCircle:
    name: str
    ground_station: GroundStation
    satellite: Satellite
    _circle_points: np.ndarray
    _circle_line: matplotlib.lines.Line2D

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
    def __init__(
            self,
            get_ground_stations_callback: typing.Callable,
            get_satellites_callback: typing.Callable
    ) -> None:
        super().__init__(title='Orbit')
        self.get_ground_stations = get_ground_stations_callback
        self.get_satellites = get_satellites_callback

        self.ground_stations: list[GroundStation] = self.get_ground_stations()
        self.satellites: list[Satellite] = self.get_satellites()

        self._timescale = 10

        self.fov_circles: list[FOVCircle] = []

        self._earth_angle = 0

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

        for gs in self.get_ground_stations():
            self.add_ground_station_to_plot(
                ground_station=gs
            )
        for sat in self.get_satellites():
            self.add_satellite_to_plot(
                satellite=sat
            )

        self.add_fov_circle(
            ground_station=self.get_ground_stations()[0],
            satellite=self.satellites[0]
        )

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

        ground_station_coords_row = widgets.DoubleEntryRow(
            title='Ground station coordinates',
            callable_1=self.set_gs_latitude,
            value_1=self.get_gs_latitude(),
            callable_2=self.set_gs_longitude,
            value_2=self.get_gs_longitude()
        )
        self.add(child=ground_station_coords_row)

        self._last_update = time.time()
        self.start_animated_plot()
    
    def draw_earth(
        self,
        image_file: str,
        mesh_resolution: int = 30
    ) -> None:
        texture = matplotlib.image.imread(image_file)

        theta = np.linspace(0, np.pi, mesh_resolution)
        phi = np.linspace(0, 2*np.pi, mesh_resolution * 2)
        theta, phi = np.meshgrid(theta, phi)

        R = 1.0
        x = R * np.sin(theta) * np.cos(phi)
        y = R * np.sin(theta) * np.sin(phi)
        z = R * np.cos(theta)

        i = (theta / np.pi * (texture.shape[0] - 1)).astype(int)
        j = (((phi + np.pi) % (2*np.pi)) / (2*np.pi) * (texture.shape[1]-1)).astype(int)
        texture_rgb = texture[i, j] / 255.0

        self._earth_verts_flat = np.column_stack([x.ravel(), y.ravel(), z.ravel()])
        self._texture_flat = texture_rgb.reshape(-1, 3)

        n_theta, n_phi = x.shape
        faces = []
        facecolors = []
        for a in range(n_theta - 1):
            for b in range(n_phi - 1):
                idx0 = a * n_phi + b
                idx1 = idx0 + 1
                idx2 = idx0 + n_phi
                idx3 = idx2 + 1
                faces.append([idx0, idx1, idx3, idx2])
                facecolors.append(self._texture_flat[idx0])
        self._faces_idx = np.array(faces)
        self._facecolors = np.array(facecolors)

        faces_init = [self._earth_verts_flat[face] for face in self._faces_idx]
        self._earth_poly = mpl_toolkits.mplot3d.art3d.Poly3DCollection(
            faces_init,
            facecolors=self._facecolors,
            linewidths=0,
            antialiased=False
        )
        self.axes.add_collection3d(self._earth_poly)

    def rotate_earth(self, angle: float) -> None:
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        self._R = np.array([
            [cos_a, -sin_a, 0],
            [sin_a,  cos_a, 0],
            [0,      0,     1]
        ])

        rotated_flat = self._earth_verts_flat @ self._R.T

        faces_rotated = [rotated_flat[face] for face in self._faces_idx]
        self._earth_poly.set_verts(faces_rotated)

    def add_ground_station_to_plot(
            self,
            ground_station: GroundStation
    ) -> None:
        lat = np.radians(ground_station.latitude)
        lon = np.radians(ground_station.longitude)

        x = np.cos(lat) * np.cos(lon)
        y = np.cos(lat) * np.sin(lon)
        z = np.sin(lat)

        ground_station._vec = np.array([x,y,z])
        ground_station._point, = self.axes.plot3D(
            [x], [y], [z],
            label=ground_station.name,
            marker='o',
            linestyle='',
            color=widgets.Colours.ORANGE.value,
            markersize=4,
            zorder=10
        )
        # self.axes.legend(frameon=False)

    def add_satellite_to_plot(
            self,
            satellite: Satellite
    ) -> None:
        satellite._theta = np.linspace(0, 2*np.pi, 100)

        orbit_radius = (EARTH_RADIUS + satellite.altitude) / EARTH_RADIUS
        orbit_inclination_rad = np.radians(satellite.inclination)

        orbit_x = orbit_radius * np.cos(satellite._theta)
        orbit_y = orbit_radius * np.sin(satellite._theta) * np.cos(orbit_inclination_rad)
        orbit_z = orbit_radius * np.sin(satellite._theta) * np.sin(orbit_inclination_rad)

        satellite._orbit, = self.axes.plot3D(
            [orbit_x], [orbit_y], [orbit_z],
            color='black',
            linewidth=1.5,
            zorder=10
        )
        
        satellite._angle = 0
        angle_rad = np.radians(satellite._angle)
        sat_x = orbit_radius * np.cos(angle_rad)
        sat_y = orbit_radius * np.sin(angle_rad) * np.cos(orbit_inclination_rad)
        sat_z = orbit_radius * np.sin(angle_rad) * np.sin(orbit_inclination_rad)

        satellite._point, = self.axes.plot3D(
            [sat_x], [sat_y], [sat_z],
            label=satellite.name,
            marker='D',
            linestyle='',
            color=widgets.Colours.TEAL.value,
            markersize=4,
            zorder=20
        )

    def add_fov_circle(
            self,
            ground_station: GroundStation,
            satellite: Satellite
    ) -> None:
        if ground_station._vec is None or ground_station.min_elevation is None:
            raise Exception

        gs_vec = ground_station._vec / np.linalg.norm(ground_station._vec)
        cone_angle = np.radians(90-ground_station.min_elevation)
        orbit_radius = (EARTH_RADIUS + satellite.altitude) / EARTH_RADIUS

        circle_centre = gs_vec * orbit_radius * np.cos(cone_angle)
        circle_radius = orbit_radius * np.sin(cone_angle)

        tmp = np.array([0,0,1]) if abs(gs_vec[2]) < 0.9 else np.array([1,0,0])
        u = np.cross(gs_vec, tmp); u /= np.linalg.norm(u)
        v = np.cross(gs_vec, u)

        theta = np.linspace(0, 2*np.pi, 200)
        circle_points = (
            circle_centre[:,None] + circle_radius*(u[:,None]*np.cos(theta) + v[:,None]*np.sin(theta))
        ).T

        x, y, z = circle_points[:,0], circle_points[:,1], circle_points[:,2]

        circle_line, = self.axes.plot3D(
            x,
            y,
            z,
            color=widgets.Colours.ORANGE.value,
            linewidth=1.0,
            zorder=10
        )
        
        fov_circle = FOVCircle(
            name=f'fov_{len(self.fov_circles)+1}',
            ground_station=ground_station,
            satellite=satellite,
            _circle_points=circle_points,
            _circle_line=circle_line
        )
        self.fov_circles.append(fov_circle)

    def update_ground_stations(self) -> None:
        if not hasattr(self, 'ground_stations'):
            return

        for gs in self.ground_stations:
            lat = np.radians(gs.latitude)
            lon = np.radians(gs.longitude)

            x = np.cos(lat) * np.cos(lon)
            y = np.cos(lat) * np.sin(lon)
            z = np.sin(lat)

            gs._vec = np.array([x,y,z])

            rotated_point = np.dot(gs._vec, self._R.T)
            if gs._point is None:
                raise Exception

            gs._point.set_data([rotated_point[0]], [rotated_point[1]])
            gs._point.set_3d_properties([rotated_point[2]])

    def update_fov_circles(self) -> None:
        if not hasattr(self, 'fov_circles'):
            return
        
        for fc in self.fov_circles:
            if fc.ground_station._vec is None or fc.ground_station.min_elevation is None:
                raise Exception

            gs_vec = fc.ground_station._vec / np.linalg.norm(fc.ground_station._vec)
            cone_angle = np.radians(90-fc.ground_station.min_elevation)
            orbit_radius = (EARTH_RADIUS + fc.satellite.altitude) / EARTH_RADIUS

            circle_centre = gs_vec * orbit_radius * np.cos(cone_angle)
            circle_radius = orbit_radius * np.sin(cone_angle)

            tmp = np.array([0,0,1]) if abs(gs_vec[2]) < 0.9 else np.array([1,0,0])
            u = np.cross(gs_vec, tmp); u /= np.linalg.norm(u)
            v = np.cross(gs_vec, u)

            theta = np.linspace(0, 2*np.pi, 200)
            circle_points = (
                circle_centre[:,None] + circle_radius*(u[:,None]*np.cos(theta) + v[:,None]*np.sin(theta))
            ).T

            rotated_circle = np.dot(circle_points, self._R.T)
            fc._circle_line.set_data(rotated_circle[:,0], rotated_circle[:,1])
            fc._circle_line.set_3d_properties(rotated_circle[:,2])

    def update_satellites(self) -> None:
        if not hasattr(self, 'satellites'):
            return

        for sat in self.satellites:
            if sat._angle is None or sat._theta is None or sat._point is None or sat._orbit is None:
                raise Exception

            angle_rad = np.radians(sat._angle)
            
            orbit_radius = (EARTH_RADIUS + sat.altitude) / EARTH_RADIUS
            orbit_inclination_rad = np.radians(sat.inclination)

            orbit_x = orbit_radius * np.cos(sat._theta)
            orbit_y = orbit_radius * np.sin(sat._theta) * np.cos(orbit_inclination_rad)
            orbit_z = orbit_radius * np.sin(sat._theta) * np.sin(orbit_inclination_rad)
            sat._orbit.set_data(
                orbit_x,
                orbit_y
            )
            sat._orbit.set_3d_properties(orbit_z)

            sat_x = orbit_radius * np.cos(angle_rad)
            sat_y = orbit_radius * np.sin(angle_rad) * np.cos(orbit_inclination_rad)
            sat_z = orbit_radius * np.sin(angle_rad) * np.sin(orbit_inclination_rad)
            sat._point.set_data([sat_x], [sat_y])
            sat._point.set_3d_properties([sat_z])

    def start_animated_plot(self) -> None:
        earth_deg_per_sec = 360/(24*3600)

        def update() -> bool:
            now = time.time()
            dt = now - self._last_update
            self._last_update = now

            dt_scaled = dt * self.get_timescale()

            self._earth_angle = (self._earth_angle + earth_deg_per_sec * self._timescale * dt_scaled) % 360
            for sat in self.satellites:
                sat_deg_per_sec = 360 / sat.period
                if sat._angle is None:
                    raise Exception

                sat._angle = (sat._angle + sat_deg_per_sec * self._timescale * dt_scaled) % 360

            self.rotate_earth(angle=self._earth_angle)
            self.update_ground_stations()
            self.update_satellites()
            self.update_fov_circles()
            self.canvas.draw_idle()
            return True

        GLib.timeout_add(100, update)

    def set_orbit_altitude(self, altitude: float | str) -> None:
        self.satellites[0].altitude = float(altitude)
        mu = 398600
        r = EARTH_RADIUS + float(altitude)
        self.satellites[0].period = 2*np.pi * np.sqrt(r**3 / mu)
        self.update_satellites()
    
    def get_orbit_altitude(self) -> float:
        return self.satellites[0].altitude
    
    def set_orbit_inclination(self, inclination: float | str) -> None:
        self.satellites[0].inclination = float(inclination)
        self.update_satellites()
    
    def get_orbit_inclination(self) -> float:
        return self.satellites[0].inclination
    
    def set_orbit_eccentricity(self, eccentricity: float | str) -> None:
        self.satellites[0].eccentricity = float(eccentricity)
        self.update_satellites()
    
    def get_orbit_eccentricity(self) -> float:
        return self.satellites[0].eccentricity
    
    def set_orbit_raan(self, raan: float | str) -> None:
        self.satellites[0].raan = float(raan)
        self.update_satellites()
    
    def get_orbit_raan(self) -> float:
        return self.satellites[0].raan
    
    def set_orbit_period(self, period: float | str) -> None:
        self.satellites[0].period = float(period)
        self.update_satellites()
    
    def get_orbit_period(self) -> float:
        return self.satellites[0].period
    
    def set_timescale(self, timescale: float | str) -> None:
        self._timescale = float(timescale)
    
    def get_timescale(self) -> float:
        return self._timescale
    
    def set_gs_latitude(self, latitude: float | str) -> None:
        self.ground_stations[0].latitude = float(latitude)

    def get_gs_latitude(self) -> float:
        return self.ground_stations[0].latitude
    
    def set_gs_longitude(self, longitude: float | str) -> None:
        self.ground_stations[0].longitude = float(longitude)
    
    def get_gs_longitude(self) -> float:
        return self.ground_stations[0].longitude

class AddGroundStationDialog(Adw.Dialog):
    def __init__(
            self,
            get_ground_stations_callback: typing.Callable,
            add_ground_station_callback: typing.Callable,
            content_height: int=500,
            content_width: int=400,
    ) -> None:
        super().__init__(
            content_height=content_height,
            content_width=content_width
        )
        self.get_ground_stations = get_ground_stations_callback
        self.add_ground_station = add_ground_station_callback

        self._gs_name = f'GS {len(self.get_ground_stations())+1}'
        self._gs_lat = 0.0
        self._gs_lon = 0.0
        self._gs_min_elevation = 0.0

        dialog_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(child=dialog_box)
        self._window_title = Adw.WindowTitle(title='Add ground station')
        dialog_header_bar = Adw.HeaderBar(
            title_widget=self._window_title
        )
        dialog_box.append(child=dialog_header_bar)

        margin = 17
        parameters_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_top=margin,
            margin_bottom=margin,
            margin_start=margin,
            margin_end=margin,
            spacing=margin
        )
        dialog_box.append(child=parameters_box)

        parameters_group = Adw.PreferencesGroup(title='Parameters')
        parameters_box.append(child=parameters_group)

        name_row = widgets.EntryRow(
            title='Name',
            value=self.get_gs_name(),
            callable=self.set_gs_name
        )
        parameters_group.add(child=name_row)

        coordinates_row = widgets.DoubleEntryRow(
            title='Coordinates',
            callable_1=self.set_gs_lat,
            callable_2=self.set_gs_lon,
            value_1=self.get_gs_lat(),
            value_2=self.get_gs_lon(),
            placeholder_text_1='latitude (°)',
            placeholder_text_2='longitude (°)'
        )
        parameters_group.add(child=coordinates_row)

        min_elevation_row = widgets.EntryRow(
            title='Minimum elevation',
            callable=self.set_gs_min_elevation,
            value=self.get_gs_min_elevation()
        )
        parameters_group.add(child=min_elevation_row)

        add_ground_station_row = widgets.ButtonBarRow(
            label='Add ground station',
            callable=self.on_add_ground_station
        )
        parameters_group.add(child=add_ground_station_row)

    def set_gs_name(self, name: str) -> None:
        self._gs_name = name
    
    def get_gs_name(self) -> str:
        return self._gs_name
    
    def set_gs_lat(self, lat: float | str) -> None:
        self._gs_lat = float(lat)
    
    def get_gs_lat(self) -> float:
        return self._gs_lat
    
    def set_gs_lon(self, lon: float | str) -> None:
        self._gs_lon = float(lon)
    
    def get_gs_lon(self) -> float:
        return self._gs_lon

    def set_gs_min_elevation(self, elevation: float | str) -> None:
        self._gs_min_elevation = float(elevation)
    
    def get_gs_min_elevation(self) -> float:
        return self._gs_min_elevation

    def on_add_ground_station(self) -> None:
        self.add_ground_station(
            name=self.get_gs_name(),
            latitude=self.get_gs_lat(),
            longitude=self.get_gs_lon(),
            min_elevation=self.get_gs_min_elevation()
        )
        self.close()

class AddSatelliteDialog(Adw.Dialog):
    def __init__(
            self,
            get_satellites_callback: typing.Callable,
            add_satellite_callback: typing.Callable,
            content_height: int=500,
            content_width: int=400,
    ) -> None:
        super().__init__(
            content_height=content_height,
            content_width=content_width
        )
        self.get_satellites = get_satellites_callback
        self.add_satellites = add_satellite_callback

        self._sat_name = f'Sat {len(self.get_satellites())+1}'
        self._sat_altitude = 0.0
        self._sat_eccentricity = 0.0
        self._sat_inclination = 0.0
        self._sat_raan = 0.0

        dialog_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(child=dialog_box)
        self._window_title = Adw.WindowTitle(title='Add satellite')
        dialog_header_bar = Adw.HeaderBar(
            title_widget=self._window_title
        )
        dialog_box.append(child=dialog_header_bar)

        margin = 17
        parameters_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_top=margin,
            margin_bottom=margin,
            margin_start=margin,
            margin_end=margin,
            spacing=margin
        )
        dialog_box.append(child=parameters_box)

        parameters_group = Adw.PreferencesGroup(title='Parameters')
        parameters_box.append(child=parameters_group)

        name_row = widgets.EntryRow(
            title='Name',
            value=self.get_sat_name(),
            callable=self.set_sat_name
        )
        parameters_group.add(child=name_row)

        altitude_row = widgets.EntryRow(
            title='Altitude',
            value=self.get_sat_altitude(),
            callable=self.set_sat_altitude
        )
        parameters_group.add(child=altitude_row)

        eccentricity_row = widgets.EntryRow(
            title='Eccentricity',
            value=self.get_sat_eccentricity(),
            callable=self.set_sat_eccentricity
        )
        parameters_group.add(child=eccentricity_row)

        inclination_row = widgets.EntryRow(
            title='Inclination',
            value=self.get_sat_inclination(),
            callable=self.set_sat_inclination
        )
        parameters_group.add(child=inclination_row)

        raan_row = widgets.EntryRow(
            title='RAAN',
            value=self.get_sat_raan(),
            callable=self.set_sat_raan
        )
        parameters_group.add(child=raan_row)

        add_satellite_row = widgets.ButtonBarRow(
            label='Add satellite',
            callable=self.on_add_satellite
        )
        parameters_group.add(child=add_satellite_row)

    def set_sat_name(self, name: str) -> None:
        self._sat_name = name
    
    def get_sat_name(self) -> str:
        return self._sat_name
    
    def set_sat_altitude(self, altitude: float | str) -> None:
        self._sat_altitude = float(altitude)
    
    def get_sat_altitude(self) -> float:
        return self._sat_altitude
    
    def set_sat_eccentricity(self, eccentricity: float | str) -> None:
        self._sat_eccentricity = float(eccentricity)
    
    def get_sat_eccentricity(self) -> float:
        return self._sat_eccentricity

    def set_sat_inclination(self, inclination: float | str) -> None:
        self._sat_inclination = float(inclination)
    
    def get_sat_inclination(self) -> float:
        return self._sat_inclination

    def set_sat_raan(self, raan: float | str) -> None:
        self._sat_raan = float(raan)
    
    def get_sat_raan(self) -> float:
        return self._sat_raan

    def on_add_satellite(self) -> None:
        self.add_satellites(
            name=self.get_sat_name(),
            altitude=self.get_sat_altitude(),
            eccentricity=self.get_sat_eccentricity(),
            inclination=self.get_sat_inclination(),
            raan=self.get_sat_raan()
        )
        self.close()

class ObjectGroup(Adw.PreferencesGroup):
    def __init__(
            self,
            title: str,
            object_type: typing.Literal['ground_station', 'satellite'],
            get_objects_callback: typing.Callable,
            add_object_callback: typing.Callable
    ) -> None:
        super().__init__(title=title)
        self.get_objects = get_objects_callback
        self.add_object = add_object_callback
        self.object_type = object_type

        for object in self.get_objects():
            object_row = widgets.DoubleButtonRow(
                title=object.name,
                label_1='Info',
                icon_name_1='dialog-information-symbolic',
                callable_1=self.on_object_info,
                label_2='Remove',
                icon_name_2='list-remove-symbolic',
                callable_2=self.on_remove_object,
            )
            self.add(child=object_row)

        add_object_row = widgets.ButtonRow(
            title=f'Add {title.removesuffix('s').lower()}',
            label='Add',
            icon_name='list-add-symbolic',
            callable=self.on_add_object
        )
        self.add(child=add_object_row)

    def on_add_object(self) -> None:
        match self.object_type:
            case 'ground_station':
                dialog = AddGroundStationDialog(
                    get_ground_stations_callback=self.get_objects,
                    add_ground_station_callback=self.add_object
                )
                dialog.present()

            case 'satellite':
                dialog = AddSatelliteDialog(
                    get_satellites_callback=self.get_objects,
                    add_satellite_callback=self.add_object
                )
                dialog.present()

    def on_remove_object(self) -> None:
        pass

    def on_object_info(self) -> None:
        pass

class GeneralPage(Adw.PreferencesPage):
    def __init__(self) -> None:
        super().__init__()
        self.ground_stations: list[GroundStation] = []
        self.satellites: list[Satellite] = []

        self.add_ground_station(
            name='HOGS',
            latitude=55.9,
            longitude=3.32,
            altitude=0.0,
            min_elevation=85.0
        )
        self.add_ground_station(
            name='Ngari',
            latitude=32,
            longitude=80,
            altitude=5.0,
            min_elevation=10.0
        )
        self.add_ground_station(
            name='Aristarchos',
            latitude=37.59,
            longitude=22.11,
            altitude=2.34,
            min_elevation=10.0
        )
        self.add_satellite(
            name='QEYSSat',
            altitude=550,
            inclination=97.6,
            eccentricity=0.0,
            raan=167.4
        )
        # self.add_satellite(
        #     name='Micius',
        #     altitude=500,
        #     inclination=97.4,
        #     eccentricity=0.0,
        #     raan=0
        # )

        self.diffraction_group = GeneralGroup(
            wavelength=785e-9,
            min_elevation=30.0
        )
        self.add(group=self.diffraction_group)

        self.orbit_group = OrbitGroup(
            get_ground_stations_callback=self.get_ground_stations,
            get_satellites_callback= self.get_satellites,
        )
        self.add(group=self.orbit_group)

        self.ground_stations_group = ObjectGroup(
            title='Ground stations',
            object_type='ground_station',
            get_objects_callback=self.get_ground_stations,
            add_object_callback=self.add_ground_station
        )
        self.add(group=self.ground_stations_group)

        self.satellites_group = ObjectGroup(
            title='Satellites',
            object_type='satellite',
            get_objects_callback=self.get_satellites,
            add_object_callback=self.add_satellite
        )
        self.add(group=self.satellites_group)

    def get_wavelength(self) -> float:
        return self.diffraction_group.get_wavelength()

    def get_ground_stations(self) -> list[GroundStation]:
        return self.ground_stations
    
    def get_satellites(self) -> list[Satellite]:
        return self.satellites

    def add_ground_station(
            self,
            name: str,
            latitude: float,
            longitude: float,
            altitude: float,
            min_elevation: float
    ) -> None:
        if name is None:
            name = f'GS {len(self.ground_stations)+1}'

        gs = GroundStation(
            name=name,
            latitude=latitude,
            longitude=longitude,
            min_elevation=min_elevation
        )
        self.ground_stations.append(gs)

    def add_satellite(
            self,
            name: str,
            altitude: float,
            inclination: float,
            eccentricity: float,
            raan: float,
            period: typing.Optional[float] = None
    ) -> None:
        if name is None:
            name = f'Sat {len(self.satellites)+1}'

        if period is None:
            mu = 398600
            r = EARTH_RADIUS + altitude
            period = float(2*np.pi * np.sqrt(r**3 / mu))

        sat = Satellite(
            name=name,
            altitude=altitude,
            inclination=inclination,
            eccentricity=eccentricity,
            raan=raan,
            period=period
        )
        self.satellites.append(sat)