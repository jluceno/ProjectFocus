import sys
import os
import logging
import threading
import json
from flask import Flask, render_template, jsonify, request
from core import Core


class FlaskServer(threading.Thread):
    test_number = 0

    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')

        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    else:
        app = Flask(__name__)

    def __init__(self):
        super().__init__()

    @staticmethod
    @app.route("/")
    def render_main_display():
        return render_template("hfile.html")

    @staticmethod
    @app.route("/config", methods=['PUT'])
    def config_pf():
        Core.add_new_api(json.loads(request.data))
        return "200"

    @staticmethod
    @app.route("/update")
    def update_display():
        message = {'greeting':'Hello from Flask!' + str(Core.test_number)}
        htmlDoc = FlaskServer.app.make_response(rv=(jsonify(message), 200, {"Access-Control-Allow-Origin":"http://127.0.0.1:8080"}))
        FlaskServer.test_number += 1
        return htmlDoc

    @staticmethod
    @app.route("/nike")
    def update_nike():
        resp = FlaskServer.app.make_response(
            rv=(Core.get_nike_data(),
            200,
            {"Access-Control-Allow-Origin":"http://127.0.0.1:8080"}
            ))
        return resp

    @staticmethod
    @app.route("/timeular")
    def update_timeular():
        resp = FlaskServer.app.make_response(
            rv=(Core.get_timeular_data(),
            200,
            {"Access-Control-Allow-Origin":"http://127.0.0.1:8080"}
            ))
        return resp

    @staticmethod
    def start():
        if FlaskServer.app is not None:
            FlaskServer.app.run(host='127.0.0.1', port=5000)