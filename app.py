import os
import platform
import signal
import subprocess
import sys
from subprocess import Popen, PIPE

from flask import Flask, render_template
from flask_cors import CORS
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from flask_blueprints.example_bp import example_bp
from flask_blueprints.example_bp import example_ws
from flask_blueprints.webview_bp import webview_bp

operating_system = str(platform.system()).lower()

if getattr(sys, 'frozen', False):
    if "window" in operating_system:
        # Logic used for packaging app with PyInstaller
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')
        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    elif "darwin" in operating_system:
        # Logic used for packaging app with py2app
        cwd = os.getcwd()
        app = Flask(__name__, static_folder=str(cwd) + "/static", template_folder=str(cwd) + "/templates")
    else:
        print("Operating system not supported, please try on Mac OS or Windows")
        sys.exit(1)
else:
    app = Flask(__name__, static_folder="static", template_folder="templates")

CORS(app)

# Disables caching for each flair app that uses PyWebView
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1

# Registers webview API's under /webview/<api-name> to keep code separate and clean
app.register_blueprint(webview_bp, url_prefix='/webview_bp')
app.register_blueprint(example_bp, url_prefix='/example_bp')

ws = Sockets(app)

ws.register_blueprint(example_ws, url_prefix='/example_ws')


@app.after_request
def add_header(response):
    """
        Disables caching for each flair app that uses PyWebView
    """
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route("/")
def home():
    """
        Templates should be stored inside templates folder
    """
    return render_template("index.html")


def kill_port(port):
    process = Popen(["lsof", "-i", ":{0}".format(port)], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    for process in str(stdout.decode("utf-8")).split("\n")[1:]:
        data = [x for x in process.split(" ") if x != '']
        if len(data) <= 1:
            continue

        os.kill(int(data[1]), signal.SIGKILL)


def run_app(url, port, start_redis):
    if "darwin" in operating_system:
        kill_port(port)
    server = pywsgi.WSGIServer((url, port), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # app.run(host=url, port=port, threaded=True)


if __name__ == '__main__':
    """
        App can be launched from this file itself
        without needing to package or launch Window.
        Can be useful for chrome tools debugging. Make sure port number
        is the same as in flair.py
    """
    run_app('localhost', port=43968, start_redis=False)
