import math
import datetime
import tempfile

import skyfield.api
import skyfield.timelib

def main():
    epoch_time = datetime.datetime(
        year=2000,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
        tzinfo=datetime.timezone.utc
    )

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

    with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tle_file:
        tle_file.write(tle_data)
        tle_file.flush()
        file_name = tle_file.name

        qeyssat = skyfield.api.load.tle_file(file_name)[0]

    hogs = skyfield.api.Topos(
        latitude=55.909723,
        longitude=-3.319995,
        elevation_m=10
    )

    time_scale = skyfield.api.load.timescale()
    t_start = time_scale.utc(epoch_time)
    t_end = time_scale.utc(
        t_start.utc_datetime() + datetime.timedelta(days=365*100)
    )

    find_zenith_pass(
        satellite=qeyssat,
        ground_station=hogs,
        t_start=t_start,
        t_end=t_end
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
        international_designator: str = '99001A'
) -> str:
    EARTH_MASS = 398600.4418
    DAY_SECONDS = 86400

    mean_notion = (1 / (2 * math.pi)) * math.sqrt(EARTH_MASS / semi_major_axis**3) * DAY_SECONDS

    year = epoch.year % 100
    day_of_year = (epoch - datetime.datetime(
        year=epoch.year,
        month=1,
        day=1,
        tzinfo=datetime.timezone.utc
    )).days + 1

    epoch_tle = f'{year:02}{day_of_year:03}.{epoch.hour * 3600 + epoch.minute * 60 + epoch.second:09.6f}'

    tle = f'''{satellite_name}
1 {catalog_number}{classification} {international_designator}   {epoch_tle}  .00000000  00000-0  00000-0 0  9991
2 {catalog_number} {inclination:8.4f} {raan:8.4f} {eccentricity * 1e7:07.0f} {arg_periapsis:8.4f} {mean_anomaly:8.4f} {mean_notion:11.8f} 00000
'''
    return tle

def find_zenith_pass(
        satellite: skyfield.api.EarthSatellite,
        ground_station: skyfield.api.Topos,
        t_start: skyfield.timelib.Time,
        t_end: skyfield.timelib.Time
) -> list | None:
    times, events = satellite.find_events(
        ground_station,
        t_start,
        t_end,
        altitude_degrees=89.9
    )
    if len(events) > 0:
        zenith_events = []
        for t, event in zip(times, events):
            if event == 1:
                print(f'Zenith pass at: {t.utc_datetime()} UTC')
                zenith_events.append(t.utc_datetime())
        return zenith_events
    else:
        print('No zenith pass found in the given time range.')
        return None

if __name__ == '__main__':
    main()