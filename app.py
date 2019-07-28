from flask import Flask, request, abort, jsonify, send_from_directory, json
from data_process import data_process
from get_functions import history_point_data
from radix_sort import radix_sort

import os

app = Flask(__name__)
url = "https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip"

@app.route("/route_sorting", methods = ["GET"])
def route_sorting():

    try:
        toPOST = request.args.get('toPOST') # user input points
    except:
        print("GET failed")
        return jsonify({"message":"request body is not json."}), 400

    if toPOST != {}:
        print("RADIX SORT START!")

        ### Process history data
        try:
            history = data_process(url) # entire historical typhoon tracks
            point_data = history_point_data(history) # P(i, j)
        except:
            return jsonify({"message":"Defective JMA API."}), 406

        ### Process similarity model
        try:
            U = json.loads(toPOST) # convert user inputs to dict
        except:
            return jsonify({"message":"Wrong fromat in points data."}), 400

        ### Success
        return jsonify(radix_sort(history, point_data, U))
    else:
        print('NO USER INPUTS!')
        return jsonify({"message":"user input is empty."}), 400


@app.route("/typhoon_history")
def typhoon_history():
    return jsonify(data_process(url))

@app.route('/')
def index():
    return send_from_directory('front', 'index.html')

@app.route('/<path:name>')
# 檔案在不在,在哪裡/有沒有亂戳,怎麼丟
def reportroute(name):
    name = 'index.html' if name is "" else name
    return send_from_directory('front', name)
