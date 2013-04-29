#based http://docs.python.org/2/library/socketserver.html
#this server is run on the raspberry pi and receives info from a client
#hooked up to the mindwave

import SocketServer
import RPi.GPIO as GPIO
import pdb

GREEN_LED = 18
RED_LED = 23

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        def parse_mindwave(data):
            return [int(x) for x in data.split(',')]

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        while self.data != '':
            print "{} wrote:".format(self.client_address[0])
            print self.data
            attention, meditation = parse_mindwave(self.data)
            if attention > 50:
                GPIO.output(RED_LED, True)
                GPIO.output(GREEN_LED, False)
            else:
                GPIO.output(GREEN_LED, True)
                GPIO.output(RED_LED, False)

            # just send back the same data, but upper-cased
            self.request.sendall(self.data.upper())
            if self.data != '':
                self.data = self.request.recv(1024).strip()
        GPIO.output(GREEN_LED, False)
        GPIO.output(RED_LED, False)


def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    GPIO.setup(RED_LED, GPIO.OUT)

if __name__ == "__main__":
    initialize_gpio()

    #HOST should be the ip address of the raspberry pi
    HOST, PORT = "192.168.0.8", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
