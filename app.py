from flask import Flask, request, abort, jsonify, json, send_from_directory
from data_process import data_process
from get_functions import history_point_data
from radix_sort import radix_sort

app = Flask(__name__)
path = 'bst_all.txt'
url = "https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip"
#U = {'points':{'point1':{'longitude': 130.3, 'latitude':21.3, 'radius': 50000}, 'point2':{'longitude': 127.9, 'latitude':21.8, 'radius': 50000}, 'point3':{'longitude': 126.0, 'latitude':22.4, 'radius': 100000}, 'point4':{'longitude': 123.2, 'latitude':23.5, 'radius': 150000}, 'point5':{'longitude': 110.2, 'latitude':23.5, 'radius': 150000}, 'point6':{'longitude': 100.2, 'latitude':23.5, 'radius': 150000}}, 'parameter':{'w':'', 'n':10, 'month':0}}
user = {}

@app.route("/typhoon_history", methods = ["GET"])
def typhoon_history():
    return jsonify(data_process(url))

@app.route("/route_sorting", methods = ["GET", "POST"])
def route_sorting():
    global user
    if request.method == "POST":
        user = request.get_json()
        print("USER INPUTS POST SUCCESS!")
        return user
    elif request.method == "GET":
        if user != {}:
            print("RASIX SORT GET START!")
            history = data_process(url) # everything
            point_data = history_point_data(history) # P(i, j)
            U = json.loads(user) # convert user inputs to dict
            return jsonify(radix_sort(history, point_data, U))
        else:
            return ("NO USER INPUTS, RE-POST PLEASE!")

@app.route("/user_inputs", methods = ["GET"])
def user_inputs():
    global user
    if user != {}:
        return user
    else:
        return ("NO USER INPUTS, RE-POST PLEASE!")
