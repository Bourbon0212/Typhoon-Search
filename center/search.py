import json
import time

import requests, datetime

from .meta import URL_MAP


ROUTE_URL = 'https://t-search-momobobowayna.herokuapp.com/route_sorting'

def list_similar_typhoons(track, radius=50000, weight="", month=0, n=5):
    points = {
        'point{}'.format(i+1): {'longitude': v[1], 'latitude': v[0], 'radius': radius}
        for i, v in enumerate(track)
    }

    data = {
        'points': points,
        'parameter': {'w': weight, 'month': month, 'n': n},
    }

    datastr = json.dumps(data)

    success = False
    retries = 0

    while not success and retries < 10:
        with requests.post(ROUTE_URL, json=datastr) as resp:
            success = resp.ok
            retries += 1


    if not success:
        raise Exception('Failed to send route data to the service (Not sucess)')

    time.sleep(0.5)

    ret = []

    with requests.get(ROUTE_URL, timeout=120) as resp:
        if resp.ok:
            body = resp.json()
            for key, payload in body.items():
                rank = int(key)
                code = payload['id']
                name = payload['name']

                info = URL_MAP.get(code, {})
                year = info.get('year', 9999)
                zh = info.get('zh', '')
                links = info.get('links', {})

                ret.append({
                    'rank': rank,
                    'name': name,
                    'zh': zh,
                    'code': code,
                    'year': year,
                    'links': links,
                })
        else:
            raise Exception('Failed to load route data from the service (Not OK)')
    return ret


def forecast_points(track, weight="", month=0, n=5):
    '''
        Get the forecast points data
    '''

    num = len(track)
    floor, ceil = 50000, 300000

    dev = int( (ceil - floor) / (num - 1) )
    radius = list(range(50000, 300001, dev))

    points = {
        'point{}'.format(i+1): {'longitude': v[1], 'latitude': v[0], 'radius': radius[i]}
        for i, v in enumerate(track)
    }

    data = {
        'points': points,
        'parameter': {'w': weight, 'month': month, 'n': n},
    }

    return data

def get_latest_link(i):

    a = URL_MAP.keys()
    yr_2digit = str(datetime.datetime.now().year)[2:]

    this = []
    for key in a:
        if key.startswith(yr_2digit):
            this.append(key)

    code = this[-i]

    return code, URL_MAP[code]['links']['cwb']
