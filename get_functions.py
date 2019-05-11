from data_process import data_process
import math

def history_point_data(path):
    '''
        POINT_DATA
            Type : Dictionary
            Keys : International ID of each typhoon, 'i' in essay
            Value: list consists of tuple(latitude, longitude) of each point('j' in essay)
    '''
    ### Part 1. get historical typhoon data
    history = data_process(path)

    ### Part 2. generate P(i, j)
    point_data = {}

    for i in history: # for each typhoon, 'i' in essay
        points = [] # list to gather all points of this typhoon

        for j in history[i]['data']: # each point of this 'i' typhoon, 'j' in essay
            # unit 0.1 degree to 1 degree
            latitude = float(history[i]['data'][j]["latitude"]) / 10
            longitude = float(history[i]['data'][j]["longitude"]) / 10
            points.append((latitude, longitude))

        # add the list into point_data
        point_data[i] = points
    print("HISTORY POINTS DATA SUCCESS!")
    return point_data


def getDistance(latA, lonA, latB, lonB):
    '''
        Calculate distance btw two points(latA, lonA, latB, lonB), in meter
    '''
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = math.radians(latA)
    radLonA = math.radians(lonA)
    radLatB = math.radians(latB)
    radLonB = math.radians(lonB)

    pA = math.atan(rb / ra * math.tan(radLatA))
    pB = math.atan(rb / ra * math.tan(radLatB))
    x = math.acos(math.sin(pA) * math.sin(pB) + math.cos(pA) * math.cos(pB) * math.cos(radLonA - radLonB))
    c1 = (math.sin(x) - x) * (math.sin(pA) + math.sin(pB))**2 / math.cos(x / 2)**2
    c2 = (math.sin(x) + x) * (math.sin(pA) - math.sin(pB))**2 / math.sin(x / 2)**2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
    return distance
