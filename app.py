import os

from flask import Flask, request, abort, jsonify, json, send_from_directory
from data_process import data_process
from get_functions import history_point_data
from radix_sort import radix_sort

app = Flask(__name__)
path = 'bst_all.txt'
url = "https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip"
#U = {'points':{'point1':{'longitude': 130.3, 'latitude':21.3, 'radius': 50000}, 'point2':{'longitude': 127.9, 'latitude':21.8, 'radius': 50000}, 'point3':{'longitude': 126.0, 'latitude':22.4, 'radius': 100000}, 'point4':{'longitude': 123.2, 'latitude':23.5, 'radius': 150000}, 'point5':{'longitude': 110.2, 'latitude':23.5, 'radius': 150000}, 'point6':{'longitude': 100.2, 'latitude':23.5, 'radius': 150000}}, 'parameter':{'w':'', 'n':10, 'month':0}}
user = {}

@app.route('/front/<path:name>')
# Front end, typhoon route visualization
def reportroute(name):
    name = 'index.html' if name is "" else name
    path = os.path.join("front", name)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    return content

def send_js(name):
    return send_from_directory('/front/js', name)

def send_css(name):
    return send_from_directory('/front/css', name)

@app.route("/route_sorting", methods = ["GET", "POST"])
def route_sorting():
    global user
    if request.method == "POST":
        user = request.get_json()
        print("USER INPUTS ===POST=== SUCCESS!")
        return user
    elif request.method == "GET":
        if user != {}:
            print("RADIX SORT ===GET=== START!")
            history = data_process(url) # everything
            point_data = history_point_data(history) # P(i, j)
            U = json.loads(user) # convert user inputs to dict
            return jsonify(radix_sort(history, point_data, U))
        else:
            print('NO USER INPUTS, ===POST=== FIRST!')
            return ("NO USER INPUTS, ===POST=== FIRST!")

@app.route("/user_inputs", methods = ["GET"])
def user_inputs():
    global user
    if user != {}:
        return user
    else:
        return ("NO USER INPUTS, ===POST=== FIRST!")

@app.route("/typhoon_history", methods = ["GET"])
def typhoon_history():
    return jsonify(data_process(url))
