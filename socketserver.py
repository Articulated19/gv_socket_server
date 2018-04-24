# encoding: utf-8

import SocketServer
import numpy as np
import thread
import json
import socket
import sys

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

        tags = {}

        len = 0

        # Listening to input from the GV server
        recv_buf = np.frombuffer(self.request[0], dtype=np.uint8)

        # Fetch the type of message from the buffer data
        type = recv_buf[0] << 24 | recv_buf[1] << 16 | recv_buf[2] << 8 | recv_buf[3]
        sub_type = recv_buf[4] << 24 | recv_buf[5] << 16 | recv_buf[6] << 8 | recv_buf[7]

        if type == 1 and sub_type == 2:

            # The number of tags in this message
            len = recv_buf[28] << 24 | recv_buf[29] << 16 | recv_buf[30] << 8 | recv_buf[31]

            # Tag data from the GulliView server is placed in the buffer data
            # from the 32nd bit. A new tag is placed then placed every 16th bit
            for i in range(len):
                base = 32 + (16 * i)

                # Fetching tag id
                id = recv_buf[base] << 24 | recv_buf[base + 1] << 16 | recv_buf[base + 2] << 8 | recv_buf[base + 3] + 3
                #print id
                # X position of tag
                x = recv_buf[base + 4] << 24 | recv_buf[base + 4 + 1] << 16 | recv_buf[base + 4 + 2] << 8 | recv_buf[
                    base + 4 + 3]

                # Y position of tag
                y = recv_buf[base + 8] << 24 | recv_buf[base + 8 + 1] << 16 | recv_buf[base + 8 + 2] << 8 | recv_buf[
                    base + 8 + 3]

                # Camera capturing the tag
                c = recv_buf[base + 12] << 24 | recv_buf[base + 12 + 1] << 16 | recv_buf[base + 12 + 2] << 8 | recv_buf[
                    base + 12 + 3]

                # The current tags in view are added to a list
                tags[id] = GulliViewTag(id, x, y, c)

        # For every connected client to our server
        # we establish a connection to them and feed them data from GV
        for client in clients:

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # We only send data about the tags the client is asking for

            t1 = int(client.tag1)
            t2 = int(client.tag2)

            if t1 in tags and t2 not in tags:
                gvTag1 = tags[t1]
                gvTag2 = GulliViewTag(0, 0, 0, 0)
            elif t1 not in tags and t2 in tags:
                gvTag1 = tags[t2]
                gvTag2 = GulliViewTag(0, 0, 0, 0)

            elif t1 in tags and t2 in tags:
                gvTag1 = tags[t1]
                gvTag2 = tags[t2]

            else:
                continue
            
            data = json.dumps({
                'tagid1': gvTag1.id,
                'x1': gvTag1.x,
                'y1': gvTag1.y,
                'cameraid': gvTag1.cameraId,
                'tagid2': gvTag2.id,
                'x2': gvTag2.x,
                'y2': gvTag2.y
            })

            sock.sendto(data.encode(), (client.ip, 2121))


def func():
    print "Add a new car:"
    ip = raw_input("Enter ROS Master Ip: ")
    tagId1 = raw_input("Enter the back tag ID: ")
    tagId2 = raw_input("Enter the front tag ID: ")
    clients.append(GVClient(ip, tagId1, tagId2))
    raw_input("Press enter to add a another car...")
    func()


if __name__ == "__main__":

    # the user must enter a host IP
    if len(sys.argv) < 2:
        print "Please enter a host ip (this computers ip address on the network)"
        exit(0)
    hostArg = sys.argv[1]

    print "Welcome to the GulliView socket server"

    HOST, PORT = hostArg, 2020
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    try:
        # user input from this thread
        thread.start_new_thread(func, ())

        # capturing gv data from this thread
        thread.start_new_thread(server.serve_forever, ())
    except:
        print "Error: unable to start thread"

    while 1:
        pass
