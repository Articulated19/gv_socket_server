# encoding: utf-8

import SocketServer
import numpy as np
import thread
import time

class MyUDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        print data


if __name__ == "__main__":
    HOST, PORT = "192.168.1.111", 2121
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()