from get_functions import history_point_data, getDistance, get_yymm, compute_weight
from center.meta import URL_MAP

def min_distance(history, point_data, U):
    '''
        MIN_DISTANCE
            Type : Dictionary
            Keys : International ID of each typhoon, 'i' in essay
            Value: (dict) Dik, the min distance for ith typhoon to kth predicted point, for all j

            {
                "typhoon_international_id" : {
                    'point_k1': (float),
                    'point_k2': (float),
                    ,...
                }
            }
    '''
    min_distance = {}

    for i in point_data: # i refers to the ith historic typhoon
        distance_ijk = {}

        for k in U['points']:
            min = 10 ** 10
            for j in point_data[i]:
                # calulate the minimum distance (lat_ij, long_ij, lat_k, long_k)
                if getDistance(j[0], j[1], U['points'][k]['latitude'], U['points'][k]['longitude']) < min:
                    min = getDistance(j[0], j[1], U['points'][k]['latitude'], U['points'][k]['longitude'])

            distance_ijk[k] = min
        min_distance[i] = distance_ijk

    print('MIN DISTANCE SUCCESS!')
    return min_distance

def weight_of_all(history, point_data, U):
    '''
        WEIGHT_OF_ALL
            Type : List
                ith:
                    0: typhoon_international_id
                    1: <Route Score> sigma(k = 1, M) [1 + kw, k, 1] | for all Dik < radius
                    2: <Time  Score> [year, month]

            [
                [ 'typhoon_international_id', sigma[1 + kw, k, 1], [year, month] ]
            ]
    '''
    temp = {} # key: typhoon name; Value: sigma(1 + k * w)
    min_dist = min_distance(history, point_data, U)
    num_predicted = len(U['points'].keys())
    w = compute_weight(num_predicted) if U['parameter']['w'] == '' else U['parameter']['w']

    ### Part 1. Route Score
    for i in point_data:
        score = [0, 0, 0] # sigma[total, k, 1]
        count = 1 # kth

        # Whether the min distance(Dik) is less than radius
        for k in U['points']:
            if min_dist[i][k] < U['points'][k]['radius']:
                score[2] += 1
                score[1] += count
            count += 1 # kth predicted

        # Route score of ith typhoon
        score[0] = score[2] + score[1] * w
        temp[i] = score

    ### Part 2. Time Score
    yymm_data = get_yymm(history)
    weight_of_all = [ [i, temp[i], yymm_data[i]] for i in temp ]

    print('WEIGHT OF ALL SUCCESS!')
    print('TIME WEIGHT: ' + str(w))
    return weight_of_all

def radix_sort(history, point_data, U):
    '''
        RADIX_SORT
            Type : Dictionary
            Keys : Priority of the approximate historic typhoons
            Value: (dict) typhoon_international_id, name, points
            {
                "1":{
                    "id": typhoon_international_id,
                    "name": name of the typhoon,
                    "points":[
                        {
                            "latitude":lat_i1,
                            "longitude":lon_i1
                        },
                        {
                            "latitude":lat_i2,
                            "longitude":lon_i2
                        },
                    ]
                },
            }
    '''
    import datetime
    weight = weight_of_all(history, point_data, U)

    ### Part 1. Sort by the year (the closer, the more prior)
    for i in range(len(weight) - 1, 0, -1):
        for j in range(i):
            if weight[j][2][0] < weight[j + 1][2][0]:
                ret = weight[j]
                weight[j] = weight[j + 1]
                weight[j + 1] = ret

    ### Part 2. Sort by the month (the closer, the more prior)
    month = U['parameter']['month']
    month = datetime.datetime.now().month if month == '0' else int(month)

    for i in range(len(weight) - 1, 0, -1):
        for j in range(i):
            if abs(weight[j][2][1] - month) > abs(weight[j + 1][2][1] - month):
                ret = weight[j]
                weight[j] = weight[j + 1]
                weight[j + 1] = ret

    ### Part 3. Sort by the route score (the higher, the more prior), S(1 + kw) > S(k) > S(1), S = Sigma
    for k in range(2, -1, -1):
        for i in range(len(weight) - 1, 0, -1):
            for j in range(i):
                if weight[j][1][k] < weight[j + 1][1][k]:
                    ret = weight[j]
                    weight[j] = weight[j + 1]
                    weight[j + 1] = ret

    ### Part 4. output
    final = {}
    n = U['parameter']['n']

    print() # For better layout of Showing total scores
    for i in range(n):
        typhoon_id = weight[i][0]

        ## name (zh first)
        en = history[typhoon_id]['header']['name']
        zh = URL_MAP[typhoon_id]['zh'] if typhoon_id in URL_MAP else en

        year = URL_MAP[typhoon_id]['year'] if typhoon_id in URL_MAP else 'N/A'
        link = URL_MAP[typhoon_id]['links']['cwb'] if typhoon_id in URL_MAP and URL_MAP[typhoon_id]['links'] != {} else 'N/A'

        print(weight[i][1], end = ", ")  ### Show the total score at local cmd
        print("NAME: " + zh, end = ", ")
        print("ID: " + typhoon_id, end = ", ")
        print("Year: " + str(year), end = ", ")
        print("link: " + link)

        json_point_data = []
        for j in point_data[typhoon_id]:
            lat = j[0]
            lon = j[1]
            temp = {"latitude": lat, "longitude": lon}
            json_point_data.append(temp)

        final[i + 1] = { "id": typhoon_id, "name": zh, "year": year, "points": json_point_data, "links": link }

    print() # For better layout of Showing total scores
    print('RADIX SORT SUCCESS!')
    return final
