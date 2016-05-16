from proto import *
from gevent import socket
from gevent import sleep
import asciify


class Render:

    def __init__(self):
        pass


class Handler(object):
    MESSAGE = 'Lol dude!'

    @classmethod
    def handle(self, conn, info):
        h = Handler(conn, info)
        h.start()
        print 'Dropped', h.info
        return h

    def __init__(self, conn, info):
        self.conn = conn
        self.info = info

    def start(self):
        self.w = 80
        self.h = 25
        self.message = []

        print 'New connection:', self.info

        self.conn.send(Codes.IAC + Codes.WILL + Codes.ECHO)
        self.conn.send(Codes.IAC + Codes.WILL + Codes.SUPPRESS_GO_AHEAD)
        self.conn.send(Codes.IAC + Codes.DO + Codes.NAWS)

        self.conn.send('\033[2J')

        while True:
            socket.wait_read(self.conn.fileno())
            c = self.conn.recv(1)

            if not c:
                return

            if c == Codes.IAC:
                print 'IAC'
                c2 = self.conn.recv(1)
                c2_name = Codes.reverse(c2)
                print c2_name
                if c2_name in ('DO', 'DONT', 'WILL', 'WONT'):
                    c3 = self.conn.recv(1)
                    c3_name = Codes.reverse(c3)
                    print c3_name
                elif c2_name == 'SB':
                    c3 = self.conn.recv(1)
                    c3_name = Codes.reverse(c3)
                    if c3_name == 'NAWS':
                        self.conn.recv(1)
                        self.w = ord(self.conn.recv(1))
                        self.conn.recv(1)
                        self.h = ord(self.conn.recv(1))
                    else:
                        pass
                        # while c3 != Codes.IAC:
                        #     self.conn.recv(1)
                    self.conn.recv(1)
                    self.conn.recv(1)
                    print 'Screen resized: {} x {}'.format(self.w, self.h)

                    # return self.bloat()
            else:
                print 'Byte:', ord(c)
                if c in ('\x0A', '\x0D'):
                    return self.bloat()
                elif c in ('\x08', '\x7F'):
                    if len(self.message):
                        self.message = self.message[:-1]
                        self.conn.send('\033[D \033[D')
                else:
                    self.message.append(c)
                    self.conn.send(c)

    def bloat(self):
        message = ''.join(self.message)
        message = asciify.horizontal(message)
        message = message.split('\n')

        for i, line in enumerate(message):
            message[i] = ' ' * self.w + message[i]

        # print message

        while True:
            try:
                for i, line in enumerate(message):
                    message[i] = message[i][1:] + message[i][0]

                # print '\r\n'.join(message)

                self.conn.send('\033[2J')

                for i, line in enumerate(message):
                    self.conn.send(message[i][0:self.w - 1] + '\r\n')

                # self.conn.send('\033[2J')
                # self.conn.send(message + ' ')
                sleep(0.1)
            except:
                return
