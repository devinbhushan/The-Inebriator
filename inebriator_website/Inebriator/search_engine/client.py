import socket   #for sockets
import sys  #for exit

class Client():
    def connect(self, host_name, port_num):
        try:
            #create an AF_INET, STREAM socket (TCP)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit();

        print 'Socket Created'

        self.host = host_name#'192.168.1.105'
        self.port = port_num

        try:
            self.remote_ip = socket.gethostbyname( self.host )

        except socket.gaierror:
            #could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()

        print 'Ip address of ' + self.host + ' is ' + self.remote_ip

        print 'Socket Connected to ' + self.host + ' on ip ' + self.remote_ip
        #Connect to remote server
        self.s.connect((self.remote_ip , self.port))

    def send(self, message):
        self.s.sendto(message, (self.remote_ip, self.port))
        print "message sent: %s" % message

    def listen(self):
        msg_rec = self.s.recv(1024)
        return msg_rec
