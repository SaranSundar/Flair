import json

from flask import Blueprint

import webview
import webview.window as window

webview_bp = Blueprint('webview_bp', __name__)


@webview_bp.route("/open-file-dialog")
def open_file_dialog():
    file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')
    result = window.Window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
    result = json.dumps(result, default=str)
    return result
