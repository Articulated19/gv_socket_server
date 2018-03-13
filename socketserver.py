# encoding: utf-8

import SocketServer
import numpy as np
import thread
import time
import json
import socket

tags = {}
clients = []

class GVClient():

    def __init__(self, ip, tag1, tag2):
        self.ip = ip
        self.tag1 = tag1
        self.tag2 = tag2

class GulliViewTag():

    def __init__(self, id, x, y, cameraId):
        self.id = id
        self.x = x
        self.y = y
        self.cameraId = cameraId

class MyUDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        recv_buf = np.frombuffer(self.request[0], dtype=np.uint8)

        type = recv_buf[0] << 24 | recv_buf[1] << 16 | recv_buf[2] << 8 | recv_buf[3]
        sub_type = recv_buf[4] << 24 | recv_buf[5] << 16 | recv_buf[6] << 8 | recv_buf[7]

        if type == 1 and sub_type == 2:
            len = recv_buf[28] << 24 | recv_buf[29] << 16 | recv_buf[30] << 8 | recv_buf[31]

            for i in range(len):

                base = 32 + (16 * i)

                id = recv_buf[base] << 24 | recv_buf[base+1] << 16 | recv_buf[base+2] << 8 | recv_buf[base+3]
                x = recv_buf[base+4] << 24 | recv_buf[base+4+1] << 16 | recv_buf[base+4+2] << 8 | recv_buf[base+4+3]
                y = recv_buf[base+8] << 24 | recv_buf[base+8+1] << 16 | recv_buf[base+8+2] << 8 | recv_buf[base+8+3]
                c = recv_buf[base+12] << 24 | recv_buf[base+12+1] << 16 | recv_buf[base+12+2] << 8 | recv_buf[base+12+3]

                tags[id] = GulliViewTag(id,x,y,c)

            #print "Tag 1 Id: %d,  x: %d y: %d, id: %d" %  (t,x,y,id)
            #print "Tag 2 Id: %d,  x: %d y: %d id: %d" %  (nt,nx,ny,nid)

        #

        for client in clients:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            gvTag1 = tags[int(client.tag1)]
            gvTag2 = tags[int(client.tag2)]

            data = json.dumps({
                'tagid1': gvTag1.id,
                'x1': gvTag1.x,
                'y1': gvTag1.y,
                'cameraId1': gvTag2.cameraId,
                'tagid2': gvTag2.id,
                'x2': gvTag2.x,
                'y2': gvTag2.y,
                'cameraId2': gvTag2.cameraId,
            })

            sock.sendto(data.encode(), (client.ip, 2121))

def func():
    print "Welcome to the GulliView socket server"
    ip = raw_input("Enter ROS Master Ip: ")
    tagId1 = raw_input("Enter GulliView Tag ID 1: ")
    tagId2 = raw_input("Enter GulliView Tag ID 2: ")
    clients.append(GVClient(ip, tagId1, tagId2))
    raw_input("Press enter to add a another car...")
    func()

if __name__ == "__main__":
    HOST, PORT = "192.168.1.111", 2020
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    try:
        thread.start_new_thread(func, ())
        thread.start_new_thread(server.serve_forever, ())
    except:
        print "Error: unable to start thread"

    while 1:
        pass