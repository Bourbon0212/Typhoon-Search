import re

import requests, datetime, time
from bs4 import BeautifulSoup

from .parsers import parse_forecast


LOG_URL = 'http://www.typhoon2000.ph/multi/log.php'
HEADERS = {'User-Agent': 'requests/2.*'}

def get_typhoons():
    '''
        Get the entire typhoon names from typhoon2000. The former, the later.

        output:
                [
                    ['<en>', '<zh-tw>', '<year>', '<key>'='<en>' + '<year>'], ...,
                ]
    '''
    with requests.get(LOG_URL, headers = HEADERS) as resp:
        resp.encoding = 'UTF-8'
        html_doc = resp.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    options = soup.select('form[name=view] option:not([value=""])')

    typhoons = []

    display_pattern = re.compile(r'(?P<en>.+) \((?P<hk>.+)/(?P<sim>.+)/(?P<tw>.+)\)')
    key_pattern = re.compile(r'(?P<name>.+)_(?P<year>\d+)')

    for elm in options:
        key = elm['value']

        md = display_pattern.search(elm.string)
        mk = key_pattern.search(key)

        if md and mk:
            gd = md.groupdict()
            gk = mk.groupdict()
            if gd['en'] != gk['name']:
                raise ValueError('Parsed names from `display` and `key` do not match: %s', key)
            else:
                typhoons.append((gd['en'], gd['tw'], int(gk['year']), key))
        else:
            raise ValueError('Fail to parse information from `display` or `key`: %s', key)

    return typhoons


def get_typhoon_track(key, member='CWB'):
    '''
        Get the specific typhoon forecast points data

        input:
            1. key: typhoon's en_year
            2. member: forecast center
        output:
            [ (lat, lon), ..., (lat, lon) ]
    '''
    params = {'name': key}

    track_pattern = re.compile(r'text\[(\d+)\] = "(.+?)";')

    with requests.get(LOG_URL, params=params, headers=HEADERS) as resp:
        resp.encoding = 'UTF-8'
        html_doc = resp.text
        results = track_pattern.findall(html_doc) # forecast points from all centers

    full_track = []

    miss = 1
    data_time = ''

    for idx, elm in enumerate(results):
        istr, raw = elm
        text = raw.replace('\\n', '\n')
        data_time, tracks = parse_forecast(text)

        try: # some centers may forecast fewer points
            full_track.append(tracks[member]['position'][0])

            if idx == len(results) - 1:
                full_track += [
                    pos for h, pos in tracks[member]['position'].items() if h > 0
                ]

        except:
            print(member + ' has fewer forecast points, ' + str(miss) + ' at ' + str(data_time))

    full_track.append(data_time)
    
    return full_track

def get_alive_typhoons(member='CWB'):

    keys = get_typhoons()[0:1]

    full_track = {}

    for typ in keys:
        key = typ[3]
        params = {'name': key}

        track_pattern = re.compile(r'text\[(\d+)\] = "(.+?)";')

        with requests.get(LOG_URL, params=params, headers=HEADERS) as resp:
            resp.encoding = 'UTF-8'
            html_doc = resp.text
            results = track_pattern.findall(html_doc) # forecast points from all centers

        full_track[key] = []

        miss = 1
        data_time = ''

        for idx, elm in enumerate(results):
            istr, raw = elm
            text = raw.replace('\\n', '\n')
            data_time, tracks = parse_forecast(text)

            try: # some centers may forecast fewer points
                full_track[key].append(tracks[member]['position'][0])

                if idx == len(results) - 1:
                    full_track[key] += [
                        pos for h, pos in tracks[member]['position'].items() if h > 0
                    ]

            except:
                print(member + ' has fewer forecast points, ' + str(miss) + ' at ' + str(data_time))

        now = datetime.datetime.now(datetime.timezone.utc)

        if now - data_time >= datetime.timedelta(days=1):
            return full_track
