from data_process import data_process
import math

def history_point_data(history):
    '''
        Input: history ( = data_process() )
        POINT_DATA
            Type : Dictionary
            Keys : International ID of each typhoon, 'i' in essay
            Value: list consists of tuple(latitude, longitude) of each point('j' in essay)

            {
                "typhoon_international_id" : [ (latitude, longitude), ]
            }
    '''
    ### Part 1: generate P(i, j)
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
        Calculate distance btw two points(latA, lonA, latB, lonB), in meters
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
    try:
        c2 = (math.sin(x) + x) * (math.sin(pA) - math.sin(pB))**2 / math.sin(x / 2)**2
    except:
        c2 = 0

    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
    return distance

def get_yymm(history):
    '''
        Find the latest time of each typhoon [int(year), int(month)]
    '''
    yymm_data = {}

    for i in history: # for each typhoon, 'i' in essay
        yymm = [] # list to gather lateset time of this typhoon

        for j in history[i]['data']:
            year, month = j[0:2], j[2:4]
            if int(year) <= 50:
                year = '20' + year
            else:
                year = '19' + year

            yymm = [int(year), int(month)]

        # add the list into yymm_data
        yymm_data[i] = yymm
    print("YYMM DATA SUCCESS!")
    return yymm_data


def compute_weight(k):
    '''
        Inverse func of: [ k + (k - 1) ] - SIGMA(i = 1, w + 2)[i] >= 1
    '''
    import math

    w = (math.sqrt(16 * k - 15) - 5) / 2
    w = int(w) #floor the float above(w)
    return w if w > 0 else 1

''' Test of Time Weight
temp = compute_weight(1)
for k in range(1, 1000):

    if compute_weight(k) == temp:
        print('w = ' + str(compute_weight(k)) + ', k =' + str(k))
    else:
        print()
        print('w = ' + str(compute_weight(k)) + ', k =' + str(k))
        temp = compute_weight(k)
'''
