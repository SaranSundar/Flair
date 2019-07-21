import os
import sys

from flask import Flask, render_template

from webview_api import webview_api

if getattr(sys, 'frozen', False):
    # Logic used for packaging app with py2app
    # cwd = os.getcwd()
    # app = Flask(__name__, static_folder=str(cwd) + "/static", template_folder=str(cwd) + "/templates")
    # Logic used for packaging app with PyInstaller
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__, static_folder="static", template_folder="templates")

# Disables caching for each flair app that uses PyWebView
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1

# Registers webview API's under /webview/<api-name> to keep code separate and clean
app.register_blueprint(webview_api, url_prefix='/webview')


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
        Can be useful for chrome tools debugging.
    """
    run_app('127.0.0.1', 43948)
