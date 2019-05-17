from flask import Flask, request, abort, jsonify, send_from_directory
from data_process import data_process
from get_functions import history_point_data
from radix_sort import radix_sort

app = Flask(__name__)
path = 'bst_all.txt'
url = "https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip"
U = {'point1':{'longitude': 130.3, 'latitude':21.3, 'radius': 50000}, 'point2':{'longitude': 127.9, 'latitude':21.8, 'radius': 500000}, 'point3':{'longitude': 126.0, 'latitude':22.4, 'radius': 150000}, 'point4':{'longitude': 123.2, 'latitude':23.5, 'radius': 150000}}

@app.route("/typhoon_history")
def typhoon_history():
    return jsonify(data_process(path))

@app.route("/route_sorting")
def route_sorting():
    return jsonify(radix_sort(path, U))
