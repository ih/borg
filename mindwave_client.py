#based http://docs.python.org/2/library/socketserver.html
#this client is run on a computer where the mindwave works and sends
#data to a server on the raspberry pi


import socket
import sys
import time
import mindwave
import pdb
def connect_to_headset(headset):
    while headset.status != 'connected':
        time.sleep(0.5)
        if headset.status == 'standby':
            headset.connect()
            print "Retrying connect..."
        else:
            print "mindwave status: %s" % headset.status
    return


def connect_to_pi():
    #192.168.0.8
    HOST, PORT = '192.168.0.8', 9999

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock




def send_data(sock):
    try:
        # Connect to server and send data
        while True:
            #print i
            data = '%s,%s' % (headset.attention,
                                                   headset.meditation)
            sock.sendall(data + "\n")
            #print data
            # Receive data from the server and shut down
            received = sock.recv(1024)
            print "Sent:     {}".format(data)
            print "Received: {}".format(received)

        # data = 'attention:%s meditation:%s' % (headset.attention,
        #                                        headset.meditation)
        # sock.sendall(data + "\n")
        #     #print data

        # # Receive data from the server and shut down
        # received = sock.recv(1024)
        # print "Sent:     {}".format(data)
        # print "Received: {}".format(received)


    finally:
        sock.close()


if __name__ == '__main__':
    # connect to mindwave
    headset = mindwave.Headset('/dev/tty.MindWave')

    connect_to_headset(headset)
    sock = connect_to_pi()
    send_data(sock)
