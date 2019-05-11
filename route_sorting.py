from get_functions import history_point_data, getDistance

#def route_sorting(path, user):

### get historical typhoon points, P(i,j) in essay
point_data = history_point_data('bst_all.txt')

### k(等小於丟)
U = {'point1':{'longitude': 123.0, 'latitude':24.5}, 'point2':{'longitude': 120.0, 'latitude':28.5}}

### generate D(i, j, k)
min_distance = {}

for i in point_data: # i refers to the ith historic typhoon

    distance_ijk = {}

    for k in U:

        min = 100000000000
        for j in point_data[i]:
            # calulate the minimum distance (lat_ij, long_ij, lat_k, long_k)
            if getDistance(j[0], j[1], U[k]['latitude'], U[k]['longitude']) < min:
                min = getDistance(j[0], j[1], U[k]['latitude'], U[k]['longitude'])

        distance_ijk[k] = min

    min_distance[i] = distance_ijk
