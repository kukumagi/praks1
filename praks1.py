#!/usr/bin/env python

import urllib, urllib.request
import urllib.unquote
import json
import threading
import random

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection

IP = '127.0.0.1'
#IP = '192.168.3.35'
PORT = 1215

laziness = 0.5
url = 'http://192.168.3.11:1215/getpeers'

neighbours = []
route = []

ID = 0
DOWNLOADIP = 1
FILEIP = 2


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "OK"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))

        senderip = self.client_address
        message = urllib.parse.urlsplit(self.path).path
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
        status = ""
        if message in ["/file", "/file/"]:
            try:
                params['id']
                #return
            except:
                status = "Error in parameters"
        else:
            status = "Error"

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

        senderip = self.client_address
        print(senderip[0])
        message = urllib.parse.urlsplit(self.path).path
        status = ""
        if message in ["/download", "/download/"]:
            params = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)

            if random.random() < laziness:
                #download
                print('downloading')
                with urllib.request.urlopen(urllib.unquote(params['url'][0])) as page:
                    mybytes = page.read()
                    data = mybytes.decode("utf8")
                    self.wfile.write(bytes(data, "utf8"))
                    page.close()
            else:
                print('forwarding')
                #forward
                templist = []
                for x in neighbours:
                    if x['IP'] == senderip[0]:
                        pass
                    else:
                        #forward
                        forward(x, params)
                        templist.append(x['IP'])
                temp = { 'ID' : params['id'][0], 'SENDERIP' : senderip, 'FILEIP' : templist }
                #print(temp)
                route.append(temp)
                #print(route[0])
            try:
                params['id']
                params['url']
            except:
                status = "Error in parameters"
        else:
            status = "Error in path"

        self.wfile.write(bytes(status, "utf8"))
        return

def forward(x, params):
    print('Forwarding to ...')
    connection = HTTPConnection(x['IP'] + ':' + x['PORT'])
    print('forward ip:' + x['IP'] + ':' + x['PORT'])
    #print(params['id'][0])
    #connection = http.client.HTTPSConnection('google.ee')
    #headers = {'Content-type': 'application/json'}
    connection.request('GET', '/download?id=' + params['id'][0] + '&url=' + params['url'][0])
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
        temp = {'IP': t[0], 'PORT': t[1]}
        if temp in neighbours:
            pass
        else:
            neighbours.append(temp)
            #neighbours = { 'IP' : t[0], 'PORT' : t[1]}
    print(neighbours)

def genid():
    return random.randint(1, 100000)

def run():
    print('starting server....')

    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = (IP, PORT)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    threading.Thread(target = httpd.serve_forever).start()
    threading.Thread(target = getpeers).start()


run()

# #testclient()
