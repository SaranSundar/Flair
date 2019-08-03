import os
import platform
import sys

from flask import Flask, render_template
from flask_cors import CORS
from flask_sockets import Sockets

from flask_blueprints.example_bp import example_bp
from flask_blueprints.example_bp import example_ws
from flask_blueprints.webview_bp import webview_bp

if getattr(sys, 'frozen', False):
    operating_system = str(platform.system()).lower()
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


def run_app(url, port):
    app.run(host=url, port=port, threaded=True)


if __name__ == '__main__':
    """
        App can be launched from this file itself
        without needing to package or launch Window.
        Can be useful for chrome tools debugging. Make sure port number
        is the same as in flair.py
    """
    run_app('127.0.0.1', port=43968)
