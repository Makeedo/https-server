#!/usr/bin/env python3

# 1) generate certificate
# openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
# make sure the generated server.pem file is in the same folder than httpserver.py
#
# 2) get and install python3
#
# 3) start server
# python3 httpserver.py [inboundPort] [outboundUrl]
# eg: python3 httpserver.py 80 http://locahlost:3000    --> forwards https://localhost to http://localhost:3000

import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

if len(sys.argv)-1 != 2:
    print("""
Usage: {} <port_number> <url>
    """.format(sys.argv[0]))
    sys.exit()

class Redirect(BaseHTTPRequestHandler):
   def do_GET(self):
       self.send_response(302)
       self.send_header('Location', sys.argv[2] + self.path)
       self.end_headers()

httpd = HTTPServer(("", int(sys.argv[1])), Redirect)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
httpd.serve_forever()