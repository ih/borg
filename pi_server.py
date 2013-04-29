#based http://docs.python.org/2/library/socketserver.html
#this server is run on the raspberry pi and receives info from a client
#hooked up to the mindwave

import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        while self.data != '':
            print "{} wrote:".format(self.client_address[0])
            print self.data
            # just send back the same data, but upper-cased
            self.request.sendall(self.data.upper())
            if self.data != '':
                self.data = self.request.recv(1024).strip()

if __name__ == "__main__":
    #HOST should be the ip address of the raspberry pi
    HOST, PORT = "192.168.0.8", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
