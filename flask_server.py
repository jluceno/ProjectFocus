import sys
import os
import logging
from flask import Flask, render_template, jsonify


class flask_server:
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')

        print(template_folder)
        print(static_folder)

        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    else:
        app = Flask(__name__)

    @staticmethod
    @app.route("/")
    def render_main_display():
        return render_template("hfile.html")

    @staticmethod
    @app.route("/update")
    def update_display():
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message), 200

    @staticmethod
    def start_server():
        if flask_server.app is not None:
            flask_server.app.run(host='127.0.0.1', port=5000)