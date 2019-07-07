import webbrowser

import webview
from flask import Blueprint, jsonify

webview_api = Blueprint('webview_api', __name__)


@webview_api.route("/choose-folder-path")
def choose_folder_path():
    """
    Invoke a folder selection dialog here
    :return directory_path : str
    """
    dirs = webview.create_file_dialog(webview.FOLDER_DIALOG)
    if dirs and len(dirs) > 0:
        directory = dirs[0]
        if isinstance(directory, bytes):
            directory = directory.decode("utf-8")

        response = {"status": "ok", "directory": directory}
    else:
        response = {"status": "cancel"}

    return jsonify(response)


@webview_api.route("/fullscreen")
def fullscreen():
    webview.toggle_fullscreen()
    return jsonify({})


@webview_api.route("/open-url/<url>")
def open_url(url):
    webbrowser.open_new_tab(url)

    return jsonify({})
