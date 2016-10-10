#!/usr/bin/env python

import urllib, urllib.request
import json
import threading

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection

#IP = '127.0.0.1'
IP = '192.168.3.35'
PORT = 1215

laziness = 0.5
url = 'http://192.168.3.11:1215/getpeers'

neighbours = []
route = []

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        senderip = self.client_address
        message = urllib.parse.urlsplit(self.path).path
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
        status = ""
        if message in ["/file", "/file/"]:
            pass
        else:
            status = "Error"

        self.wfile.write(bytes(message, "utf8"))
        self.wfile.write(bytes(status, "utf8"))


    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "OK"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        self.wfile.write(bytes("\n<br>" + str(self.client_address), "utf8"))
        self.wfile.write(bytes("\n<br>" + str(urllib.parse.urlsplit(self.path)), "utf8"))
        self.wfile.write(bytes("\n<br>" + str(urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)), "utf8"))
        return

def testclient():
    connection = HTTPConnection(IP + PORT)
    #connection = http.client.HTTPSConnection('google.ee')
    #headers = {'Content-type': 'application/json'}
    connection.request('GET', '/message?param1=val1')
    response = connection.getresponse()
    print(response.read().decode())

def getpeers():
    threading.Timer(5, getpeers).start()
    print('getting peers')

    with urllib.request.urlopen(url) as page:
        mybytes = page.read()
        peers = mybytes.decode("utf8")
        page.close()
        # print(peers)
        peers_obj = json.loads(peers)
        #peers_obj[0] omab ip v''rtust.
        # print(peers_obj[0])

    for x in peers_obj:
        t = x.split(sep=':')
        if t in neighbours:
            pass
        else:
            neighbours.append(t)
    print(neighbours)


def run():
    print('starting server....')
    getpeers()

    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = (IP, PORT)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
#testclient()
#getpeers()