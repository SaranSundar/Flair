import json

from flask import Blueprint

import webview

webview_bp = Blueprint('webview_bp', __name__)


@webview_bp.route("/start-dialog/<option>")
def start_dialog(option):
    option = option.lower()
    choice = webview.OPEN_DIALOG  # DEFAULT
    if option == "save":
        choice = webview.SAVE_DIALOG
    elif option == "open":
        choice = webview.OPEN_DIALOG
    elif option == "folder":
        choice = webview.FOLDER_DIALOG
    file_types = ['All files (*.*)']
    result = webview.windows[0].create_file_dialog(choice, allow_multiple=True, file_types=file_types)
    result = json.dumps(result, default=str)
    return result  # if result is null this means nothing was chosen and dialog was cancelled
