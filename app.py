from flask import Flask, request, abort, jsonify, send_from_directory
from data_process import data_process

app = Flask(__name__)


@app.route("/typhoon_history")
def typhoon_history():
    return jsonify(data_process('bst_all.txt'))
