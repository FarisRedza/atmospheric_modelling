import math
import datetime
import tempfile
import os

import skyfield.api
import skyfield.timelib
# from skyfield.api import load, wgs84, EarthSatellite, Timescale, Time

def main():
    epoch_time = datetime.datetime(
        year=2025,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
        tzinfo=datetime.timezone.utc
    )
    print(epoch_time)
    exit()
    tle_data = kepler_to_tle(
        satellite_name='QEYSSat',
        semi_major_axis=6921000,
        eccentricity=0,
        inclination=97.6,
        raan=167.4,
        arg_periapsis=98.9170,
        mean_anomaly=60,
        epoch=epoch_time
    )
    print(tle_data)


    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(tle_data)
            qrackling = skyfield.api.load(tmp.name)[0]
    finally:
        os.remove(path)

    hogs = skyfield.api.wgs84.latlon(
        latitude_degrees=55.9097,
        longitude_degrees=-3.3200,
        elevation_m=10
    )

    time_scale = skyfield.api.load.timescale()
    t_start = time_scale.utc(epoch_time)
    t_end = time_scale.utc(
        t_start.utc_datetime() + datetime.timedelta(days=365*2)
    )

def kepler_to_tle(
        satellite_name: str,
        semi_major_axis: float,
        eccentricity: float,
        inclination: float,
        raan: float,
        arg_periapsis: float,
        mean_anomaly: float,
        epoch: datetime.datetime,
        catalog_number: int = 99999,
        classification: str = 'U',
        international_designator: str = '99001A',
) -> str:
    EARTH_MASS = 398600.4418
    DAY_SECONDS = 86400

    mean_notion = (1 / (2 * math.pi)) * math.sqrt(EARTH_MASS / semi_major_axis**3) * DAY_SECONDS
    
    year = epoch.year % 100
    day_of_year = (
        epoch - datetime.datetime(
            year=year,
            month=1,
            day=1,
            tzinfo=datetime.timezone.utc
        )
    ).days + 1

    epoch_tle = f'{year:02}{day_of_year:03}.{epoch.hour * 3600 + epoch.minute * 60 + epoch.second:09.6f}'
    
    tle = f'''{satellite_name}
1 {catalog_number}{classification} {international_designator}   {epoch_tle}  .00000000  00000-0  00000-0 0  9991
2 {catalog_number} {inclination:8.4f} {raan:8.4f} {eccentricity * 1e7:07.0f} {arg_periapsis:8.4f} {mean_anomaly:8.4f} {mean_notion:11.8f} 00000
'''
    return tle

def get_zenith_overpass():
    pass

if __name__ == '__main__':
    main()