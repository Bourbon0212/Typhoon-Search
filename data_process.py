def data_process(path):
    ## Part 1. Find the length of the data
    fh1 = open(path, 'r')

    length = 0
    for aline in fh1:
        length += 1

    fh1.close()

    ## Part 2. return the data in dictionary

    fh1 = open(path, 'r')

    # variables
    history = {} # record each typhoon paths with header and data
    initial = True
    count = 1

    for aline in fh1:

        # 1. If encounter a header(begin with 66666)
        if aline[0:5] == '66666':
            # 1-1. After each typhoon ends
            if initial == False:
                # record header and data into history
                history[inter_ID] = {'header':header, 'data':data}

            # 1-2. Announce new header & data for the next typhoon
            inter_ID = aline[6:10]

            header = {}
            header['lines'] = aline[12:15].strip()
            header['tropical_ID'] = aline[16:20].strip()
            header['flag'] = aline[26].strip()
            header['time_diff'] = aline[28].strip()
            header['name'] = aline[30:50].strip()
            header['latest_revision'] = aline[64:72].strip()

            data = {}

            initial = False # eliminate the empty data for the first time

        # 2. For each point data of the typhoon
        else:
            point = aline[0:8]

            local = {}
            local['indicator'] = aline[9:12].strip()
            local['grade'] = aline[13].strip()
            local['latitude'] = aline[15:18].strip()
            local['longitude'] = aline[19:23].strip()
            local['central_pressure'] = aline[24:28].strip()
            local['max_windspeed'] = aline[33:36].strip()
            local['direction_50ktup'] = aline[41].strip()
            local['max_radius_50ktup'] = aline[42:46].strip()
            local['min_radius_50ktup'] = aline[47:51].strip()
            local['direction_30ktup'] = aline[52].strip()
            local['max_radius_30ktup'] = aline[53:57].strip()
            local['min_radius_30ktup'] = aline[58:62].strip()
            local['landfall_or_passage'] = aline[71].strip()

            # data (type: dict) records all the point data with points as keys
            data[point] = local

        # 3. For the last row in the data, record the last typhoon data to history
        if count == length:
            history[inter_ID] = {'header':header, 'data':data}

        # 4. update count times of the for loop
        count += 1

    fh1.close()

    print('DATA_PROCESS SUCCESS!')
    return history
