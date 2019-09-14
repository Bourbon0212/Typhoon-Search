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

    input = math.sin(pA) * math.sin(pB) + math.cos(pA) * math.cos(pB) * math.cos(radLonA - radLonB)
    input = -1 if input < -1 else input
    input = 1 if input > 1 else input
    x = math.acos(input)

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
        Find the argmax(w) of the corresponding k predicted points

        Theory:

            (i) When hasConflict --> a + bw versus c + dw, and a < c, b > d, where
                 |￣                x                                 x+w      ￣|
                 |　  a = x,  b = SIGMA(k - i),  c = x + omega,  d = SIGMA i  　 |
                 |　               i=0                                i=1     　 |
                 |__                                                      　　 __|

            (ii) Next, w = argmax omega{ Wp }, which means,
    　　                      p
            　        w = -(a - c) / (b - d) | b - d = 1, c - a = omega by altering different gap, x
    '''
    ### Part 1. Fing all the possible score pairs
    total_pair = [] # all the possible scor pairs (Sigmw i, Sigma k)
    num = list(range(1, k + 1))

    for i in range(1, 1 + k):
        row_of_i = []
        # 1. find the min sigma k, for given sigma i
        start = 0
        for k in range(i):
            start += num[k]

        # 2. find the max sigma k, for given sigma i
        end = 0
        for k in range(1, i + 1):
            end += num[-k]

        # 3. List all the possible sigma k
        ready = list(range(start, end + 1))

        for d in ready:
            temp = (i, d)
            row_of_i.append(temp)

        # 4. Append all possible pairs, for given Sigma i
        total_pair.append(row_of_i)

    ### Part 2. Find the all the omegas and W = argmax(w)
    omega_list = [] # List to contains all omegas
    maxk = len(total_pair)

    for l in range(maxk): # l refers to the current row, x in the discussion
        target = total_pair[l][-1] # Given sigma i, the biggest sigma k
        hasConflict = True
        m = l + 1 # m refers to the following rows after l, x + omega in the discussion

        while hasConflict and m < maxk: # If it is possible to have conflict
            if target[1] <= total_pair[m][0][1]: # If the target's max sigma k _lt_ the min of the Mth's, there's no conflict
                hasConflict = False
            else:
                omega = m - l # b/c: m - l = (x + omega) - x = omega
                omega_list.append(omega)

            m += 1 # Search for the next row


    return 1 if len(omega_list) == 0 else (max(omega_list))
