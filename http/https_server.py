#!/usr/bin/python

import BaseHTTPServer
import SimpleHTTPServer
import ssl

httpd = BaseHTTPServer.HTTPServer(('192.168.168.163', 443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./localhost.pem', keyfile='localhost.key', server_side=True)
httpd.serve_forever()
