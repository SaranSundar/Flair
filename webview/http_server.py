import webview
import os
import sys
import socket
import threading
import logging

from random import random
from webview.util import base_uri

try:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import SimpleHTTPRequestHandler, HTTPServer

logger = logging.getLogger('pywebview')



def _get_random_port():
    def random_port():
        port = int(random() * 64512 + 1023)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.bind(('localhost', port))
            result = port
        except:
            result = None
            logger.warning('Port %s is in use' % port)
        finally:
            sock.close()

        return result

    port = random_port()
    while not port:
        port = random_port()

    return port


class HTTPHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath


def start_server(url):
    def _start():
        server_address = ('localhost', port)

        try:
            httpd = HTTPServer(server_address, HTTPHandler)
            httpd.base_path = base_path
            httpd.serve_forever()
        except Exception as e:
            logger.exception(e)

    base_path = os.path.dirname(url.replace('file://', ''))
    if not os.path.exists(base_path):
        raise IOError('Directory %s is not found' % base_path)
    port = _get_random_port()

    t = threading.Thread(target=_start)
    t.daemon = True
    t.start()

    new_url = 'http://localhost:{0}/{1}'.format(port, os.path.basename(url))
    logger.debug('HTTP server started on http://localhost:{0}'.format(port))
    return new_url