# encoding: utf-8

import SocketServer
import numpy as np

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        # data = np.n(self.request[0])
        recv_buf = np.frombuffer(self.request[0], dtype=np.uint8)

        type = recv_buf[0] << 24 | recv_buf[1] << 16 | recv_buf[2] << 8 | recv_buf[3]
        sub_type = recv_buf[4] << 24 | recv_buf[5] << 16 | recv_buf[6] << 8 | recv_buf[7]

        if type == 1 and sub_type == 2:
            len = recv_buf[28] << 24 | recv_buf[29] << 16 | recv_buf[30] << 8 | recv_buf[31]

            nid = 0
            nx = 0
            ny = 0
            nt = 0
            id = 0
            x = 0
            y = 0
            t = 0

            print len
            for i in range(len):
                if i == 0:
                    id = recv_buf[32] << 24 | recv_buf[33] << 16 | recv_buf[34] << 8 | recv_buf[35]
                    x = recv_buf[36] << 24 | recv_buf[37] << 16 | recv_buf[38] << 8 | recv_buf[39]
                    y = recv_buf[40] << 24 | recv_buf[41] << 16 | recv_buf[42] << 8 | recv_buf[43]
                    t = recv_buf[44] << 24 | recv_buf[45] << 16 | recv_buf[46] << 8 | recv_buf[47]
                else:
                    nid = recv_buf[48] << 24 | recv_buf[49] << 16 | recv_buf[50] << 8 | recv_buf[51]
                    nx = recv_buf[52] << 24 | recv_buf[53] << 16 | recv_buf[54] << 8 | recv_buf[55]
                    ny = recv_buf[56] << 24 | recv_buf[57] << 16 | recv_buf[58] << 8 | recv_buf[59]
                    nt = recv_buf[60] << 24 | recv_buf[61] << 16 | recv_buf[62] << 8 | recv_buf[63]

            print "Tag 1 Id: %d,  x: %d y: %d, id: %d" %  (t,x,y,id)
            print "Tag 2 Id: %d,  x: %d y: %d id: %d" %  (nt,nx,ny,nid)

        # socket.sendto(data.upper(), ('127.0.0.1', 2121))

if __name__ == "__main__":
    HOST, PORT = "192.168.1.111", 2020
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()