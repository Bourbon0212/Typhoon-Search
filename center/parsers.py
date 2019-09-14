import os
import re
from datetime import datetime, timezone

_date_pattern = re.compile(r'^\((.+) UTC\)$')
_member_pattern = re.compile(r'^([A-Z]+):$')
_initial_pattern = re.compile(r'^(?P<time>\d{6})Z (?P<lat>\d+(\.\d+)?[NS]) (?P<lon>\d+(\.\d+)?[EW]) (?P<ws>\d+)KT$')
_forecast_pattern = re.compile(r'^\(\+(?P<hour>\d+)H\) (?P<lat>\d+(\.\d+)?[NS]) (?P<lon>\d+(\.\d+)?[EW]) (?P<ws>.+)KT$')

def parse_forecast(text):

    '''
        Get all the center points w.r.t. each time

        output:
            1. time: e.g.: 2019-07-26 03:30:42+00:00
            2. tracks:
                {
                    'HKO':
                        {'initial_time': '260600', 'position':
                            {
                                0: (30.8, 136.1), 24: (34.9, 136.6), 48: (36.7, 140.3)
                            }
                        }
                    , ..., 
                }
    '''
    content = text.split('\n')

    time = None
    tracks = {}
    member_holder = None

    for line in content:
        # Extract date
        m = _date_pattern.search(line)
        if m:
            time = datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

        # Extract member name and hold it
        m = _member_pattern.search(line)
        if m:
            member = m.group(1)
            tracks.update({member: {'initial_time': None, 'position': {}}})
            member_holder = member

        # Extract initial location
        m = _initial_pattern.search(line)
        if m and member_holder is not None:
            d = m.groupdict()
            tracks[member_holder]['initial_time'] = d['time']
            lat = float(d['lat'][:-1]) if d['lat'][-1] == 'N' else -float(d['lat'][:-1])
            lon = float(d['lon'][:-1]) if d['lon'][-1] == 'E' else -float(d['lon'][:-1])
            tracks[member_holder]['position'].update({
                0: (lat, lon)
            })

        # Extract forecast track
        m = _forecast_pattern.search(line)
        if m and member_holder is not None:
            d = m.groupdict()
            hour = int(d['hour'])
            lat = float(d['lat'][:-1]) if d['lat'][-1] == 'N' else -float(d['lat'][:-1])
            lon = float(d['lon'][:-1]) if d['lon'][-1] == 'E' else -float(d['lon'][:-1])
            tracks[member_holder]['position'].update({
                hour: (lat, lon)
            })

    return time, tracks


def parse_besttrack_fromfile(fp):
    result = []
    with open(fp, 'r') as f:
        name = None
        code = None
        dissipation = None
        time_series = {}
        for line in f:
            if line[:5] == '66666': # typhoon header
                if code is not None: # exist code; skip 0th step
                    result.append({
                        'name': name,
                        'code': code,
                        'time_series': dict(time_series),
                        'dissipation': dissipation,
                    })
                name = line[30:50].strip()
                code = line[6:10]
                dissipation = line[26:27]
                time_series = {}
            elif line[9:12] == '002': # track
                year = int(line[0:2]) + 1900
                if year < 1950:
                    year += 100
                month = int(line[2:4])
                day = int(line[4:6])
                hour = int(line[6:8])
                time = datetime(year, month, day, hour, tzinfo=timezone.utc)

                lat = float(line[15:18]) / 10
                lon = float(line[19:23]) / 10
                time_series.update({time: (lat, lon)})
    return result
