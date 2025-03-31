import datetime
import tempfile

import numpy as np
import skyfield
from skyfield.api import load, Topos, EarthSatellite
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
        sat_name='QEYSSat',
        semi_major_axis=6921000,
        eccentricity=0,
        inclination=97.6,
        raan=167.4,
        arg_periapsis=98.9170,
        mean_anomaly=60,
        epoch=epoch_time
    )

    # file_name = 'qeyssat.TLE'
    # with open(file=file_name, mode='w') as file:
    #     file.write(tle_data)

    with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tle_file:
        tle_file.write(tle_data)
        tle_file.flush()
        file_name = tle_file.name

        qeyssat = load.tle_file(file_name)[0]

    hogs = Topos(
        latitude=55.909723000000000,
        longitude=-3.319995000000000,
        elevation_m=10
    )

    ts: skyfield.timelib.Timescale = load.timescale()
    t_start: skyfield.timelib.Time = ts.utc(epoch_time)
    t_end: skyfield.timelib.Time = ts.utc(t_start.utc_datetime() + datetime.timedelta(days=100*365))

    find_zenith_pass(
        satellite=qeyssat,
        ground_station=hogs,
        t_start=t_start,
        t_end=t_end
    )

def kepler_to_tle(
        sat_name: str,
        semi_major_axis: float,
        eccentricity: float,
        inclination: float,
        raan: float,
        arg_periapsis: float,
        mean_anomaly: float,
        epoch: datetime.datetime
) -> str:
    GM = 398600.4418
    DAY_SECONDS = 86400

    mean_notion = (1 / (2 * np.pi)) * np.sqrt(GM / semi_major_axis**3) * DAY_SECONDS

    year = epoch.year % 100
    doy = (epoch - datetime.datetime(
        year=epoch.year,
        month=1,
        day=1,
        tzinfo=datetime.timezone.utc
    )).days + 1

    epoch_tle = f'{year:02}{doy:03}.{epoch.hour * 3600 + epoch.minute * 60 + epoch.second:09.6f}'

    tle = f'''{sat_name}
1 99999U 24001A   {epoch_tle}  .00000000  00000-0  00000-0 0  9991
2 99999 {inclination:8.4f} {raan:8.4f} {eccentricity * 1e7:07.0f} {arg_periapsis:8.4f} {mean_anomaly:8.4f} {mean_notion:11.8f} 00000
'''
    return tle

def find_zenith_pass(
        satellite: EarthSatellite,
        ground_station: Topos,
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